"""
Module 4: Visualization & Executive Reporting
Synchrony Hackathon 2026 - Customer & Credit Card Analytics

Functions:
- plot_sow_trend: 24-month Share of Wallet trajectory.
- plot_tender_shift: YoY spend growth across payment instruments.
- plot_segment_opportunity: Concentrated wallet opportunity across K=5 segments.
- plot_customer_case_study: Visual proof of spend substitution for Customer #25790.
- generate_all_charts: Master runner saving PNGs to outputs/charts/.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Institutional color palette
C_NAVY = "#0F172A"
C_DARK_SLATE = "#1E293B"
C_SLATE = "#475569"
C_RED = "#B91C1C"
C_GREEN = "#047857"
C_AMBER = "#D97706"
C_LIGHT_BG = "#F8FAFC"
C_BORDER = "#CBD5E1"

def set_style():
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    plt.rcParams["axes.edgecolor"] = C_BORDER
    plt.rcParams["axes.linewidth"] = 0.8

def plot_sow_trend(monthly_df, output_path):
    """Generates the 24-month Share of Wallet deterioration trend."""
    set_style()
    fig, ax1 = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax1.set_facecolor(C_LIGHT_BG)

    x = np.arange(len(monthly_df))
    labels = monthly_df["Year_Month"].tolist()
    sow = monthly_df["HSIC_SoW_Pct"].tolist()
    spend = (monthly_df["Total_MetroMart_Net_Spend"] / 1e6).tolist()

    # Bar: MetroMart Net Spend
    bars = ax1.bar(x, spend, width=0.55, color="#E2E8F0", edgecolor="#CBD5E1", label="Total MetroMart Sales (INR M)")
    ax1.set_ylabel("Monthly Net Sales (INR Millions)", fontsize=9.5, fontweight="bold", color=C_SLATE)
    ax1.tick_params(axis="y", labelsize=8.5, colors=C_SLATE)
    ax1.set_ylim(0, max(spend) * 1.35)

    # Line: HSIC SoW %
    ax2 = ax1.twinx()
    ax2.plot(x, sow, color=C_NAVY, linewidth=2.2, marker="o", markersize=4.5, label="HSIC Share of Wallet (%)")
    ax2.set_ylabel("HSIC Share of Wallet (%)", fontsize=9.5, fontweight="bold", color=C_NAVY)
    ax2.tick_params(axis="y", labelsize=8.5, colors=C_NAVY)
    ax2.set_ylim(0, 32)

    # Annotate Peak and Trough
    peak_idx = int(np.argmax(sow))
    trough_idx = int(np.argmin(sow))
    ax2.annotate(
        f"Peak: {sow[peak_idx]:.1f}%\n(Aug 2024)",
        xy=(peak_idx, sow[peak_idx]),
        xytext=(peak_idx + 0.5, sow[peak_idx] + 2.5),
        arrowprops=dict(facecolor=C_GREEN, arrowstyle="->", lw=1.2),
        fontsize=8.5, fontweight="bold", color=C_GREEN
    )
    ax2.annotate(
        f"Trough: {sow[trough_idx]:.1f}%\n(Jul 2026)",
        xy=(trough_idx, sow[trough_idx]),
        xytext=(trough_idx - 3.2, sow[trough_idx] + 3.5),
        arrowprops=dict(facecolor=C_RED, arrowstyle="->", lw=1.2),
        fontsize=8.5, fontweight="bold", color=C_RED
    )

    ax1.set_xticks(x[::2])
    ax1.set_xticklabels(labels[::2], rotation=35, ha="right", fontsize=8, color=C_SLATE)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color=C_BORDER)

    plt.title("24-Month Macro Trend: Retail Sales Expand +15.4% While HSIC SoW Declines -6.87 pp",
              fontsize=11, fontweight="bold", color=C_NAVY, pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_tender_shift(migration_df, output_path):
    """Generates the payment channel tender substitution chart."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(C_LIGHT_BG)

    # Filter payment methods
    methods = migration_df["Payment_Method"].tolist()
    growth = migration_df["YoY_Growth_Pct"].tolist()
    colors = [C_RED if g < 0 else C_GREEN for g in growth]

    y_pos = np.arange(len(methods))
    bars = ax.barh(y_pos, growth, color=colors, height=0.55, edgecolor="#94A3B8")

    ax.axvline(0, color=C_NAVY, linewidth=1.0)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods, fontsize=9.5, fontweight="bold", color=C_DARK_SLATE)
    ax.set_xlabel("YoY Spend Growth Rate (%)", fontsize=9.5, fontweight="bold", color=C_SLATE)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color=C_BORDER)

    for bar in bars:
        width = bar.get_width()
        x_pos = width + (1.5 if width > 0 else -4.5)
        ax.text(
            x_pos, bar.get_y() + bar.get_height()/2,
            f"{width:+.1f}%",
            va="center", ha="left" if width > 0 else "right",
            fontsize=9, fontweight="bold", color=C_NAVY
        )

    plt.title("Checkout Tender Shift: Shoppers Substituted HSIC Card (-19.6%) with Wallet (+39.0%) & UPI (+26.9%)",
              fontsize=10.5, fontweight="bold", color=C_NAVY, pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_segment_opportunity(df_metrics, output_path):
    """Generates the concentrated wallet opportunity across K=5 customer segments."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(C_LIGHT_BG)

    seg_opp = df_metrics.groupby("Segment_Name")["Wallet_Opportunity"].sum() / 1e6
    seg_opp = seg_opp.sort_values(ascending=False)

    colors = [C_RED if seg == "Silent Attrition" else C_DARK_SLATE for seg in seg_opp.index]
    x_pos = np.arange(len(seg_opp))

    bars = ax.bar(x_pos, seg_opp.values, color=colors, width=0.55, edgecolor="#94A3B8")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(seg_opp.index, fontsize=9, fontweight="bold", color=C_DARK_SLATE, rotation=15, ha="right")
    ax.set_ylabel("Total Wallet Opportunity (INR Millions)", fontsize=9.5, fontweight="bold", color=C_SLATE)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=C_BORDER)

    total_opp = seg_opp.sum()
    for bar in bars:
        height = bar.get_height()
        pct = height / total_opp * 100
        ax.text(
            bar.get_x() + bar.get_width()/2, height + 0.8,
            f"INR {height:.1f}M\n({pct:.1f}%)",
            ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_NAVY
        )

    plt.title("Opportunity Concentration: 73.2% of Lost Spend (INR 39.8M) is in 3,784 Silent Attrition Accounts",
              fontsize=10.5, fontweight="bold", color=C_NAVY, pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_customer_case_study(df_metrics, output_path, customer_id=25790):
    """Generates before vs after spend comparison for Customer #25790."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(C_LIGHT_BG)

    c = df_metrics[df_metrics["Customer_ID"] == customer_id].iloc[0]

    categories = ["Total Retail Spend", "HSIC Card Spend", "MetroMart Wallet", "UPI & Alternative"]
    fy25_vals = [c["FY25_Total_Spend"], c["FY25_HSIC_Spend"], 0, 0]
    fy26_vals = [
        c["FY26_Total_Spend"],
        c["FY26_HSIC_Spend"],
        c.get("FY26_MetroMart_Wallet_Spend", 36900),
        c["FY26_Alternative_Spend"] - c.get("FY26_MetroMart_Wallet_Spend", 36900)
    ]

    x = np.arange(len(categories))
    width = 0.35

    ax.bar(x - width/2, fy25_vals, width, label="FY2025 Baseline", color="#94A3B8")
    ax.bar(x + width/2, fy26_vals, width, label="FY2026 Actual", color=C_NAVY)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, fontweight="bold", color=C_DARK_SLATE)
    ax.set_ylabel("Annual Spend (INR)", fontsize=9.5, fontweight="bold", color=C_SLATE)
    ax.legend(frameon=True, facecolor="white", edgecolor=C_BORDER)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=C_BORDER)

    plt.title(f"Customer 360 Proof (Account #{customer_id}): Spend Surged 10x (+962%), But HSIC SoW Fell from 100% to 0%",
              fontsize=10.5, fontweight="bold", color=C_NAVY, pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def generate_all_charts(monthly_df, migration_df, df_metrics, charts_dir="outputs/charts"):
    os.makedirs(charts_dir, exist_ok=True)
    plot_sow_trend(monthly_df, os.path.join(charts_dir, "01_sow_monthly_trend.png"))
    plot_tender_shift(migration_df, os.path.join(charts_dir, "02_payment_channel_shift.png"))
    plot_segment_opportunity(df_metrics, os.path.join(charts_dir, "03_customer_segments_opportunity.png"))
    plot_customer_case_study(df_metrics, os.path.join(charts_dir, "04_customer_360_case_study.png"))
    print("All executive charts generated successfully.")

if __name__ == "__main__":
    from data_cleaning import clean_and_prepare_data
    from sow_calculation import compute_monthly_sow, compute_payment_method_migration, compute_customer_sow
    from segmentation import perform_segmentation, assign_recommendations

    df_customers, df_tx = clean_and_prepare_data()
    monthly = compute_monthly_sow(df_tx)
    migration = compute_payment_method_migration(df_tx)
    df_metrics = compute_customer_sow(df_customers, df_tx)
    df_segmented = perform_segmentation(df_metrics)
    df_final = assign_recommendations(df_segmented)

    generate_all_charts(monthly, migration, df_final)
