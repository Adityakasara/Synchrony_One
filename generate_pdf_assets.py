"""
generate_pdf_assets.py
Generates clean, publication-grade charts tailored for the 5-page Executive Findings PDF.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import json

# Set clean aesthetic defaults
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#1E293B'
plt.rcParams['axes.labelcolor'] = '#475569'
plt.rcParams['xtick.color'] = '#64748B'
plt.rcParams['ytick.color'] = '#64748B'
plt.rcParams['axes.edgecolor'] = '#E2E8F0'
plt.rcParams['axes.linewidth'] = 0.8

CHARTS_DIR = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/outputs/pdf_assets"
os.makedirs(CHARTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# CHART 1: Page 1 Spend Growth Divergence (Contrast Bar)
# -------------------------------------------------------------
def create_chart_spend_divergence():
    fig, ax = plt.subplots(figsize=(7.2, 1.9), dpi=300)
    
    categories = ['MetroMart Net Sales\n(Total Retail Growth)', 'HSIC Co-Branded Card\n(Cardholder Spend)']
    values = [15.37, -19.55]
    colors = ['#16A34A', '#DC2626']
    
    x = [0.4, 1.2]
    bars = ax.bar(x, values, color=colors, width=0.45, zorder=3)
    ax.axhline(0, color='#94A3B8', linewidth=1.2, linestyle='-', zorder=2)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9, fontweight='bold', color='#1E293B')
    ax.set_xlim(-0.1, 1.7)
    ax.set_ylim(-30, 26)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0', zorder=1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='y', labelsize=8.5)
    
    # Value labels with clear breathing room
    ax.text(x[0], 15.37 + 1.8, "+15.37% YoY\n(INR 377.65M -> INR 435.69M)", ha='center', va='bottom',
            fontsize=8.5, fontweight='bold', color='#16A34A')
            
    ax.text(x[1], -19.55 - 1.8, "-19.55% YoY\n(INR 85.67M -> INR 68.92M)", ha='center', va='top',
            fontsize=8.5, fontweight='bold', color='#DC2626')
            
    fig.tight_layout()
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
        'Merchant Stored Wallet\n(+INR 22.2M net shift)',
        'Mobile UPI QR\n(+INR 18.4M net shift)',
        'Competitor Credit Cards\n(+INR 20.3M net shift)',
        'Debit Cards\n(+INR 13.9M net shift)',
        'HSIC Co-Branded Card\n(-INR 16.8M contraction)'
    ]
    rates = [38.96, 26.87, 22.04, 18.66, -19.55]
    colors = ['#0284C7', '#0284C7', '#0284C7', '#64748B', '#DC2626']
    
    y_pos = np.arange(len(tenders))
    bars = ax.barh(y_pos, rates, color=colors, height=0.55, zorder=3)
    ax.axvline(0, color='#94A3B8', linewidth=1, linestyle='-', zorder=2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tenders, fontsize=8.5, color='#1E293B')
    ax.invert_yaxis()
    
    ax.set_xlim(-28, 52)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.xaxis.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0', zorder=1)
    
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='x', labelsize=8.5)
    
    for bar, r in zip(bars, rates):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        if r > 0:
            ax.text(w + 1.2, y, f"+{r:.2f}%", va='center', ha='left', fontsize=8.5, fontweight='bold', color='#1E293B')
        else:
            ax.text(w - 1.2, y, f"{r:.2f}%", va='center', ha='right', fontsize=8.5, fontweight='bold', color='#DC2626')
            
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "p2_payment_migration.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 2B: Page 2 24-Month Monthly SoW Trend
# -------------------------------------------------------------
def create_chart_monthly_sow_trend():
    with open('/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/docs/api/monthly-sow.json') as fp:
        monthly_data = json.load(fp)
        
    dates = [m['Year_Month'] for m in monthly_data]
    sow = [m['HSIC_SoW_Pct'] for m in monthly_data]
    
    fig, ax = plt.subplots(figsize=(7.2, 2.5), dpi=300)
    
    x = np.arange(len(dates))
    ax.plot(x, sow, color='#DC2626', linewidth=2.2, marker='o', markersize=4, zorder=4, label='HSIC Share of Wallet (%)')
    ax.fill_between(x, sow, color='#FEE2E2', alpha=0.5, zorder=2)
    
    # FY divider
    ax.axvline(11.5, color='#64748B', linestyle='--', linewidth=1.2, zorder=3)
    ax.text(5.5, 27.5, "FY2025 (Average: 22.69%)", ha='center', fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.text(17.5, 27.5, "FY2026 (Average: 15.82%)", ha='center', fontsize=8.5, fontweight='bold', color='#DC2626')
    
    # Key callouts: Peak and Trough - adjusted so no overlap occurs
    peak_idx = 0
    trough_idx = len(sow) - 1
    ax.annotate(f"Peak: {sow[peak_idx]:.2f}%\n(Aug 2024)",
                xy=(peak_idx, sow[peak_idx]), xytext=(peak_idx + 1.2, sow[peak_idx] - 6.8),
                arrowprops=dict(arrowstyle='->', color='#1E293B', lw=1),
                fontsize=8, fontweight='bold', color='#1E293B')
    
    ax.annotate(f"Trough: {sow[trough_idx]:.2f}%\n(Jul 2026)",
                xy=(trough_idx, sow[trough_idx]), xytext=(trough_idx - 3.8, sow[trough_idx] + 2.8),
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1),
                fontsize=8, fontweight='bold', color='#DC2626')
    
    ax.set_ylim(8, 29.5)
    ax.set_xticks(x[::2])
    ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=0, fontsize=7.5)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis='both', labelsize=8)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0', zorder=1)
    
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "p2_monthly_sow_trend.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 3: Page 3 Customer Segment Opportunity Sizing
# -------------------------------------------------------------
def create_chart_segment_opportunity():
    fig, ax = plt.subplots(figsize=(7.2, 2.1), dpi=300)
    
    segments = ['Low Engagement\n(25,916 accts)', 'Grocery Heavy Users\n(6,814 accts)', 'Emerging Risk\n(4,565 accts)', 'Prime Users\n(3,921 accts)']
    opp_inr = [28.45, 12.18, 9.85, 3.88] # Total opportunity INR Millions
    colors = ['#94A3B8', '#0284C7', '#DC2626', '#16A34A']
    
    y_pos = np.arange(len(segments))
    bars = ax.barh(y_pos, opp_inr, color=colors, height=0.5, zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(segments, fontsize=8, color='#1E293B')
    ax.invert_yaxis()
    
    ax.set_xlim(0, 35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.xaxis.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0', zorder=1)
    
    ax.tick_params(axis='x', labelsize=8)
    ax.set_xlabel("Estimated Wallet Opportunity (INR Millions)", fontsize=8, color='#475569')
    
    for bar, val in zip(bars, opp_inr):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.text(w + 0.6, y, f"INR {val:.2f}M", va='center', ha='left', fontsize=8, fontweight='bold', color='#1E293B')
        
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "p3_segment_opportunity.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

# -------------------------------------------------------------
# CHART 5: Page 5 Illustrative Recovery Scenarios
# -------------------------------------------------------------
def create_chart_recovery_scenarios():
    fig, ax = plt.subplots(figsize=(7.2, 2.1), dpi=300)
    
    scenarios = ['5% Recapture\nScenario', '10% Base Case\nScenario', '15% Recapture\nScenario', '20% Recapture\nScenario']
    gross_spend = [2.72, 5.44, 8.15, 10.87] # in INR Millions
    net_roi = ["3.2x ROI", "5.2x ROI", "8.6x ROI", "11.8x ROI"]
    colors = ['#94A3B8', '#16A34A', '#0284C7', '#0F766E']
    
    x = np.arange(len(scenarios))
    bars = ax.bar(x, gross_spend, color=colors, width=0.46, zorder=3)
    
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=8, color='#1E293B')
    ax.set_ylim(0, 13)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.yaxis.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0', zorder=1)
    
    ax.set_ylabel("Gross Spend Recaptured (INR M)", fontsize=8, color='#475569')
    ax.tick_params(axis='both', labelsize=8)
    
    for bar, val, roi in zip(bars, gross_spend, net_roi):
        h = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        ax.text(x_pos, h + 0.35, f"INR {val:.2f}M", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1E293B')
        ax.text(x_pos, h / 2, roi, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "p5_recovery_scenarios.png")
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created:", path)

if __name__ == "__main__":
    create_chart_spend_divergence()
    create_chart_payment_migration()
    create_chart_monthly_sow_trend()
    create_chart_segment_opportunity()
    create_chart_recovery_scenarios()
    print("Updated all charts successfully.")
