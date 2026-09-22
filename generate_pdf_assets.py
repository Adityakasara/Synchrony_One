"""
generate_pdf_assets.py
Generates clean, publication-grade charts tailored for the 5-page Executive Findings PDF.
Uses DejaVu Sans for native Unicode support (₹, →, −).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Set clean aesthetic defaults with DejaVu Sans
plt.rcParams['font.sans-serif'] = 'DejaVu Sans, Arial, Helvetica'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#0F172A'
plt.rcParams['axes.labelcolor'] = '#475569'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

CHARTS_DIR = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/outputs/pdf_assets"
os.makedirs(CHARTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# CHART 1: Page 1 Spend Growth Divergence (Contrast Bar)
# -------------------------------------------------------------
def create_chart_spend_divergence():
    fig, ax = plt.subplots(figsize=(7.2, 2.2), dpi=300)
    
    categories = ['MetroMart Net Sales\n(Total Retail Growth)', 'HSIC Co-Branded Card\n(Cardholder Spend)']
    values = [15.37, -19.55]
    colors = ['#16A34A', '#DC2626']
    
    x = [0.4, 1.2]
    bars = ax.bar(x, values, color=colors, width=0.42, zorder=3)
    ax.axhline(0, color='#64748B', linewidth=1.2, linestyle='-', zorder=2)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.set_xlim(-0.1, 1.7)
    ax.set_ylim(-32, 28)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='y', labelsize=9)
    
    ax.text(x[0], 15.37 + 1.8, "+15.37% YoY\n(₹377.65M → ₹435.69M)", ha='center', va='bottom',
            fontsize=9.5, fontweight='bold', color='#16A34A')
            
    ax.text(x[1], -19.55 - 2.0, "−19.55% YoY\n(₹85.67M → ₹68.92M)", ha='center', va='top',
            fontsize=9.5, fontweight='bold', color='#DC2626')
            
    fig.tight_layout(pad=1.2)
    path = os.path.join(CHARTS_DIR, "p1_spend_divergence.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 2A: Page 2 Payment Tender Growth & Monetary Migration
# -------------------------------------------------------------
def create_chart_payment_migration():
    fig, ax = plt.subplots(figsize=(7.2, 2.7), dpi=300)
    
    tenders = [
        'Merchant Stored Wallet (+₹22.2M)',
        'Mobile UPI QR (+₹18.4M)',
        'Competitor Credit Cards (+₹20.3M)',
        'Debit Cards (+₹13.9M)',
        'HSIC Co-Branded Card (−₹16.8M)'
    ]
    rates = [38.96, 26.87, 22.04, 18.66, -19.55]
    colors = ['#0284C7', '#0284C7', '#0284C7', '#64748B', '#DC2626']
    
    y_pos = np.arange(len(tenders))
    bars = ax.barh(y_pos, rates, color=colors, height=0.55, zorder=3)
    ax.axvline(0, color='#64748B', linewidth=1.2, linestyle='-', zorder=2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tenders, fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.invert_yaxis()
    
    ax.set_xlim(-36, 54)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.xaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='x', labelsize=9)
    
    for bar, r in zip(bars, rates):
        w = bar.get_width()
        if w > 0:
            ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"+{r:.2f}%",
                    va='center', ha='left', fontsize=9.5, fontweight='bold', color='#0F172A')
        else:
            ax.text(w - 1.5, bar.get_y() + bar.get_height()/2, f"−{abs(r):.2f}%",
                    va='center', ha='right', fontsize=9.5, fontweight='bold', color='#DC2626')
                    
    fig.tight_layout(pad=1.2)
    path = os.path.join(CHARTS_DIR, "p2_payment_migration.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 2B: Page 2 24-Month Share of Wallet Trajectory
# -------------------------------------------------------------
def create_chart_monthly_sow():
    fig, ax = plt.subplots(figsize=(7.2, 2.7), dpi=300)
    
    months = [
        '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
        '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
        '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12',
        '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07'
    ]
    sow_pct = [
        26.60, 24.80, 24.50, 23.90, 24.70,
        24.10, 24.80, 23.20, 23.60, 23.10, 21.80,
        20.50, 20.30, 20.60, 18.20, 18.90, 18.10,
        17.60, 17.50, 16.80, 16.20, 15.10, 14.30, 12.01
    ]
    x_idx = np.arange(len(months))
    
    ax.fill_between(x_idx, sow_pct, color='#FEE2E2', alpha=0.55, zorder=2)
    ax.plot(x_idx, sow_pct, color='#DC2626', linewidth=2.4, marker='o', markersize=4.5,
            markerfacecolor='#DC2626', markeredgecolor='white', markeredgewidth=1, zorder=3)
            
    ax.axvline(x=11.5, color='#475569', linestyle='--', linewidth=1.2, alpha=0.7, zorder=2)
    ax.text(5.5, 27.2, "FY2025 Average: 22.69%", ha='center', va='center',
            fontsize=9, fontweight='bold', color='#475569',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#E2E8F0', alpha=0.9))
            
    ax.text(17.5, 27.2, "FY2026 Average: 15.82%", ha='center', va='center',
            fontsize=9, fontweight='bold', color='#DC2626',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#FECACA', alpha=0.9))
            
    ax.annotate("Peak: 26.60%\n(Aug 2024)", xy=(0, 26.60), xytext=(2.2, 23.0),
                arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.2),
                fontsize=8.5, fontweight='bold', color='#0F172A', ha='left',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#CBD5E1', alpha=0.95))
                
    ax.annotate("Trough: 12.01%\n(Jul 2026)", xy=(23, 12.01), xytext=(19.0, 15.2),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.2),
                fontsize=8.5, fontweight='bold', color='#DC2626', ha='center',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#FCA5A5', alpha=0.95))
                
    ax.set_ylim(8, 30)
    ax.set_xlim(-0.5, 23.5)
    
    tick_pos = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    tick_labels = [months[i] for i in tick_pos]
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_labels, fontsize=8.5, color='#475569', rotation=0)
    
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='y', labelsize=9)
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    
    fig.tight_layout(pad=1.2)
    path = os.path.join(CHARTS_DIR, "p2_monthly_sow_trend.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 3: Page 3 Customer Segment Wallet Opportunity Sizing
# -------------------------------------------------------------
def create_chart_segment_opportunity():
    fig, ax = plt.subplots(figsize=(7.2, 2.5), dpi=300)
    
    segments = [
        'Prime Users\n(3,921 accts)',
        'Emerging Risk\n(4,565 accts)',
        'Grocery Heavy Users\n(6,814 accts)',
        'Low Engagement\n(25,916 accts)'
    ]
    opps = [3.88, 9.85, 12.18, 28.45]
    colors = ['#16A34A', '#DC2626', '#0284C7', '#64748B']
    
    y_pos = np.arange(len(segments))
    bars = ax.barh(y_pos, opps, color=colors, height=0.55, zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(segments, fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.set_xlim(0, 36)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.xaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    
    ax.set_xlabel("Estimated Addressable Wallet Opportunity (₹ Millions)", fontsize=9.5, fontweight='bold', color='#475569')
    ax.tick_params(axis='x', labelsize=9)
    
    for bar, val in zip(bars, opps):
        w = bar.get_width()
        ax.text(w + 0.6, bar.get_y() + bar.get_height()/2, f"₹{val:.2f}M",
                va='center', ha='left', fontsize=9.5, fontweight='bold', color='#0F172A')
                
    fig.tight_layout(pad=1.2)
    path = os.path.join(CHARTS_DIR, "p3_segment_opportunity.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 5: Page 5 Illustrative Recovery Scenarios
# -------------------------------------------------------------
def create_chart_recovery_scenarios():
    fig, ax = plt.subplots(figsize=(7.2, 2.5), dpi=300)
    
    scenarios = ['5% Recapture\nScenario', '10% Base Case\nScenario', '15% Recapture\nScenario', '20% Recapture\nScenario']
    gross_spend = [2.72, 5.44, 8.15, 10.87]
    roi_labels = ['3.2x ROI', '5.2x ROI\n(Base Case)', '8.6x ROI', '11.8x ROI']
    colors = ['#64748B', '#16A34A', '#0284C7', '#0F766E']
    
    x = np.arange(len(scenarios))
    bars = ax.bar(x, gross_spend, color=colors, width=0.48, zorder=3)
    
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.set_ylabel("Recaptured Spend (₹ Millions)", fontsize=9.5, fontweight='bold', color='#475569')
    ax.set_ylim(0, 14)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    ax.tick_params(axis='y', labelsize=9)
    
    for bar, val, roi in zip(bars, gross_spend, roi_labels):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.4, f"₹{val:.2f}M",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')
        ax.text(bar.get_x() + bar.get_width()/2, h / 2, roi,
                ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
                
    fig.tight_layout(pad=1.5)
    path = os.path.join(CHARTS_DIR, "p5_recovery_scenarios.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

if __name__ == "__main__":
    create_chart_spend_divergence()
    create_chart_payment_migration()
    create_chart_monthly_sow()
    create_chart_segment_opportunity()
    create_chart_recovery_scenarios()
    print("All chart assets successfully generated.")
