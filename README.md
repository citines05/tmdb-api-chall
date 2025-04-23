# TMDB API Challenge

This repository contains the solution to a technical challenge that involves preparing a movie dataset and creating a REST API to consume the processed data.

---

## Project Structure

```bash
tmdb-api-chall/
├── api/                  # FastAPI application (API only reads the database)
│   └── main.py
├── db/                   # Database schema generation and population
│   ├── create_db.py
│   └── movies.db         # Generated SQLite database (ignored in .git)
├── data/                 # Dataset cleaning and preprocessing
│   ├── clean_movies.py
│   └── movies_clean.csv  # Cleaned dataset (ignored in .git)
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Goals

### 1. Dataset Preparation

- Downloaded the [TMDB Movie Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
- Cleaned and preprocessed the data by:
  - Dropping irrelevant or null-heavy columns
  - Filtering duplicates based on movie `id`
  - Converting the `genres` column into a normalized many-to-many structure
- Saved the cleaned dataset to `movies_clean.csv`
- Created a normalized SQLite database using the cleaned dataset

### 2. API Creation

- Developed a RESTful API with FastAPI to expose the data
- Implemented the following endpoints:
  - `GET /` – Health check
  - `GET /movies` – Retrieve up to 100 movies
  - `GET /movies/{id}` – Get details of a specific movie
  - `GET /movies?genre=Action` – Filter movies by genre
  - `GET /genres` – List all available genres
- Responses are serialized using Pydantic models

---

## Technologies Used

- Python 3.10
- FastAPI
- SQLite3
- Pandas
- Docker

---

## Running the Project

### Requirements

- Python 3.10+ (for manual run)
- Or Docker and Docker Compose (for containerized execution)

---

### Option 1: Run manually

```bash
# 1. Clean the raw dataset
python data/clean_movies.py

# 2. Create and populate the SQLite database
python db/create_db.py

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

> The container will clean the data, build the database, and launch the API automatically.

---

## Endpoints Overview

| Method | Endpoint              | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/`                   | Health check                   |
| GET    | `/movies`             | List movies (max 100)          |
| GET    | `/movies/{id}`        | Get movie by ID                |
| GET    | `/movies?genre=Drama` | Filter movies by genre         |
| GET    | `/genres`             | List all genres                |

---

## Database Schema

Three relational tables were created:

- `movies`: Stores metadata about movies
- `genres`: Stores unique genre names
- `movie_genres`: Many-to-many link table between movies and genres

---

## Design Decisions

- **SQLite**: Chosen for its simplicity and zero-dependency setup — ideal for this challenge
- **FastAPI**: Enables fast, type-safe API creation with automatic documentation
- **Docker**: Provides an isolated, reproducible environment for running the full pipeline
- **Modular Structure**: Data cleaning and DB creation are decoupled from the API logic
- **OS-Neutral**: Uses `pathlib` for filesystem operations to support both Windows and Linux
- **Filtering**: Genre filtering is implemented via query parameters to reflect real-world use cases

---

## Limitations

- SQLite is not suitable for concurrent production workloads
- Pagination and advanced querying (e.g., sorting, full-text search) are not yet implemented

---

## Notes

- The `.db` file is not committed to GitHub to keep the repository light and cross-platform
- Scripts for cleaning and database generation are provided and documented for manual testing
- Git LFS is recommended for large dataset handling in future projects

---

## Author

**Caio M. Antunes**

---
