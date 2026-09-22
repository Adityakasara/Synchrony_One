"""
build_findings_pdf.py
Generates the complete 5-Page Executive Analysis & Findings PDF for Synchrony Analytics Hackathon 2026.
Strictly follows humanised consulting style, no repeated headers/footers, no URLs, 75-90% visual coverage.
"""

import os
import matplotlib
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -------------------------------------------------------------
# Font Registration (DejaVu Sans for native ₹, →, − support)
# -------------------------------------------------------------
mpl_ttf_dir = os.path.join(matplotlib.get_data_path(), 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(mpl_ttf_dir, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(mpl_ttf_dir, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', os.path.join(mpl_ttf_dir, 'DejaVuSans-Oblique.ttf')))

# Color Palette
C_NAVY_DARK = colors.HexColor("#0F172A")    # Primary titles / dark text
C_SLATE = colors.HexColor("#334155")        # Body text
C_MUTED = colors.HexColor("#64748B")        # Subtext / labels
C_LIGHT_BG = colors.HexColor("#F8FAFC")     # Card neutral background
C_CARD_BORDER = colors.HexColor("#E2E8F0")  # Card border
C_GREEN = colors.HexColor("#16A34A")        # Positive / Growth
C_RED = colors.HexColor("#DC2626")          # Negative / Risk
C_BLUE = colors.HexColor("#0284C7")         # Accent / Process
C_AMBER = colors.HexColor("#D97706")        # Watchlist
C_CALLOUT_BG = colors.HexColor("#EFF6FF")   # Key finding light blue
C_CALLOUT_BORDER = colors.HexColor("#BFDBFE")

# -------------------------------------------------------------
# Styles Definition
# -------------------------------------------------------------
styles = getSampleStyleSheet()

s_meta = ParagraphStyle('Meta', fontName='DejaVuSans-Bold', fontSize=8.5, leading=11, textColor=C_BLUE)
s_title = ParagraphStyle('DocTitle', fontName='DejaVuSans-Bold', fontSize=21, leading=25, textColor=C_NAVY_DARK)
s_subtitle = ParagraphStyle('DocSubtitle', fontName='DejaVuSans', fontSize=11, leading=15, textColor=C_MUTED)

s_h1 = ParagraphStyle('H1', fontName='DejaVuSans-Bold', fontSize=15, leading=19, textColor=C_NAVY_DARK)
s_h3 = ParagraphStyle('H3', fontName='DejaVuSans-Bold', fontSize=10, leading=13, textColor=C_NAVY_DARK)

s_body = ParagraphStyle('Body', fontName='DejaVuSans', fontSize=9.5, leading=13.5, textColor=C_SLATE)
s_caption = ParagraphStyle('Caption', fontName='DejaVuSans', fontSize=8, leading=11, textColor=C_MUTED)
s_caption_bold = ParagraphStyle('CaptionBold', fontName='DejaVuSans-Bold', fontSize=8, leading=11, textColor=C_NAVY_DARK)

s_callout_title = ParagraphStyle('CalloutTitle', fontName='DejaVuSans-Bold', fontSize=9, leading=12, textColor=C_NAVY_DARK)
s_callout_body = ParagraphStyle('CalloutBody', fontName='DejaVuSans', fontSize=9, leading=13, textColor=C_SLATE)

# Base Canvas Geometry (A4: 595.27 x 841.89 pt, margin 36 pt -> 523.27 usable width)
USABLE_WIDTH = 523.27
CHARTS_DIR = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/outputs/pdf_assets"

# -------------------------------------------------------------
# Helper: Callout Box
# -------------------------------------------------------------
def make_callout(title_text, body_text, bg_color=C_CALLOUT_BG, border_color=C_CALLOUT_BORDER, pad=8):
    content = [
        Paragraph(title_text, s_callout_title),
        Spacer(1, 3),
        Paragraph(body_text, s_callout_body)
    ]
    t = Table([[content]], colWidths=[USABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('TOPPADDING', (0,0), (-1,-1), pad),
        ('BOTTOMPADDING', (0,0), (-1,-1), pad),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

# -------------------------------------------------------------
# BUILD STORY
# -------------------------------------------------------------
story = []

# =============================================================
# PAGE 1: EXECUTIVE FINDING
# =============================================================
story.append(Paragraph("SYNCHRONY ANALYTICS HACKATHON 2026", s_meta))
story.append(Spacer(1, 4))
story.append(Paragraph("HSIC SOLUTION", s_title))
story.append(Paragraph("Silent Attrition & Share-of-Wallet Recovery", ParagraphStyle('Sub1', fontName='DejaVuSans-Bold', fontSize=15, leading=18, textColor=C_NAVY_DARK)))
story.append(Paragraph("Turning payment migration into targeted customer action", s_subtitle))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.2, color=C_CARD_BORDER, spaceBefore=0, spaceAfter=8))

story.append(Paragraph("The retailer is growing. HSIC's share of that growth is shrinking.", s_h1))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "MetroMart continues to grow, but HSIC is capturing a smaller portion of that spending. "
    "The data points to a payment-behaviour problem rather than a simple loss of customers.",
    s_body
))
story.append(Spacer(1, 8))

# 5 Large KPI Cards in 2+3 layout
kpi_row1 = [
    [
        Paragraph("<font size=8 color='#64748B'>FY26 METROMART SALES</font><br/><b><font size=18 color='#0F172A'>₹435.69M</font></b><br/><font size=8.5 color='#16A34A'><b>+15.37% YoY</b> Retail Sales Growth</font>", ParagraphStyle('K1', fontName='DejaVuSans', leading=15)),
        Paragraph("<font size=8 color='#64748B'>HSIC CARD SPEND YoY</font><br/><b><font size=18 color='#DC2626'>−19.55%</font></b><br/><font size=8.5 color='#64748B'>Contracted to ₹68.92M (from ₹85.67M)</font>", ParagraphStyle('K2', fontName='DejaVuSans', leading=15))
    ]
]
t_kpi1 = Table(kpi_row1, colWidths=[USABLE_WIDTH/2 - 4, USABLE_WIDTH/2 - 4])
t_kpi1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ('PADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_kpi1)
story.append(Spacer(1, 5))

kpi_row2 = [
    [
        Paragraph("<font size=7.5 color='#64748B'>FY26 HSIC SHARE OF WALLET</font><br/><b><font size=16 color='#0F172A'>15.82%</font></b><br/><font size=8 color='#64748B'>Down from 22.69% in FY25</font>", ParagraphStyle('K3', fontName='DejaVuSans', leading=14)),
        Paragraph("<font size=7.5 color='#64748B'>HSIC SoW CHANGE</font><br/><b><font size=16 color='#DC2626'>−6.87 pp</font></b><br/><font size=8 color='#64748B'>Net Portfolio Share Loss</font>", ParagraphStyle('K4', fontName='DejaVuSans', leading=14)),
        Paragraph("<font size=7.5 color='#64748B'>SILENT ATTRITION CUSTOMERS</font><br/><b><font size=16 color='#DC2626'>3,784</font></b><br/><font size=8 color='#64748B'>8.41% Active Cardholders</font>", ParagraphStyle('K5', fontName='DejaVuSans', leading=14))
    ]
]
w3 = (USABLE_WIDTH - 8) / 3
t_kpi2 = Table(kpi_row2, colWidths=[w3, w3, w3])
t_kpi2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ('PADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_kpi2)
story.append(Spacer(1, 8))

# Large visual comparison
story.append(Paragraph("<b>SPENDING DIVERGENCE:</b> Retail Expansion vs. Co-Brand Card Contraction", s_h3))
story.append(Spacer(1, 3))
story.append(Image(os.path.join(CHARTS_DIR, "p1_spend_divergence.png"), width=USABLE_WIDTH, height=140))
story.append(Spacer(1, 6))

# Key Finding Box
story.append(make_callout(
    "KEY FINDING",
    "Customers are still shopping at MetroMart. An increasing portion of their checkout spend is moving away from HSIC. "
    "Because retail spending is actively growing, this is not an account churn problem — it is a tender displacement problem."
))
story.append(Spacer(1, 8))

# 5-Step Solution Journey
story.append(Paragraph("<b>THE END-TO-END ANALYTICAL RECOVERY JOURNEY:</b>", s_h3))
story.append(Spacer(1, 4))
flow_cols = [
    Paragraph("<b>1. DETECT</b><br/><font size=7.5 color='#64748B'>Falling SoW</font>", ParagraphStyle('F1', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=12>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>2. DIAGNOSE</b><br/><font size=7.5 color='#64748B'>Where did spend move?</font>", ParagraphStyle('F2', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=12>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>3. SEGMENT</b><br/><font size=7.5 color='#64748B'>Who behaves similarly?</font>", ParagraphStyle('F3', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=12>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>4. RECOMMEND</b><br/><font size=7.5 color='#64748B'>What should we offer?</font>", ParagraphStyle('F4', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=12>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>5. RECOVER</b><br/><font size=7.5 color='#64748B'>Did HSIC regain share?</font>", ParagraphStyle('F5', fontName='DejaVuSans', alignment=1, leading=10))
]
w_box = (USABLE_WIDTH - (4 * 16)) / 5
t_flow = Table([flow_cols], colWidths=[w_box, 16, w_box, 16, w_box, 16, w_box, 16, w_box])
t_flow.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), C_LIGHT_BG),
    ('BACKGROUND', (2,0), (2,0), C_LIGHT_BG),
    ('BACKGROUND', (4,0), (4,0), C_LIGHT_BG),
    ('BACKGROUND', (6,0), (6,0), C_LIGHT_BG),
    ('BACKGROUND', (8,0), (8,0), C_LIGHT_BG),
    ('BOX', (0,0), (0,0), 1, C_CARD_BORDER),
    ('BOX', (2,0), (2,0), 1, C_CARD_BORDER),
    ('BOX', (4,0), (4,0), 1, C_CARD_BORDER),
    ('BOX', (6,0), (6,0), 1, C_CARD_BORDER),
    ('BOX', (8,0), (8,0), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ('PADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_flow)
story.append(Spacer(1, 8))

# Finishing paragraph
story.append(Paragraph(
    "The solution turns a portfolio-level warning into a customer-level action. By isolating exactly where cardholder spend "
    "leaks across checkout registers, Synchrony can identify which cardholders are silently diverting spend and deliver "
    "targeted commercial interventions before payment diversion hardens into permanent brand churn.",
    s_body
))

# Page 1 Break
story.append(PageBreak())

# =============================================================
# PAGE 2: WHERE DID THE LOST SPEND GO?
# =============================================================
story.append(Paragraph("Where did the lost HSIC spend go?", s_title))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "HSIC's decline is happening while MetroMart itself is growing. Looking at payment tender makes the shift visible.",
    s_body
))
story.append(Spacer(1, 8))

# Visual 1: Large Payment Migration Chart
story.append(Paragraph("<b>PAYMENT TENDER MIGRATION:</b> YoY Spend Shift Across Checkout Methods", s_h3))
story.append(Spacer(1, 3))
story.append(Image(os.path.join(CHARTS_DIR, "p2_payment_migration.png"), width=USABLE_WIDTH, height=160))
story.append(Spacer(1, 6))

# WHAT WE SEE
obs_cells = [
    [
        Paragraph("<b>1. Convenience Pull</b><br/><font size=8.5 color='#334155'>Stored wallet usage is increasing strongly (+38.96%, +₹22.2M), suggesting customers are moving everyday checkout behaviour toward convenience.</font>", ParagraphStyle('O1', fontName='DejaVuSans', leading=12)),
        Paragraph("<b>2. Everyday UPI Scanning</b><br/><font size=8.5 color='#334155'>UPI is gaining share (+26.87%, +₹18.4M), particularly relevant for frequent and smaller purchases where plastic card checkout feels slower.</font>", ParagraphStyle('O2', fontName='DejaVuSans', leading=12)),
        Paragraph("<b>3. Big-Ticket Financing</b><br/><font size=8.5 color='#334155'>Competitor credit cards are gaining share (+22.04%, +₹20.3M), especially important in categories such as Electronics and Appliances with instant EMI.</font>", ParagraphStyle('O3', fontName='DejaVuSans', leading=12))
    ]
]
t_obs = Table(obs_cells, colWidths=[w3, w3, w3])
t_obs.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ('PADDING', (0,0), (-1,-1), 7),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_obs)
story.append(Spacer(1, 8))

# Visual 2: Large 24-Month SoW Trend
story.append(Paragraph("<b>24-MONTH PORTFOLIO TRAJECTORY:</b> Share of Wallet Slide from Peak to Trough", s_h3))
story.append(Spacer(1, 3))
story.append(Image(os.path.join(CHARTS_DIR, "p2_monthly_sow_trend.png"), width=USABLE_WIDTH, height=160))
story.append(Spacer(1, 6))

# Callout
story.append(make_callout(
    "STRUCTURAL CONCERN",
    "The concern is not simply fewer transactions. It is declining HSIC capture of transactions that are still happening. "
    "From a peak of 26.60% (Aug 2024), HSIC Share of Wallet eroded steadily to 12.01% (Jul 2026). "
    "Traditional churn models miss this entirely because cardholders remain active in MetroMart's loyalty database."
))

# Page 2 Break
story.append(PageBreak())

# =============================================================
# PAGE 3: WHO IS ACTUALLY AT RISK?
# =============================================================
story.append(Paragraph("Who is actually at risk?", s_title))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Silent attrition becomes useful when we can identify the customers behind the portfolio-level decline.",
    s_body
))
story.append(Spacer(1, 8))

