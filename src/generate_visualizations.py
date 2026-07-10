from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample" / "sample_metadata.csv"
ASSETS_DIR = ROOT / "assets"


def save_category_distribution(data: pd.DataFrame) -> None:
    counts = data["category"].value_counts().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind="barh", ax=ax)
    ax.set_title("Acoustic Metadata Records by Category")
    ax.set_xlabel("Record count")
    ax.set_ylabel("Category")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "category_distribution.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_quality_status(data: pd.DataFrame) -> None:
    counts = data["quality_status"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    counts.plot(kind="pie", autopct="%1.0f%%", startangle=90, ax=ax)
    ax.set_title("Metadata Quality Status")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "quality_status.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA_PATH)

    save_category_distribution(data)
    save_quality_status(data)

    print("Created:")
    print(ASSETS_DIR / "category_distribution.png")
    print(ASSETS_DIR / "quality_status.png")


if __name__ == "__main__":
    main()
