# Setup Guide - Business Coaching Analytics

Complete step-by-step guide to set up the Business Coaching Analytics project from scratch, including troubleshooting common issues.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Database Configuration](#database-configuration)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software

#### 1. Python 3.12+

**Check if installed**:
```bash
python --version  # Should output Python 3.12.x or higher
```

**Install Python**:

**macOS (using Homebrew)**:
```bash
brew install python@3.12
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

**Windows**:
Download from [python.org](https://www.python.org/downloads/) and run installer

#### 2. PostgreSQL 14+

**Check if installed**:
```bash
psql --version  # Should output psql 14.x or higher
```

**Install PostgreSQL**:

**macOS (using Homebrew)**:
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows**:
Download from [postgresql.org](https://www.postgresql.org/download/windows/) and run installer

#### 3. uv Package Manager

**Install uv**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation**:
```bash
uv --version
```

#### 4. Git

**Check if installed**:
```bash
git --version
```

**Install Git**:
- **macOS**: `brew install git`
- **Ubuntu/Debian**: `sudo apt install git`
- **Windows**: Download from [git-scm.com](https://git-scm.com/downloads)

---

## Installation Steps

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd business-coach
```

If you don't have a repository yet:
```bash
# Create a new directory
mkdir business-coach
cd business-coach

# Initialize git
git init
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment with uv
uv venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

**Verify activation**:
Your prompt should now start with `(.venv)`

### Step 3: Install Dependencies

```bash
# Install all project dependencies
uv pip install -e .

# Verify installation
python -c "import pandas; import fastapi; import psycopg2; print('All dependencies installed successfully')"
```

**Expected output**:
```
All dependencies installed successfully
```

---

## Database Configuration

### Step 1: Start PostgreSQL

**macOS**:
```bash
brew services start postgresql@14
```

**Linux**:
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql  # Should show "active (running)"
```

**Windows**:
PostgreSQL should start automatically after installation. Check Services app.

### Step 2: Create Database User

```bash
# Connect to PostgreSQL as superuser
# macOS/Linux:
psql postgres

# Ubuntu (might need sudo):
sudo -u postgres psql
```

Once in psql:
```sql
-- Create user
CREATE USER coaching_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
ALTER USER coaching_user CREATEDB;

-- Exit psql
\q
```

### Step 3: Create Database

```bash
# Create database using command line
createdb -U coaching_user -h localhost coaching_analytics

# Or using psql
psql -U coaching_user -h localhost -d postgres
```

In psql:
```sql
CREATE DATABASE coaching_analytics OWNER coaching_user;
\c coaching_analytics
\q
```

### Step 4: Verify Database Connection

```bash
# Test connection
psql -U coaching_user -h localhost -d coaching_analytics -c "SELECT version();"
```

**Expected output**:
Should display PostgreSQL version information

---

## Environment Setup

### Step 1: Create .env File

```bash
# Copy example file
cp .env.example .env

# Edit the file
nano .env  # or use your preferred editor
```

### Step 2: Configure Environment Variables

Edit `.env` with your values:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=coaching_analytics
DB_USER=coaching_user
DB_PASSWORD=your_secure_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Optional: Sphinx.ai Integration (for AI features)
SPHINX_API_KEY=your_sphinx_api_key_here
```

**Important**: Replace `your_secure_password` with your actual PostgreSQL password

### Step 3: Verify Configuration

```bash
# Test configuration
python -c "from src.config import DB_CONFIG; print(f'Database: {DB_CONFIG[\"database\"]}')"
```

**Expected output**:
```
Database: coaching_analytics
```

---

## Running the Application

### Step 1: Initialize Database Schema

```bash
# Run database setup script
python src/db_setup.py
```

**Expected output**:
```
============================================================
Business Coaching Analytics - Database Setup
============================================================

Connecting to PostgreSQL at localhost:5432
Database: coaching_analytics
User: coaching_user

Step 1: Creating database...
 Database 'coaching_analytics' already exists

Step 2: Creating tables and indexes...
 Table 'sales' created successfully
 Index 'idx_sales_date' created successfully
 Index 'idx_sales_product' created successfully
 Index 'idx_sales_closer' created successfully
 Index 'idx_sales_country' created successfully
 Index 'idx_sales_date_product' created successfully
 Index 'idx_sales_date_closer' created successfully
 Index 'idx_sales_upsell' created successfully

 Database schema setup completed successfully

Step 3: Verifying setup...
 Verification: 'sales' table exists
 Verification: 8 indexes created
 Verification: 11 columns defined

============================================================
Database setup completed successfully!
============================================================

Next step: Run 'python src/load_data.py' to load the data
```

### Step 2: Generate and Load Data

```bash
# Generate mock data (if not already generated)
python src/data_generation.py

# Load data into database
python src/load_data.py
```

**Expected output for data loading**:
```
Loading data from: data/raw/coaching_sales_2025.csv
 Data loaded successfully
 195 records inserted

Verifying data load...
 Total records in database: 195

Sample records:
...
```

### Step 3: Verify Data

```bash
# Check row count
python -c "from src.db_utils import get_db_connection; import pandas as pd; conn = get_db_connection(); print(f'Total rows: {pd.read_sql(\"SELECT COUNT(*) FROM sales\", conn).iloc[0, 0]}')"
```

**Expected output**:
```
Total rows: 195
```

### Step 4: Start API Server

```bash
# Start FastAPI server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Will watch for changes in these directories: ['/path/to/business-coach']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 5: Test API

Open a new terminal and test:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test sales endpoint
curl http://localhost:8000/api/sales?page=1&page_size=5

# Or open in browser
open http://localhost:8000/docs  # macOS
# or visit http://localhost:8000/docs in your browser
```

---

## Verification

### Complete System Check

Run this comprehensive verification:

```bash
# Create verification script
cat > verify_setup.py << 'EOF'
"""Verify complete system setup"""
import sys

print("=" * 60)
print("System Verification")
print("=" * 60)

# 1. Check Python version
print("\n1. Python Version")
print(f"   {sys.version}")
assert sys.version_info >= (3, 12), "Python 3.12+ required"
print("    Python version OK")

# 2. Check imports
print("\n2. Required Packages")
try:
    import pandas
    print("    pandas")
    import numpy
    print("    numpy")
    import psycopg2
    print("    psycopg2")
    import fastapi
    print("    fastapi")
    import plotly
    print("    plotly")
except ImportError as e:
    print(f"    Missing package: {e}")
    sys.exit(1)

# 3. Check database connection
print("\n3. Database Connection")
try:
    from src.db_utils import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    print(f"    Connected to database")
    print(f"    Found {count} sales records")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"    Database error: {e}")
    sys.exit(1)

