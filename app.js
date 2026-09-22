/*
==============================================================================
HSIC SOLUTION - FRONTEND CONTROLLER (INSTITUTIONAL STANDARD)
==============================================================================
*/

let chartMonthly = null;
let chartPaymentMigration = null;
let chartSegmentDist = null;
let chartSegmentOpp = null;
let chartPmGrowth = null;
let chartMembership = null;

document.addEventListener("DOMContentLoaded", () => {
    initClock();
    initTabs();
    loadCustomer(25790);
    loadDashboardData();
    initSearch();
    initSimulator();
});

function initClock() {
    const el = document.getElementById("live-time");
    function update() {
        const d = new Date();
        el.innerText = d.toISOString().replace("T", " ").substring(0, 19) + " UTC";
    }
    update();
    setInterval(update, 1000);
}

function initTabs() {
    const tabs = document.querySelectorAll(".nav-tab");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
            
            tab.classList.add("active");
            const target = tab.getAttribute("data-tab");
            const pane = document.getElementById(target);
            if (pane) pane.classList.add("active");
        });
    });
}

async function fetchData(url, fallbackUrl) {
    if (window.SYNCHRONY_DATA) {
        if (url.includes("summary.json") || (fallbackUrl && fallbackUrl.includes("/api/summary"))) {
            return window.SYNCHRONY_DATA["summary.json"];
        }
        if (url.includes("monthly-sow.json") || (fallbackUrl && fallbackUrl.includes("/api/monthly-sow"))) {
            return window.SYNCHRONY_DATA["monthly-sow.json"];
        }
        if (url.includes("categories.json") || (fallbackUrl && fallbackUrl.includes("/api/categories"))) {
            return window.SYNCHRONY_DATA["categories.json"];
        }
        if (url.includes("segments.json") || (fallbackUrl && fallbackUrl.includes("/api/segments"))) {
            return window.SYNCHRONY_DATA["segments.json"];
        }
        if (url.includes("sensitivity.json") || (fallbackUrl && fallbackUrl.includes("/api/sensitivity"))) {
            return window.SYNCHRONY_DATA["sensitivity.json"];
        }
        if (url.includes("/customers/") || (fallbackUrl && fallbackUrl.includes("/api/customer/"))) {
            const parts = url.split("/");
            const cid = parts[parts.length - 1].replace(".json", "");
            if (window.SYNCHRONY_DATA.customers && window.SYNCHRONY_DATA.customers[cid]) {
                return window.SYNCHRONY_DATA.customers[cid];
            }
        }
    }

    try {
        const res = await fetch(url);
        if (res.ok) return await res.json();
    } catch (e) {}
    if (fallbackUrl) {
        try {
            const res2 = await fetch(fallbackUrl);
            if (res2.ok) return await res2.json();
        } catch (e) {}
    }
    throw new Error(`Failed to load data from ${url}`);
}

async function loadDashboardData() {
    try {
        // 1. Fetch Summary
        const summary = await fetchData("./api/summary.json", "/api/summary");
        
        document.getElementById("kpi-sow-fy26").innerText = `${summary.fy26_hsic_sow_pct}%`;
        document.getElementById("kpi-sow-delta").innerText = `▼ ${summary.sow_change_pp} pp YoY (FY25: ${summary.fy25_hsic_sow_pct}%)`;
        document.getElementById("kpi-total-spend").innerText = `INR ${(summary.fy26_total_spend / 1e6).toFixed(2)}M`;
        document.getElementById("kpi-at-risk-count").innerText = `${summary.silent_attrition_count.toLocaleString()}`;
        document.getElementById("kpi-wallet-opp").innerText = `INR ${(summary.total_wallet_opportunity / 1e6).toFixed(2)}M`;
        document.getElementById("kpi-base-recovery").innerText = `INR ${(summary.total_wallet_opportunity * 0.10 / 1e6).toFixed(2)}M`;

        // 2. Fetch Monthly SoW
        const monthly = await fetchData("./api/monthly-sow.json", "/api/monthly-sow");
        renderMonthlyChart(monthly);

        // 3. Fetch Categories
        const categories = await fetchData("./api/categories.json", "/api/categories");
        renderCategoryTable(categories);

        // 4. Fetch Segments
        const segments = await fetchData("./api/segments.json", "/api/segments");
        renderSegmentTablesAndCharts(segments);

        // 5. Render Payment Migration & Additional Charts
        renderPaymentMigrationChart();

        // 6. Fetch Sensitivity
        const sens = await fetchData("./api/sensitivity.json", "/api/sensitivity");
        renderSensitivityTable(sens);

        // Load Default Customer 25790
        loadCustomer(25790);

    } catch (err) {
        console.error("Failed loading dashboard data:", err);
    }
}

