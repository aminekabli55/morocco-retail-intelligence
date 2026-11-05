import pandas as pd


def build_dataset_overview(
    datasets: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Generate a summary of all loaded datasets."""

    report = []

    for name, df in datasets.items():
        report.append({
            "dataset": name,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "duplicate_rows": df.duplicated().sum(),
            "memory_mb": round(
                df.memory_usage(deep=True).sum() / (1024 ** 2),
                2,
            ),
        })

    return pd.DataFrame(report)


def profile_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a column-level data quality report."""

    missing = df.isna().sum()

    return pd.DataFrame({
        "data_type": df.dtypes.astype(str),
        "non_null_count": df.notna().sum(),
        "missing_count": missing,
        "missing_percentage": (
            missing / len(df) * 100
        ).round(2),
        "unique_values": df.nunique(),
    })
