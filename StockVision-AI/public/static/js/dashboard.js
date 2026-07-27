/*
====================================================
            StockVision AI Dashboard
====================================================
*/

let currentSymbol = "AAPL";

document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname === "/dashboard") {

        loadDashboard(currentSymbol);

        // Refresh every 60 seconds
        setInterval(() => {
            loadDashboard(currentSymbol);
        }, 60000);

        const form = document.getElementById("dashboard-symbol-form");
        const input = document.getElementById("dashboard-symbol");

        if (form && input) {
            form.addEventListener("submit", (event) => {
                event.preventDefault();
                const symbol = input.value.trim().toUpperCase();
                if (symbol) {
                    loadDashboard(symbol);
                }
            });
        }

    }

});

async function loadDashboard(symbol) {

    currentSymbol = symbol;

    try {

        showLoading();

        const data = await apiFetch(`/api/dashboard/${symbol}`);

        if (!data) return;

        updateKPICards(data);
        updateMarketSummary(data);

        if (typeof renderDashboardChart === "function") {
            renderDashboardChart(data.history, "price-chart");
        }

        showToast(`${symbol} data updated`, "success");

    }

    catch (error) {

        console.error(error);

        showToast("Dashboard update failed.", "danger");

    }

    finally {

        hideLoading();

    }

}

function updateKPICards(data) {

    const currency = data.currency || "USD";

    setValue("current-price", formatCurrency(data.current_price, currency));
    setValue("day-high", formatCurrency(data.day_high, currency));
    setValue("day-low", formatCurrency(data.day_low, currency));
    setValue("volume", formatNumber(data.volume));

}

function updateMarketSummary(data) {

    setValue("update-time", data.updated_at);

}

function setValue(id, value) {

    const element = document.getElementById(id);

    if (!element) return;

    animateValue(element, value);

}

function animateValue(element, value) {

    element.style.opacity = 0;

    setTimeout(() => {

        element.textContent = value;
        element.style.opacity = 1;

    }, 200);

}
