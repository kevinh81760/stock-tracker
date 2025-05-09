function openTab(tabName) {
    const tabs = document.getElementsByClassName("tab-content");
    for (let tab of tabs) {
        tab.style.display = "none";
    }

    const buttons = document.getElementsByClassName("tab-button");
    for (let btn of buttons) {
        btn.classList.remove("active");
    }

    document.getElementById(tabName).style.display = "block";
    document
        .querySelector(`[onclick="openTab('${tabName}')"]`)
        .classList.add("active");

    // Load history when history tab is opened
    if (tabName === 'history') {
        loadHistory();
    }
}

function loadHistory() {
    const historyDiv = document.getElementById("history");
    historyDiv.innerHTML = '<div class="loading">Loading history...</div>';

    fetch('/history')
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            if (data.error) {
                historyDiv.innerHTML = `<div class="error">${data.error}</div>`;
                return;
            }

            if (data.history.length === 0) {
                historyDiv.innerHTML = '<div class="no-data">No search history available</div>';
                return;
            }

            historyDiv.innerHTML = `
                <table class="data-table">
                    <tr>
                        <th>Ticker Symbol</th>
                        <th>Search Time</th>
                    </tr>
                    ${data.history.map(entry => `
                        <tr>
                            <td>${entry.ticker}</td>
                            <td>${new Date(entry.timestamp).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </table>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            historyDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        });
}

function loadCompany(event) {
    event.preventDefault();

    const ticker = document.getElementById("ticker").value.trim();
    const status = document.getElementById("status");
    const outlook = document.getElementById("outlook");
    const summary = document.getElementById("summary");

    if (!ticker) {
        alert("Please enter a valid ticker symbol");
        return;
    }

    status.innerHTML = "Loading...";
    outlook.innerHTML = "";
    summary.innerHTML = "";

    fetch(`/company?ticker=${ticker}`)
        .then((res) => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then((data) => {
            if (data.error) {
                status.innerHTML = `Error: ${data.error}`;
                return;
            }

            status.innerHTML = "Successfully loaded";

            outlook.innerHTML = `
                <table class="data-table">
                    <tr><td><strong>Company Name</strong></td><td>${data.company.name}</td></tr>
                    <tr><td><strong>Ticker Symbol</strong></td><td>${data.company.ticker}</td></tr>
                    <tr><td><strong>Exchange</strong></td><td>${data.company.exchangeCode}</td></tr>
                    <tr><td><strong>Start Date</strong></td><td>${new Date(data.company.startDate).toLocaleDateString()}</td></tr>
                    <tr><td><strong>Description</strong></td><td>${data.company.description}</td></tr>
                </table>
            `;

            const last = data.stock.last;
            const prevClose = data.stock.prevClose;
            const change = last !== null && prevClose !== null ? last - prevClose : null;
            const changePercent = change !== null ? (change / prevClose) * 100 : null;
            const arrow = change !== null ? (change >= 0 ? "🟢 ▲" : "🔴 ▼") : "";

            summary.innerHTML = `
                <table class="data-table">
                    <tr><td><strong>Stock Ticker Symbol</strong></td><td>${data.stock.ticker}</td></tr>
                    <tr><td><strong>Trading Day</strong></td><td>${new Date(data.stock.timestamp).toLocaleDateString()}</td></tr>
                    <tr><td><strong>Previous Closing Price</strong></td><td>$${prevClose !== null ? prevClose.toFixed(2) : "N/A"}</td></tr>
                    <tr><td><strong>Opening Price</strong></td><td>$${data.stock.open !== null ? data.stock.open.toFixed(2) : "N/A"}</td></tr>
                    <tr><td><strong>High Price</strong></td><td>$${data.stock.high !== null ? data.stock.high.toFixed(2) : "N/A"}</td></tr>
                    <tr><td><strong>Low Price</strong></td><td>$${data.stock.low !== null ? data.stock.low.toFixed(2) : "N/A"}</td></tr>
                    <tr><td><strong>Last Price</strong></td><td>$${last !== null ? last.toFixed(2) : "N/A"}</td></tr>
                    <tr><td><strong>Change</strong></td><td>${change !== null ? change.toFixed(2) + " " + arrow : "N/A"}</td></tr>
                    <tr><td><strong>Change Percent</strong></td><td>${changePercent !== null ? changePercent.toFixed(2) + "% " + arrow : "N/A"}</td></tr>
                    <tr><td><strong>Number of Shares Traded</strong></td><td>${data.stock.volume !== null ? data.stock.volume.toLocaleString() : "N/A"}</td></tr>
                </table>
            `;
        })
        .catch((error) => {
            console.error("Fetch failed:", error);
            status.innerHTML = `Error: ${error.message}`;
        });
}
