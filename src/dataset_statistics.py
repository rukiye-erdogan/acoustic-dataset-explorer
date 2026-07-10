from pathlib import Path
import argparse
import pandas as pd

def create_statistics(csv_path: Path) -> None:
    data = pd.read_csv(csv_path)
    print("Acoustic Dataset Summary")
    print("=" * 26)
    print(f"Records: {len(data)}")
    print(f"Sources: {data['source'].nunique()}")
    print(f"Event types: {data['event_type'].nunique()}")
    print(f"Categories: {data['category'].nunique()}")
    print(f"Total duration: {data['duration_seconds'].sum():.2f} seconds")
    print("\nRecords by category")
    print(data["category"].value_counts().to_string())

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    create_statistics(args.csv_path)

if __name__ == "__main__":
    main()
