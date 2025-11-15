# API Documentation - Business Coaching Analytics

## Overview

The Coaching Analytics API provides comprehensive access to business coaching sales data, metrics, and AI-powered insights. Built with FastAPI, it offers a RESTful interface with automatic OpenAPI documentation.

**Base URL**: `http://localhost:8000`
**API Version**: 1.0.0

## Quick Start

### Starting the API Server

```bash
# From project root
cd api
python main.py

# Or using uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Interactive Documentation

Once the server is running, access interactive documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, the API does not require authentication. This can be added in future versions using JWT tokens or API keys.

## Endpoints

### Root Endpoints

#### GET `/`
Welcome message with API information and links.

**Response**:
```json
{
  "message": "Welcome to the Coaching Analytics API",
  "version": "1.0.0",
  "documentation": "/docs",
  "endpoints": {
    "sales": "/api/sales",
    "metrics": "/api/metrics/summary",
    "export": "/api/export/csv or /api/export/json"
  }
}
```

#### GET `/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Sales Endpoints

### GET `/api/sales`

Get paginated list of sales with optional filtering.

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number (min: 1) |
| page_size | integer | No | 50 | Items per page (min: 1, max: 200) |
| start_date | date | No | None | Filter from date (YYYY-MM-DD) |
| end_date | date | No | None | Filter to date (YYYY-MM-DD) |
| product | string | No | None | Filter by product name |
| closer | string | No | None | Filter by closer name |
| country | string | No | None | Filter by country (US, UK, EU) |

**Example Request**:
```bash
# Get first page of all sales
curl http://localhost:8000/api/sales

# Get sales for specific product with date range
curl "http://localhost:8000/api/sales?product=Elite%20Business%20Accelerator&start_date=2025-01-01&end_date=2025-03-31"

# Get sales by closer
curl "http://localhost:8000/api/sales?closer=Sarah%20Mitchell&page_size=100"
```

**Response**:
```json
{
  "total": 195,
  "page": 1,
  "page_size": 50,
  "total_pages": 4,
  "sales": [
    {
      "sale_id": 1,
      "sale_date": "2025-01-15",
      "product": "Elite Business Accelerator",
      "revenue": 15000.00,
      "cash_collected": 13500.00,
      "closer": "Sarah Mitchell",
      "country": "US",
      "upsell": false
    }
  ]
}
```

### GET `/api/sales/{sale_id}`

Get a single sale by ID.

**Path Parameters**:
- `sale_id` (integer): Unique sale identifier

**Example Request**:
```bash
curl http://localhost:8000/api/sales/42
```

**Response**:
```json
{
  "sale_id": 42,
  "sale_date": "2025-03-10",
  "product": "Executive Leadership Mastery",
  "revenue": 25000.00,
  "cash_collected": 23750.00,
  "closer": "Marcus Thompson",
  "country": "UK",
  "upsell": true
}
```

**Error Response** (404):
```json
{
  "detail": "Sale with ID 999 not found"
}
```

---

## Metrics Endpoints

### GET `/api/metrics/summary`

Get aggregate summary metrics across all sales.

**Query Parameters**: Same filtering options as `/api/sales` (start_date, end_date, product, closer, country)

**Example Request**:
```bash
# Get overall summary
curl http://localhost:8000/api/metrics/summary

# Get summary for Q1 2025
curl "http://localhost:8000/api/metrics/summary?start_date=2025-01-01&end_date=2025-03-31"
```

**Response**:
```json
{
  "total_revenue": 5847500.00,
  "total_cash_collected": 5290456.25,
  "total_sales": 195,
  "average_deal_size": 29987.18,
  "cash_collection_rate": 90.47,
  "upsell_rate": 25.64,
  "unique_closers": 3
}
```

### GET `/api/metrics/by-product`

Get performance metrics grouped by product.

**Query Parameters**:
- `start_date` (date, optional): Filter from date
- `end_date` (date, optional): Filter to date

**Example Request**:
```bash
curl http://localhost:8000/api/metrics/by-product
```

**Response**:
```json
[
  {
    "product": "Scale to 7-Figures Program",
    "total_revenue": 3250000.00,
    "total_sales": 65,
    "average_deal_size": 50000.00,
    "cash_collection_rate": 91.25,
    "upsell_rate": 27.69
  },
  {
    "product": "Executive Leadership Mastery",
    "total_revenue": 1575000.00,
    "total_sales": 63,
    "average_deal_size": 25000.00,
    "cash_collection_rate": 89.84,
    "upsell_rate": 25.40
  },
  {
    "product": "Elite Business Accelerator",
    "total_revenue": 1022500.00,
    "total_sales": 67,
    "average_deal_size": 15000.00,
    "cash_collection_rate": 90.33,
    "upsell_rate": 23.88
  }
]
```

### GET `/api/metrics/by-closer`

