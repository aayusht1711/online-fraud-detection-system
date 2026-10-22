import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Color Palette
NAVY = RGBColor(0x12, 0x30, 0x4A)      # #12304A
ORANGE = RGBColor(0xF2, 0x8C, 0x28)    # #F28C28
CYAN = RGBColor(0x2E, 0xA3, 0xF2)      # #2EA3F2
GRAY = RGBColor(0x44, 0x44, 0x44)      # #444444
WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # #FFFFFF

def set_text_block(shape, paragraphs_data, clear_first=True):
    """
    paragraphs_data: list of tuples:
      (text, font_size_pt, is_bold, color_rgb, alignment)
    """
    tf = shape.text_frame
    if clear_first:
        tf.clear()
    
    for i, p_info in enumerate(paragraphs_data):
        text, size_pt, bold, color, align = p_info
        if clear_first and i == 0 and len(tf.paragraphs) > 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        p.text = text
        if align is not None:
            p.alignment = align
        if p.runs:
            run = p.runs[0]
            run.font.name = "Arial"
            if size_pt is not None:
                run.font.size = Pt(size_pt)
            if bold is not None:
                run.font.bold = bold
            if color is not None:
                run.font.color.rgb = color

def update_presentation(src_path, dst_path):
    print(f"Loading presentation from: {src_path}")
    prs = pptx.Presentation(src_path)

    # ==========================================
    # SLIDE 1: TITLE
    # ==========================================
    s1 = prs.slides[0]
    # Shape 1 (Text 1): Major Project
    set_text_block(s1.shapes[1], [("Major Project", 17.0, True, CYAN, None)])
    # Shape 3 (Text 2): Project Aegis
    set_text_block(s1.shapes[3], [("Project Aegis", 27.0, True, NAVY, None)])
    # Shape 4 (Text 3): Subtitle
    set_text_block(s1.shapes[4], [
        ("A Unified ML-Driven Fraud Detection and Deceptive Honeypot", 18.0, True, ORANGE, None),
        ("Defence Platform for UPI and Card Payments", 18.0, True, ORANGE, None)
    ])
    # Shape 5 (Text 4): B.Tech CSE
    set_text_block(s1.shapes[5], [("B.Tech CSE | School of Computer Science | UPES Dehradun", 13.0, False, GRAY, None)])
    # Shape 6 (Text 5): Team
    set_text_block(s1.shapes[6], [
        ("Presented by:", 12.0, False, NAVY, None),
        ("590017378 - Aayush Tripathi", 12.0, False, NAVY, None),
        ("590016767 - Akhil Pundir", 12.0, False, NAVY, None),
        ("590017232 - Aryan Singh", 12.0, False, NAVY, None)
    ])
    # Shape 7 (Text 6): Mentored By
    set_text_block(s1.shapes[7], [
        ("Mentored By:", 12.0, True, NAVY, None),
        ("School of Computer Science Faculty Guide", 12.0, True, NAVY, None)
    ])

    # ==========================================
    # SLIDE 2: CONTENT (AGENDA) - Keep perfectly styled
    # ==========================================
    s2 = prs.slides[1]
    set_text_block(s2.shapes[1], [("Content", 17.0, True, CYAN, None)])
    set_text_block(s2.shapes[3], [
        ("Introduction", 15.0, False, NAVY, None),
        ("Literature Review", 15.0, False, NAVY, None),
        ("Objectives", 15.0, False, NAVY, None),
        ("Methodology", 15.0, False, NAVY, None),
        ("Working Model", 15.0, False, NAVY, None),
        ("Results", 15.0, False, NAVY, None),
        ("Conclusion", 15.0, False, NAVY, None),
        ("References", 15.0, False, NAVY, None)
    ])
    set_text_block(s2.shapes[4], [("MID-TERM", 14.0, True, ORANGE, None)])

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    s3 = prs.slides[2]
    set_text_block(s3.shapes[1], [("Introduction", 17.0, True, CYAN, None)])
    # Card 1: Technical background
    set_text_block(s3.shapes[4], [("Technical background", 13.0, True, ORANGE, None)])
    set_text_block(s3.shapes[5], [
        ("Real-time UPI & card settlement leaves sub-second windows for fraud interception.", 11.0, False, NAVY, None),
        ("Attacks exploit social engineering (active calls, remote desktop) and automated bot scripts.", 11.0, False, NAVY, None)
    ])
    # Card 2: Algorithms & telemetry
    set_text_block(s3.shapes[7], [("Algorithms & telemetry", 13.0, True, ORANGE, None)])
    set_text_block(s3.shapes[8], [
        ("Three XGBoost tree ensembles fused with real-time heuristic contextual engines.", 11.0, False, NAVY, None),
        ("60Hz Shannon directional entropy H(D) < 0.60 & keystroke flight Tf <= 2.5ms detect bots.", 11.0, False, NAVY, None),
        ("Haversine spacetime velocity (>650 mph) and Levenshtein VPA typo-squatting (>=0.75).", 11.0, False, NAVY, None)
    ])
    # Card 3: Motivation & problem
    set_text_block(s3.shapes[10], [("Motivation & problem", 13.0, True, ORANGE, None)])
    set_text_block(s3.shapes[11], [
        ("Rule-only systems miss multi-modal context; static 403 blocks trigger fast bot proxy rotation.", 11.0, False, NAVY, None),
        ("Aegis traps bots in a 2,400ms cryptographic tarpit while preserving genuine user velocity.", 11.0, False, NAVY, None),
        ("Proportionate multi-tier responses eliminate friction for 98%+ of legitimate transactions.", 11.0, False, NAVY, None)
    ])
    # Card 4: Applications
    set_text_block(s3.shapes[13], [("Applications", 13.0, True, ORANGE, None)])
    set_text_block(s3.shapes[14], [
        ("Banks, UPI PSPs (GPay, PhonePe, Paytm), payment switches, and enterprise SOC platforms.", 11.0, False, NAVY, None)
    ])
    # Card 5: Datasets & input
    set_text_block(s3.shapes[16], [("Datasets & input", 13.0, True, ORANGE, None)])
    set_text_block(s3.shapes[17], [
        ("4 datasets: Login telemetry, Card velocity, Unified UPI (9,000+ total rows) & Decoy intercepts.", 11.0, False, NAVY, None),
        ("Live 60Hz biometric telemetry stream + JSON payment payloads via 9 REST API endpoints.", 11.0, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 4: LITERATURE REVIEW
    # ==========================================
    s4 = prs.slides[3]
    set_text_block(s4.shapes[1], [("Literature Review", 17.0, True, CYAN, None)])
    set_text_block(s4.shapes[3], [("Related work & foundations", 13.0, True, ORANGE, None)])
    set_text_block(s4.shapes[4], [
        ("XGBoost: Chen & Guestrin, 2016; Shannon Directional Entropy: Shannon, 1948.", 11.0, False, NAVY, None),
        ("Levenshtein distance (1966); Haversine spherical geodesy (Sinnott, 1984); SMOTE (Chawla, 2002).", 11.0, False, NAVY, None),
        ("Regulatory guidelines: RBI Master Directions (2021), DPDP Act (2023), NPCI UPI Standards.", 11.0, False, NAVY, None)
    ])
    set_text_block(s4.shapes[5], [
        ("Inference: Tree ensembles fit tabular fraud; dynamic biometrics and honeypot tarpits close perimeter gaps.", 11.0, True, NAVY, None)
    ])
    # SWOT
    set_text_block(s4.shapes[7], [("Strengths", 13.0, True, ORANGE, None)])
    set_text_block(s4.shapes[8], [
        ("Proportionate 4-tier response; 60Hz biometric bot detection; sub-2ms inference; silent STUN IP capture.", 11.0, False, NAVY, None)
    ])
    set_text_block(s4.shapes[10], [("Weaknesses", 13.0, True, ORANGE, None)])
    set_text_block(s4.shapes[11], [
        ("Synthetic baseline data; advanced physical mouse replay attacks require multi-factor verification.", 11.0, False, NAVY, None)
    ])
    set_text_block(s4.shapes[13], [("Opportunities", 13.0, True, ORANGE, None)])
    set_text_block(s4.shapes[14], [
        ("Rising UPI scale (14B+ monthly txns); strong banking demand for active deception & bot tarpits.", 11.0, False, NAVY, None)
    ])
    set_text_block(s4.shapes[16], [("Threats", 13.0, True, ORANGE, None)])
    set_text_block(s4.shapes[17], [
        ("Headless browser botnets (Puppeteer/Stealth), residential proxy hopping, and generative phishing.", 11.0, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 5: OBJECTIVE
    # ==========================================
    s5 = prs.slides[4]
    set_text_block(s5.shapes[1], [("Objective", 17.0, True, CYAN, None)])
    set_text_block(s5.shapes[3], [("Main Objective", 16.0, True, ORANGE, None)])
    set_text_block(s5.shapes[4], [
        ("Build a real-time, explainable fraud & bot defense platform with proportionate 4-tier responses.", 14.0, False, NAVY, None)
    ])
    set_text_block(s5.shapes[5], [
        ("Approve   |   Friction (Pre-PIN Cooldown)   |   Block   |   Honeypot Tarpit", 13.0, True, CYAN, PP_ALIGN.CENTER)
    ])
    set_text_block(s5.shapes[6], [("Sub Objectives", 16.0, True, ORANGE, None)])
    set_text_block(s5.shapes[7], [
        ("1. Train 3 XGBoost fraud classifiers (Login, Card Velocity, and Unified UPI Transaction).", 11.5, False, NAVY, None),
        ("2. Engineer 60Hz Shannon directional entropy H(D) < 0.60 & keystroke flight Tf <= 2.5ms bot sensors.", 11.5, False, NAVY, None),
        ("3. Deploy Haversine spacetime travel & Levenshtein typo-squatting heuristic verification engines.", 11.5, False, NAVY, None),
        ("4. Implement 2,400ms PoW tarpit, ghost banking sandbox & decoy NPCI switch error interceptor.", 11.5, False, NAVY, None),
        ("5. Expose 9 production REST APIs and deliver an interactive SOC portal with Chrome extension simulator.", 11.5, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 6: METHODOLOGY
    # ==========================================
    s6 = prs.slides[5]
    set_text_block(s6.shapes[1], [("Methodology", 17.0, True, CYAN, None)])
    set_text_block(s6.shapes[3], [("Incremental Prototype Model", 14.0, True, NAVY, None)])
    set_text_block(s6.shapes[24], [("Timeline: September - October 2026", 12.0, False, GRAY, None)])
    set_text_block(s6.shapes[25], [("Progress: 100% Core Engine & Defense Verified", 12.0, True, ORANGE, None)])
    # Shape 26 is the progress bar fill! Set to full width 3.40 inches
    s6.shapes[27].width = s6.shapes[26].width  # 100% progress!
    
    # Done card
    set_text_block(s6.shapes[29], [("Done (100% Engine & Defense Verified)", 13.0, True, ORANGE, None)])
    set_text_block(s6.shapes[30], [
        ("* 4 telemetry CSV datasets and 3 trained XGBoost models + serialized pipelines.", 10.5, False, NAVY, None),
        ("* 60Hz Shannon biometrics engine, keystroke dynamics analyzer, Haversine & Levenshtein engines.", 10.5, False, NAVY, None),
        ("* 9 REST API endpoints, 5 responsive portals, Chrome extension bot simulator, VS Code setup.", 10.5, False, NAVY, None),
        ("* 2,400ms PoW honeypot tarpit, ghost banking sandbox, decoy wire interceptor (mule_sweep01@okaxis).", 10.5, False, NAVY, None),
        ("* Automated benchmark test suite with 100.00% detection accuracy on test_bot_csv.py.", 10.5, False, NAVY, None)
    ])
    # Pending card
    set_text_block(s6.shapes[32], [("Future Milestones", 13.0, True, ORANGE, None)])
    set_text_block(s6.shapes[33], [
        ("* Signed mobile-SDK telemetry integration for native Android/iOS banking applications.", 11.0, False, NAVY, None),
        ("* Distributed Redis cache cluster for cross-region velocity state and persistent mule graph DB.", 11.0, False, NAVY, None),
        ("* Automated CI/CD retraining loop and Kubernetes containerized edge orchestration.", 11.0, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 7: WORKING MODEL
    # ==========================================
    s7 = prs.slides[6]
    set_text_block(s7.shapes[1], [("Working Model", 17.0, True, CYAN, None)])
    set_text_block(s7.shapes[3], [("SRS completed  |  Live demo: /demo & Extension  |  10/10 Attack Benchmarks Verified", 12.0, True, NAVY, None)])
    
    # Flowchart Pipeline Boxes
    # Box 1: Client UI
    set_text_block(s7.shapes[5], [("Client UI & sensors", 10.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s7.shapes[6], [("60Hz Biometrics / JSON", 8.0, False, GRAY, PP_ALIGN.CENTER)])
    # Box 2: Flask API
    set_text_block(s7.shapes[9], [("Flask REST API", 10.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s7.shapes[10], [("9 REST endpoints", 8.0, False, GRAY, PP_ALIGN.CENTER)])
    # Box 3: Risk engines
    set_text_block(s7.shapes[13], [("Risk engines", 10.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s7.shapes[14], [("3 XGBoost + VPA + Geo + H", 8.0, False, GRAY, PP_ALIGN.CENTER)])
    # Box 4: Decision switch
    set_text_block(s7.shapes[17], [("Decision switch", 10.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s7.shapes[18], [("4 Tiers (Approve/Friction/Block/Tarpit)", 7.5, False, GRAY, PP_ALIGN.CENTER)])
    # Box 5: Honeypot + logs
    set_text_block(s7.shapes[21], [("Honeypot Tarpit", 10.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s7.shapes[22], [("2,400ms Stall + Decoy wire", 8.0, False, GRAY, PP_ALIGN.CENTER)])

    # Working modules
    set_text_block(s7.shapes[24], [("Working modules", 13.0, True, ORANGE, None)])
    set_text_block(s7.shapes[25], [
        ("* Login, Card velocity, and Unified UPI scoring engines.", 11.0, False, NAVY, None),
        ("* 60Hz Shannon directional entropy & keystroke dynamics sensor.", 11.0, False, NAVY, None),
        ("* VPA Levenshtein checker, PoW tarpit, and STUN IP attribution.", 11.0, False, NAVY, None)
    ])
    # Decision tiers
    set_text_block(s7.shapes[27], [("Decision tiers", 13.0, True, ORANGE, None)])
    set_text_block(s7.shapes[28], [
        ("* P < 0.30: Approve (Instant execution).", 11.0, False, NAVY, None),
        ("* 0.30 - 0.70: Friction (5s Pre-PIN cooldown & biometric challenge).", 11.0, False, NAVY, None),
        ("* P > 0.70: Block | Bot: Honeypot Tarpit (2,400ms PoW stall).", 11.0, False, NAVY, None)
    ])
    # Libraries
    set_text_block(s7.shapes[30], [("Libraries & Stack", 13.0, True, ORANGE, None)])
    set_text_block(s7.shapes[31], [
        ("* Flask, XGBoost, scikit-learn, NumPy, pandas, Gunicorn.", 11.0, False, NAVY, None),
        ("* math (Shannon entropy, Haversine), Levenshtein, hashlib.", 11.0, False, NAVY, None),
        ("* Selenium, Chrome Extensions API, Chart.js, Tailwind CSS.", 11.0, False, NAVY, None)
    ])
    # Communication
    set_text_block(s7.shapes[33], [("Communication & Data Flow", 13.0, True, ORANGE, None)])
    set_text_block(s7.shapes[34], [
        ("* HTTP/JSON: Browser portal & extension to Flask REST API.", 11.0, False, NAVY, None),
        ("* In-memory inference: Sub-2ms end-to-end pipeline latency.", 11.0, False, NAVY, None),
        ("* WebRTC STUN IP deanonymization & forensic CSV audit logs.", 11.0, False, NAVY, None)
    ])
    # Attained deliverables
    set_text_block(s7.shapes[36], [("Attained deliverables", 13.0, True, ORANGE, None)])
    set_text_block(s7.shapes[37], [
        ("* Production server: 9 endpoints, 5 portals, Chrome bot extension.", 11.0, False, NAVY, None),
        ("* Verified defense: 10/10 automated benchmark test cases passing.", 11.0, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 8: RESULTS
    # ==========================================
    s8 = prs.slides[7]
    set_text_block(s8.shapes[1], [("Results", 17.0, True, CYAN, None)])
    
    # Table 0: Update rows with exact styling
    table_shape = None
    for sh in s8.shapes:
        if sh.has_table:
            table_shape = sh
            break
    if table_shape:
        table = table_shape.table
        rows_data = [
            ("Scenario", "Risk P", "Action Taken"),
            ("Clean UPI payment", "0.0002", "Approve (Instant)"),
            ("Call + gallery QR", "0.6200", "Friction (5s PIN hold)"),
            ("Collect + call scam", "0.9450", "Block (Social Eng.)"),
            ("Screen share (AnyDesk)", "0.9920", "Block (Remote desktop)"),
            ("Typo-squat VPA handle", "0.8950", "Block (Levenshtein >=0.75)"),
            ("Impossible travel (>650mph)", "0.9840", "Block (Spacetime Geo)"),
            ("Bot biometrics (H < 0.60)", "0.9980", "Honeypot Tarpit (2,400ms)")
        ]
        for r_idx, r_vals in enumerate(rows_data):
            for c_idx, val in enumerate(r_vals):
                cell = table.cell(r_idx, c_idx)
                cell.text = val
                p = cell.text_frame.paragraphs[0]
                if p.runs:
                    r = p.runs[0]
                    r.font.name = "Arial"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = NAVY
                    if r_idx == 0:
                        r.font.bold = True
                        r.font.color.rgb = ORANGE

    # ROC-AUC text & bars
    set_text_block(s8.shapes[4], [("Model & Biometric Performance", 13.0, True, ORANGE, None)])
    set_text_block(s8.shapes[5], [("Login Model", 11.0, False, NAVY, None)])
    set_text_block(s8.shapes[7], [("0.9995", 10.0, True, NAVY, None)])
    set_text_block(s8.shapes[8], [("Card Model", 11.0, False, NAVY, None)])
    set_text_block(s8.shapes[10], [("1.0000", 10.0, True, NAVY, None)])
    set_text_block(s8.shapes[11], [("Unified UPI", 11.0, False, NAVY, None)])
    set_text_block(s8.shapes[13], [("1.0000", 10.0, True, NAVY, None)])
    
    # Text 12: Benchmark validation note
    set_text_block(s8.shapes[14], [
        ("Benchmark validation: 100.00% accuracy on test_bot_csv.py (10/10 test traces separated).", 10.0, True, GRAY, None)
    ])
    
    # Rule-only vs Aegis
    set_text_block(s8.shapes[16], [("Rule-only / Traditional WAF", 13.0, True, ORANGE, None)])
    set_text_block(s8.shapes[17], [
        ("Rigid binary decline; zero behavioral context; immediate 403 Forbidden alerts bots to rotate residential proxies.", 11.0, False, NAVY, None)
    ])
    set_text_block(s8.shapes[19], [("Project Aegis Platform", 13.0, True, ORANGE, None)])
    set_text_block(s8.shapes[20], [
        ("Multi-modal context fusion; proportionate 4-tier enforcement; 2,400ms PoW tarpit stalls bots and logs mule forensics.", 11.0, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 9: CONCLUSION
    # ==========================================
    s9 = prs.slides[8]
    set_text_block(s9.shapes[1], [("Conclusion", 17.0, True, CYAN, None)])
    set_text_block(s9.shapes[3], [("Justification of Objectives", 16.0, True, ORANGE, None)])
    set_text_block(s9.shapes[4], [
        ("Complete defense verification: All 8 real-time attack scenarios executed intended proportionate responses without false positives.", 12.5, False, NAVY, None),
        ("Unified multi-modal intelligence successfully fuses 3 XGBoost models, 60Hz client biometrics, and heuristic rules.", 12.5, False, NAVY, None),
        ("Validated deceptive honeypot tarpit: neutralized automated bot attacks, stalled attackers for 2,400ms, and captured IP & mule audit trails.", 12.5, False, NAVY, None),
        ("100.00% benchmark trace accuracy achieved on test_bot_csv.py; fully demonstrated live in VS Code and Chrome extension.", 12.5, False, NAVY, None)
    ])
    set_text_block(s9.shapes[5], [("Future Scope", 16.0, True, ORANGE, None)])
    set_text_block(s9.shapes[6], [
        ("Partner with banking PSPs and payment gateways to evaluate live production traffic under real-world drift.", 12.5, False, NAVY, None),
        ("Deploy signed client SDK telemetry modules for native Android and iOS mobile UPI banking applications.", 12.5, False, NAVY, None),
        ("Construct Graph Neural Network (GNN) intelligence for tracking multi-hop money-mule syndicate networks.", 12.5, False, NAVY, None),
        ("Implement ONNX Runtime quantization for sub-millisecond edge model inference and distributed tarpit scaling.", 12.5, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 10: REFERENCE
    # ==========================================
    s10 = prs.slides[9]
    set_text_block(s10.shapes[1], [("Reference", 17.0, True, CYAN, None)])
    set_text_block(s10.shapes[3], [("A: Research Specifications & Artifacts", 14.0, True, ORANGE, None)])
    set_text_block(s10.shapes[4], [
        ("Project Aegis System Architecture & Gap Analysis Specifications, UPES (October 2026).", 12.5, False, NAVY, None)
    ])
    set_text_block(s10.shapes[5], [("B: List of Cited Standards & Research Literature", 14.0, True, ORANGE, None)])
    set_text_block(s10.shapes[6], [
        ("Shannon, C.E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal, 27(3), 379-423.", 11.5, False, NAVY, None),
        ("Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. ACM SIGKDD, 785-794.", 11.5, False, NAVY, None),
        ("Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. Soviet Physics Doklady.", 11.5, False, NAVY, None),
        ("Sinnott, R.W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.", 11.5, False, NAVY, None),
        ("Chawla, N.V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique. JAIR, 16, 321-357.", 11.5, False, NAVY, None),
        ("Reserve Bank of India (2021). Master Directions on Digital Payment Security Controls; DPDP Act (2023); NPCI UPI Guidelines.", 11.5, False, NAVY, None)
    ])

    # ==========================================
    # SLIDE 11: THANK YOU
    # ==========================================
    s11 = prs.slides[10]
    set_text_block(s11.shapes[4], [("Thank You", 32.0, True, NAVY, PP_ALIGN.CENTER)])
    set_text_block(s11.shapes[5], [("Questions & Live Demonstration", 15.0, True, ORANGE, PP_ALIGN.CENTER)])

    prs.save(dst_path)
    print(f"Successfully saved updated presentation to: {dst_path}")

if __name__ == "__main__":
    src = r"C:\Users\dell\Downloads\Project_Aegis_Mid_Term_Presentation_Original_Backup.pptx"
    dst1 = r"C:\Users\dell\Downloads\Project_Aegis_Mid_Term_Presentation.pptx"
    dst2 = r"c:\Users\dell\Desktop\project 2\Project_Aegis_Mid_Term_Presentation.pptx"
    
    update_presentation(src, dst1)
    shutil.copy(dst1, dst2)
    print(f"Copied to project directory: {dst2}")
