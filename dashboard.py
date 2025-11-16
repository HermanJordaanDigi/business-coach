"""
Business Coaching Analytics - Streamlit Dashboard

Interactive dashboard for visualizing sales data, metrics, and insights.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.db_helpers import (
    get_all_sales,
    get_sales_by_date_range,
    get_table_stats
)

# Page configuration
st.set_page_config(
    page_title="Business Coaching Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_sales_data():
    """Load sales data with caching (5-minute TTL)"""
    return get_all_sales()


@st.cache_data(ttl=300)
def load_table_stats():
    """Load table statistics with caching"""
    return get_table_stats()


def main():
    """Main dashboard function"""

    # Header
    st.markdown('<div class="main-header">📊 Business Coaching Analytics Dashboard</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=Coach+Analytics", use_column_width=True)
        st.markdown("---")

        st.header("🎯 Filters")

        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime(2025, 1, 1),
                key="start_date"
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime(2025, 11, 30),
                key="end_date"
            )

        st.markdown("---")
        st.header("📈 View Options")
        show_raw_data = st.checkbox("Show Raw Data", value=False)
        show_insights = st.checkbox("Show AI Insights", value=True)

    # Load data
    with st.spinner("Loading data..."):
        df = load_sales_data()
        stats = load_table_stats()

    # Filter data by date range
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df_filtered = df[
        (df['sale_date'] >= pd.Timestamp(start_date)) &
        (df['sale_date'] <= pd.Timestamp(end_date))
    ]

    # Key Metrics Row
    st.header("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_revenue = df_filtered['revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{len(df_filtered)} sales"
        )

    with col2:
        avg_deal_size = df_filtered['revenue'].mean()
        st.metric(
            label="📈 Avg Deal Size",
            value=f"${avg_deal_size:,.0f}",
            delta=f"{df_filtered['revenue'].std():,.0f} std dev"
        )

    with col3:
        cash_collected = df_filtered['cash_collected'].sum()
        collection_rate = (cash_collected / total_revenue * 100) if total_revenue > 0 else 0
        st.metric(
            label="💵 Cash Collected",
            value=f"${cash_collected:,.0f}",
            delta=f"{collection_rate:.1f}% rate"
        )

    with col4:
        upsell_rate = (df_filtered['upsell'].sum() / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.metric(
            label="🎯 Upsell Rate",
            value=f"{upsell_rate:.1f}%",
            delta=f"{df_filtered['upsell'].sum()} upsells"
        )

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Revenue Trend Over Time")
        revenue_by_month = df_filtered.groupby(df_filtered['sale_date'].dt.to_period('M'))['revenue'].sum()
        revenue_by_month.index = revenue_by_month.index.to_timestamp()

        fig_revenue = px.line(
            x=revenue_by_month.index,
            y=revenue_by_month.values,
            labels={'x': 'Month', 'y': 'Revenue ($)'},
            title="Monthly Revenue Trend"
        )
        fig_revenue.update_traces(line_color='#1f77b4', line_width=3)
        fig_revenue.update_layout(hovermode='x unified')
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        st.subheader("🎁 Product Performance")
        product_revenue = df_filtered.groupby('product')['revenue'].sum().sort_values(ascending=False)

        fig_products = px.bar(
            x=product_revenue.values,
            y=product_revenue.index,
            orientation='h',
            labels={'x': 'Total Revenue ($)', 'y': 'Product'},
            title="Revenue by Product",
            color=product_revenue.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_products, use_container_width=True)

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 Closer Performance")
        closer_stats = df_filtered.groupby('closer').agg({
            'revenue': ['sum', 'count', 'mean']
        }).round(0)
        closer_stats.columns = ['Total Revenue', 'Sales Count', 'Avg Deal Size']
        closer_stats = closer_stats.sort_values('Total Revenue', ascending=False)

        fig_closers = go.Figure()
        fig_closers.add_trace(go.Bar(
            name='Total Revenue',
            x=closer_stats.index,
            y=closer_stats['Total Revenue'],
            marker_color='#1f77b4'
        ))
        fig_closers.update_layout(
            title="Sales Closer Performance",
            xaxis_title="Closer",
            yaxis_title="Total Revenue ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_closers, use_container_width=True)

    with col2:
        st.subheader("🌍 Geographic Distribution")
        country_revenue = df_filtered.groupby('country')['revenue'].sum().sort_values(ascending=False)

        fig_geo = px.pie(
            values=country_revenue.values,
            names=country_revenue.index,
            title="Revenue Distribution by Country",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_geo.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_geo, use_container_width=True)

    # Deal Size Distribution
    st.subheader("💼 Deal Size Distribution")
    fig_dist = px.histogram(
        df_filtered,
        x='revenue',
        nbins=30,
        labels={'revenue': 'Deal Size ($)', 'count': 'Frequency'},
        title="Distribution of Deal Sizes",
        color_discrete_sequence=['#1f77b4']
    )
    fig_dist.update_layout(showlegend=False)
    st.plotly_chart(fig_dist, use_container_width=True)

    # Insights Section
    if show_insights:
        st.markdown("---")
        st.header("💡 AI-Powered Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"""
            **Top Product**
            {df_filtered.groupby('product')['revenue'].sum().idxmax()}
            Revenue: ${df_filtered.groupby('product')['revenue'].sum().max():,.0f}
            """)

        with col2:
            st.success(f"""
            **Top Closer**
            {df_filtered.groupby('closer')['revenue'].sum().idxmax()}
            Revenue: ${df_filtered.groupby('closer')['revenue'].sum().max():,.0f}
            """)

        with col3:
            best_month = revenue_by_month.idxmax().strftime('%B %Y')
            st.warning(f"""
            **Best Month**
            {best_month}
            Revenue: ${revenue_by_month.max():,.0f}
            """)

    # Raw Data Section
    if show_raw_data:
        st.markdown("---")
        st.header("📋 Raw Sales Data")
        st.dataframe(
            df_filtered[['sale_date', 'product', 'revenue', 'cash_collected', 'closer', 'country', 'upsell']],
            use_container_width=True,
            height=400
        )

        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666;'>"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Total records in database: {stats['total_rows']} | "
        f"Filtered records: {len(df_filtered)}"
        f"</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
