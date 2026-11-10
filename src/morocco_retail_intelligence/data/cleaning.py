
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
