"""
Database utility functions for the Business Coaching Analytics project.
Provides reusable connection and query execution helpers.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from config import DB_CONFIG


@contextmanager
def get_db_connection(cursor_factory=None):
    """
    Context manager for database connections.
    Automatically handles connection closing and error rollback.

    Args:
        cursor_factory: Optional cursor factory (e.g., RealDictCursor)

    Yields:
        psycopg2.connection: Database connection object

    Example:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sales")
            results = cursor.fetchall()
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            cursor_factory=cursor_factory
        )
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def execute_query(query: str, params: Optional[tuple] = None, fetch: str = "all") -> List[Any]:
    """
    Execute a SELECT query and return results.

    Args:
        query: SQL query string
        params: Optional query parameters for parameterized queries
        fetch: "all", "one", or "none" to specify fetch behavior

    Returns:
        Query results as list of tuples (or single tuple if fetch="one")

    Example:
        results = execute_query("SELECT * FROM sales WHERE closer = %s", ("Sarah Mitchell",))
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if fetch == "all":
            return cursor.fetchall()
        elif fetch == "one":
            return cursor.fetchone()
        else:
            return []


def execute_query_dict(query: str, params: Optional[tuple] = None, fetch: str = "all") -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries.

    Args:
        query: SQL query string
        params: Optional query parameters
        fetch: "all", "one", or "none" to specify fetch behavior

    Returns:
        Query results as list of dictionaries

    Example:
        results = execute_query_dict("SELECT * FROM sales WHERE country = %s", ("US",))
        # Returns: [{"id": 1, "date": "2025-01-01", ...}, ...]
    """
    with get_db_connection(cursor_factory=RealDictCursor) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if fetch == "all":
            return [dict(row) for row in cursor.fetchall()]
        elif fetch == "one":
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            return []


