import pandas as pd


def calculate_review_kpis(
    reviews: pd.DataFrame,
) -> dict:
    """Calculate overall customer satisfaction KPIs."""

    valid_ratings = reviews["rating"].dropna()

    total_reviews = len(reviews)
    valid_count = len(valid_ratings)

    positive_reviews = int(valid_ratings.ge(4).sum())
    negative_reviews = int(valid_ratings.le(2).sum())

    return {
        "total_reviews": int(total_reviews),
        "valid_ratings": int(valid_count),
        "average_rating": (
            float(valid_ratings.mean()) if valid_count else None
        ),
        "median_rating": (
            float(valid_ratings.median()) if valid_count else None
        ),
        "satisfaction_rate_pct": (
            positive_reviews / valid_count * 100
            if valid_count else 0
        ),
        "dissatisfaction_rate_pct": (
            negative_reviews / valid_count * 100
            if valid_count else 0
        ),
        "five_star_reviews": int(valid_ratings.eq(5).sum()),
        "one_star_reviews": int(valid_ratings.eq(1).sum()),
    }


def calculate_rating_distribution(
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the count and percentage for each rating."""

    result = (
        reviews["rating"]
        .value_counts()
        .sort_index()
        .rename_axis("rating")
        .reset_index(name="review_count")
    )

    total_ratings = result["review_count"].sum()

    result["percentage"] = (
        result["review_count"] / total_ratings * 100
        if total_ratings else 0
    )

    return result


def calculate_satisfaction_by_city(
    reviews: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate average ratings by order city."""

    review_data = reviews.merge(
        orders[["order_id", "shipping_city"]],
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    return (
        review_data.dropna(subset=["rating"])
        .groupby("shipping_city")
        .agg(
            average_rating=("rating", "mean"),
            median_rating=("rating", "median"),
            total_reviews=("rating", "count"),
        )
        .reset_index()
        .sort_values("average_rating", ascending=False)
    )


def calculate_satisfaction_by_segment(
    reviews: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate average ratings by customer segment."""

    review_data = reviews.merge(
        customers[["customer_id", "customer_segment"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    return (
        review_data.dropna(subset=["rating"])
        .groupby("customer_segment")
        .agg(
            average_rating=("rating", "mean"),
            median_rating=("rating", "median"),
            total_reviews=("rating", "count"),
        )
        .reset_index()
        .sort_values("average_rating", ascending=False)
    )


def calculate_monthly_satisfaction(
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate average customer rating per month."""

    review_data = reviews.dropna(
        subset=["rating", "review_date"]
    ).copy()

    review_data["review_month"] = (
        review_data["review_date"].dt.to_period("M")
    )

    return (
        review_data.groupby("review_month")
        .agg(
            average_rating=("rating", "mean"),
            total_reviews=("rating", "count"),
        )
        .reset_index()
        .sort_values("review_month")
    )


def calculate_comment_statistics(
    reviews: pd.DataFrame,
    comment_column: str = "review_comment",
) -> dict:
    """Calculate the number of reviews with and without comments."""

    if comment_column not in reviews.columns:
        raise ValueError(
            f"Comment column '{comment_column}' not found."
        )

    comments = reviews[comment_column].astype("string").str.strip()

    has_comment = comments.notna() & comments.ne("")

    total_reviews = len(reviews)
    reviews_with_comments = int(has_comment.sum())

    return {
        "total_reviews": int(total_reviews),
        "reviews_with_comments": reviews_with_comments,
        "reviews_without_comments": (
            total_reviews - reviews_with_comments
        ),
        "comment_completion_rate_pct": (
            reviews_with_comments / total_reviews * 100
            if total_reviews else 0
        ),
    }