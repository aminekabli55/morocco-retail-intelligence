from dataclasses import dataclass, field


@dataclass(frozen=True)
class DatasetCleaningConfig:
    """Define the cleaning rules for one dataset."""

    date_columns: list[str] = field(default_factory=list)
    numeric_columns: list[str] = field(default_factory=list)
    integer_columns: list[str] = field(default_factory=list)
    text_columns: list[str] = field(default_factory=list)
    lowercase_columns: list[str] = field(default_factory=list)
    remove_exact_duplicates: bool = False


DATASET_CONFIGS = {
    "customers": DatasetCleaningConfig(
        date_columns=["signup_date"],
        numeric_columns=["customer_age"],
        integer_columns=["customer_age"],
        text_columns=["city", "customer_segment"],
        lowercase_columns=["city", "customer_segment"],
    ),
    "products": DatasetCleaningConfig(
        numeric_columns=[
            "unit_price_mad",
            "cost_price_mad",
        ],
        text_columns=["category"],
        lowercase_columns=["category"],
    ),
    "orders": DatasetCleaningConfig(
        date_columns=["order_date", "delivery_date"],
        numeric_columns=["shipping_fee_mad"],
        text_columns=["shipping_city", "order_status"],
        lowercase_columns=["shipping_city", "order_status"],
        remove_exact_duplicates=True,
    ),
    "order_items": DatasetCleaningConfig(
        numeric_columns=[
            "quantity",
            "unit_price_mad",
            "discount_rate",
            "line_total_mad",
        ],
        integer_columns=["quantity"],
    ),
    "payments": DatasetCleaningConfig(
        numeric_columns=["payment_amount_mad"],
        text_columns=["payment_method", "payment_status"],
        lowercase_columns=["payment_method", "payment_status"],
    ),
    "reviews": DatasetCleaningConfig(
        date_columns=["review_date"],
        numeric_columns=["rating"],
        integer_columns=["rating"],
    ),
}