# 3 Large Risk Cards with clean spacing (no font collision)
rc_title_red = ParagraphStyle('RCTR', fontName='DejaVuSans-Bold', fontSize=9, leading=12, textColor=C_RED)
rc_num_red = ParagraphStyle('RCNR', fontName='DejaVuSans-Bold', fontSize=22, leading=26, textColor=C_RED)
rc_sub = ParagraphStyle('RCS', fontName='DejaVuSans-Bold', fontSize=9, leading=12, textColor=C_NAVY_DARK)
rc_desc = ParagraphStyle('RCD', fontName='DejaVuSans', fontSize=8, leading=11, textColor=C_MUTED)

rc_title_amb = ParagraphStyle('RCTA', fontName='DejaVuSans-Bold', fontSize=9, leading=12, textColor=C_AMBER)
rc_num_amb = ParagraphStyle('RCNA', fontName='DejaVuSans-Bold', fontSize=22, leading=26, textColor=C_AMBER)

rc_title_grn = ParagraphStyle('RCTG', fontName='DejaVuSans-Bold', fontSize=9, leading=12, textColor=C_GREEN)
rc_num_grn = ParagraphStyle('RCNG', fontName='DejaVuSans-Bold', fontSize=22, leading=26, textColor=C_GREEN)

c_high = [
    Paragraph("HIGH RISK", rc_title_red),
    Spacer(1, 2),
    Paragraph("1,245", rc_num_red),
    Spacer(1, 2),
    Paragraph("Severe Attrition", rc_sub),
    Paragraph("SoW drop &gt; 40.0 pp<br/>Immediate tender intervention", rc_desc)
]

