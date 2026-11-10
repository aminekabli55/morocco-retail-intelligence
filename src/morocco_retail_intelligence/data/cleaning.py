import pandas as pd


def remove_duplicate_rows(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Remove exact duplicate rows without modifying the original."""

    return df.drop_duplicates().copy()


def remove_duplicates_with_report(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Remove exact duplicates and report the changes."""

    original_rows = len(df)

    cleaned_df = df.drop_duplicates().copy()

    removed_rows = original_rows - len(cleaned_df)

    report = {
        "original_rows": original_rows,
        "cleaned_rows": len(cleaned_df),
        "removed_rows": removed_rows,
    }

    return cleaned_df, report


def build_missing_values_report(
    df: pd.DataFrame,
    dataset_name: str,
) -> pd.DataFrame:
    """Generate a report of missing values for each column."""

    missing_count = df.isna().sum()

    report = pd.DataFrame(
        {
            "dataset": dataset_name,
            "column": df.columns,
            "missing_count": missing_count.values,
            "missing_percentage": (missing_count / len(df) * 100).round(2).values,
        }
    )

    return report.sort_values(
        by="missing_percentage",
        ascending=False,
    ).reset_index(drop=True)


def fill_missing_values(
    df: pd.DataFrame,
    fill_values: dict,
) -> pd.DataFrame:
    """Fill missing values using explicitly supplied values."""

    result = df.copy()

    return result.fillna(fill_values)
