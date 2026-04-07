# CineScope - Movie Recommender System 🎬

CineScope is a sleek, highly-optimized Movie Recommender web application powered by Machine Learning and Flask. It uses dynamic fetching and beautiful UI cards wrapped in a dark glassmorphism aesthetic.

## Features ✨
- **Machine Learning Engine**: Relies on a pre-trained cosine similarity matrix to accurately recommend similar movie titles.
- **Asynchronous API Processing**: Pulls TMDB & OMDb posters concurrently using a `ThreadPoolExecutor`, eliminating network bottlenecks and vastly increasing load speeds.
- **Resilient Fallback Multi-Threading**: Reconnects on network loss instantly, and intelligently proxies missing posters through a 3-layer TMDB-to-OMDb fallback pipeline to ensure unbroken UI structures.

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/rajashekarg084/MOVIE_RECOMMENDER_SYSTEM.git
cd MOVIE_RECOMMENDER_SYSTEM
```

2. Activate a Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

*(Note: You must extract and place your trained `movies.pkl` and `similarity.pkl` files into the root directory before running! They are ignored by Git due to their massive file size.)*

3. Set up Environment Variables:
Create a `.env` file in the root directory linking your developer API keys securely:
```env
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

4. Run the Application:
```bash
python app_flask.py
```
Open your web browser and navigate to `http://localhost:5000` to interact with the recommender.

## Built With 💻
- **Backend:** Flask, Python
- **Frontend:** Vanilla JS, CSS3 (CSS Grid, Glassmorphism), HTML5
- **Data/Math:** Pandas, Pickle
- **APIs:** TheMovieDatabase (TMDB), Open Movie Database (OMDb)
