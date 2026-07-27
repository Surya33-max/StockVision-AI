# StockVision AI

Flask backend (yfinance data + a simple trend-based prediction) with a
server-rendered frontend (Jinja templates + vanilla JS), structured to
deploy on Vercel as-is.


## Run locally

```bash
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Visit http://127.0.0.1:5000

## Deploy to Vercel

1. Push this folder to a GitHub repo.
2. Go to vercel.com → **Add New Project** → import the repo.
3. Leave the framework preset as-is (or "Other") — Vercel detects
   `app.py` automatically as the Python entrypoint. No extra build
   settings needed. Click **Deploy**.
4. (Optional) In Project → Settings → Environment Variables, set
   `SECRET_KEY` to something random for production.

If you change any file under `static/`, copy it into `public/static/`
too (same relative path) so the Vercel-hosted version stays in sync.

## One real limitation to know about

`/api/portfolio/add` and `/api/portfolio/delete` write to a JSON file.
On Vercel, only `/tmp` is writable, and `/tmp` is wiped whenever the
serverless function cold-starts — so portfolio changes are **not**
permanently saved on Vercel (they will be locally, since `dataset/` is
writable on your machine). If you want portfolios to persist for real
users, swap `PortfolioService` for a small database — Vercel KV,
Supabase, or even a free-tier Postgres — happy to help wire that up
when you're ready.

## Project structure

```
app.py               Flask app factory (Vercel entrypoint too)
vercel.json           Vercel function config (timeout)
config.py            App configuration
src/routes.py        All page + API routes
src/stock_service.py Yahoo Finance data + indicators
src/prediction_service.py  Simple trend-based BUY/SELL/HOLD signal
src/portfolio_service.py   JSON-file-backed portfolio storage
src/news_service.py  RSS market news feed
templates/           Jinja HTML pages
static/              CSS/JS (served by Flask locally)
public/static/       Same CSS/JS, served by Vercel's CDN
```
