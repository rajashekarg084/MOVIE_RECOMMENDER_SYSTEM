# 🎬 CineScope — Movie Recommender System

CineScope is a sleek, high-performance **Movie Recommender Web Application** powered by **Machine Learning** and built using **Flask**. It delivers fast, accurate movie recommendations with a visually appealing **dark glassmorphism UI**.

---

## 🚀 Features

✨ **Machine Learning Engine**

* Uses a pre-trained **cosine similarity matrix** to recommend movies based on user selection.

⚡ **Asynchronous API Processing**

* Fetches movie posters from **TMDB** and **OMDb** using multi-threading (`ThreadPoolExecutor`) for faster response times.

🛡️ **Resilient Fallback System**

* 3-layer fallback pipeline:

  * TMDB → OMDb → Placeholder
* Ensures **no broken UI elements**, even during API failures.

🎨 **Modern UI/UX**

* Glassmorphism design
* Responsive movie cards
* Smooth and clean user interaction

## 🏗️ Tech Stack

**Backend**

* Flask (Python)

**Frontend**

* HTML5
* CSS3 (Glassmorphism, Grid)
* Vanilla JavaScript

**Data & ML**

* Pandas
* Pickle (Pre-trained model)

**APIs**

* TMDB (The Movie Database)
* OMDb (Open Movie Database)

---

## 📦 Important: Required Model Files

This project depends on two pre-trained files:

* `movies.pkl`
* `similarity.pkl`

⚠️ These files are **NOT included** in this repository due to their large size.

---

### 📁 Place Files Like This

```
MOVIE_RECOMMENDER_SYSTEM/
│── app_flask.py
│── movies.pkl
│── similarity.pkl
│── templates/
│── static/
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rajashekarg084/MOVIE_RECOMMENDER_SYSTEM.git
cd MOVIE_RECOMMENDER_SYSTEM
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Windows**

```bash
venv\Scripts\activate
```

* **Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file in the root directory:

```
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

---

### 5️⃣ Run the Application

```bash
python app_flask.py
```

---

### 🌐 Open in Browser

```
http://localhost:5000
```

---

## 🧠 How It Works

1. User selects a movie
2. System finds similar movies using **cosine similarity**
3. Fetches posters via APIs
4. Displays recommendations in a clean UI

---

## 📌 Future Improvements

* 🔍 Search autocomplete
* 🎯 Personalized recommendations
* 🧾 Movie details page
* ☁️ Deployment (Render / AWS / Vercel backend)
* 📊 User analytics dashboard

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* TMDB API
* OMDb API
* Open-source ML community

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🧠 Share ideas

---

**Built with passion by Rajashekar G 🚀**
