"""
SQL Queries for Business Coaching Analytics

This module contains all analytical SQL queries for generating business insights
from the sales data. Each query is documented with its business purpose.

Schema Reference:
- id: SERIAL PRIMARY KEY
- date: DATE (sale date)
- name: VARCHAR(100) (customer name)
- email: VARCHAR(100) (customer email)
- revenue: DECIMAL(10, 2) (total deal value)
- cash_collected: DECIMAL(10, 2) (cash collected so far)
- product: VARCHAR(100) (coaching product sold)
- closer: VARCHAR(50) (sales closer name)
- country: VARCHAR(10) (US, UK, EU)
- upsell: BOOLEAN (whether this was an upsell)
- created_at: TIMESTAMP (record creation time)
"""

# ============================================================================
# REVENUE ANALYSIS QUERIES
# ============================================================================

REVENUE_BY_PRODUCT = """
-- Total revenue by product
-- Business Purpose: Identify which coaching programs generate the most revenue
-- Use Case: Product portfolio optimization and marketing focus
SELECT
    product,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_deal_size,
    MIN(revenue) as min_deal_size,
    MAX(revenue) as max_deal_size,
    ROUND((SUM(revenue) / (SELECT SUM(revenue) FROM sales) * 100), 2) as revenue_percentage
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;
"""

REVENUE_BY_MONTH = """
-- Revenue by month (time series)
-- Business Purpose: Track revenue trends over time to identify seasonality and growth patterns
-- Use Case: Financial forecasting and trend analysis
SELECT
    DATE_TRUNC('month', date) as month,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_deal_size,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage
FROM sales
GROUP BY DATE_TRUNC('month', date)
ORDER BY month;
"""

# ============================================================================
# SALES TEAM PERFORMANCE QUERIES
# ============================================================================

CLOSER_PERFORMANCE = """
-- Closer performance metrics
-- Business Purpose: Evaluate individual sales closer effectiveness
-- Use Case: Sales team management, compensation planning, coaching needs
SELECT
    closer,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_deal_size,
    ROUND(AVG(revenue), 2) as avg_deal_value,
    SUM(cash_collected) as total_cash_collected,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate_percentage,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage,
    MIN(date) as first_sale_date,
    MAX(date) as latest_sale_date,
    ROUND(SUM(revenue) / COUNT(DISTINCT DATE_TRUNC('month', date)), 2) as avg_monthly_revenue
FROM sales
GROUP BY closer
ORDER BY total_revenue DESC;
"""

CLOSER_PRODUCT_MATRIX = """
-- Closer performance by product
-- Business Purpose: Understand which closers excel at selling specific products
-- Use Case: Territory/product assignment optimization
SELECT
    closer,
    product,
    COUNT(*) as deals_closed,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_deal_size,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate
FROM sales
GROUP BY closer, product
ORDER BY closer, total_revenue DESC;
"""

# ============================================================================
# CASH COLLECTION ANALYSIS QUERIES
# ============================================================================

CASH_COLLECTION_ANALYSIS = """
-- Cash collection analysis
-- Business Purpose: Monitor cash flow and identify collection issues
-- Use Case: Financial health monitoring, payment plan effectiveness
SELECT
    product,
    COUNT(*) as total_deals,
    SUM(revenue) as total_committed_revenue,
    SUM(cash_collected) as total_cash_collected,
    SUM(revenue - cash_collected) as outstanding_balance,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as overall_collection_rate,
    ROUND(AVG((cash_collected / revenue * 100)), 2) as avg_individual_collection_rate,
    COUNT(CASE WHEN cash_collected = revenue THEN 1 END) as fully_paid_deals,
    COUNT(CASE WHEN cash_collected < revenue THEN 1 END) as partial_payment_deals,
    ROUND(
        COUNT(CASE WHEN cash_collected = revenue THEN 1 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as fully_paid_percentage
FROM sales
GROUP BY product
ORDER BY overall_collection_rate DESC;
"""

CASH_COLLECTION_BY_CLOSER = """
-- Cash collection by closer
-- Business Purpose: Identify closers who structure better payment plans
-- Use Case: Best practices sharing, closer training
SELECT
    closer,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    SUM(cash_collected) as cash_collected,
    SUM(revenue - cash_collected) as outstanding,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate,
    COUNT(CASE WHEN cash_collected = revenue THEN 1 END) as full_payment_count,
    ROUND(
        COUNT(CASE WHEN cash_collected = revenue THEN 1 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as full_payment_percentage
FROM sales
GROUP BY closer
ORDER BY collection_rate DESC;
"""

