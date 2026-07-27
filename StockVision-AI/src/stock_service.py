"""
=====================================================
StockVision AI
Stock Data Service
=====================================================

Author: Surya
Version: 1.0.0

Description:
------------
Handles all interactions with Yahoo Finance.
"""
from datetime import datetime
import yfinance as yf
import pandas as pd

# ------------------------------------------------------------------
# Curated catalog of popular stocks (US + India).
#
# Indian symbols need Yahoo Finance's exchange suffix to resolve:
#   ".NS" = NSE (National Stock Exchange), ".BO" = BSE (Bombay Stock Exchange)
# e.g. "RELIANCE.NS", "TCS.NS", "INFY.NS"
#
# NOTE: this list only powers the *search suggestions* and the
# ticker/heatmap widgets. It is not a restriction -- any valid Yahoo
# Finance ticker symbol (typed directly into the Symbol field on the
# Dashboard, Search, or Prediction pages) works, whether or not it's
# in this list.
# ------------------------------------------------------------------
POPULAR_STOCKS = {

    # ---- US ----
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms Inc.",
    "NVDA": "NVIDIA Corporation",
    "TSLA": "Tesla Inc.",
    "NFLX": "Netflix Inc.",
    "AMD": "Advanced Micro Devices",
    "INTC": "Intel Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.",
    "WMT": "Walmart Inc.",
    "DIS": "The Walt Disney Company",
    "BA": "Boeing Company",
    "KO": "The Coca-Cola Company",
    "PEP": "PepsiCo Inc.",
    "MCD": "McDonald's Corporation",
    "NKE": "Nike Inc.",
    "IBM": "IBM Corporation",
    "ORCL": "Oracle Corporation",
    "PYPL": "PayPal Holdings",
    "ADBE": "Adobe Inc.",
    "CRM": "Salesforce Inc.",
    "UBER": "Uber Technologies",
    "SBUX": "Starbucks Corporation",

    # ---- India (NSE) ----
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys Ltd.",
    "HDFCBANK.NS": "HDFC Bank Ltd.",
    "ICICIBANK.NS": "ICICI Bank Ltd.",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel Ltd.",
    "ITC.NS": "ITC Ltd.",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "AXISBANK.NS": "Axis Bank Ltd.",
    "BAJFINANCE.NS": "Bajaj Finance Ltd.",
    "MARUTI.NS": "Maruti Suzuki India",
    "ASIANPAINT.NS": "Asian Paints Ltd.",
    "WIPRO.NS": "Wipro Ltd.",
    "TATAMOTORS.NS": "Tata Motors Ltd.",
    "SUNPHARMA.NS": "Sun Pharmaceutical",
    "TITAN.NS": "Titan Company Ltd.",
    "ADANIENT.NS": "Adani Enterprises",
    "ZOMATO.NS": "Zomato Ltd.",
    "PAYTM.NS": "One97 Communications (Paytm)",

}


