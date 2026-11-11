import pandas as pd


def _get_customer_sales(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Connect delivered sales to customer information."""

    delivered_orders = orders.loc[
        orders["order_status"].eq("delivered"),
        ["order_id", "customer_id"],
    ]

    sales = order_items.merge(
        delivered_orders,
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    return sales.merge(
        customers[["customer_id", "customer_segment", "customer_age"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )


def calculate_segment_performance(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate sales performance by customer segment."""

    sales = _get_customer_sales(orders, order_items, customers)

    result = (
        sales.groupby("customer_segment")
        .agg(
            revenue_mad=("line_total_mad", "sum"),
            orders=("order_id", "nunique"),
            customers=("customer_id", "nunique"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
    )

    result["average_order_value_mad"] = result["revenue_mad"] / result["orders"]

    total_revenue = result["revenue_mad"].sum()

    result["revenue_share_pct"] = (
        result["revenue_mad"] / total_revenue * 100 if total_revenue else 0
    )

    return result.sort_values("revenue_mad", ascending=False)


def calculate_customer_performance(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate observed revenue and order activity per customer."""

    sales = _get_customer_sales(orders, order_items, customers)

    result = (
        sales.groupby(["customer_id", "customer_segment"])
        .agg(
            total_revenue_mad=("line_total_mad", "sum"),
            total_orders=("order_id", "nunique"),
            total_units=("quantity", "sum"),
        )
        .reset_index()
    )

    result["average_order_value_mad"] = (
        result["total_revenue_mad"] / result["total_orders"]
    )

    return result.sort_values(
        "total_revenue_mad",
        ascending=False,
    )