function renderMonthlyChart(monthly) {
    const ctx = document.getElementById("chart-monthly-sow").getContext("2d");
    const labels = monthly.map(m => m.Year_Month);
    const sowValues = monthly.map(m => m.HSIC_SoW_Pct);
    const mmSpend = monthly.map(m => (m.Total_MetroMart_Net_Spend / 1e6).toFixed(2));

    if (chartMonthly) chartMonthly.destroy();

    chartMonthly = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "HSIC Share of Wallet (%)",
                    data: sowValues,
                    borderColor: "#B91C1C",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    pointRadius: 3,
                    pointBackgroundColor: "#B91C1C",
                    yAxisID: "y"
                },
                {
                    label: "Total MetroMart Net Sales (INR M)",
                    data: mmSpend,
                    borderColor: "#0F294A",
                    backgroundColor: "rgba(15, 41, 74, 0.06)",
                    borderWidth: 1.5,
                    borderDash: [4, 4],
                    pointRadius: 0,
                    fill: true,
                    yAxisID: "y1"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: {
                    position: "top",
                    labels: { font: { size: 10, family: "sans-serif" }, boxWidth: 12 }
                },
                tooltip: {
                    callbacks: {
                        label: function(c) {
                            if (c.datasetIndex === 0) return `HSIC SoW: ${c.raw}%`;
                            return `MetroMart Sales: INR ${c.raw}M`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: "#E2E8F0" },
                    ticks: { font: { size: 9 }, maxRotation: 45 }
                },
                y: {
                    type: "linear",
                    display: true,
                    position: "left",
                    title: { display: true, text: "Share of Wallet (%)", font: { size: 10 } },
                    grid: { color: "#E2E8F0" },
                    ticks: { font: { size: 9 }, callback: v => v + "%" }
                },
                y1: {
                    type: "linear",
                    display: true,
                    position: "right",
                    title: { display: true, text: "Net Sales (INR M)", font: { size: 10 } },
                    grid: { drawOnChartArea: false },
                    ticks: { font: { size: 9 }, callback: v => "INR " + v + "M" }
                }
            }
        }
    });
}

