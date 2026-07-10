from pathlib import Path
from src.validate_metadata import validate_metadata

def test_sample_metadata_is_valid():
    assert validate_metadata(Path("data/sample/sample_metadata.csv")) == []
