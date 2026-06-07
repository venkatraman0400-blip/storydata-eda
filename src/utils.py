"""
utils.py — StoryData EDA
Shared helper functions, plot configuration, and narrative utilities.
Import this at the top of every notebook:
    from src.utils import *
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os

warnings.filterwarnings("ignore")


# ──────────────────────────────────────────────
# PLOT STYLE CONFIG
# ──────────────────────────────────────────────

PALETTE = {
    "purple": "#534AB7",
    "teal":   "#1D9E75",
    "coral":  "#D85A30",
    "blue":   "#378ADD",
    "amber":  "#BA7517",
    "pink":   "#D4537E",
    "gray":   "#888780",
}

SEQUENTIAL = ["#EEEDFE", "#AFA9EC", "#7F77DD", "#534AB7", "#3C3489", "#26215C"]
DIVERGING  = ["#D85A30", "#F5C4B3", "#F1EFE8", "#CECBF6", "#534AB7", "#26215C"]
CATEGORICAL = list(PALETTE.values())


def set_style():
    """Apply consistent Seaborn + Matplotlib style across all acts."""
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        "figure.facecolor":  "white",
        "axes.facecolor":    "white",
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.spines.left":  True,
        "axes.spines.bottom":True,
        "axes.edgecolor":    "#D3D1C7",
        "axes.linewidth":    0.8,
        "grid.color":        "#F1EFE8",
        "grid.linewidth":    0.6,
        "font.family":       "sans-serif",
        "text.color":        "#2C2C2A",
        "axes.labelcolor":   "#5F5E5A",
        "xtick.color":       "#5F5E5A",
        "ytick.color":       "#5F5E5A",
    })


set_style()


# ──────────────────────────────────────────────
# NARRATIVE HELPERS
# ──────────────────────────────────────────────

def act_header(act_num: int, title: str, opening_question: str):
    """
    Print a formatted act header in the notebook.
    Call at the top of each notebook's first cell.
    """
    divider = "─" * 60
    print(f"\n{divider}")
    print(f"  ACT {act_num} — {title.upper()}")
    print(divider)
    print(f"\n  Opening question:\n  \"{opening_question}\"\n")


def insight_callout(text: str, label: str = "Key insight"):
    """Print a plain-English insight callout after a chart."""
    print(f"\n  ╔══ {label.upper()} ══")
    for line in text.strip().split("\n"):
        print(f"  ║  {line}")
    print(f"  ╚{'═' * (len(label) + 7)}\n")


def punchline(text: str):
    """Print the closing punchline for an act."""
    print(f"\n  ★  {text}\n")


# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────

def load_raw(filename: str) -> pd.DataFrame:
    """Load a CSV from data/raw/ with a confirmation message."""
    path = os.path.join("data", "raw", filename)
    df = pd.read_csv(path)
    print(f"Loaded '{filename}' — {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def load_processed(filename: str) -> pd.DataFrame:
    """Load a CSV from data/processed/."""
    path = os.path.join("data", "processed", filename)
    df = pd.read_csv(path)
    print(f"Loaded processed '{filename}' — {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def save_processed(df: pd.DataFrame, filename: str):
    """Save a cleaned dataframe to data/processed/."""
    path = os.path.join("data", "processed", filename)
    df.to_csv(path, index=False)
    print(f"Saved to data/processed/{filename}")


# ──────────────────────────────────────────────
# ACT 1 — DATA OVERVIEW
# ──────────────────────────────────────────────

def data_snapshot(df: pd.DataFrame):
    """
    Print a plain-English data overview — shape, dtypes, missing values.
    Designed for non-technical audiences.
    """
    print(f"\n  Dataset has {df.shape[0]:,} records and {df.shape[1]} columns.")
    print(f"  Think of it as a spreadsheet with {df.shape[0]:,} rows of information.\n")

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)
    missing_df = pd.DataFrame({
        "column": missing.index,
        "missing_count": missing.values,
        "missing_%": missing_pct.values
    }).query("missing_count > 0").sort_values("missing_%", ascending=False)

    if missing_df.empty:
        print("  No missing values found. The dataset is complete.")
    else:
        print(f"  {len(missing_df)} column(s) have missing values:\n")
        print(missing_df.to_string(index=False))


def plot_missing_heatmap(df: pd.DataFrame, figsize=(14, 5)):
    """Seaborn heatmap of missing values across the dataset."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        df.isnull(),
        cbar=False,
        cmap=["#F1EFE8", "#534AB7"],
        ax=ax,
        yticklabels=False,
        linewidths=0
    )
    ax.set_title(
        "Where is data missing?  (purple = missing, light = present)",
        fontsize=13, pad=12, color="#2C2C2A"
    )
    ax.set_xlabel("")
    plt.xticks(rotation=40, ha="right", fontsize=10)
    plt.tight_layout()
    save_figure(fig, "act1_missing_heatmap.png")
    plt.show()


def plot_dtype_bar(df: pd.DataFrame, figsize=(8, 4)):
    """Bar chart of column data types."""
    dtype_counts = df.dtypes.astype(str).value_counts()
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.barh(dtype_counts.index, dtype_counts.values, color=CATEGORICAL[:len(dtype_counts)])
    ax.set_xlabel("Number of columns")
    ax.set_title("Column types — what kind of data do we have?", fontsize=13, pad=10)
    for bar, val in zip(bars, dtype_counts.values):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=11)
    plt.tight_layout()
    save_figure(fig, "act1_dtype_bar.png")
    plt.show()


