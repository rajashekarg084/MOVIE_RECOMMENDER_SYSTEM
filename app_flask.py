import os
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

app = Flask(__name__)

# API Keys
API_KEY = os.getenv("TMDB_API_KEY", "YOUR_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")

# Configure Session with Retries to prevent ConnectionResetError (10054)
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry, pool_connections=15, pool_maxsize=15)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Load data at startup into memory
print("Loading similarity matrix and movies list...")
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_list = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movie_list)
    movie_titles = movies['title'].values.tolist()
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    similarity = None
    movies = None
    movie_titles = []

def fetch_poster(task_data):
    """Fetches poster from TMDB ID, fallback to TMDB Search, fallback to OMDB."""
    movie_id, movie_title = task_data
    
    # 1. Try TMDB via Direct ID
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        print(f"TMDB ID error for {movie_title}: {e}")

    # 2. Try TMDB Title Search Fallback (Extremely reliable for mismatched IDs)
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}&language=en-US"
        search_res = session.get(search_url, timeout=5)
        if search_res.status_code == 200:
            search_data = search_res.json()
            if search_data.get("results") and len(search_data["results"]) > 0:
                fallback_poster_path = search_data["results"][0].get("poster_path")
                if fallback_poster_path:
                    return f"https://image.tmdb.org/t/p/w500/{fallback_poster_path}"
    except Exception as e:
        print(f"TMDB Search error for {movie_title}: {e}")

    # 3. If everything TMDB fails, use OMDB Fallback
    OMDB_KEY = os.getenv("OMDB_API_KEY", "")
    if OMDB_KEY and OMDB_KEY != "your_omdb_key_here":
        try:
            omdb_url = "http://www.omdbapi.com/"
            omdb_res = session.get(omdb_url, params={"t": movie_title, "apikey": OMDB_KEY}, timeout=5)
            if omdb_res.status_code == 200:
                omdb_data = omdb_res.json()
                omdb_poster = omdb_data.get("Poster")
                if omdb_poster and omdb_poster != "N/A":
                    return omdb_poster
        except Exception as e:
            print(f"OMDB error for {movie_title}: {e}")

    # 4. Final Fallback placeholder
    return "https://via.placeholder.com/300x450?text=No+Poster"

def get_recommendations_logic(movie_name):
    """Pure logic to get distance indices and map to dictionaries."""
    if movies is None or similarity is None:
        return []
    
    if movie_name not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    # Get top 10 similar
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommendations = []
    
    # Store IDs and names sequentially so it matches threading correctly
    movie_tasks = []
    for i in movies_list:
        movie_data = movies.iloc[i[0]]
        movie_tasks.append((movie_data['movie_id'], movie_data['title']))
        recommendations.append({
            "title": movie_data['title'],
            "poster": None # to be populated
        })

    # Threading for huge speedup compared to synchronous Streamlit version
    with ThreadPoolExecutor(max_workers=10) as executor:
        posters = list(executor.map(fetch_poster, movie_tasks))

    # Add back the pulled posters
    for i, p in enumerate(posters):
        recommendations[i]["poster"] = p
        
    return recommendations

@app.route('/')
def home():
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_name = data.get('movie')

    if not movie_name:
        return jsonify({"error": "No movie provided"}), 400

    results = get_recommendations_logic(movie_name)
    
    if not results:
        return jsonify({"error": "Movie not found or failed to load recommendations"}), 404

    return jsonify({"recommendations": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