Get performance metrics grouped by sales closer.

**Query Parameters**:
- `start_date` (date, optional): Filter from date
- `end_date` (date, optional): Filter to date

**Example Request**:
```bash
curl http://localhost:8000/api/metrics/by-closer
```

**Response**:
```json
[
  {
    "closer": "Sarah Mitchell",
    "total_revenue": 2339000.00,
    "total_sales": 78,
    "average_deal_size": 29987.18,
    "cash_collection_rate": 90.55,
    "upsell_rate": 26.92
  },
  {
    "closer": "Marcus Thompson",
    "total_revenue": 2095500.00,
    "total_sales": 68,
    "average_deal_size": 30816.18,
    "cash_collection_rate": 90.25,
    "upsell_rate": 25.00
  },
  {
    "closer": "Julia Rodriguez",
    "total_revenue": 1413000.00,
    "total_sales": 49,
    "average_deal_size": 28836.73,
    "cash_collection_rate": 90.65,
    "upsell_rate": 24.49
  }
]
```

### GET `/api/metrics/by-country`

Get performance metrics grouped by country.

**Query Parameters**:
- `start_date` (date, optional): Filter from date
- `end_date` (date, optional): Filter to date

**Example Request**:
```bash
curl http://localhost:8000/api/metrics/by-country
```

**Response**:
```json
[
  {
    "country": "US",
    "total_revenue": 3508500.00,
    "total_sales": 117,
    "average_deal_size": 29987.18,
    "revenue_percentage": 60.00
  },
  {
    "country": "UK",
    "total_revenue": 1169500.00,
    "total_sales": 39,
    "average_deal_size": 29987.18,
    "revenue_percentage": 20.00
  },
  {
    "country": "EU",
    "total_revenue": 1169500.00,
    "total_sales": 39,
    "average_deal_size": 29987.18,
    "revenue_percentage": 20.00
  }
]
```

### GET `/api/metrics/time-series`

Get metrics as monthly time series data.

**Query Parameters**:
- `start_date` (date, optional): Filter from date
- `end_date` (date, optional): Filter to date

**Example Request**:
```bash
curl http://localhost:8000/api/metrics/time-series
```

**Response**:
```json
[
  {
    "period": "2025-01",
    "total_revenue": 450000.00,
    "total_sales": 15,
    "average_deal_size": 30000.00
  },
  {
    "period": "2025-02",
    "total_revenue": 750000.00,
    "total_sales": 25,
    "average_deal_size": 30000.00
  }
]
```

---

## Export Endpoints

### GET `/api/export/csv`

Export sales data as downloadable CSV file.

**Query Parameters**: Same filtering options as `/api/sales`

**Example Request**:
```bash
# Export all sales
curl -O http://localhost:8000/api/export/csv

# Export filtered sales
curl -O "http://localhost:8000/api/export/csv?product=Elite%20Business%20Accelerator&start_date=2025-01-01"
```

**Response**: CSV file download with name `sales_export.csv`

### GET `/api/export/json`

Export sales data as downloadable JSON file.

**Query Parameters**: Same filtering options as `/api/sales`

**Example Request**:
```bash
curl -O http://localhost:8000/api/export/json
```

**Response**: JSON file download with name `sales_export.json`

**JSON Structure**:
```json
{
  "total_records": 195,
  "export_date": "2025-11-15",
  "filters": {
    "start_date": null,
    "end_date": null,
    "product": null,
    "closer": null,
    "country": null
  },
  "sales": [...]
}
```

---

## AI Insights Endpoint

### POST `/api/insights/ai`

Get AI-powered insights from natural language queries.

**Request Body**:
```json
{
  "query": "What is our total revenue?",
  "context": "Q1 2025 performance review"
}
```

**Example Requests**:
```bash
# Simple query
curl -X POST http://localhost:8000/api/insights/ai \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our total revenue?"}'

# Query with context
curl -X POST http://localhost:8000/api/insights/ai \
  -H "Content-Type: application/json" \
  -d '{"query": "Which product performs best?", "context": "Looking for growth opportunities"}'
```

**Example Queries**:
- "What is our total revenue?"
- "Which product performs best?"
- "Who is the top closer?"
- "What are the revenue trends?"
- "Show me the best performers"

**Response**:
```json
{
  "query": "What is our total revenue?",
  "insight": "Based on the data, total revenue is $5,847,500.00 from 195 sales. The average deal size is $29,987.18 with a cash collection rate of 90.5%.",
  "data_points": {
    "total_revenue": 5847500.00,
    "total_sales": 195,
    "average_deal_size": 29987.18,
    "cash_collection_rate": 90.47
  },
  "confidence": 0.7
}
```

**Note**: Currently uses rule-based fallback. Set `SPHINX_API_KEY` environment variable to enable enhanced AI features with Sphinx.ai.

