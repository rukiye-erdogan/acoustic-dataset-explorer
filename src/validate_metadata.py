from pathlib import Path
import argparse
import sys
import pandas as pd

REQUIRED_COLUMNS = {
    "file_id", "source", "event_type", "category",
    "duration_seconds", "sample_rate", "channels",
    "license", "quality_status",
}

def validate_metadata(csv_path: Path) -> list[str]:
    errors = []
    if not csv_path.exists():
        return [f"File not found: {csv_path}"]
    data = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        errors.append("Missing columns: " + ", ".join(sorted(missing)))
    if data.empty:
        errors.append("Dataset contains no records.")
    if "file_id" in data.columns and data["file_id"].duplicated().any():
        errors.append("Duplicate file_id values detected.")
    for column in ("duration_seconds", "sample_rate", "channels"):
        if column in data.columns:
            values = pd.to_numeric(data[column], errors="coerce")
            if values.isna().any() or (values <= 0).any():
                errors.append(f"Invalid values in {column}.")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    errors = validate_metadata(args.csv_path)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation successful.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