function renderPaymentMigrationChart() {
    const ctx = document.getElementById("chart-payment-migration").getContext("2d");
    
    const methods = ["HSIC Card", "Other Credit Card", "Debit Card", "Cash / UPI", "MetroMart Wallet"];
    const fy25Spend = [85.67, 92.14, 74.32, 68.51, 57.00];
    const fy26Spend = [68.92, 112.45, 88.19, 86.92, 79.21];

    if (chartPaymentMigration) chartPaymentMigration.destroy();

    chartPaymentMigration = new Chart(ctx, {
        type: "bar",
        data: {
            labels: methods,
            datasets: [
                {
                    label: "FY2025 Spend (INR M)",
                    data: fy25Spend,
                    backgroundColor: "#94A3B8",
                    borderColor: "#64748B",
                    borderWidth: 1
                },
                {
                    label: "FY2026 Spend (INR M)",
                    data: fy26Spend,
                    backgroundColor: ["#B91C1C", "#1E3A8A", "#0F294A", "#0284C7", "#059669"],
                    borderColor: "#0F172A",
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top", labels: { font: { size: 10 }, boxWidth: 12 } }
            },
            scales: {
                x: { grid: { color: "#E2E8F0" }, ticks: { font: { size: 9 } } },
                y: {
                    grid: { color: "#E2E8F0" },
                    ticks: { font: { size: 9 }, callback: v => "INR " + v + "M" },
                    title: { display: true, text: "Net Spend Volume (INR Millions)", font: { size: 10 } }
                }
            }
        }
    });

    // Payment growth chart in tab 4
    const ctxGrowth = document.getElementById("chart-pm-growth");
    if (ctxGrowth) {
        if (chartPmGrowth) chartPmGrowth.destroy();
        chartPmGrowth = new Chart(ctxGrowth.getContext("2d"), {
            type: "bar",
            data: {
                labels: methods,
                datasets: [{
                    label: "YoY Spend Growth (%)",
                    data: [-19.55, 22.04, 18.66, 26.87, 38.96],
                    backgroundColor: ["#B91C1C", "#047857", "#047857", "#047857", "#047857"],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { font: { size: 9 } } },
                    y: { ticks: { font: { size: 9 }, callback: v => v + "%" }, title: { display: true, text: "YoY Growth Rate (%)", font: { size: 10 } } }
                }
            }
        });
    }

    // Membership retention chart in tab 4
    const ctxMem = document.getElementById("chart-membership-sow");
    if (ctxMem) {
        if (chartMembership) chartMembership.destroy();
        chartMembership = new Chart(ctxMem.getContext("2d"), {
            type: "bar",
            data: {
                labels: ["Prime Members (59.9%)", "Non-Prime Members (40.1%)"],
                datasets: [
                    { label: "FY2025 SoW", data: [22.27, 23.30], backgroundColor: "#94A3B8" },
                    { label: "FY2026 SoW", data: [15.93, 15.65], backgroundColor: "#1E3A8A" }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "top", labels: { font: { size: 10 } } } },
                scales: {
                    y: { ticks: { callback: v => v + "%" }, title: { display: true, text: "Share of Wallet (%)", font: { size: 10 } } }
                }
            }
        });
    }
}