COLLECTION_STATUS_DISTRIBUTION = """
-- Distribution of payment completion status
-- Business Purpose: Understand the overall payment pattern
-- Use Case: Financial forecasting, payment plan design
SELECT
    CASE
        WHEN cash_collected = revenue THEN 'Fully Paid'
        WHEN cash_collected >= revenue * 0.75 THEN 'Nearly Complete (75-99%)'
        WHEN cash_collected >= revenue * 0.5 THEN 'Half Paid (50-74%)'
        WHEN cash_collected >= revenue * 0.25 THEN 'Quarter Paid (25-49%)'
        ELSE 'Minimal Payment (0-24%)'
    END as payment_status,
    COUNT(*) as deal_count,
    SUM(revenue) as total_revenue,
    SUM(cash_collected) as total_collected,
    SUM(revenue - cash_collected) as outstanding_balance,
    ROUND((COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM sales)::NUMERIC * 100), 2) as percentage_of_deals
FROM sales
GROUP BY payment_status
ORDER BY
    CASE payment_status
        WHEN 'Fully Paid' THEN 1
        WHEN 'Nearly Complete (75-99%)' THEN 2
        WHEN 'Half Paid (50-74%)' THEN 3
        WHEN 'Quarter Paid (25-49%)' THEN 4
        ELSE 5
    END;
"""

# ============================================================================
# GEOGRAPHIC ANALYSIS QUERIES
# ============================================================================

GEOGRAPHIC_DISTRIBUTION = """
-- Geographic distribution and performance
-- Business Purpose: Understand market performance by region
-- Use Case: Marketing budget allocation, regional strategy
SELECT
    country,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_deal_size,
    ROUND((COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM sales)::NUMERIC * 100), 2) as deal_percentage,
    ROUND((SUM(revenue) / (SELECT SUM(revenue) FROM sales) * 100), 2) as revenue_percentage,
    SUM(cash_collected) as cash_collected,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage
FROM sales
GROUP BY country
ORDER BY total_revenue DESC;
"""

COUNTRY_PRODUCT_PERFORMANCE = """
-- Product performance by country
-- Business Purpose: Identify product-market fit by region
-- Use Case: Regional product strategy, localization decisions
SELECT
    country,
    product,
    COUNT(*) as deals,
    SUM(revenue) as revenue,
    ROUND(AVG(revenue), 2) as avg_deal_size,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate
FROM sales
GROUP BY country, product
ORDER BY country, revenue DESC;
"""

# ============================================================================
# UPSELL ANALYSIS QUERIES
# ============================================================================

UPSELL_ANALYSIS = """
-- Upsell analysis
-- Business Purpose: Measure effectiveness of upselling strategies
-- Use Case: Customer journey optimization, LTV improvement
SELECT
    product,
    COUNT(*) as total_deals,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    SUM(CASE WHEN upsell = FALSE THEN 1 ELSE 0 END) as initial_sale_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage,
    ROUND(AVG(CASE WHEN upsell = TRUE THEN revenue END), 2) as avg_upsell_value,
    ROUND(AVG(CASE WHEN upsell = FALSE THEN revenue END), 2) as avg_initial_sale_value,
    SUM(CASE WHEN upsell = TRUE THEN revenue ELSE 0 END) as total_upsell_revenue,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN revenue ELSE 0 END) / SUM(revenue) * 100,
        2
    ) as upsell_revenue_percentage
FROM sales
GROUP BY product
ORDER BY upsell_rate_percentage DESC;
"""

UPSELL_BY_CLOSER = """
-- Upsell performance by closer
-- Business Purpose: Identify top upsellers for best practice sharing
-- Use Case: Sales training, compensation design
SELECT
    closer,
    COUNT(*) as total_deals,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage,
    SUM(CASE WHEN upsell = TRUE THEN revenue ELSE 0 END) as upsell_revenue,
    ROUND(AVG(CASE WHEN upsell = TRUE THEN revenue END), 2) as avg_upsell_value
FROM sales
GROUP BY closer
ORDER BY upsell_rate_percentage DESC;
"""

UPSELL_BY_MONTH = """
-- Upsell trends over time
-- Business Purpose: Track upsell strategy effectiveness over time
-- Use Case: Strategy evaluation, seasonal pattern identification
SELECT
    DATE_TRUNC('month', date) as month,
    COUNT(*) as total_deals,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsell_count,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate_percentage,
    SUM(CASE WHEN upsell = TRUE THEN revenue ELSE 0 END) as upsell_revenue,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN revenue ELSE 0 END) / SUM(revenue) * 100,
        2
    ) as upsell_revenue_percentage
FROM sales
GROUP BY DATE_TRUNC('month', date)
ORDER BY month;
"""