c_watch = [
    Paragraph("WATCHLIST", rc_title_amb),
    Spacer(1, 2),
    Paragraph("3,210", rc_num_amb),
    Spacer(1, 2),
    Paragraph("Emerging Risk", rc_sub),
    Paragraph("Tender switching (10–40 pp)<br/>Active leakage in key aisles", rc_desc)
]

c_health = [
    Paragraph("HEALTHY", rc_title_grn),
    Spacer(1, 2),
    Paragraph("40,000", rc_num_grn),
    Spacer(1, 2),
    Paragraph("Stable &amp; Loyal", rc_sub),
    Paragraph("Consistently high card share<br/>Focus on loyalty retention", rc_desc)
]

t_risk = Table([[c_high, c_watch, c_health]], colWidths=[w3, w3, w3])
t_risk.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (0,0), 1.5, colors.HexColor('#FCA5A5')),
    ('BOX', (1,0), (1,0), 1.5, colors.HexColor('#FCD34D')),
    ('BOX', (2,0), (2,0), 1.5, colors.HexColor('#86EFAC')),
    ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ('PADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_risk)
story.append(Spacer(1, 8))

# Large Horizontal Flow
story.append(Paragraph("<b>HOW THE BEHAVIOURAL SIGNAL TRANSLATES INTO INTERVENTION:</b>", s_h3))
story.append(Spacer(1, 4))
chain_cols = [
    Paragraph("<b>CUSTOMER</b><br/><font size=7 color='#64748B'>Active cardholder</font>", ParagraphStyle('C1', fontName='DejaVuSans', alignment=1, leading=9)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>SPENDING PATTERN</b><br/><font size=7 color='#64748B'>Category baskets</font>", ParagraphStyle('C2', fontName='DejaVuSans', alignment=1, leading=9)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>PAYMENT TENDER</b><br/><font size=7 color='#64748B'>Register choice</font>", ParagraphStyle('C3', fontName='DejaVuSans', alignment=1, leading=9)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>SoW CHANGE</b><br/><font size=7 color='#64748B'>Share delta</font>", ParagraphStyle('C4', fontName='DejaVuSans', alignment=1, leading=9)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>RISK / OPPORTUNITY</b><br/><font size=7 color='#64748B'>Targeted action</font>", ParagraphStyle('C5', fontName='DejaVuSans', alignment=1, leading=9))
]
t_chain = Table([chain_cols], colWidths=[w_box, 16, w_box, 16, w_box, 16, w_box, 16, w_box])
t_chain.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), C_CALLOUT_BG),
    ('BACKGROUND', (2,0), (2,0), C_CALLOUT_BG),
    ('BACKGROUND', (4,0), (4,0), C_CALLOUT_BG),
    ('BACKGROUND', (6,0), (6,0), C_CALLOUT_BG),
    ('BACKGROUND', (8,0), (8,0), C_CALLOUT_BG),
    ('BOX', (0,0), (0,0), 1, C_CALLOUT_BORDER),
    ('BOX', (2,0), (2,0), 1, C_CALLOUT_BORDER),
    ('BOX', (4,0), (4,0), 1, C_CALLOUT_BORDER),
    ('BOX', (6,0), (6,0), 1, C_CALLOUT_BORDER),
    ('BOX', (8,0), (8,0), 1, C_CALLOUT_BORDER),
    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ('PADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_chain)
story.append(Spacer(1, 8))

# Four Actionable Segments Grid
story.append(Paragraph("<b>CUSTOMER SEGMENT RECOVERY PLAYBOOK:</b>", s_h3))
story.append(Spacer(1, 3))
seg_w2 = (USABLE_WIDTH - 6) / 2
seg_grid = [
    [
        Paragraph(
            "<b>EMERGING RISK</b> (4,565 customers)<br/>"
            "<font size=8.5 color='#475569'>Current SoW: <b>9.47%</b> | Expected Recovery: <b><font color='#16A34A'>+3.2% SoW</font></b><br/>"
            "Recommended Action: <b>10% Electronics Cashback (+ 0% POS EMI)</b></font>",
            ParagraphStyle('S1', fontName='DejaVuSans', leading=13)
        ),
        Paragraph(
            "<b>GROCERY HEAVY USERS</b> (6,814 customers)<br/>"
            "<font size=8.5 color='#475569'>Current SoW: <b>12.40%</b> | Expected Recovery: <b><font color='#16A34A'>+4.8% SoW</font></b><br/>"
            "Recommended Action: <b>Segment Campaign: Extra 5% Grocery Cashback</b></font>",
            ParagraphStyle('S2', fontName='DejaVuSans', leading=13)
        )
    ],
    [
        Paragraph(
            "<b>PRIME USERS</b> (3,921 customers)<br/>"
            "<font size=8.5 color='#475569'>Current SoW: <b>48.89%</b> | Expected Recovery: <b><font color='#16A34A'>+5.5% SoW</font></b><br/>"
            "Recommended Action: <b>Double Reward Week (2X Points + Free Delivery)</b></font>",
            ParagraphStyle('S3', fontName='DejaVuSans', leading=13)
        ),
        Paragraph(
            "<b>LOW ENGAGEMENT</b> (25,916 customers)<br/>"
            "<font size=8.5 color='#475569'>Current SoW: <b>11.99%</b> | Expected Recovery: <b><font color='#16A34A'>+2.1% SoW</font></b><br/>"
            "Recommended Action: <b>₹500 Welcome Back Bonus Voucher</b></font>",
            ParagraphStyle('S4', fontName='DejaVuSans', leading=13)
        )
    ]
]
t_seg = Table(seg_grid, colWidths=[seg_w2, seg_w2])
t_seg.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ('PADDING', (0,0), (-1,-1), 7),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_seg)
story.append(Spacer(1, 8))

