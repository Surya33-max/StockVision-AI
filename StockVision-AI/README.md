# StockVision AI

Flask backend (yfinance data + a simple trend-based prediction) with a
server-rendered frontend (Jinja templates + vanilla JS), structured to
deploy on Vercel as-is.

## What changed from the original

- Fixed `src/stock_service.py`: four methods (`get_quote`, `get_history`,
  `search_stock`, `market_heatmap`) had accidentally landed outside the
  `StockService` class, so every API route that used them was crashing.
- Fixed `src/routes.py`: removed a circular `import app` and consolidated
  every route into `register_routes()` so it actually runs.
- **Prediction page didn't work at all**: `prediction.html`'s form was
  never wired to any JavaScript, so clicking "Generate Prediction" just
  reloaded the page. Rewrote `loadPrediction()`, hooked it to the form
  submit, and had the backend return a real forecast series (not just
  one number) so the chart has something to plot. Also fixed a
  duplicate `id="confidence"` that appeared twice on that page — one
  of Flask's more silent bugs, since browsers just use the first match
  and ignore the rest.
- **Search page didn't work at all**: the form and "quick stock" buttons
  filled the text box but never fetched anything, and the JS was
  already trying to write into a `#search-results` div that didn't
  exist in the HTML. Wired up `runStockSearch()`, added the missing
  container, and exposed `/api/company/<symbol>` (the backend method
  for it already existed, it just had no route).
- **Dashboard chart silently failed**: `renderDashboardChart()` was
  hardcoded to target a div id (`dashboard-chart`) that doesn't exist
  on the page — the real one is `price-chart`. Also added a symbol
  switcher input, since the dashboard was previously hardcoded to
  always show AAPL with no way to change it.
- **Stock coverage was tiny (5-10 US symbols)**: expanded the catalog
  used by search suggestions, the market ticker, and the heatmap to
  ~45 stocks across US and Indian (NSE) markets. This only affects
  autocomplete/suggestions — you can already type **any** valid Yahoo
  Finance ticker directly into the Symbol field on Dashboard, Search,
  or Prediction. For Indian stocks, Yahoo needs the exchange suffix:
  `.NS` for NSE, `.BO` for BSE — e.g. `RELIANCE.NS`, `TCS.NS`,
  `INFY.NS`, not just `RELIANCE`.
- Fixed `templates/base.html`: it referenced `css/dashboard.css`,
  `css/responsive.css`, and `js/charts.js`, none of which exist
  (typo — the real file is `chart.js`). Removed the dead links.
- Trimmed `requirements.txt`: scikit-learn, `ta`, plotly, openpyxl, and
  python-dateutil were listed but never imported anywhere in the code —
  removed. Also dropped gunicorn/pytest, which aren't needed for a
  Vercel deployment. Install size went from ~250MB+ to a few MB.
- Vercel's current Python runtime auto-detects a Flask `app` instance
  directly in `app.py` at the project root — no `api/index.py` wrapper
  or legacy `builds`/`routes` config needed. `vercel.json` now just sets
  a longer function timeout, since a few routes (ticker, heatmap) loop
  over several yfinance calls.
- Vercel does **not** serve files through Flask's `static_folder` —
  it wants static assets in a top-level `public/**` folder, served
  straight from its CDN. `static/` is kept for local development
  (Flask serves it directly), and the same files are duplicated into
  `public/static/` so the exact same `/static/...` URLs work on Vercel
  too, without touching any template code.
- `PortfolioService` now writes to `/tmp` when running on Vercel, since
  Vercel's filesystem is read-only outside `/tmp` (see note below).

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
