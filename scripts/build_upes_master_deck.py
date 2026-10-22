import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# COLOR PALETTE (UPES Corporate & Tech Colors)
# ==========================================
NAVY = RGBColor(0x0A, 0x25, 0x40)       # #0A2540 Deep UPES / Corporate Navy
ORANGE = RGBColor(0xF2, 0x8C, 0x28)     # #F28C28 UPES Accent Orange / Amber
CYAN = RGBColor(0x00, 0x70, 0xBA)       # #0070BA Tech Blue / Cyan
GREEN = RGBColor(0x16, 0xA3, 0x4A)      # #16A34A Emerald Success
RED = RGBColor(0xDC, 0x26, 0x26)        # #DC2626 Danger / Fraud Block
PURPLE = RGBColor(0x8B, 0x5C, 0xF6)     # #8B5CF6 Honeypot Purple
SLATE = RGBColor(0x1E, 0x29, 0x3B)      # #1E293B Body Text Dark Slate
MUTED = RGBColor(0x64, 0x74, 0x8B)      # #64748B Subtext / Secondary Gray
CARD_BG = RGBColor(0xF8, 0xFA, 0xFC)    # #F8FAFC Soft Off-White Card Fill
WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # #FFFFFF Pure White
BORDER_COLOR = RGBColor(0xCB, 0xD5, 0xE1)# #CBD5E1 Slate 300 Border Line

FOOTER_TEXT = "Project Aegis , BCA Sem 5 Project / UPES"

def setup_header(slide, category_text, title_text):
    """Adds the standard category pill and slide header title."""
    # Category Pill
    tb_cat = slide.shapes.add_textbox(Inches(0.89), Inches(0.25), Inches(6.00), Inches(0.28))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = CYAN

    # Header Title
    tb_title = slide.shapes.add_textbox(Inches(0.89), Inches(0.50), Inches(10.00), Inches(0.70))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

