"""
build_findings_pdf.py
Generates the official 5-page Judge-Facing Analysis & Findings PDF
for the Synchrony Analytics Hackathon 2026.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/HSIC_SOLUTION_Executive_Findings.pdf"
CHARTS_DIR = "/Users/apple/.gemini/antigravity-ide/scratch/Synchrony_Hackathon/outputs/pdf_assets"

# -------------------------------------------------------------
# NUMBERED CANVAS (Two-pass canvas for exact "Page X of 5")
# -------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        navy = colors.HexColor("#0F172A")
        slate = colors.HexColor("#64748B")
        border_color = colors.HexColor("#E2E8F0")
        
        # Top Header (pages 2-5)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(navy)
            self.drawString(36, 815, "HSIC SOLUTION")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(slate)
            self.drawString(108, 815, "|   Silent Attrition & Share-of-Wallet Recovery   —   Synchrony Hackathon 2026")
            
            # Right header
            self.drawRightString(595.28 - 36, 815, "Executive Findings & Case Study")
            
            # Header rule
            self.setStrokeColor(border_color)
            self.setLineWidth(0.6)
            self.line(36, 808, 595.28 - 36, 808)
            
        # Bottom Footer (all pages)
        self.setStrokeColor(border_color)
        self.setLineWidth(0.6)
        self.line(36, 32, 595.28 - 36, 32)
        
        self.setFont("Helvetica", 7.2)
        self.setFillColor(slate)
        self.drawString(36, 21, "Live Solution: adityakasara.github.io/Synchrony_One    |    GitHub: github.com/Adityakasara/Synchrony_One")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.2)
        self.drawRightString(595.28 - 36, 21, page_str)
        
        self.restoreState()

# -------------------------------------------------------------
# BUILD PDF
# -------------------------------------------------------------
def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#0F172A")
    DARK_SLATE = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#475569")
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    RED_ACCENT = colors.HexColor("#DC2626")
    GREEN_ACCENT = colors.HexColor("#16A34A")
    BLUE_ACCENT = colors.HexColor("#0284C7")
    AMBER_ACCENT = colors.HexColor("#D97706")
    
    # Custom Typography Styles
    title_meta = ParagraphStyle('TitleMeta', parent=styles['Normal'],
                                fontName='Helvetica-Bold', fontSize=8, leading=10,
                                textColor=BLUE_ACCENT)
    
    doc_title = ParagraphStyle('DocTitle', parent=styles['Normal'],
                               fontName='Helvetica-Bold', fontSize=19, leading=22,
                               textColor=NAVY)
    
    doc_subtitle = ParagraphStyle('DocSubtitle', parent=styles['Normal'],
                                  fontName='Helvetica', fontSize=10, leading=13.5,
                                  textColor=TEXT_MUTED)
    
    page_headline = ParagraphStyle('PageHeadline', parent=styles['Normal'],
                                   fontName='Helvetica-Bold', fontSize=14, leading=17.5,
                                   textColor=NAVY)
    
    page_subheadline = ParagraphStyle('PageSubHeadline', parent=styles['Normal'],
                                      fontName='Helvetica', fontSize=9.5, leading=13.5,
                                      textColor=TEXT_MUTED)
    
    body_p = ParagraphStyle('BodyP', parent=styles['Normal'],
                            fontName='Helvetica', fontSize=8.6, leading=12.2,
                            textColor=DARK_SLATE)
    
    body_bold = ParagraphStyle('BodyBold', parent=styles['Normal'],
                              fontName='Helvetica-Bold', fontSize=8.6, leading=12.2,
                              textColor=DARK_SLATE)
    
    callout_text = ParagraphStyle('CalloutText', parent=styles['Normal'],
                                  fontName='Helvetica-Bold', fontSize=8.8, leading=12.5,
                                  textColor=NAVY)
    
    takeaway_text = ParagraphStyle('TakeawayText', parent=styles['Normal'],
                                   fontName='Helvetica', fontSize=7.8, leading=10.8,
                                   textColor=TEXT_MUTED)
    
    kpi_num = ParagraphStyle('KpiNum', parent=styles['Normal'],
                             fontName='Helvetica-Bold', fontSize=12.5, leading=14.5,
                             alignment=1, textColor=NAVY)
    
    kpi_lbl = ParagraphStyle('KpiLbl', parent=styles['Normal'],
                             fontName='Helvetica-Bold', fontSize=6.8, leading=8.5,
                             alignment=1, textColor=TEXT_MUTED)
    
    kpi_sub = ParagraphStyle('KpiSub', parent=styles['Normal'],
                             fontName='Helvetica', fontSize=6.8, leading=8.5,
                             alignment=1, textColor=NAVY)

    flow = []
    USABLE_W = 523.28

    # =========================================================
    # PAGE 1: EXECUTIVE FINDING
    # =========================================================
    flow.append(Paragraph("SYNCHRONY ANALYTICS HACKATHON 2026  |  EXECUTIVE CASE STUDY", title_meta))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph("HSIC SOLUTION: Silent Attrition & Share-of-Wallet Recovery", doc_title))
    flow.append(Paragraph("Turning payment migration into targeted customer action", doc_subtitle))
    flow.append(Spacer(1, 8))
    flow.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=10))

    # Core Headline
    flow.append(Paragraph("The retailer is growing. HSIC's share of that growth is shrinking.", page_headline))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(
        "MetroMart continues to grow, but HSIC is capturing a smaller share of that spending. "
        "The data points to a payment-behaviour problem rather than a simple loss of customers.",
        body_p
    ))
    flow.append(Spacer(1, 10))

    # 5 Large KPI Cards Table
    kpi_data = [
        [
            Paragraph("FY26 METROMART SALES", kpi_lbl),
            Paragraph("METROMART YOY GROWTH", kpi_lbl),
            Paragraph("FY26 HSIC SHARE OF WALLET", kpi_lbl),
            Paragraph("HSIC SOW CHANGE", kpi_lbl),
            Paragraph("SILENT ATTRITION", kpi_lbl)
        ],
        [
            Paragraph("INR 435.69M", kpi_num),
            Paragraph("+15.37%", ParagraphStyle('Kg1', parent=kpi_num, textColor=GREEN_ACCENT)),
            Paragraph("15.82%", kpi_num),
            Paragraph("−6.87 pp", ParagraphStyle('Kr1', parent=kpi_num, textColor=RED_ACCENT)),
            Paragraph("3,784", ParagraphStyle('Kr2', parent=kpi_num, textColor=RED_ACCENT))
        ],
        [
            Paragraph("+15.37% Retail Net Sales", kpi_sub),
            Paragraph("from INR 377.65M in FY25", kpi_sub),
            Paragraph("Co-Brand Spend: INR 68.92M", kpi_sub),
            Paragraph("from 22.69% in FY25", kpi_sub),
            Paragraph("8.41% Active Accounts", kpi_sub)
        ]
    ]
    t_kpi = Table(kpi_data, colWidths=[USABLE_W / 5.0] * 5)
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    flow.append(t_kpi)
    flow.append(Spacer(1, 12))

    # Visual Spend Divergence Chart
    chart_p1_path = os.path.join(CHARTS_DIR, "p1_spend_divergence.png")
    if os.path.exists(chart_p1_path):
        flow.append(Image(chart_p1_path, width=USABLE_W, height=115))
        flow.append(Spacer(1, 2))
        flow.append(Paragraph("<b>Takeaway:</b> MetroMart retail sales expanded by +15.37% YoY, while co-branded card spending contracted by −19.55% YoY.", takeaway_text))
    flow.append(Spacer(1, 12))

    # Highlighted Insight Box
    insight_content = [
        [Paragraph("<b>Key Strategic Insight:</b> Customers are still shopping at MetroMart. The problem is that an increasing portion of their checkout spend is moving away from HSIC.", callout_text)]
    ]
    t_insight = Table(insight_content, colWidths=[USABLE_W])
    t_insight.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    flow.append(t_insight)
    flow.append(Spacer(1, 14))

    # Solution Flow Diagram: DETECT -> DIAGNOSE -> SEGMENT -> RECOMMEND -> RECOVER
    flow_steps = [
        [
            Paragraph("<b>1. DETECT</b><br/><font size=6.5 color='#475569'>Flag Silent Attrition & SoW Drop</font>", ParagraphStyle('F1', parent=kpi_lbl, alignment=1)),
            Paragraph("<b>2. DIAGNOSE</b><br/><font size=6.5 color='#475569'>Identify Diverted Channel & Category</font>", ParagraphStyle('F2', parent=kpi_lbl, alignment=1)),
            Paragraph("<b>3. SEGMENT</b><br/><font size=6.5 color='#475569'>Cluster by Tender & Basket Behaviour</font>", ParagraphStyle('F3', parent=kpi_lbl, alignment=1)),
            Paragraph("<b>4. RECOMMEND</b><br/><font size=6.5 color='#475569'>Trigger Automated Next Best Offer</font>", ParagraphStyle('F4', parent=kpi_lbl, alignment=1)),
            Paragraph("<b>5. RECOVER</b><br/><font size=6.5 color='#475569'>Measure Share & ROI Recapture</font>", ParagraphStyle('F5', parent=kpi_lbl, alignment=1))
        ]
    ]
    t_flow = Table(flow_steps, colWidths=[USABLE_W / 5.0] * 5)
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    flow.append(t_flow)
    flow.append(Spacer(1, 8))

    flow.append(Paragraph(
        "<b>How the System Works:</b> Our solution identifies customers whose HSIC Share of Wallet is deteriorating, "
        "explains where that spend is moving, groups customers by behaviour, and converts those signals into targeted Next Best Offers.",
        body_p
    ))

    flow.append(PageBreak())

    # =========================================================
    # PAGE 2: WHAT THE DATA TELLS US
    # =========================================================
    flow.append(Paragraph("Where did the lost HSIC spend go?", page_headline))
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("The decline is not happening in isolation. Other payment methods are gaining share while HSIC declines.", page_subheadline))
    flow.append(Spacer(1, 8))

    # Payment Migration Chart
    chart_p2_path = os.path.join(CHARTS_DIR, "p2_payment_migration.png")
    if os.path.exists(chart_p2_path):
        flow.append(Image(chart_p2_path, width=USABLE_W, height=155))
        flow.append(Spacer(1, 2))
        flow.append(Paragraph("<b>Takeaway:</b> Digital stored wallets (+38.96%) and mobile UPI QR (+26.87%) captured everyday transactions, while competitor credit cards (+22.04%) captured high-ticket purchases.", takeaway_text))
    flow.append(Spacer(1, 8))

    # Three Patterns Stand Out Box
    patterns_content = [
        [
            Paragraph("<b>Three observed patterns explain the tender substitution:</b>", ParagraphStyle('PH', parent=body_bold, textColor=NAVY))
        ],
        [
            Paragraph("<b>1. Convenience pull toward in-app stored wallets & UPI:</b> Merchant Stored Wallet spend jumped <b>+38.96% (+INR 22.2M)</b> and Mobile UPI QR expanded <b>+26.87% (+INR 18.4M)</b>, driven by 1-tap checkout discounts and mobile contactless POS scanning.", body_p)
        ],
        [
            Paragraph("<b>2. Competitor credit cards dominating high-ticket purchases:</b> High-ticket merchandise (Electronics and Appliances) shifted away to competitor cards (<b>+22.04%, +INR 20.3M</b>), indicating promotional competitor bank zero-cost EMI financing at POS counters.", body_p)
        ],
        [
            Paragraph("<b>3. Fundamental payment tender substitution:</b> HSIC card spend declined <b>−19.55% (−INR 16.75M)</b>. Cardholders did not stop shopping at MetroMart; they silently diverted payment at the register into alternative instruments.", body_p)
        ]
    ]
    t_patterns = Table(patterns_content, colWidths=[USABLE_W])
    t_patterns.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    flow.append(t_patterns)
    flow.append(Spacer(1, 8))

    # 24-Month Monthly SoW Trend Chart
    chart_p2b_path = os.path.join(CHARTS_DIR, "p2_monthly_sow_trend.png")
    if os.path.exists(chart_p2b_path):
        flow.append(Image(chart_p2b_path, width=USABLE_W, height=140))
        flow.append(Spacer(1, 2))
        flow.append(Paragraph("<b>Takeaway:</b> HSIC Share of Wallet experienced an unbroken 24-month structural slide from a peak of 26.60% (Aug 2024) to a trough of 12.01% (Jul 2026).", takeaway_text))
    flow.append(Spacer(1, 8))

    # Structural Risk Callout Box
    risk_callout = [
        [Paragraph("<b>Structural Risk Assessment:</b> The key risk is structural: if customers continue shopping but increasingly pay through other tenders, HSIC can lose transaction share without traditional churn being visible.", callout_text)]
    ]
    t_risk = Table(risk_callout, colWidths=[USABLE_W])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FECACA")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    flow.append(t_risk)

    flow.append(PageBreak())

    # =========================================================
    # PAGE 3: WHO IS AT RISK?
    # =========================================================
    flow.append(Paragraph("The opportunity is concentrated in identifiable customer behaviours.", page_headline))
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("Early detection requires grouping customers by risk severity and behavioral spending patterns.", page_subheadline))
    flow.append(Spacer(1, 8))

    # Early Warning Center (3 Tiers with clean dots)
    ew_data = [
        [
            Paragraph("<font color='#DC2626'>&#9679;</font>  HIGH RISK", ParagraphStyle('EwR1', parent=kpi_lbl, textColor=RED_ACCENT)),
            Paragraph("<font color='#D97706'>&#9679;</font>  WATCHLIST", ParagraphStyle('EwW1', parent=kpi_lbl, textColor=AMBER_ACCENT)),
            Paragraph("<font color='#16A34A'>&#9679;</font>  HEALTHY", ParagraphStyle('EwH1', parent=kpi_lbl, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("1,245 Customers", ParagraphStyle('EwR2', parent=kpi_num, textColor=RED_ACCENT)),
            Paragraph("3,210 Customers", ParagraphStyle('EwW2', parent=kpi_num, textColor=AMBER_ACCENT)),
            Paragraph("40,000 Customers", ParagraphStyle('EwH2', parent=kpi_num, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("Severe Silent Attrition<br/>SoW drop > 40.0 percentage points", kpi_sub),
            Paragraph("Emerging tender migration<br/>SoW drop 10.0 to 40.0 pp", kpi_sub),
            Paragraph("Stable & loyal cardholders<br/>Protected top-of-wallet habits", kpi_sub)
        ]
    ]
    t_ew = Table(ew_data, colWidths=[USABLE_W / 3.0] * 3)
    t_ew.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    flow.append(t_ew)
    flow.append(Spacer(1, 8))

    # Clarification Callout
    silent_attr_box = [
        [Paragraph("<b>Crucial Business Distinction:</b> Silent Attrition does not mean the customer has stopped shopping. It means the customer is still valuable to the retailer, but HSIC is losing the payment share.", callout_text)]
    ]
    t_sa = Table(silent_attr_box, colWidths=[USABLE_W])
    t_sa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    flow.append(t_sa)
    flow.append(Spacer(1, 8))

    # Four Actionable Customer Segments Table
    flow.append(Paragraph("<b>Customer Segment Recovery Playbook:</b>", body_bold))
    flow.append(Spacer(1, 4))
    
    seg_table_data = [
        [
            Paragraph("CUSTOMER SEGMENT", ParagraphStyle('Sh1', parent=kpi_lbl, alignment=0)),
            Paragraph("CUSTOMERS", ParagraphStyle('Sh2', parent=kpi_lbl, alignment=1)),
            Paragraph("CURRENT SOW", ParagraphStyle('Sh3', parent=kpi_lbl, alignment=1)),
            Paragraph("RECOMMENDED CAMPAIGN", ParagraphStyle('Sh4', parent=kpi_lbl, alignment=0)),
            Paragraph("EXPECTED RECOVERY*", ParagraphStyle('Sh5', parent=kpi_lbl, alignment=1))
        ],
        [
            Paragraph("<b>Emerging Risk</b>", body_p),
            Paragraph("4,565", ParagraphStyle('Sc1', parent=body_p, alignment=1)),
            Paragraph("9.47%", ParagraphStyle('Sc2', parent=body_p, alignment=1)),
            Paragraph("10% Electronics Cashback (+ 0% POS EMI)", body_p),
            Paragraph("<b>+3.2% SoW</b>", ParagraphStyle('Sr1', parent=body_p, alignment=1, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("<b>Grocery Heavy Users</b>", body_p),
            Paragraph("6,814", ParagraphStyle('Sc3', parent=body_p, alignment=1)),
            Paragraph("12.40%", ParagraphStyle('Sc4', parent=body_p, alignment=1)),
            Paragraph("Segment-level campaign: Extra 5% Grocery Cashback", body_p),
            Paragraph("<b>+4.8% SoW</b>", ParagraphStyle('Sr2', parent=body_p, alignment=1, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("<b>Prime Users</b>", body_p),
            Paragraph("3,921", ParagraphStyle('Sc5', parent=body_p, alignment=1)),
            Paragraph("48.89%", ParagraphStyle('Sc6', parent=body_p, alignment=1)),
            Paragraph("Double Reward Week (2X points + Free Delivery)", body_p),
            Paragraph("<b>+5.5% SoW</b>", ParagraphStyle('Sr3', parent=body_p, alignment=1, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("<b>Low Engagement</b>", body_p),
            Paragraph("25,916", ParagraphStyle('Sc7', parent=body_p, alignment=1)),
            Paragraph("11.99%", ParagraphStyle('Sc8', parent=body_p, alignment=1)),
            Paragraph("INR 500 Welcome Back Bonus Voucher", body_p),
            Paragraph("<b>+2.1% SoW</b>", ParagraphStyle('Sr4', parent=body_p, alignment=1, textColor=GREEN_ACCENT))
        ]
    ]
    t_seg = Table(seg_table_data, colWidths=[110, 60, 65, 198, 90.28])
    t_seg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ]))
    flow.append(t_seg)
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("<i>* Expected Recovery numbers represent analytical modeled segment expectations calibrated against customer transaction history, not guaranteed revenue.</i>", takeaway_text))
    flow.append(Spacer(1, 8))

    # Segment Opportunity Chart
    chart_p3_path = os.path.join(CHARTS_DIR, "p3_segment_opportunity.png")
    if os.path.exists(chart_p3_path):
        flow.append(Image(chart_p3_path, width=USABLE_W, height=115))
        flow.append(Spacer(1, 2))
        flow.append(Paragraph("<b>Takeaway:</b> While Low Engagement accounts hold high gross gap (INR 28.5M), Emerging Risk and Grocery Users offer higher responsiveness to targeted intervention.", takeaway_text))
    flow.append(Spacer(1, 8))

    flow.append(Paragraph(
        "<b>Strategic Personalization:</b> Segmentation prevents an expensive, one-size-fits-all campaign. "
        "A customer losing electronics spend to a competitor credit card requires zero-cost EMI financing, whereas a grocery-heavy shopper migrating to UPI requires contactless everyday card rewards.<br/>"
        "<font size=7 color='#64748B'>* K-Means behavioural segmentation | Features: SoW Delta, Basket Size, Category Concentration, Tender Ratio | K=5 | Silhouette ≈ 0.393</font>",
        body_p
    ))

    flow.append(PageBreak())

    # =========================================================
    # PAGE 4: FROM ANALYSIS TO ACTION
    # =========================================================
    flow.append(Paragraph("From \"Who is at risk?\" to \"What should we do?\"", page_headline))
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("Next Best Offer (NBO) converts diagnosed customer behavior directly into deterministic commercial actions.", page_subheadline))
    flow.append(Spacer(1, 8))

    # Visual NBO Decision Table
    flow.append(Paragraph("<b>Deterministic Next Best Offer (NBO) Decision Engine:</b>", body_bold))
    flow.append(Spacer(1, 4))
    
    nbo_table_data = [
        [
            Paragraph("OBSERVED CUSTOMER SIGNAL", ParagraphStyle('Nh1', parent=kpi_lbl, alignment=0)),
            Paragraph("ROOT CAUSE DIAGNOSIS", ParagraphStyle('Nh2', parent=kpi_lbl, alignment=0)),
            Paragraph("RECOMMENDED ACTION (NBO RULE)", ParagraphStyle('Nh3', parent=kpi_lbl, alignment=0))
        ],
        [
            Paragraph("Electronics purchases shifted away to rival credit card", body_p),
            Paragraph("Competitor-card migration in high-ticket electronics (EMI deals)", body_p),
            Paragraph("<b>10% Electronics Cashback</b> for 30 days + 0% Instant POS EMI", body_p)
        ],
        [
            Paragraph("Frequent grocery shopper (>= 2 visits) AND HSIC SoW < 40%", body_p),
            Paragraph("Everyday supermarket basket spend moving to UPI / debit", body_p),
            Paragraph("<b>Customer-level NBO: Extra 3% Grocery Cashback</b> for 60 days", body_p)
        ],
        [
            Paragraph("MetroMart Stored Wallet is dominant payment tender", body_p),
            Paragraph("Checkout convenience discounts replacing card swipes in-app", body_p),
            Paragraph("<b>2.5% Instant Auto-Reload Bonus</b> on wallet when funded via HSIC Card", body_p)
        ],
        [
            Paragraph("Displaced by QR phone scanning at physical POS registers", body_p),
            Paragraph("Plastic card friction at counter checkouts", body_p),
            Paragraph("<b>Virtual RuPay Card on UPI</b> with 1.5% scan-and-pay cashback", body_p)
        ],
        [
            Paragraph("100% HSIC card loyalty AND Non-Prime member", body_p),
            Paragraph("Exemplary top-of-wallet cardholder retention opportunity", body_p),
            Paragraph("<b>Complimentary 1-Year Prime Upgrade</b> as VIP Loyalty Reward", body_p)
        ]
    ]
    t_nbo = Table(nbo_table_data, colWidths=[150, 160, 213.28])
    t_nbo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ]))
    flow.append(t_nbo)
    flow.append(Spacer(1, 7))

    # Architecture Box: Clarifying 3% vs 5%
    arch_box = [
        [Paragraph(
            "<b>Two-Tier Offer Architecture:</b> "
            "Customer-level NBO rules (e.g. <b>3% grocery cashback</b>) trigger automated micro-incentives for targeted accounts to protect program margin. "
            "Segment-level campaigns (e.g. <b>5% grocery cashback</b>) represent promotional, portfolio-wide marketing pushes across the entire cohort (6,814 cardholders).",
            callout_text
        )]
    ]
    t_arch = Table(arch_box, colWidths=[USABLE_W])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    flow.append(t_arch)
    flow.append(Spacer(1, 8))

    # Customer 360 Mini Case Study Strip
    flow.append(Paragraph("<b>Representative Customer 360 Diagnostic Case Studies:</b>", body_bold))
    flow.append(Spacer(1, 4))

    c360_data = [
        [
            Paragraph("ACCOUNT", ParagraphStyle('Ch1', parent=kpi_lbl, alignment=0)),
            Paragraph("PROFILE & TREND", ParagraphStyle('Ch2', parent=kpi_lbl, alignment=0)),
            Paragraph("DIAGNOSED ROOT CAUSE", ParagraphStyle('Ch3', parent=kpi_lbl, alignment=0)),
            Paragraph("NEXT BEST OFFER TRIGGERED", ParagraphStyle('Ch4', parent=kpi_lbl, alignment=0))
        ],
        [
            Paragraph("<b>#25790</b>", body_p),
            Paragraph("Prime | −100.0 pp SoW<br/>Spend grew INR 4.9k -> INR 52.3k", body_p),
            Paragraph("<font color='#DC2626'>&#9679;</font> <b>Risk Radar:</b> Shifted INR 36.9k checkouts to MetroMart Wallet", body_p),
            Paragraph("<b>2.5% Auto-Reload Bonus</b> on Card Top-Up (power the wallet)", body_p)
        ],
        [
            Paragraph("<b>#33822</b>", body_p),
            Paragraph("Non-Prime | −35.2 pp SoW<br/>Frequent supermarket visits", body_p),
            Paragraph("<font color='#DC2626'>&#9679;</font> <b>Risk Radar:</b> Food & grocery basket migration to UPI", body_p),
            Paragraph("<b>Customer-level NBO: 3% Grocery Cashback</b> for 60 Days", body_p)
        ],
        [
            Paragraph("<b>#24664</b>", body_p),
            Paragraph("Prime | High-Ticket Attrition<br/>Electronics purchases diverted", body_p),
            Paragraph("<font color='#DC2626'>&#9679;</font> <b>Risk Radar:</b> Shifted purchases to competitor credit card", body_p),
            Paragraph("<b>10% Electronics Cashback</b> + 0% Instant POS EMI", body_p)
        ],
        [
            Paragraph("<b>#58218</b>", body_p),
            Paragraph("Non-Prime | −42.1 pp SoW<br/>Counter register checkout", body_p),
            Paragraph("<font color='#DC2626'>&#9679;</font> <b>Risk Radar:</b> Point-of-sale plastic card friction", body_p),
            Paragraph("<b>Virtual RuPay Card on UPI</b> with 1.5% Scan & Pay", body_p)
        ],
        [
            Paragraph("<b>#25555</b>", ParagraphStyle('Cg1', parent=body_p, textColor=GREEN_ACCENT)),
            Paragraph("Non-Prime | <b>+84.4 pp SoW Lift</b><br/>100% HSIC card loyalty", body_p),
            Paragraph("<font color='#16A34A'>&#9679;</font> <b>Loyalty Radar:</b> 100% Co-Brand Capture (Success Case)", body_p),
            Paragraph("<b>Complimentary 1-Yr Prime Upgrade</b> (Loyalty Retention)", body_p)
        ]
    ]
    t_c360 = Table(c360_data, colWidths=[65, 130, 160, 168.28])
    t_c360.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
    ]))
    flow.append(t_c360)
    flow.append(Spacer(1, 6))

    flow.append(Paragraph(
        "<b>Explainable Analytics:</b> Account #25555 illustrates that our system evaluates all customer dimensions—celebrating loyal, expanding accounts rather than issuing false churn alerts. Every offer is directly auditable to the root-cause tender shift.",
        takeaway_text
    ))

    flow.append(PageBreak())

    # =========================================================
    # PAGE 5: BUSINESS IMPACT & RECOMMENDATIONS
    # =========================================================
    flow.append(Paragraph("The goal is not to win back lost shoppers. It is to win back lost payment share.", page_headline))
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("Because customers are still shopping at MetroMart, the recovery opportunity is to redirect a portion of existing spend back to HSIC.", page_subheadline))
    flow.append(Spacer(1, 8))

    # Opportunity Sizing & Illustrative Scenarios Table
    flow.append(Paragraph("<b>Estimated Wallet Opportunity: INR 54.36M (Historical Baseline Share Gap)</b>", body_bold))
    flow.append(Spacer(1, 4))

    scen_data = [
        [
            Paragraph("RECOVERY SCENARIO*", ParagraphStyle('Sh1', parent=kpi_lbl, alignment=0)),
            Paragraph("GROSS CARD SPEND RECAPTURED", ParagraphStyle('Sh2', parent=kpi_lbl, alignment=1)),
            Paragraph("ESTIMATED CAMPAIGN BUDGET", ParagraphStyle('Sh3', parent=kpi_lbl, alignment=1)),
            Paragraph("NET FINANCIAL LIFT", ParagraphStyle('Sh4', parent=kpi_lbl, alignment=1)),
            Paragraph("PROJECTED NET ROI", ParagraphStyle('Sh5', parent=kpi_lbl, alignment=1))
        ],
        [
            Paragraph("5% Recapture Scenario", body_p),
            Paragraph("INR 2.72M", ParagraphStyle('S1', parent=body_p, alignment=1)),
            Paragraph("INR 500,000", ParagraphStyle('S2', parent=body_p, alignment=1)),
            Paragraph("INR 2.22M", ParagraphStyle('S3', parent=body_p, alignment=1)),
            Paragraph("3.2x ROI", ParagraphStyle('S4', parent=body_p, alignment=1))
        ],
        [
            Paragraph("<b>10% Recapture Scenario (Base Case)</b>", body_p),
            Paragraph("<b>INR 5.44M</b>", ParagraphStyle('Sb1', parent=body_p, alignment=1, textColor=GREEN_ACCENT)),
            Paragraph("INR 850,000", ParagraphStyle('Sb2', parent=body_p, alignment=1)),
            Paragraph("<b>INR 4.59M</b>", ParagraphStyle('Sb3', parent=body_p, alignment=1, textColor=GREEN_ACCENT)),
            Paragraph("<b>5.2x ROI</b>", ParagraphStyle('Sb4', parent=body_p, alignment=1, textColor=GREEN_ACCENT))
        ],
        [
            Paragraph("15% Recapture Scenario", body_p),
            Paragraph("INR 8.15M", ParagraphStyle('S5', parent=body_p, alignment=1)),
            Paragraph("INR 1,150,000", ParagraphStyle('S6', parent=body_p, alignment=1)),
            Paragraph("INR 7.00M", ParagraphStyle('S7', parent=body_p, alignment=1)),
            Paragraph("8.6x ROI", ParagraphStyle('S8', parent=body_p, alignment=1))
        ],
        [
            Paragraph("20% Recapture Scenario", body_p),
            Paragraph("INR 10.87M", ParagraphStyle('S9', parent=body_p, alignment=1)),
            Paragraph("INR 1,450,000", ParagraphStyle('Sa1', parent=body_p, alignment=1)),
            Paragraph("INR 9.42M", ParagraphStyle('Sa2', parent=body_p, alignment=1)),
            Paragraph("11.8x ROI", ParagraphStyle('Sa3', parent=body_p, alignment=1))
        ]
    ]
    t_scen = Table(scen_data, colWidths=[150, 105, 95, 85, 88.28])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    flow.append(t_scen)
    flow.append(Spacer(1, 3))
    flow.append(Paragraph("<i>* Note: Modelled as conservative illustrative recovery scenarios across the 3,784 Silent Attrition cardholders, not speculative forecasts or guaranteed revenue.</i>", takeaway_text))
    flow.append(Spacer(1, 8))

    # Recovery Scenarios Chart
    chart_p5_path = os.path.join(CHARTS_DIR, "p5_recovery_scenarios.png")
    if os.path.exists(chart_p5_path):
        flow.append(Image(chart_p5_path, width=USABLE_W, height=115))
        flow.append(Spacer(1, 2))
        flow.append(Paragraph("<b>Takeaway:</b> Under the base case 10% recovery scenario, recapturing INR 5.44M in gross card spend yields an INR 4.59M net profit lift after promotional costs (5.2x Net ROI).", takeaway_text))
    flow.append(Spacer(1, 8))

    # Simple Business Action Roadmap
    flow.append(Paragraph("<b>Five-Stage Operational Action Roadmap:</b>", body_bold))
    flow.append(Spacer(1, 4))
    
    roadmap_data = [
        [
            Paragraph("<b>1. DETECT</b><br/><font size=7 color='#475569'>Monitor monthly Share of Wallet and active tender shifts weekly at checkout.</font>", body_p),
            Paragraph("<b>2. DIAGNOSE</b><br/><font size=7 color='#475569'>Pinpoint leakage by merchandise category (electronics, groceries) and competitor tender.</font>", body_p),
            Paragraph("<b>3. PRIORITIZE</b><br/><font size=7 color='#475569'>Rank cardholders by estimated wallet opportunity to optimize marketing efficiency.</font>", body_p),
            Paragraph("<b>4. PERSONALIZE</b><br/><font size=7 color='#475569'>Deploy automated rule-driven NBOs (EMI subsidies, wallet top-up bonus, UPI cards).</font>", body_p),
            Paragraph("<b>5. MEASURE</b><br/><font size=7 color='#475569'>Track incremental card spend, SoW recapture, offer redemption rate, and campaign ROI.</font>", body_p)
        ]
    ]
    t_roadmap = Table(roadmap_data, colWidths=[USABLE_W / 5.0] * 5)
    t_roadmap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    flow.append(t_roadmap)
    flow.append(Spacer(1, 8))

    # Production Validation Box
    val_box = [
        [Paragraph(
            "<b>How We Would Validate This in Production:</b> "
            "Deploy controlled A/B test experiments comparing targeted NBO offers against a randomized holdout control group. "
            "Measure incremental HSIC card spend, Share of Wallet recovery trajectory, offer redemption rate, customer acquisition/retention cost, and net return on investment before enterprise roll-out.",
            callout_text
        )]
    ]
    t_val = Table(val_box, colWidths=[USABLE_W])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    flow.append(t_val)
    flow.append(Spacer(1, 8))

    # Final Closing Statement
    flow.append(Paragraph(
        "<b>Conclusion:</b> Instead of waiting for visible account closure, Synchrony can intervene while the customer is still active at MetroMart—when there is still wallet share to recover.",
        ParagraphStyle('ClosingP', parent=body_bold, fontSize=9.2, leading=13, textColor=NAVY)
    ))

    # Build the document
    doc.build(flow, canvasmaker=NumberedCanvas)
    print(f"Successfully generated findings PDF at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
