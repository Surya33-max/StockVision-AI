"""
=====================================================
StockVision AI
Application Configuration
=====================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base Configuration
    """

    # ----------------------------------
    # Flask Configuration
    # ----------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "stockvision-ai-secret-key-change-in-production"
    )

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    TESTING = False

    # ----------------------------------
    # Application Information
    # ----------------------------------

    APP_NAME = "StockVision AI"

    APP_VERSION = "1.0.0"

    COMPANY_NAME = "StockVision"

    # ----------------------------------
    # Stock API Configuration
    # ----------------------------------

    DEFAULT_STOCK = "AAPL"

    DEFAULT_PERIOD = "6mo"

    DEFAULT_INTERVAL = "1d"

    # ----------------------------------
    # Model Configuration
    # ----------------------------------

    MODEL_DIRECTORY = "saved_models"

    DATASET_DIRECTORY = "dataset"

    # ----------------------------------
    # Upload Configuration
    # ----------------------------------

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # ----------------------------------
    # Chart Configuration
    # ----------------------------------

    CHART_HEIGHT = 500

    CHART_THEME = "plotly_dark"

    # ----------------------------------
    # Portfolio Configuration
    # ----------------------------------

    DEFAULT_INITIAL_INVESTMENT = 10000

    RISK_FREE_RATE = 0.05

    # ----------------------------------
    # Cache
    # ----------------------------------

    CACHE_TIMEOUT = 300

    # ----------------------------------
    # Logging
    # ----------------------------------

    LOG_LEVEL = "INFO"