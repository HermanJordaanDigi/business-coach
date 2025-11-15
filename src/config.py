"""
Configuration settings for the Business Coaching Analytics project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
VISUALIZATIONS_DIR = OUTPUTS_DIR / "visualizations"

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "coaching_analytics"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}

# Data generation settings
DATA_SETTINGS = {
    "total_rows": 195,
    "start_date": "2025-01-01",
    "end_date": "2025-11-30",
    "products": {
        "Elite Business Accelerator": 15000,
        "Executive Leadership Mastery": 25000,
        "Scale to 7-Figures Program": 50000,
    },
    "closers": ["Sarah Mitchell", "Marcus Thompson", "Julia Rodriguez"],
    "countries": ["US", "UK", "EU"],
    "country_weights": [0.60, 0.20, 0.20],  # Distribution weights
    "closer_weights": [0.40, 0.35, 0.25],  # Performance distribution
    "cash_collection_rate": (0.85, 0.95),  # Min and max rates
    "upsell_rate": (0.20, 0.30),  # Min and max rates
    # Seasonal distribution (Q1, Q2, Q3, Q4-partial for 11 months)
    "seasonal_weights": [0.15, 0.25, 0.28, 0.32],
}

# API configuration
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "8000")),
    "title": "Coaching Analytics API",
    "description": "REST API for business coaching sales analytics",
    "version": "1.0.0",
}

# Sphinx.ai configuration (to be filled in later)
SPHINX_CONFIG = {
    "api_key": os.getenv("SPHINX_API_KEY", ""),
    "api_url": "https://api.sphinx.ai",  # Update with actual endpoint when available
}

# Visualization settings
VIZ_CONFIG = {
    "figure_size": (12, 6),
    "dpi": 100,
    "style": "seaborn-v0_8-darkgrid",
    "color_palette": "husl",
}
