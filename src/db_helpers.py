"""
Database helper functions for Python analysis.
Provides convenient functions to query data and load into pandas DataFrames.
"""
import pandas as pd
import psycopg2
from psycopg2 import sql
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from src.config import DB_CONFIG


@contextmanager
def get_connection():
    """
    Context manager for database connections.
    Automatically handles connection closing.

    Usage:
        with get_connection() as conn:
            df = pd.read_sql("SELECT * FROM sales", conn)
    """
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: Optional[tuple] = None) -> List[tuple]:
    """
    Execute a SQL query and return results as list of tuples.

    Args:
        query: SQL query string
        params: Optional tuple of query parameters

    Returns:
        List of tuples containing query results
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def query_to_dataframe(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.

    Args:
        query: SQL query string
        params: Optional tuple of query parameters

    Returns:
        pandas DataFrame with query results
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=params)


def get_all_sales() -> pd.DataFrame:
    """
    Load all sales data from the database into a DataFrame.

    Returns:
        pandas DataFrame with all sales records
    """
    query = """
        SELECT
            id,
            date as sale_date,
            product,
            revenue,
            closer,
            country,
            cash_collected,
            upsell
        FROM sales
        ORDER BY date
    """
    return query_to_dataframe(query)


def get_sales_by_date_range(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Load sales data for a specific date range.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format

    Returns:
        pandas DataFrame with filtered sales records
    """
    query = """
        SELECT
            id,
            date as sale_date,
            product,
            revenue,
            closer,
            country,
            cash_collected,
            upsell
        FROM sales
        WHERE date BETWEEN %s AND %s
        ORDER BY date
    """
    return query_to_dataframe(query, (start_date, end_date))


def get_sales_by_product(product: str) -> pd.DataFrame:
    """
    Load sales data for a specific product.

    Args:
        product: Product name

    Returns:
        pandas DataFrame with filtered sales records
    """
    query = """
        SELECT
            id,
            date as sale_date,
            product,
            revenue,
            closer,
            country,
            cash_collected,
            upsell
        FROM sales
        WHERE product = %s
        ORDER BY date
    """
    return query_to_dataframe(query, (product,))


def get_sales_by_closer(closer: str) -> pd.DataFrame:
    """
    Load sales data for a specific closer.

    Args:
        closer: Closer name

    Returns:
        pandas DataFrame with filtered sales records
    """
    query = """
        SELECT
            id,
            date as sale_date,
            product,
            revenue,
            closer,
            country,
            cash_collected,
            upsell
        FROM sales
        WHERE closer = %s
        ORDER BY date
    """
    return query_to_dataframe(query, (closer,))


def get_table_stats() -> Dict[str, Any]:
    """
    Get basic statistics about the sales table.

    Returns:
        Dictionary with table statistics
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Total rows
            cur.execute("SELECT COUNT(*) FROM sales")
            total_rows = cur.fetchone()[0]

            # Date range
            cur.execute("SELECT MIN(date), MAX(date) FROM sales")
            min_date, max_date = cur.fetchone()

            # Total revenue
            cur.execute("SELECT SUM(revenue) FROM sales")
            total_revenue = cur.fetchone()[0]

            # Distinct counts
            cur.execute("SELECT COUNT(DISTINCT product) FROM sales")
            distinct_products = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT closer) FROM sales")
            distinct_closers = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT country) FROM sales")
            distinct_countries = cur.fetchone()[0]

    return {
        "total_rows": total_rows,
        "date_range": (min_date, max_date),
        "total_revenue": float(total_revenue),
        "distinct_products": distinct_products,
        "distinct_closers": distinct_closers,
        "distinct_countries": distinct_countries,
    }