# Segment Opportunity Visual
story.append(Paragraph("<b>ADDRESSABLE WALLET OPPORTUNITY BY SEGMENT:</b> Total Pool = ₹54.36M", s_h3))
story.append(Spacer(1, 2))
story.append(Image(os.path.join(CHARTS_DIR, "p3_segment_opportunity.png"), width=USABLE_WIDTH, height=135))
story.append(Spacer(1, 6))

# Business Value Callout
story.append(make_callout(
    "BUSINESS VALUE OF SEGMENTATION",
    "Segmentation gives us a practical way to avoid blanket campaigns. Different behaviours require different interventions. "
    "A customer losing electronics spend to a competitor credit card requires point-of-sale zero-cost EMI financing, "
    "whereas a grocery-heavy household migrating to UPI needs contactless everyday card rewards."
))
story.append(Spacer(1, 4))
story.append(Paragraph("<font size=7.5 color='#64748B'>* Behavioural segmentation: K-Means, K=5 | Silhouette ≈ 0.393 | Expected recovery numbers represent analytical modelled segment expectations, not guaranteed revenue.</font>", s_caption))

# Page 3 Break
story.append(PageBreak())

# =============================================================
# PAGE 4: FROM INSIGHT TO ACTION
# =============================================================
story.append(Paragraph("From \"Who is at risk?\" to \"What should we do?\"", s_title))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Next Best Offer turns a customer's observed behaviour into a specific commercial action. "
    "Instead of blanket promotions, explainable customer-level rules directly address the root-cause reason for tender diversion.",
    s_body
))
story.append(Spacer(1, 8))

