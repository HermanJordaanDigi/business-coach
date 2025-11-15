# Business Coaching Analytics Project - Requirements

## Project Overview
A comprehensive data analytics project for a high-ticket online business coaching company. This project demonstrates skills in SQL, Python, API development, data visualization, and AI-powered insights using Sphinx.ai.

## Business Context
- **Company Type**: High-ticket online coaching business specializing in business consulting
- **Products**: 3 premium coaching programs at different price points
- **Sales Team**: 3 closers with varying performance profiles
- **Market**: US, UK, and EU territories
- **Time Period**: January - November 2025 (Year-to-date)

## Dataset Requirements

### Data Volume
- **Total Records**: 195 rows
- **Time Coverage**: 11 months (Jan - Nov 2025)
- **Distribution**: Realistic spread across months with seasonal patterns

### Schema Design
The dataset must include the following columns:

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| `date` | DATE | Transaction date (2025-01-01 to 2025-11-30) |
| `name` | VARCHAR(100) | Customer full name |
| `email` | VARCHAR(100) | Customer email address |
| `revenue` | DECIMAL(10,2) | Sale amount in USD |
| `cash_collected` | DECIMAL(10,2) | Actual cash collected from sale |
| `product` | VARCHAR(100) | Product/program name |
| `closer` | VARCHAR(50) | Sales closer name |
| `country` | VARCHAR(10) | Customer country (US, UK, EU) |
| `upsell` | BOOLEAN | Whether customer purchased upsell |

### Product Specifications
Three high-ticket coaching programs:

1. **Elite Business Accelerator**
   - Price: $3,000
   - Target: Small business owners scaling to 6 figures
   - Duration: 12 weeks

2. **Executive Leadership Mastery**
   - Price: $7,000
   - Target: Mid-level executives and business leaders
   - Duration: 6 months

3. **Scale to 7-Figures Program**
   - Price: $15,000
   - Target: Established businesses scaling to 7 figures
   - Duration: 12 months

### Sales Team (Closers)
Three sales professionals with distinct profiles:

1. **Sarah Mitchell** - High performer (40% of deals)
2. **Marcus Thompson** - Consistent performer (35% of deals)
3. **Julia Rodriguez** - Developing performer (25% of deals)

### Geographic Distribution
- **United States**: 60% of sales
- **United Kingdom**: 20% of sales
- **European Union**: 20% of sales

### Business Logic Rules
1. **Cash Collection Rate**: 85-95% of revenue (payment plans, defaults)
2. **Upsell Rate**: 20-30% across all products
3. **Seasonal Patterns**:
   - Q1 (Jan-Mar): Slower period (15% of annual)
   - Q2 (Apr-Jun): Growth period (25% of annual)
   - Q3 (Jul-Sep): Moderate period (28% of annual)
   - Q4 (Oct-Nov): Strong period (32% of annual YTD)
4. **Realistic Constraints**:
   - No sales on weekends for some months
   - Names and emails must be realistic
   - Each customer should be unique

## Technical Requirements

### Database
- **Technology**: PostgreSQL 14+
- **Database Name**: `coaching_analytics`
- **Schema**: Public schema
- **Table Name**: `sales`
- **Indexes**: On date, product, closer, country for query performance
- **Constraints**: Primary key, NOT NULL where appropriate

### Programming Languages & Frameworks
- **Python**: 3.11+
- **SQL**: PostgreSQL dialect
- **API Framework**: FastAPI
- **Data Analysis**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Database Driver**: psycopg2 or asyncpg
- **Environment Management**: uv (already in project)

### Analysis Capabilities Required

#### SQL Analysis
Demonstrate proficiency with:
- Aggregation queries (SUM, AVG, COUNT, GROUP BY)
- Window functions (ROW_NUMBER, RANK, LAG/LEAD)
- CTEs (Common Table Expressions)
- Joins (if multi-table design)
- Date functions and time-series queries
- Subqueries and complex filtering

#### Python Analysis
Showcase skills in:
- Data loading from PostgreSQL
- Data cleaning and validation
- Exploratory Data Analysis (EDA)
- Statistical analysis
- Time series analysis
- Cohort analysis
- Customer segmentation
- Correlation analysis

#### API Development
Build RESTful API with:
- Multiple endpoints for data access
- Query parameter filtering
- Aggregation endpoints
- Data export capabilities (CSV, JSON)
- Error handling and validation
- API documentation (Swagger/OpenAPI)

#### Data Visualization
Create insightful visualizations:
- Revenue trends over time (line charts)
- Product performance comparison (bar charts)
- Closer leaderboards (horizontal bars)
- Geographic distribution (pie/donut charts)
- Cash collection funnel analysis
- Upsell conversion rates
- Monthly performance dashboards
- Interactive plots where beneficial

#### Sphinx.ai Integration
- Connect to Sphinx.ai API
- Natural language query capability
- AI-generated insights
- Anomaly detection
- Predictive recommendations

## Deliverables

### Core Deliverables
1. **Mock Dataset**: CSV file with 195 realistic records
2. **Database Schema**: PostgreSQL schema with indexes
3. **Data Loading Script**: Python script to load CSV into PostgreSQL
4. **SQL Query Library**: Collection of analytical SQL queries
5. **Python Analysis Scripts**: EDA and statistical analysis
6. **Visualization Suite**: Multiple charts and dashboards
7. **REST API**: FastAPI application with endpoints
8. **Sphinx.ai Integration**: AI-powered insights module
9. **Insights Report**: Business insights and recommendations

### Documentation
1. **README.md**: Project overview and setup instructions
2. **requirements.txt**: Python dependencies
3. **API Documentation**: Endpoint documentation
4. **Database Documentation**: Schema and query examples
5. **Analysis Documentation**: Methodology and findings

## Success Criteria
- Dataset is realistic and follows business logic
- SQL queries demonstrate advanced capabilities
- Python analysis provides actionable insights
- Visualizations are clear and professional
- API is functional and well-documented
- Sphinx.ai integration provides value
- Project demonstrates portfolio-worthy skills

## Out of Scope
- Unit testing
- End-to-end testing
- Deployment to production
- User authentication/authorization
- Frontend/dashboard application
- Real-time data streaming
- Machine learning models (unless time permits)

## Assumptions
- Local development environment
- PostgreSQL is installed or will be installed
- Project is for portfolio/learning purposes
- Sphinx.ai API access will be configured separately
- Data is fictional and for demonstration only
