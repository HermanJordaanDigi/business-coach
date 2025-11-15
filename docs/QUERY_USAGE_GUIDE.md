# Quick Start Guide - SQL Query Execution

This guide shows you how to run the SQL queries and get insights from your coaching sales data.

---

## Prerequisites

1. PostgreSQL database running with data loaded
2. Python environment set up (Phase 1 & 2 complete)
3. All dependencies installed (`uv sync`)

---

## Quick Start

### 1. List Available Queries

See all 26 queries organized by category:

```bash
uv run python src/run_queries.py --list
```

**Output:**
```
REVENUE:
  - revenue_by_product
  - revenue_by_month

PERFORMANCE:
  - closer_performance
  - closer_product_matrix
  ...
```

---

### 2. Run Dashboard Summary

Get a quick overview of all key business metrics:

```bash
uv run python src/run_queries.py --category dashboard
```

**Shows:**
- Total deals and customers
- Total revenue and cash collected
- Collection and upsell rates
- Active closers and products
- Date ranges

---

### 3. Run All Queries

Execute all 26 queries at once:

```bash
uv run python src/run_queries.py
```

**Results:**
- Console output for each query
- CSV files in `outputs/query_results/csv/`
- JSON files in `outputs/query_results/json/`

---

## Query Categories

### Revenue Analysis

```bash
uv run python src/run_queries.py --category revenue
```

**Answers:**
- Which products generate the most revenue?
- What are our monthly revenue trends?
- What is our average deal size by product?

---

### Sales Team Performance

```bash
uv run python src/run_queries.py --category performance
```

**Answers:**
- Who are our top performing closers?
- What is each closer's average deal size?
- Which closers excel at which products?
- How do closers rank across multiple dimensions?

---

### Cash Collection Analysis

```bash
uv run python src/run_queries.py --category collection
```

**Answers:**
- What is our overall collection rate?
- Which products have the best collection rates?
- Which closers are best at collecting cash?
- How are payments distributed (fully paid vs. partial)?

---

### Geographic Analysis

```bash
uv run python src/run_queries.py --category geographic
```

**Answers:**
- Which countries generate the most revenue?
- What is the average deal size by region?
- Which products perform best in which countries?

---

### Upsell Analysis

```bash
uv run python src/run_queries.py --category upsell
```

**Answers:**
- What is our upsell rate?
- Which closers are best at upselling?
- How do upsell values compare to initial sales?
- Are upsell rates improving over time?

---

### Top Deals

```bash
uv run python src/run_queries.py --category top_deals
```

**Answers:**
- What are our biggest wins?
- What are the top deals for each product?
- Who closed the highest value deals?

---

### Cohort Analysis

```bash
uv run python src/run_queries.py --category cohort
```

**Answers:**
- How do monthly acquisition cohorts compare?
- Are product preferences changing over time?
- Which months had the best quality customers?

---

### Trends and Growth

```bash
uv run python src/run_queries.py --category trends
```

**Answers:**
- What is our month-over-month growth rate?
- What are our 3-month moving averages?
- What are our cumulative metrics?
- How do we compare year-over-year?

---

### Advanced Insights

```bash
uv run python src/run_queries.py --category advanced
```

**Answers:**
- Do customers buy multiple products?
- What is our deal size distribution?
- What is our sales velocity?

---

## Command Options

### Skip CSV Export

```bash
uv run python src/run_queries.py --no-csv
```

### Skip JSON Export

```bash
uv run python src/run_queries.py --no-json
```

### Skip Console Display

```bash
uv run python src/run_queries.py --no-display
```

Useful when you only want the export files.

### Control Display Rows

```bash
uv run python src/run_queries.py --max-rows 20
```

Show more rows in console output (default is 10).

### Combine Options

```bash
uv run python src/run_queries.py --category performance --no-json --max-rows 5
```

---

## Output Files

### CSV Files

**Location**: `outputs/query_results/csv/`

**Format**: `{query_name}_{timestamp}.csv`

**Example**: `revenue_by_product_20251115_130722.csv`

**Use for:**
- Excel analysis
- Data visualization tools
- Further data processing

---

### JSON Files

**Location**: `outputs/query_results/json/`

**Format**: `{query_name}_{timestamp}.json`

