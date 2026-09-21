"""
Module 2: Share of Wallet (SoW) Calculation & Tender Migration Analysis
Synchrony Hackathon 2026 - Customer & Credit Card Analytics

Functions:
- compute_monthly_sow: 24-month portfolio net spend and HSIC SoW trend.
- compute_payment_method_migration: Tender substitution analysis (FY25 vs FY26).
- compute_customer_sow: Customer-level baseline vs actual SoW and Wallet Opportunity.
"""

import pandas as pd
import numpy as np

def compute_monthly_sow(df_tx):
    """
    Computes portfolio-level Share of Wallet across 24 months (Aug 2024 to Jul 2026).
    Formula: Monthly SoW % = (HSIC Net Spend / Total MetroMart Net Spend) * 100
    """
    monthly = df_tx.groupby("Year_Month").agg(
        Total_MetroMart_Net_Spend=("Net_Sales", "sum"),
        HSIC_Net_Spend=("Net_Sales", lambda s: s[df_tx.loc[s.index, "Payment_Code"] == "1"].sum()),
        Total_Transactions=("Transaction_Amount", "count")
    ).reset_index()

    monthly["HSIC_SoW_Pct"] = (monthly["HSIC_Net_Spend"] / monthly["Total_MetroMart_Net_Spend"] * 100).round(2)
    return monthly

def compute_payment_method_migration(df_tx):
    """
    Computes YoY spend and mix shift across the 5 payment methods.
    Shows the tender diversion from HSIC Credit Card to Wallet, UPI, and Rival Bank Cards.
    """
    tender_summary = df_tx.groupby(["Payment_Method", "Fiscal_Year"])["Net_Sales"].sum().unstack().fillna(0)
    tender_summary = tender_summary[["FY25", "FY26"]]

    tender_summary["YoY_Growth_Pct"] = (
        (tender_summary["FY26"] - tender_summary["FY25"]) / tender_summary["FY25"] * 100
    ).round(2)

    total_fy25 = tender_summary["FY25"].sum()
    total_fy26 = tender_summary["FY26"].sum()

    tender_summary["FY25_Mix_Pct"] = (tender_summary["FY25"] / total_fy25 * 100).round(2)
    tender_summary["FY26_Mix_Pct"] = (tender_summary["FY26"] / total_fy26 * 100).round(2)
    tender_summary["Mix_Delta_pp"] = (tender_summary["FY26_Mix_Pct"] - tender_summary["FY25_Mix_Pct"]).round(2)

    return tender_summary.reset_index()

