# Customer and Credit Card Analytics — Silent Attrition & Share of Wallet Optimization

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Interactive%20Dashboard-brightgreen?style=for-the-badge&logo=googlechrome)](https://adityakasara.github.io/Synchrony_One/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange?style=for-the-badge&logo=jupyter)](notebooks/analysis.ipynb)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)](LICENSE)

An institutional-grade analytics solution for detecting **Silent Attrition**, diagnosing **Share of Wallet (SoW)** erosion, and executing an automated **Next Best Offer (NBO) Engine** on customer and credit card transaction data.

---

## 🚀 Live Interactive Dashboard
Experience the live web application directly in your browser:  
👉 **[https://adityakasara.github.io/Synchrony_One/](https://adityakasara.github.io/Synchrony_One/)**

---

## 📌 Problem Overview & Key Insights

While overall store retail spend expanded by **+15.37% YoY** (reaching INR 435.69M in FY26), co-branded card spending contracted by **-19.55% YoY**, causing the co-branded card's **Share of Wallet (SoW)** to fall from **22.69% to 15.82% (-6.87 pp)**.

### What is Silent Attrition?
Cardholders did **not** stop shopping at the retailer. Instead, they silently diverted their payment tenders at checkout into:
- **Merchant Stored Wallet:** **+38.96%** (+INR 22.2M) due to 1-tap in-app discount convenience.
- **Mobile UPI QR Scanning:** **+26.87%** (+INR 18.4M) due to POS plastic card friction.
- **Competitor Credit Cards:** **+22.04%** (+INR 20.3M) in high-ticket categories (Electronics, Appliances).
- **Debit Cards:** **+18.66%** (+INR 13.9M) among budget-conscious shoppers managing debt.

---

## 🎯 Core Features

### 1. Customer Risk & Loyalty Radar (Root Cause "Why" Diagnosis)
Instead of treating customer risk as an unexplained black-box label, the Radar diagnoses the exact root cause:
- **Electronics Diversion:** Flags big-ticket purchases drifting to competitor cards with terminal EMI deals.
- **Grocery & Daily Spend:** Identifies frequent supermarket shoppers using UPI rather than the co-branded card.
- **100% Card Loyalty Recognition:** Recognizes growing, loyal cardholders (e.g. Customer `#25555`) with a green **Loyalty & Retention Radar**, acknowledging **SoW Lift** instead of false churn warnings.

### 2. Next Best Offer (NBO) Engine ⭐
Translates diagnostic analytics into deterministic **IF / THEN** commercial action rules:
- **`IF Electronics Shifted to Rival Bank CC`** $\rightarrow$ *"Offer 10% cashback on Electronics for 30 days + 0% Instant POS EMI"*
- **`IF Frequent Grocery Shopper (>= 2 visits) AND SoW < 40%`** $\rightarrow$ *"Customer-level NBO: Extra 3% grocery cashback on all MetroMart purchases for 60 days"*
- **`IF MetroMart Stored Wallet Dominant Tender`** $\rightarrow$ *"Offer 2.5% instant auto-reload wallet bonus when funded via HSIC Card"*
- **`IF Displaced by UPI QR Phone Scanning`** $\rightarrow$ *"Issue Virtual RuPay Card on UPI with 1.5% scan-and-pay cashback"*
- **`IF 100% HSIC Loyalty AND Non-Prime Member`** $\rightarrow$ *"Complimentary 1-Year Prime Upgrade as Top Customer Loyalty Reward"*

> [!IMPORTANT]
> **Two-Tier Offer Architecture (Customer-Level NBO vs. Segment-Level Campaign):**
> - **Customer-level NBO $\rightarrow$ 3% cashback:** A personalized micro-incentive triggered for individual cardholders displaying early grocery tender diversion to protect program margin.
> - **Segment-level campaign $\rightarrow$ 5% cashback:** A promotional, portfolio-wide marketing push deployed across the broader "Grocery Heavy Users" cohort (6,814 accounts) to recapture top-of-wallet volume.

### 3. Early Warning Center (Watchlist)
- 🔴 **High Risk (1,245 customers):** Severe Silent Attrition (SoW drop > 40%)
- 🟡 **Watchlist (3,210 customers):** Emerging Risk & Tender Switching
- 🟢 **Healthy (40,000 customers):** Stable & Loyal Card Usage Habit

### 4. Segment Recovery Playbook ⭐
| Segment | Customers | Current SoW | Recommended Campaign | Expected Recovery | Strategy Tier |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Emerging Risk** | 4,565 | 9.47% | **10% Electronics Cashback** | **+3.2% SoW** | High-ticket POS EMI capture |
| **Grocery Heavy Users** | 6,814 | 12.40% | **Segment-level campaign: Extra 5% Grocery Cashback** *(vs 3% Customer-level NBO)* | **+4.8% SoW** | Portfolio-wide supermarket push |
| **Prime Users** | 3,921 | 48.89% | **Double Reward Week** | **+5.5% SoW** | High-margin loyalty defense |
| **Low Engagement** | 25,916 | 11.99% | **₹500 Welcome Back Bonus** | **+2.1% SoW** | Win-back activation tender |

### 5. 10% Recovery Scenario & Business Sizing
*(Note: Modeled as a conservative 10% recapture scenario, not a speculative prediction.)*
- **Total Wallet Opportunity:** **₹54.36M** historical baseline share gap
- **10% Recovery Scenario (Gross Spend Lift):** **₹5.44M** incremental annual card spend
- **Targeted Campaign Budget:** **₹850,000** (Cashback subsidies, wallet auto-reload bonus, tech enablement)
- **Net Incremental Financial Lift:** **₹4.59M** net profit lift
- **Return on Investment (ROI):** **5.2x Net ROI Multiple**

---

## 📂 Repository Structure

```text
Synchrony_Hackathon/
│
├── docs/                               # GitHub Pages Live Web Application
│   ├── index.html                      # Interactive 3-module dashboard
│   ├── style.css                       # Clean institutional styling
│   ├── app.js                          # Client-side analytics & lookup logic
│   └── api/                            # Static analytical JSON endpoints
│       ├── summary.json                # Macro portfolio KPIs
│       ├── monthly-sow.json            # 24-month spend trend
│       ├── categories.json             # 10 merchandise category breakdowns
│       ├── segments.json               # K-Means behavioral clustering
│       └── customers/                  # Sample customer 360 profiles
│
├── notebooks/
│   └── analysis.ipynb                  # 5-module end-to-end Jupyter analysis
│
├── src/
│   ├── data_cleaning.py                # Net sales, fiscal calendar & date imputation
│   ├── sow_calculation.py              # Share of Wallet & category leakage aggregation
│   ├── segmentation.py                 # K-Means clustering, Risk Radar & NBO rules
│   └── visualization.py               # Generates 4 clean presentation PNG charts
│
├── data_dictionary/
│   └── assumptions.txt                 # Business definitions & accounting assumptions
│
├── outputs/
│   ├── charts/                         # Exported high-res analytical charts
│   │   ├── 01_sow_monthly_trend.png
│   │   ├── 02_payment_channel_shift.png
│   │   ├── 03_customer_segments_opportunity.png
│   │   └── 04_customer_360_case_study.png
│   ├── customer_segments.csv           # 45,000 customers with cluster assignments
│   └── final_results.csv               # Complete profile with Risk Radar & NBO rules
│
├── requirements.txt                    # Minimal dependencies (pandas, scikit-learn, matplotlib)
└── README.md                           # Public documentation & interaction guide
```

---

## ⚡ Quickstart & How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Adityakasara/Synchrony_One.git
cd Synchrony_One
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline Scripts
```bash
# 1. Clean data & impute active windows
python src/data_cleaning.py

# 2. Compute customer Share of Wallet & category diversion
python src/sow_calculation.py

# 3. Perform segmentation & execute Next Best Offer engine
python src/segmentation.py

# 4. Generate visual charts
python src/visualization.py
```

### 4. Run the Jupyter Notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## 🔍 Featured Customer Profiles to Explore

Search these representative account IDs on the [Live Dashboard](https://adityakasara.github.io/Synchrony_One/):

| Account ID | Profile & Trend | Diagnosed Root Cause | Next Best Offer Triggered |
| :---: | :--- | :--- | :--- |
| **`#25555`** | Non-Prime, **+84.4 pp SoW Lift** (100% Loyalty) | 🟢 **Loyalty Radar:** 100% Co-Brand Capture | `IF 100% Loyalty AND Non-Prime` $\rightarrow$ **Complimentary 1-Yr Prime Upgrade** |
| **`#25790`** | Prime, **-100.0 pp SoW Drop** (Severe Attrition) | 🔴 **Risk Radar:** Shifted checkouts to Wallet | `IF Wallet Dominant` $\rightarrow$ **2.5% Auto-Reload Bonus on Card Top-Up** |
| **`#33822`** | Core Grocery Basket Migration (-35.2 pp) | 🔴 **Risk Radar:** Food baskets shifted to UPI | `IF Frequent Grocery Shopper` $\rightarrow$ **Customer-level NBO: Extra 3% Grocery Cashback for 60 Days** |
| **`#24664`** | Electronics Migration to Competitor Card | 🔴 **Risk Radar:** Shifted to rival credit card | `IF Electronics Shifted to Rival CC` $\rightarrow$ **10% Cashback + 0% Instant POS EMI** |
| **`#58218`** | Counter UPI QR Migration (-42.1 pp) | 🔴 **Risk Radar:** POS plastic card friction | `IF Displaced by UPI QR` $\rightarrow$ **Virtual RuPay Card on UPI (1.5% Scan&Pay)** |

---

 
- Developed for the **Synchrony Analytics Hackathon 2026**.
