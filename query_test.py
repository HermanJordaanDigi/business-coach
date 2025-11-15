"""
Quick script to test database queries.
Run with: uv run python query_test.py
"""
import sys
sys.path.append('src')

from db_utils import execute_query, execute_query_dict, query_to_dataframe

print("=" * 60)
print("Testing Database Queries")
print("=" * 60)

# Query 1: Row count
print("\n1. Total row count:")
result = execute_query("SELECT COUNT(*) FROM sales", fetch="one")
print(f"   {result[0]} rows")

# Query 2: Revenue by closer
print("\n2. Revenue by closer:")
query = """
    SELECT
        closer,
        COUNT(*) as deals,
        SUM(revenue) as total_revenue,
        AVG(revenue) as avg_deal_size
    FROM sales
    GROUP BY closer
    ORDER BY total_revenue DESC
"""
results = execute_query(query)
for closer, deals, revenue, avg_size in results:
    print(f"   {closer:20} {deals:3} deals  ${revenue:>12,.2f}  (avg: ${avg_size:,.2f})")

# Query 3: Top 5 deals
print("\n3. Top 5 highest value deals:")
query = """
    SELECT date, name, product, revenue, closer, country
    FROM sales
    ORDER BY revenue DESC, date DESC
    LIMIT 5
"""
results = execute_query_dict(query)
for i, row in enumerate(results, 1):
    print(f"   {i}. ${row['revenue']:>8,.2f} - {row['name']:25} | {row['product'][:30]}")
    print(f"      {row['date']} | {row['closer']} | {row['country']}")

# Query 4: Monthly revenue
print("\n4. Revenue by month:")
query = """
    SELECT
        TO_CHAR(date, 'YYYY-MM') as month,
        COUNT(*) as sales,
        SUM(revenue) as revenue
    FROM sales
    GROUP BY TO_CHAR(date, 'YYYY-MM')
    ORDER BY month
"""
results = execute_query(query)
for month, sales, revenue in results:
    print(f"   {month}: {sales:3} sales, ${revenue:>10,.2f}")

# Query 5: Load data into DataFrame
print("\n5. Loading data into pandas DataFrame:")
df = query_to_dataframe("SELECT * FROM sales")
print(f"   Loaded {len(df)} rows, {len(df.columns)} columns")
print(f"   Columns: {', '.join(df.columns[:5])}...")

print("\n" + "=" * 60)
print("✓ All queries executed successfully!")
print("=" * 60)
