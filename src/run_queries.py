"""
Query Execution Script for Business Coaching Analytics

This script executes all analytical SQL queries and exports results to multiple formats:
- CSV files for data analysis
- JSON files for API/web consumption
- Formatted console output for quick review

Usage:
    python src/run_queries.py                    # Run all queries
    python src/run_queries.py --query revenue    # Run specific query category
    python src/run_queries.py --list             # List all available queries
"""

import pandas as pd
import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import argparse
from typing import Dict, List, Any, Optional

from config import DB_CONFIG
import sql_queries
# Import centralized database utilities
from db_utils import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directories
OUTPUTS_DIR = Path("outputs")
QUERIES_OUTPUT_DIR = OUTPUTS_DIR / "query_results"
CSV_OUTPUT_DIR = QUERIES_OUTPUT_DIR / "csv"
JSON_OUTPUT_DIR = QUERIES_OUTPUT_DIR / "json"

# Create output directories
for dir_path in [OUTPUTS_DIR, QUERIES_OUTPUT_DIR, CSV_OUTPUT_DIR, JSON_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


# ============================================================================
# QUERY EXECUTION
# ============================================================================

def execute_query(conn, query_name: str, query_sql: str) -> Optional[pd.DataFrame]:
    """
    Execute a SQL query and return results as a DataFrame.

    Args:
        conn: Database connection
        query_name: Name of the query for logging
        query_sql: SQL query string to execute

    Returns:
        pandas DataFrame with query results, or None if error
    """
    try:
        print(f"  Executing {query_name}...")
        df = pd.read_sql_query(query_sql, conn)
        print(f"  ✓ {query_name}: {len(df)} rows returned")
        return df
    except Exception as e:
        print(f"  ✗ Error executing {query_name}: {e}")
        return None


def export_to_csv(df: pd.DataFrame, query_name: str) -> str:
    """
    Export DataFrame to CSV file.

    Args:
        df: DataFrame to export
        query_name: Name for the output file

    Returns:
        Path to the exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{query_name}_{timestamp}.csv"
    filepath = CSV_OUTPUT_DIR / filename

    df.to_csv(filepath, index=False)
    return str(filepath)


def export_to_json(df: pd.DataFrame, query_name: str) -> str:
    """
    Export DataFrame to JSON file.

    Args:
        df: DataFrame to export
        query_name: Name for the output file

    Returns:
        Path to the exported file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{query_name}_{timestamp}.json"
    filepath = JSON_OUTPUT_DIR / filename

    # Convert DataFrame to JSON with proper formatting
    df.to_json(filepath, orient='records', indent=2, date_format='iso')
    return str(filepath)


def display_results(df: pd.DataFrame, query_name: str, max_rows: int = 10):
    """
    Display query results in formatted console output.

    Args:
        df: DataFrame to display
        query_name: Name of the query
        max_rows: Maximum number of rows to display
    """
    print(f"\n{'=' * 80}")
    print(f"Query: {query_name}")
    print(f"{'=' * 80}")

    if df is None or df.empty:
        print("No results returned.")
        return

    print(f"\nTotal rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns.tolist())}\n")

    # Display first N rows
    if len(df) > max_rows:
        print(f"Showing first {max_rows} rows:\n")
        print(df.head(max_rows).to_string(index=False))
        print(f"\n... and {len(df) - max_rows} more rows")
    else:
        print(df.to_string(index=False))

    print(f"\n{'=' * 80}\n")


# ============================================================================
# QUERY CATEGORIES
# ============================================================================

QUERY_CATEGORIES = {
    'revenue': [
        'revenue_by_product',
        'revenue_by_month',
    ],
    'performance': [
        'closer_performance',
        'closer_product_matrix',
        'closer_efficiency_ranking',
    ],
    'collection': [
        'cash_collection_analysis',
        'cash_collection_by_closer',
        'collection_status_distribution',
    ],
    'geographic': [
        'geographic_distribution',
        'country_product_performance',
    ],
    'upsell': [
        'upsell_analysis',
        'upsell_by_closer',
        'upsell_by_month',
    ],
    'top_deals': [
        'top_10_deals',
        'top_deals_by_product',
    ],
    'cohort': [
        'monthly_cohort_analysis',
        'cohort_product_mix',
    ],
    'trends': [
        'running_totals',
        'moving_averages_by_month',
        'revenue_growth_rates',
        'year_over_year_comparison',
        'quarterly_comparison',
    ],
    'advanced': [
        'product_cannibalization_analysis',
        'deal_size_distribution',
        'sales_velocity_metrics',
    ],
    'dashboard': [
        'business_dashboard_summary',
    ],
}


def get_queries_by_category(category: Optional[str] = None) -> List[str]:
    """
    Get list of queries by category.

    Args:
        category: Category name, or None for all queries

    Returns:
        List of query names
    """
    if category is None:
        return sql_queries.list_available_queries()

    if category in QUERY_CATEGORIES:
        return QUERY_CATEGORIES[category]

    print(f"✗ Unknown category: {category}")
    print(f"Available categories: {', '.join(QUERY_CATEGORIES.keys())}")
    sys.exit(1)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_query_suite(
    category: Optional[str] = None,
    export_csv: bool = True,
    export_json: bool = True,
    display: bool = True,
    max_display_rows: int = 10
) -> Dict[str, Any]:
    """
    Run a suite of queries and export results.

    Args:
        category: Query category to run (None for all)
        export_csv: Whether to export results to CSV
        export_json: Whether to export results to JSON
        display: Whether to display results in console
        max_display_rows: Maximum rows to display per query

    Returns:
        Dictionary with execution results and statistics
    """
    print("=" * 80)
    print("Business Coaching Analytics - Query Execution")
    print("=" * 80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get database connection
    print(f"\nConnecting to database: {DB_CONFIG['database']}...")
    conn = get_db_connection()
    print("✓ Connected successfully\n")

    # Get queries to run
    query_names = get_queries_by_category(category)
    category_label = category if category else "all"
    print(f"Running {len(query_names)} queries from category: {category_label}\n")

    # Execute queries
    results = {}
    exported_files = {'csv': [], 'json': []}
    success_count = 0
    error_count = 0

    for query_name in query_names:
        try:
            # Get query SQL
            query_sql = sql_queries.get_query(query_name)

            # Execute query
            df = execute_query(conn, query_name, query_sql)

            if df is not None:
                results[query_name] = {
                    'rows': len(df),
                    'columns': df.columns.tolist(),
                    'success': True
                }

                # Export to CSV
                if export_csv and not df.empty:
                    csv_path = export_to_csv(df, query_name)
                    exported_files['csv'].append(csv_path)
                    results[query_name]['csv_file'] = csv_path

                # Export to JSON
                if export_json and not df.empty:
                    json_path = export_to_json(df, query_name)
                    exported_files['json'].append(json_path)
                    results[query_name]['json_file'] = json_path

                # Display results
                if display:
                    display_results(df, query_name, max_display_rows)

                success_count += 1
            else:
                results[query_name] = {
                    'success': False,
                    'error': 'Query returned no results'
                }
                error_count += 1

        except Exception as e:
            print(f"  ✗ Error processing {query_name}: {e}")
            results[query_name] = {
                'success': False,
                'error': str(e)
            }
            error_count += 1

    # Close connection
    conn.close()
    print("✓ Database connection closed\n")

    # Summary
    print("=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total queries: {len(query_names)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {error_count}")

    if exported_files['csv']:
        print(f"\nCSV files exported: {len(exported_files['csv'])}")
        print(f"Location: {CSV_OUTPUT_DIR}")

    if exported_files['json']:
        print(f"\nJSON files exported: {len(exported_files['json'])}")
        print(f"Location: {JSON_OUTPUT_DIR}")

    print("\n" + "=" * 80)

    return {
        'results': results,
        'exported_files': exported_files,
        'success_count': success_count,
        'error_count': error_count,
        'timestamp': datetime.now().isoformat()
    }


def list_queries():
    """List all available queries organized by category."""
    print("=" * 80)
    print("Available Query Categories and Queries")
    print("=" * 80)

    for category, queries in QUERY_CATEGORIES.items():
        print(f"\n{category.upper()}:")
        for query in queries:
            print(f"  - {query}")

    print(f"\nTotal queries available: {len(sql_queries.list_available_queries())}")
    print("\nUsage:")
    print("  python src/run_queries.py --category revenue")
    print("  python src/run_queries.py --category performance")
    print("  python src/run_queries.py  (run all queries)")
    print("=" * 80)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Execute SQL queries and export results',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--category',
        '-c',
        type=str,
        help='Query category to run (revenue, performance, collection, etc.)'
    )

    parser.add_argument(
        '--list',
        '-l',
        action='store_true',
        help='List all available queries and categories'
    )

    parser.add_argument(
        '--no-csv',
        action='store_true',
        help='Skip CSV export'
    )

    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Skip JSON export'
    )

    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Skip console display of results'
    )

    parser.add_argument(
        '--max-rows',
        type=int,
        default=10,
        help='Maximum rows to display per query (default: 10)'
    )

    args = parser.parse_args()

    # List queries and exit
    if args.list:
        list_queries()
        sys.exit(0)

    # Run query suite
    try:
        results = run_query_suite(
            category=args.category,
            export_csv=not args.no_csv,
            export_json=not args.no_json,
            display=not args.no_display,
            max_display_rows=args.max_rows
        )

        # Exit with error code if any queries failed
        if results['error_count'] > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n✗ Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
