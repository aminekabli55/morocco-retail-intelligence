import pandas as pd

from morocco_retail_intelligence.data.cleaning import (
    remove_duplicates_with_report,
)
from morocco_retail_intelligence.data.cleaning_config import (
    DatasetCleaningConfig,
)
from morocco_retail_intelligence.data.transformations import (
    convert_date_columns,
    convert_numeric_columns,
    normalize_text_columns,
)
import json
from pathlib import Path


def _validate_columns(
    df: pd.DataFrame,
    columns: list[str],
    dataset_name: str,
) -> None:
    """Ensure configured columns exist in the DataFrame."""

    missing_columns = set(columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name}: configured columns not found: {sorted(missing_columns)}"
        )


def clean_dataframe(
    df: pd.DataFrame,
    dataset_name: str,
    config: DatasetCleaningConfig,
) -> tuple[pd.DataFrame, dict]:
    """Clean one dataset and return it with an audit report."""

    result = df.copy()

    original_rows = len(result)
    missing_before = int(result.isna().sum().sum())

    configured_columns = (
        config.date_columns + config.numeric_columns + config.text_columns
    )

    _validate_columns(result, configured_columns, dataset_name)

    # 1. Remove exact duplicate rows when configured.
    duplicates_removed = 0

    if config.remove_exact_duplicates:
        result, duplicate_report = remove_duplicates_with_report(result)
        duplicates_removed = duplicate_report["removed_rows"]

    # 2. Convert dates and track parsing failures.
    date_failures = {}

    for column in config.date_columns:
        original_values = result[column]
        converted_values = pd.to_datetime(
            original_values,
            errors="coerce",
        )

        date_failures[column] = int(
            (original_values.notna() & converted_values.isna()).sum()
        )

        result[column] = converted_values

    # 3. Convert numeric columns and track invalid values.
    numeric_failures = {}

    for column in config.numeric_columns:
        original_values = result[column]
        converted_values = pd.to_numeric(
            original_values,
            errors="coerce",
        )

        numeric_failures[column] = int(
            (original_values.notna() & converted_values.isna()).sum()
        )

        if column in config.integer_columns:
            fractional_values = converted_values.notna() & (converted_values % 1 != 0)

            if fractional_values.any():
                raise ValueError(
                    f"{dataset_name}.{column} contains "
                    f"{int(fractional_values.sum())} non-integer values."
                )

    result = convert_numeric_columns(
        result,
        columns=config.numeric_columns,
        integer_columns=config.integer_columns,
    )

    # 4. Normalize text columns.
    result = normalize_text_columns(
        result,
        columns=config.text_columns,
        lowercase_columns=config.lowercase_columns,
    )

    # 5. Build the audit report.
    report = {
        "dataset": dataset_name,
        "original_rows": original_rows,
        "cleaned_rows": len(result),
        "duplicates_removed": duplicates_removed,
        "missing_values_before": missing_before,
        "missing_values_after": int(result.isna().sum().sum()),
        "date_conversion_failures": date_failures,
        "numeric_conversion_failures": numeric_failures,
    }

    return result, report


def save_cleaned_datasets(
    cleaned_datasets: dict[str, pd.DataFrame],
    cleaning_reports: list[dict],
    output_dir: Path,
) -> None:
    """Save cleaned datasets and their audit report."""

    output_dir.mkdir(parents=True, exist_ok=True)

    # Save each cleaned dataset.
    for dataset_name, df in cleaned_datasets.items():
        output_path = output_dir / f"{dataset_name}.csv"

        df.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

    # Convert nested dictionaries into JSON strings for CSV compatibility.
    report_df = pd.DataFrame(cleaning_reports)

    for column in [
        "date_conversion_failures",
        "numeric_conversion_failures",
    ]:
        if column in report_df.columns:
            report_df[column] = report_df[column].apply(lambda value: json.dumps(value))

    report_path = output_dir / "cleaning_report.csv"

    report_df.to_csv(report_path, index=False)

    print(f"Saved audit report: {report_path}")
