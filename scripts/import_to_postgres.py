import sqlite3

import pandas as pd
from sqlalchemy import create_engine, text

SQLITE_PATH = "data/public/acoustic_metadata.db"
POSTGRES_URL = (
    "postgresql+psycopg2://metabase:metabase123"
    "@localhost:5432/acoustic_dataset"
)

with sqlite3.connect(SQLITE_PATH) as sqlite_connection:
    dataframe = pd.read_sql_query(
        "SELECT * FROM acoustic_metadata",
        sqlite_connection,
    )

engine = create_engine(POSTGRES_URL)

dataframe.to_sql(
    "acoustic_metadata",
    engine,
    schema="public",
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=500,
)

with engine.connect() as connection:
    imported_rows = connection.execute(
        text("SELECT COUNT(*) FROM public.acoustic_metadata")
    ).scalar_one()

print("POSTGRES IMPORT COMPLETED")
print("=" * 40)
print(f"Rows loaded from SQLite: {len(dataframe):,}")
print(f"Rows stored in PostgreSQL: {imported_rows:,}")
print(f"Columns: {len(dataframe.columns)}")
print("Table: public.acoustic_metadata")