# 3-Column Decision Engine Visual Table
story.append(Paragraph("<b>NEXT BEST OFFER (NBO) DECISION ENGINE:</b> Customer-Level Rules", s_h3))
story.append(Spacer(1, 3))
nbo_headers = [
    Paragraph("<b>OBSERVED BEHAVIOUR</b>", ParagraphStyle('NH1', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>DIAGNOSIS</b>", ParagraphStyle('NH2', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>NEXT BEST OFFER (NBO RULE)</b>", ParagraphStyle('NH3', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white))
]
nbo_rows = [
    nbo_headers,
    [
        Paragraph("Electronics spend shifted to rival credit card", s_caption_bold),
        Paragraph("Competitor-card migration in big-ticket items", s_caption),
        Paragraph("<b>10% Electronics Cashback</b> + 0% Instant POS EMI", s_caption_bold)
    ],
    [
        Paragraph("Frequent grocery shopper + SoW &lt; 40%", s_caption_bold),
        Paragraph("Everyday supermarket basket moving to UPI / debit", s_caption),
        Paragraph("<b>Customer-level NBO: 3% Grocery Cashback</b> (60 days)", s_caption_bold)
    ],
    [
        Paragraph("MetroMart Stored Wallet dominant tender", s_caption_bold),
        Paragraph("Checkout shifting to stored wallet for 1-tap discounts", s_caption),
        Paragraph("<b>2.5% card-funded auto-reload bonus</b> on wallet", s_caption_bold)
    ],
    [
        Paragraph("UPI QR migration at physical POS registers", s_caption_bold),
        Paragraph("Card usage displaced by phone scanning friction", s_caption),
        Paragraph("<b>Virtual RuPay Card on UPI</b> + 1.5% scan cashback", s_caption_bold)
    ],
    [
        Paragraph("100% HSIC card loyalty + Non-Prime member", s_caption_bold),
        Paragraph("Retention / loyalty opportunity (Zero churn risk)", s_caption),
        Paragraph("<b>Complimentary 1-Year Prime Upgrade</b> (VIP Reward)", ParagraphStyle('PR', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN))
    ]
]
t_nbo = Table(nbo_rows, colWidths=[170, 160, USABLE_WIDTH - 330])
t_nbo.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_LIGHT_BG, colors.white]),
    ('GRID', (0,0), (-1,-1), 0.5, C_CARD_BORDER),
    ('PADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_nbo)
story.append(Spacer(1, 7))

# Distinction Callout Box
story.append(make_callout(
    "TWO-TIER OFFER ARCHITECTURE",
    "Customer-level NBO rules trigger automated micro-incentives (e.g. 3% grocery cashback for 60 days) to individual accounts to protect operating margins. "
    "In contrast, portfolio-wide marketing pushes represent broader promotional campaigns (e.g. 5% grocery cashback across the entire 6,814 cohort)."
))
story.append(Spacer(1, 9))

# Customer 360 Case Studies Section
story.append(Paragraph("<b>CUSTOMER 360 — WHAT THIS LOOKS LIKE IN PRACTICE:</b>", s_h3))
story.append(Spacer(1, 4))
cust_headers = [
    Paragraph("<b>ACCOUNT</b>", ParagraphStyle('CH1', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>STATUS &amp; TREND</b>", ParagraphStyle('CH2', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>DIAGNOSED ROOT CAUSE</b>", ParagraphStyle('CH3', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>TRIGGERED NEXT BEST OFFER</b>", ParagraphStyle('CH4', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white))
]
cust_rows = [
    cust_headers,
    [
        Paragraph("<b>#25790</b>", s_caption_bold),
        Paragraph("Prime<br/><font color='#DC2626'><b>SoW −100 pp</b></font>", s_caption),
        Paragraph("<b>Wallet migration</b> (Shifted ₹36.9k to MetroMart Wallet)", s_caption),
        Paragraph("<b>2.5% Auto-Reload Bonus</b> on Card Top-Up", s_caption_bold)
    ],
    [
        Paragraph("<b>#33822</b>", s_caption_bold),
        Paragraph("Non-Prime<br/><font color='#DC2626'><b>SoW −35.2 pp</b></font>", s_caption),
        Paragraph("<b>Grocery migration</b> (Supermarket spend shifting to UPI)", s_caption),
        Paragraph("<b>Customer-level NBO: 3% Grocery Cashback</b>", s_caption_bold)
    ],
    [
        Paragraph("<b>#24664</b>", s_caption_bold),
        Paragraph("Prime<br/><font color='#DC2626'><b>Electronics attrition</b></font>", s_caption),
        Paragraph("<b>Competitor card</b> (Appliance/electronics EMI diversion)", s_caption),
        Paragraph("<b>10% Cashback + 0% Instant POS EMI</b>", s_caption_bold)
    ],
    [
        Paragraph("<b>#58218</b>", s_caption_bold),
        Paragraph("Non-Prime<br/><font color='#DC2626'><b>SoW −42.1 pp</b></font>", s_caption),
        Paragraph("<b>UPI migration</b> (Physical register card swipe friction)", s_caption),
        Paragraph("<b>Virtual RuPay Card on UPI</b> + 1.5% cashback", s_caption_bold)
    ],
    [
        Paragraph("<b>#25555</b>", ParagraphStyle('CPOS', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN)),
        Paragraph("Non-Prime<br/><font color='#16A34A'><b>SoW +84.4 pp Lift</b></font>", s_caption),
        Paragraph("<font color='#16A34A'><b>100% HSIC card loyalty</b> (Exemplary usage)</font>", s_caption),
        Paragraph("<b>Complimentary 1-Yr Prime Upgrade</b> (VIP Retention)", ParagraphStyle('CPOS2', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN))
    ]
]
t_cust = Table(cust_rows, colWidths=[65, 105, 185, USABLE_WIDTH - 355])
t_cust.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [C_LIGHT_BG, colors.white]),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F0FDF4')),  # Soft green highlight for #25555
    ('GRID', (0,0), (-1,-1), 0.5, C_CARD_BORDER),
    ('PADDING', (0,0), (-1,-1), 5.5),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_cust)
story.append(Spacer(1, 9))

# Human Takeaway Box
story.append(make_callout(
    "HUMAN ANALYTICAL TAKEAWAY",
    "The important part is not just identifying a risky customer. It is being able to explain why — and what action follows. "
    "Note that account #25555 is not a risk customer; it is an exemplary loyalty success case (+84.4 pp SoW) that our system recognizes "
    "and rewards with a VIP Prime upgrade rather than issuing a false churn alert."
))

# Page 4 Break
story.append(PageBreak())

# =============================================================
# PAGE 5: WHAT COULD RECOVERY LOOK LIKE?
# =============================================================
story.append(Paragraph("The opportunity is not lost customers. It is lost payment share.", s_title))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Because these customers are still shopping at MetroMart, the recovery opportunity is to redirect a portion of existing spend back to HSIC.",
    s_body
))
story.append(Spacer(1, 8))

