import pandas as pd


def convert_date_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert selected columns to Pandas datetime."""

    result = df.copy()

    for column in columns:
        result[column] = pd.to_datetime(
            result[column],
            errors="coerce",
        )

    return result


def convert_age_to_int(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert selected columns to Pandas integer."""

    result = df.copy()

    for column in columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        ).astype("Int64")

    return result
