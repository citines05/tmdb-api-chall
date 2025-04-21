# TMDB API Challenge

This repository contains the solution to a technical challenge that involves preparing a movie dataset and creating an API to consume the processed data.

## Project Structure

```bash
tmdb-api-chall/
├── api/                  # FastAPI application
│   └── main.py
├── db/                   # Database creation scripts and SQLite database
│   ├── clean_movies.py
│   ├── create_db.py
│   └── movies.db
├── data/                 # Processed dataset
│   ├── movies_clean.csv
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Goals

### 1. Dataset Preparation

- Downloaded the [TMDB Movie Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies).
- Analyzed and cleaned the dataset by removing irrelevant or null-heavy columns.
- Filtered duplicates by movie `id`.
- Normalized the genres column into a relational schema with a many-to-many relationship.
- Saved the cleaned data in `movies_clean.csv`.
- Created the database schema using SQLite.

### 2. API Creation

- Developed a RESTful API using FastAPI.
- Created endpoints to serve data from the database:
  - `GET /` - Health check
  - `GET /movies` - List all movies (limit 100 by default)
  - `GET /movies/{id}` - Retrieve a movie by its ID
  - `GET /movies?genre=Action` - Filter movies by genre
  - `GET /genres` - List all unique genres
- Used Pydantic models for response serialization and validation.

## Technologies Used

- Python 3.10
- FastAPI
- SQLite3
- Pandas
- Docker & Docker Compose

## How to Run the Project

### Prerequisites

- Docker and Docker Compose installed

### 1. Clone the repository

```bash
git clone https://github.com/citines05/tmdb-api-chall.git
cd tmdb-api-chall
```

### 2. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 3. Access the API

- API Base URL: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints Overview

| Method | Endpoint              | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/`                   | Health check                   |
| GET    | `/movies`             | List movies (limit 100)        |
| GET    | `/movies/{id}`        | Get movie by ID                |
| GET    | `/movies?genre=Drama` | Filter movies by genre         |
| GET    | `/genres`             | List all genres                |

## Database Schema

Three tables were created:

- `movies`: stores general movie information
- `genres`: stores unique genre names
- `movie_genres`: intermediary table for many-to-many relation

## Project Decisions and Justification

- **SQLite**: Chosen for simplicity, local use, and fast prototyping. Ideal for lightweight API scenarios.
- **FastAPI**: Modern, fast, and self-documented. Swagger UI is automatically available.
- **Docker**: Provides an isolated and reproducible environment. Makes project easily testable.
- **Modular Design**: Scripts are organized into data cleaning and DB creation.
- **Filtering**: Genre filtering was implemented as query parameters to demonstrate real-world use cases.

## Limitations

- SQLite is not suitable for production with concurrent access.
- Pagination and sorting were not implemented but can be added.

## Notes

- The `movies.db` file is approximately 66 MB. Although this exceeds GitHub's 50 MB recommendation, it is necessary for testing and is included in the repository.
- Git LFS is recommended for handling large files in future projects.

## Author

Caio M. Antunes

---

For any questions, please contact: [your-email@example.com]