# Large Central Figure Card (₹54.36M) - separated cleanly into paragraphs
opp_elements = [
    Paragraph("<font size=9 color='#64748B'><b>ESTIMATED WALLET OPPORTUNITY (HISTORICAL BASELINE SHARE GAP)</b></font>", ParagraphStyle('OCT', fontName='DejaVuSans', alignment=1, leading=12)),
    Spacer(1, 4),
    Paragraph("<b><font size=28 color='#0F172A'>₹54.36M</font></b>", ParagraphStyle('OCN', fontName='DejaVuSans-Bold', alignment=1, leading=32)),
    Spacer(1, 4),
    Paragraph("<font size=8.5 color='#334155'>Annualized spending gap across the 3,784 Silent Attrition cardholders if restored to historical tender baseline.</font>", ParagraphStyle('OCD', fontName='DejaVuSans', alignment=1, leading=13))
]
t_opp = Table([[opp_elements]], colWidths=[USABLE_WIDTH])
t_opp.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#CBD5E1')),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ('PADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_opp)
story.append(Spacer(1, 8))

# Recovery Scenario Table & Chart
story.append(Paragraph("<b>ILLUSTRATIVE RECOVERY SCENARIOS:</b> Modelled Financial Impact Across 3,784 Accounts", s_h3))
story.append(Spacer(1, 3))

