"""
Data loading script for the Business Coaching Analytics project.
Loads the CSV data into PostgreSQL database.
"""
import psycopg2
import csv
import sys
from pathlib import Path
from config import DB_CONFIG, RAW_DATA_DIR


def load_csv_to_postgres(csv_file_path):
    """Load data from CSV file into PostgreSQL sales table."""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'sales'
            )
        """)
        if not cursor.fetchone()[0]:
            print("✗ Error: 'sales' table does not exist")
            print("  Please run 'python src/db_setup.py' first")
            return False

        # Clear existing data (optional - for clean reload)
        cursor.execute("SELECT COUNT(*) FROM sales")
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            response = input(f"\n⚠ Table contains {existing_count} rows. Clear existing data? (y/n): ")
            if response.lower() == 'y':
                cursor.execute("TRUNCATE TABLE sales RESTART IDENTITY CASCADE")
                conn.commit()
                print("✓ Existing data cleared")

        # Read and load CSV data
        print(f"\nReading data from: {csv_file_path}")
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            # Prepare insert query
            insert_query = """
                INSERT INTO sales (date, name, email, revenue, cash_collected,
                                   product, closer, country, upsell)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Track loading progress
            rows_loaded = 0
            errors = []

            for row_num, row in enumerate(csv_reader, start=2):  # start=2 because CSV has header
                try:
                    # Convert upsell to boolean
                    upsell = row['upsell'].strip().lower() in ('true', '1', 'yes')

                    # Prepare values
                    values = (
                        row['date'],
                        row['name'],
                        row['email'],
                        float(row['revenue']),
                        float(row['cash_collected']),
                        row['product'],
                        row['closer'],
                        row['country'],
                        upsell
                    )

                    # Insert row
                    cursor.execute(insert_query, values)
                    rows_loaded += 1

                    # Print progress every 50 rows
                    if rows_loaded % 50 == 0:
                        print(f"  Loaded {rows_loaded} rows...")

                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    if len(errors) > 10:  # Stop if too many errors
                        print(f"\n✗ Too many errors encountered. Stopping load.")
                        break

            # Commit transaction
            if errors:
                print(f"\n⚠ Loaded with {len(errors)} errors:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"  - {error}")
                if len(errors) > 5:
                    print(f"  ... and {len(errors) - 5} more errors")

            conn.commit()
            print(f"\n✓ Successfully loaded {rows_loaded} rows into database")

        cursor.close()
        conn.close()
        return True

    except FileNotFoundError:
        print(f"✗ Error: CSV file not found at {csv_file_path}")
        return False
    except psycopg2.Error as e:
        print(f"✗ Database error: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def verify_data_load():
    """Verify the data has been loaded correctly."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("Data Verification")
        print("=" * 60)

        # Total row count
        cursor.execute("SELECT COUNT(*) FROM sales")
        total_rows = cursor.fetchone()[0]
        print(f"\n✓ Total rows in database: {total_rows}")

        # Date range
        cursor.execute("SELECT MIN(date), MAX(date) FROM sales")
        min_date, max_date = cursor.fetchone()
        print(f"✓ Date range: {min_date} to {max_date}")

        # Revenue statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total_sales,
                SUM(revenue) as total_revenue,
                AVG(revenue) as avg_revenue,
                MIN(revenue) as min_revenue,
                MAX(revenue) as max_revenue
            FROM sales
        """)
        stats = cursor.fetchone()
        print(f"\n✓ Revenue Statistics:")
        print(f"  - Total Sales: {stats[0]}")
        print(f"  - Total Revenue: ${stats[1]:,.2f}")
        print(f"  - Average Revenue: ${stats[2]:,.2f}")
        print(f"  - Min Revenue: ${stats[3]:,.2f}")
        print(f"  - Max Revenue: ${stats[4]:,.2f}")

        # Products distribution
        cursor.execute("""
            SELECT product, COUNT(*) as count, SUM(revenue) as revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
        """)
        print(f"\n✓ Sales by Product:")
        for product, count, revenue in cursor.fetchall():
            print(f"  - {product}: {count} sales, ${revenue:,.2f}")

        # Closers performance
        cursor.execute("""
            SELECT closer, COUNT(*) as deals, SUM(revenue) as revenue
            FROM sales
            GROUP BY closer
            ORDER BY revenue DESC
        """)
        print(f"\n✓ Sales by Closer:")
        for closer, deals, revenue in cursor.fetchall():
            print(f"  - {closer}: {deals} deals, ${revenue:,.2f}")

        # Country distribution
        cursor.execute("""
            SELECT country, COUNT(*) as count, SUM(revenue) as revenue
            FROM sales
            GROUP BY country
            ORDER BY count DESC
        """)
        print(f"\n✓ Sales by Country:")
        for country, count, revenue in cursor.fetchall():
            print(f"  - {country}: {count} sales, ${revenue:,.2f}")

        # Upsell statistics
        cursor.execute("""
            SELECT
                upsell,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
            FROM sales
            GROUP BY upsell
            ORDER BY upsell DESC
        """)
        print(f"\n✓ Upsell Statistics:")
        for upsell, count, percentage in cursor.fetchall():
            upsell_label = "Yes" if upsell else "No"
            print(f"  - {upsell_label}: {count} sales ({percentage}%)")

        # Cash collection rate
        cursor.execute("""
            SELECT
                ROUND(AVG(cash_collected / revenue * 100), 2) as avg_collection_rate,
                ROUND(MIN(cash_collected / revenue * 100), 2) as min_collection_rate,
                ROUND(MAX(cash_collected / revenue * 100), 2) as max_collection_rate
            FROM sales
            WHERE revenue > 0
        """)
        avg_rate, min_rate, max_rate = cursor.fetchone()
        print(f"\n✓ Cash Collection Rate:")
        print(f"  - Average: {avg_rate}%")
        print(f"  - Range: {min_rate}% - {max_rate}%")

        # Sample records
        cursor.execute("""
            SELECT date, name, product, revenue, closer, country
            FROM sales
            ORDER BY date
            LIMIT 5
        """)
        print(f"\n✓ Sample Records (First 5):")
        for date, name, product, revenue, closer, country in cursor.fetchall():
            print(f"  - {date} | {name} | {product[:30]}... | ${revenue:,.2f} | {closer} | {country}")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("✓ Data verification completed successfully")
        print("=" * 60)
        return True

    except psycopg2.Error as e:
        print(f"\n✗ Verification error: {e}")
        return False


def main():
    """Main function to load data."""
    print("=" * 60)
    print("Business Coaching Analytics - Data Loading")
    print("=" * 60)

    # Locate CSV file
    csv_file = RAW_DATA_DIR / "coaching_sales_2025.csv"

    if not csv_file.exists():
        print(f"\n✗ Error: CSV file not found at {csv_file}")
        print("  Please ensure the data generation script has been run.")
        sys.exit(1)

    print(f"\nDatabase: {DB_CONFIG['database']}")
    print(f"CSV File: {csv_file}")
    print(f"\nStarting data load...\n")

    # Load data
    if not load_csv_to_postgres(csv_file):
        print("\n✗ Data loading failed")
        sys.exit(1)

    # Verify data
    if not verify_data_load():
        print("\n✗ Data verification failed")
        sys.exit(1)

    print("\n✓ Data loading and verification completed successfully!")
    print("\nNext steps:")
    print("  1. Run SQL queries: python src/sql_queries.py")
    print("  2. Perform analysis: python src/data_analysis.py")
    print("  3. Generate visualizations: python src/visualizations.py")


if __name__ == "__main__":
    main()
