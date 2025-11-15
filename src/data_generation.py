"""
Data generation script for Business Coaching Analytics project.
Generates realistic mock sales data for a high-ticket coaching business.
"""
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import numpy as np
from faker import Faker

from config import DATA_SETTINGS, RAW_DATA_DIR

# Initialize Faker with seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)


def generate_dates(n_records: int) -> list[datetime]:
    """
    Generate dates with seasonal weighting across 11 months (Jan-Nov 2025).

    Args:
        n_records: Total number of records to generate

    Returns:
        List of datetime objects
    """
    start_date = datetime.strptime(DATA_SETTINGS["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(DATA_SETTINGS["end_date"], "%Y-%m-%d")

    # Define month ranges for quarters
    q1_months = [1, 2, 3]  # Jan-Mar
    q2_months = [4, 5, 6]  # Apr-Jun
    q3_months = [7, 8, 9]  # Jul-Sep
    q4_months = [10, 11]   # Oct-Nov (partial)

    seasonal_weights = DATA_SETTINGS["seasonal_weights"]

    # Calculate records per quarter
    q1_records = int(n_records * seasonal_weights[0])
    q2_records = int(n_records * seasonal_weights[1])
    q3_records = int(n_records * seasonal_weights[2])
    q4_records = n_records - q1_records - q2_records - q3_records  # Remainder

    dates = []

    def generate_quarter_dates(months: list, n: int) -> list[datetime]:
        quarter_dates = []
        for _ in range(n):
            month = random.choice(months)
            # Avoid weekends for some realism (80% weekdays)
            for _ in range(10):  # Try up to 10 times
                day = random.randint(1, 28)  # Safe day range
                date = datetime(2025, month, day)
                if random.random() < 0.8:  # 80% weekdays
                    if date.weekday() < 5:  # Monday-Friday
                        quarter_dates.append(date)
                        break
                else:
                    quarter_dates.append(date)
                    break
            else:
                quarter_dates.append(date)  # Use last generated if no weekday found
        return quarter_dates

    dates.extend(generate_quarter_dates(q1_months, q1_records))
    dates.extend(generate_quarter_dates(q2_months, q2_records))
    dates.extend(generate_quarter_dates(q3_months, q3_records))
    dates.extend(generate_quarter_dates(q4_months, q4_records))

    # Sort dates chronologically
    dates.sort()

    return dates


def generate_customer_info(n_records: int) -> tuple[list[str], list[str]]:
    """
    Generate realistic customer names and emails.

    Args:
        n_records: Number of customers to generate

    Returns:
        Tuple of (names, emails)
    """
    names = []
    emails = []

    used_emails = set()

    for _ in range(n_records):
        name = fake.name()
        # Generate unique email
        for _ in range(10):  # Try up to 10 times
            email = fake.email()
            if email not in used_emails:
                used_emails.add(email)
                break

        names.append(name)
        emails.append(email)

    return names, emails


def generate_products(n_records: int) -> list[str]:
    """
    Generate product selections with realistic distribution.

    Args:
        n_records: Number of product selections

    Returns:
        List of product names
    """
    products = list(DATA_SETTINGS["products"].keys())

    # Realistic distribution: lower price = higher volume
    product_weights = [0.50, 0.35, 0.15]  # Elite, Executive, Scale

    selected_products = random.choices(products, weights=product_weights, k=n_records)

    return selected_products


def generate_closers(n_records: int) -> list[str]:
    """
    Generate closer assignments based on performance distribution.

    Args:
        n_records: Number of assignments

    Returns:
        List of closer names
    """
    closers = DATA_SETTINGS["closers"]
    weights = DATA_SETTINGS["closer_weights"]

    assigned_closers = random.choices(closers, weights=weights, k=n_records)

    return assigned_closers


def generate_countries(n_records: int) -> list[str]:
    """
    Generate countries based on market distribution.

    Args:
        n_records: Number of country assignments

    Returns:
        List of country codes
    """
    countries = DATA_SETTINGS["countries"]
    weights = DATA_SETTINGS["country_weights"]

    assigned_countries = random.choices(countries, weights=weights, k=n_records)

    return assigned_countries


def generate_revenue_and_cash(products: list[str]) -> tuple[list[float], list[float]]:
    """
    Generate revenue and cash collected based on products.

    Args:
        products: List of product names

    Returns:
        Tuple of (revenue, cash_collected)
    """
    product_prices = DATA_SETTINGS["products"]
    min_rate, max_rate = DATA_SETTINGS["cash_collection_rate"]

    revenue = []
    cash_collected = []

    for product in products:
        price = product_prices[product]
        revenue.append(price)

        # Cash collection rate with some variance
        collection_rate = random.uniform(min_rate, max_rate)
        cash = round(price * collection_rate, 2)
        cash_collected.append(cash)

    return revenue, cash_collected


def generate_upsells(n_records: int, products: list[str]) -> list[bool]:
    """
    Generate upsell flags with realistic patterns.

    Args:
        n_records: Number of records
        products: List of products (higher tiers more likely to upsell)

    Returns:
        List of boolean upsell flags
    """
    min_rate, max_rate = DATA_SETTINGS["upsell_rate"]

    upsells = []
    for product in products:
        # Higher-tier products slightly more likely to upsell
        if product == "Scale to 7-Figures Program":
            rate = max_rate
        elif product == "Executive Leadership Mastery":
            rate = (min_rate + max_rate) / 2
        else:
            rate = min_rate

        upsell = random.random() < rate
        upsells.append(upsell)

    return upsells


def generate_coaching_data() -> pd.DataFrame:
    """
    Generate complete coaching sales dataset.

    Returns:
        DataFrame with all sales data
    """
    n_records = DATA_SETTINGS["total_rows"]

    print(f"Generating {n_records} sales records...")

    # Generate all data
    dates = generate_dates(n_records)
    names, emails = generate_customer_info(n_records)
    products = generate_products(n_records)
    closers = generate_closers(n_records)
    countries = generate_countries(n_records)
    revenue, cash_collected = generate_revenue_and_cash(products)
    upsells = generate_upsells(n_records, products)

    # Create DataFrame
    df = pd.DataFrame({
        "date": dates,
        "name": names,
        "email": emails,
        "revenue": revenue,
        "cash_collected": cash_collected,
        "product": products,
        "closer": closers,
        "country": countries,
        "upsell": upsells,
    })

    # Ensure exactly n_records (handle any rounding issues)
    df = df.head(n_records)

    return df


def validate_data(df: pd.DataFrame) -> None:
    """
    Validate the generated data meets requirements.

    Args:
        df: DataFrame to validate
    """
    print("\n=== Data Validation ===")

    # Check row count
    assert len(df) == DATA_SETTINGS["total_rows"], f"Expected {DATA_SETTINGS['total_rows']} rows, got {len(df)}"
    print(f"✓ Row count: {len(df)}")

    # Check for duplicates
    duplicates = df.duplicated(subset=["email"]).sum()
    print(f"✓ Duplicate emails: {duplicates}")

    # Check date range
    min_date = df["date"].min()
    max_date = df["date"].max()
    print(f"✓ Date range: {min_date.date()} to {max_date.date()}")

    # Check products
    product_dist = df["product"].value_counts()
    print(f"\n✓ Product distribution:")
    for product, count in product_dist.items():
        pct = count / len(df) * 100
        print(f"  - {product}: {count} ({pct:.1f}%)")

    # Check closers
    closer_dist = df["closer"].value_counts()
    print(f"\n✓ Closer distribution:")
    for closer, count in closer_dist.items():
        pct = count / len(df) * 100
        print(f"  - {closer}: {count} ({pct:.1f}%)")

    # Check countries
    country_dist = df["country"].value_counts()
    print(f"\n✓ Country distribution:")
    for country, count in country_dist.items():
        pct = count / len(df) * 100
        print(f"  - {country}: {count} ({pct:.1f}%)")

    # Check cash collection
    avg_collection_rate = (df["cash_collected"] / df["revenue"]).mean()
    print(f"\n✓ Average cash collection rate: {avg_collection_rate:.1%}")

    # Check upsell rate
    upsell_rate = df["upsell"].mean()
    print(f"✓ Upsell rate: {upsell_rate:.1%}")

    # Check revenue stats
    print(f"\n✓ Revenue statistics:")
    print(f"  - Total: ${df['revenue'].sum():,.2f}")
    print(f"  - Average: ${df['revenue'].mean():,.2f}")
    print(f"  - Min: ${df['revenue'].min():,.2f}")
    print(f"  - Max: ${df['revenue'].max():,.2f}")

    print("\n✓ All validation checks passed!")


def main():
    """Main execution function."""
    # Ensure output directory exists
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Generate data
    df = generate_coaching_data()

    # Validate data
    validate_data(df)

    # Save to CSV
    output_path = RAW_DATA_DIR / "coaching_sales_2025.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✓ Data saved to: {output_path}")

    # Display sample
    print("\n=== Sample Data (first 5 rows) ===")
    print(df.head().to_string())


if __name__ == "__main__":
    main()
