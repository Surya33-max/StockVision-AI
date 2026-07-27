/*
====================================================
                StockVision AI
                main.js
====================================================
*/

// ================================================
// Application Namespace
// ================================================

const StockVision = {

    appName: "StockVision AI",

    version: "1.0.0"

};

// ================================================
// DOM Ready
// ================================================

document.addEventListener("DOMContentLoaded", () => {

    initializeApplication();

});

// ================================================
// Initialize Application
// ================================================

function initializeApplication() {

    highlightActiveNavbar();

    initializeTooltips();

    initializeForms();

    initializeQuickButtons();

    console.log(

        `${StockVision.appName} v${StockVision.version} Loaded`

    );

}

// ================================================
// Active Navbar
// ================================================

function highlightActiveNavbar() {

    const currentPath = window.location.pathname;

    document.querySelectorAll(".nav-link").forEach(link => {

        if (link.getAttribute("href") === currentPath) {

            link.classList.add("active");

        }

    });

}

// ================================================
// Bootstrap Tooltips
// ================================================

function initializeTooltips() {

    const tooltipTriggerList = document.querySelectorAll(

        '[data-bs-toggle="tooltip"]'

    );

    tooltipTriggerList.forEach(element => {

        new bootstrap.Tooltip(element);

    });

}

// ================================================
// Form Validation
// ================================================

function initializeForms() {

    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", function(event){

            if(!form.checkValidity()){

                event.preventDefault();

                event.stopPropagation();

                showToast(

                    "Please complete all required fields.",

                    "warning"

                );

            }

            form.classList.add("was-validated");

        });

    });

}

// ================================================
// Loading Spinner
// ================================================

function showLoading(){

    let loader = document.getElementById("loading-overlay");

    if(loader){

        loader.classList.remove("d-none");

    }

}

function hideLoading(){

    let loader = document.getElementById("loading-overlay");

    if(loader){

        loader.classList.add("d-none");

    }

}

// ================================================
// Toast Notification
// ================================================

function showToast(message,type="success"){

    const toast = document.createElement("div");

    toast.className = `toast-message ${type}`;

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.classList.add("show");

    },100);

    setTimeout(()=>{

        toast.classList.remove("show");

        setTimeout(()=>{

            toast.remove();

        },300);

    },3000);

}

// ================================================
// Number Formatter
// ================================================

function formatNumber(value){

    return new Intl.NumberFormat().format(value);

}

// ================================================
// Percentage Formatter
// ================================================

function formatPercentage(value){

    return `${Number(value).toFixed(2)}%`;

}

// ================================================
// Date Formatter
// ================================================

function formatDate(date){

    return new Date(date).toLocaleDateString();

}

// ================================================
// Fetch Wrapper
// ================================================

async function apiFetch(url,options={}){

    try{

        showLoading();

        const response = await fetch(url,options);

        if(!response.ok){

            throw new Error(

                `HTTP ${response.status}`

            );

        }

        return await response.json();

    }

    catch(error){

        console.error(error);

        showToast(

            "Unable to fetch data.",

            "danger"

        );

        return null;

    }

    finally{

        hideLoading();

    }

}

// ================================================
// Quick Stock Buttons
// ================================================

function initializeQuickButtons(){

    document.querySelectorAll(".quick-stock")

    .forEach(button=>{

        button.addEventListener("click",()=>{

            const symbol=

            button.dataset.symbol;

            const input=

            document.getElementById("stock-symbol");

            if(input){

                input.value=symbol;

            }

            if (typeof runStockSearch === "function") {
                runStockSearch(symbol);
            }

        });

    });

}

// ================================================
// Smooth Scroll
// ================================================

document.querySelectorAll('a[href^="#"]')

.forEach(anchor=>{

    anchor.addEventListener("click",function(e){

        e.preventDefault();

        document.querySelector(

            this.getAttribute("href")

        ).scrollIntoView({

            behavior:"smooth"

        });

    });

});

// ================================================
// Back To Top
// ================================================

window.addEventListener("scroll",()=>{

    const button=

    document.getElementById("backToTop");

    if(!button) return;

    if(window.scrollY>400){

        button.classList.remove("d-none");

    }

    else{

        button.classList.add("d-none");

    }

});