def add_card(slide, left, top, width, height, bg_rgb=CARD_BG, border_rgb=BORDER_COLOR, border_pt=1.0):
    """Creates a rounded rectangle card with background and border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_rgb
    card.line.color.rgb = border_rgb
    card.line.width = Pt(border_pt)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.16)
    tf.margin_bottom = Inches(0.16)
    return card

def add_footer(slide):
    """Updates or adds the template footer."""
    for sh in slide.shapes:
        if sh.has_text_frame and "<<Project Title>>" in sh.text_frame.text:
            sh.text_frame.text = FOOTER_TEXT
            p = sh.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = MUTED
            return
    # If not found, add a footer box
    tb = slide.shapes.add_textbox(Inches(4.42), Inches(6.95), Inches(5.00), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = FOOTER_TEXT
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED

def build_presentation(template_path, output_path):
    print(f"Loading template from: {template_path}")
    prs = pptx.Presentation(template_path)
    
    layout12 = prs.slide_masters[0].slide_layouts[12] # 1_Title and Content (widescreen template)
    layout10 = prs.slide_masters[0].slide_layouts[10] # Vertical Title and Text (Thank You layout)
    
    # We have 5 initial slides:
    # Slide 1: Cover
    # Slide 2: Table of Contents
    # Slide 3: 01 / Introduction
    # Slide 4: 02 / Research Foundation & SWOT
    # Slide 5: 03 / Project Scope & Decision Matrix
    # We add 9 more slides: Slides 6 through 14
    while len(prs.slides) < 14:
        if len(prs.slides) == 13:
            prs.slides.add_slide(layout10) # Slide 14: Thank You
        else:
            prs.slides.add_slide(layout12)

    print(f"Total slides prepared: {len(prs.slides)}")

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides[0]
    add_footer(s1)
    
    # Adjust UPES Logo Position (Picture 4)
    for sh in s1.shapes:
        if sh.name == "Picture 4":
            sh.left = Inches(4.20)
            sh.top = Inches(1.10)
            sh.width = Inches(5.00)
            sh.height = Inches(2.15)
            
    # Title & Subtitle Box
    tb_title = s1.shapes.add_textbox(Inches(1.00), Inches(3.40), Inches(11.33), Inches(1.50))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p1 = tf_title.paragraphs[0]
    p1.text = "Project Aegis: Unified ML-Driven Fraud Detection & Deceptive Honeypot"
    p1.font.name = "Arial"
    p1.font.size = Pt(23)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_title.add_paragraph()
    p2.text = "A Multi-Layer Fraud Prevention Platform for UPI & Card Payments Powered by Real-Time Telemetry CSVs, Behavioral Biometrics & Active Deception"
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = ORANGE
    p2.alignment = PP_ALIGN.CENTER

    # Team & Presentation Info Card
    card_team = add_card(s1, 1.50, 5.05, 10.33, 1.65, bg_rgb=WHITE, border_rgb=BORDER_COLOR)
    tf_team = card_team.text_frame
    
    p_t1 = tf_team.paragraphs[0]
    p_t1.text = "Presented By:"
    p_t1.font.name = "Arial"
    p_t1.font.size = Pt(11)
    p_t1.font.bold = True
    p_t1.font.color.rgb = CYAN
    p_t1.alignment = PP_ALIGN.CENTER

    p_t2 = tf_team.add_paragraph()
    p_t2.text = "Aayush Tripathi (590017378)   •   Akhil Pundir (590016767)   •   Aryan Singh (590017232)"
    p_t2.font.name = "Arial"
    p_t2.font.size = Pt(13)
    p_t2.font.bold = True
    p_t2.font.color.rgb = NAVY
    p_t2.alignment = PP_ALIGN.CENTER

    p_t3 = tf_team.add_paragraph()
    p_t3.text = "B.Tech CSE / BCA Sem 5 Project  |  School of Computer Science • UPES Dehradun"
    p_t3.font.name = "Arial"
    p_t3.font.size = Pt(11)
    p_t3.font.color.rgb = MUTED
    p_t3.alignment = PP_ALIGN.CENTER

    p_t4 = tf_team.add_paragraph()
    p_t4.text = "● Status: 100% Core Engine & Defense Verified  |  Sub-2ms Latency  |  10/10 Attack Benchmarks Passed"
    p_t4.font.name = "Arial"
    p_t4.font.size = Pt(11)
    p_t4.font.bold = True
    p_t4.font.color.rgb = GREEN
    p_t4.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: TABLE OF CONTENTS
    # =========================================================================
    s2 = prs.slides[1]
    # Clear placeholders from layout
    for sh in list(s2.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s2)
    setup_header(s2, "PROJECT AGENDA", "Table of Contents")

    toc_items = [
        ("01. Introduction & Problem Context", "Instant UPI settlement pressure, social engineering vectors & WAF bypass vulnerabilities."),
        ("02. Research Foundation & SWOT Analysis", "Academic foundations (Shannon, XGBoost, Haversine, Levenshtein, SMOTE) & regulatory standards."),
        ("03. Project Scope & 4-Tier Decision Matrix", "Approve (Instant), Friction (5s PIN hold), Block (Hard decline), and Honeypot Tarpit (Bots)."),
        ("04. Data Architecture & Telemetry CSVs", "4 Specialized forensic datasets: Login telemetry, Card velocity, Unified UPI & Decoy Wire ledger."),
        ("05. Behavioral Biometrics Engineering", "60Hz Shannon directional entropy H(D) < 0.60, keystroke flight dynamics & Web Worker ring buffer."),
        ("06. Methodology & Implementation Status", "Incremental Prototype Model lifecycle, 100% Core Engine verification & future milestones."),
        ("07. System Implementation & Working Model", "9 Flask REST APIs, 5 UI portals, Ghost sandbox (2,400ms PoW stall, STUN IP capture, mule wire intercept)."),
        ("08. Verification, Results & Benchmarks", "8 Attack benchmark scenarios, 100% detection accuracy on test_bot_csv.py & ROC-AUC curves.")
    ]

    for i, (title, desc) in enumerate(toc_items):
        col = i // 4
        row = i % 4
        c_left = 0.89 if col == 0 else 6.75
        c_top = 1.45 + row * 1.30
        card = add_card(s2, c_left, c_top, 5.65, 1.20)
        tf = card.text_frame
        p_h = tf.paragraphs[0]
        p_h.text = title
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12.5)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.0)
        p_d.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 3: 01 / INTRODUCTION & PROBLEM CONTEXT
    # =========================================================================
    s3 = prs.slides[2]
    for sh in list(s3.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s3)
    setup_header(s3, "01 / INTRODUCTION & PROBLEM CONTEXT", "Motivation, Threat Vectors & Telemetry Inputs")

    # Card 1 (Left): Technical Background & Threats
    c1 = add_card(s3, 0.89, 1.45, 5.65, 5.25)
    tf1 = c1.text_frame
    p = tf1.paragraphs[0]
    p.text = "Technical Background & Threat Landscape"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    points_left = [
        ("Instant UPI Settlement Pressure:", "Real-time payment clearance leaves sub-second windows for fraud interception, rendering post-facto chargeback retrieval obsolete."),
        ("Social Engineering Coercion:", "Scammers manipulate victims over live calls into scanning gallery QR codes and authorizing fraudulent collect requests."),
        ("Remote Screen Share Takeover:", "AnyDesk/TeamViewer virtual display hooks invisibly capture mobile keypad PIN entries during fraudulent sessions."),
        ("Limitations of Traditional WAFs:", "Static rule engines return immediate HTTP 403 Forbidden errors, instantly alerting botnets to rotate residential proxies and user-agents.")
    ]
    for h, b in points_left:
        p_h = tf1.add_paragraph()
        p_h.text = "• " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf1.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE

    # Card 2 (Right): Project Aegis Paradigm
    c2 = add_card(s3, 6.75, 1.45, 5.65, 5.25)
    tf2 = c2.text_frame
    p = tf2.paragraphs[0]
    p.text = "Project Aegis Defense Paradigm"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    points_right = [
        ("Multi-Modal Telemetry Ingestion:", "Fuses passive client biometrics, card physical velocity, and transaction semantic metadata into a unified risk scoring vector."),
        ("4 Specialized Forensic CSV Datasets:", "9,000+ total rows tracking 60Hz mouse paths, inter-key flight latencies, spacetime coordinates, and telephony states."),
        ("Sub-2ms Latency Envelope:", "High-throughput machine learning inference designed for immediate deployment directly into upstream banking switches."),
        ("Active Deception Honeypot Tarpit:", "Replaces binary rejection with a 2,400ms Proof-of-Work delay, isolating bot attacks in decoy sandboxes while harvesting threat intelligence.")
    ]
    for h, b in points_right:
        p_h = tf2.add_paragraph()
        p_h.text = "• " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf2.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 4: 02 / RESEARCH FOUNDATION & SWOT ANALYSIS
    # =========================================================================
    s4 = prs.slides[3]
    for sh in list(s4.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s4)
    setup_header(s4, "02 / RESEARCH FOUNDATION & SWOT ANALYSIS", "Academic Literature, Standards & Strategic SWOT")

    # Top summary pill card
    top_pill = add_card(s4, 0.89, 1.45, 11.55, 0.75, bg_rgb=WHITE)
    tf_pill = top_pill.text_frame
    p_p = tf_pill.paragraphs[0]
    p_p.text = "Foundational Standards: Shannon (1948) Directional Entropy • Chen & Guestrin (XGBoost 2016) • Sinnott (1984) Haversine • Levenshtein (1966) NLP • Chawla (SMOTE 2002) • RBI Payment Security (2021) • DPDP Act (2023)"
    p_p.font.name = "Arial"
    p_p.font.size = Pt(10.5)
    p_p.font.bold = True
    p_p.font.color.rgb = NAVY

    # 4-Quadrant SWOT Cards
    swot_cards = [
        ("Strengths (S)", GREEN, 0.89, 2.35, [
            "• Sub-2ms low latency scoring via trained XGBoost models.",
            "• 60Hz client behavioral biometrics detection (H < 0.60).",
            "• Proportionate 4-tier response prevents blanket account lockouts.",
            "• Silent WebRTC STUN IP capture without alerting attackers."
        ]),
        ("Weaknesses (W)", RED, 6.75, 2.35, [
            "• Initial models trained on synthetic rule-labelled datasets.",
            "• Novel zero-day social engineering scams require heuristic rules.",
            "• Advanced physical human replay scripts require multi-factor checks.",
            "• Cold-start user profile constraints for newly issued cards."
        ]),
        ("Opportunities (O)", CYAN, 0.89, 4.55, [
            "• Exploding UPI transaction volumes in India (>14 Billion/month).",
            "• RBI & NPCI mandates for real-time proactive fraud mitigation.",
            "• Scalable API licensing to regional cooperative and commercial banks.",
            "• Strong enterprise banking demand for active honeypot deception."
        ]),
        ("Threats (T)", ORANGE, 6.75, 4.55, [
            "• Headless browser botnets (Puppeteer/Stealth) with human mouse jitter.",
            "• Distributed residential proxy hopping and IP pool rotation.",
            "• AI-generated synthetic voice phishing (vishing) coercion.",
            "• DPDP Act 2023 compliance constraints on client telemetry collection."
        ])
    ]

    for title, col_rgb, c_left, c_top, bullets in swot_cards:
        card = add_card(s4, c_left, c_top, 5.65, 2.05)
        tf = card.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col_rgb

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.name = "Arial"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 5: 03 / PROJECT SCOPE & FOUR-TIER DECISION MATRIX
    # =========================================================================
    s5 = prs.slides[4]
    for sh in list(s5.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s5)
    setup_header(s5, "03 / PROJECT SCOPE & DECISION TIERS", "Primary Goals & Four-Tier Proportionate Enforcement")

    # Scope Summary Box
    scope_card = add_card(s5, 0.89, 1.45, 11.55, 1.05, bg_rgb=WHITE)
    tf_sc = scope_card.text_frame
    p_sc = tf_sc.paragraphs[0]
    p_sc.text = "PRIMARY OBJECTIVE"
    p_sc.font.name = "Arial"
    p_sc.font.size = Pt(11)
    p_sc.font.bold = True
    p_sc.font.color.rgb = CYAN

    p_sc2 = tf_sc.add_paragraph()
    p_sc2.text = "Build a unified, explainable fraud detection and deceptive bot defense platform that replaces rigid binary hard declines with proportionate, context-aware responses tailored to real-time evaluated risk."
    p_sc2.font.name = "Arial"
    p_sc2.font.size = Pt(11.5)
    p_sc2.font.color.rgb = NAVY

    # 4 Tier Cards
    tiers = [
        ("APPROVE", "P < 0.30", GREEN, [
            "Instant, frictionless settlement for genuine trusted users.",
            "Evaluates clean mouse biometrics, recognized device IDs, and trusted VPAs.",
            "Zero checkout friction or UI latency overhead (<2ms processing)."
        ]),
        ("FRICTION", "0.30 ≤ P ≤ 0.70", ORANGE, [
            "Mandatory 5-second Pre-PIN countdown warning modal.",
            "Triggered by active voice call + gallery QR code upload.",
            "Psychologically breaks fraudster coercion before fund deduction occurs."
        ]),
        ("BLOCK", "P > 0.70", RED, [
            "Upstream API gateway rejection halts unauthorized payouts.",
            "Triggered by impossible travel (>650 mph), remote desktop hooks, or spam VPAs.",
            "Prevents account takeover and blinds PIN keypad display layer."
        ]),
        ("HONEYPOT", "Bot Trigger", PURPLE, [
            "2,400ms Proof-of-Work cryptographic tarpit delay.",
            "Diverts automated scripts to Decoy Ghost Sandbox banking dashboard.",
            "Traps attacker wire transfer to mule_sweep01@okaxis and captures STUN IP."
        ])
    ]

    for i, (name, cond, col_rgb, desc_bullets) in enumerate(tiers):
        t_left = 0.89 + i * 2.95
        card = add_card(s5, t_left, 2.70, 2.75, 4.05)
        tf = card.text_frame
        
        p_n = tf.paragraphs[0]
        p_n.text = name
        p_n.font.name = "Arial"
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = col_rgb

        p_c = tf.add_paragraph()
        p_c.text = cond
        p_c.font.name = "Arial"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = NAVY

        for b in desc_bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.name = "Arial"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 6: 04 / DATA ARCHITECTURE & TELEMETRY CSVS
    # =========================================================================
    s6 = prs.slides[5]
    for sh in list(s6.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s6)
    setup_header(s6, "04 / DATA ARCHITECTURE & TELEMETRY CSVS", "Core Datasets: Named Telemetry CSV Architecture")

    # Table with 5 rows x 4 cols
    t_shape = s6.shapes.add_table(5, 4, Inches(0.89), Inches(1.50), Inches(11.55), Inches(5.15))
    table = t_shape.table
    table.columns[0].width = Inches(3.00)
    table.columns[1].width = Inches(1.40)
    table.columns[2].width = Inches(3.80)
    table.columns[3].width = Inches(3.35)

    table_data = [
        ("CSV File Name", "Dataset Scale", "Key Telemetry Feature Attributes", "Target Label & Defense Function"),
        ("honeypot_login_telemetry.csv", "2,000 Rows", "failed_attempts, typing_similarity, mouse_entropy, is_new_device, vpn_flag", "target_honeypot_action: Detects automated bot ingress & credential stuffing."),
        ("card_velocity_telemetry.csv", "2,000 Rows", "time_delta_seconds, distance_miles, required_speed_mph, merchant_risk", "is_card_fraud: Enforces Haversine spacetime physics (speed > 650 mph)."),
        ("unified_transaction_risk.csv", "5,000 Rows", "screen_sharing_active, upi_brand_similarity, is_collect_request, travel_speed", "is_fraud: Real-time XGBoost scoring of UPI interaction semantics."),
        ("honeypot_session_forensics.csv", "Live Ledger", "webrtc_reflexive_ip, dwell_time_seconds, target_vpa, attempted_amount, error_code", "Forensic Intel: Traps attacker IP and blacklists destination mule accounts.")
    ]

    for r_idx, r_vals in enumerate(table_data):
        for c_idx, val in enumerate(r_vals):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
            else:
                p.font.size = Pt(9.5)
                p.font.color.rgb = SLATE
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else CARD_BG

    # =========================================================================
    # SLIDE 7: 05 / BEHAVIORAL BIOMETRICS ENGINEERING
    # =========================================================================
    s7 = prs.slides[6]
    for sh in list(s7.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s7)
    setup_header(s7, "05 / BEHAVIORAL BIOMETRICS ENGINEERING", "60Hz Sensor Math, Shannon Entropy & Keystroke Dynamics")

    # Top privacy badge
    badge = add_card(s7, 0.89, 1.45, 11.55, 0.65, bg_rgb=WHITE)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "Client Privacy Protection: Captures passive physics metadata only; raw passwords & sensitive inputs are never transmitted | DPDP Act 2023 Compliant"
    p_b.font.name = "Arial"
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = GREEN

    # 3 Analytical Cards
    bio_cards = [
        ("Mouse Path Directional Entropy", CYAN, [
            "• Mathematical Formulation:",
            "  H(D) = -∑ p(b_k) log2 p(b_k) across 8 directional octant bins.",
            "• Genuine Human Cursor Dynamics:",
            "  H(D) ∈ [2.40, 3.80] exhibiting physiological micro-jitters & variable acceleration.",
            "• Headless Bot / Automation Script:",
            "  H(D) < 0.60 exhibiting synthetic collinear vectors & zero curvature.",
            "• Real-Time Sampling:",
            "  60Hz PointerEvents captures micro-movements on payment forms."
        ]),
        ("Keystroke Flight Dynamics", PURPLE, [
            "• Inter-Key Latency Tracking:",
            "  Monitored via high-precision window.performance.now().",
            "• Mathematical Timing Metrics:",
            "  T_Dwell = t_keyup - t_keydown",
            "  T_Flight = t_keydown(i) - t_keyup(i-1)",
            "• Genuine Human Typist:",
            "  T_Flight ∈ [60ms, 300ms] with natural cadence variation.",
            "• Programmatic Script / Paste Injection:",
            "  T_Flight ≤ 2.5 ms (often exactly 0ms DOM value assignment)."
        ]),
        ("Web Worker Ring Buffer Engine", ORANGE, [
            "• Multi-Threaded Decoupling:",
            "  Biometric computation executed in an isolated background Web Worker.",
            "• High-Performance Data Transfer:",
            "  Zero-copy postMessage transfers via 128-sample circular ring buffer.",
            "• Zero UI Responsiveness Lag:",
            "  Main-thread CPU utilization maintained under 0.4% at steady 60 FPS.",
            "• Cross-Platform Support:",
            "  Tested live on mobile touch gestures & desktop mouse interfaces."
        ])
    ]

    for i, (title, col_rgb, bullets) in enumerate(bio_cards):
        c_left = 0.89 + i * 3.95
        card = add_card(s7, c_left, 2.25, 3.75, 4.45)
        tf = card.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col_rgb

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.name = "Arial"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 8: 06 / METHODOLOGY & IMPLEMENTATION STATUS
    # =========================================================================
    s8 = prs.slides[7]
    for sh in list(s8.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s8)
    setup_header(s8, "06 / METHODOLOGY & TIMELINE", "Incremental Prototype Model & Completion Status")

    # Progress Bar Card
    prog_card = add_card(s8, 0.89, 1.45, 11.55, 0.90, bg_rgb=WHITE)
    tf_pr = prog_card.text_frame
    p_pr = tf_pr.paragraphs[0]
    p_pr.text = "Development Timeline: September - October 2026   |   Progress: 100% Core Engine & Defense Verified"
    p_pr.font.name = "Arial"
    p_pr.font.size = Pt(11.5)
    p_pr.font.bold = True
    p_pr.font.color.rgb = GREEN

    p_pr2 = tf_pr.add_paragraph()
    p_pr2.text = "Lifecycle: Analysis  →  Data Generation  →  Model Training  →  Algorithmic Engines  →  Flask REST API  →  UI & Honeypot  →  Verification"
    p_pr2.font.name = "Arial"
    p_pr2.font.size = Pt(10)
    p_pr2.font.color.rgb = MUTED

    # Done vs Pending Cards
    c_done = add_card(s8, 0.89, 2.50, 5.65, 4.25)
    tf_d = c_done.text_frame
    p_dt = tf_d.paragraphs[0]
    p_dt.text = "Attained Deliverables (Done - 100% Verified)"
    p_dt.font.name = "Arial"
    p_dt.font.size = Pt(13)
    p_dt.font.bold = True
    p_dt.font.color.rgb = GREEN

    done_items = [
        ("4 Telemetry CSV Datasets:", "Generated and validated 9,000 synthetic rows across login biometrics, card velocity, and UPI transactions."),
        ("3 Trained XGBoost Classifiers:", "Trained models achieving ROC-AUC ≥ 0.9995 with SMOTE class rebalancing and hyperparameter optimization."),
        ("Algorithmic Heuristic Engines:", "Implemented 60Hz Shannon entropy H(D), Haversine spacetime velocity, and Levenshtein VPA matching."),
        ("Production REST APIs & Frontends:", "Exposed 9 Flask endpoints, 5 responsive portals, and interactive Chrome Extension bot simulator."),
        ("Automated Benchmark Test Suite:", "100.00% detection accuracy on test_bot_csv.py (10/10 attack traces perfectly separated).")
    ]
    for h, b in done_items:
        p_h = tf_d.add_paragraph()
        p_h.text = "✔ " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf_d.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE

    c_pen = add_card(s8, 6.75, 2.50, 5.65, 4.25)
    tf_p = c_pen.text_frame
    p_pt = tf_p.paragraphs[0]
    p_pt.text = "Future Milestones (Production Scaling)"
    p_pt.font.name = "Arial"
    p_pt.font.size = Pt(13)
    p_pt.font.bold = True
    p_pt.font.color.rgb = ORANGE

    pending_items = [
        ("Signed Mobile SDK Signals:", "Hardware-backed cryptographic HMAC tagging of live camera QR optics for native Android/iOS UPI apps."),
        ("Gateway Shadow Integration:", "Production Envoy/Kong proxy configuration for transparent upstream honeypot tarpit routing."),
        ("Mule Account Graph Intelligence:", "Deploying Neo4j to track and freeze multi-hop beneficiary money laundering velocity across nodes."),
        ("Automated Drift Retraining:", "Continuous feedback loop ingesting bank dispute data into fraud_labels.csv for online model updating."),
        ("Production Containerization:", "Dockerized orchestration and ONNX Runtime quantization for sub-millisecond edge model inference.")
    ]
    for h, b in pending_items:
        p_h = tf_p.add_paragraph()
        p_h.text = "→ " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf_p.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 9: 07 / SYSTEM IMPLEMENTATION & WORKING MODEL
    # =========================================================================
    s9 = prs.slides[8]
    for sh in list(s9.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s9)
    setup_header(s9, "07 / SYSTEM IMPLEMENTATION & ARCHITECTURE", "REST APIs, Microservices & Active Deception Pipeline")

    # Top Status Badge
    badge_impl = add_card(s9, 0.89, 1.45, 11.55, 0.65, bg_rgb=WHITE)
    tf_bi = badge_impl.text_frame
    p_bi = tf_bi.paragraphs[0]
    p_bi.text = "9 Flask REST Endpoints  |  Sub-2ms Latency  |  Core Stack: Flask, XGBoost, scikit-learn, NumPy, pandas, Gunicorn, Selenium"
    p_bi.font.name = "Arial"
    p_bi.font.size = Pt(10.5)
    p_bi.font.bold = True
    p_bi.font.color.rgb = CYAN

    # 3 Architectural Columns
    arch_cols = [
        ("Sensors & UI (Frontend)", CYAN, [
            "• 60Hz Mouse entropy circular buffer",
            "• Inter-key keystroke flight times sensor",
            "• AudioManager telephony call state hook",
            "• Virtual display / AnyDesk flag detector",
            "• Submits JSON payload via fetch() API",
            "• Chrome Extension Bot Simulator support"
        ]),
        ("Flask API Core (Backend)", NAVY, [
            "• POST /api/v1/auth/login (Biometrics & IP)",
            "• POST /api/v1/upi/evaluate (Multi-modal risk)",
            "• POST /api/v1/card/verify (Haversine velocity)",
            "• POST /api/v1/test-bot-sample (Benchmarking)",
            "• Sub-15ms rule engines: Haversine & Levenshtein",
            "• 4-Tier decision switch enforcement"
        ]),
        ("Ghost State (Active Honeypot)", PURPLE, [
            "• Synthetic ledger balance (₹50,000 decoy funds)",
            "• 2,400ms Proof-of-Work tarpit stall challenge",
            "• Silent WebRTC STUN IP capture (103.21.14.88)",
            "• Intercepts mule wire: mule_sweep01@okaxis",
            "• Returns deterministic NPCI_ERR_ZM error",
            "• Exports audit trail to forensic CSV ledger"
        ])
    ]

    for i, (title, col_rgb, bullets) in enumerate(arch_cols):
        c_left = 0.89 + i * 3.95
        card = add_card(s9, c_left, 2.25, 3.75, 4.45)
        tf = card.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col_rgb

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.name = "Arial"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 10: 08 / VERIFICATION & ATTACK BENCHMARK MATRIX
    # =========================================================================
    s10 = prs.slides[9]
    for sh in list(s10.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s10)
    setup_header(s10, "08 / VERIFICATION & ATTACK BENCHMARKS", "Attack Scenario Benchmark Matrix & Model Performance")

    # Table of 8 Scenarios (8 rows x 5 cols)
    t_shape10 = s10.shapes.add_table(8, 5, Inches(0.89), Inches(1.45), Inches(11.55), Inches(3.70))
    table10 = t_shape10.table
    table10.columns[0].width = Inches(2.65)
    table10.columns[1].width = Inches(2.95)
    table10.columns[2].width = Inches(1.30)
    table10.columns[3].width = Inches(1.65)
    table10.columns[4].width = Inches(3.00)

    bench_data = [
        ("Attack Test Scenario", "Trigger Telemetry / Sensor", "Evaluated P", "Enforced Action", "Target Defensive Outcome"),
        ("1. Clean Genuine Payment", "Normal biometrics, trusted device", "0.0002", "Approve", "Zero friction instant settlement"),
        ("2. Call + Gallery QR", "AudioManager active, file stream", "0.6200", "Friction", "5-second mandatory warning modal"),
        ("3. Collect + Active Call", "Inbound pull request + live call", "0.9450", "Block", "Halts coercive fund transfer"),
        ("4. Screen Share + Call", "AnyDesk virtual display hook", "0.9920", "Block", "Blinds PIN keypad display layer"),
        ("5. Typo-Squatted VPA", "Levenshtein similarity ≥ 0.75", "0.8950", "Block", "Flags look-alike brand impersonation"),
        ("6. Impossible Travel", "Haversine speed > 650 mph", "0.9840", "Block", "Rejects physical spacetime anomaly"),
        ("7. Automated Bot Attack", "Mouse entropy < 0.60, 0ms flight", "0.9960", "Honeypot", "2,400ms PoW tarpit & mule capture")
    ]

    for r_idx, r_vals in enumerate(bench_data):
        for c_idx, val in enumerate(r_vals):
            cell = table10.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                p.font.size = Pt(10)
                p.font.bold = True
                p.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
            else:
                p.font.size = Pt(9.0)
                p.font.color.rgb = SLATE
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else CARD_BG
                if c_idx == 3:
                    p.font.bold = True
                    if val == "Approve":
                        p.font.color.rgb = GREEN
                    elif val == "Friction":
                        p.font.color.rgb = ORANGE
                    elif val == "Block":
                        p.font.color.rgb = RED
                    elif val == "Honeypot":
                        p.font.color.rgb = PURPLE

    # 4 Metric Cards below Table
    metrics = [
        ("Login ROC-AUC", "0.9995", CYAN),
        ("Card Physics ROC-AUC", "1.0000", PURPLE),
        ("Unified UPI ROC-AUC", "1.0000", GREEN),
        ("Inference Latency", "1.7 ms", ORANGE)
    ]
    for i, (m_name, m_val, m_col) in enumerate(metrics):
        m_left = 0.89 + i * 2.95
        card = add_card(s10, m_left, 5.30, 2.75, 1.40, bg_rgb=WHITE)
        tf = card.text_frame
        p_mn = tf.paragraphs[0]
        p_mn.text = m_name
        p_mn.font.name = "Arial"
        p_mn.font.size = Pt(10)
        p_mn.font.bold = True
        p_mn.font.color.rgb = MUTED
        p_mn.alignment = PP_ALIGN.CENTER

        p_mv = tf.add_paragraph()
        p_mv.text = m_val
        p_mv.font.name = "Arial"
        p_mv.font.size = Pt(18)
        p_mv.font.bold = True
        p_mv.font.color.rgb = m_col
        p_mv.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 11: 09 / CONCLUSION & JUSTIFICATION OF OBJECTIVES
    # =========================================================================
    s11 = prs.slides[10]
    for sh in list(s11.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s11)
    setup_header(s11, "09 / CONCLUSION & JUSTIFICATION", "Defense Validation, Deception Breakthrough & Future Scope")

    # Card 1: Justification of Objectives
    c11_left = add_card(s11, 0.89, 1.45, 5.65, 5.25)
    tf_11l = c11_left.text_frame
    p = tf_11l.paragraphs[0]
    p.text = "Justification of Objectives (Achieved)"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GREEN

    just_points = [
        ("All 8 Attack Scenarios Verified:", "Produced expected deterministic and proportional actions across legitimate users, social engineering calls, and automated bot injections."),
        ("Unified Multi-Rail Pipeline:", "Successfully evaluates login, card velocity, and UPI risk within a sub-2ms latency envelope suitable for high-volume core banking."),
        ("Active Honeypot Intelligence Extraction:", "Traps malicious bot actors in a 2,400ms tarpit, harvesting origin IPs (103.21.14.88) and intercepting mule accounts (mule_sweep01@okaxis)."),
        ("100% Benchmark Separation:", "Achieved 100.00% detection accuracy on test_bot_csv.py with zero false positive disruptions for legitimate users.")
    ]
    for h, b in just_points:
        p_h = tf_11l.add_paragraph()
        p_h.text = "✔ " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf_11l.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE

    # Card 2: Future Scope
    c11_right = add_card(s11, 6.75, 1.45, 5.65, 5.25)
    tf_11r = c11_right.text_frame
    p = tf_11r.paragraphs[0]
    p.text = "Future Scope & Production Hardening"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    future_points = [
        ("Mule Account Graph Intelligence:", "Deploying Neo4j graph database to freeze multi-hop beneficiary laundering syndicates and track coordinated fraud networks."),
        ("Signed Mobile SDK Signals:", "Hardware-backed cryptographic HMAC tagging of live camera QR optics for native Android/iOS banking applications."),
        ("Distributed Redis Velocity Synchronization:", "Multi-region cluster synchronization for high-throughput distributed gateway infrastructure."),
        ("Continuous Drift Retraining Loop:", "Automated feedback pipeline ingesting bank dispute and chargeback data into fraud_labels.csv for online model updating.")
    ]
    for h, b in future_points:
        p_h = tf_11r.add_paragraph()
        p_h.text = "→ " + h
        p_h.font.name = "Arial"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY

        p_b = tf_11r.add_paragraph()
        p_b.text = "   " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 12: 10 / REFERENCES & CITED STANDARDS
    # =========================================================================
    s12 = prs.slides[11]
    for sh in list(s12.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s12)
    setup_header(s12, "10 / REFERENCES & STANDARDS", "Academic Literature, Standards & Regulatory Frameworks")

    c12_left = add_card(s12, 0.89, 1.45, 5.65, 5.25)
    tf_12l = c12_left.text_frame
    p = tf_12l.paragraphs[0]
    p.text = "Academic & Research Publications"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY

    acad_refs = [
        "1. Shannon, C.E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal, 27(3), 379–423.",
        "2. Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. ACM SIGKDD, 785–794.",
        "3. Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. Soviet Physics Doklady.",
        "4. Sinnott, R.W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159."
    ]
    for r in acad_refs:
        p_r = tf_12l.add_paragraph()
        p_r.text = r
        p_r.font.name = "Arial"
        p_r.font.size = Pt(10)
        p_r.font.color.rgb = SLATE

    c12_right = add_card(s12, 6.75, 1.45, 5.65, 5.25)
    tf_12r = c12_right.text_frame
    p = tf_12r.paragraphs[0]
    p.text = "Regulatory Frameworks & Technical Specs"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN

    reg_refs = [
        "5. Chawla, N.V., Bowyer, K.W., Hall, L.O., & Kegelmeyer, W.P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. JAIR.",
        "6. Reserve Bank of India (2021). Master Directions on Digital Payment Security Controls. RBI/2020-21/74.",
        "7. Digital Personal Data Protection (DPDP) Act, 2023; NPCI Unified Payments Interface (UPI) Guidelines.",
        "8. Project Aegis System Architecture & Gap Analysis Specifications, School of Computer Science, UPES (October 2026)."
    ]
    for r in reg_refs:
        p_r = tf_12r.add_paragraph()
        p_r.text = r
        p_r.font.name = "Arial"
        p_r.font.size = Pt(10)
        p_r.font.color.rgb = SLATE

    # =========================================================================
    # SLIDE 13: QUESTIONS & DISCUSSION
    # =========================================================================
    s13 = prs.slides[12]
    for sh in list(s13.shapes):
        if sh.name not in ["Picture 7", "Picture 8", "Picture 9"]:
            sp_p = sh._element
            sp_p.getparent().remove(sp_p)
    add_footer(s13)
    setup_header(s13, "DISCUSSION & EVALUATION", "Questions & Live Demonstration")

    card_q = add_card(s13, 2.50, 1.85, 8.33, 4.45, bg_rgb=WHITE)
    tf_q = card_q.text_frame
    p_q = tf_q.paragraphs[0]
    p_q.text = "Questions & Feedback"
    p_q.font.name = "Arial"
    p_q.font.size = Pt(22)
    p_q.font.bold = True
    p_q.font.color.rgb = NAVY
    p_q.alignment = PP_ALIGN.CENTER

    p_qs = tf_q.add_paragraph()
    p_qs.text = "Live Interactive Demonstration Ready"
    p_qs.font.name = "Arial"
    p_qs.font.size = Pt(13)
    p_qs.font.bold = True
    p_qs.font.color.rgb = ORANGE
    p_qs.alignment = PP_ALIGN.CENTER

    demo_bullets = [
        "• Web Application Demo: http://127.0.0.1:5000/demo (8 Attack Scenarios)",
        "• Chrome Extension Bot Simulator: 60Hz Real-Time Biometric Injection",
        "• Automated Benchmark Test Suite: python test_bot_csv.py (10/10 Traces Passing)",
        "• Decoy Wire Intercept: mule_sweep01@okaxis (₹75,000 stalled in 2,400ms tarpit)"
    ]
    for b in demo_bullets:
        p_b = tf_q.add_paragraph()
        p_b.text = b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = SLATE
        p_b.alignment = PP_ALIGN.CENTER

    p_qc = tf_q.add_paragraph()
    p_qc.text = "\nSchool of Computer Science • UPES Dehradun"
    p_qc.font.name = "Arial"
    p_qc.font.size = Pt(11)
    p_qc.font.color.rgb = MUTED
    p_qc.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 14: THANK YOU (Closing Slide)
    # =========================================================================
    s14 = prs.slides[13]
    add_footer(s14)
    card_ty = add_card(s14, 2.50, 1.80, 8.33, 4.40, bg_rgb=WHITE)
    tf_ty = card_ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU"
    p_ty.font.name = "Arial"
    p_ty.font.size = Pt(40)
    p_ty.font.bold = True
    p_ty.font.color.rgb = NAVY
    p_ty.alignment = PP_ALIGN.CENTER

    p_sub = tf_ty.add_paragraph()
    p_sub.text = "Project Aegis: Unified ML-Driven Fraud Detection & Deceptive Honeypot"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ORANGE
    p_sub.alignment = PP_ALIGN.CENTER

    p_team = tf_ty.add_paragraph()
    p_team.text = "\nAayush Tripathi (590017378)   •   Akhil Pundir (590016767)   •   Aryan Singh (590017232)"
    p_team.font.name = "Arial"
    p_team.font.size = Pt(13)
    p_team.font.bold = True
    p_team.font.color.rgb = NAVY
    p_team.alignment = PP_ALIGN.CENTER

    p_sch = tf_ty.add_paragraph()
    p_sch.text = "B.Tech CSE / BCA Sem 5 Project  |  School of Computer Science • UPES Dehradun"
    p_sch.font.name = "Arial"
    p_sch.font.size = Pt(11)
    p_sch.font.color.rgb = MUTED
    p_sch.alignment = PP_ALIGN.CENTER

    p_live = tf_ty.add_paragraph()
    p_live.text = "● Live Prototype & Chrome Bot Extension Ready for Demonstration"
    p_live.font.name = "Arial"
    p_live.font.size = Pt(11)
    p_live.font.bold = True
    p_live.font.color.rgb = GREEN
    p_live.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Master presentation generated and saved to: {output_path}")

if __name__ == "__main__":
    template = r"C:\Users\dell\Downloads\Template Synopsis Presentation_Original_Backup.pptx"
    out1 = r"C:\Users\dell\Downloads\Template Synopsis Presentation.pptx"
    out2 = r"C:\Users\dell\Downloads\Project_Aegis_UPES_Master_Presentation.pptx"
    out3 = r"c:\Users\dell\Desktop\project 2\Project_Aegis_UPES_Master_Presentation.pptx"

    build_presentation(template, out2)
    shutil.copy(out2, out1)
    shutil.copy(out2, out3)
    print("All copies updated successfully!")