# 4. Check configuration
print("\n4. Configuration")
try:
    from src.config import DB_CONFIG, API_CONFIG
    print(f"    Database: {DB_CONFIG['database']}")
    print(f"    API Port: {API_CONFIG['port']}")
except Exception as e:
    print(f"    Config error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print(" All checks passed! System is ready.")
print("=" * 60)
EOF

# Run verification
python verify_setup.py
```

### Test Each Component

**Database**:
```bash
psql -U coaching_user -d coaching_analytics -c "SELECT COUNT(*), MIN(date), MAX(date) FROM sales;"
```

**Python Analysis**:
```bash
python src/data_analysis.py
```

**Visualizations**:
```bash
python src/visualizations.py
ls -lh outputs/visualizations/
```

**API**:
```bash
# In one terminal
uvicorn api.main:app --reload

# In another terminal
curl http://localhost:8000/api/metrics/summary | python -m json.tool
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:

a. **Check PostgreSQL is running**:
```bash
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Check port is listening
sudo lsof -i :5432  # macOS/Linux
netstat -an | find "5432"  # Windows
```

b. **Verify connection parameters**:
```bash
psql -U coaching_user -h localhost -d postgres
# If this works, database exists
# If this fails, check username/password
```

c. **Check pg_hba.conf** (Linux/macOS):
```bash
# Find config file
psql -U postgres -c "SHOW hba_file;"

# Edit config (example path)
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add or modify line:
host    all    all    127.0.0.1/32    md5
# or
host    all    all    127.0.0.1/32    scram-sha-256

# Restart PostgreSQL
sudo systemctl restart postgresql
```

d. **Reset password**:
```bash
# Connect as superuser
sudo -u postgres psql

# Reset password
ALTER USER coaching_user WITH PASSWORD 'new_secure_password';
\q

# Update .env file with new password
```

#### 2. Python Package Issues

**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solutions**:

a. **Verify virtual environment is activated**:
```bash
which python  # Should point to .venv/bin/python
```

b. **Reinstall dependencies**:
```bash
uv pip install --force-reinstall -e .
```

c. **Check Python version**:
```bash
python --version  # Must be 3.12+
```

d. **Clear package cache**:
```bash
uv cache clean
uv pip install -e .
```

#### 3. Port Already in Use

**Error**: `Address already in use` or `Port 8000 is already in use`

**Solutions**:

a. **Find process using port**:
```bash
# macOS/Linux
lsof -ti :8000

# Kill the process
kill -9 $(lsof -ti :8000)

# Windows
netstat -ano | findstr :8000
# Note the PID and kill it
taskkill /PID <PID> /F
```

b. **Use different port**:
```bash
uvicorn api.main:app --port 8001
```

#### 4. Data Loading Failures

**Error**: `FileNotFoundError: data/raw/coaching_sales_2025.csv`

**Solutions**:

a. **Generate data first**:
```bash
python src/data_generation.py
ls -l data/raw/coaching_sales_2025.csv
```

b. **Check directory structure**:
```bash
mkdir -p data/raw
python src/data_generation.py
```

c. **Verify CSV format**:
```bash
head -5 data/raw/coaching_sales_2025.csv
```

#### 5. Import Errors in Scripts

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solutions**:

a. **Run from project root**:
```bash
cd /path/to/business-coach
python src/data_analysis.py
```

b. **Add project to PYTHONPATH**:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/data_analysis.py
```

c. **Use module syntax**:
```bash
python -m src.data_analysis
```

#### 6. Visualization Display Issues

**Error**: `UserWarning: Matplotlib is currently using agg`

**Solutions**:

a. **Install display backend** (macOS):
```bash
brew install pkg-config
```

b. **Install tkinter** (Ubuntu):
```bash
sudo apt-get install python3-tk
```

c. **Use non-interactive backend**:
```python
# At top of script
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```

#### 7. Permission Denied Errors

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solutions**:

a. **Check file permissions**:
```bash
ls -l data/raw/
chmod 644 data/raw/*.csv
```

b. **Check directory permissions**:
```bash
chmod 755 data/ data/raw/ outputs/
```

c. **Database permissions**:
```sql
-- As postgres user
GRANT ALL PRIVILEGES ON DATABASE coaching_analytics TO coaching_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO coaching_user;
```

#### 8. Environment Variable Issues

**Error**: `KeyError: 'DB_PASSWORD'`

**Solutions**:

a. **Verify .env file exists**:
```bash
ls -la .env
cat .env  # Check contents
```

b. **Check .env format**:
```bash
# Must be KEY=VALUE format, no spaces around =
DB_PASSWORD=mypassword  # Correct
DB_PASSWORD = mypassword  # Incorrect
```

c. **Load environment manually**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('DB_PASSWORD'))  # Should print password
```

#### 9. API Returns Empty Results

**Error**: API returns `{"total": 0, "sales": []}`

**Solutions**:

a. **Verify data is loaded**:
```bash
psql -U coaching_user -d coaching_analytics -c "SELECT COUNT(*) FROM sales;"
```

b. **Check filters**:
```bash
# Try without filters
curl "http://localhost:8000/api/sales?page=1&page_size=10"
```

c. **Check database connection in API**:
```python
# In api/database.py, add print statements
print(f"Query returned {len(results)} rows")
```

#### 10. Slow Query Performance

**Issue**: Queries taking too long

**Solutions**:

a. **Verify indexes exist**:
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'sales';
```

b. **Analyze query plan**:
```sql
EXPLAIN ANALYZE
SELECT * FROM sales WHERE date >= '2025-01-01';
```

c. **Update statistics**:
```sql
ANALYZE sales;
VACUUM ANALYZE sales;
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change all default passwords
- [ ] Set strong `DB_PASSWORD` in `.env`
- [ ] Enable SSL for PostgreSQL
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Use environment-specific configs
- [ ] Set up reverse proxy (nginx)
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up error tracking (Sentry)
- [ ] Enable HTTPS
- [ ] Review security settings

### Production Environment Setup

**1. Database**:
```bash
# Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
# Or secure self-hosted PostgreSQL:

# postgresql.conf
ssl = on
max_connections = 100
shared_buffers = 256MB

# pg_hba.conf
hostssl all all 0.0.0.0/0 scram-sha-256
```

**2. API Server**:
```bash
# Use Gunicorn with Uvicorn workers
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**3. Reverse Proxy (nginx)**:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**4. Docker (Optional)**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install -e .

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Quick Reference

### Start Everything

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Start PostgreSQL (if not running)
brew services start postgresql@14  # macOS

# 3. Start API server
uvicorn api.main:app --reload
```

### Stop Everything

```bash
# 1. Stop API (Ctrl+C in terminal)

# 2. Deactivate virtual environment
deactivate

# 3. Stop PostgreSQL (optional)
brew services stop postgresql@14
```

### Reset Everything

```bash
# WARNING: This deletes all data

# 1. Drop and recreate database
dropdb -U coaching_user coaching_analytics
createdb -U coaching_user coaching_analytics

# 2. Reinitialize
python src/db_setup.py
python src/data_generation.py
python src/load_data.py
```

---

## Additional Resources

- [README.md](../README.md) - Project overview
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) - Data definitions

---

## Getting Help

If you encounter issues not covered here:

1. Check error logs
2. Review related documentation
3. Search GitHub issues
4. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System information
   - Relevant logs

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