def compute_customer_sow(df_customers, df_tx):
    """
    Computes customer-level FY25 and FY26 metrics:
    - Total MetroMart Spend (FY25, FY26)
    - HSIC Card Spend (FY25, FY26)
    - HSIC Share of Wallet % (FY25, FY26)
    - SoW Change (percentage points)
    - Alternative Payment Method Spend (Wallet, UPI, Rival CC, Debit)
    - Dominant Alternative Payment Method
    - Wallet Opportunity (Historical Share Gap Recovery)
    """
    # Active Window Filter: strictly evaluate HSIC spend during active card window
    active_tx = df_tx[df_tx["Is_Card_Active"]].copy()

    # Pivot customer spending by payment method and fiscal year
    pivot_pay = active_tx.pivot_table(
        index="Customer_ID",
        columns=["Fiscal_Year", "Payment_Method"],
        values="Net_Sales",
        aggfunc="sum",
        fill_value=0
    )
    pivot_pay.columns = [f"{fy}_{pm.replace(' ', '_').replace('/', '_')}_Spend" for fy, pm in pivot_pay.columns]
    pivot_pay.reset_index(inplace=True)

    # Aggregate Total & HSIC spend by Fiscal Year
    cust_agg = active_tx.groupby(["Customer_ID", "Fiscal_Year"]).agg(
        Total_Spend=("Net_Sales", "sum"),
        HSIC_Spend=("Net_Sales", lambda s: s[active_tx.loc[s.index, "Payment_Code"] == "1"].sum()),
        Tx_Count=("Net_Sales", "count")
    ).unstack().fillna(0)

    # Flatten column multi-index
    df_metrics = pd.DataFrame(index=cust_agg.index)
    df_metrics["FY25_Total_Spend"] = cust_agg[("Total_Spend", "FY25")]
    df_metrics["FY26_Total_Spend"] = cust_agg[("Total_Spend", "FY26")]
    df_metrics["FY25_HSIC_Spend"] = cust_agg[("HSIC_Spend", "FY25")]
    df_metrics["FY26_HSIC_Spend"] = cust_agg[("HSIC_Spend", "FY26")]
    df_metrics.reset_index(inplace=True)

    # Merge customer base demographics
    df_metrics = df_customers.merge(df_metrics, on="Customer_ID", how="left").fillna(0)
    df_metrics = df_metrics.merge(pivot_pay, on="Customer_ID", how="left").fillna(0)

    # Compute SoW %
    df_metrics["FY25_HSIC_SoW"] = np.where(
        df_metrics["FY25_Total_Spend"] > 0,
        (df_metrics["FY25_HSIC_Spend"] / df_metrics["FY25_Total_Spend"] * 100).clip(0, 100),
        0.0
    ).round(2)

    df_metrics["FY26_HSIC_SoW"] = np.where(
        df_metrics["FY26_Total_Spend"] > 0,
        (df_metrics["FY26_HSIC_Spend"] / df_metrics["FY26_Total_Spend"] * 100).clip(0, 100),
        0.0
    ).round(2)

    df_metrics["SoW_Change_pp"] = (df_metrics["FY26_HSIC_SoW"] - df_metrics["FY25_HSIC_SoW"]).round(2)
    df_metrics["Total_Spend_Growth_Pct"] = np.where(
        df_metrics["FY25_Total_Spend"] > 0,
        ((df_metrics["FY26_Total_Spend"] - df_metrics["FY25_Total_Spend"]) / df_metrics["FY25_Total_Spend"] * 100),
        0.0
    ).round(2)

    # Alternative spend in FY26
    df_metrics["FY26_Wallet_Spend"] = df_metrics.get("FY26_MetroMart_Wallet_Spend", 0)
    df_metrics["FY26_UPI_Spend"] = df_metrics.get("FY26_Cash___UPI_Spend", 0)
    df_metrics["FY26_Other_CC_Spend"] = df_metrics.get("FY26_Other_Bank_Credit_Card_Spend", 0)
    df_metrics["FY26_Debit_Spend"] = df_metrics.get("FY26_Debit_Card_Spend", 0)

    df_metrics["FY26_Alternative_Spend"] = (
        df_metrics["FY26_Wallet_Spend"] +
        df_metrics["FY26_UPI_Spend"] +
        df_metrics["FY26_Other_CC_Spend"] +
        df_metrics["FY26_Debit_Spend"]
    )

    # Determine Dominant Alternative Payment Method
    alt_cols = {
        "MetroMart Wallet": df_metrics["FY26_Wallet_Spend"],
        "Cash/UPI": df_metrics["FY26_UPI_Spend"],
        "Other Bank Credit Card": df_metrics["FY26_Other_CC_Spend"],
        "Debit Card": df_metrics["FY26_Debit_Spend"]
    }
    df_alt = pd.DataFrame(alt_cols)
    df_metrics["Dominant_Alternative_Method"] = df_alt.idxmax(axis=1)
    df_metrics.loc[df_metrics["FY26_Alternative_Spend"] <= 0, "Dominant_Alternative_Method"] = "None (HSIC Only)"

    # Wallet Opportunity Sizing Formula (Historical Share-of-Wallet Baseline Gap)
    # Expected_FY26_HSIC_Spend = FY26_Total_Spend * (FY25_HSIC_SoW / 100)
    # Wallet_Opportunity = max(0, Expected_FY26_HSIC_Spend - FY26_HSIC_Spend)
    expected_spend = df_metrics["FY26_Total_Spend"] * (df_metrics["FY25_HSIC_SoW"] / 100.0)
    df_metrics["Wallet_Opportunity"] = (expected_spend - df_metrics["FY26_HSIC_Spend"]).clip(lower=0.0).round(2)

    # -------------------------------------------------------------
    # Customer Risk Radar & NBO Features: Top Diverted Category & Grocery Frequency
    # -------------------------------------------------------------
    fy26_alt_tx = active_tx[(active_tx["Fiscal_Year"] == "FY26") & (active_tx["Payment_Code"] != "1")].copy()
    if not fy26_alt_tx.empty:
        cat_agg = fy26_alt_tx.groupby(["Customer_ID", "Category_Name"])["Net_Sales"].sum().reset_index()
        idx_max = cat_agg.groupby("Customer_ID")["Net_Sales"].idxmax()
        top_cat_df = cat_agg.loc[idx_max, ["Customer_ID", "Category_Name", "Net_Sales"]]
        top_cat_df.rename(columns={"Category_Name": "Top_Diverted_Category", "Net_Sales": "Top_Category_Diverted_Spend"}, inplace=True)
        df_metrics = df_metrics.merge(top_cat_df, on="Customer_ID", how="left")
    
    if "Top_Diverted_Category" not in df_metrics.columns:
        df_metrics["Top_Diverted_Category"] = "General Merchandise"
        df_metrics["Top_Category_Diverted_Spend"] = 0.0
    else:
        df_metrics["Top_Diverted_Category"] = df_metrics["Top_Diverted_Category"].fillna("General Merchandise")
        df_metrics["Top_Category_Diverted_Spend"] = df_metrics["Top_Category_Diverted_Spend"].fillna(0.0)

    # Frequency of Grocery purchases in FY26
    grocery_tx = active_tx[(active_tx["Fiscal_Year"] == "FY26") & (active_tx["Category_Name"].astype(str).str.lower().str.contains("grocer"))]
    groc_freq = grocery_tx.groupby("Customer_ID")["Transaction_ID"].count().reset_index()
    groc_freq.rename(columns={"Transaction_ID": "FY26_Grocery_Tx_Count"}, inplace=True)
    df_metrics = df_metrics.merge(groc_freq, on="Customer_ID", how="left")
    df_metrics["FY26_Grocery_Tx_Count"] = df_metrics["FY26_Grocery_Tx_Count"].fillna(0).astype(int)

    print("Customer SoW, Wallet Opportunity, and Diverted Category metrics computed.")
    print(f"Total Portfolio Wallet Opportunity: INR {df_metrics['Wallet_Opportunity'].sum():,.2f}")
    return df_metrics

if __name__ == "__main__":
    from data_cleaning import clean_and_prepare_data
    df_customers, df_tx = clean_and_prepare_data()
    monthly = compute_monthly_sow(df_tx)
    migration = compute_payment_method_migration(df_tx)
    cust_sow = compute_customer_sow(df_customers, df_tx)
