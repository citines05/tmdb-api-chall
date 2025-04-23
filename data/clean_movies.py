import pandas as pd
from pathlib import Path
import zipfile

# Base paths
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "data"
output_path = data_dir / "movies_clean.csv"

# Columns to keep that are useful for the API and database
COLUMNS_TO_KEEP = [
    "id", "title", "release_date", "vote_average", "vote_count", "status",
    "runtime", "adult", "budget", "revenue", "original_language", "popularity", "genres"
]

# Extracts the first found ZIP in the data directory if it contains any raw CSV not yet extracted.
def extract_zip_if_needed(data_dir: Path) -> None:
    zip_files = list(data_dir.glob("*.zip"))
    if not zip_files:
        raise FileNotFoundError("No ZIP file found in the 'data/' directory.")

    zip_path = zip_files[0]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Avoids false positives by excluding already cleaned CSV files
        csv_inside_zip = [f for f in zip_ref.namelist() if f.endswith(".csv") and "clean" not in f.lower()]
        for f in csv_inside_zip:
            extracted_path = data_dir / Path(f).name
            if not extracted_path.exists():
                zip_ref.extract(f, path=data_dir)
                print(f"Extracted {f} from {zip_path.name}")

# Finds the first raw CSV file in the data directory, excluding any already cleaned CSVs.
def find_raw_csv(data_dir: Path) -> Path:
    csv_candidates = [f for f in data_dir.glob("*.csv") if "clean" not in f.name.lower()]
    if not csv_candidates:
        raise FileNotFoundError("No raw CSV file found in the 'data/' directory.")
    return csv_candidates[0]

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
    return clean_dataset_from_df(df, columns_to_keep)

if __name__ == "__main__":
    # Dataset extraction
    extract_zip_if_needed(data_dir)
    input_path = find_raw_csv(data_dir)

    # Dataset cleaning
    df_clean = clean_dataset_from_file(input_path)
    df_clean.to_csv(output_path, index=False)
    print(f"Clean dataset saved at: {output_path}")