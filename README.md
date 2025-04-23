# TMDB API project

This repository contains a small backend project that involves preparing a movie dataset and creating a REST API to consume the processed data.

---

## Project Structure

```bash
tmdb-api-chall/
├── api/                  # FastAPI application (API only reads the database)
│   └── main.py
├── data/                 # Dataset cleaning and preprocessing
│   └── clean_movies.py   # Cleaned dataset (ignored in .git)
├── db/                   # Database schema generation and population
│   └── create_db.py      # Generated SQLite database (ignored in .git)
├── notebooks/
│   └── exploratory_analysis.ipynb # Prototype notebook for the dataset cleaning logic used in clean_movies.py."
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Technologies Used

- Python 3.11
- FastAPI
- SQLite3
- Pandas
- Docker

---

## Goals

### 1. Dataset Preparation

- Downloaded the [TMDB Movie Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
- Cleaned and preprocessed the data by:
  - **Dropping irrelevant or null-heavy columns**: columns such as `homepage`, `tagline`, `poster_path`, `keywords`, and others were removed due to being either irrelevant to the project scope or having excessive missing data.
  - **Filtering duplicates based on movie `id`**: the dataset was checked for duplicate entries based on the `id` field. Only the first occurrence was retained to ensure primary key uniqueness in the database.
  - **Converting the `genres` column into a normalized many-to-many structure**: the `genres` column originally held comma-separated values as strings (e.g., `"Action, Comedy"`). This was split into individual genres, added to a separate `genres` table, and connected to movies using a `movie_genres` many-to-many relationship table.
- Saved the cleaned dataset to `movies_clean.csv`
- Created a normalized SQLite database using the cleaned dataset

### 2. Database Schema

Three relational tables were created:

- `movies`: stores metadata about movies
- `genres`: stores unique genre names
- `movie_genres`: many-to-many link table between movies and genres

---

### 3. API Creation

- Developed a RESTful API with FastAPI to expose the data
- Implemented the following endpoints:
  - `GET /` – Health check
  - `GET /movies` – Retrieve up to 100 movies
  - `GET /movies/{id}` – Get details of a specific movie
  - `GET /movies?genre=Action` – Filter movies by genre
  - `GET /genres` – List all available genres
- Responses are serialized using Pydantic models

---

### 4. Design Decisions

- **SQLite**: chosen as the database engine for its lightweight, serverless architecture, which requires no setup beyond including the .db file.
- **FastAPI**: selected for its modern, high-performance capabilities for building APIs with Python.
- **Docker**: used to ensure the entire application runs inside a reproducible and isolated container.
- **Modular Structure**: data cleaning and DB creation are decoupled from the API logic, wich means it improves maintainability, simplifies testing, and allows each component to be reused independently.
- **OS-Neutral**: all file and path operations use the pathlib library instead of OS-dependent strings. This ensures full compatibility across operating systems (Linux, macOS, Windows) and avoids common path errors.

---

## Running the Project

### Requirements

- Python 3.10+ (for manual run)
- Pandas, FastAPI, Uvicorn (listed in `requirements.txt`).
  Note: if you don’t have the required packages installed, run the following command:

  ```bash
  pip install --no-cache-dir -r requirements.txt  # Use 'pip3' if needed
  ```

- Or Docker and Docker Compose (for containerized execution)

---

1. **Clone this repository**  

   ```bash
   git clone https://github.com/citines05/tmdb-api-chall.git
   cd tmdb-api-chall
   ```

2. **Download the dataset**  
   Go to [TMDB Movie Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) and download the ZIP file. Then, move it into the `data/` directory of the cloned repository. The `clean_movies.py` script will automatically extract the contents and process the CSV file.

3. **You can now run the project using one of the following options:**

### Option 1: Run manually

```bash
# 1. Clean the raw dataset
python data/clean_movies.py # use 'python3' on Linux if needed

# 2. Create and populate the SQLite database
python db/create_db.py # use 'python3' on Linux if needed

# 3. Start the API
uvicorn api.main:app --reload
```

Visit:

- API root: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Run with Docker

```bash
docker-compose up --build
```

> The container will clean the data, build the database and launch the API automatically.

---

## Notes

- The `.db` file is not committed to GitHub to keep the repository light and cross-platform
- Scripts for cleaning and database generation are provided and documented for manual testing

---

## Author

- **Caio M. Antunes**