function scrollToTop(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}
function formatCurrency(value, currency = "USD") {

    if (value === null || value === undefined) {

        return "--";

    }

    return new Intl.NumberFormat("en-US", {

        style: "currency",

        currency: currency,

        maximumFractionDigits: 2

    }).format(value);

}
/* ===========================================
        LIVE SEARCH
=========================================== */

const stockInput = document.getElementById("stock-symbol");

if (stockInput) {

    stockInput.addEventListener("input", async function () {

        const query = this.value.trim();

        const container = document.getElementById("search-results");

        if (!container) return;

        if (query.length < 1) {

            container.innerHTML = "";

            return;

        }

        const response = await apiFetch(

            `/api/search?q=${encodeURIComponent(query)}`

        );

        if (!response) return;

        container.innerHTML = "";

        response.forEach(stock => {

            const item = document.createElement("div");

            item.className = "search-item";

            item.innerHTML = `

                <strong>${stock.symbol}</strong>

                <span>${stock.company}</span>

            `;

            item.onclick = () => {

                stockInput.value = stock.symbol;

                container.innerHTML = "";

            };

            container.appendChild(item);

        });

    });

}

/* ===========================================
        STOCK SEARCH (full lookup: company info,
        live quote, historical chart)
=========================================== */

async function runStockSearch(symbol){

    symbol = (symbol || "").trim().toUpperCase();

    if (!symbol) {
        showToast("Enter a stock symbol first.", "warning");
        return;
    }

    const resultsContainer = document.getElementById("search-results");
    if (resultsContainer) resultsContainer.innerHTML = "";

    const [company, dashboard] = await Promise.all([
        apiFetch(`/api/company/${symbol}`),
        apiFetch(`/api/dashboard/${symbol}`)
    ]);

    if (!company && !dashboard) {
        showToast(`Couldn't find data for ${symbol}.`, "danger");
        return;
    }

    if (company) {
        setValue("company-name", company.company_name || "N/A");
        setValue("sector", company.sector || "N/A");
        setValue("industry", company.industry || "N/A");
        setValue("country", company.country || "N/A");
        setValue("website", company.website || "N/A");
    }

    if (dashboard) {
        const currency = dashboard.currency || "USD";
        setValue("current-price", formatCurrency(dashboard.current_price, currency));
        setValue("open-price", formatCurrency(dashboard.history?.at(-1)?.open, currency));
        setValue("high-price", formatCurrency(dashboard.day_high, currency));
        setValue("low-price", formatCurrency(dashboard.day_low, currency));
        setValue("volume", formatNumber(dashboard.volume));

        if (dashboard.history && typeof renderDashboardChart === "function") {
            renderDashboardChart(dashboard.history, "history-chart");
        }
    }

}

function initializeStockSearchForm() {

    const form = document.getElementById("stock-search-form");
    const input = document.getElementById("stock-symbol");

    if (!form || !input) return;

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        runStockSearch(input.value);
    });

}

document.addEventListener("DOMContentLoaded", () => {
    initializeStockSearchForm();
});

/* ===========================================
        LIVE MARKET TICKER
=========================================== */

document.addEventListener("DOMContentLoaded", () => {

    loadTicker();

});

async function loadTicker() {

    const container = document.getElementById("ticker-track");

    if (!container) return;

    const data = await apiFetch("/api/ticker");

    if (!data) return;

    container.innerHTML = "";

    data.forEach(stock => {

        container.innerHTML += `

        <div class="ticker-item">

            <strong>${stock.symbol}</strong>

            <span class="ticker-green">

                ${formatCurrency(stock.price)}

            </span>

        </div>

        `;

    });

}
/* ===========================================
        AI Prediction
=========================================== */

