"""
=====================================================
StockVision AI
Application Routes
=====================================================

Author: Surya
Version: 1.0.0
"""
from flask import jsonify, request, render_template

from config import Config
from src.stock_service import StockService
from src.news_service import NewsService
from src.portfolio_service import PortfolioService
from src.prediction_service import PredictionService

stock_service = StockService()


def register_routes(app):
    """
    Register all application routes (pages + API) on the given Flask app.
    """

    # ============================================
    # Pages
    # ============================================

    @app.route("/")
    def home():
        return render_template("index.html", app_name=Config.APP_NAME)

    @app.route("/dashboard")
    def dashboard():
        return render_template(
            "dashboard.html",
            app_name=Config.APP_NAME,
            page_title="Dashboard"
        )

    @app.route("/search")
    def search():
        return render_template(
            "search.html",
            app_name=Config.APP_NAME,
            page_title="Search Stocks"
        )

    @app.route("/prediction")
    def prediction():
        return render_template(
            "prediction.html",
            app_name=Config.APP_NAME,
            page_title="Prediction"
        )

    @app.route("/analytics")
    def analytics():
        return render_template(
            "analytics.html",
            app_name=Config.APP_NAME,
            page_title="Analytics"
        )

    @app.route("/portfolio")
    def portfolio():
        return render_template(
            "portfolio.html",
            app_name=Config.APP_NAME,
            page_title="Portfolio Optimizer"
        )

    @app.route("/about")
    def about():
        return render_template(
            "about.html",
            app_name=Config.APP_NAME,
            page_title="About"
        )

    @app.route("/contact")
    def contact():
        return render_template(
            "contact.html",
            app_name=Config.APP_NAME,
            page_title="Contact"
        )

    @app.errorhandler(404)
    def page_not_found(error):
        return (
            render_template("404.html", app_name=Config.APP_NAME, page_title="404"),
            404,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            render_template("500.html", app_name=Config.APP_NAME, page_title="500"),
            500,
        )

    # ============================================
    # API - Dashboard
    # ============================================

    @app.route("/api/dashboard/<symbol>")
    def api_dashboard(symbol):
        try:
            symbol = symbol.upper()
            quote = stock_service.get_quote(symbol)
            history = stock_service.get_history(symbol)

            return jsonify({
                "symbol": symbol,
                "current_price": quote.get("current_price"),
                "day_high": quote.get("day_high"),
                "day_low": quote.get("day_low"),
                "volume": quote.get("volume"),
                "currency": quote.get("currency"),
                "updated_at": quote.get("updated_at"),
                "history": history
            })
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # ============================================
    # API - Search Stocks
    # ============================================

    @app.route("/api/search")
    def api_search():
        query = request.args.get("q", "").strip()

        if len(query) < 1:
            return jsonify([])

        return jsonify(stock_service.search_stock(query))

    # ============================================
    # API - Company Info
    # ============================================

    @app.route("/api/company/<symbol>")
    def api_company(symbol):
        info = stock_service.get_stock_info(symbol.upper())

        if info is None:
            return jsonify({"success": False, "message": "Symbol not found"}), 404

        return jsonify(info)

    # ============================================
    # API - Market Ticker
    # ============================================

    @app.route("/api/ticker")
    def api_ticker():
        symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
        ]

        ticker = []
        for symbol in symbols:
            try:
                quote = stock_service.get_quote(symbol)
                ticker.append({
                    "symbol": symbol,
                    "price": quote.get("current_price")
                })
            except Exception:
                continue

        return jsonify(ticker)

    # ============================================
    # API - AI Prediction
    # ============================================

    @app.route("/api/predict/<symbol>")
    def api_predict(symbol):
        try:
            days = int(request.args.get("days", 7))
            history = stock_service.get_history(symbol)
            return jsonify(PredictionService.analyze(history, days=days))
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # ============================================
    # API - Portfolio
    # ============================================

    @app.route("/api/portfolio")
    def get_portfolio():
        return jsonify(PortfolioService.load())

    @app.route("/api/portfolio/add", methods=["POST"])
    def add_portfolio():
        data = request.json
        PortfolioService.add(data["symbol"], data["shares"], data["buy_price"])
        return jsonify({"success": True})

    @app.route("/api/portfolio/delete/<symbol>", methods=["DELETE"])
    def delete_portfolio(symbol):
        PortfolioService.delete(symbol)
        return jsonify({"success": True})

    # ============================================
    # API - Market News
    # ============================================

    @app.route("/api/news")
    def api_news():
        return jsonify(NewsService.latest())

    # ============================================
    # API - Heatmap
    # ============================================

    @app.route("/api/heatmap")
    def api_heatmap():
        return jsonify(stock_service.market_heatmap())