# ============================================================================
# TOP DEALS AND OUTLIERS QUERIES
# ============================================================================

TOP_10_DEALS = """
-- Top 10 highest value deals
-- Business Purpose: Identify and celebrate biggest wins
-- Use Case: Case study creation, sales team motivation
SELECT
    id,
    date,
    name,
    email,
    product,
    closer,
    country,
    revenue,
    cash_collected,
    ROUND((cash_collected / revenue * 100), 2) as collection_percentage,
    upsell,
    CASE
        WHEN upsell = TRUE THEN 'Upsell Deal'
        ELSE 'Initial Sale'
    END as deal_type
FROM sales
ORDER BY revenue DESC
LIMIT 10;
"""

TOP_DEALS_BY_PRODUCT = """
-- Top 5 deals per product
-- Business Purpose: Understand best case scenarios for each product
-- Use Case: Sales training, pricing strategy validation
WITH ranked_deals AS (
    SELECT
        product,
        name,
        closer,
        country,
        revenue,
        cash_collected,
        date,
        upsell,
        ROW_NUMBER() OVER (PARTITION BY product ORDER BY revenue DESC) as rank
    FROM sales
)
SELECT
    product,
    rank,
    name,
    closer,
    country,
    revenue,
    ROUND((cash_collected / revenue * 100), 2) as collection_rate,
    date,
    upsell
FROM ranked_deals
WHERE rank <= 5
ORDER BY product, rank;
"""

# ============================================================================
# COHORT ANALYSIS QUERIES
# ============================================================================

MONTHLY_COHORT_ANALYSIS = """
-- Monthly cohort analysis
-- Business Purpose: Track performance metrics by acquisition month
-- Use Case: Marketing campaign effectiveness, seasonal trends
SELECT
    DATE_TRUNC('month', date) as cohort_month,
    COUNT(*) as customers_acquired,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_revenue_per_customer,
    SUM(cash_collected) as total_cash_collected,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate,
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as upsells,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate,
    COUNT(DISTINCT closer) as active_closers,
    COUNT(DISTINCT product) as products_sold
FROM sales
GROUP BY DATE_TRUNC('month', date)
ORDER BY cohort_month;
"""

COHORT_PRODUCT_MIX = """
-- Product mix by monthly cohort
-- Business Purpose: Understand how product preferences change over time
-- Use Case: Product strategy evolution, market trend identification
SELECT
    DATE_TRUNC('month', date) as cohort_month,
    product,
    COUNT(*) as deals,
    SUM(revenue) as revenue,
    ROUND(
        COUNT(*)::NUMERIC /
        SUM(COUNT(*)) OVER (PARTITION BY DATE_TRUNC('month', date))::NUMERIC * 100,
        2
    ) as percentage_of_month_deals
FROM sales
GROUP BY DATE_TRUNC('month', date), product
ORDER BY cohort_month, revenue DESC;
"""

# ============================================================================
# WINDOW FUNCTIONS - RUNNING TOTALS AND MOVING AVERAGES
# ============================================================================

RUNNING_TOTALS = """
-- Running totals and cumulative metrics
-- Business Purpose: Track cumulative progress toward goals
-- Use Case: Real-time performance dashboards, goal tracking
SELECT
    date,
    product,
    closer,
    revenue,
    cash_collected,
    SUM(revenue) OVER (ORDER BY date) as cumulative_revenue,
    SUM(cash_collected) OVER (ORDER BY date) as cumulative_cash,
    COUNT(*) OVER (ORDER BY date) as cumulative_deals,
    ROUND(AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 2) as moving_avg_30_day_revenue,
    SUM(revenue) OVER (
        PARTITION BY closer
        ORDER BY date
    ) as closer_cumulative_revenue,
    ROW_NUMBER() OVER (
        PARTITION BY closer
        ORDER BY date
    ) as closer_deal_number
FROM sales
ORDER BY date, closer;
"""