scen_headers = [
    Paragraph("<b>RECOVERY SCENARIO*</b>", ParagraphStyle('SH1', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>GROSS CARD SPEND RECAPTURED</b>", ParagraphStyle('SH2', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>ESTIMATED CAMPAIGN BUDGET</b>", ParagraphStyle('SH3', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>NET FINANCIAL LIFT</b>", ParagraphStyle('SH4', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white)),
    Paragraph("<b>PROJECTED ROI</b>", ParagraphStyle('SH5', fontName='DejaVuSans-Bold', fontSize=8, textColor=colors.white))
]
scen_rows = [
    scen_headers,
    [
        Paragraph("5% Recapture Scenario", s_caption),
        Paragraph("₹2.72M", s_caption_bold),
        Paragraph("₹500,000", s_caption),
        Paragraph("₹2.22M", s_caption_bold),
        Paragraph("3.2x Net ROI", s_caption)
    ],
    [
        Paragraph("<b>10% Recapture Scenario (Base Case)</b>", ParagraphStyle('B1', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN)),
        Paragraph("<b>₹5.44M</b>", ParagraphStyle('B2', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN)),
        Paragraph("₹850,000", s_caption),
        Paragraph("<b>₹4.59M</b>", ParagraphStyle('B3', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN)),
        Paragraph("<b>5.2x Net ROI</b>", ParagraphStyle('B4', fontName='DejaVuSans-Bold', fontSize=8, textColor=C_GREEN))
    ],
    [
        Paragraph("15% Recapture Scenario", s_caption),
        Paragraph("₹8.15M", s_caption_bold),
        Paragraph("₹1,150,000", s_caption),
        Paragraph("₹7.00M", s_caption_bold),
        Paragraph("8.6x Net ROI", s_caption)
    ],
    [
        Paragraph("20% Recapture Scenario", s_caption),
        Paragraph("₹10.87M", s_caption_bold),
        Paragraph("₹1,450,000", s_caption),
        Paragraph("₹9.42M", s_caption_bold),
        Paragraph("11.8x Net ROI", s_caption)
    ]
]
t_scen = Table(scen_rows, colWidths=[150, 105, 95, 95, USABLE_WIDTH - 445])
t_scen.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_LIGHT_BG, colors.white]),
    ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#F0FDF4')),  # Soft green highlight for base case
    ('GRID', (0,0), (-1,-1), 0.5, C_CARD_BORDER),
    ('PADDING', (0,0), (-1,-1), 4.5),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_scen)
