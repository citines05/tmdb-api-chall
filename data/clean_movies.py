import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent 
input_path = base_dir / "data" / "TMDB_movie_dataset_v11.csv"  # Change the dataset name if necessary
output_path = base_dir / "data" / "movies_clean.csv"

# Columns to keep that are useful for the API and database
COLUMNS_TO_KEEP = [
    "id", "title", "release_date", "vote_average", "vote_count", "status",
    "runtime", "adult", "budget", "revenue", "original_language", "popularity", "genres"
]

# Cleans and filters the dataset from a DataFrame
def clean_dataset_from_df(df: pd.DataFrame, columns_to_keep: list = COLUMNS_TO_KEEP) -> pd.DataFrame:
    df_clean = df[columns_to_keep].copy()
    # Remove rows with missing 'title' or 'genres'
    df_clean = df_clean.dropna(subset=['title', 'genres'])
    # Remove duplicate rows based on 'id'
    df_clean = df_clean.drop_duplicates(subset=['id'], keep="first")
    # Convert 'release_date' to datetime format
    df_clean['release_date'] = pd.to_datetime(df_clean['release_date'], errors='coerce')
    # Keep only rows with valid release dates
    df_clean = df_clean[df_clean['release_date'].notnull()]
    return df_clean

# Loads and cleans the dataset from a CSV file
def clean_dataset_from_file(input_path: Path, columns_to_keep: list = COLUMNS_TO_KEEP) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    # Apply cleaning logic
    return clean_dataset_from_df(df, columns_to_keep)

if __name__ == "__main__":
    df_clean = clean_dataset_from_file(input_path)
    df_clean.to_csv(output_path, index=False)
    print(f"Clean dataset saved at: {output_path}")