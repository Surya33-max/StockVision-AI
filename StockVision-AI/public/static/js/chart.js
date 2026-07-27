/*
====================================================
            StockVision AI Charts
            Plotly.js
====================================================
*/

let dashboardChart = null;

/* ===========================================
        Dashboard Chart
=========================================== */

function renderDashboardChart(history, targetId = "price-chart") {

    if (!history || history.length === 0) {

        console.warn("No historical data available.");

        return;

    }

    const dates = history.map(item => item.date);

    const open = history.map(item => item.open);

    const high = history.map(item => item.high);

    const low = history.map(item => item.low);

    const close = history.map(item => item.close);

    const volume = history.map(item => item.volume);

    const candlestick = {

        x: dates,

        open: open,

        high: high,

        low: low,

        close: close,

        type: "candlestick",

        name: "Price",

        increasing: {

            line: {

                color: "#00D084"

            }

        },

        decreasing: {

            line: {

                color: "#EF4444"

            }

        }

    };

    const volumeBar = {

        x: dates,

        y: volume,

        type: "bar",

        name: "Volume",

        yaxis: "y2",

        opacity: 0.35

    };

    const layout = {

        paper_bgcolor: "transparent",

        plot_bgcolor: "transparent",

        dragmode: "zoom",

        hovermode: "x unified",

        margin: {

            l: 50,

            r: 30,

            t: 30,

            b: 40

        },

        xaxis: {

            rangeslider: {

                visible: false

            },

            color: "#FFFFFF"

        },

        yaxis: {

            title: "Price",

            color: "#FFFFFF"

        },

        yaxis2: {

            title: "Volume",

            overlaying: "y",

            side: "right",

            showgrid: false,

            color: "#AAAAAA"

        },

        legend: {

            orientation: "h",

            font: {

                color: "#FFFFFF"

            }

        }

    };

    const config = {

        responsive: true,

        displaylogo: false,

        scrollZoom: true,

        displayModeBar: true

    };

    Plotly.newPlot(

        targetId,

        [

            candlestick,

            volumeBar

        ],

        layout,

        config

    );

}

/* ===========================================
        Prediction Chart
=========================================== */

function renderPredictionChart(actual, predicted) {

    Plotly.newPlot(

        "prediction-chart",

        [

            {

                x: actual.map(item => item.date),

                y: actual.map(item => item.close),

                mode: "lines",

                name: "Actual"

            },

            {

                x: predicted.map(item => item.date),

                y: predicted.map(item => item.price),

                mode: "lines",

                line: {

                    dash: "dash"

                },

                name: "Predicted"

            }

        ],

        {

            paper_bgcolor: "transparent",

            plot_bgcolor: "transparent",

            font: {

                color: "#FFFFFF"

            }

        },

        {

            responsive: true

        }

    );

}

/* ===========================================
        Portfolio Pie Chart
=========================================== */

function renderPortfolioChart(data) {

    Plotly.newPlot(

        "portfolio-chart",

        [

            {

                values: data.map(item => item.value),

                labels: data.map(item => item.symbol),

                type: "pie",

                hole: 0.55,

                textinfo: "label+percent"

            }

        ],

        {

            paper_bgcolor: "transparent",

            plot_bgcolor: "transparent",

            font: {

                color: "#FFFFFF"

            },

            showlegend: true

        },

        {

            responsive: true

        }

    );

}

/* ===========================================
        Resize Chart
=========================================== */

window.addEventListener("resize", () => {

    if (document.getElementById("dashboard-chart")) {

        Plotly.Plots.resize(

            document.getElementById("dashboard-chart")

        );

    }

});