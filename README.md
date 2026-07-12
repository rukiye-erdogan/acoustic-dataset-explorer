# Acoustic Dataset Explorer

Interactive Streamlit dashboard for exploring and analysing acoustic metadata from Freesound and ZapSplat.

## Dashboard features

- Category distribution
- Total audio-file count
- Event-type statistics
- Source comparison
- URL availability monitoring
- Metadata preview with source links
- URL export
- Source-distribution visualisation

## Dataset snapshot

- 2,613 metadata records
- 504 event types
- 7 categories
- 2 metadata sources
- 100% source-URL availability

## Data sources

- Freesound
- ZapSplat

This repository contains metadata and source references only. It does not redistribute third-party audio files.

## Project structure

```text
acoustic-dataset-explorer/
├── .streamlit/
│   └── config.toml
├── data/
│   └── public/
│       ├── acoustic_metadata.db
│       └── acoustic_metadata_public.csv
├── app.py
├── import_to_postgres.py
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

## Run locally

```bash
git clone https://github.com/rukiye-erdogan/acoustic-dataset-explorer.git
cd acoustic-dataset-explorer
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open `http://localhost:8501`.

## Technologies

- Python
- Streamlit
- pandas
- Plotly
- SQLite
- PostgreSQL
- Git and GitHub

## Licence

The source code is licensed under the MIT License.
