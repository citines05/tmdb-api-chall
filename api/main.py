from fastapi import FastAPI, HTTPException, Query
import sqlite3
from typing import List
from pydantic import BaseModel

app = FastAPI()

db = "db/movies.db"

# 

# Model response for a movie structure

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
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"message": "this api is running"}

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
            LIMIT 100;           
        """, (genre,))
    else:
        cursor.execute("SELECT * FROM movies LIMIT 100")

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie_by_id(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Movie not found, try another ID")
    return dict(row)

@app.get("/genres")
def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genres ORDER BY name;")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