async function loadPrediction(symbol, days = 7){

    const data = await apiFetch(
        `/api/predict/${symbol}?days=${days}`
    );

    if(!data) return;

    setValue("signal", data.signal);
    setValue("confidence", data.confidence != null ? data.confidence + "%" : "--");
    setValue("predicted-confidence", data.confidence != null ? data.confidence + "%" : "--");
    setValue("trend", data.trend);
    setValue("risk", data.risk);

    const currency = "USD"; // prediction endpoint doesn't return currency; default display

    setValue(
        "current-price",
        data.current_price != null ? formatCurrency(data.current_price, currency) : "--"
    );

    setValue(
        "predicted-price",
        data.prediction != null ? formatCurrency(data.prediction, currency) : "--"
    );

    if (data.current_price && data.prediction != null) {
        const change = ((data.prediction - data.current_price) / data.current_price) * 100;
        setValue("expected-change", `${change >= 0 ? "+" : ""}${change.toFixed(2)}%`);
    } else {
        setValue("expected-change", "--");
    }

    const summary = document.getElementById("prediction-summary");
    if (summary) {
        summary.innerHTML = `<p>${symbol} is showing a <strong>${data.trend}</strong> trend. ` +
            `Based on recent price action versus its 20-day moving average, the model leans ` +
            `<strong>${data.signal}</strong> with ${data.confidence}% confidence and ${data.risk} risk.</p>`;
    }

    // Fetch actual history for the "Actual" line on the chart
    const dashboardData = await apiFetch(`/api/dashboard/${symbol}`);

    if (dashboardData && dashboardData.history && typeof renderPredictionChart === "function") {
        renderPredictionChart(dashboardData.history, data.series || []);
    }

}

function initializePredictionForm() {

    const form = document.getElementById("prediction-form");
    const symbolInput = document.getElementById("symbol");
    const daysSelect = document.getElementById("days");

    if (!form || !symbolInput) return;

    form.addEventListener("submit", (event) => {

        event.preventDefault();

        const symbol = symbolInput.value.trim().toUpperCase();

        if (!symbol) {
            showToast("Enter a stock symbol first.", "warning");
            return;
        }

        const days = daysSelect ? parseInt(daysSelect.value, 10) : 7;

        loadPrediction(symbol, days);

    });

}

document.addEventListener("DOMContentLoaded", () => {
    initializePredictionForm();
});
/* ===========================================
        Portfolio
=========================================== */

async function addPortfolio(){

    const symbol =

        document.getElementById("portfolio-symbol").value;

    const shares =

        document.getElementById("portfolio-shares").value;

    const buy_price =

        document.getElementById("portfolio-price").value;

    const response = await apiFetch(

        "/api/portfolio/add",

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                symbol,

                shares,

                buy_price

            })

        }

    );

    if(response){

        showToast(

            "Added to Portfolio"

        );

        loadPortfolio();

    }

}

async function loadPortfolio(){

    const portfolio =

        await apiFetch(

            "/api/portfolio"

        );

    console.log(portfolio);

}
/* ===========================================
        NEWS FEED
=========================================== */

async function loadNews(){

    const container =

        document.getElementById("news-feed");

    if(!container) return;

    const news = await apiFetch("/api/news");

    if(!news) return;

    container.innerHTML = "";

    news.forEach(item=>{

        container.innerHTML += `

        <div class="news-item">

            <a href="${item.link}"

               target="_blank">

                ${item.title}

            </a>

            <small>

                ${item.published}

            </small>

        </div>

        `;

    });

}

document.addEventListener(

    "DOMContentLoaded",

    loadNews

);
/* ===========================================
        MARKET HEATMAP
=========================================== */

async function loadHeatmap(){

    const container =

        document.getElementById(

            "market-heatmap"

        );

    if(!container) return;

    const stocks =

        await apiFetch(

            "/api/heatmap"

        );

    if(!stocks) return;

    container.innerHTML="";

    stocks.forEach(stock=>{

        let color="heat-neutral";

        if(stock.change>0)

            color="heat-green";

        else if(stock.change<0)

            color="heat-red";

        container.innerHTML+=`

        <div class="heat-card ${color}">

            <div class="heat-symbol">

                ${stock.symbol}

            </div>

            <div class="heat-company">

                ${stock.company}

            </div>

            <div class="heat-price">

                ${formatCurrency(stock.price)}

            </div>

            <div class="heat-change">

                ${stock.change>0?"+":""}

                ${stock.change}%

            </div>

        </div>

        `;

    });

}

document.addEventListener(

    "DOMContentLoaded",

    loadHeatmap

);