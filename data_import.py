import polars as pl

from pathlib import Path

app_dir = Path(__file__).parent

csv_path = app_dir / "data/penguins.csv"

df = pl.read_csv(csv_path)
