from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Acoustic Dataset Explorer",
    page_icon="🎵",
    layout="wide",
)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DATABASE_PATH = Path("data/public/acoustic_metadata.db")
TABLE_NAME = "acoustic_metadata"


# ---------------------------------------------------------
# Category metadata
# ---------------------------------------------------------

CATEGORY_DESCRIPTIONS = {
    "environment": "Environmental sounds, nature, weather, cities and everyday life",
    "damage_related": "Damage, breaks, impacts and vandalism-related sounds",
    "vehicle": "Vehicles, engines, driving sounds, doors and tyres",
    "synthetic_electronic": "Electronic sounds, signals, devices and effects",
    "mechanical_contact": "Friction, scratching, grinding and metal contact",
    "air_leak": "Air release, hissing, escaping pressure, valves and leaks",
    "music": "Music, voices, singing and instruments",
}

CATEGORY_ORDER = [
    "environment",
    "damage_related",
    "vehicle",
    "synthetic_electronic",
    "mechanical_contact",
    "air_leak",
    "music",
]

CATEGORY_COLORS = {
    "environment": "#B9DFAE",
    "damage_related": "#F7AAA7",
    "vehicle": "#A7CDEB",
    "synthetic_electronic": "#D9B3E5",
    "mechanical_contact": "#F4D17D",
    "air_leak": "#9ED7D4",
    "music": "#F2AE7E",
}


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH.resolve()}"
        )

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(
            f"SELECT * FROM {TABLE_NAME}",
            connection,
        )

    return dataframe


try:
    df = load_data()
except Exception as error:
    st.error(f"Could not load the acoustic dataset: {error}")
    st.stop()


# ---------------------------------------------------------
# Data preparation
# ---------------------------------------------------------

required_columns = {
    "file_name",
    "category",
    "event_type",
    "source",
    "source_url",
}

missing_columns = required_columns.difference(df.columns)

