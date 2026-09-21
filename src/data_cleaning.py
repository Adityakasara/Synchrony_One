"""
Module 1: Data Cleaning & Preprocessing
Synchrony Hackathon 2026 - Customer & Credit Card Analytics

Functions:
- load_datasets: Load the 4 primary CSV datasets.
- clean_and_prepare_data: Clean dates, calculate net sales (Purchases - Returns),
  apply active card windowing, and merge human-readable labels.
"""

import os
import pandas as pd
import numpy as np

def load_datasets(data_dir="data"):
    """Loads the four given datasets from data_dir or adjacent search paths."""
    search_paths = [
        data_dir,
        os.path.join(os.path.dirname(__file__), "..", "data"),
        os.path.join(os.path.dirname(__file__), "..", "..", "data"),
        os.path.join(os.path.dirname(__file__), "..", "..", "hsic-solution", "data"),
        "../data",
        "data"
    ]
    resolved_dir = None
    for p in search_paths:
        if os.path.exists(os.path.join(p, "Customer Data.csv")):
            resolved_dir = p
            break
    if not resolved_dir:
        resolved_dir = data_dir

    customers_path = os.path.join(resolved_dir, "Customer Data.csv")
    transactions_path = os.path.join(resolved_dir, "Transactions Data.csv")
    categories_path = os.path.join(resolved_dir, "Category Code.csv")
    payments_path = os.path.join(resolved_dir, "Payment Code.csv")

    df_customers = pd.read_csv(customers_path)
    df_transactions = pd.read_csv(transactions_path)
    df_categories = pd.read_csv(categories_path)
    df_payments = pd.read_csv(payments_path)

    print(f"Loaded {len(df_customers):,} customers from '{resolved_dir}'.")
    print(f"Loaded {len(df_transactions):,} transactions.")
    return df_customers, df_transactions, df_categories, df_payments

def clean_and_prepare_data(data_dir="data"):
    """
    Cleans raw transactions and customers:
    1. Parse transaction and open dates.
    2. Map MetroMart Fiscal Years:
       - FY2025: 2024-08-01 to 2025-07-31
       - FY2026: 2025-08-01 to 2026-07-31
    3. Accounting: Net Sales = Gross Purchases - Returns.
       Returns contribute zero effective transaction count.
    4. Active Card Windowing:
       Identifies whether the HSIC card was active at transaction time.
       If Credit_Card_Open_Date is missing, imputes baseline as the first observed transaction.
    5. Merges Category and Payment Code descriptions.
    """
    df_customers, df_tx, df_cat, df_pay = load_datasets(data_dir)

    # Standardize column types & parse dates
    df_tx["Transaction_Date"] = pd.to_datetime(df_tx["Transaction_Date"])
    df_customers["Credit_Card_Open_Date"] = pd.to_datetime(df_customers["Credit_Card_Open_Date"])
    df_customers["Prime_Flag"] = (df_customers["Membership_Type"].str.strip().str.lower() == "prime").astype(int)

    # Map Fiscal Year
    df_tx["Fiscal_Year"] = np.where(
        df_tx["Transaction_Date"] >= "2025-08-01", "FY26", "FY25"
    )
    df_tx["Year_Month"] = df_tx["Transaction_Date"].dt.strftime("%Y-%m")

    # Net Sales Formulation (Accounting Standard)
    df_tx["Net_Sales"] = np.where(
        df_tx["Transaction_Type"].astype(str).str.strip().str.lower() == "return",
        -df_tx["Transaction_Amount"].abs(),
        df_tx["Transaction_Amount"].abs()
    )

    # Merge Customer fields to establish Active Window
    df_tx = df_tx.merge(
        df_customers[["Customer_ID", "Credit_Card_Open_Date", "Prime_Flag", "Credit_Card_Limit", "Credit_Card_APR"]],
        on="Customer_ID",
        how="left"
    )

    # Impute missing Open_Date as first transaction date (Version B baseline)
    first_tx = df_tx.groupby("Customer_ID")["Transaction_Date"].min().reset_index()
    first_tx.rename(columns={"Transaction_Date": "First_Tx_Date"}, inplace=True)
    df_tx = df_tx.merge(first_tx, on="Customer_ID", how="left")

    df_tx["Effective_Open_Date"] = df_tx["Credit_Card_Open_Date"].fillna(df_tx["First_Tx_Date"])
    df_tx["Is_Card_Active"] = df_tx["Transaction_Date"] >= df_tx["Effective_Open_Date"]

    # Merge Category and Payment Names
    df_tx["Category_Code"] = df_tx["Category_Code"].astype(str).str.strip()
    df_cat["Category_Code"] = df_cat["Category_Code"].astype(str).str.strip()
    df_tx = df_tx.merge(df_cat, on="Category_Code", how="left")
    df_tx["Category_Name"] = df_tx["Category"].fillna("General Merchandise")

    df_tx["Payment_Code"] = df_tx["Payment_Code"].astype(str).str.strip()
    df_pay["Payment_Code"] = df_pay["Payment_Code"].astype(str).str.strip()
    df_tx = df_tx.merge(df_pay, on="Payment_Code", how="left")

    payment_map = {
        "1": "HSIC Bank Credit Card",
        "2": "Other Bank Credit Card",
        "3": "Debit Card",
        "4": "Cash / UPI",
        "5": "MetroMart Wallet"
    }
    df_tx["Payment_Method"] = df_tx["Payment_Code"].map(payment_map).fillna("Other")

    print("Data cleaning completed successfully.")
    print(f"Net Sales Portfolio Total: INR {df_tx['Net_Sales'].sum():,.2f}")
    return df_customers, df_tx

if __name__ == "__main__":
    df_customers, df_tx = clean_and_prepare_data()