# ──────────────────────────────────────────────
# ACT 2 — DISTRIBUTIONS
# ──────────────────────────────────────────────

def plot_distribution(df: pd.DataFrame, col: str, color: str = "#534AB7", figsize=(12, 4)):
    """
    Side-by-side histogram + boxplot for a single numeric column.
    Annotates mean and median in plain English.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Histogram with KDE
    sns.histplot(df[col].dropna(), kde=True, color=color, ax=axes[0], linewidth=0)
    axes[0].axvline(df[col].mean(), color="#D85A30", linestyle="--", linewidth=1.5, label=f"Mean: {df[col].mean():.1f}")
    axes[0].axvline(df[col].median(), color="#1D9E75", linestyle="--", linewidth=1.5, label=f"Median: {df[col].median():.1f}")
    axes[0].set_title(f"Spread of values — {col}", fontsize=12)
    axes[0].legend(fontsize=10)

    # Boxplot
    sns.boxplot(x=df[col].dropna(), color=color, ax=axes[1], width=0.4,
                flierprops=dict(marker="o", markerfacecolor="#D85A30", markersize=4, alpha=0.5))
    axes[1].set_title(f"Outlier view — {col}", fontsize=12)

    plt.tight_layout()
    save_figure(fig, f"act2_dist_{col}.png")
    plt.show()


def plot_violin(df: pd.DataFrame, col: str, group_col: str, figsize=(12, 5)):
    """Violin plot comparing a numeric column across categories."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.violinplot(data=df, x=group_col, y=col, palette=CATEGORICAL, ax=ax, inner="quartile")
    ax.set_title(f"How {col} varies across {group_col}", fontsize=13)
    plt.tight_layout()
    save_figure(fig, f"act2_violin_{col}_by_{group_col}.png")
    plt.show()


# ──────────────────────────────────────────────
# ACT 3 — RELATIONSHIPS / CORRELATIONS
# ──────────────────────────────────────────────

def plot_correlation_heatmap(df: pd.DataFrame, figsize=(11, 8)):
    """
    Annotated Seaborn correlation heatmap.
    Only uses numeric columns.
    """
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))  # upper triangle hidden

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap=sns.diverging_palette(20, 250, as_cmap=True),
        center=0,
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor="#F1EFE8",
        ax=ax,
        annot_kws={"size": 9}
    )
    ax.set_title(
        "How closely do columns move together?\n(+1 = always together, –1 = always opposite, 0 = no link)",
        fontsize=12, pad=14
    )
    plt.tight_layout()
    save_figure(fig, "act3_correlation_heatmap.png")
    plt.show()


# ──────────────────────────────────────────────
# ACT 4 — TIME TRENDS (Plotly animated)
# ──────────────────────────────────────────────

def plot_animated_line(df: pd.DataFrame, x_col: str, y_col: str,
                       color_col: str = None, title: str = "Change over time"):
    """
    Plotly animated line chart. Exports to outputs/figures/ as HTML.
    df must have a sortable time column as x_col.
    """
    fig = px.line(
        df.sort_values(x_col),
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        color_discrete_sequence=CATEGORICAL,
        template="plotly_white",
        markers=True
    )
    fig.update_layout(
        title_font_size=15,
        hovermode="x unified",
        legend_title_text=color_col or "",
        margin=dict(t=60, b=40)
    )
    save_plotly(fig, "act4_animated_line.html")
    fig.show()


# ──────────────────────────────────────────────
# ACT 5 — OUTLIER DETECTION
# ──────────────────────────────────────────────

def flag_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Flag outliers using the IQR method.
    Adds a boolean column '{col}_is_outlier' to the dataframe.
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df.copy()
    df[f"{col}_is_outlier"] = (df[col] < lower) | (df[col] > upper)
    n_out = df[f"{col}_is_outlier"].sum()
    print(f"  {n_out} outliers found in '{col}' (IQR method)")
    print(f"  Normal range: {lower:.2f} — {upper:.2f}")
    return df


def plot_outlier_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                         outlier_col: str, label_col: str = None,
                         title: str = "Who breaks the rules?"):
    """
    Interactive Plotly scatter with outliers highlighted in coral.
    Hover shows the label_col if provided.
    """
    df = df.copy()
    df["_color"] = df[outlier_col].map({True: "Outlier", False: "Normal"})

    hover_data = [label_col] if label_col else []

    fig = px.scatter(
        df, x=x_col, y=y_col,
        color="_color",
        color_discrete_map={"Normal": "#534AB7", "Outlier": "#D85A30"},
        hover_data=hover_data,
        title=title,
        template="plotly_white",
        opacity=0.75
    )
    fig.update_traces(marker=dict(size=7))
    fig.update_layout(
        legend_title_text="",
        title_font_size=15,
        margin=dict(t=60, b=40)
    )
    save_plotly(fig, "act5_outlier_scatter.html")
    fig.show()


# ──────────────────────────────────────────────
# FIGURE EXPORT HELPERS
# ──────────────────────────────────────────────

FIGURES_DIR = os.path.join("outputs", "figures")


def save_figure(fig, filename: str, dpi: int = 150):
    """Save a Matplotlib figure to outputs/figures/."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    print(f"  Saved → {path}")


def save_plotly(fig, filename: str):
    """Save a Plotly figure as an interactive HTML file."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, filename)
    fig.write_html(path, include_plotlyjs="cdn")
    print(f"  Saved → {path}")
