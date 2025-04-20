import pandas as pd
import os

# Paths
data_in = 'data/TMDB_movie_dataset_v11.csv'
data_out = 'data/movies_clean.csv'

# Relevant columns
columns_to_keep = ["id", "title", "release_date", "vote_average", "vote_count", "status",
    "runtime", "adult", "budget", "revenue", "original_language", "popularity", "genres"
]

# Function to clear the dataset
def clean_dataset(data_in, data_out, col_to_keep):
    df = pd.read_csv(data_in)

    df_clean = df[col_to_keep].copy()

    # Removes movies without title or genre and possible duplicates
    df_clean = df_clean.dropna(subset=['title', 'genres'])
    df_clean = df_clean.drop_duplicates(subset=['id'], keep="first")

    # Convert date from string to datetime
    df_clean['release_date'] = pd.to_datetime(df_clean['release_date'], errors='coerce')
    # Filters the release_date to drop nulls
    df_clean = df_clean[df_clean['release_date'].notnull()]
    
    df_clean.to_csv(data_out, index=False)

    print(f'Dataset saved at: {data_out}')

    return

if __name__ == '__main__':
    clean_dataset(data_in, data_out, columns_to_keep)