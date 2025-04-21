import pandas as pd
import sqlite3
import os

movies_csv = 'data/movies_clean.csv'
db = 'db/movies.db'

def create_database(movie_path, db_path):
    print("Database creation started...")

    df = pd.read_csv(movie_path)

    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Cleans the database
    cursor.execute('DROP TABLE IF EXISTS movie_genres')
    cursor.execute('DROP TABLE IF EXISTS genres')
    cursor.execute('DROP TABLE IF EXISTS movies')

    # Table movies creation
    print("Creating the tables...")
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

    # Table genres creation
    cursor.execute("""
        CREATE TABLE genres (
            genre_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );
    """)
    
    # Table movie_genres creation (N:N)
    cursor.execute("""
        CREATE TABLE movie_genres (
            movie_id INTEGER,
            genre_id INTEGER,
            FOREIGN KEY(movie_id) REFERENCES movies(id),
            FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
        );
    """)

    # Inserting movies in the movies table
    print("Populating the database...")
    df_movies = df.drop(columns=['genres'])
    df_movies.to_sql('movies', conn, if_exists='append', index=False)

    # Inserting unique genres in the genre table
    genre_id_map = {}
    genre_id_count = 1
    movie_genres_data = []

    for _,row in df.iterrows():
        movie_id = row['id']
        genres_str = row['genres'].strip('"')
        genres = [g.strip() for g in genres_str.split(",") if g.strip()]

        for genre in genres:
            if genre not in genre_id_map:
                # Insert into genres table
                cursor.execute("INSERT INTO genres (genre_id, name) VALUES (?, ?);", (genre_id_count, genre))
                genre_id_map[genre] = genre_id_count
                genre_id_count += 1
            
            genre_id = genre_id_map[genre]
            movie_genres_data.append((movie_id, genre_id))
    
    # Inserting movie-genre in movie_genres
    cursor.executemany("INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)", movie_genres_data)

    conn.commit()
    conn.close()

    print(f'Database successfully created in {db_path}')
    return

if __name__ == "__main__":
    create_database(movie_path=movies_csv, db_path=db)