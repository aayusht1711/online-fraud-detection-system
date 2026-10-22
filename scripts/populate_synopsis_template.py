import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Colors
UPES_BLUE = RGBColor(0x0A, 0x25, 0x40)
ACCENT_ORANGE = RGBColor(0xF2, 0x8C, 0x28)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)

def populate_synopsis(src_path, dst_path):
    print(f"Loading template: {src_path}")
    prs = pptx.Presentation(src_path)

    # Global footer replacement
    project_footer = "Project Aegis: Fraud Detection & Honeypot Platform | UPES"
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    if "<<Project Title>>" in p.text:
                        p.text = p.text.replace("<<Project Title>> , BCA Sem 5 Project", project_footer)
                        p.text = p.text.replace("<<Project Title>>", "Project Aegis")

    # Slide 2: Title and Team
    s2 = prs.slides[1]
    for sh in s2.shapes:
        if sh.name == "TextBox 2" and sh.has_text_frame:
            sh.text_frame.clear()
            p0 = sh.text_frame.paragraphs[0]
            p0.text = "Synopsis Presentation"
            p0.font.size = Pt(24)
            p0.font.bold = True
            p0.font.color.rgb = ACCENT_ORANGE
            
            p1 = sh.text_frame.add_paragraph()
            p1.text = "Project Aegis: ML Fraud Detection & Deceptive Honeypot"
            p1.font.size = Pt(28)
            p1.font.bold = True
            p1.font.color.rgb = UPES_BLUE
            
        elif sh.name == "TextBox 3" and sh.has_text_frame:
            sh.text_frame.clear()
            p0 = sh.text_frame.paragraphs[0]
            p0.text = "Presented By:"
            p0.font.size = Pt(16)
            p0.font.bold = True
            p0.font.color.rgb = UPES_BLUE
            
            team = [
                "Aayush Tripathi, SAP ID: 590017378",
                "Akhil Pundir, SAP ID: 590016767",
                "Aryan Singh, SAP ID: 590017232"
            ]
            for m in team:
                p = sh.text_frame.add_paragraph()
                p.text = m
                p.font.size = Pt(14)
                p.font.color.rgb = DARK_GRAY

    # Slide 3: Table of Contents
    s3 = prs.slides[2]
    for sh in s3.shapes:
        if sh.name == "Rectangle 1" and sh.has_text_frame:
            sh.text_frame.clear()
            items = [
                "1. Introduction & Motivation (UPI & Card Security Landscape)",
                "2. Literature Survey & Theoretical Foundations",
                "3. Problem Statement & Research Gaps",
                "4. Research Methodology & Multi-Engine Architecture",
                "5. Implementation & Progress Chart (100% Core Engine Verified)",
                "6. Results, Honeypot Tarpit Benchmarks & Conclusion",
                "7. References & Regulatory Standards"
            ]
            for i, it in enumerate(items):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = it
                p.font.size = Pt(14)
                p.font.color.rgb = UPES_BLUE

    # Slide 4: Introduction
    s4 = prs.slides[3]
    for sh in s4.shapes:
        if sh.name == "Content Placeholder 3" and sh.has_text_frame:
            sh.text_frame.clear()
            bullets = [
                "Digital Payments Revolution: UPI processes over 14 billion monthly transactions in India, creating immense vulnerability to real-time automated fraud.",
                "Emerging Threat Vectors: Attackers exploit social engineering (active phone calls, remote screen-share tools), look-alike typo-squatted VPAs, and automated bot injections.",
                "Limitations of Traditional Defense: Static WAFs and rule engines return immediate HTTP 403 Forbidden errors, instantly alerting attackers to rotate residential proxies and user-agents.",
                "Project Aegis Paradigm: A unified multi-modal platform fusing 3 XGBoost classifiers, 60Hz client behavioral biometrics, and active honeypot tarpit deception."
            ]
            for i, b in enumerate(bullets):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = "* " + b
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY

    # Slide 5: Literature Survey
    s5 = prs.slides[4]
    for sh in s5.shapes:
        if sh.name == "Content Placeholder 5" and sh.has_text_frame:
            sh.text_frame.clear()
            bullets = [
                "Shannon Directional Entropy (Shannon, 1948): Quantifies behavioral randomness in human cursor movement H(D) in [2.4, 3.8] vs bot straight-line scripts H(D) < 0.60.",
                "Gradient Tree Boosting (Chen & Guestrin, XGBoost 2016): Superior tabular classification on high-dimensional financial transaction features with sub-2ms latency.",
                "String Similarity & Geodesy: Levenshtein distance (1966) for VPA typo-squatting detection; Haversine formula (Sinnott, 1984) for spacetime velocity violation (>650 mph).",
                "Imbalanced Learning & Regulation: SMOTE (Chawla et al., 2002); RBI Master Directions on Payment Security (2021); DPDP Act compliance (2023)."
            ]
            for i, b in enumerate(bullets):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = "* " + b
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY

    # Slide 7: Problem Statement
    s7 = prs.slides[6]
    for sh in s7.shapes:
        if sh.name == "Content Placeholder 3" and sh.has_text_frame:
            sh.text_frame.clear()
            bullets = [
                "Research Gap 1: Existing payment gateways lack client-side micro-behavioral awareness, unable to differentiate human mouse/keyboard cadence from headless browser bots.",
                "Research Gap 2: Binary block mechanisms alert attackers, accelerating bot evasion strategies. There is a lack of active deceptive honeypot tarpits in payment switching.",
                "Core Problem Statement: Design and engineer a sub-2ms multi-modal fraud detection system that fuses contextual heuristic rules, machine learning inference, and cryptographic honeypot tarpit stalling.",
                "Core Objectives: Achieve 99.9%+ ROC-AUC across login, card velocity, and UPI transactions, with 100% automated bot trap verification and forensic exfiltration interception."
            ]
            for i, b in enumerate(bullets):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = "* " + b
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY

    # Slide 8: Research Methodology
    s8 = prs.slides[7]
    for sh in s8.shapes:
        if sh.name == "Content Placeholder 3" and sh.has_text_frame:
            sh.text_frame.clear()
            bullets = [
                "Pipeline Architecture: Client 60Hz Telemetry Sensor -> Flask REST API (9 Endpoints) -> Multi-Modal Inference Engine -> 4-Tier Proportionate Decision Switch.",
                "Engine Fusion: 3 trained XGBoost classifiers + Haversine Geo Engine + Levenshtein VPA Checker + Shannon Entropy H(D) Analyzer.",
                "4-Tier Enforcement: Tier 1: Approve (P < 0.30) | Tier 2: Friction 5s PIN cooldown (0.30 <= P <= 0.70) | Tier 3: Block (P > 0.70) | Tier 4: Honeypot Tarpit (Bots).",
                "Datasets: 4 specialized forensic datasets covering Login biometrics, Card velocity, Unified UPI transactions (9,000+ samples), and Decoy mule wire captures."
            ]
            for i, b in enumerate(bullets):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = "* " + b
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY

    # Slide 9: Progress Chart
    s9 = prs.slides[8]
    # Add a clean text box for progress details
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    progress_items = [
        "Status: 100% Core Engine & Defense Verified (September - October 2026)",
        "Completed Milestones:",
        "  [x] 4 CSV Forensic Datasets & 3 Trained XGBoost Models (ROC-AUC >= 0.9995)",
        "  [x] 60Hz Real-Time Shannon Directional Entropy H(D) & Keystroke Flight Sensor",
        "  [x] 2,400ms Proof-of-Work Honeypot Tarpit, Ghost Banking Sandbox & Mule Interceptor",
        "  [x] 9 Flask Production REST Endpoints, 5 Portal Pages, Chrome Bot Extension Simulator",
        "  [x] 10/10 Automated Attack Test Traces Verified with 100% Accuracy on test_bot_csv.py",
        "Future Enhancements:",
        "  [ ] Native Mobile SDK Integration for Android/iOS UPI Apps",
        "  [ ] Distributed Redis Velocity Cache & Graph Database for Mule Syndicates (Neo4j)"
    ]
    for i, p_str in enumerate(progress_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = p_str
        p.font.size = Pt(13)
        if "Status:" in p_str or "Milestones:" in p_str:
            p.font.bold = True
            p.font.color.rgb = UPES_BLUE
        else:
            p.font.color.rgb = DARK_GRAY

    # Slide 10: Conclusion
    s10 = prs.slides[9]
    for sh in s10.shapes:
        if sh.name == "Content Placeholder 3" and sh.has_text_frame:
            sh.text_frame.clear()
            bullets = [
                "Successful Validation: All 8 real-time attack scenarios executed intended proportionate responses without interrupting legitimate users.",
                "Breakthrough Deception: Deceptive honeypot tarpit successfully stalled automated bots for 2,400ms in ghost sandboxes, preventing proxy recycling and logging forensic audit trails.",
                "Sub-2ms Decision Latency: High throughput pipeline capable of handling high-volume instant payment infrastructure demands.",
                "Production Ready: Validated via automated test suites (test_bot_csv.py) and interactive browser/extension interfaces."
            ]
            for i, b in enumerate(bullets):
                p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
                p.text = "* " + b
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY

    # Slide 11: References
    s11 = prs.slides[10]
    tb11 = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.5))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    refs = [
        "1. Shannon, C.E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.",
        "2. Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. ACM SIGKDD.",
        "3. Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals.",
        "4. Sinnott, R.W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.",
        "5. Chawla, N.V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique. JAIR.",
        "6. Reserve Bank of India (2021). Master Directions on Digital Payment Security Controls.",
        "7. Digital Personal Data Protection (DPDP) Act, 2023; NPCI Unified Payments Interface Guidelines."
    ]
    for i, r_str in enumerate(refs):
        p = tf11.paragraphs[0] if i == 0 else tf11.add_paragraph()
        p.text = r_str
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY

    prs.save(dst_path)
    print(f"Successfully saved updated synopsis presentation to: {dst_path}")

if __name__ == "__main__":
    src = r"C:\Users\dell\Downloads\Template Synopsis Presentation.pptx"
    dst1 = r"C:\Users\dell\Downloads\Project_Aegis_Synopsis_Template_Updated.pptx"
    dst2 = r"c:\Users\dell\Desktop\project 2\Project_Aegis_Synopsis_Template_Updated.pptx"
    
    populate_synopsis(src, dst1)
    shutil.copy(dst1, dst2)
    print(f"Copied to project directory: {dst2}")
