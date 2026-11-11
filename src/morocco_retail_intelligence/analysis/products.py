import pandas as pd


def _get_delivered_sales(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Return order-item records belonging to delivered orders."""

    delivered_orders = orders.loc[
        orders["order_status"].eq("delivered"),
        ["order_id"],
    ]

    return order_items.merge(
        delivered_orders,
        on="order_id",
        how="inner",
        validate="many_to_one",
    )


def calculate_product_performance(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate revenue, units, and order count per product."""

    sales = _get_delivered_sales(orders, order_items)

    sales = sales.merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    result = (
        sales.groupby(["product_id", "category"])
        .agg(
            revenue_mad=("line_total_mad", "sum"),
            units_sold=("quantity", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    result["average_selling_price_mad"] = (
        result["revenue_mad"] / result["units_sold"]
    )

    return result.sort_values("revenue_mad", ascending=False)


def calculate_category_performance(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate sales performance for each product category."""

    sales = _get_delivered_sales(orders, order_items)

    sales = sales.merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    result = (
        sales.groupby("category")
        .agg(
            revenue_mad=("line_total_mad", "sum"),
            units_sold=("quantity", "sum"),
            orders=("order_id", "nunique"),
            unique_products=("product_id", "nunique"),
        )
        .reset_index()
    )

    total_revenue = result["revenue_mad"].sum()

    result["revenue_share_pct"] = (
        result["revenue_mad"] / total_revenue * 100
        if total_revenue else 0
    )

    return result.sort_values("revenue_mad", ascending=False)


def calculate_product_profitability(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Estimate product-level gross profit and gross margin."""

    sales = _get_delivered_sales(orders, order_items)

    sales = sales.merge(
        products[["product_id", "category", "cost_price_mad"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    sales["estimated_cost_mad"] = (
        sales["quantity"] * sales["cost_price_mad"]
    )

    sales["estimated_gross_profit_mad"] = (
        sales["line_total_mad"] - sales["estimated_cost_mad"]
    )

    result = (
        sales.groupby(["product_id", "category"])
        .agg(
            revenue_mad=("line_total_mad", "sum"),
            cost_mad=("estimated_cost_mad", "sum"),
            gross_profit_mad=("estimated_gross_profit_mad", "sum"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
    )

    result["gross_margin_pct"] = (
        result["gross_profit_mad"]
        .div(result["revenue_mad"].where(result["revenue_mad"].ne(0)))
        .mul(100)
    )

    return result.sort_values("gross_profit_mad", ascending=False)