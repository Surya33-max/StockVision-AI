"""
StockVision AI
Main Flask Application
Author: Surya
"""
from flask import Flask
from config import Config
from src.routes import register_routes


def create_app():
    """
    Application Factory
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Register all routes
    register_routes(app)

    return app


# Create Flask App
app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
