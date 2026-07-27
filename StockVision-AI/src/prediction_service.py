"""
=====================================================
StockVision AI
Prediction Service
=====================================================
"""

from datetime import datetime, timedelta

import numpy as np


class PredictionService:

    @staticmethod
    def analyze(history, days=7):

        """
        Basic AI recommendation engine.
        Uses trend analysis (price vs its 20-period moving average) to
        produce a BUY/SELL/HOLD signal and a simple linear price
        projection for the chart. This is a heuristic, not a trained
        ML model -- good enough for a demo, not for real trading
        decisions.
        """

        if len(history) < 20:

            return {

                "signal": "HOLD",

                "confidence": 50,

                "trend": "Unknown",

                "risk": "High",

                "current_price": history[-1]["close"] if history else None,

                "prediction": None,

                "series": []

            }

        closes = np.array([x["close"] for x in history])

        sma20 = np.mean(closes[-20:])

        latest = closes[-1]

        difference = ((latest - sma20) / sma20) * 100

        if difference > 3:

            signal = "BUY"
            trend = "Bullish"
            confidence = min(95, 70 + abs(difference))

        elif difference < -3:

            signal = "SELL"
            trend = "Bearish"
            confidence = min(95, 70 + abs(difference))

        else:

            signal = "HOLD"
            trend = "Sideways"
            confidence = 65

        volatility = np.std(closes[-20:])

        if volatility > 10:

            risk = "High"

        elif volatility > 5:

            risk = "Medium"

        else:

            risk = "Low"

        predicted_price = round(

            latest * (1 + difference / 100),

            2

        )

        # Simple linear projection from the latest close to the
        # predicted price, spread across `days` calendar days, so the
        # frontend has something real to plot on the prediction chart.
        try:
            last_date = datetime.strptime(history[-1]["date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            last_date = datetime.now()

        series = []
        for i in range(1, days + 1):
            step_price = round(
                latest + (predicted_price - latest) * (i / days),
                2
            )
            series.append({
                "date": (last_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "price": step_price
            })

        return {

            "signal": signal,

            "confidence": round(confidence),

            "trend": trend,

            "risk": risk,

            "current_price": round(float(latest), 2),

            "prediction": predicted_price,

            "series": series

        }