MOVING_AVERAGES_BY_MONTH = """
-- Monthly moving averages
-- Business Purpose: Smooth out volatility to see true trends
-- Use Case: Executive reporting, strategic planning
WITH monthly_metrics AS (
    SELECT
        DATE_TRUNC('month', date) as month,
        COUNT(*) as deals,
        SUM(revenue) as revenue,
        ROUND(AVG(revenue), 2) as avg_deal_size,
        SUM(cash_collected) as cash_collected
    FROM sales
    GROUP BY DATE_TRUNC('month', date)
)
SELECT
    month,
    deals,
    revenue,
    avg_deal_size,
    cash_collected,
    ROUND(AVG(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as three_month_moving_avg_revenue,
    ROUND(AVG(deals) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as three_month_moving_avg_deals,
    SUM(revenue) OVER (ORDER BY month) as cumulative_revenue
FROM monthly_metrics
ORDER BY month;
"""

REVENUE_GROWTH_RATES = """
-- Month-over-month growth rates
-- Business Purpose: Measure growth velocity
-- Use Case: Investor reporting, growth tracking
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', date) as month,
        SUM(revenue) as revenue,
        COUNT(*) as deals
    FROM sales
    GROUP BY DATE_TRUNC('month', date)
)
SELECT
    month,
    revenue,
    deals,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month_revenue,
    LAG(deals, 1) OVER (ORDER BY month) as prev_month_deals,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY month)) /
        NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0) * 100,
        2
    ) as revenue_growth_percentage,
    ROUND(
        (deals - LAG(deals, 1) OVER (ORDER BY month))::NUMERIC /
        NULLIF(LAG(deals, 1) OVER (ORDER BY month), 0) * 100,
        2
    ) as deals_growth_percentage
FROM monthly_revenue
ORDER BY month;
"""

# ============================================================================
# YEAR-OVER-YEAR COMPARISON
# ============================================================================

YEAR_OVER_YEAR_COMPARISON = """
-- Year-over-year comparison (if applicable)
-- Business Purpose: Compare performance across years
-- Use Case: Annual planning, seasonality analysis
-- Note: This query will return results only if data spans multiple years
WITH yearly_metrics AS (
    SELECT
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(MONTH FROM date) as month,
        COUNT(*) as deals,
        SUM(revenue) as revenue,
        SUM(cash_collected) as cash_collected,
        ROUND(AVG(revenue), 2) as avg_deal_size
    FROM sales
    GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
)
SELECT
    year,
    month,
    TO_CHAR(TO_DATE(month::TEXT, 'MM'), 'Month') as month_name,
    deals,
    revenue,
    cash_collected,
    avg_deal_size,
    LAG(deals, 12) OVER (ORDER BY year, month) as same_month_last_year_deals,
    LAG(revenue, 12) OVER (ORDER BY year, month) as same_month_last_year_revenue,
    ROUND(
        (revenue - LAG(revenue, 12) OVER (ORDER BY year, month)) /
        NULLIF(LAG(revenue, 12) OVER (ORDER BY year, month), 0) * 100,
        2
    ) as yoy_revenue_growth_percentage
FROM yearly_metrics
ORDER BY year, month;
"""

QUARTERLY_COMPARISON = """
-- Quarterly performance comparison
-- Business Purpose: Track quarterly business cycles
-- Use Case: Quarterly business reviews, board reporting
SELECT
    EXTRACT(YEAR FROM date) as year,
    EXTRACT(QUARTER FROM date) as quarter,
    'Q' || EXTRACT(QUARTER FROM date) || ' ' || EXTRACT(YEAR FROM date) as quarter_label,
    COUNT(*) as total_deals,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_deal_size,
    SUM(cash_collected) as cash_collected,
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as collection_rate,
    COUNT(DISTINCT closer) as active_closers,
    ROUND(SUM(revenue) / COUNT(DISTINCT closer), 2) as revenue_per_closer
FROM sales
GROUP BY EXTRACT(YEAR FROM date), EXTRACT(QUARTER FROM date)
ORDER BY year, quarter;
"""

# ============================================================================
# BUSINESS INSIGHTS - ADVANCED QUERIES
# ============================================================================

