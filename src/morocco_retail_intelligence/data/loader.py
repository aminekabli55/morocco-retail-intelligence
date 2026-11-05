from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class RetailData:
    customers: pd.DataFrame
    products: pd.DataFrame
    orders: pd.DataFrame
    order_items: pd.DataFrame
    payments: pd.DataFrame
    reviews: pd.DataFrame


def load_data(data_dir: Path) -> RetailData:
    """Load all raw retail CSV datasets."""

    return RetailData(
        customers=pd.read_csv(data_dir / "customers.csv"),
        products=pd.read_csv(data_dir / "products.csv"),
        orders=pd.read_csv(data_dir / "orders.csv"),
        order_items=pd.read_csv(data_dir / "order_items.csv"),
        payments=pd.read_csv(data_dir / "payments.csv"),
        reviews=pd.read_csv(data_dir / "reviews.csv"),
    )
