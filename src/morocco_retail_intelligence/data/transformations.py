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


def convert_numeric_columns(
    df: pd.DataFrame,
    columns: list[str],
    integer_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Convert selected columns to numeric types."""

    result = df.copy()
    integer_columns = integer_columns or []

    for column in columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )

        if column in integer_columns:
            result[column] = result[column].astype("Int64")

    return result


def normalize_text_columns(
    df: pd.DataFrame,
    columns: list[str],
    lowercase_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Remove unnecessary whitespace and optionally normalize case."""

    result = df.copy()
    lowercase_columns = lowercase_columns or []

    for column in columns:
        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

        if column in lowercase_columns:
            result[column] = result[column].str.lower()

    return result