CLOSER_EFFICIENCY_RANKING = """
-- Closer efficiency ranking
-- Business Purpose: Identify most efficient closers across multiple dimensions
-- Use Case: Sales team benchmarking, hiring criteria
WITH closer_stats AS (
    SELECT
        closer,
        COUNT(*) as total_deals,
        SUM(revenue) as total_revenue,
        AVG(revenue) as avg_deal_size,
        SUM(cash_collected) / SUM(revenue) * 100 as collection_rate,
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100 as upsell_rate
    FROM sales
    GROUP BY closer
)
SELECT
    closer,
    total_deals,
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(avg_deal_size, 2) as avg_deal_size,
    ROUND(collection_rate, 2) as collection_rate,
    ROUND(upsell_rate, 2) as upsell_rate,
    ROUND(
        (RANK() OVER (ORDER BY total_revenue DESC))::NUMERIC /
        (SELECT COUNT(DISTINCT closer) FROM sales)::NUMERIC * 100,
        2
    ) as revenue_percentile,
    ROUND(
        (RANK() OVER (ORDER BY avg_deal_size DESC))::NUMERIC /
        (SELECT COUNT(DISTINCT closer) FROM sales)::NUMERIC * 100,
        2
    ) as deal_size_percentile
FROM closer_stats
ORDER BY total_revenue DESC;
"""

PRODUCT_CANNIBALIZATION_ANALYSIS = """
-- Product cannibalization analysis
-- Business Purpose: Check if products compete with each other
-- Use Case: Product portfolio optimization, pricing strategy
WITH customer_products AS (
    SELECT
        email,
        COUNT(DISTINCT product) as products_purchased,
        ARRAY_AGG(DISTINCT product ORDER BY product) as product_list,
        SUM(revenue) as total_spent,
        MIN(date) as first_purchase_date,
        MAX(date) as last_purchase_date
    FROM sales
    GROUP BY email
)
SELECT
    products_purchased,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_customer_ltv,
    ROUND(
        COUNT(*)::NUMERIC /
        (SELECT COUNT(DISTINCT email) FROM sales)::NUMERIC * 100,
        2
    ) as percentage_of_customers
FROM customer_products
GROUP BY products_purchased
ORDER BY products_purchased;
"""

DEAL_SIZE_DISTRIBUTION = """
-- Deal size distribution analysis
-- Business Purpose: Understand pricing and deal structure patterns
-- Use Case: Pricing optimization, discount policy evaluation
SELECT
    CASE
        WHEN revenue < 5000 THEN 'Under $5K'
        WHEN revenue < 10000 THEN '$5K - $10K'
        WHEN revenue < 15000 THEN '$10K - $15K'
        WHEN revenue < 20000 THEN '$15K - $20K'
        WHEN revenue < 25000 THEN '$20K - $25K'
        ELSE 'Over $25K'
    END as deal_size_range,
    COUNT(*) as deal_count,
    ROUND(AVG(revenue), 2) as avg_revenue,
    SUM(revenue) as total_revenue,
    ROUND((COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM sales)::NUMERIC * 100), 2) as percentage_of_deals,
    ROUND((SUM(revenue) / (SELECT SUM(revenue) FROM sales) * 100), 2) as percentage_of_revenue,
    ROUND(AVG((cash_collected / revenue * 100)), 2) as avg_collection_rate
FROM sales
GROUP BY deal_size_range
ORDER BY
    CASE deal_size_range
        WHEN 'Under $5K' THEN 1
        WHEN '$5K - $10K' THEN 2
        WHEN '$10K - $15K' THEN 3
        WHEN '$15K - $20K' THEN 4
        WHEN '$20K - $25K' THEN 5
        ELSE 6
    END;
"""

SALES_VELOCITY_METRICS = """
-- Sales velocity metrics
-- Business Purpose: Measure how quickly revenue is generated
-- Use Case: Sales forecasting, capacity planning
WITH daily_metrics AS (
    SELECT
        date,
        COUNT(*) as deals_per_day,
        SUM(revenue) as revenue_per_day,
        COUNT(DISTINCT closer) as active_closers
    FROM sales
    GROUP BY date
)
SELECT
    ROUND(AVG(deals_per_day), 2) as avg_deals_per_day,
    ROUND(AVG(revenue_per_day), 2) as avg_revenue_per_day,
    ROUND(MAX(revenue_per_day), 2) as best_day_revenue,
    ROUND(MIN(revenue_per_day), 2) as worst_day_revenue,
    ROUND(STDDEV(revenue_per_day), 2) as revenue_volatility,
    ROUND(AVG(revenue_per_day) * 30, 2) as projected_monthly_revenue,
    ROUND(AVG(revenue_per_day) * 365, 2) as projected_annual_revenue,
    ROUND(AVG(active_closers), 2) as avg_daily_active_closers
FROM daily_metrics;
"""

# ============================================================================
# COMPREHENSIVE BUSINESS DASHBOARD QUERY
# ============================================================================

