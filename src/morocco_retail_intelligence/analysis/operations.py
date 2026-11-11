import pandas as pd


def calculate_order_status_performance(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate order counts and percentages by status."""

    result = (
        orders.groupby("order_status")
        .agg(total_orders=("order_id", "nunique"))
        .reset_index()
    )

    total_orders = result["total_orders"].sum()

    result["percentage"] = (
        result["total_orders"] / total_orders * 100
        if total_orders else 0
    )

    return result.sort_values("total_orders", ascending=False)


def calculate_cancellation_and_return_rates(
    orders: pd.DataFrame,
) -> dict:
    """Calculate cancellation and return rates using all orders."""

    total_orders = orders["order_id"].nunique()

    cancelled_orders = orders.loc[
        orders["order_status"].eq("cancelled"),
        "order_id",
    ].nunique()

    returned_orders = orders.loc[
        orders["order_status"].eq("returned"),
        "order_id",
    ].nunique()

    return {
        "total_orders": int(total_orders),
        "cancelled_orders": int(cancelled_orders),
        "returned_orders": int(returned_orders),
        "cancellation_rate_pct": (
            cancelled_orders / total_orders * 100
            if total_orders else 0
        ),
        "return_rate_pct": (
            returned_orders / total_orders * 100
            if total_orders else 0
        ),
    }


def calculate_payment_method_performance(
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Analyze transaction counts and amounts by payment method."""

    result = (
        payments.groupby("payment_method")
        .agg(
            transactions=("order_id", "nunique"),
            payment_amount_mad=("payment_amount_mad", "sum"),
        )
        .reset_index()
    )

    total_transactions = result["transactions"].sum()

    result["transaction_share_pct"] = (
        result["transactions"] / total_transactions * 100
        if total_transactions else 0
    )

    return result.sort_values("transactions", ascending=False)


def calculate_payment_status_performance(
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Analyze payment outcomes."""

    result = (
        payments.groupby("payment_status")
        .agg(
            transactions=("order_id", "nunique"),
            payment_amount_mad=("payment_amount_mad", "sum"),
        )
        .reset_index()
    )

    total_transactions = result["transactions"].sum()

    result["percentage"] = (
        result["transactions"] / total_transactions * 100
        if total_transactions else 0
    )

    return result.sort_values("transactions", ascending=False)


def calculate_payment_failure_rate(
    payments: pd.DataFrame,
) -> float:
    """Calculate the percentage of failed payment transactions."""

    total_transactions = payments["order_id"].nunique()

    failed_transactions = payments.loc[
        payments["payment_status"].eq("failed"),
        "order_id",
    ].nunique()

    return (
        failed_transactions / total_transactions * 100
        if total_transactions else 0
    )


def calculate_delivery_performance(
    orders: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate delivery durations and summary metrics."""

    delivered = orders.loc[
        orders["order_status"].eq("delivered")
        & orders["order_date"].notna()
        & orders["delivery_date"].notna()
    ].copy()

    delivered["delivery_days"] = (
        delivered["delivery_date"] - delivered["order_date"]
    ).dt.total_seconds() / 86400

    valid_deliveries = delivered.loc[
        delivered["delivery_days"].ge(0)
    ].copy()

    summary = pd.DataFrame([
        {
            "metric": "Average delivery time",
            "value": valid_deliveries["delivery_days"].mean(),
            "unit": "Days",
        },
        {
            "metric": "Median delivery time",
            "value": valid_deliveries["delivery_days"].median(),
            "unit": "Days",
        },
        {
            "metric": "Minimum delivery time",
            "value": valid_deliveries["delivery_days"].min(),
            "unit": "Days",
        },
        {
            "metric": "Maximum delivery time",
            "value": valid_deliveries["delivery_days"].max(),
            "unit": "Days",
        },
    ])

    return valid_deliveries, summary


def calculate_delivery_by_city(
    delivery_data: pd.DataFrame,
) -> pd.DataFrame:
    """Compare delivery durations across cities."""

    return (
        delivery_data.groupby("shipping_city")
        .agg(
            delivered_orders=("order_id", "nunique"),
            average_delivery_days=("delivery_days", "mean"),
            median_delivery_days=("delivery_days", "median"),
        )
        .reset_index()
        .sort_values("average_delivery_days", ascending=False)
    )