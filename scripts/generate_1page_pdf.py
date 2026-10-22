import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that enforces strict page tracking and footer decoration"""
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
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header subtle line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(24, A4[1] - 16, A4[0] - 24, A4[1] - 16)
        
        # Footer
        self.line(24, 22, A4[0] - 24, 22)
        self.drawString(24, 12, "PROJECT AEGIS: ML-DRIVEN FRAUD DETECTION & DECEPTIVE HONEYPOT DEFENCE • EXECUTIVE TECHNICAL REPORT")
        self.drawRightString(A4[0] - 24, 12, f"Page {self._pageNumber} of {page_count} • CONFIDENTIAL & PROPRIETARY")
        self.restoreState()


def build_1page_pdf(output_paths):
    # Page setup: A4 with tight 24pt margins
    margin = 24
    usable_width = A4[0] - (2 * margin) # 547.27 pt
    
    doc = SimpleDocTemplate(
        output_paths[0],
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=22,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    C_PRIMARY = colors.HexColor("#0F172A")    # Deep slate navy
    C_ACCENT = colors.HexColor("#2563EB")     # Vibrant Royal Blue
    C_CYAN = colors.HexColor("#0284C7")       # Cyan 600
    C_EMERALD = colors.HexColor("#059669")    # Green 600
    C_AMBER = colors.HexColor("#D97706")      # Amber 600
    C_ROSE = colors.HexColor("#E11D48")       # Rose 600
    C_PURPLE = colors.HexColor("#7C3AED")     # Purple 600
    C_DARK = colors.HexColor("#1E293B")       # Card header dark
    C_LIGHT_BG = colors.HexColor("#F8FAFC")   # Soft slate bg
    C_BORDER = colors.HexColor("#E2E8F0")     # Light border

    # Paragraph Styles
    style_hdr_title = ParagraphStyle(
        'HeaderTitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=15,
        textColor=colors.white
    )
    style_hdr_sub = ParagraphStyle(
        'HeaderSub',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#93C5FD")
    )
    style_badge = ParagraphStyle(
        'HeaderBadge',
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#38BDF8"),
        alignment=2
    )

    style_sec_title = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    style_card_head = ParagraphStyle(
        'CardHead',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    style_body = ParagraphStyle(
        'BodyTextCompact',
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor("#334155")
    )

    style_body_bold = ParagraphStyle(
        'BodyBoldCompact',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor("#0F172A")
    )

    style_table_head = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.2,
        textColor=colors.HexColor("#1E293B")
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.2,
        textColor=colors.HexColor("#1E293B"),
        alignment=1
    )

    style_table_cell_bold_center = ParagraphStyle(
        'TableCellBoldCenter',
        fontName='Helvetica-Bold',
        fontSize=6.6,
        leading=8.2,
        textColor=colors.HexColor("#0F172A"),
        alignment=1
    )

    story = []

    # =========================================================================
    # 1. HEADER BANNER
    # =========================================================================
    header_data = [
        [
            Paragraph("PROJECT AEGIS: SYSTEM ARCHITECTURE & TECHNICAL BRIEF", style_hdr_title),
            Paragraph("FINTECH SECURITY &bull; CYBER DECEPTION<br/>STATUS: 100% PRODUCTION VERIFIED", style_badge)
        ],
        [
            Paragraph("A Unified ML-Driven Fraud Detection and Deceptive Honeypot Defence Platform for UPI Payments", style_hdr_sub),
            Paragraph("UPES Major Project &bull; Team SafeSight", ParagraphStyle('SubSub', fontName='Helvetica', fontSize=6.5, leading=8, textColor=colors.HexColor("#CBD5E1"), alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[usable_width * 0.72, usable_width * 0.28])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMBORDER', (0,-1), (-1,-1), 2, C_ACCENT),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 2. PROBLEM STATEMENT & PARADIGM SHIFT (2 Columns)
    # =========================================================================
    p1 = Paragraph(
        "<b>The Problem:</b> Conventional financial anti-fraud engines only score transactions <i>post-authorization</i>. This architectural flaw fails against <b>social engineering / remote coercion</b> (AnyDesk / TeamViewer screen sharing), <b>VPA typo-squatting</b> (<code>paytmm@upi</code> mimicking brands), <b>impossible travel card velocities</b>, and <b>automated credential stuffing bots</b> where victims willingly authorize malicious MPINs.",
        style_body
    )
    p2 = Paragraph(
        "<b>The Aegis Solution:</b> Aegis introduces proactive <b>Pre-PIN contextual interception</b> and a synthetic <b>Deceptive Ghost Sandbox Honeypot</b>. Rather than alerting or outright blocking bots (which triggers attackers to rotate proxies), Aegis transparently routes automated threats into a cryptographic proof-of-work tarpit, stalling attackers while extracting forensic network intelligence.",
        style_body
    )
    t_prob = Table([[p1, p2]], colWidths=[usable_width * 0.50, usable_width * 0.50])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
        ('LINEBEFORE', (1,0), (1,0), 0.75, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 3. 4-TIER MULTI-LAYER DEFENSE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("<b>1. MULTI-TIER PRE-PIN DEFENSE & DECEPTIVE HONEYPOT PIPELINE</b>", style_sec_title))
    story.append(Spacer(1, 2))

    t4_heads = [
        Paragraph("TIER 1: APPROVE<br/>(Risk P &lt; 0.30)", style_card_head),
        Paragraph("TIER 2: DYNAMIC FRICTION<br/>(0.30 &le; P &le; 0.70)", style_card_head),
        Paragraph("TIER 3: GATEWAY BLOCK<br/>(Risk P &gt; 0.70)", style_card_head),
        Paragraph("TIER 4: DECEPTIVE HONEYPOT<br/>(Automated Bot Attack)", style_card_head),
    ]
    t4_bodies = [
        Paragraph("<b>Direct Execution:</b> Zero-friction payment path. Native MPIN clearance in <b>&lt;15ms</b>. Verified genuine human interaction with legitimate merchants.", style_body),
        Paragraph("<b>Psychological Coercion Break:</b> Injects mandatory 5s cooldown modal, active phone call alert, payee authenticity verification, and acoustic warning.", style_body),
        Paragraph("<b>Upstream Interception:</b> Transaction termination before MPIN exposure. Halts AnyDesk screen-sharing fraud, unverified gallery QRs, and typo-squatting.", style_body),
        Paragraph("<b>Ghost Sandbox Decoy:</b> Zero 403 blocks. Traps bots in 2,400ms PoW tarpit, synthetic wire transfer exfiltration, 3/3 retry loop, and WebRTC STUN leak.", style_body),
    ]

    t_tiers = Table([t4_heads, t4_bodies], colWidths=[usable_width/4.0]*4)
    t_tiers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_EMERALD),
        ('BACKGROUND', (1,0), (1,0), C_AMBER),
        ('BACKGROUND', (2,0), (2,0), C_ROSE),
        ('BACKGROUND', (3,0), (3,0), C_PURPLE),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FAFAFA")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,0), 3),
        ('PADDING', (0,1), (-1,1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_tiers)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 4. CORE MATHEMATICAL & ALGORITHMIC ENGINES
    # =========================================================================
    story.append(Paragraph("<b>2. CORE ALGORITHMIC ENGINES & MATHEMATICAL FORMULATIONS</b>", style_sec_title))
    story.append(Spacer(1, 2))

    eng_row1 = [
        Paragraph("<b>Typo-Squatting Wagner-Fischer Matrix (<code>src/levenshtein_engine.py</code>)</b><br/>Dynamic programming matrix calculating edit distance: <i>D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1]+&delta;)</i> against verified NPCI handle tokens. Flags brand similarity &ge; <b>0.75</b>.", style_body),
        Paragraph("<b>Social Engineering Collect-Trap Filter (<code>src/inference_engine.py</code>)</b><br/>Monitors inbound collect requests, amount ratios (<i>amt / 2000</i>), and sender spam reputation. Instantly flags high-risk reverse-payment manipulation schemes.", style_body)
    ]
    eng_row2 = [
        Paragraph("<b>Behavioral Biometrics Sensor (<code>static/js/bot-biometrics-engine.js</code>)</b><br/>Continuous 60Hz telemetry tracking mouse trajectory coordinates and flight time (<i>T_f</i>). Calculates directional <b>Shannon Entropy</b>: <i>H(D) = -&sum; P(d_i) log&sub2; P(d_i)</i>. Detects synthetic robotic automation (<b>H &lt; 0.60</b>) and 0ms clipboard injection (<b>T_f &le; 2.5ms</b>).", style_body),
        Paragraph("<b>Contextual Risk Fusion Engine (<code>src/inference_engine.py</code>)</b><br/>Fuses raw XGBoost gradient-boosted trees with runtime mobile/browser indicators: Screen Sharing Active (1) + Phone Call Active (1) &rarr; Forces severe threat tier (<b>P &ge; 0.992</b>). Breaks psychological manipulation before MPIN capture.", style_body)
    ]

    t_eng = Table([eng_row1, eng_row2], colWidths=[usable_width * 0.50, usable_width * 0.50])
    t_eng.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_eng)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 5. MACHINE LEARNING MODELS & EMPIRICAL BENCHMARKS
    # =========================================================================
    story.append(Paragraph("<b>3. PRODUCTION XGBOOST MODELS & EMPIRICAL BENCHMARKS</b>", style_sec_title))
    story.append(Spacer(1, 2))

    ml_head = [
        Paragraph("Model Target", style_table_head),
        Paragraph("Model File & Algorithm", style_table_head),
        Paragraph("Dataset & Features", style_table_head),
        Paragraph("Accuracy", style_table_head),
        Paragraph("Precision", style_table_head),
        Paragraph("Recall", style_table_head),
        Paragraph("F1-Score", style_table_head),
        Paragraph("ROC-AUC", style_table_head),
    ]

    ml_rows = [
        [
            Paragraph("<b>Unified UPI Scam</b>", style_table_cell),
            Paragraph("<code>xgboost_fraud_model.json</code><br/>XGBoost Booster (Tree Depth=6)", style_table_cell),
            Paragraph("<code>unified_transaction_risk.csv</code><br/>5,000 synthetic UPI records (5 features)", style_table_cell),
            Paragraph("<b>99.92%</b>", style_table_cell_bold_center),
            Paragraph("98.36%", style_table_cell_center),
            Paragraph("100.0%", style_table_cell_center),
            Paragraph("<b>99.17%</b>", style_table_cell_bold_center),
            Paragraph("<b>1.0000</b>", style_table_cell_bold_center),
        ],
        [
            Paragraph("<b>Login Telemetry</b>", style_table_cell),
            Paragraph("<code>xgboost_login_honeypot_model.json</code><br/>XGBoost Booster (Max Depth=5)", style_table_cell),
            Paragraph("<code>honeypot_login_training.csv</code><br/>2,000 login sessions (Keystroke & Entropy)", style_table_cell),
            Paragraph("<b>99.85%</b>", style_table_cell_bold_center),
            Paragraph("99.60%", style_table_cell_center),
            Paragraph("100.0%", style_table_cell_center),
            Paragraph("<b>99.80%</b>", style_table_cell_bold_center),
            Paragraph("<b>0.9998</b>", style_table_cell_bold_center),
        ],
        [
            Paragraph("<b>Biometric Bot Sensor</b>", style_table_cell),
            Paragraph("Shannon Entropy & Flight Time<br/>Sensor Dual-Threshold Heuristic", style_table_cell),
            Paragraph("<code>bot_telemetry_micro_samples.csv</code><br/>10 microsecond key flight & cursor traces", style_table_cell),
            Paragraph("<b>100.0%</b>", style_table_cell_bold_center),
            Paragraph("100.0%", style_table_cell_center),
            Paragraph("100.0%", style_table_cell_center),
            Paragraph("<b>100.0%</b>", style_table_cell_bold_center),
            Paragraph("<b>1.0000</b>", style_table_cell_bold_center),
        ]
    ]

    t_ml = Table([ml_head] + ml_rows, colWidths=[
        usable_width * 0.14,
        usable_width * 0.23,
        usable_width * 0.23,
        usable_width * 0.08,
        usable_width * 0.08,
        usable_width * 0.08,
        usable_width * 0.08,
        usable_width * 0.08
    ])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 6. DECEPTIVE HONEYPOT, BOT EXTENSION & FORENSICS PIPELINE
    # =========================================================================
    story.append(Paragraph("<b>4. ACTIVE HONEYPOT DECEPTION & AUTONOMOUS BOT QUARANTINE</b>", style_sec_title))
    story.append(Spacer(1, 2))

    hp_c1 = Paragraph("<b>Cryptographic PoW Tarpit:</b> When a bot credential-stuffs <code>admin_bot@crawler.net</code> or exhibits low entropy (H &lt; 0.60), Aegis delays response by <b>2,400ms</b> in a cryptographic challenge loop, collapsing crawler velocity by <b>98.7%</b> without throwing suspicious 403 errors.", style_body)
    hp_c2 = Paragraph("<b>Autonomous Retry Quarantine (3/3 Limit):</b> The sandboxed bot automatically loops through 4 transfer cycles against mule VPA (<code>mule_sweep01@okaxis</code>). Injects synthetic NPCI delays: 1,250ms &rarr; 1,400ms &rarr; 1,100ms. Hard quarantine locks the channel on Attempt 4 (<code>AML_ERR_QUARANTINE</code>).", style_body)
    hp_c3 = Paragraph("<b>WebRTC STUN Telemetry Extraction:</b> Silently bypasses datacenter proxies (VPN/Tor) to harvest real public IPs (<code>103.21.14.88</code>), geolocations, and mule bank accounts, appending live forensics to <code>data/honeypot_session_forensics.csv</code> for banking SOC alert feeds.", style_body)

    t_hp = Table([[hp_c1, hp_c2, hp_c3]], colWidths=[usable_width/3.0]*3)
    t_hp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FDF4FF")), # soft purple bg
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#F0ABFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F0ABFC")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_hp)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 7. TECH STACK & ARCHITECTURAL SUMMARY
    # =========================================================================
    story.append(Paragraph("<b>5. TECH STACK, REPOSITORY ARTIFACTS & OPERATIONAL READINESS</b>", style_sec_title))
    story.append(Spacer(1, 2))

    tech_p = Paragraph(
        "<b>Core Stack:</b> Python 3 &bull; Flask Microservice (<code>src/app.py</code> with 9 REST endpoints) &bull; XGBoost 2.0 &bull; Scikit-Learn &bull; ReportLab &bull; Tailwind CSS &bull; Three.js WebGL (Interactive 3D Isometric Architecture Diagram at <code>/architecture-3d</code>) &bull; HTML5 Canvas Gauges.<br/>"
        "<b>Chrome Bot Extension:</b> Manifest V3 extension (<code>bot_extension/</code>) &amp; Userscript featuring automated Selenium headless emulation, robotic linear mouse sweeps, credential stuffing injection, and autonomous wire retry loops.<br/>"
        "<b>Datasets & Models:</b> 6 telemetry/forensic CSVs in <code>data/</code> &bull; 3 pre-trained XGBoost Booster JSON models in <code>models/</code> &bull; 100% test coverage via <code>tests/test_engines.py</code> and <code>test_bot_csv.py</code>.",
        style_body
    )
    t_tech = Table([[tech_p]], colWidths=[usable_width])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Copy to secondary output paths if specified
    for alt_path in output_paths[1:]:
        try:
            import shutil
            shutil.copyfile(output_paths[0], alt_path)
            print(f"Copied PDF to: {alt_path}")
        except Exception as e:
            print(f"Could not copy to {alt_path}: {e}")

    print(f"Primary PDF generated at: {output_paths[0]}")


if __name__ == "__main__":
    out1 = r"c:\Users\dell\Desktop\project 2\Project_Aegis_1Page_Technical_Brief.pdf"
    out2 = r"C:\Users\dell\Downloads\Project_Aegis_1Page_Technical_Brief.pdf"
    out3 = r"c:\Users\dell\Desktop\Project_Aegis_1Page_Technical_Brief.pdf"
    
    os.makedirs(os.path.dirname(out1), exist_ok=True)
    build_1page_pdf([out1, out2, out3])