if missing_columns:
    st.error(
        "The following required columns are missing: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()


df["category"] = df["category"].fillna("unknown").astype(str)
df["event_type"] = df["event_type"].fillna("unknown").astype(str)
df["source"] = df["source"].fillna("Unknown").astype(str)
df["source_url"] = df["source_url"].fillna("").astype(str)

total_files = len(df)
total_categories = df["category"].nunique()
total_event_types = df["event_type"].nunique()
total_sources = df["source"].nunique()

valid_url_mask = df["source_url"].str.strip().ne("")
url_percentage = (
    valid_url_mask.mean() * 100
    if total_files > 0
    else 0
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

.url-heading {
    margin-top: 26px;
    margin-bottom: 6px;
    font-size: 1.35rem;
    font-weight: 700;
    color: #30493b;
}

 url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght;400;500;600;700&display=swap");


.stDataFrame {

    background: rgba(255,255,255,0.92) !important;

    border-radius: 14px !important;

}



.stDataFrame table {

    background: #ffffff !important;

    color: #24372e !important;

}



.stDataFrame thead tr th {

    background: #edf5ef !important;

    color: #30493b !important;

    font-weight: 700 !important;

}



.stDataFrame tbody tr:nth-child(even) {

    background: #f8fbf8 !important;

}




html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: "IBM Plex Sans","Segoe UI","Helvetica Neue",Arial,sans-serif !important;
}


html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: "IBM Plex Sans","Segoe UI","Helvetica Neue",Arial,sans-serif !important;
}


    .stApp{
        background:
            radial-gradient(circle at top left, #fffefb 0%, #f7f4ed 48%, #f1eee6 100%);
            color: #24372e;
        }

        .block-container {
            max-width: none !important;
            width: 100% !important;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
            padding-top: 3.8rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            color: #30493b;
            letter-spacing: -0.02em;
        }

        .section-heading {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 2px;
        }

        .section-icon {
            font-size: 42px;
            line-height: 1;
        }

        .section-title {
            font-size: 34px;
            font-weight: 900;
            color: #30493b;
            line-height: 1.1;
        }

        .section-subtitle {
            font-size: 17px;
            color: #59635d;
            margin-top: 6px;
            margin-bottom: 18px;
        }

        .panel {
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid rgba(120, 110, 90, 0.16);
            border-radius: 15px;
            padding: 18px;
            box-shadow: 0 5px 18px rgba(80, 70, 50, 0.07);
        }

        .kpi-card {
            min-height: 118px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(115, 105, 85, 0.18);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow: 0 10px 26px rgba(60,55,45,.12);
            position: relative;
        }

        .kpi-value {
            font-size: 36px;
            font-weight: 750;
            line-height: 1.05;
        }

        .kpi-label {
            font-size:15px;
            font-weight: 650;
            color: #35433d;
            margin-top: 12px;
        }

        .kpi-icon {
            position: absolute;
            right: 16px;
            top: 24px;
            font-size: 35px;
            opacity: 0.82;
        }

        .category-count-card {
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(120,110,90,0.17);
            border-radius: 14px;
            padding: 13px 23px;
            text-align: center;
            min-width: 110px;
            box-shadow: 0 5px 15px rgba(80,70,50,0.06);
        }

        .category-count-number {
            font-size: 28px;
            font-weight: 750;
            color: #30493b;
        }

        .category-count-label {
            font-size:15px;
            margin-top: 4px;
        }

        div[data-testid="stDataFrame"] {
            background: rgba(255,255,255,0.75);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(120,110,90,0.14);
        }

        div.stDownloadButton > button {
            border-radius: 10px;
            border: 1px solid rgba(100,90,70,0.24);
            background-color: rgba(255,255,255,0.78);
        }

        footer {
            visibility: hidden;
        }

        #MainMenu {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Main layout
# ---------------------------------------------------------

left_column, right_column = st.columns(
    [1.0, 1.0],
    gap="large",
)


# =========================================================
# LEFT SIDE — CATEGORY OVERVIEW
# =========================================================

with left_column:
    header_column, count_column = st.columns(
        [5.2, 1],
        vertical_alignment="top",
    )

    with header_column:
        st.markdown(
            """
            <div class="section-heading">
                <div class="section-icon">📚</div>
                <div class="section-title">1. Category Overview</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="section-subtitle">
                Total: {total_files:,} audio files
            </div>
            """,
            unsafe_allow_html=True,
        )

    with count_column:
        st.markdown(
            f"""
            <div class="category-count-card">
                <div class="category-count-number">{total_categories}</div>
                <div class="category-count-label">Categories</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    category_counts = (
        df.groupby("category", dropna=False)
        .size()
        .reset_index(name="count")
    )

    category_counts["category"] = pd.Categorical(
        category_counts["category"],
        categories=CATEGORY_ORDER,
        ordered=True,
    )

    category_counts = (
        category_counts
        .sort_values("category")
        .dropna(subset=["category"])
    )

    category_counts["share"] = (
        category_counts["count"] / total_files * 100
    )

    category_counts["description"] = (
        category_counts["category"]
        .astype(str)
        .map(CATEGORY_DESCRIPTIONS)
        .fillna("Other acoustic category")
    )

    category_counts = category_counts.sort_values("count", ascending=True)

    category_figure = px.bar(
        category_counts,
        x="count",
        y="category",
        orientation="h",
        text="count",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        labels={
            "category": "Category",
            "count": "Number of Audio Files",
        },
    )

    category_figure.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        textfont=dict(size=22),
        marker_line_width=0,
        hovertemplate=(
            "<b>Category:</b>&nbsp;&nbsp;&nbsp;&nbsp;%{y}<br>"
            "<b>Audio Files:</b>&nbsp;%{x:,.0f}"
            "<extra></extra>"
        ),
    )

    category_figure.update_layout(
        hoverlabel=dict(
            bgcolor="#fffefb",
            bordercolor="#aeb5af",
            align="left",
            font=dict(
                family="Menlo, Monaco, Courier New, monospace",
                size=15,
                color="#30493b",
            ),
        ),
        width=980,
        
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=115, r=115, t=10, b=80),
        font=dict(
            family="IBM Plex Sans",
            size=15,
            color="#202622",
        ),
        xaxis=dict(
            title="Audio Files",
            type="log",
            range=[1, 3.75],
            tickvals=[10, 30, 100, 300, 1000, 3000],
            ticktext=["10", "30", "100", "300", "1,000", "3,000"],
            tickfont=dict(size=16, color="#30493b"),
            title_font=dict(size=17, color="#30493b"),
            showgrid=True,
            gridcolor="rgba(90,90,90,0.10)",
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            autorange="reversed",
            tickfont=dict(size=16, color="#30493b"),
        ),
    )

    with st.container(border=False):
        st.plotly_chart(
            category_figure,
            width="stretch",
            config={"displayModeBar": False},
        )

        category_table = category_counts[
            ["category", "description", "count", "share"]
        ].copy()

        category_table.columns = [
            "Category",
            "Description",
            "Count",
            "Share",
        ]

        category_table["Category"] = (
            category_table["Category"].astype(str)
        )

        category_table["Count"] = category_table["Count"].map(
            lambda value: f"{int(value):,}"
        )

        category_table["Share"] = category_table["Share"].map(
            lambda value: f"{float(value):.1f}%"
        )

        st.dataframe(
            category_table,
            hide_index=True,
            use_container_width=True,
            
            width="stretch",
        )


# =========================================================
# RIGHT SIDE — FILES AND SOURCES OVERVIEW
# =========================================================

with right_column:
    st.markdown(
        """
        <div class="section-heading">
            <div class="section-icon">🔗</div>
            <div class="section-title">2. Files &amp; Sources Overview</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Sample overview of audio files and their sources
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(4, gap="medium")

    metric_definitions = [
        {
            "value": f"{total_files:,}",
            "label": "Total Files",
            "icon": "🎵",
            "color": "#8A745D",
        },
        {
            "value": f"{total_event_types:,}",
            "label": "Event Types",
            "icon": "📋",
            "color": "#C9826B",
        },
        {
            "value": f"{total_sources:,}",
            "label": "Sources",
            "icon": "🌐",
            "color": "#496755",
        },
        {
            "value": f"{url_percentage:.0f}%",
            "label": "URLs Available",
            "icon": "✅",
            "color": "#C89C21",
        },
    ]

    for metric_column, metric in zip(
        metric_columns,
        metric_definitions,
    ):
        with metric_column:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div
                        class="kpi-value"
                        style="color:{metric['color']};"
                    >
                        {metric['value']}
                    </div>
                    <div class="kpi-label">
                        {metric['label']}
                    </div>
                    <div class="kpi-icon">
                        {metric['icon']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="url-heading">Sample URL Overview — First 10 Records</div>
        """,
        unsafe_allow_html=True,
    )

    table_column, export_column = st.columns(
        [4.7, 1.3],
        vertical_alignment="top",
    )

    export_df = df[
        [
            "file_name",
            "category",
            "event_type",
            "source",
            "source_url",
        ]
    ].copy()

    export_df.columns = [
        "File Name",
        "Category",
        "Event Type",
        "Source",
        "URL",
    ]

    with export_column:
        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇ Export All URLs",
            data=csv_data,
            file_name="acoustic_dataset_urls.csv",
            mime="text/csv",
            width="stretch",
        )

    with st.container(border=False):
        st.dataframe(
            export_df.head(10),
            hide_index=True,
            use_container_width=True,
            width="stretch",
            
            column_config={
                "URL": st.column_config.LinkColumn(
                    "URL",
                    display_text="Open source page",
                ),
            },
        )

    st.markdown("### Source Distribution")

    source_counts = (
        df.groupby("source", dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    source_counts["share"] = (
        source_counts["count"] / total_files * 100
    )

    source_figure = px.pie(
        source_counts,
        names="source",
        values="count",
        hole=0.54,
        color="source",
        color_discrete_sequence=[
            "#A9D8A5",
            "#93BFE0",
            "#E6C47B",
            "#D1A5D9",
        ],
    )

    source_figure.update_traces(
        domain=dict(x=[0.02, 0.60]),
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Files:&nbsp;&nbsp;&nbsp;%{value:,.0f}<br>"
            "Share:&nbsp;&nbsp;&nbsp;%{percent}"
            "<extra></extra>"
        ),
    )

    source_figure.update_layout(
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        hoverlabel=dict(
            bgcolor="#fffefb",
            bordercolor="#aeb5af",
            align="left",
            font=dict(
                family="Menlo, Monaco, Courier New, monospace",
                size=13,
                color="#30493b",
            ),
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.50,
            font=dict(size=28),
        ),
        font=dict(
            family="IBM Plex Sans",
            size=15,
            color="#202622",
        ),
    )

    source_details = source_counts.copy()
    source_details["Files"] = source_details["count"].map(
        lambda value: f"{int(value):,}"
    )
    source_details["Share"] = source_details["share"].map(
        lambda value: f"{float(value):.1f}%"
    )

    source_details = source_details[
        ["source", "Files", "Share"]
    ]

    source_details.columns = [
        "Source",
        "Files",
        "Share",
    ]

    source_text_column, source_chart_column = st.columns([1.15, 0.85],
        vertical_alignment="top",
    )

    with source_text_column:
        rows = {
            str(row["Source"]).lower(): row
            for _, row in source_details.iterrows()
        }

        for brand, brand_style in [
            ("ZapSplat", "font-size:25px;font-weight:900;font-style:italic;"),
            ("Freesound", "font-size:21px;font-weight:800;"),
        ]:
            row = rows.get(brand.lower(), {"Files": "0", "Share": "0.0%"})

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid rgba(80,90,80,.14);
                    border-radius:14px;
                    padding:14px 18px;
                    margin-bottom:10px;
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    gap:20px;
                    box-shadow:0 5px 16px rgba(70,65,50,.06);
                ">
                    <div style="{brand_style}color:#263c31;">
                        {brand}
                    </div>
                    <div style="display:flex;gap:28px;text-align:left;">
                        <div>
                            <div style="font-size:14px;color:#6d766f;">Files</div>
                            <div style="font-size:19px;font-weight:800;">{row["Files"]}</div>
                        </div>
                        <div>
                            <div style="font-size:14px;color:#6d766f;">Share</div>
                            <div style="font-size:19px;font-weight:800;color:#71a86d;">
                                {row["Share"]}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with source_chart_column:
        st.plotly_chart(
            source_figure,
width="stretch",
            config={"displayModeBar": False},
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div style="
        border-top: 1px solid rgba(70,90,75,.16);
        margin-top: 28px;
        padding: 18px 4px 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    ">
        <div style="font-size:15px;color:#607068;">
            Acoustic Dataset Explorer · Metadata snapshot
        </div>
        <div style="display:flex;gap:18px;font-size:14px;font-weight:700;">
            <span style="color:#30493b;">◉ GitHub</span>
            <span style="color:#78a8ca;">▣ Freesound</span>
            <span style="color:#78ad72;">▣ ZapSplat</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
