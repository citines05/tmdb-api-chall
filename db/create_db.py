import pandas as pd
import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
input_csv = base_dir / "data" / "movies_clean.csv"
output_db = base_dir / "db" / "movies.db"

def create_database_from_df(df: pd.DataFrame, db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Limpa o banco
    cursor.execute("DROP TABLE IF EXISTS movie_genres")
    cursor.execute("DROP TABLE IF EXISTS genres")
    cursor.execute("DROP TABLE IF EXISTS movies")

    # Criação das tabelas
    cursor.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            vote_average REAL,
            vote_count INTEGER,
            status TEXT,
            runtime INTEGER,
            adult BOOLEAN,
            budget INTEGER,
            revenue INTEGER,
            original_language TEXT,
            popularity REAL
        );
    """)
    cursor.execute("""
        CREATE TABLE genres (
            genre_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );
    """)
    cursor.execute("""
        CREATE TABLE movie_genres (
            movie_id INTEGER,
            genre_id INTEGER,
            FOREIGN KEY(movie_id) REFERENCES movies(id),
            FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
        );
    """)

    # movies table
    df_movies = df.drop(columns=["genres"])
    df_movies.to_sql("movies", conn, if_exists="append", index=False)

    # movies_genre association
    genre_id_map = {}
    genre_id_count = 1
    movie_genres_data = []

    for _, row in df.iterrows():
        movie_id = row["id"]
        genres_str = row["genres"].strip('"')
        genres = [g.strip() for g in genres_str.split(",") if g.strip()]

        for genre in genres:
            if genre not in genre_id_map:
                cursor.execute("INSERT INTO genres (genre_id, name) VALUES (?, ?);", (genre_id_count, genre))
                genre_id_map[genre] = genre_id_count
                genre_id_count += 1

            genre_id = genre_id_map[genre]
            movie_genres_data.append((movie_id, genre_id))

    cursor.executemany("INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)", movie_genres_data)

    conn.commit()
    conn.close()
    print(f"Database created at: {db_path}")

if __name__ == "__main__":
    df = pd.read_csv(input_csv)
    create_database_from_df(df, output_db)