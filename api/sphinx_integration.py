"""
Sphinx.ai integration module for AI-powered insights.

This module provides functions to interact with Sphinx.ai API
for natural language queries and AI-generated business insights.
"""
import httpx
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from src.config import SPHINX_CONFIG

from api.database import (
    get_metrics_summary,
    get_metrics_by_product,
    get_metrics_by_closer,
    get_time_series_metrics,
)


class SphinxAIClient:
    """Client for interacting with Sphinx.ai API"""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize Sphinx.ai client.

        Args:
            api_key: Sphinx.ai API key (defaults to config)
            api_url: Sphinx.ai API URL (defaults to config)
        """
        self.api_key = api_key or SPHINX_CONFIG["api_key"]
        self.api_url = api_url or SPHINX_CONFIG["api_url"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def generate_insight(
        self,
        query: str,
        context: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate AI insights based on a natural language query.

        Args:
            query: Natural language query from the user
            context: Additional context for the query
            data: Relevant data to include in the analysis

        Returns:
            Dictionary with insight, confidence score, and data points
        """
        if not self.api_key:
            return self._generate_fallback_insight(query, data)

        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "query": query,
                    "context": context or "Business coaching sales analytics",
                    "data": data,
                }

                response = await client.post(
                    f"{self.api_url}/insights",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0,
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    # Fallback if API call fails
                    return self._generate_fallback_insight(query, data)

        except Exception as e:
            # Fallback on any error
            return self._generate_fallback_insight(query, data, error=str(e))

    def _generate_fallback_insight(
        self,
        query: str,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a fallback insight when Sphinx.ai is not available.

        This provides basic rule-based insights based on the query keywords.
        """
        query_lower = query.lower()

        # Default response
        insight = "Unable to generate AI insight at this time."
        confidence = 0.0
        data_points = {}

        # Rule-based insights based on query keywords
        if any(keyword in query_lower for keyword in ["revenue", "sales", "performance"]):
            summary = get_metrics_summary()
            insight = (
                f"Based on the data, total revenue is ${summary['total_revenue']:,.2f} "
                f"from {summary['total_sales']} sales. "
                f"The average deal size is ${summary['average_deal_size']:,.2f} "
                f"with a cash collection rate of {summary['cash_collection_rate']:.1f}%."
            )
            data_points = summary
            confidence = 0.7

        elif any(keyword in query_lower for keyword in ["product", "products"]):
            products = get_metrics_by_product()
            if products:
                top_product = products[0]
                insight = (
                    f"The top performing product is '{top_product['product']}' "
                    f"with ${top_product['total_revenue']:,.2f} in revenue "
                    f"from {top_product['total_sales']} sales. "
                    f"The average deal size is ${top_product['average_deal_size']:,.2f}."
                )
                data_points = {"products": products}
                confidence = 0.7

        elif any(keyword in query_lower for keyword in ["closer", "closers", "sales team"]):
            closers = get_metrics_by_closer()
            if closers:
                top_closer = closers[0]
                insight = (
                    f"The top performing closer is {top_closer['closer']} "
                    f"with ${top_closer['total_revenue']:,.2f} in revenue "
                    f"from {top_closer['total_sales']} sales. "
                    f"Their average deal size is ${top_closer['average_deal_size']:,.2f} "
                    f"and upsell rate is {top_closer['upsell_rate']:.1f}%."
                )
                data_points = {"closers": closers}
                confidence = 0.7

        elif any(keyword in query_lower for keyword in ["trend", "time", "month", "growth"]):
            time_series = get_time_series_metrics()
            if len(time_series) >= 2:
                latest = time_series[-1]
                previous = time_series[-2]
                change = ((latest['total_revenue'] - previous['total_revenue']) /
                         previous['total_revenue'] * 100)
                direction = "increased" if change > 0 else "decreased"
                insight = (
                    f"Revenue has {direction} by {abs(change):.1f}% from the previous month. "
                    f"In {latest['period']}, revenue was ${latest['total_revenue']:,.2f} "
                    f"from {latest['total_sales']} sales."
                )
                data_points = {"time_series": time_series[-3:]}  # Last 3 months
                confidence = 0.7

        elif any(keyword in query_lower for keyword in ["best", "top", "highest"]):
            products = get_metrics_by_product()
            closers = get_metrics_by_closer()
            insight = (
                f"Top performers: Product - '{products[0]['product']}' "
                f"(${products[0]['total_revenue']:,.2f}), "
                f"Closer - {closers[0]['closer']} "
                f"(${closers[0]['total_revenue']:,.2f})."
            )
            data_points = {
                "top_product": products[0],
                "top_closer": closers[0]
            }
            confidence = 0.7

        # If we have an error, append it to the insight
        if error:
            insight += f" Note: Sphinx.ai API unavailable - {error}"

        return {
            "insight": insight,
            "confidence": confidence,
            "data_points": data_points,
        }


async def get_ai_insight(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to get AI insights.

    Args:
        query: Natural language query
        context: Optional context for the query

    Returns:
        Dictionary with insight, confidence, and data points
    """
    client = SphinxAIClient()

    # Gather relevant data based on query keywords
    query_lower = query.lower()
    data = {}

    if any(keyword in query_lower for keyword in ["all", "summary", "overview"]):
        data["summary"] = get_metrics_summary()
        data["products"] = get_metrics_by_product()
        data["closers"] = get_metrics_by_closer()
    elif "product" in query_lower:
        data["products"] = get_metrics_by_product()
    elif "closer" in query_lower or "sales team" in query_lower:
        data["closers"] = get_metrics_by_closer()
    elif "trend" in query_lower or "time" in query_lower:
        data["time_series"] = get_time_series_metrics()

    return await client.generate_insight(query, context, data)


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    async def test_insights():
        """Test the insights functionality"""
        test_queries = [
            "What is our total revenue?",
            "Which product performs best?",
            "Who is the top closer?",
            "What are the revenue trends?",
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            result = await get_ai_insight(query)
            print(f"Insight: {result['insight']}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            print("-" * 80)

    asyncio.run(test_insights())
