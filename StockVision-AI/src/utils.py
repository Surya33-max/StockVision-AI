"""
=====================================================
StockVision AI
Utility Functions
=====================================================

Author : Surya
Version: 1.0.0

Description
-----------
Common helper functions used throughout
the application.
"""

from datetime import datetime
import pandas as pd


class Utils:

    # ==========================================
    # Currency Formatter
    # ==========================================

    @staticmethod
    def currency(value):

        if value is None:
            return "N/A"

        return f"${value:,.2f}"

    # ==========================================
    # Integer Formatter
    # ==========================================

    @staticmethod
    def number(value):

        if value is None:
            return "N/A"

        return f"{value:,}"

    # ==========================================
    # Percentage Formatter
    # ==========================================

    @staticmethod
    def percentage(value):

        if value is None:
            return "N/A"

        return f"{value:.2f}%"

    # ==========================================
    # Billion Formatter
    # ==========================================

    @staticmethod
    def billions(value):

        if value is None:
            return "N/A"

        return f"${value/1_000_000_000:.2f}B"

    # ==========================================
    # Million Formatter
    # ==========================================

    @staticmethod
    def millions(value):

        if value is None:
            return "N/A"

        return f"${value/1_000_000:.2f}M"

    # ==========================================
    # Date Formatter
    # ==========================================

    @staticmethod
    def date(date):

        if pd.isna(date):
            return "N/A"

        return date.strftime("%d %b %Y")

    # ==========================================
    # Datetime Formatter
    # ==========================================

    @staticmethod
    def datetime():

        return datetime.now().strftime(
            "%d %b %Y %I:%M %p"
        )

    # ==========================================
    # Price Change
    # ==========================================

    @staticmethod
    def change(current, previous):

        if current is None or previous is None:

            return 0

        return current - previous

    # ==========================================
    # Percentage Change
    # ==========================================

    @staticmethod
    def change_percent(current, previous):

        if current is None or previous is None:

            return 0

        if previous == 0:

            return 0

        return ((current - previous) / previous) * 100

    # ==========================================
    # Risk Category
    # ==========================================

    @staticmethod
    def risk(volatility):

        if volatility < 0.01:

            return "Low"

        elif volatility < 0.03:

            return "Medium"

        else:

            return "High"

    # ==========================================
    # Convert DataFrame to Dictionary
    # ==========================================

    @staticmethod
    def dataframe_to_dict(df):

        return df.to_dict(
            orient="records"
        )

    # ==========================================
    # Latest Close
    # ==========================================

    @staticmethod
    def latest_close(df):

        if len(df) == 0:

            return None

        return float(df["Close"].iloc[-1])

    # ==========================================
    # Latest Volume
    # ==========================================

    @staticmethod
    def latest_volume(df):

        if len(df) == 0:

            return None

        return int(df["Volume"].iloc[-1])

    # ==========================================
    # Data Validation
    # ==========================================

    @staticmethod
    def validate_symbol(symbol):

        if symbol is None:

            return False

        symbol = symbol.strip()

        if len(symbol) == 0:

            return False

        return True

    # ==========================================
    # Success Response
    # ==========================================

    @staticmethod
    def success(message):

        return {

            "status": "success",

            "message": message

        }

    # ==========================================
    # Error Response
    # ==========================================

    @staticmethod
    def error(message):

        return {

            "status": "error",

            "message": message

        }