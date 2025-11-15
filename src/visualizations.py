"""
Visualization module for Business Coaching Analytics project.
Creates professional charts and graphs for data storytelling.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import psycopg2
from pathlib import Path
import warnings
from datetime import datetime

from config import DB_CONFIG, VISUALIZATIONS_DIR

warnings.filterwarnings('ignore')

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Custom color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#F77F00',
    'danger': '#D62828',
    'elite': '#2E86AB',
    'executive': '#A23B72',
    'scale': '#F18F01',
}

PRODUCT_COLORS = {
    'Elite Business Accelerator': COLORS['elite'],
    'Executive Leadership Mastery': COLORS['executive'],
    'Scale to 7-Figures Program': COLORS['scale'],
}


def get_data():
    """Load data from PostgreSQL database."""
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT * FROM sales ORDER BY date"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert date columns and rename for consistency
    df['sale_date'] = pd.to_datetime(df['date'])
    df['sale_id'] = df['id']
    df['year_month'] = df['sale_date'].dt.to_period('M')
    df['month_name'] = df['sale_date'].dt.strftime('%b %Y')

    return df


def ensure_output_dir():
    """Ensure output directory exists."""
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig, filename, tight=True):
    """Save matplotlib figure with consistent settings."""
    filepath = VISUALIZATIONS_DIR / filename
    if tight:
        fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close(fig)


def save_plotly(fig, filename):
    """Save plotly figure as HTML and static image."""
    html_path = VISUALIZATIONS_DIR / f"{filename}.html"
    png_path = VISUALIZATIONS_DIR / f"{filename}.png"

    fig.write_html(html_path)
    fig.write_image(png_path, width=1200, height=700)
    print(f"✓ Saved: {filename}.html and {filename}.png")


def plot_revenue_trend(df):
    """Create revenue trend line chart (monthly)."""
    print("\n📊 Creating revenue trend chart...")

    monthly_revenue = df.groupby('month_name')['revenue'].sum().reset_index()
    monthly_revenue['sort_date'] = pd.to_datetime(df.groupby('month_name')['sale_date'].min().values)
    monthly_revenue = monthly_revenue.sort_values('sort_date')

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(monthly_revenue['month_name'], monthly_revenue['revenue'],
            marker='o', linewidth=2.5, markersize=8, color=COLORS['primary'])
    ax.fill_between(range(len(monthly_revenue)), monthly_revenue['revenue'],
                     alpha=0.3, color=COLORS['primary'])

    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Revenue Trend - 2025', fontsize=16, fontweight='bold', pad=20)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, alpha=0.3)

    save_figure(fig, '01_revenue_trend.png')


def plot_product_performance(df):
    """Create product performance comparison bar chart."""
    print("📊 Creating product performance chart...")

    product_stats = df.groupby('product').agg({
        'revenue': 'sum',
        'sale_id': 'count'
    }).reset_index()
    product_stats.columns = ['product', 'revenue', 'deals']
    product_stats = product_stats.sort_values('revenue', ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Revenue by product
    colors = [PRODUCT_COLORS[p] for p in product_stats['product']]
    ax1.barh(product_stats['product'], product_stats['revenue'], color=colors)
    ax1.set_xlabel('Total Revenue ($)', fontsize=11, fontweight='bold')
    ax1.set_title('Revenue by Product', fontsize=13, fontweight='bold')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Deal count by product
    ax2.barh(product_stats['product'], product_stats['deals'], color=colors)
    ax2.set_xlabel('Number of Deals', fontsize=11, fontweight='bold')
    ax2.set_title('Deal Volume by Product', fontsize=13, fontweight='bold')

    save_figure(fig, '02_product_performance.png')


def plot_closer_leaderboard(df):
    """Create closer leaderboard horizontal bar chart."""
    print("📊 Creating closer leaderboard...")

    closer_stats = df.groupby('closer').agg({
        'revenue': 'sum',
        'sale_id': 'count'
    }).reset_index()
    closer_stats.columns = ['closer', 'revenue', 'deals']
    closer_stats['avg_deal'] = closer_stats['revenue'] / closer_stats['deals']
    closer_stats = closer_stats.sort_values('revenue', ascending=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Total revenue
    axes[0].barh(closer_stats['closer'], closer_stats['revenue'], color=COLORS['primary'])
    axes[0].set_xlabel('Total Revenue ($)', fontsize=10, fontweight='bold')
    axes[0].set_title('Total Revenue by Closer', fontsize=12, fontweight='bold')
    axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Deal count
    axes[1].barh(closer_stats['closer'], closer_stats['deals'], color=COLORS['secondary'])
    axes[1].set_xlabel('Number of Deals', fontsize=10, fontweight='bold')
    axes[1].set_title('Deals Closed', fontsize=12, fontweight='bold')

    # Average deal size
    axes[2].barh(closer_stats['closer'], closer_stats['avg_deal'], color=COLORS['accent'])
    axes[2].set_xlabel('Average Deal Size ($)', fontsize=10, fontweight='bold')
    axes[2].set_title('Average Deal Size', fontsize=12, fontweight='bold')
    axes[2].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    save_figure(fig, '03_closer_leaderboard.png')


def plot_geographic_distribution(df):
    """Create geographic distribution pie/donut chart."""
    print("📊 Creating geographic distribution chart...")

    country_stats = df.groupby('country').agg({
        'revenue': 'sum',
        'sale_id': 'count'
    }).reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Revenue by country (donut chart)
    colors_geo = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    wedges, texts, autotexts = ax1.pie(country_stats['revenue'], labels=country_stats['country'],
                                         autopct='%1.1f%%', startangle=90, colors=colors_geo,
                                         wedgeprops=dict(width=0.5))
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax1.set_title('Revenue Distribution by Country', fontsize=13, fontweight='bold', pad=20)

    # Deal count by country
    wedges, texts, autotexts = ax2.pie(country_stats['sale_id'], labels=country_stats['country'],
                                         autopct='%1.1f%%', startangle=90, colors=colors_geo,
                                         wedgeprops=dict(width=0.5))
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax2.set_title('Deal Volume by Country', fontsize=13, fontweight='bold', pad=20)

    save_figure(fig, '04_geographic_distribution.png')


def plot_cash_collection_funnel(df):
    """Create cash collection funnel visualization."""
    print("📊 Creating cash collection funnel...")

    total_revenue = df['revenue'].sum()
    total_cash = df['cash_collected'].sum()
    collection_rate = (total_cash / total_revenue) * 100

    # By product
    product_funnel = df.groupby('product').agg({
        'revenue': 'sum',
        'cash_collected': 'sum'
    }).reset_index()
    product_funnel['collection_rate'] = (product_funnel['cash_collected'] / product_funnel['revenue']) * 100
    product_funnel = product_funnel.sort_values('revenue', ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Overall funnel
    stages = ['Revenue\nGenerated', 'Cash\nCollected']
    values = [total_revenue, total_cash]
    colors_funnel = [COLORS['primary'], COLORS['success']]

    ax1.bar(stages, values, color=colors_funnel, width=0.6)
    ax1.set_ylabel('Amount ($)', fontsize=11, fontweight='bold')
    ax1.set_title(f'Cash Collection Overview\nCollection Rate: {collection_rate:.1f}%',
                  fontsize=13, fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Add value labels
    for i, v in enumerate(values):
        ax1.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

    # Collection rate by product
    x_pos = range(len(product_funnel))
    colors_prod = [PRODUCT_COLORS[p] for p in product_funnel['product']]
    ax2.bar(x_pos, product_funnel['collection_rate'], color=colors_prod)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(product_funnel['product'], rotation=45, ha='right')
    ax2.set_ylabel('Collection Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Cash Collection Rate by Product', fontsize=13, fontweight='bold')
    ax2.axhline(y=collection_rate, color='red', linestyle='--', label=f'Average: {collection_rate:.1f}%')
    ax2.legend()

    # Add value labels
    for i, v in enumerate(product_funnel['collection_rate']):
        ax2.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

    save_figure(fig, '05_cash_collection_funnel.png')


def plot_upsell_conversion(df):
    """Create upsell conversion rate chart."""
    print("📊 Creating upsell conversion chart...")

    # Overall upsell rate
    total_deals = len(df)
    total_upsells = df['upsell'].sum()
    overall_rate = (total_upsells / total_deals) * 100

    # By product
    product_upsell = df.groupby('product').agg({
        'sale_id': 'count',
        'upsell': 'sum'
    }).reset_index()
    product_upsell['rate'] = (product_upsell['upsell'] / product_upsell['sale_id']) * 100
    product_upsell = product_upsell.sort_values('rate', ascending=False)

    # By closer
    closer_upsell = df.groupby('closer').agg({
        'sale_id': 'count',
        'upsell': 'sum'
    }).reset_index()
    closer_upsell['rate'] = (closer_upsell['upsell'] / closer_upsell['sale_id']) * 100
    closer_upsell = closer_upsell.sort_values('rate', ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # By product
    colors_prod = [PRODUCT_COLORS[p] for p in product_upsell['product']]
    ax1.bar(range(len(product_upsell)), product_upsell['rate'], color=colors_prod)
    ax1.set_xticks(range(len(product_upsell)))
    ax1.set_xticklabels(product_upsell['product'], rotation=45, ha='right')
    ax1.set_ylabel('Upsell Rate (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Upsell Conversion Rate by Product', fontsize=13, fontweight='bold')
    ax1.axhline(y=overall_rate, color='red', linestyle='--', label=f'Average: {overall_rate:.1f}%')
    ax1.legend()

    for i, v in enumerate(product_upsell['rate']):
        ax1.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

    # By closer
    ax2.barh(closer_upsell['closer'], closer_upsell['rate'], color=COLORS['secondary'])
    ax2.set_xlabel('Upsell Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Upsell Conversion Rate by Closer', fontsize=13, fontweight='bold')
    ax2.axvline(x=overall_rate, color='red', linestyle='--', label=f'Average: {overall_rate:.1f}%')
    ax2.legend()

    save_figure(fig, '06_upsell_conversion.png')


def plot_revenue_heatmap(df):
    """Create heatmap for revenue by month and product."""
    print("📊 Creating revenue heatmap...")

    # Prepare pivot table
    heatmap_data = df.pivot_table(
        values='revenue',
        index='product',
        columns='month_name',
        aggfunc='sum',
        fill_value=0
    )

    # Sort columns by date
    month_order = df.groupby('month_name')['sale_date'].min().sort_values().index
    heatmap_data = heatmap_data[month_order]

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.heatmap(heatmap_data / 1000, annot=True, fmt='.0f', cmap='YlOrRd',
                cbar_kws={'label': 'Revenue ($K)'}, ax=ax, linewidths=0.5)
    ax.set_title('Revenue Heatmap by Product and Month ($K)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=11, fontweight='bold')
    ax.set_ylabel('Product', fontsize=11, fontweight='bold')
    plt.xticks(rotation=45, ha='right')

    save_figure(fig, '07_revenue_heatmap.png')


def plot_deal_size_distribution(df):
    """Create box plot for deal size distribution by product."""
    print("📊 Creating deal size distribution chart...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Box plot
    product_order = df.groupby('product')['revenue'].median().sort_values(ascending=False).index
    colors_prod = [PRODUCT_COLORS[p] for p in product_order]

    bp = ax1.boxplot([df[df['product'] == p]['revenue'] for p in product_order],
                      labels=product_order, patch_artist=True, widths=0.6)

    for patch, color in zip(bp['boxes'], colors_prod):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax1.set_ylabel('Deal Size ($)', fontsize=11, fontweight='bold')
    ax1.set_title('Deal Size Distribution by Product', fontsize=13, fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)

    # Violin plot
    product_plot_data = []
    for product in product_order:
        product_data = df[df['product'] == product]['revenue'].values
        product_plot_data.append(product_data)

    parts = ax2.violinplot(product_plot_data, positions=range(len(product_order)),
                           showmeans=True, showmedians=True)

    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors_prod[i])
        pc.set_alpha(0.7)

    ax2.set_xticks(range(len(product_order)))
    ax2.set_xticklabels(product_order, rotation=45, ha='right')
    ax2.set_ylabel('Deal Size ($)', fontsize=11, fontweight='bold')
    ax2.set_title('Deal Size Distribution (Violin Plot)', fontsize=13, fontweight='bold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax2.grid(True, alpha=0.3)

    save_figure(fig, '08_deal_size_distribution.png')


def plot_revenue_vs_cash(df):
    """Create scatter plot for revenue vs cash collected."""
    print("📊 Creating revenue vs cash collected scatter plot...")

    fig, ax = plt.subplots(figsize=(12, 8))

    products = df['product'].unique()
    for product in products:
        product_data = df[df['product'] == product]
        ax.scatter(product_data['revenue'], product_data['cash_collected'],
                  label=product, alpha=0.6, s=100, color=PRODUCT_COLORS[product])

    # Add perfect collection line
    max_val = max(df['revenue'].max(), df['cash_collected'].max())
    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='100% Collection')

    ax.set_xlabel('Revenue ($)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cash Collected ($)', fontsize=12, fontweight='bold')
    ax.set_title('Revenue vs Cash Collected by Product', fontsize=14, fontweight='bold', pad=20)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)

    save_figure(fig, '09_revenue_vs_cash.png')


def create_interactive_dashboard(df):
    """Create interactive plotly dashboard for key metrics."""
    print("📊 Creating interactive Plotly dashboard...")

    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Monthly Revenue Trend', 'Revenue by Product',
                       'Closer Performance', 'Geographic Distribution',
                       'Collection Rate by Product', 'Upsell Rate by Closer'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.12
    )

    # 1. Monthly Revenue Trend
    monthly_revenue = df.groupby('month_name')['revenue'].sum().reset_index()
    monthly_revenue['sort_date'] = pd.to_datetime(df.groupby('month_name')['sale_date'].min().values)
    monthly_revenue = monthly_revenue.sort_values('sort_date')

    fig.add_trace(
        go.Scatter(x=monthly_revenue['month_name'], y=monthly_revenue['revenue'],
                  mode='lines+markers', name='Revenue', line=dict(color=COLORS['primary'], width=3)),
        row=1, col=1
    )

    # 2. Revenue by Product
    product_revenue = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=product_revenue.index, y=product_revenue.values, name='Product Revenue',
              marker_color=[PRODUCT_COLORS[p] for p in product_revenue.index]),
        row=1, col=2
    )

    # 3. Closer Performance
    closer_revenue = df.groupby('closer')['revenue'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(y=closer_revenue.index, x=closer_revenue.values, name='Closer Revenue',
              orientation='h', marker_color=COLORS['secondary']),
        row=2, col=1
    )

    # 4. Geographic Distribution
    country_revenue = df.groupby('country')['revenue'].sum()
    fig.add_trace(
        go.Pie(labels=country_revenue.index, values=country_revenue.values, name='Geography',
              marker=dict(colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent']])),
        row=2, col=2
    )

    # 5. Collection Rate by Product
    product_collection = df.groupby('product').agg({
        'revenue': 'sum',
        'cash_collected': 'sum'
    })
    product_collection['rate'] = (product_collection['cash_collected'] / product_collection['revenue']) * 100
    product_collection = product_collection.sort_values('rate', ascending=False)

    fig.add_trace(
        go.Bar(x=product_collection.index, y=product_collection['rate'], name='Collection Rate',
              marker_color=[PRODUCT_COLORS[p] for p in product_collection.index]),
        row=3, col=1
    )

    # 6. Upsell Rate by Closer
    closer_upsell = df.groupby('closer').agg({
        'sale_id': 'count',
        'upsell': 'sum'
    })
    closer_upsell['rate'] = (closer_upsell['upsell'] / closer_upsell['sale_id']) * 100
    closer_upsell = closer_upsell.sort_values('rate', ascending=False)

    fig.add_trace(
        go.Bar(x=closer_upsell.index, y=closer_upsell['rate'], name='Upsell Rate',
              marker_color=COLORS['accent']),
        row=3, col=2
    )

    # Update layout
    fig.update_layout(
        title_text="Business Coaching Analytics Dashboard - 2025",
        title_font_size=20,
        showlegend=False,
        height=1200,
        width=1400
    )

    # Update axes labels
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_xaxes(title_text="Revenue ($)", row=2, col=1)
    fig.update_xaxes(title_text="Product", row=3, col=1)
    fig.update_yaxes(title_text="Collection Rate (%)", row=3, col=1)
    fig.update_xaxes(title_text="Closer", row=3, col=2)
    fig.update_yaxes(title_text="Upsell Rate (%)", row=3, col=2)

    save_plotly(fig, '10_interactive_dashboard')


def create_all_visualizations():
    """Generate all visualizations."""
    print("=" * 70)
    print("🎨 BUSINESS COACHING ANALYTICS - VISUALIZATION GENERATOR")
    print("=" * 70)

    # Ensure output directory exists
    ensure_output_dir()

    # Load data
    print("\n📥 Loading data from database...")
    df = get_data()
    print(f"✓ Loaded {len(df)} records")

    # Generate all visualizations
    plot_revenue_trend(df)
    plot_product_performance(df)
    plot_closer_leaderboard(df)
    plot_geographic_distribution(df)
    plot_cash_collection_funnel(df)
    plot_upsell_conversion(df)
    plot_revenue_heatmap(df)
    plot_deal_size_distribution(df)
    plot_revenue_vs_cash(df)
    create_interactive_dashboard(df)

    print("\n" + "=" * 70)
    print(f"✅ All visualizations saved to: {VISUALIZATIONS_DIR}")
    print("=" * 70)

    # Print summary
    print("\n📊 Generated Visualizations:")
    print("  1. Monthly Revenue Trend (line chart)")
    print("  2. Product Performance Comparison (bar charts)")
    print("  3. Closer Leaderboard (horizontal bars)")
    print("  4. Geographic Distribution (donut charts)")
    print("  5. Cash Collection Funnel")
    print("  6. Upsell Conversion Rates")
    print("  7. Revenue Heatmap (product × month)")
    print("  8. Deal Size Distribution (box & violin plots)")
    print("  9. Revenue vs Cash Collected (scatter plot)")
    print(" 10. Interactive Dashboard (Plotly)")


if __name__ == "__main__":
    create_all_visualizations()
