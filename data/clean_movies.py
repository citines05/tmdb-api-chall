import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent 
input_path = base_dir / "data" / "TMDB_movie_dataset_v11.csv" # change the dataset name if necessary
output_path = base_dir / "data" / "movies_clean.csv"

# Columns to keep that are usefull
COLUMNS_TO_KEEP = [
    "id", "title", "release_date", "vote_average", "vote_count", "status",
    "runtime", "adult", "budget", "revenue", "original_language", "popularity", "genres"
]

def clean_dataset_from_df(df: pd.DataFrame, columns_to_keep: list = COLUMNS_TO_KEEP) -> pd.DataFrame:
    df_clean = df[columns_to_keep].copy()
    df_clean = df_clean.dropna(subset=['title', 'genres'])
    df_clean = df_clean.drop_duplicates(subset=['id'], keep="first")
    df_clean['release_date'] = pd.to_datetime(df_clean['release_date'], errors='coerce')
    df_clean = df_clean[df_clean['release_date'].notnull()]
    return df_clean

def clean_dataset_from_file(input_path: Path, columns_to_keep: list = COLUMNS_TO_KEEP) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    return clean_dataset_from_df(df, columns_to_keep)

if __name__ == "__main__":
    df_clean = clean_dataset_from_file(input_path)
    df_clean.to_csv(output_path, index=False)
    print(f"Clean dataset saved at: {output_path}")
