"""Generate synthetic retail data for the RetailOps project."""

import numpy as np
import pandas as pd


def generate_data(n_rows=500, random_state=42):
    """Return reproducible synthetic retail data as a pandas DataFrame."""
    if n_rows < 1:
        raise ValueError("n_rows must be at least 1")

    rng = np.random.default_rng(random_state)

    regions = ["South", "North", "West", "East"]
    categories = ["Apparel", "Electronics", "Home & Kitchen", "Groceries"]

    data = pd.DataFrame(
        {
            "Store_ID": rng.integers(101, 115, size=n_rows),
            "Region": rng.choice(regions, size=n_rows),
            "Category": rng.choice(categories, size=n_rows),
            "Customer_Footfall": rng.integers(100, 801, size=n_rows),
            "Marketing_Spend": np.round(
                rng.uniform(500, 1100, size=n_rows), 2
            ),
        }
    )

    region_effect = {
        "South": 100,
        "North": 50,
        "West": -50,
        "East": -100,
    }
    category_effect = {
        "Apparel": 0,
        "Electronics": 100,
        "Home & Kitchen": 50,
        "Groceries": -50,
    }

    sales_revenue = (
        1800
        + data["Customer_Footfall"] * 4.2
        + data["Marketing_Spend"] * 1.4
        + data["Region"].map(region_effect)
        + data["Category"].map(category_effect)
        + rng.normal(0, 700, size=n_rows)
    )

    data["Sales_Revenue"] = sales_revenue.clip(lower=500).round(2)

    # Keep the six fields in the same order as the dashboard reference.
    return data[
        [
            "Store_ID",
            "Region",
            "Category",
            "Sales_Revenue",
            "Customer_Footfall",
            "Marketing_Spend",
        ]
    ]


if __name__ == "__main__":
    retail_data = generate_data()
    print(retail_data.head(10).to_string(index=False))
    print(f"\nRows: {len(retail_data)} | Columns: {len(retail_data.columns)}")