"""
=====================================================
StockVision AI
Portfolio Service
=====================================================
"""

import json
import os
import shutil

# Vercel's filesystem is read-only except /tmp, and /tmp is wiped between
# cold starts, so portfolio data won't persist long-term on Vercel. This is
# fine for a demo; swap in a real database (e.g. Vercel KV / Supabase) if
# you need portfolios to survive restarts.
if os.environ.get("VERCEL"):
    PORTFOLIO_FILE = "/tmp/portfolio.json"
    _SEED_FILE = os.path.join(os.path.dirname(__file__), "..", "dataset", "portfolio.json")
    if not os.path.exists(PORTFOLIO_FILE) and os.path.exists(_SEED_FILE):
        shutil.copy(_SEED_FILE, PORTFOLIO_FILE)
else:
    PORTFOLIO_FILE = "dataset/portfolio.json"


class PortfolioService:

    @staticmethod
    def load():

        if not os.path.exists(PORTFOLIO_FILE):

            with open(PORTFOLIO_FILE, "w") as f:

                json.dump([], f)

        with open(PORTFOLIO_FILE, "r") as f:

            return json.load(f)

    @staticmethod
    def save(data):

        with open(PORTFOLIO_FILE, "w") as f:

            json.dump(data, f, indent=4)

    @staticmethod
    def add(symbol, shares, buy_price):

        portfolio = PortfolioService.load()

        portfolio.append({

            "symbol": symbol.upper(),

            "shares": float(shares),

            "buy_price": float(buy_price)

        })

        PortfolioService.save(portfolio)

        return portfolio

    @staticmethod
    def delete(symbol):

        portfolio = PortfolioService.load()

        portfolio = [

            stock for stock in portfolio

            if stock["symbol"] != symbol.upper()

        ]

        PortfolioService.save(portfolio)

        return portfolio