"""
Database setup script for the Business Coaching Analytics project.
Creates the PostgreSQL database and tables with appropriate schema.
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from config import DB_CONFIG


def create_database():
    """Create the coaching_analytics database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server (default postgres database)
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG["database"],)
        )
        exists = cursor.fetchone()

        if not exists:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_CONFIG["database"])
                )
            )
            print(f"✓ Database '{DB_CONFIG['database']}' created successfully")
        else:
            print(f"✓ Database '{DB_CONFIG['database']}' already exists")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"✗ Error creating database: {e}")
        return False


def create_tables():
    """Create the sales table with proper schema and constraints."""
    try:
        # Connect to the coaching_analytics database
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        cursor = conn.cursor()

        # Drop table if exists (for clean setup)
        cursor.execute("DROP TABLE IF EXISTS sales CASCADE")

        # Create sales table
        create_table_query = """
        CREATE TABLE sales (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            revenue DECIMAL(10, 2) NOT NULL CHECK (revenue > 0),
            cash_collected DECIMAL(10, 2) NOT NULL CHECK (cash_collected >= 0),
            product VARCHAR(100) NOT NULL,
            closer VARCHAR(50) NOT NULL,
            country VARCHAR(10) NOT NULL,
            upsell BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT check_cash_not_exceeds_revenue CHECK (cash_collected <= revenue),
            CONSTRAINT check_valid_country CHECK (country IN ('US', 'UK', 'EU')),
            CONSTRAINT check_valid_product CHECK (
                product IN (
                    'Elite Business Accelerator',
                    'Executive Leadership Mastery',
                    'Scale to 7-Figures Program'
                )
            )
        )
        """
        cursor.execute(create_table_query)
        print("✓ Table 'sales' created successfully")

        # Create indexes for better query performance
        indexes = [
            ("idx_sales_date", "CREATE INDEX idx_sales_date ON sales(date)"),
            ("idx_sales_product", "CREATE INDEX idx_sales_product ON sales(product)"),
            ("idx_sales_closer", "CREATE INDEX idx_sales_closer ON sales(closer)"),
            ("idx_sales_country", "CREATE INDEX idx_sales_country ON sales(country)"),
            ("idx_sales_date_product", "CREATE INDEX idx_sales_date_product ON sales(date, product)"),
            ("idx_sales_date_closer", "CREATE INDEX idx_sales_date_closer ON sales(date, closer)"),
            ("idx_sales_upsell", "CREATE INDEX idx_sales_upsell ON sales(upsell)"),
        ]

        for index_name, index_query in indexes:
            cursor.execute(index_query)
            print(f"✓ Index '{index_name}' created successfully")

        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        print("\n✓ Database schema setup completed successfully")
        return True

    except psycopg2.Error as e:
        print(f"✗ Error creating tables: {e}")
        if conn:
            conn.rollback()
        return False


def verify_setup():
    """Verify the database and table setup."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        cursor = conn.cursor()

        # Check table exists
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'sales'
        """)
        if cursor.fetchone():
            print("\n✓ Verification: 'sales' table exists")

        # Check indexes
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'sales' AND schemaname = 'public'
        """)
        indexes = cursor.fetchall()
        print(f"✓ Verification: {len(indexes)} indexes created")

        # Get table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'sales' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        print(f"✓ Verification: {len(columns)} columns defined")
        print("\nTable structure:")
        for col_name, col_type, nullable in columns:
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            print(f"  - {col_name}: {col_type} ({nullable_str})")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"✗ Error verifying setup: {e}")
        return False


def main():
    """Main function to set up the database."""
    print("=" * 60)
    print("Business Coaching Analytics - Database Setup")
    print("=" * 60)
    print(f"\nConnecting to PostgreSQL at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"User: {DB_CONFIG['user']}\n")

    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        print("\n✗ Database setup failed")
        sys.exit(1)

    # Step 2: Create tables and indexes
    print("\nStep 2: Creating tables and indexes...")
    if not create_tables():
        print("\n✗ Table setup failed")
        sys.exit(1)

    # Step 3: Verify setup
    print("\nStep 3: Verifying setup...")
    if not verify_setup():
        print("\n✗ Verification failed")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Database setup completed successfully!")
    print("=" * 60)
    print("\nNext step: Run 'python src/load_data.py' to load the data")


if __name__ == "__main__":
    main()
