
import pandas as pd


def calculate_sales_kpis(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> dict:
    """Calculate core sales KPIs using delivered orders only."""

    delivered_orders = orders.loc[
        orders["order_status"].eq("delivered")
    ].copy()

    delivered_sales = order_items.merge(
        delivered_orders[["order_id"]],
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    total_revenue = delivered_sales["line_total_mad"].sum()
    total_orders = delivered_orders["order_id"].nunique()
    total_units = delivered_sales["quantity"].sum()

    average_order_value = (
        total_revenue / total_orders if total_orders else 0
    )

    return {
        "total_revenue_mad": float(total_revenue),
        "total_delivered_orders": int(total_orders),
        "total_units_sold": int(total_units),
        "average_order_value_mad": float(average_order_value),
    }


def calculate_monthly_sales(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate monthly revenue, orders, units, and average order value."""

    delivered_orders = orders.loc[
        orders["order_status"].eq("delivered"),
        ["order_id", "order_date"],
    ].copy()

    delivered_sales = order_items.merge(
        delivered_orders,
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    delivered_sales["order_month"] = (
        delivered_sales["order_date"].dt.to_period("M")
    )

    monthly_sales = (
        delivered_sales
        .groupby("order_month")
        .agg(
            revenue_mad=("line_total_mad", "sum"),
            orders=("order_id", "nunique"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    monthly_sales["average_order_value_mad"] = (
        monthly_sales["revenue_mad"]
        / monthly_sales["orders"]
    )

    monthly_sales["revenue_growth_pct"] = (
        monthly_sales["revenue_mad"]
        .pct_change()
        .mul(100)
    )

    return monthly_sales
