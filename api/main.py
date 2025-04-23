from fastapi import FastAPI, HTTPException, Query
import sqlite3
from typing import List
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "db" / "movies.db"

# Pydantic model used to define the response schema for a movie
class Movie(BaseModel):
    id: int
    title: str
    release_date: str
    vote_average: float
    vote_count: int
    status: str
    runtime: int
    adult: bool
    budget: int
    revenue: int
    original_language: str
    popularity: float

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Test get
@app.get("/")
def root():
    return {"message": "This API is running"}

# Retrieve the top 100 movies ordered by ID, optionally filtered by genre
@app.get("/movies", response_model=List[Movie])
def get_movies(genre: str = Query(None, description="Filter by genre name")):
    conn = get_db_connection()
    cursor = conn.cursor()
    if genre:
        cursor.execute("""
            SELECT m.* FROM movies m
            JOIN movie_genres mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            WHERE g.name = ?
            ORDER BY m.id
            LIMIT 100;
        """, (genre,))
    else:
        cursor.execute("SELECT * FROM movies LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Retrieve a specific movie by its ID
@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie_by_id(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return dict(row)

# Get all genres ordered by ID
@app.get("/genres")
def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genres ORDER BY genre_id;")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