BUSINESS_DASHBOARD_SUMMARY = """
-- Comprehensive business dashboard summary
-- Business Purpose: One-query overview of all key business metrics
-- Use Case: Executive dashboard, daily standup metrics
SELECT
    -- Overall Metrics
    COUNT(*) as total_deals,
    COUNT(DISTINCT email) as unique_customers,
    SUM(revenue) as total_revenue,
    SUM(cash_collected) as total_cash_collected,
    ROUND(AVG(revenue), 2) as avg_deal_size,

    -- Collection Metrics
    ROUND((SUM(cash_collected) / SUM(revenue) * 100), 2) as overall_collection_rate,
    SUM(revenue - cash_collected) as total_outstanding,
    COUNT(CASE WHEN cash_collected = revenue THEN 1 END) as fully_paid_deals,

    -- Upsell Metrics
    SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END) as total_upsells,
    ROUND(
        SUM(CASE WHEN upsell = TRUE THEN 1 ELSE 0 END)::NUMERIC /
        COUNT(*)::NUMERIC * 100,
        2
    ) as upsell_rate,

    -- Team Metrics
    COUNT(DISTINCT closer) as active_closers,
    COUNT(DISTINCT product) as products_sold,
    COUNT(DISTINCT country) as countries_served,

    -- Time Range
    MIN(date) as first_sale_date,
    MAX(date) as latest_sale_date,
    MAX(date) - MIN(date) as days_of_operation,

    -- Performance Metrics
    ROUND(SUM(revenue) / COUNT(DISTINCT closer), 2) as revenue_per_closer,
    ROUND(SUM(revenue) / (MAX(date) - MIN(date) + 1), 2) as revenue_per_day,
    ROUND(COUNT(*)::NUMERIC / COUNT(DISTINCT closer), 2) as deals_per_closer
FROM sales;
"""

# ============================================================================
# QUERY EXECUTION HELPERS
# ============================================================================

# Dictionary mapping query names to SQL strings for easy access
QUERIES = {
    # Revenue Analysis
    'revenue_by_product': REVENUE_BY_PRODUCT,
    'revenue_by_month': REVENUE_BY_MONTH,

    # Sales Team Performance
    'closer_performance': CLOSER_PERFORMANCE,
    'closer_product_matrix': CLOSER_PRODUCT_MATRIX,
    'closer_efficiency_ranking': CLOSER_EFFICIENCY_RANKING,

    # Cash Collection
    'cash_collection_analysis': CASH_COLLECTION_ANALYSIS,
    'cash_collection_by_closer': CASH_COLLECTION_BY_CLOSER,
    'collection_status_distribution': COLLECTION_STATUS_DISTRIBUTION,

    # Geographic Analysis
    'geographic_distribution': GEOGRAPHIC_DISTRIBUTION,
    'country_product_performance': COUNTRY_PRODUCT_PERFORMANCE,

    # Upsell Analysis
    'upsell_analysis': UPSELL_ANALYSIS,
    'upsell_by_closer': UPSELL_BY_CLOSER,
    'upsell_by_month': UPSELL_BY_MONTH,

    # Top Deals
    'top_10_deals': TOP_10_DEALS,
    'top_deals_by_product': TOP_DEALS_BY_PRODUCT,

    # Cohort Analysis
    'monthly_cohort_analysis': MONTHLY_COHORT_ANALYSIS,
    'cohort_product_mix': COHORT_PRODUCT_MIX,

    # Window Functions
    'running_totals': RUNNING_TOTALS,
    'moving_averages_by_month': MOVING_AVERAGES_BY_MONTH,
    'revenue_growth_rates': REVENUE_GROWTH_RATES,

    # Year over Year
    'year_over_year_comparison': YEAR_OVER_YEAR_COMPARISON,
    'quarterly_comparison': QUARTERLY_COMPARISON,

    # Advanced Insights
    'product_cannibalization_analysis': PRODUCT_CANNIBALIZATION_ANALYSIS,
    'deal_size_distribution': DEAL_SIZE_DISTRIBUTION,
    'sales_velocity_metrics': SALES_VELOCITY_METRICS,

    # Dashboard
    'business_dashboard_summary': BUSINESS_DASHBOARD_SUMMARY,
}

def get_query(query_name: str) -> str:
    """
    Retrieve a query by name.

    Args:
        query_name: The name of the query to retrieve

    Returns:
        The SQL query string

    Raises:
        KeyError: If the query name is not found
    """
    return QUERIES[query_name]

def list_available_queries() -> list:
    """
    List all available query names.

    Returns:
        List of query names
    """
    return sorted(QUERIES.keys())
