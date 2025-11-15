# Phase 2: Database Setup Guide

## Overview
Phase 2 focuses on setting up PostgreSQL database and loading the coaching sales data.

## Prerequisites

### 1. Install PostgreSQL

**Option A: Using Homebrew (Recommended for macOS)**
```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Add PostgreSQL to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"

# Verify installation
psql --version
```

**Option B: Using Docker**
```bash
# Run PostgreSQL in Docker
docker run --name coaching-analytics-db \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16

# Verify container is running
docker ps | grep coaching-analytics-db
```

**Option C: Download from postgresql.org**
- Visit https://www.postgresql.org/download/
- Download and install PostgreSQL 16 or later
- Follow the installation wizard

### 2. Verify Installation

Test that PostgreSQL is running:
```bash
# Test connection to PostgreSQL
psql -U postgres -c "SELECT version();"
```

### 3. Create Environment Configuration

Create a `.env` file in the project root (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` and update database credentials if needed:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=coaching_analytics
DB_USER=postgres
DB_PASSWORD=postgres  # Change to your actual password
```

## Phase 2 Execution Steps

### Step 1: Set Up Database Schema

Run the database setup script to create the database and tables:

```bash
python src/db_setup.py
```

**What this does:**
- Creates `coaching_analytics` database if it doesn't exist
- Creates `sales` table with proper schema:
  - Columns: id, date, name, email, revenue, cash_collected, product, closer, country, upsell, created_at
  - Constraints: Primary key, NOT NULL, CHECK constraints
  - Validation: country in (US, UK, EU), valid products, cash_collected <= revenue
- Creates 7 indexes for query optimization:
  - idx_sales_date
  - idx_sales_product
  - idx_sales_closer
  - idx_sales_country
  - idx_sales_date_product
  - idx_sales_date_closer
  - idx_sales_upsell
- Verifies the setup

**Expected output:**
```
============================================================
Business Coaching Analytics - Database Setup
============================================================
Connecting to PostgreSQL at localhost:5432
Database: coaching_analytics
User: postgres

Step 1: Creating database...
✓ Database 'coaching_analytics' created successfully

Step 2: Creating tables and indexes...
✓ Table 'sales' created successfully
✓ Index 'idx_sales_date' created successfully
✓ Index 'idx_sales_product' created successfully
...

✓ Database schema setup completed successfully
```

### Step 2: Load CSV Data

Load the generated CSV data into PostgreSQL:

```bash
python src/load_data.py
```

**What this does:**
- Reads `data/raw/coaching_sales_2025.csv`
- Loads 195 rows into the `sales` table
- Converts data types (boolean for upsell, decimals for money)
- Shows loading progress
- Performs comprehensive verification:
  - Row count
  - Date range
  - Revenue statistics
  - Sales by product, closer, country
  - Upsell statistics
  - Cash collection rates
  - Sample records

**Expected output:**
```
============================================================
Business Coaching Analytics - Data Loading
============================================================
Database: coaching_analytics
CSV File: /path/to/data/raw/coaching_sales_2025.csv

Starting data load...

Reading data from: /path/to/data/raw/coaching_sales_2025.csv
  Loaded 50 rows...
  Loaded 100 rows...
  Loaded 150 rows...

✓ Successfully loaded 195 rows into database

============================================================
Data Verification
============================================================

✓ Total rows in database: 195
✓ Date range: 2025-01-02 to 2025-11-29

✓ Revenue Statistics:
  - Total Sales: 195
  - Total Revenue: $4,725,000.00
  - Average Revenue: $24,230.77
  ...
```

### Step 3: Test Database Utilities

Test the database utility functions:

```bash
python src/db_utils.py
```

**What this does:**
- Tests database connection
- Retrieves table statistics
- Tests various query execution methods
- Tests DataFrame loading
- Tests column statistics

### Step 4: Manual Verification (Optional)

Connect to PostgreSQL and run queries manually:

```bash
# Connect to database
psql -U postgres -d coaching_analytics

# In psql, run queries:
\dt              # List tables
\d sales         # Describe sales table
\di              # List indexes

SELECT COUNT(*) FROM sales;
SELECT * FROM sales LIMIT 5;
SELECT closer, COUNT(*), SUM(revenue) FROM sales GROUP BY closer;

# Exit psql
\q
```

## Troubleshooting

### Issue: "psql: command not found"
**Solution:** PostgreSQL is not installed or not in PATH
- Install PostgreSQL using one of the methods above
- Add PostgreSQL to your PATH

### Issue: "Connection refused"
**Solution:** PostgreSQL service is not running
```bash
# For Homebrew installation
brew services start postgresql@16

# For Docker installation
docker start coaching-analytics-db

# Check PostgreSQL status
brew services list | grep postgresql
# or
docker ps | grep coaching-analytics-db
```

### Issue: "password authentication failed"
**Solution:** Update credentials in `.env` file
- Check your PostgreSQL password
- Update `DB_PASSWORD` in `.env`
- For new installations, default password is often empty or "postgres"

### Issue: "database does not exist"
**Solution:** Run the setup script first
```bash
python src/db_setup.py
```

### Issue: "Permission denied"
**Solution:** Grant permissions to PostgreSQL user
```bash
# Connect as superuser
psql -U postgres

# Grant permissions
GRANT ALL PRIVILEGES ON DATABASE coaching_analytics TO postgres;
```

## Files Created in Phase 2

```
business-coach/
├── src/
│   ├── db_setup.py       # Database and schema creation
│   ├── load_data.py      # CSV data loading
│   └── db_utils.py       # Reusable database utilities
├── .env.example          # Environment configuration template
├── .env                  # Your actual configuration (git-ignored)
└── PHASE2_SETUP.md      # This guide
```

## Database Schema

### Table: sales

| Column          | Type          | Constraints                    |
|----------------|---------------|--------------------------------|
| id             | SERIAL        | PRIMARY KEY                    |
| date           | DATE          | NOT NULL                       |
| name           | VARCHAR(100)  | NOT NULL                       |
| email          | VARCHAR(100)  | NOT NULL                       |
| revenue        | DECIMAL(10,2) | NOT NULL, CHECK (revenue > 0)  |
| cash_collected | DECIMAL(10,2) | NOT NULL, CHECK (>= 0)        |
| product        | VARCHAR(100)  | NOT NULL, CHECK (valid values) |
| closer         | VARCHAR(50)   | NOT NULL                       |
| country        | VARCHAR(10)   | NOT NULL, CHECK (US/UK/EU)    |
| upsell         | BOOLEAN       | NOT NULL, DEFAULT FALSE        |
| created_at     | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP      |

## Key Statistics (After Loading)

- **Total Records:** 195
- **Date Range:** January 1 - November 30, 2025
- **Total Revenue:** ~$4.7M
- **Average Deal Size:** ~$24,231
- **Products:** 3 (Elite Business Accelerator, Executive Leadership Mastery, Scale to 7-Figures)
- **Closers:** 3 (Sarah Mitchell, Marcus Thompson, Julia Rodriguez)
- **Countries:** 3 (US, UK, EU)

## Next Steps

After completing Phase 2, proceed to:
- **Phase 3:** SQL Analysis & Queries
- **Phase 4:** Python Data Analysis
- **Phase 5:** Data Visualization
- **Phase 6:** API Development & Sphinx.ai Integration

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [pandas SQL Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)
