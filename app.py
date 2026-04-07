import streamlit as st
import pickle
import pandas as pd
import requests

# 🔧 Replace with your actual API key
API_KEY = "YOUR_API_KEY"


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5ef13f829f95e5c912b53b2f29d0bc61&language=en-US"
        
        response = requests.get(url, timeout=5)
        data = response.json()

        # ✅ DEBUG (keep this for now)
        print(f"\nMovie ID: {movie_id}")
        print("Response:", data)

        # ❌ Movie not found
        if data.get("status_code") == 34:
            return "https://via.placeholder.com/300x450?text=Not+Found"

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"

        # ❌ No poster available
        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        print("Error:", e)
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommended_movies_poster = []
    recommended_movies = []

    for i in movies_list:
        movie_data = movies.iloc[i[0]]

        # ✅ DEBUG: Check movie + ID
        print("Movie:", movie_data['title'])
        print("Movie ID:", movie_data.get('movie_id'))

        recommended_movies.append(movie_data['title'])
        recommended_movies_poster.append(
            fetch_poster(movie_data['movie_id'])
        )

    return recommended_movies, recommended_movies_poster


# ---------------- STREAMLIT UI ---------------- #

st.title('Movie Recommender System')

similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_list)


selected_movies = st.selectbox(
    'Select any movie below!',
    movies['title'].values
)


if st.button('Recommend'):
    names, poster = recommend(selected_movies)

    # ✅ DEBUG: Check posters list
    print("Poster list:", poster)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])

            # ✅ SAFE IMAGE DISPLAY
            if poster[i] and poster[i].startswith("http"):
                st.image(poster[i])
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image")