**Example**: `closer_performance_20251115_130722.json`

**Use for:**
- API integration
- Web applications
- JavaScript processing

---

## Common Workflows

### Daily Performance Review

```bash
# Quick dashboard check
uv run python src/run_queries.py --category dashboard

# Check sales team performance
uv run python src/run_queries.py --category performance --max-rows 20
```

---

### Weekly Business Review

```bash
# Run all analyses
uv run python src/run_queries.py

# Review outputs in outputs/query_results/csv/
# Import CSVs into Excel for presentations
```

---

### Monthly Deep Dive

```bash
# Get comprehensive insights
uv run python src/run_queries.py --category revenue
uv run python src/run_queries.py --category trends
uv run python src/run_queries.py --category cohort
uv run python src/run_queries.py --category advanced
```

---

### Executive Reporting

```bash
# Get key metrics only
uv run python src/run_queries.py --category dashboard --no-display

# Open: outputs/query_results/csv/business_dashboard_summary_*.csv
# Copy key numbers to presentation
```

---

## Using Query Results

### In Excel

1. Run queries with CSV export (default)
2. Navigate to `outputs/query_results/csv/`
3. Open CSV files in Excel
4. Create pivot tables, charts, and reports

---

### In Python/Pandas

```python
import pandas as pd

# Read exported CSV
df = pd.read_csv('outputs/query_results/csv/revenue_by_product_20251115_130722.csv')

# Analyze further
print(df.describe())
```

---

### In Web Applications

```javascript
// Read exported JSON
fetch('outputs/query_results/json/dashboard_summary.json')
  .then(response => response.json())
  .then(data => {
    // Display in web dashboard
    console.log(data);
  });
```

---

## Programmatic Usage

### Import in Python

```python
from src import sql_queries
from src.config import DB_CONFIG
import psycopg2
import pandas as pd

# Get a specific query
query = sql_queries.get_query('revenue_by_product')

# Execute it
conn = psycopg2.connect(**DB_CONFIG)
df = pd.read_sql_query(query, conn)
conn.close()

print(df)
```

---

### Custom Analysis

```python
from src.run_queries import run_query_suite

# Run specific categories programmatically
results = run_query_suite(
    category='revenue',
    export_csv=True,
    export_json=False,
    display=False
)

print(f"Executed {results['success_count']} queries successfully")
```

---

## Troubleshooting

### Database Connection Error

**Error**: `Error connecting to database`

**Solution**:
1. Check PostgreSQL is running
2. Verify `.env` file has correct credentials
3. Test connection: `psql -U [username] -d coaching_analytics`

---

### Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'psycopg2'`

**Solution**:
```bash
uv sync
```

---

### No Results Returned

**Error**: Query returns 0 rows

**Solution**:
1. Check data is loaded: `uv run python src/load_data.py`
2. Verify with: `SELECT COUNT(*) FROM sales;`

---

### Permission Denied

**Error**: Can't write to outputs directory

**Solution**:
```bash
mkdir -p outputs/query_results/csv outputs/query_results/json
chmod 755 outputs
```

---

## Next Steps

Once you're comfortable running queries:

1. **Explore Results**: Review CSV outputs in Excel
2. **Customize Queries**: Modify `src/sql_queries.py` to add new queries
3. **Automate**: Set up scheduled query runs (cron jobs)
4. **Integrate**: Use JSON outputs in dashboards or APIs

---

## Additional Resources

- **Full Documentation**: `docs/sql_queries_documentation.md`
- **Query Library**: `src/sql_queries.py`
- **Execution Script**: `src/run_queries.py`
- **Phase 3 Summary**: `PHASE3_COMPLETE.md`

---

## Support

For detailed query documentation, including business context and sample insights, see:
[SQL Queries Documentation](sql_queries_documentation.md)

---

**Quick Reference:**

```bash
# List all queries
uv run python src/run_queries.py --list

# Run dashboard
uv run python src/run_queries.py --category dashboard

# Run specific category
uv run python src/run_queries.py --category [revenue|performance|collection|geographic|upsell|top_deals|cohort|trends|advanced]

# Run all queries
uv run python src/run_queries.py
```

---

*Last Updated: 2025-11-15 | Phase 3: SQL Analysis & Queries*
