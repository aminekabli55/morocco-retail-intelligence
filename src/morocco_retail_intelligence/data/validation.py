import pandas as pd


def validate_primary_key(
    df: pd.DataFrame,
    column: str,
    dataset_name: str,
) -> dict:
    """Check whether a column satisfies primary key requirements."""

    missing_count = int(df[column].isna().sum())
    duplicate_count = int(df[column].duplicated().sum())

    return {
        "dataset": dataset_name,
        "column": column,
        "total_rows": len(df),
        "missing_keys": missing_count,
        "duplicate_keys": duplicate_count,
        "is_valid": missing_count == 0 and duplicate_count == 0,
    }



def validate_foreign_key(
    child_df: pd.DataFrame,
    child_column: str,
    parent_df: pd.DataFrame,
    parent_column: str,
    relationship_name: str,
) -> dict:
    """Check whether foreign keys reference existing parent records."""

    child_values = child_df[child_column]

    missing_count = int(child_values.isna().sum())

    parent_values = parent_df[parent_column].dropna()

    invalid_mask = (
        child_values.notna()
        & ~child_values.isin(parent_values)
    )

    invalid_count = int(invalid_mask.sum())

    return {
        "relationship": relationship_name,
        "missing_foreign_keys": missing_count,
        "invalid_foreign_keys": invalid_count,
        "is_valid": missing_count == 0 and invalid_count == 0,
    }
