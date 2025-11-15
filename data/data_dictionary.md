# Data Dictionary - Business Coaching Sales Data

## Overview
This dataset contains sales transaction data for a high-ticket online business coaching company operating in the US, UK, and EU markets. The data covers 11 months of 2025 (January through November) with 195 sales records.

## Dataset: coaching_sales_2025.csv

### Schema

| Column Name | Data Type | Description | Constraints | Example |
|------------|-----------|-------------|-------------|---------|
| `date` | DATE | Transaction date | YYYY-MM-DD format, Jan 1 - Nov 30, 2025 | 2025-03-15 |
| `name` | VARCHAR(100) | Customer full name | Not null, realistic names | John Smith |
| `email` | VARCHAR(100) | Customer email address | Not null, unique, valid format | john.smith@example.com |
| `revenue` | DECIMAL(10,2) | Sale amount in USD | Positive, matches product pricing | 25000.00 |
| `cash_collected` | DECIMAL(10,2) | Actual cash collected | 85-95% of revenue | 22500.50 |
| `product` | VARCHAR(100) | Product/program name | One of 3 coaching programs | Executive Leadership Mastery |
| `closer` | VARCHAR(50) | Sales closer name | One of 3 sales team members | Sarah Mitchell |
| `country` | VARCHAR(10) | Customer country | US, UK, or EU | US |
| `upsell` | BOOLEAN | Upsell purchase flag | TRUE or FALSE | TRUE |

## Products

### Elite Business Accelerator
- **Price**: $15,000
- **Target Audience**: Small business owners scaling to 6 figures
- **Duration**: 12 weeks
- **Volume**: ~50% of sales (most popular)

### Executive Leadership Mastery
- **Price**: $25,000
- **Target Audience**: Mid-level executives and business leaders
- **Duration**: 6 months
- **Volume**: ~35% of sales

### Scale to 7-Figures Program
- **Price**: $50,000
- **Target Audience**: Established businesses scaling to 7 figures
- **Duration**: 12 months
- **Volume**: ~15% of sales (premium tier)

## Sales Team (Closers)

### Sarah Mitchell
- **Performance Level**: High performer
- **Sales Volume**: ~40% of total deals
- **Characteristics**: Consistently closes high-value deals

### Marcus Thompson
- **Performance Level**: Consistent performer
- **Sales Volume**: ~35% of total deals
- **Characteristics**: Steady, reliable conversion rates

### Julia Rodriguez
- **Performance Level**: Developing performer
- **Sales Volume**: ~25% of total deals
- **Characteristics**: Growing closer, improving performance

## Geographic Markets

### United States (US)
- **Market Share**: 60% of sales
- **Characteristics**: Primary market, highest volume

### United Kingdom (UK)
- **Market Share**: 20% of sales
- **Characteristics**: Strong secondary market

### European Union (EU)
- **Market Share**: 20% of sales
- **Characteristics**: Growing market presence

## Business Rules & Logic

### Cash Collection
- **Rate**: 85-95% of revenue
- **Variance**: Reflects payment plans, partial payments, and occasional defaults
- **Calculation**: `cash_collected = revenue * random(0.85, 0.95)`

### Upsell Flag
- **Base Rate**: 20-30% across all products
- **Product Influence**:
  - Elite Business Accelerator: ~20% upsell rate
  - Executive Leadership Mastery: ~25% upsell rate
  - Scale to 7-Figures Program: ~30% upsell rate
- **Definition**: Indicates customer purchased additional services/upgrades

### Seasonal Patterns
- **Q1 (Jan-Mar)**: 15% of annual sales - Slower period post-holidays
- **Q2 (Apr-Jun)**: 25% of annual sales - Growth period
- **Q3 (Jul-Sep)**: 28% of annual sales - Moderate period
- **Q4 (Oct-Nov)**: 32% of YTD sales - Strong period (only 2 months)

### Date Distribution
- **Weekday Preference**: ~80% of sales occur on weekdays (Mon-Fri)
- **Weekend Sales**: ~20% occur on weekends
- **Rationale**: Reflects typical B2B sales patterns

## Data Quality

### Validation Checks
- ✓ No duplicate email addresses
- ✓ All dates within valid range (2025-01-01 to 2025-11-30)
- ✓ Revenue matches product pricing exactly
- ✓ Cash collected is between 85-95% of revenue
- ✓ All closers, products, and countries from predefined lists
- ✓ Upsell rate between 20-30%

### Statistics (195 Records)
- **Total Revenue**: $4,380,000
- **Average Deal Size**: $22,461.54
- **Average Cash Collection Rate**: 90.0%
- **Overall Upsell Rate**: 25.1%

## Use Cases

This dataset is designed for demonstrating:
1. **SQL Analysis**: Aggregations, window functions, time-series queries, cohort analysis
2. **Python Analysis**: Pandas EDA, statistical analysis, correlation studies
3. **Data Visualization**: Revenue trends, product performance, geographic distribution
4. **API Development**: RESTful endpoints for data access and filtering
5. **Business Intelligence**: KPI tracking, performance metrics, forecasting

## Data Generation

- **Method**: Programmatically generated using Python (Faker library)
- **Seed**: Fixed seed (42) for reproducibility
- **Realistic Patterns**: Business logic applied for realistic distributions
- **Anonymization**: All customer names and emails are fictional

## Notes

- This is **mock data** for educational and portfolio purposes
- All customer information is generated and not based on real individuals
- Revenue figures are representative of high-ticket coaching industry
- Seasonal patterns reflect typical B2B sales cycles
- Data can be regenerated with different seed for variation

## Related Files

- **Source Script**: `src/data_generation.py`
- **Configuration**: `src/config.py`
- **Raw Data**: `data/raw/coaching_sales_2025.csv`
- **Requirements**: `specs/coaching-analytics-project/requirements.md`
- **Implementation Plan**: `specs/coaching-analytics-project/implementation-plan.md`

## Version History

- **v1.0** (2025-11-15): Initial dataset generation - 195 records, 11 months 2025
