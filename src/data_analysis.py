"""
Comprehensive Python data analysis for Business Coaching Analytics.
Performs statistical analysis, cohort analysis, and generates insights.
"""
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
from typing import Dict, List, Tuple, Any
import json

from src.db_helpers import get_all_sales, get_table_stats
from src.config import REPORTS_DIR


class SalesAnalyzer:
    """Main class for performing sales data analysis."""

    def __init__(self):
        """Initialize the analyzer and load data."""
        print("Loading sales data from database...")
        self.df = get_all_sales()
        self.df['sale_date'] = pd.to_datetime(self.df['sale_date'])

        # Add derived columns
        self.df['year_month'] = self.df['sale_date'].dt.to_period('M')
        self.df['month'] = self.df['sale_date'].dt.month
        self.df['quarter'] = self.df['sale_date'].dt.quarter
        self.df['cash_collection_rate'] = (self.df['cash_collected'] / self.df['revenue']) * 100

        print(f"✓ Loaded {len(self.df)} sales records")
        print(f"✓ Date range: {self.df['sale_date'].min().date()} to {self.df['sale_date'].max().date()}")

        self.insights = []

    def data_quality_checks(self) -> Dict[str, Any]:
        """
        Perform comprehensive data quality checks.

        Returns:
            Dictionary with data quality metrics
        """
        print("\n" + "=" * 60)
        print("DATA QUALITY CHECKS")
        print("=" * 60)

        checks = {
            "total_records": len(self.df),
            "null_values": self.df.isnull().sum().to_dict(),
            "duplicate_records": self.df.duplicated().sum(),
            "date_range": {
                "min": str(self.df['sale_date'].min().date()),
                "max": str(self.df['sale_date'].max().date()),
            },
            "data_types": self.df.dtypes.astype(str).to_dict(),
            "negative_values": {
                "revenue": (self.df['revenue'] < 0).sum(),
                "cash_collected": (self.df['cash_collected'] < 0).sum(),
            },
            "invalid_rates": {
                "cash_collection_over_100": (self.df['cash_collection_rate'] > 100).sum(),
            },
        }

        print(f"\nTotal Records: {checks['total_records']}")
        print(f"Duplicate Records: {checks['duplicate_records']}")
        print(f"Null Values:\n{pd.Series(checks['null_values'])}")
        print(f"Date Range: {checks['date_range']['min']} to {checks['date_range']['max']}")

        # Add insight if data quality is good
        if checks['duplicate_records'] == 0 and all(v == 0 for v in checks['null_values'].values()):
            self.insights.append({
                "category": "Data Quality",
                "insight": "Dataset is clean with no duplicates or missing values",
                "confidence": "High"
            })

        return checks

    def summary_statistics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        print("\n" + "=" * 60)
        print("SUMMARY STATISTICS")
        print("=" * 60)

        summary = {
            "numeric_summary": self.df[['revenue', 'cash_collected', 'cash_collection_rate']].describe().to_dict(),
            "categorical_counts": {
                "products": self.df['product'].value_counts().to_dict(),
                "closers": self.df['closer'].value_counts().to_dict(),
                "countries": self.df['country'].value_counts().to_dict(),
                "upsell": self.df['upsell'].value_counts().to_dict(),
            },
            "totals": {
                "total_revenue": float(self.df['revenue'].sum()),
                "total_cash_collected": float(self.df['cash_collected'].sum()),
                "average_deal_size": float(self.df['revenue'].mean()),
                "median_deal_size": float(self.df['revenue'].median()),
            },
        }

        print("\nNumeric Variables Summary:")
        print(pd.DataFrame(summary['numeric_summary']))

        print("\nTotal Revenue: ${:,.2f}".format(summary['totals']['total_revenue']))
        print("Total Cash Collected: ${:,.2f}".format(summary['totals']['total_cash_collected']))
        print("Average Deal Size: ${:,.2f}".format(summary['totals']['average_deal_size']))
        print("Median Deal Size: ${:,.2f}".format(summary['totals']['median_deal_size']))

        return summary

    def calculate_business_metrics(self) -> Dict[str, Any]:
        """
        Calculate key business metrics.

        Returns:
            Dictionary with business metrics
        """
        print("\n" + "=" * 60)
        print("KEY BUSINESS METRICS")
        print("=" * 60)

        # Overall metrics
        total_sales = len(self.df)
        total_revenue = self.df['revenue'].sum()
        total_cash = self.df['cash_collected'].sum()
        upsell_count = self.df['upsell'].sum()

        metrics = {
            "overall": {
                "total_sales_count": total_sales,
                "total_revenue": float(total_revenue),
                "total_cash_collected": float(total_cash),
                "overall_cash_collection_rate": float((total_cash / total_revenue) * 100),
                "upsell_count": int(upsell_count),
                "upsell_rate": float((upsell_count / total_sales) * 100),
                "average_deal_size": float(self.df['revenue'].mean()),
                "median_deal_size": float(self.df['revenue'].median()),
            },
            "by_product": {},
            "by_closer": {},
            "by_country": {},
        }

        # Product metrics
        for product in self.df['product'].unique():
            product_df = self.df[self.df['product'] == product]
            metrics['by_product'][product] = {
                "count": len(product_df),
                "total_revenue": float(product_df['revenue'].sum()),
                "avg_deal_size": float(product_df['revenue'].mean()),
                "cash_collection_rate": float((product_df['cash_collected'].sum() / product_df['revenue'].sum()) * 100),
                "upsell_rate": float((product_df['upsell'].sum() / len(product_df)) * 100),
            }

        # Closer metrics
        for closer in self.df['closer'].unique():
            closer_df = self.df[self.df['closer'] == closer]
            metrics['by_closer'][closer] = {
                "count": len(closer_df),
                "total_revenue": float(closer_df['revenue'].sum()),
                "avg_deal_size": float(closer_df['revenue'].mean()),
                "cash_collection_rate": float((closer_df['cash_collected'].sum() / closer_df['revenue'].sum()) * 100),
                "upsell_rate": float((closer_df['upsell'].sum() / len(closer_df)) * 100),
            }

        # Country metrics
        for country in self.df['country'].unique():
            country_df = self.df[self.df['country'] == country]
            metrics['by_country'][country] = {
                "count": len(country_df),
                "total_revenue": float(country_df['revenue'].sum()),
                "avg_deal_size": float(country_df['revenue'].mean()),
                "revenue_share": float((country_df['revenue'].sum() / total_revenue) * 100),
            }

        # Print overall metrics
        print("\nOverall Metrics:")
        print(f"  Total Sales: {metrics['overall']['total_sales_count']}")
        print(f"  Total Revenue: ${metrics['overall']['total_revenue']:,.2f}")
        print(f"  Cash Collection Rate: {metrics['overall']['overall_cash_collection_rate']:.2f}%")
        print(f"  Upsell Rate: {metrics['overall']['upsell_rate']:.2f}%")
        print(f"  Average Deal Size: ${metrics['overall']['average_deal_size']:,.2f}")

        # Add insights
        if metrics['overall']['overall_cash_collection_rate'] > 90:
            self.insights.append({
                "category": "Cash Collection",
                "insight": f"Excellent cash collection rate of {metrics['overall']['overall_cash_collection_rate']:.1f}%",
                "confidence": "High"
            })

        if metrics['overall']['upsell_rate'] > 25:
            self.insights.append({
                "category": "Upsells",
                "insight": f"Strong upsell performance at {metrics['overall']['upsell_rate']:.1f}%",
                "confidence": "High"
            })

        return metrics

    def analyze_revenue_trends(self) -> Dict[str, Any]:
        """
        Analyze revenue trends over time.

        Returns:
            Dictionary with time series analysis
        """
        print("\n" + "=" * 60)
        print("REVENUE TRENDS OVER TIME")
        print("=" * 60)

        # Monthly aggregation
        monthly = self.df.groupby('year_month').agg({
            'revenue': ['sum', 'mean', 'count'],
            'cash_collected': 'sum',
            'upsell': 'sum'
        }).round(2)

        monthly.columns = ['_'.join(col).strip() for col in monthly.columns.values]
        monthly = monthly.reset_index()
        monthly['year_month'] = monthly['year_month'].astype(str)

        # Calculate month-over-month growth
        monthly_revenue = self.df.groupby('year_month')['revenue'].sum()
        mom_growth = monthly_revenue.pct_change() * 100

        trends = {
            "monthly_data": monthly.to_dict('records'),
            "growth_metrics": {
                "average_mom_growth": float(mom_growth.mean()),
                "total_growth": float((monthly_revenue.iloc[-1] / monthly_revenue.iloc[0] - 1) * 100),
                "best_month": str(monthly_revenue.idxmax()),
                "best_month_revenue": float(monthly_revenue.max()),
                "worst_month": str(monthly_revenue.idxmin()),
                "worst_month_revenue": float(monthly_revenue.min()),
            },
        }

        print("\nMonthly Revenue:")
        print(monthly[['year_month', 'revenue_sum', 'revenue_count']])

        print(f"\nAverage Month-over-Month Growth: {trends['growth_metrics']['average_mom_growth']:.2f}%")
        print(f"Best Month: {trends['growth_metrics']['best_month']} (${trends['growth_metrics']['best_month_revenue']:,.2f})")

        # Add insight about growth trend
        if trends['growth_metrics']['average_mom_growth'] > 0:
            self.insights.append({
                "category": "Revenue Growth",
                "insight": f"Positive month-over-month growth averaging {trends['growth_metrics']['average_mom_growth']:.1f}%",
                "confidence": "High"
            })

        return trends

    def analyze_product_performance(self) -> Dict[str, Any]:
        """
        Analyze detailed product performance.

        Returns:
            Dictionary with product analysis
        """
        print("\n" + "=" * 60)
        print("PRODUCT PERFORMANCE ANALYSIS")
        print("=" * 60)

        product_analysis = {}

        for product in self.df['product'].unique():
            product_df = self.df[self.df['product'] == product]

            monthly_trend = product_df.groupby('year_month')['revenue'].sum()
            monthly_trend_dict = {str(k): float(v) for k, v in monthly_trend.items()}

            product_analysis[product] = {
                "count": len(product_df),
                "total_revenue": float(product_df['revenue'].sum()),
                "avg_revenue": float(product_df['revenue'].mean()),
                "median_revenue": float(product_df['revenue'].median()),
                "std_revenue": float(product_df['revenue'].std()),
                "min_revenue": float(product_df['revenue'].min()),
                "max_revenue": float(product_df['revenue'].max()),
                "revenue_share": float((product_df['revenue'].sum() / self.df['revenue'].sum()) * 100),
                "cash_collection_rate": float((product_df['cash_collected'].sum() / product_df['revenue'].sum()) * 100),
                "upsell_rate": float((product_df['upsell'].sum() / len(product_df)) * 100),
                "monthly_trend": monthly_trend_dict,
            }

            print(f"\n{product}:")
            print(f"  Sales Count: {product_analysis[product]['count']}")
            print(f"  Total Revenue: ${product_analysis[product]['total_revenue']:,.2f}")
            print(f"  Avg Deal Size: ${product_analysis[product]['avg_revenue']:,.2f}")
            print(f"  Revenue Share: {product_analysis[product]['revenue_share']:.1f}%")
            print(f"  Upsell Rate: {product_analysis[product]['upsell_rate']:.1f}%")

        # Identify top product by revenue
        top_product = max(product_analysis.items(), key=lambda x: x[1]['total_revenue'])
        self.insights.append({
            "category": "Product Performance",
            "insight": f"{top_product[0]} is the top revenue generator with ${top_product[1]['total_revenue']:,.0f} ({top_product[1]['revenue_share']:.1f}% of total)",
            "confidence": "High"
        })

        return product_analysis

    def analyze_closer_performance(self) -> Dict[str, Any]:
        """
        Analyze closer performance with statistical comparisons.

        Returns:
            Dictionary with closer analysis and statistical tests
        """
        print("\n" + "=" * 60)
        print("CLOSER PERFORMANCE ANALYSIS")
        print("=" * 60)

        closer_analysis = {}
        closer_revenues = []

        for closer in self.df['closer'].unique():
            closer_df = self.df[self.df['closer'] == closer]

            closer_analysis[closer] = {
                "count": len(closer_df),
                "total_revenue": float(closer_df['revenue'].sum()),
                "avg_deal_size": float(closer_df['revenue'].mean()),
                "median_deal_size": float(closer_df['revenue'].median()),
                "std_deal_size": float(closer_df['revenue'].std()),
                "cash_collection_rate": float((closer_df['cash_collected'].sum() / closer_df['revenue'].sum()) * 100),
                "upsell_rate": float((closer_df['upsell'].sum() / len(closer_df)) * 100),
                "product_mix": closer_df['product'].value_counts().to_dict(),
                "country_mix": closer_df['country'].value_counts().to_dict(),
            }

            closer_revenues.append(closer_df['revenue'].values)

            print(f"\n{closer}:")
            print(f"  Sales Count: {closer_analysis[closer]['count']}")
            print(f"  Total Revenue: ${closer_analysis[closer]['total_revenue']:,.2f}")
            print(f"  Avg Deal Size: ${closer_analysis[closer]['avg_deal_size']:,.2f}")
            print(f"  Cash Collection: {closer_analysis[closer]['cash_collection_rate']:.1f}%")
            print(f"  Upsell Rate: {closer_analysis[closer]['upsell_rate']:.1f}%")

        # Statistical comparison using ANOVA
        if len(closer_revenues) >= 2:
            f_stat, p_value = stats.f_oneway(*closer_revenues)
            closer_analysis['statistical_test'] = {
                "test": "One-way ANOVA",
                "f_statistic": float(f_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "interpretation": "Significant differences exist between closers" if p_value < 0.05 else "No significant differences between closers"
            }

            print(f"\n\nStatistical Test (ANOVA):")
            print(f"  F-statistic: {f_stat:.4f}")
            print(f"  P-value: {p_value:.4f}")
            print(f"  Result: {closer_analysis['statistical_test']['interpretation']}")

        # Identify top closer
        top_closer = max(closer_analysis.items(), key=lambda x: x[1]['total_revenue'] if isinstance(x[1], dict) and 'total_revenue' in x[1] else 0)
        if isinstance(top_closer[1], dict):
            self.insights.append({
                "category": "Closer Performance",
                "insight": f"{top_closer[0]} is the top performer with ${top_closer[1]['total_revenue']:,.0f} in revenue",
                "confidence": "High"
            })

        return closer_analysis

    def analyze_geographic_performance(self) -> Dict[str, Any]:
        """
        Analyze geographic performance patterns.

        Returns:
            Dictionary with geographic analysis
        """
        print("\n" + "=" * 60)
        print("GEOGRAPHIC PERFORMANCE ANALYSIS")
        print("=" * 60)

        geo_analysis = {}
        total_revenue = self.df['revenue'].sum()

        for country in self.df['country'].unique():
            country_df = self.df[self.df['country'] == country]

            geo_analysis[country] = {
                "count": len(country_df),
                "total_revenue": float(country_df['revenue'].sum()),
                "revenue_share": float((country_df['revenue'].sum() / total_revenue) * 100),
                "avg_deal_size": float(country_df['revenue'].mean()),
                "cash_collection_rate": float((country_df['cash_collected'].sum() / country_df['revenue'].sum()) * 100),
                "upsell_rate": float((country_df['upsell'].sum() / len(country_df)) * 100),
                "product_mix": country_df['product'].value_counts().to_dict(),
                "top_closer": country_df.groupby('closer')['revenue'].sum().idxmax(),
            }

            print(f"\n{country}:")
            print(f"  Sales Count: {geo_analysis[country]['count']}")
            print(f"  Total Revenue: ${geo_analysis[country]['total_revenue']:,.2f}")
            print(f"  Revenue Share: {geo_analysis[country]['revenue_share']:.1f}%")
            print(f"  Avg Deal Size: ${geo_analysis[country]['avg_deal_size']:,.2f}")
            print(f"  Top Closer: {geo_analysis[country]['top_closer']}")

        return geo_analysis

    def calculate_correlations(self) -> Dict[str, Any]:
        """
        Calculate correlation matrix for numeric variables.

        Returns:
            Dictionary with correlation analysis
        """
        print("\n" + "=" * 60)
        print("CORRELATION ANALYSIS")
        print("=" * 60)

        # Select numeric columns
        numeric_cols = ['revenue', 'cash_collected', 'cash_collection_rate']

        # Add encoded categorical variables
        df_corr = self.df[numeric_cols].copy()
        df_corr['upsell_numeric'] = self.df['upsell'].astype(int)

        # Calculate correlation matrix
        corr_matrix = df_corr.corr()

        print("\nCorrelation Matrix:")
        print(corr_matrix)

        # Find strong correlations
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:
                    strong_corr.append({
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "correlation": float(corr_value)
                    })

        correlations = {
            "matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_corr,
        }

        print("\nStrong Correlations (|r| > 0.5):")
        for corr in strong_corr:
            print(f"  {corr['var1']} <-> {corr['var2']}: {corr['correlation']:.3f}")

        return correlations

    def cohort_analysis(self) -> Dict[str, Any]:
        """
        Perform cohort analysis by month.

        Returns:
            Dictionary with cohort analysis
        """
        print("\n" + "=" * 60)
        print("COHORT ANALYSIS BY MONTH")
        print("=" * 60)

        cohorts = {}

        for month_period in self.df['year_month'].unique():
            cohort_df = self.df[self.df['year_month'] == month_period]

            cohorts[str(month_period)] = {
                "month": str(month_period),
                "customer_count": len(cohort_df),
                "total_revenue": float(cohort_df['revenue'].sum()),
                "avg_deal_size": float(cohort_df['revenue'].mean()),
                "cash_collection_rate": float((cohort_df['cash_collected'].sum() / cohort_df['revenue'].sum()) * 100),
                "upsell_rate": float((cohort_df['upsell'].sum() / len(cohort_df)) * 100),
                "product_mix": cohort_df['product'].value_counts().to_dict(),
                "top_product": cohort_df.groupby('product')['revenue'].sum().idxmax(),
                "top_closer": cohort_df.groupby('closer')['revenue'].sum().idxmax(),
            }

        # Print summary
        print("\nMonthly Cohort Summary:")
        cohort_df_summary = pd.DataFrame([
            {
                "Month": v['month'],
                "Customers": v['customer_count'],
                "Revenue": f"${v['total_revenue']:,.0f}",
                "Avg Deal": f"${v['avg_deal_size']:,.0f}",
                "Upsell %": f"{v['upsell_rate']:.1f}%"
            }
            for v in cohorts.values()
        ])
        print(cohort_df_summary.to_string(index=False))

        return cohorts

    def identify_outliers(self) -> Dict[str, Any]:
        """
        Identify top performers and outlier deals.

        Returns:
            Dictionary with outlier analysis
        """
        print("\n" + "=" * 60)
        print("OUTLIER & TOP PERFORMER IDENTIFICATION")
        print("=" * 60)

        # Calculate IQR for revenue
        Q1 = self.df['revenue'].quantile(0.25)
        Q3 = self.df['revenue'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Identify outliers
        outliers_df = self.df[self.df['revenue'] > upper_bound]

        # Top 10 deals
        top_deals = self.df.nlargest(10, 'revenue')[['id', 'sale_date', 'product', 'revenue', 'closer', 'country', 'upsell']]

        # Top performers by closer
        closer_performance = self.df.groupby('closer').agg({
            'revenue': ['sum', 'mean', 'count']
        }).round(2)
        closer_performance.columns = ['total_revenue', 'avg_revenue', 'deal_count']
        closer_performance = closer_performance.sort_values('total_revenue', ascending=False)

        # Top performers by product
        product_performance = self.df.groupby('product').agg({
            'revenue': ['sum', 'mean', 'count']
        }).round(2)
        product_performance.columns = ['total_revenue', 'avg_revenue', 'deal_count']
        product_performance = product_performance.sort_values('total_revenue', ascending=False)

        outliers = {
            "statistical_bounds": {
                "Q1": float(Q1),
                "Q3": float(Q3),
                "IQR": float(IQR),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
            },
            "outlier_count": len(outliers_df),
            "outlier_deals": outliers_df[['id', 'sale_date', 'product', 'revenue', 'closer']].to_dict('records'),
            "top_10_deals": top_deals.to_dict('records'),
            "closer_rankings": closer_performance.to_dict('index'),
            "product_rankings": product_performance.to_dict('index'),
        }

        print(f"\nRevenue Distribution:")
        print(f"  Q1: ${Q1:,.2f}")
        print(f"  Median: ${self.df['revenue'].median():,.2f}")
        print(f"  Q3: ${Q3:,.2f}")
        print(f"  Upper Bound (outlier threshold): ${upper_bound:,.2f}")
        print(f"\nOutliers Found: {len(outliers_df)}")

        print("\nTop 10 Highest Value Deals:")
        print(top_deals.to_string(index=False))

        print("\nCloser Rankings by Total Revenue:")
        print(closer_performance)

        return outliers

    def generate_insights_summary(self) -> List[Dict[str, str]]:
        """
        Generate a summary of all insights discovered.

        Returns:
            List of insight dictionaries
        """
        print("\n" + "=" * 60)
        print("KEY INSIGHTS SUMMARY")
        print("=" * 60)

        print(f"\nTotal Insights Generated: {len(self.insights)}")
        for i, insight in enumerate(self.insights, 1):
            print(f"\n{i}. [{insight['category']}] {insight['insight']}")
            print(f"   Confidence: {insight['confidence']}")

        return self.insights

    def run_full_analysis(self) -> Dict[str, Any]:
        """
        Run all analysis methods and return comprehensive results.

        Returns:
            Dictionary with all analysis results
        """
        print("\n" + "=" * 80)
        print("BUSINESS COACHING ANALYTICS - COMPREHENSIVE DATA ANALYSIS")
        print("=" * 80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        results = {
            "metadata": {
                "analysis_date": datetime.now().isoformat(),
                "total_records": len(self.df),
                "date_range": {
                    "start": str(self.df['sale_date'].min().date()),
                    "end": str(self.df['sale_date'].max().date()),
                }
            },
            "data_quality": self.data_quality_checks(),
            "summary_statistics": self.summary_statistics(),
            "business_metrics": self.calculate_business_metrics(),
            "revenue_trends": self.analyze_revenue_trends(),
            "product_performance": self.analyze_product_performance(),
            "closer_performance": self.analyze_closer_performance(),
            "geographic_performance": self.analyze_geographic_performance(),
            "correlations": self.calculate_correlations(),
            "cohort_analysis": self.cohort_analysis(),
            "outliers": self.identify_outliers(),
            "insights": self.generate_insights_summary(),
        }

        return results

    def export_results(self, results: Dict[str, Any], filename: str = "analysis_results.json"):
        """
        Export analysis results to JSON file.

        Args:
            results: Dictionary with analysis results
            filename: Output filename
        """
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n✓ Analysis results exported to: {output_path}")


def main():
    """Main execution function."""
    # Initialize analyzer
    analyzer = SalesAnalyzer()

    # Run full analysis
    results = analyzer.run_full_analysis()

    # Export results
    analyzer.export_results(results)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nTotal Insights Generated: {len(results['insights'])}")
    print(f"Results saved to: {REPORTS_DIR / 'analysis_results.json'}")


if __name__ == "__main__":
    main()