function renderCategoryTable(categories) {
    const tbody = document.querySelector("#table-categories tbody");
    tbody.innerHTML = "";
    categories.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${c.Category}</strong></td>
            <td class="num">${c.FY25_HSIC_SoW_Pct}%</td>
            <td class="num">${c.FY26_HSIC_SoW_Pct}%</td>
            <td class="num delta-neg">${c.SoW_Change_pp} pp</td>
            <td class="num delta-pos">+${c.Total_Spend_Growth_Pct}%</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderSegmentTablesAndCharts(segments) {
    const tbodySummary = document.querySelector("#table-segments-summary tbody");
    const tbodyFull = document.querySelector("#table-full-segmentation tbody");
    
    tbodySummary.innerHTML = "";
    if (tbodyFull) tbodyFull.innerHTML = "";

    const totalCust = segments.reduce((a, b) => a + b.Customer_Count, 0);

    segments.forEach(s => {
        const pct = (s.Customer_Count / totalCust * 100).toFixed(1);
        
        // Summary row
        const trSum = document.createElement("tr");
        trSum.innerHTML = `
            <td><strong>${s.Customer_Segment}</strong></td>
            <td class="num">${s.Customer_Count.toLocaleString()}</td>
            <td class="num">${s.Avg_HSIC_SoW_FY26}%</td>
            <td class="num">${s.Avg_Risk_Score}</td>
            <td class="num">INR ${(s.Total_Wallet_Opportunity / 1e6).toFixed(2)}M</td>
        `;
        tbodySummary.appendChild(trSum);

        // Full tab 3 row
        if (tbodyFull) {
            const trFull = document.createElement("tr");
            trFull.innerHTML = `
                <td><strong>${s.Customer_Segment}</strong></td>
                <td class="num">${s.Customer_Count.toLocaleString()}</td>
                <td class="num">${pct}%</td>
                <td class="num">${s.Avg_HSIC_SoW_FY26}%</td>
                <td class="num delta-neg">${s.Avg_SoW_Change_pp} pp</td>
                <td class="num">${s.Avg_Risk_Score}</td>
                <td class="num">INR ${Math.round(s.Avg_Total_Spend_FY26).toLocaleString()}</td>
                <td class="num">INR ${Math.round(s.Avg_Wallet_Opportunity).toLocaleString()}</td>
                <td class="num"><strong>INR ${(s.Total_Wallet_Opportunity / 1e6).toFixed(2)}M</strong></td>
            `;
            tbodyFull.appendChild(trFull);
        }
    });

    // Charts in Tab 3
    const ctxDist = document.getElementById("chart-segment-distribution");
    if (ctxDist) {
        if (chartSegmentDist) chartSegmentDist.destroy();
        chartSegmentDist = new Chart(ctxDist.getContext("2d"), {
            type: "doughnut",
            data: {
                labels: segments.map(s => s.Customer_Segment),
                datasets: [{
                    data: segments.map(s => s.Customer_Count),
                    backgroundColor: ["#94A3B8", "#0284C7", "#B45309", "#047857", "#B91C1C"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "right", labels: { font: { size: 10 } } } }
            }
        });
    }

    const ctxOpp = document.getElementById("chart-segment-opp");
    if (ctxOpp) {
        if (chartSegmentOpp) chartSegmentOpp.destroy();
        chartSegmentOpp = new Chart(ctxOpp.getContext("2d"), {
            type: "bar",
            data: {
                labels: segments.map(s => s.Customer_Segment),
                datasets: [{
                    label: "Total Wallet Opportunity (INR M)",
                    data: segments.map(s => (s.Total_Wallet_Opportunity / 1e6).toFixed(2)),
                    backgroundColor: ["#94A3B8", "#0284C7", "#B45309", "#047857", "#B91C1C"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { font: { size: 9 } } },
                    y: { ticks: { callback: v => "INR " + v + "M" } }
                }
            }
        });
    }
}

function renderSensitivityTable(sens) {
    const tbody = document.querySelector("#table-sensitivity tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    sens.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${s.Analysis_Track}</strong></td>
            <td class="num">${s.Customer_Count.toLocaleString()}</td>
            <td class="num">INR ${(s.FY25_Total_Spend_INR / 1e6).toFixed(2)}M</td>
            <td class="num">INR ${(s.FY26_Total_Spend_INR / 1e6).toFixed(2)}M</td>
            <td class="num">${s.FY25_HSIC_SoW_Pct}%</td>
            <td class="num">${s.FY26_HSIC_SoW_Pct}%</td>
            <td class="num delta-neg">${s.SoW_Change_pp} pp</td>
            <td class="num">${s.Silent_Attrition_Count.toLocaleString()}</td>
            <td class="num"><strong>INR ${(s.Total_Wallet_Opportunity_INR / 1e6).toFixed(2)}M</strong></td>
        `;
        tbody.appendChild(tr);
    });
}

function initSearch() {
    const btn = document.getElementById("btn-search");
    const input = document.getElementById("input-customer-search");

    const doSearch = async () => {
        const val = input.value.trim();
        if (!val) return;
        btn.disabled = true;
        btn.innerText = "Searching...";
        try {
            await loadCustomer(val);
        } finally {
            btn.disabled = false;
            btn.innerText = "Search";
        }
    };

    btn.addEventListener("click", doSearch);
    input.addEventListener("keyup", (e) => {
        if (e.key === "Enter") doSearch();
    });
}

function loadShardScript(prefix) {
    return new Promise((resolve, reject) => {
        if (window.SYNCHRONY_SHARDS && window.SYNCHRONY_SHARDS[prefix]) return resolve();
        // Check if script already injected
        const existing = document.querySelector(`script[data-shard="${prefix}"]`);
        if (existing) {
            existing.addEventListener("load", () => resolve());
            existing.addEventListener("error", () => reject(new Error(`Shard ${prefix} failed to load`)));
            return;
        }
        const s = document.createElement("script");
        s.setAttribute("data-shard", prefix);
        s.src = `./api/customers/shard_${prefix}.js`;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error(`Shard ${prefix} failed to load`));
        document.head.appendChild(s);
    });
}

async function loadCustomer(cid) {
    try {
        let c;
        // Clean customer ID to numbers only (handles #25790, Customer 25790, etc.)
        const cidStr = String(cid).replace(/[^0-9]/g, "").trim();
        if (!cidStr) {
            alert("Please enter a valid numeric Customer ID (e.g. 25790, 83487, 45620).");
            return;
        }
        const prefix = cidStr.slice(0, 2);

        // 1. Check in-memory shards
        if (window.SYNCHRONY_SHARDS && window.SYNCHRONY_SHARDS[prefix] && window.SYNCHRONY_SHARDS[prefix][cidStr]) {
            c = window.SYNCHRONY_SHARDS[prefix][cidStr];
        }
        // 2. Check pre-bundled customer sample
        else if (window.SYNCHRONY_DATA && window.SYNCHRONY_DATA.customers && window.SYNCHRONY_DATA.customers[cidStr]) {
            c = window.SYNCHRONY_DATA.customers[cidStr];
        }
        // 3. Load shard on-demand via script tag (100% compatible with file:/// and HTTP/HTTPS)
        else {
            try {
                await loadShardScript(prefix);
                if (window.SYNCHRONY_SHARDS && window.SYNCHRONY_SHARDS[prefix]) {
                    c = window.SYNCHRONY_SHARDS[prefix][cidStr];
                }
            } catch(e) {
                console.warn(`Could not load shard_${prefix}.js:`, e);
            }
        }

        // 4. Fallback to individual customer endpoint if available
        if (!c) {
            try {
                c = await fetchData(`./api/customers/${cidStr}.json`, `/api/customer/${cidStr}`);
            } catch (e) {}
        }

        if (!c) {
            alert(`Customer ID #${cidStr} was not found in dataset. Valid customer IDs range from 10000 to 99999.`);
            return;
        }

        // Update Tab 2 UI
        document.getElementById("c360-id").innerText = `Customer #${c.Customer_ID}`;
        document.getElementById("c360-tier").innerText = `${(c.Membership_Type || "Standard").toUpperCase()} MEMBER | ${(c.Gender || "N/A").toUpperCase()}, AGE ${c.Age}`;
        document.getElementById("c360-segment").innerText = c.Customer_Segment;
        
        // Status tag color
        const tag = document.getElementById("c360-segment");
        if (c.Customer_Segment === "Silent Attrition") {
            tag.style.backgroundColor = "var(--crimson-50)";
            tag.style.color = "var(--crimson-700)";
            tag.style.borderColor = "#FECACA";
        } else if (c.Customer_Segment === "Loyal HSIC Customer") {
            tag.style.backgroundColor = "var(--emerald-50)";
            tag.style.color = "var(--emerald-700)";
            tag.style.borderColor = "#A7F3D0";
        } else {
            tag.style.backgroundColor = "var(--slate-100)";
            tag.style.color = "var(--slate-800)";
            tag.style.borderColor = "var(--border-color)";
        }

        document.getElementById("c360-limit").innerText = c.Credit_Card_Limit ? `INR ${c.Credit_Card_Limit.toLocaleString()}` : "N/A";
        document.getElementById("c360-apr").innerText = c.Credit_Card_APR ? `${c.Credit_Card_APR}%` : "N/A";
        document.getElementById("c360-open").innerText = c.Credit_Card_Open_Date || "Imputed Baseline";
        document.getElementById("c360-status").innerText = c.Credit_Card_Closed_Date ? `Closed on ${c.Credit_Card_Closed_Date}` : "Active / Open";

        // Risk
        document.getElementById("c360-risk-score").innerText = `${c.Risk_Score.toFixed(1)} / 100`;
        document.getElementById("c360-risk-bar").style.width = `${Math.min(100, c.Risk_Score)}%`;
        if (c.Risk_Score >= 70) {
            document.getElementById("c360-risk-bar").style.backgroundColor = "var(--crimson-700)";
            document.getElementById("c360-risk-score").style.color = "var(--crimson-700)";
        } else if (c.Risk_Score >= 40) {
            document.getElementById("c360-risk-bar").style.backgroundColor = "var(--amber-700)";
            document.getElementById("c360-risk-score").style.color = "var(--amber-700)";
        } else {
            document.getElementById("c360-risk-bar").style.backgroundColor = "var(--emerald-700)";
            document.getElementById("c360-risk-score").style.color = "var(--emerald-700)";
        }

        // Wallet Opportunity
        document.getElementById("c360-wallet-opp").innerText = `INR ${c.Wallet_Opportunity.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        // Spend comparison
        document.getElementById("c360-fy25-total").innerText = `INR ${Math.round(c.FY25_Total_Spend).toLocaleString()}`;
        document.getElementById("c360-fy26-total").innerText = `FY26: INR ${Math.round(c.FY26_Total_Spend).toLocaleString()} (${c.Total_Spend_Change_pct >= 0 ? '+' : ''}${c.Total_Spend_Change_pct}%)`;

        document.getElementById("c360-fy25-hsic").innerText = `INR ${Math.round(c.FY25_HSIC_Spend).toLocaleString()}`;
        document.getElementById("c360-fy26-hsic").innerText = `FY26: INR ${Math.round(c.FY26_HSIC_Spend).toLocaleString()} (${c.HSIC_Spend_Change_pct >= 0 ? '+' : ''}${c.HSIC_Spend_Change_pct}%)`;

        document.getElementById("c360-fy25-sow").innerText = `${c.FY25_HSIC_SoW.toFixed(1)}%`;
        document.getElementById("c360-fy26-sow").innerText = `FY26: ${c.FY26_HSIC_SoW.toFixed(1)}% (${c.SoW_Change_pp >= 0 ? '+' : ''}${c.SoW_Change_pp} pp)`;

        // Payment Breakdown Table
        const tbBreak = document.querySelector("#c360-payment-breakdown tbody");
        tbBreak.innerHTML = `
            <tr>
                <td><strong>HSIC Bank Credit Card</strong></td>
                <td class="num">INR ${Math.round(c.FY25_HSIC_Spend).toLocaleString()}</td>
                <td class="num">INR ${Math.round(c.FY26_HSIC_Spend).toLocaleString()}</td>
                <td class="num"><strong>${c.FY26_HSIC_SoW.toFixed(1)}%</strong></td>
                <td>${c.FY26_HSIC_Spend < c.FY25_HSIC_Spend ? '<span class="delta-neg">Contraction</span>' : '<span class="delta-pos">Stable/Growing</span>'}</td>
            </tr>
            <tr>
                <td>Other Bank Credit Card</td>
                <td class="num">INR ${Math.round(c.FY25_Other_CC_Spend).toLocaleString()}</td>
                <td class="num">INR ${Math.round(c.FY26_Other_CC_Spend).toLocaleString()}</td>
                <td class="num">${c.FY26_Total_Spend > 0 ? (c.FY26_Other_CC_Spend / c.FY26_Total_Spend * 100).toFixed(1) : 0}%</td>
                <td>${c.Dominant_Alternative_Method === 'Other Bank Credit Card' ? '<strong>Primary Substitute</strong>' : 'Secondary'}</td>
            </tr>
            <tr>
                <td>Debit Card</td>
                <td class="num">INR ${Math.round(c.FY25_Debit_Spend).toLocaleString()}</td>
                <td class="num">INR ${Math.round(c.FY26_Debit_Spend).toLocaleString()}</td>
                <td class="num">${c.FY26_Total_Spend > 0 ? (c.FY26_Debit_Spend / c.FY26_Total_Spend * 100).toFixed(1) : 0}%</td>
                <td>${c.Dominant_Alternative_Method === 'Debit Card' ? '<strong>Primary Substitute</strong>' : 'Secondary'}</td>
            </tr>
            <tr>
                <td>Cash / UPI</td>
                <td class="num">INR ${Math.round(c.FY25_UPI_Spend).toLocaleString()}</td>
                <td class="num">INR ${Math.round(c.FY26_UPI_Spend).toLocaleString()}</td>
                <td class="num">${c.FY26_Total_Spend > 0 ? (c.FY26_UPI_Spend / c.FY26_Total_Spend * 100).toFixed(1) : 0}%</td>
                <td>${c.Dominant_Alternative_Method === 'Cash/UPI' ? '<strong>Primary Substitute</strong>' : 'Secondary'}</td>
            </tr>
            <tr>
                <td>MetroMart Wallet</td>
                <td class="num">INR ${Math.round(c.FY25_Wallet_Spend).toLocaleString()}</td>
                <td class="num">INR ${Math.round(c.FY26_Wallet_Spend).toLocaleString()}</td>
                <td class="num">${c.FY26_Total_Spend > 0 ? (c.FY26_Wallet_Spend / c.FY26_Total_Spend * 100).toFixed(1) : 0}%</td>
                <td>${c.Dominant_Alternative_Method === 'MetroMart Wallet' ? '<strong>Primary Substitute</strong>' : 'Secondary'}</td>
            </tr>
        `;

        // Customer Risk Radar & Next Best Offer Engine ⭐
        const sowDelta = c.SoW_Change_pp !== undefined && c.SoW_Change_pp !== null ? c.SoW_Change_pp : 0;
        const isLoyalOrGrowing = sowDelta >= 0 || c.Risk_Score < 25;

        // Dynamic Badge & Box Theme (Green for Loyalty/Growth, Red for Risk/Attrition)
        const badgeRadarEl = document.querySelector(".badge-risk-radar");
        const radarBoxEl = document.querySelector(".risk-radar-box");
        const reasonTextEl = document.getElementById("c360-radar-reason");

        if (isLoyalOrGrowing) {
            if (badgeRadarEl) {
                badgeRadarEl.innerText = "LOYALTY & RETENTION RADAR";
                badgeRadarEl.style.backgroundColor = "#16A34A";
            }
            if (radarBoxEl) {
                radarBoxEl.style.borderLeftColor = "#16A34A";
                radarBoxEl.style.borderColor = "#BBF7D0";
                radarBoxEl.style.backgroundColor = "#F0FDF4";
            }
            if (reasonTextEl) {
                reasonTextEl.style.color = "#14532D";
                reasonTextEl.style.borderColor = "#86EFAC";
                reasonTextEl.style.backgroundColor = "#FFFFFF";
            }
        } else {
            if (badgeRadarEl) {
                badgeRadarEl.innerText = "CUSTOMER RISK RADAR";
                badgeRadarEl.style.backgroundColor = "#DC2626";
            }
            if (radarBoxEl) {
                radarBoxEl.style.borderLeftColor = "#DC2626";
                radarBoxEl.style.borderColor = "#FECACA";
                radarBoxEl.style.backgroundColor = "#FEF2F2";
            }
            if (reasonTextEl) {
                reasonTextEl.style.color = "#7F1D1D";
                reasonTextEl.style.borderColor = "#FCA5A5";
                reasonTextEl.style.backgroundColor = "#FFFFFF";
            }
        }

        if (reasonTextEl) reasonTextEl.innerText = c.Risk_Radar_Reason || c.Recommendation_Reason || "Behavioral spend pattern evaluated across checkout channels.";

        const radarSowLabelEl = document.getElementById("c360-radar-sow-label");
        if (radarSowLabelEl) radarSowLabelEl.innerText = sowDelta >= 0 ? "SoW Lift:" : "SoW Drop:";

        const radarSowEl = document.getElementById("c360-radar-sow");
        if (radarSowEl) {
            radarSowEl.innerText = `${sowDelta > 0 ? '+' : ''}${sowDelta.toFixed(1)} pp`;
            radarSowEl.className = `chip-val ${sowDelta < 0 ? 'delta-neg' : 'delta-pos'}`;
        }

        const radarCatEl = document.getElementById("c360-radar-cat");
        if (radarCatEl) radarCatEl.innerText = c.Top_Diverted_Category || "General Merchandise";

        const radarAltEl = document.getElementById("c360-radar-alt");
        if (radarAltEl) radarAltEl.innerText = c.Dominant_Alternative_Method || "None (100% HSIC)";

        const nboRuleEl = document.getElementById("c360-nbo-rule");
        if (nboRuleEl) nboRuleEl.innerText = c.NBO_Rule_Triggered || "IF Multi-Tender Checkout Pattern";

        const nboOfferEl = document.getElementById("c360-nbo-offer");
        if (nboOfferEl) nboOfferEl.innerText = c.Next_Best_Offer || c.Recommended_Action || "Offer targeted category cashback";

        const stratEl = document.getElementById("c360-rec-strategy");
        if (stratEl) stratEl.innerText = c.Strategy_Details || "Translates customer payment and basket analytics into tailored commercial intervention.";

    } catch (err) {
        console.error("Error loading customer:", err);
    }
}

function initSimulator() {
    const slider = document.getElementById("slider-recovery");
    if (!slider) return;
    const lblVal = document.getElementById("lbl-slider-val");

    async function updateSim() {
        const rate = parseFloat(slider.value);
        lblVal.innerText = `${rate.toFixed(1)}%`;
        
        try {
            const res = await fetch(`/api/simulator?rate=${rate}`);
            const data = await res.json();

            document.getElementById("sim-recoverable-total").innerText = `INR ${Math.round(data.estimated_recoverable_inr).toLocaleString()}`;
            document.getElementById("sim-recoverable-sub").innerText = `Based on ${rate.toFixed(1)}% Recovery Rate`;
            document.getElementById("sim-recoverable-per-cust").innerText = `INR ${data.recoverable_per_at_risk_customer.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

            // Scenario Table
            const tbody = document.querySelector("#table-simulator-scenarios tbody");
            tbody.innerHTML = "";
            const labels = ["Conservative Case", "Base Case (Target)", "Target Case", "Optimistic Case", "High Campaign Intensity", "Aggressive Case"];
            
            data.scenarios.forEach((sc, i) => {
                const isSelected = Math.abs(sc.rate_pct - rate) < 0.1;
                const tr = document.createElement("tr");
                if (isSelected) tr.style.backgroundColor = "var(--slate-200)";
                tr.innerHTML = `
                    <td><strong>${labels[i] || 'Scenario'}</strong> ${isSelected ? '(Active Selection)' : ''}</td>
                    <td class="num">${sc.rate_pct.toFixed(1)}%</td>
                    <td class="num"><strong>INR ${Math.round(sc.recoverable_inr).toLocaleString()}</strong></td>
                    <td class="num">INR ${sc.per_account_inr.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                    <td>${getFeasibilityText(sc.rate_pct)}</td>
                `;
                tbody.appendChild(tr);
            });

        } catch (err) {
            console.error("Simulator error:", err);
        }
    }

    slider.addEventListener("input", updateSim);
    updateSim();
}

function getFeasibilityText(rate) {
    if (rate <= 5) return "High feasibility via automated digital wallet reminders & top-of-wallet prompts.";
    if (rate <= 10) return "Achievable through targeted 5% cashback category accelerators & INR 500 milestone statement credits.";
    if (rate <= 15) return "Requires multi-touch omnichannel campaign and merchant checkout banner integrations.";
    if (rate <= 20) return "Aggressive scenario requiring double points promo and fee waivers on high-ticket retail categories.";
    return "Maximum theoretical recovery requiring extensive subsidies and co-brand partner co-funding.";
}