story.append(Spacer(1, 6))

# Recovery Visual Chart
story.append(Image(os.path.join(CHARTS_DIR, "p5_recovery_scenarios.png"), width=USABLE_WIDTH, height=135))
story.append(Spacer(1, 4))
story.append(Paragraph("<font size=7.5 color='#64748B'>* Note: These are illustrative recovery scenarios, not guaranteed revenue or speculative forecasts. Actual recovery should be validated through controlled campaigns.</font>", s_caption))
story.append(Spacer(1, 6))

# Production Roadmap
story.append(Paragraph("<b>HOW WE WOULD TAKE THIS TO PRODUCTION:</b>", s_h3))
story.append(Spacer(1, 3))
prod_cols = [
    Paragraph("<b>1. Detect</b><br/><font size=7.5 color='#64748B'>Track SoW and tender migration</font>", ParagraphStyle('P1', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>2. Diagnose</b><br/><font size=7.5 color='#64748B'>Understand category &amp; tender behaviour</font>", ParagraphStyle('P2', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>3. Prioritize</b><br/><font size=7.5 color='#64748B'>Focus on valuable / high-risk accounts</font>", ParagraphStyle('P3', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>4. Personalize</b><br/><font size=7.5 color='#64748B'>Deploy targeted commercial NBOs</font>", ParagraphStyle('P4', fontName='DejaVuSans', alignment=1, leading=10)),
    Paragraph("<font color='#64748B' size=11>→</font>", ParagraphStyle('Arr', fontName='DejaVuSans', alignment=1)),
    Paragraph("<b>5. Measure</b><br/><font size=7.5 color='#64748B'>Track incremental spend, SoW &amp; ROI</font>", ParagraphStyle('P5', fontName='DejaVuSans', alignment=1, leading=10))
]
t_prod = Table([prod_cols], colWidths=[w_box, 16, w_box, 16, w_box, 16, w_box, 16, w_box])
t_prod.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), C_LIGHT_BG),
    ('BACKGROUND', (2,0), (2,0), C_LIGHT_BG),
    ('BACKGROUND', (4,0), (4,0), C_LIGHT_BG),
    ('BACKGROUND', (6,0), (6,0), C_LIGHT_BG),
    ('BACKGROUND', (8,0), (8,0), C_LIGHT_BG),
    ('BOX', (0,0), (0,0), 1, C_CARD_BORDER),
    ('BOX', (2,0), (2,0), 1, C_CARD_BORDER),
    ('BOX', (4,0), (4,0), 1, C_CARD_BORDER),
    ('BOX', (6,0), (6,0), 1, C_CARD_BORDER),
    ('BOX', (8,0), (8,0), 1, C_CARD_BORDER),
    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ('PADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_prod)
story.append(Spacer(1, 8))

# Production Validation Callout Box
story.append(make_callout(
    "HOW WE WOULD VALIDATE THIS IN PRODUCTION",
    "Run controlled A/B test experiments comparing targeted offers against a randomized control group. "
    "Measure incremental HSIC card spend, Share of Wallet recovery trajectory, offer redemption rate, campaign cost, and net return on investment before enterprise deployment."
))
story.append(Spacer(1, 8))

# Final Large Closing Statement
final_stmt = [
    [
        Paragraph(
            "<b><font size=10.5 color='#0F172A'>Instead of waiting for visible churn, Synchrony can intervene while the customer is still active at the retailer — when there is still wallet share to recover.</font></b>",
            ParagraphStyle('FS', fontName='DejaVuSans-Bold', alignment=1, leading=15)
        )
    ]
]
t_final = Table(final_stmt, colWidths=[USABLE_WIDTH])
t_final.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1.5, C_NAVY_DARK),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ('PADDING', (0,0), (-1,-1), 10),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_final)

# -------------------------------------------------------------
# PDF BUILD
# -------------------------------------------------------------
OUTPUT_PDF = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/HSIC_SOLUTION_Executive_Findings.pdf"

# Clean simple canvas with NO headers, NO footers, NO page numbers
doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=A4,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

doc.build(story)
print("Successfully generated polished redesigned PDF at:", OUTPUT_PDF)