---

## Error Responses

All endpoints return standard HTTP status codes:

- **200 OK**: Successful request
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Invalid parameters
- **500 Internal Server Error**: Server error

**Error Response Format**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Data Models

### Sale Object
```json
{
  "sale_id": 1,
  "sale_date": "2025-01-15",
  "product": "Elite Business Accelerator",
  "revenue": 15000.00,
  "cash_collected": 13500.00,
  "closer": "Sarah Mitchell",
  "country": "US",
  "upsell": false
}
```

### Products
- Elite Business Accelerator ($15,000)
- Executive Leadership Mastery ($25,000)
- Scale to 7-Figures Program ($50,000)

### Closers
- Sarah Mitchell
- Marcus Thompson
- Julia Rodriguez

### Countries
- US (United States)
- UK (United Kingdom)
- EU (European Union)

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production environments.

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Get summary metrics
response = requests.get(f"{BASE_URL}/api/metrics/summary")
metrics = response.json()
print(f"Total Revenue: ${metrics['total_revenue']:,.2f}")

# Get sales with filtering
params = {
    "product": "Elite Business Accelerator",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "page_size": 100
}
response = requests.get(f"{BASE_URL}/api/sales", params=params)
sales_data = response.json()
print(f"Found {sales_data['total']} sales")

# Get AI insights
insight_request = {
    "query": "Which closer has the best upsell rate?"
}
response = requests.post(
    f"{BASE_URL}/api/insights/ai",
    json=insight_request
)
insight = response.json()
print(insight['insight'])

# Export data
response = requests.get(f"{BASE_URL}/api/export/csv")
with open("sales_export.csv", "wb") as f:
    f.write(response.content)
```

---

## JavaScript/TypeScript Client Example

```javascript
const BASE_URL = 'http://localhost:8000';

// Get summary metrics
async function getSummary() {
  const response = await fetch(`${BASE_URL}/api/metrics/summary`);
  const metrics = await response.json();
  console.log(`Total Revenue: $${metrics.total_revenue.toLocaleString()}`);
}

// Get sales with filtering
async function getSales() {
  const params = new URLSearchParams({
    product: 'Elite Business Accelerator',
    start_date: '2025-01-01',
    end_date: '2025-03-31',
    page_size: '100'
  });

  const response = await fetch(`${BASE_URL}/api/sales?${params}`);
  const data = await response.json();
  console.log(`Found ${data.total} sales`);
  return data.sales;
}

// Get AI insights
async function getInsights(query) {
  const response = await fetch(`${BASE_URL}/api/insights/ai`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query })
  });

  const insight = await response.json();
  console.log(insight.insight);
}

// Export data
async function exportData() {
  const response = await fetch(`${BASE_URL}/api/export/json`);
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'sales_export.json';
  a.click();
}
```

---

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get all sales
curl http://localhost:8000/api/sales

# Get specific sale
curl http://localhost:8000/api/sales/1

# Get metrics
curl http://localhost:8000/api/metrics/summary
curl http://localhost:8000/api/metrics/by-product
curl http://localhost:8000/api/metrics/by-closer

# Export data
curl -O http://localhost:8000/api/export/csv

# AI insights
curl -X POST http://localhost:8000/api/insights/ai \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our best performing product?"}'
```

### Using Python requests

```python
import requests

# Test all endpoints
base_url = "http://localhost:8000"

# Health check
print(requests.get(f"{base_url}/health").json())

# Get sales
print(requests.get(f"{base_url}/api/sales").json())

# Get metrics
print(requests.get(f"{base_url}/api/metrics/summary").json())
```

---

## Configuration

API configuration is managed through environment variables:

```bash
# .env file
API_HOST=0.0.0.0
API_PORT=8000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=coaching_analytics
DB_USER=postgres
DB_PASSWORD=your_password
SPHINX_API_KEY=your_sphinx_api_key  # Optional
```

---

## Deployment Notes

### Production Considerations

1. **Database Connection Pooling**: Implement connection pooling for better performance
2. **CORS Configuration**: Configure CORS for frontend applications
3. **Authentication**: Add JWT or API key authentication
4. **Rate Limiting**: Implement rate limiting to prevent abuse
5. **HTTPS**: Deploy behind reverse proxy with SSL/TLS
6. **Logging**: Add structured logging for monitoring
7. **Error Handling**: Enhance error messages for production

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t coaching-analytics-api .
docker run -p 8000:8000 --env-file .env coaching-analytics-api
```

---

## Support

For issues or questions:
1. Check the interactive documentation at `/docs`
2. Review this documentation
3. Check application logs for error details

---

## Version History

- **v1.0.0** (2025-11-15): Initial release
  - Core sales and metrics endpoints
  - Export functionality
  - AI insights with rule-based fallback
  - Comprehensive filtering options