class StockService:
    """
    Stock Service Class
    """

    @staticmethod
    def get_stock_info(symbol: str):
        """
        Returns general company information.
        """

        try:

            stock = yf.Ticker(symbol.upper())

            info = stock.info

            return {

                "symbol": symbol.upper(),

                "company_name": info.get("longName", "N/A"),

                "sector": info.get("sector", "N/A"),

                "industry": info.get("industry", "N/A"),

                "website": info.get("website", "N/A"),

                "country": info.get("country", "N/A"),

                "market_cap": info.get("marketCap", 0),

                "employees": info.get("fullTimeEmployees", "N/A")

            }

        except Exception as e:

            print(e)

            return None

    # -------------------------------------------------

    @staticmethod
    def get_live_price(symbol: str):
        """
        Returns latest market data.
        """

        try:

            stock = yf.Ticker(symbol.upper())

            info = stock.info

            return {

                "symbol": symbol.upper(),

                "current_price": info.get("currentPrice"),

                "previous_close": info.get("previousClose"),

                "open": info.get("open"),

                "high": info.get("dayHigh"),

                "low": info.get("dayLow"),

                "volume": info.get("volume"),

                "currency": info.get("currency")

            }

        except Exception as e:

            print(e)

            return None

    # -------------------------------------------------

    @staticmethod
    def get_historical_data(
            symbol,
            period="6mo",
            interval="1d"
    ):
        """
        Returns historical stock prices.
        """

        try:

            stock = yf.Ticker(symbol.upper())

            history = stock.history(
                period=period,
                interval=interval
            )

            history.reset_index(inplace=True)

            return history

        except Exception as e:

            print(e)

            return pd.DataFrame()

    # -------------------------------------------------

    @staticmethod
    def calculate_returns(dataframe):
        """
        Daily Returns
        """

        dataframe["Daily Return"] = dataframe["Close"].pct_change()

        return dataframe

    # -------------------------------------------------

    @staticmethod
    def moving_average(dataframe, window=20):
        """
        Moving Average
        """

        dataframe[f"MA_{window}"] = (
            dataframe["Close"]
            .rolling(window=window)
            .mean()
        )

        return dataframe

    # -------------------------------------------------

    @staticmethod
    def exponential_moving_average(dataframe, window=20):
        """
        EMA
        """

        dataframe[f"EMA_{window}"] = (
            dataframe["Close"]
            .ewm(span=window)
            .mean()
        )

        return dataframe

    # -------------------------------------------------

    @staticmethod
    def volatility(dataframe):
        """
        Volatility
        """

        dataframe["Volatility"] = (
            dataframe["Close"]
            .pct_change()
            .rolling(20)
            .std()
        )

        return dataframe

    # -------------------------------------------------

    @staticmethod
    def highest_price(dataframe):

        return dataframe["High"].max()

    # -------------------------------------------------

    @staticmethod
    def lowest_price(dataframe):

        return dataframe["Low"].min()

    # -------------------------------------------------

    @staticmethod
    def average_volume(dataframe):

        return dataframe["Volume"].mean()

    # -------------------------------------------------

    @staticmethod
    def latest_close(dataframe):

        return dataframe.iloc[-1]["Close"]

    # -------------------------------------------------

    @staticmethod
    def latest_date(dataframe):

        return dataframe.iloc[-1]["Date"]

    # -------------------------------------------------

    @staticmethod
    def get_quote(symbol):
        """
        Returns dashboard quote data.
        """

        ticker = yf.Ticker(symbol.upper())

        info = ticker.info

        return {

            "current_price": info.get("currentPrice"),

            "day_high": info.get("dayHigh"),

            "day_low": info.get("dayLow"),

            "volume": info.get("volume"),

            "currency": info.get("currency", "USD"),

            "updated_at": datetime.now().strftime("%I:%M %p")

        }

    # -------------------------------------------------

    @staticmethod
    def get_history(symbol, period="3mo"):
        """
        Returns formatted historical data for charts.
        """

        ticker = yf.Ticker(symbol.upper())

        df = ticker.history(period=period)

        history = []

        for index, row in df.iterrows():

            history.append({

                "date": index.strftime("%Y-%m-%d"),

                "open": round(float(row["Open"]), 2),

                "high": round(float(row["High"]), 2),

                "low": round(float(row["Low"]), 2),

                "close": round(float(row["Close"]), 2),

                "volume": int(row["Volume"])

            })

        return history

    # -------------------------------------------------

    @staticmethod
    def search_stock(query):
        """
        Search the curated catalog by symbol or company name.
        Matching is substring-based, so "bank" surfaces every bank in
        the catalog and "reliance" finds RELIANCE.NS, etc.
        """

        query = query.upper().strip()

        matches = []

        for symbol, company in POPULAR_STOCKS.items():

            if query in symbol or query in company.upper():

                matches.append({

                    "symbol": symbol,

                    "company": company

                })

        return matches[:15]

    # -------------------------------------------------

    @staticmethod
    def market_heatmap():

        stocks = [
            # US
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "NFLX",
            # India
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
            "ICICIBANK.NS", "SBIN.NS", "TATAMOTORS.NS", "ITC.NS",
        ]

        heatmap = []

        for symbol in stocks:

            try:

                info = yf.Ticker(symbol).info

                price = info.get("currentPrice")

                previous = info.get("previousClose")

                company = info.get("shortName", symbol)

                if price and previous:

                    change = round(

                        ((price - previous) / previous) * 100,

                        2

                    )

                else:

                    change = 0

                heatmap.append({

                    "symbol": symbol,

                    "company": company,

                    "price": price,

                    "change": change

                })

            except Exception:

                continue

        return heatmap