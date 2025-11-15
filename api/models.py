"""
Pydantic models for API request/response schemas.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SaleBase(BaseModel):
    """Base model for sale data"""
    sale_id: int = Field(..., description="Unique sale identifier")
    sale_date: date = Field(..., description="Date of the sale")
    product: str = Field(..., description="Product name")
    revenue: float = Field(..., description="Total revenue amount")
    cash_collected: float = Field(..., description="Cash collected amount")
    closer: str = Field(..., description="Sales closer name")
    country: str = Field(..., description="Country code (US, UK, EU)")
    upsell: bool = Field(..., description="Whether this was an upsell")


class SaleResponse(SaleBase):
    """Response model for sale data"""
    model_config = ConfigDict(from_attributes=True)


class SalesListResponse(BaseModel):
    """Response model for list of sales with pagination"""
    total: int = Field(..., description="Total number of sales")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    sales: List[SaleResponse] = Field(..., description="List of sales")


class MetricsSummary(BaseModel):
    """Summary metrics response"""
    total_revenue: float = Field(..., description="Total revenue")
    total_cash_collected: float = Field(..., description="Total cash collected")
    total_sales: int = Field(..., description="Total number of sales")
    average_deal_size: float = Field(..., description="Average deal size")
    cash_collection_rate: float = Field(..., description="Cash collection rate percentage")
    upsell_rate: float = Field(..., description="Upsell rate percentage")
    unique_closers: int = Field(..., description="Number of unique closers")


class ProductMetrics(BaseModel):
    """Metrics by product"""
    product: str = Field(..., description="Product name")
    total_revenue: float = Field(..., description="Total revenue")
    total_sales: int = Field(..., description="Number of sales")
    average_deal_size: float = Field(..., description="Average deal size")
    cash_collection_rate: float = Field(..., description="Cash collection rate percentage")
    upsell_rate: float = Field(..., description="Upsell rate percentage")


class CloserMetrics(BaseModel):
    """Metrics by closer"""
    closer: str = Field(..., description="Closer name")
    total_revenue: float = Field(..., description="Total revenue")
    total_sales: int = Field(..., description="Number of sales")
    average_deal_size: float = Field(..., description="Average deal size")
    cash_collection_rate: float = Field(..., description="Cash collection rate percentage")
    upsell_rate: float = Field(..., description="Upsell rate percentage")


class CountryMetrics(BaseModel):
    """Metrics by country"""
    country: str = Field(..., description="Country code")
    total_revenue: float = Field(..., description="Total revenue")
    total_sales: int = Field(..., description="Number of sales")
    average_deal_size: float = Field(..., description="Average deal size")
    revenue_percentage: float = Field(..., description="Percentage of total revenue")


class TimeSeriesPoint(BaseModel):
    """Single point in time series data"""
    period: str = Field(..., description="Time period (YYYY-MM)")
    total_revenue: float = Field(..., description="Total revenue for period")
    total_sales: int = Field(..., description="Number of sales for period")
    average_deal_size: float = Field(..., description="Average deal size for period")


class AIInsightRequest(BaseModel):
    """Request model for AI insights"""
    query: str = Field(..., description="Natural language query", min_length=1)
    context: Optional[str] = Field(None, description="Additional context for the query")


class AIInsightResponse(BaseModel):
    """Response model for AI insights"""
    query: str = Field(..., description="Original query")
    insight: str = Field(..., description="AI-generated insight")
    data_points: Optional[dict] = Field(None, description="Relevant data points")
    confidence: Optional[float] = Field(None, description="Confidence score")
