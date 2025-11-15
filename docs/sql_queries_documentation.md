# SQL Queries Documentation - Business Coaching Analytics

## Overview

This document provides comprehensive documentation for all analytical SQL queries in the Business Coaching Analytics project. Each query is designed to answer specific business questions and provide actionable insights.

**Last Updated**: 2025-01-15

---

## Table of Contents

1. [Revenue Analysis Queries](#revenue-analysis-queries)
2. [Sales Team Performance Queries](#sales-team-performance-queries)
3. [Cash Collection Analysis Queries](#cash-collection-analysis-queries)
4. [Geographic Analysis Queries](#geographic-analysis-queries)
5. [Upsell Analysis Queries](#upsell-analysis-queries)
6. [Top Deals and Outliers Queries](#top-deals-and-outliers-queries)
7. [Cohort Analysis Queries](#cohort-analysis-queries)
8. [Window Functions - Running Totals and Moving Averages](#window-functions-queries)
9. [Year-over-Year Comparison Queries](#year-over-year-comparison-queries)
10. [Advanced Business Insights Queries](#advanced-business-insights-queries)
11. [Dashboard Summary Query](#dashboard-summary-query)

---

## Revenue Analysis Queries

### 1. Total Revenue by Product

**Query Name**: `revenue_by_product`

**Business Purpose**: Identify which coaching programs generate the most revenue to inform product portfolio decisions and marketing resource allocation.

**Use Cases**:
- Product portfolio optimization
- Marketing budget allocation
- Product development prioritization
- Sales team focus areas

**Key Metrics**:
- Total deals per product
- Total revenue per product
- Average deal size
- Revenue percentage contribution
- Min/max deal sizes

**Business Questions Answered**:
- Which product is our top revenue generator?
- What percentage of total revenue does each product contribute?
- Which product has the highest average deal value?
- Are there significant pricing variations within products?

**Sample Insights**:
- "Elite Business Accelerator generates 45% of total revenue with an average deal size of $18,500"
- "Scale to 7-Figures Program has the highest average deal size at $22,000 but fewer total deals"

---

### 2. Revenue by Month (Time Series)

**Query Name**: `revenue_by_month`

**Business Purpose**: Track revenue trends over time to identify seasonality, growth patterns, and forecast future performance.

**Use Cases**:
- Financial forecasting
- Trend analysis
- Seasonality identification
- Growth tracking
- Board reporting

**Key Metrics**:
- Monthly deal count
- Monthly total revenue
- Monthly average deal size
- Monthly upsell count and rate

**Business Questions Answered**:
- Are we growing month-over-month?
- Is there seasonal variation in our sales?
- What is our revenue trajectory?
- How do upsell rates vary by month?

**Sample Insights**:
- "Revenue grew 25% from January to February, indicating strong Q1 momentum"
- "September shows a dip in average deal size, suggesting increased discount activity"

---

## Sales Team Performance Queries

### 3. Closer Performance Metrics

**Query Name**: `closer_performance`

**Business Purpose**: Evaluate individual sales closer effectiveness across multiple dimensions to support performance management, compensation planning, and training needs identification.

**Use Cases**:
- Performance reviews
- Compensation calculations
- Coaching and training identification
- Top performer recognition
- Hiring benchmarks

**Key Metrics**:
- Total deals closed
- Total revenue generated
- Average deal size
- Cash collection rate
- Upsell count and rate
- Average monthly revenue
- Active selling period

**Business Questions Answered**:
- Who are our top-performing closers?
- Which closers have the highest average deal values?
- Who is most effective at collecting cash?
- Which closers excel at upselling?
- What is a realistic revenue target per closer?

**Sample Insights**:
- "Sarah Johnson leads in total revenue ($450K) with a 92% collection rate"
- "Mike Chen has the highest upsell rate at 35%, generating $180K in upsell revenue"

---

### 4. Closer Product Matrix

**Query Name**: `closer_product_matrix`

**Business Purpose**: Understand which closers excel at selling specific products to optimize territory/product assignments and identify training opportunities.

**Use Cases**:
- Product-closer matching
- Specialization strategy
- Training program design
- Territory assignment

**Key Metrics**:
- Deals closed by closer and product
- Revenue by closer and product
- Average deal size by combination
- Collection rate by combination

**Business Questions Answered**:
- Which closers are most effective with which products?
- Should we specialize closers by product?
- Where are the skill gaps?
- Which closer-product combinations drive the best results?

**Sample Insights**:
- "Sarah excels at Elite Business Accelerator ($320K) but struggles with Scale to 7-Figures"
- "Closer specialization could increase overall performance by 15-20%"

---

### 5. Closer Efficiency Ranking

**Query Name**: `closer_efficiency_ranking`

**Business Purpose**: Rank closers across multiple performance dimensions to identify top performers and establish benchmarks for hiring and compensation.

**Use Cases**:
- Performance benchmarking
- Hiring criteria definition
- Compensation structure design
- Team composition planning

**Key Metrics**:
- Revenue percentile ranking
- Deal size percentile ranking
- Collection rate
- Upsell rate
- Multi-dimensional efficiency scores

**Business Questions Answered**:
- Who is in the top 10% of performers?
- What characteristics define top performers?
- How do closers rank across different metrics?
- What should our hiring standards be?

---

## Cash Collection Analysis Queries

### 6. Cash Collection Analysis

**Query Name**: `cash_collection_analysis`

**Business Purpose**: Monitor cash flow health and identify collection issues by product to ensure healthy working capital and payment plan effectiveness.

**Use Cases**:
- Cash flow forecasting
- Working capital management
- Payment plan optimization
- Financial health monitoring
- Product pricing strategy

**Key Metrics**:
- Total committed revenue
- Total cash collected
- Outstanding balance
- Overall collection rate
- Fully paid vs. partial payment deals
- Collection rate by product

**Business Questions Answered**:
- How effective are our payment plans?
- Which products have better collection rates?
- What is our total outstanding balance?
- What percentage of deals are fully paid?
- Where are collection issues concentrated?

**Sample Insights**:
- "Elite Business Accelerator has a 89% collection rate with $125K outstanding"
- "78% of deals are fully paid, indicating strong payment discipline"

---

### 7. Cash Collection by Closer

**Query Name**: `cash_collection_by_closer`

**Business Purpose**: Identify closers who structure better payment plans and collect cash more effectively to share best practices.

**Use Cases**:
- Best practice identification
- Payment plan training
- Compensation design (cash collection bonuses)
- Deal structure optimization

**Key Metrics**:
- Collection rate by closer
- Full payment percentage
- Outstanding balance by closer
- Cash collected vs. revenue

**Business Questions Answered**:
- Which closers are best at cash collection?
- What payment structures do top collectors use?
- Who needs training on payment plans?
- Should we tie compensation to collection rates?

**Sample Insights**:
- "Top collectors average 92% collection rate vs. 78% for bottom performers"
- "Closers who offer quarterly payment plans have 15% higher collection rates"

---

### 8. Collection Status Distribution

**Query Name**: `collection_status_distribution`

**Business Purpose**: Understand the overall payment pattern distribution to forecast future cash flow and optimize payment plan design.

**Use Cases**:
- Cash flow forecasting
- Payment plan design
- Risk assessment
- Financial planning

**Key Metrics**:
- Distribution across payment completion buckets
- Deal count by status
- Revenue and collected amounts by status
- Outstanding balance by status

**Business Questions Answered**:
- What is the typical payment pattern?
- How many deals are at risk of non-payment?
- What is our expected future cash flow?
- Should we adjust our payment plan options?

---

## Geographic Analysis Queries

### 9. Geographic Distribution and Performance

**Query Name**: `geographic_distribution`

**Business Purpose**: Understand market performance by region to optimize marketing spend, identify growth opportunities, and refine regional strategies.

**Use Cases**:
- Marketing budget allocation
- Regional strategy development
- Market expansion planning
- Competitive analysis

**Key Metrics**:
- Deals and revenue by country
- Average deal size by region
- Deal and revenue percentages
- Collection rates by region
- Upsell rates by region

**Business Questions Answered**:
- Which regions are our strongest markets?
- Where should we focus expansion efforts?
- Do deal sizes vary by region?
- Are collection rates region-dependent?

**Sample Insights**:
- "US market generates 55% of revenue with highest average deal size ($19,200)"
- "EU market has 95% collection rate, significantly higher than US (85%)"

---

### 10. Country-Product Performance

**Query Name**: `country_product_performance`

**Business Purpose**: Identify product-market fit by region to inform regional product strategies and localization decisions.

**Use Cases**:
- Regional product strategy
- Localization prioritization
- Market-specific messaging
- Product launch planning

**Key Metrics**:
- Revenue by country and product
- Deal count by combination
- Average deal size variations
- Collection rates by combination

**Business Questions Answered**:
- Which products perform best in which regions?
- Should we customize products by region?
- Are pricing strategies appropriate for each market?
- Which product should we lead with in each region?

---

## Upsell Analysis Queries

### 11. Upsell Analysis

**Query Name**: `upsell_analysis`

**Business Purpose**: Measure effectiveness of upselling strategies to improve customer lifetime value and revenue per customer.

**Use Cases**:
- Customer journey optimization
- LTV improvement
- Sales process refinement
- Revenue growth strategies

**Key Metrics**:
- Upsell count and rate by product
- Average upsell value vs. initial sale value
- Upsell revenue percentage
- Product-specific upsell performance

**Business Questions Answered**:
- How effective are our upselling efforts?
- Which products have the best upsell potential?
- What is the average value difference between upsells and initial sales?
- What percentage of revenue comes from upsells?

**Sample Insights**:
- "28% of all deals are upsells, contributing 35% of total revenue"
- "Average upsell value ($21K) is 40% higher than initial sales ($15K)"

---

### 12. Upsell Performance by Closer

**Query Name**: `upsell_by_closer`

**Business Purpose**: Identify top upsellers to share best practices and improve overall team upselling effectiveness.

**Use Cases**:
- Sales training
- Best practice documentation
- Compensation design
- Team coaching

**Key Metrics**:
- Upsell rate by closer
- Upsell revenue by closer
- Average upsell value by closer

**Business Questions Answered**:
- Who are our best upsellers?
- What techniques do top upsellers use?
- What is a realistic upsell target?
- Who needs upselling training?

---

### 13. Upsell Trends Over Time

**Query Name**: `upsell_by_month`

**Business Purpose**: Track upsell strategy effectiveness over time to identify trends and seasonal patterns.

**Use Cases**:
- Strategy evaluation
- Seasonal planning
- Campaign effectiveness measurement
- Process improvement tracking

**Key Metrics**:
- Monthly upsell count and rate
- Monthly upsell revenue
- Month-over-month trends

**Business Questions Answered**:
- Is our upsell rate improving over time?
- Are there seasonal upsell patterns?
- Did recent upsell training improve results?
- When is the best time to present upsells?

---

## Top Deals and Outliers Queries

### 14. Top 10 Highest Value Deals

**Query Name**: `top_10_deals`

**Business Purpose**: Identify and celebrate biggest wins while creating case studies for sales training.

**Use Cases**:
- Case study creation
- Team motivation
- Success pattern identification
- Client testimonial targeting

**Key Metrics**:
- Deal details (customer, product, closer, revenue)
- Collection status
- Deal type (upsell vs. initial)
- Geographic information

**Business Questions Answered**:
- What are our biggest wins?
- What common patterns exist among top deals?
- Which clients should we target for testimonials?
- What made these deals successful?

---

### 15. Top Deals by Product

**Query Name**: `top_deals_by_product`

**Business Purpose**: Understand best-case scenarios for each product to validate pricing and identify success patterns.

**Use Cases**:
- Pricing strategy validation
- Product positioning
- Sales training examples
- Target customer profiling

**Key Metrics**:
- Top 5 deals per product
- Deal characteristics
- Common success factors

**Business Questions Answered**:
- What is the ceiling for each product?
- Are we pricing products optimally?
- What do ideal customers look like for each product?

---

## Cohort Analysis Queries

### 16. Monthly Cohort Analysis

**Query Name**: `monthly_cohort_analysis`

**Business Purpose**: Track performance metrics by acquisition month to evaluate marketing campaign effectiveness and identify seasonal trends.

**Use Cases**:
- Marketing campaign effectiveness
- Seasonal trend identification
- Customer acquisition strategy
- Performance benchmarking

**Key Metrics**:
- Customers acquired by month
- Revenue per cohort
- Collection rates by cohort
- Upsell rates by cohort
- Active closers per cohort

**Business Questions Answered**:
- Which acquisition months perform best?
- Do seasonal campaigns work better?
- How do cohorts compare in quality?
- What is the best time to acquire customers?

---

### 17. Cohort Product Mix

**Query Name**: `cohort_product_mix`

**Business Purpose**: Understand how product preferences change over time to inform product strategy evolution.

**Use Cases**:
- Product strategy evolution
- Market trend identification
- Campaign planning
- Inventory/capacity planning

**Key Metrics**:
- Product distribution by cohort
- Revenue share by product and time
- Product preference trends

**Business Questions Answered**:
- Are product preferences changing?
- Which products are gaining/losing popularity?
- Should we adjust our product mix?
- What trends should inform future development?

---

## Window Functions Queries

### 18. Running Totals and Cumulative Metrics

**Query Name**: `running_totals`

**Business Purpose**: Track cumulative progress toward goals in real-time for performance dashboards.

**Use Cases**:
- Real-time dashboards
- Goal tracking
- Performance monitoring
- Team motivation

**Key Metrics**:
- Cumulative revenue
- Cumulative cash collected
- Cumulative deal count
- 30-day moving averages
- Closer-specific cumulative metrics

**Business Questions Answered**:
- Are we on track to hit our goals?
- What is our current trajectory?
- How do daily fluctuations smooth out over time?
- What is each closer's cumulative contribution?

---

### 19. Monthly Moving Averages

**Query Name**: `moving_averages_by_month`

**Business Purpose**: Smooth out volatility to see true trends for executive reporting and strategic planning.

**Use Cases**:
- Executive reporting
- Strategic planning
- Trend identification
- Noise reduction in data

**Key Metrics**:
- 3-month moving averages
- Cumulative revenue
- Smoothed deal counts

**Business Questions Answered**:
- What is the underlying trend beyond monthly noise?
- Are we in a true growth trend or just experiencing volatility?
- What should our long-term projections be?

---

### 20. Revenue Growth Rates

**Query Name**: `revenue_growth_rates`

**Business Purpose**: Measure growth velocity month-over-month for investor reporting and growth tracking.

**Use Cases**:
- Investor reporting
- Growth tracking
- Performance assessment
- Strategic planning

**Key Metrics**:
- Month-over-month revenue growth
- Month-over-month deal growth
- Growth rate trends

**Business Questions Answered**:
- What is our growth rate?
- Are we accelerating or decelerating?
- How do we compare to growth targets?
- What is our growth story for investors?

---

## Year-over-Year Comparison Queries

### 21. Year-over-Year Comparison

**Query Name**: `year_over_year_comparison`

**Business Purpose**: Compare performance across years to understand annual growth and seasonality patterns.

**Use Cases**:
- Annual planning
- Seasonality analysis
- Multi-year trend identification
- Board reporting

**Key Metrics**:
- Year-over-year revenue growth
- Year-over-year deal growth
- Same-month comparisons across years

**Business Questions Answered**:
- How do we compare to last year?
- What is our annual growth rate?
- Are seasonal patterns consistent year-over-year?

**Note**: Requires multiple years of data to be meaningful.

---

### 22. Quarterly Performance Comparison

**Query Name**: `quarterly_comparison`

**Business Purpose**: Track quarterly business cycles for quarterly business reviews and board reporting.

**Use Cases**:
- Quarterly business reviews
- Board reporting
- Strategic planning
- Resource allocation

**Key Metrics**:
- Quarterly revenue and deals
- Quarter-over-quarter growth
- Revenue per closer by quarter
- Collection rates by quarter

**Business Questions Answered**:
- How did we perform this quarter?
- What is our quarterly growth trajectory?
- How efficient is our team by quarter?

---

## Advanced Business Insights Queries

### 23. Product Cannibalization Analysis

**Query Name**: `product_cannibalization_analysis`

**Business Purpose**: Check if products compete with each other to optimize product portfolio and pricing strategy.

**Use Cases**:
- Product portfolio optimization
- Pricing strategy
- Product development decisions
- Bundle creation

**Key Metrics**:
- Multi-product purchase patterns
- Customer lifetime value by product count
- Cross-product purchase rates

**Business Questions Answered**:
- Do customers buy multiple products?
- Is there product cannibalization?
- What is the LTV lift from multi-product customers?
- Should we create bundles?

---

### 24. Deal Size Distribution Analysis

**Query Name**: `deal_size_distribution`

**Business Purpose**: Understand pricing and deal structure patterns to optimize pricing and discount policies.

**Use Cases**:
- Pricing optimization
- Discount policy evaluation
- Sales process design
- Target customer segmentation

**Key Metrics**:
- Deal count by size bucket
- Revenue concentration by bucket
- Collection rates by deal size

**Business Questions Answered**:
- Where do most deals fall in terms of size?
- Which deal size ranges generate most revenue?
- Should we adjust our pricing tiers?
- Do larger deals have different collection patterns?

---

### 25. Sales Velocity Metrics

**Query Name**: `sales_velocity_metrics`

**Business Purpose**: Measure how quickly revenue is generated for sales forecasting and capacity planning.

**Use Cases**:
- Sales forecasting
- Capacity planning
- Hiring decisions
- Performance benchmarking

**Key Metrics**:
- Average deals per day
- Average revenue per day
- Revenue volatility
- Projected monthly/annual revenue
- Active closer counts

**Business Questions Answered**:
- What is our sales velocity?
- How predictable is our revenue?
- Do we need to hire more closers?
- What should we forecast for the next period?

---

## Dashboard Summary Query

### 26. Business Dashboard Summary

**Query Name**: `business_dashboard_summary`

**Business Purpose**: One-query overview of all key business metrics for executive dashboards and daily standups.

**Use Cases**:
- Executive dashboard
- Daily standup metrics
- Quick performance snapshot
- Board meeting prep

**Key Metrics**:
- All critical metrics in one view
- Overall revenue and deals
- Collection metrics
- Upsell metrics
- Team metrics
- Time range coverage

**Business Questions Answered**:
- How is the business performing overall?
- What are the key numbers I need to know?
- Are we hitting our targets across all dimensions?

---

## Query Execution

### Running Queries

#### Run All Queries
```bash
python src/run_queries.py
```

#### Run Specific Category
```bash
python src/run_queries.py --category revenue
python src/run_queries.py --category performance
python src/run_queries.py --category collection
```

#### List Available Queries
```bash
python src/run_queries.py --list
```

#### Custom Options
```bash
# Run without CSV export
python src/run_queries.py --no-csv

# Run without console display
python src/run_queries.py --no-display

# Show more rows in console output
python src/run_queries.py --max-rows 20
```

### Output Locations

- **CSV Files**: `outputs/query_results/csv/`
- **JSON Files**: `outputs/query_results/json/`
- **Console**: Standard output

---

## Query Categories

### Available Categories

1. **revenue** - Revenue analysis queries
2. **performance** - Sales team performance queries
3. **collection** - Cash collection analysis queries
4. **geographic** - Geographic distribution queries
5. **upsell** - Upsell effectiveness queries
6. **top_deals** - Top performing deals
7. **cohort** - Cohort analysis queries
8. **trends** - Time series and trend queries
9. **advanced** - Advanced business insights
10. **dashboard** - Summary dashboard query

---

## Database Schema Reference

### Sales Table

```sql
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Valid Values

- **Products**: Elite Business Accelerator, Executive Leadership Mastery, Scale to 7-Figures Program
- **Countries**: US, UK, EU
- **Closers**: Sarah Johnson, Mike Chen, Jessica Williams, David Rodriguez, Emily Brown

---

## Best Practices

### Performance Optimization

1. All key columns are indexed for optimal query performance
2. Aggregate functions are used efficiently
3. Window functions are optimized with proper partitioning
4. CTEs are used for complex queries to improve readability

### Query Maintenance

1. All queries include business context comments
2. Queries are organized by category
3. Query names are descriptive and consistent
4. Results include percentages for easy interpretation

### Data Quality

1. Queries handle NULL values appropriately
2. Division by zero is prevented with NULLIF
3. Results are rounded for readability
4. Data types are cast properly for calculations

---

## Troubleshooting

### Common Issues

**Issue**: Query returns no results
- **Solution**: Check that data has been loaded into the database

**Issue**: Division by zero error
- **Solution**: Queries include NULLIF to handle this, but check for empty tables

**Issue**: Slow query performance
- **Solution**: Verify indexes are created; run `EXPLAIN ANALYZE` on slow queries

**Issue**: Date range limitations
- **Solution**: Some queries (YoY) require multiple years of data

---

## Support

For questions or issues:
1. Check this documentation first
2. Review the SQL query comments in [sql_queries.py](../src/sql_queries.py)
3. Examine sample outputs in `outputs/query_results/`
4. Review database schema in [db_setup.py](../src/db_setup.py)

---

## Version History

- **v1.0** (2025-01-15) - Initial comprehensive query library with 26+ queries
- All queries tested and documented with business context
- Full export functionality (CSV/JSON)
- Category-based organization

---

*This documentation is part of the Business Coaching Analytics Project - Phase 3: SQL Analysis & Queries*
