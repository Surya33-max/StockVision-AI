"""
=====================================================
StockVision AI
News Service
=====================================================
"""

import feedparser


class NewsService:

    RSS_URL = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US"

    @staticmethod
    def latest(limit=10):

        feed = feedparser.parse(NewsService.RSS_URL)

        news = []

        for item in feed.entries[:limit]:

            news.append({

                "title": item.get("title"),

                "link": item.get("link"),

                "published": item.get("published")

            })

        return news