"""
Database connection and query utilities for the API.

This module uses the centralized database utilities from src/db_utils.py.
"""
from typing import List, Dict, Any, Optional
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from src.db_utils import get_db_connection, execute_query_dict


def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries.

    Args:
        query: SQL query string
        params: Query parameters tuple

    Returns:
        List of dictionaries representing rows
    """
    return execute_query_dict(query, params, fetch="all")


def execute_single_query(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """
    Execute a SELECT query and return a single result as dictionary.

    Args:
        query: SQL query string
        params: Query parameters tuple

    Returns:
        Dictionary representing the row, or None if no results
    """
    return execute_query_dict(query, params, fetch="one")


def get_all_sales(
    page: int = 1,
    page_size: int = 50,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product: Optional[str] = None,
    closer: Optional[str] = None,
    country: Optional[str] = None,
) -> tuple[List[Dict[str, Any]], int]:
    """
    Get all sales with pagination and optional filtering.

    Returns:
        Tuple of (sales_list, total_count)
    """
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    if product:
        where_clauses.append("product = %s")
        params.append(product)

    if closer:
        where_clauses.append("closer = %s")
        params.append(closer)

    if country:
        where_clauses.append("country = %s")
        params.append(country)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Get total count
    count_query = f"SELECT COUNT(*) as total FROM sales WHERE {where_sql}"
    count_result = execute_single_query(count_query, tuple(params))
    total = count_result['total'] if count_result else 0

    # Get paginated results
    offset = (page - 1) * page_size
    params.extend([page_size, offset])

    query = f"""
        SELECT id as sale_id, date as sale_date, product, revenue, cash_collected,
               closer, country, upsell
        FROM sales
        WHERE {where_sql}
        ORDER BY date DESC, id DESC
        LIMIT %s OFFSET %s
    """

    sales = execute_query(query, tuple(params))
    return sales, total


def get_sale_by_id(sale_id: int) -> Optional[Dict[str, Any]]:
    """Get a single sale by ID"""
    query = """
        SELECT id as sale_id, date as sale_date, product, revenue, cash_collected,
               closer, country, upsell
        FROM sales
        WHERE id = %s
    """
    return execute_single_query(query, (sale_id,))


def get_metrics_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product: Optional[str] = None,
    closer: Optional[str] = None,
    country: Optional[str] = None,
) -> Dict[str, Any]:
    """Get summary metrics with optional filtering"""
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    if product:
        where_clauses.append("product = %s")
        params.append(product)

    if closer:
        where_clauses.append("closer = %s")
        params.append(closer)

    if country:
        where_clauses.append("country = %s")
        params.append(country)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT
            COUNT(*) as total_sales,
            SUM(revenue) as total_revenue,
            SUM(cash_collected) as total_cash_collected,
            AVG(revenue) as average_deal_size,
            (SUM(cash_collected) / NULLIF(SUM(revenue), 0) * 100) as cash_collection_rate,
            (SUM(CASE WHEN upsell THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0) * 100) as upsell_rate,
            COUNT(DISTINCT closer) as unique_closers
        FROM sales
        WHERE {where_sql}
    """

    result = execute_single_query(query, tuple(params))

    if not result or result['total_sales'] == 0:
        return {
            'total_revenue': 0.0,
            'total_cash_collected': 0.0,
            'total_sales': 0,
            'average_deal_size': 0.0,
            'cash_collection_rate': 0.0,
            'upsell_rate': 0.0,
            'unique_closers': 0
        }

    return result


def get_metrics_by_product(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Get metrics grouped by product"""
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT
            product,
            COUNT(*) as total_sales,
            SUM(revenue) as total_revenue,
            AVG(revenue) as average_deal_size,
            (SUM(cash_collected) / NULLIF(SUM(revenue), 0) * 100) as cash_collection_rate,
            (SUM(CASE WHEN upsell THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0) * 100) as upsell_rate
        FROM sales
        WHERE {where_sql}
        GROUP BY product
        ORDER BY total_revenue DESC
    """

    return execute_query(query, tuple(params) if params else None)


def get_metrics_by_closer(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Get metrics grouped by closer"""
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT
            closer,
            COUNT(*) as total_sales,
            SUM(revenue) as total_revenue,
            AVG(revenue) as average_deal_size,
            (SUM(cash_collected) / NULLIF(SUM(revenue), 0) * 100) as cash_collection_rate,
            (SUM(CASE WHEN upsell THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0) * 100) as upsell_rate
        FROM sales
        WHERE {where_sql}
        GROUP BY closer
        ORDER BY total_revenue DESC
    """

    return execute_query(query, tuple(params) if params else None)


def get_metrics_by_country(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Get metrics grouped by country"""
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        WITH country_totals AS (
            SELECT
                country,
                COUNT(*) as total_sales,
                SUM(revenue) as total_revenue,
                AVG(revenue) as average_deal_size
            FROM sales
            WHERE {where_sql}
            GROUP BY country
        ),
        grand_total AS (
            SELECT SUM(revenue) as grand_total_revenue
            FROM sales
            WHERE {where_sql}
        )
        SELECT
            ct.country,
            ct.total_sales,
            ct.total_revenue,
            ct.average_deal_size,
            (ct.total_revenue / NULLIF(gt.grand_total_revenue, 0) * 100) as revenue_percentage
        FROM country_totals ct
        CROSS JOIN grand_total gt
        ORDER BY ct.total_revenue DESC
    """

    return execute_query(query, tuple(params) if params else None)


def get_time_series_metrics(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Get metrics as time series by month"""
    where_clauses = []
    params = []

    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT
            TO_CHAR(date, 'YYYY-MM') as period,
            COUNT(*) as total_sales,
            SUM(revenue) as total_revenue,
            AVG(revenue) as average_deal_size
        FROM sales
        WHERE {where_sql}
        GROUP BY TO_CHAR(date, 'YYYY-MM')
        ORDER BY period
    """

    return execute_query(query, tuple(params) if params else None)