def execute_update(query: str, params: Optional[tuple] = None) -> int:
    """
    Execute an INSERT, UPDATE, or DELETE query.

    Args:
        query: SQL query string
        params: Optional query parameters

    Returns:
        Number of rows affected

    Example:
        rows_updated = execute_update(
            "UPDATE sales SET revenue = %s WHERE id = %s",
            (25000, 1)
        )
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.rowcount


def query_to_dataframe(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Execute a query and return results as a pandas DataFrame.

    Args:
        query: SQL query string
        params: Optional query parameters

    Returns:
        pandas DataFrame with query results

    Example:
        df = query_to_dataframe("SELECT * FROM sales WHERE date >= %s", ("2025-01-01",))
    """
    with get_db_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def load_table_to_dataframe(table_name: str, columns: str = "*",
                             where_clause: str = "", params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Load a complete table or filtered subset into a pandas DataFrame.

    Args:
        table_name: Name of the table to load
        columns: Columns to select (default: "*")
        where_clause: Optional WHERE clause (without "WHERE" keyword)
        params: Optional parameters for WHERE clause

    Returns:
        pandas DataFrame with table data

    Example:
        df = load_table_to_dataframe("sales", columns="date, revenue, closer")
        df = load_table_to_dataframe("sales", where_clause="country = %s", params=("US",))
    """
    query = f"SELECT {columns} FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"

    return query_to_dataframe(query, params)


def get_table_stats(table_name: str) -> Dict[str, Any]:
    """
    Get basic statistics about a table.

    Args:
        table_name: Name of the table

    Returns:
        Dictionary with table statistics

    Example:
        stats = get_table_stats("sales")
        print(f"Total rows: {stats['row_count']}")
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        # Get column information
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            ORDER BY ordinal_position
        """, (table_name,))
        columns = cursor.fetchall()

        # Get table size
        cursor.execute("""
            SELECT pg_size_pretty(pg_total_relation_size(%s))
        """, (table_name,))
        table_size = cursor.fetchone()[0]

        return {
            "table_name": table_name,
            "row_count": row_count,
            "column_count": len(columns),
            "columns": [{"name": col[0], "type": col[1]} for col in columns],
            "table_size": table_size
        }


def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        True if connection successful, False otherwise

    Example:
        if test_connection():
            print("Database connection successful")
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result[0] == 1
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False


def execute_query_batch(queries: List[tuple]) -> List[int]:
    """
    Execute multiple queries in a single transaction.

    Args:
        queries: List of tuples (query, params)

    Returns:
        List of row counts for each query

    Example:
        queries = [
            ("INSERT INTO sales (...) VALUES (...)", (values1,)),
            ("INSERT INTO sales (...) VALUES (...)", (values2,))
        ]
        results = execute_query_batch(queries)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        row_counts = []

        for query, params in queries:
            cursor.execute(query, params)
            row_counts.append(cursor.rowcount)

        return row_counts


def get_column_stats(table_name: str, column_name: str) -> Dict[str, Any]:
    """
    Get statistics for a specific column.

    Args:
        table_name: Name of the table
        column_name: Name of the column

    Returns:
        Dictionary with column statistics

    Example:
        stats = get_column_stats("sales", "revenue")
    """
    query = f"""
        SELECT
            COUNT(*) as total_count,
            COUNT({column_name}) as non_null_count,
            COUNT(DISTINCT {column_name}) as unique_count
        FROM {table_name}
    """

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        total, non_null, unique = cursor.fetchone()

        # Check data type
        cursor.execute("""
            SELECT data_type
            FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s
        """, (table_name, column_name))
        data_type = cursor.fetchone()[0]

        stats = {
            "column_name": column_name,
            "data_type": data_type,
            "total_count": total,
            "non_null_count": non_null,
            "null_count": total - non_null,
            "unique_count": unique,
        }

        # Add numeric stats if applicable
        if data_type in ('numeric', 'integer', 'bigint', 'double precision', 'real'):
            cursor.execute(f"""
                SELECT
                    MIN({column_name}) as min_value,
                    MAX({column_name}) as max_value,
                    AVG({column_name}) as avg_value,
                    STDDEV({column_name}) as stddev_value
                FROM {table_name}
                WHERE {column_name} IS NOT NULL
            """)
            min_val, max_val, avg_val, stddev_val = cursor.fetchone()
            stats.update({
                "min": float(min_val) if min_val is not None else None,
                "max": float(max_val) if max_val is not None else None,
                "avg": float(avg_val) if avg_val is not None else None,
                "stddev": float(stddev_val) if stddev_val is not None else None,
            })

        return stats


# Example usage and tests
if __name__ == "__main__":
    print("Testing database utility functions...")
    print("=" * 60)

    # Test connection
    print("\n1. Testing connection...")
    if test_connection():
        print("✓ Connection successful")
    else:
        print("✗ Connection failed")
        exit(1)

    # Get table stats
    print("\n2. Getting table statistics...")
    try:
        stats = get_table_stats("sales")
        print(f"✓ Table: {stats['table_name']}")
        print(f"  - Rows: {stats['row_count']}")
        print(f"  - Columns: {stats['column_count']}")
        print(f"  - Size: {stats['table_size']}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test query execution
    print("\n3. Testing query execution...")
    try:
        result = execute_query("SELECT COUNT(*) FROM sales", fetch="one")
        print(f"✓ Row count: {result[0]}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test dictionary query
    print("\n4. Testing dictionary query...")
    try:
        results = execute_query_dict("SELECT * FROM sales LIMIT 3")
        print(f"✓ Retrieved {len(results)} records as dictionaries")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test DataFrame loading
    print("\n5. Testing DataFrame loading...")
    try:
        df = load_table_to_dataframe("sales")
        print(f"✓ Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test column stats
    print("\n6. Testing column statistics...")
    try:
        col_stats = get_column_stats("sales", "revenue")
        print(f"✓ Revenue column stats:")
        print(f"  - Min: ${col_stats.get('min', 0):,.2f}")
        print(f"  - Max: ${col_stats.get('max', 0):,.2f}")
        print(f"  - Avg: ${col_stats.get('avg', 0):,.2f}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "=" * 60)
    print("✓ Database utility tests completed")
