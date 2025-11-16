"""
FastAPI application for Business Coaching Analytics.

This API provides endpoints for accessing sales data, metrics, and AI-powered insights.
Includes API key authentication, CORS, and rate limiting for security.
"""
from fastapi import FastAPI, HTTPException, Query, Security, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional, List
from datetime import date
import io
import csv
import json
import math
import sys
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from src.config import API_CONFIG
from src.db_utils import close_connection_pool

from api.models import (
    SaleResponse,
    SalesListResponse,
    MetricsSummary,
    ProductMetrics,
    CloserMetrics,
    CountryMetrics,
    TimeSeriesPoint,
    AIInsightRequest,
    AIInsightResponse,
)
from api.database import (
    get_all_sales,
    get_sale_by_id,
    get_metrics_summary,
    get_metrics_by_product,
    get_metrics_by_closer,
    get_metrics_by_country,
    get_time_series_metrics,
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Load API keys from environment
VALID_API_KEYS = os.getenv("API_KEYS", "dev_key_12345").split(",")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key for protected endpoints.

    For development: API key is optional (returns None if not provided)
    For production: Set REQUIRE_API_KEY=true in .env to enforce
    """
    require_api_key = os.getenv("REQUIRE_API_KEY", "false").lower() == "true"

    if not require_api_key and api_key is None:
        logger.warning("API key not provided - running in development mode")
        return None

    if api_key not in VALID_API_KEYS:
        logger.warning(f"Invalid API key attempt: {api_key[:10] if api_key else 'None'}...")
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )

    return api_key

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info("Starting Business Coaching Analytics API...")
    logger.info(f"API Version: {API_CONFIG['version']}")
    logger.info(f"Rate Limiting: Enabled")
    logger.info(f"CORS: Enabled")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down API...")
    close_connection_pool()
    logger.info("Database connection pool closed")


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with welcome message and links"""
    return {
        "message": "Welcome to the Coaching Analytics API",
        "version": API_CONFIG["version"],
        "documentation": "/docs",
        "endpoints": {
            "sales": "/api/sales",
            "metrics": "/api/metrics/summary",
            "export": "/api/export/csv or /api/export/json",
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": API_CONFIG["version"]}


# Sales Endpoints
@app.get("/api/sales", response_model=SalesListResponse, tags=["Sales"])
@limiter.limit("100/minute")
async def list_sales(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Number of items per page"),
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    closer: Optional[str] = Query(None, description="Filter by closer name"),
    country: Optional[str] = Query(None, description="Filter by country code (US, UK, EU)"),
    api_key: str = Depends(verify_api_key),
):
    """
    Get list of all sales with pagination and filtering options.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50, max: 200)
    - **start_date**: Filter sales from this date onwards
    - **end_date**: Filter sales up to this date
    - **product**: Filter by specific product
    - **closer**: Filter by specific closer
    - **country**: Filter by specific country
    """
    try:
        sales, total = get_all_sales(
            page=page,
            page_size=page_size,
            start_date=start_date,
            end_date=end_date,
            product=product,
            closer=closer,
            country=country,
        )

        total_pages = math.ceil(total / page_size) if total > 0 else 0

        return SalesListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            sales=[SaleResponse(**sale) for sale in sales],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales: {str(e)}")


@app.get("/api/sales/{sale_id}", response_model=SaleResponse, tags=["Sales"])
async def get_sale(sale_id: int):
    """
    Get a single sale by ID.

    - **sale_id**: Unique identifier of the sale
    """
    try:
        sale = get_sale_by_id(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale with ID {sale_id} not found")
        return SaleResponse(**sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sale: {str(e)}")


# Metrics Endpoints
@app.get("/api/metrics/summary", response_model=MetricsSummary, tags=["Metrics"])
async def get_summary_metrics(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    closer: Optional[str] = Query(None, description="Filter by closer name"),
    country: Optional[str] = Query(None, description="Filter by country code (US, UK, EU)"),
):
    """
    Get summary metrics across all sales with optional filtering.

    Returns aggregate metrics including:
    - Total revenue and cash collected
    - Number of sales and average deal size
    - Cash collection rate and upsell rate
    - Number of unique closers
    """
    try:
        metrics = get_metrics_summary(
            start_date=start_date,
            end_date=end_date,
            product=product,
            closer=closer,
            country=country,
        )
        return MetricsSummary(**metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summary metrics: {str(e)}")


@app.get("/api/metrics/by-product", response_model=List[ProductMetrics], tags=["Metrics"])
async def get_product_metrics(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
):
    """
    Get metrics grouped by product.

    Returns performance metrics for each product including revenue, sales count,
    average deal size, cash collection rate, and upsell rate.
    """
    try:
        metrics = get_metrics_by_product(start_date=start_date, end_date=end_date)
        return [ProductMetrics(**m) for m in metrics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product metrics: {str(e)}")


@app.get("/api/metrics/by-closer", response_model=List[CloserMetrics], tags=["Metrics"])
async def get_closer_metrics(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
):
    """
    Get metrics grouped by closer.

    Returns performance metrics for each sales closer including revenue, sales count,
    average deal size, cash collection rate, and upsell rate.
    """
    try:
        metrics = get_metrics_by_closer(start_date=start_date, end_date=end_date)
        return [CloserMetrics(**m) for m in metrics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching closer metrics: {str(e)}")


@app.get("/api/metrics/by-country", response_model=List[CountryMetrics], tags=["Metrics"])
async def get_country_metrics(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
):
    """
    Get metrics grouped by country.

    Returns performance metrics for each country including revenue, sales count,
    average deal size, and percentage of total revenue.
    """
    try:
        metrics = get_metrics_by_country(start_date=start_date, end_date=end_date)
        return [CountryMetrics(**m) for m in metrics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching country metrics: {str(e)}")


@app.get("/api/metrics/time-series", response_model=List[TimeSeriesPoint], tags=["Metrics"])
async def get_time_series(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
):
    """
    Get metrics as a time series by month.

    Returns monthly aggregated metrics including revenue, sales count,
    and average deal size over time.
    """
    try:
        metrics = get_time_series_metrics(start_date=start_date, end_date=end_date)
        return [TimeSeriesPoint(**m) for m in metrics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching time series metrics: {str(e)}")


# Export Endpoints
@app.get("/api/export/csv", tags=["Export"])
async def export_csv(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    closer: Optional[str] = Query(None, description="Filter by closer name"),
    country: Optional[str] = Query(None, description="Filter by country code (US, UK, EU)"),
):
    """
    Export filtered sales data as CSV file.

    Returns a downloadable CSV file with all matching sales records.
    """
    try:
        # Get all sales without pagination
        sales, _ = get_all_sales(
            page=1,
            page_size=10000,  # Large number to get all results
            start_date=start_date,
            end_date=end_date,
            product=product,
            closer=closer,
            country=country,
        )

        if not sales:
            raise HTTPException(status_code=404, detail="No sales data found with given filters")

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=sales[0].keys())
        writer.writeheader()
        writer.writerows(sales)

        # Create streaming response
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sales_export.csv"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")


@app.get("/api/export/json", tags=["Export"])
async def export_json(
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    closer: Optional[str] = Query(None, description="Filter by closer name"),
    country: Optional[str] = Query(None, description="Filter by country code (US, UK, EU)"),
):
    """
    Export filtered sales data as JSON file.

    Returns a downloadable JSON file with all matching sales records.
    """
    try:
        # Get all sales without pagination
        sales, total = get_all_sales(
            page=1,
            page_size=10000,  # Large number to get all results
            start_date=start_date,
            end_date=end_date,
            product=product,
            closer=closer,
            country=country,
        )

        if not sales:
            raise HTTPException(status_code=404, detail="No sales data found with given filters")

        # Convert dates to strings for JSON serialization
        for sale in sales:
            if 'sale_date' in sale and isinstance(sale['sale_date'], date):
                sale['sale_date'] = sale['sale_date'].isoformat()

        export_data = {
            "total_records": total,
            "export_date": date.today().isoformat(),
            "filters": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
                "product": product,
                "closer": closer,
                "country": country,
            },
            "sales": sales
        }

        # Create JSON response
        json_str = json.dumps(export_data, indent=2, default=str)

        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=sales_export.json"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting JSON: {str(e)}")


# AI Insights Endpoint
@app.post("/api/insights/ai", response_model=AIInsightResponse, tags=["AI Insights"])
async def get_ai_insights(request: AIInsightRequest):
    """
    Get AI-powered insights using natural language queries.

    This endpoint accepts natural language queries and returns AI-generated insights
    based on the sales data. Currently uses a rule-based fallback system.

    **Examples**:
    - "What is our total revenue?"
    - "Which product performs best?"
    - "Who is the top closer?"
    - "What are the revenue trends?"

    **Note**: Full Sphinx.ai integration requires API credentials in .env file.
    Set SPHINX_API_KEY to enable enhanced AI features.
    """
    try:
        from api.sphinx_integration import get_ai_insight

        result = await get_ai_insight(request.query, request.context)

        return AIInsightResponse(
            query=request.query,
            insight=result["insight"],
            data_points=result.get("data_points"),
            confidence=result.get("confidence")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI insights: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True
    )
