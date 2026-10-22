import os
import sys

def update_gap_analysis():
    p = 'PROJECT_AEGIS_GAP_ANALYSIS_ARCHITECTURE_REPORT.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('**Target Systems:** UPI 2.0 Payment Rail, Card Velocity Guard, Real-Time Behavioral Risk Engine',
                  '**Target Systems:** UPI 2.0 Payment Rail, Honeypot Telemetry Engine, Real-Time Behavioral Risk Engine')
    c = c.replace("across India's Unified Payments Interface (UPI) and card payment ecosystems.",
                  "across India's Unified Payments Interface (UPI) ecosystem.")
    c = c.replace('| - Haversine Physics (>900km/h)|', '| - Shannon Entropy (H < 0.60)  |')
    c = c.replace('└── Haversine Velocity Physics Engine (>900 km/h)     └── Neo4j Graph DB (Mule Account Velocity & Fan-Out)',
                  '└── Shannon Biometrics Engine (H < 0.60)              └── Neo4j Graph DB (Mule Account Velocity & Fan-Out)')
    c = c.replace('|  ├── Model 2: Card Velocity Classifier (XGBoost)                                                                |\n', '')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", p)


def update_system_architecture():
    p = 'PROJECT_AEGIS_SYSTEM_ARCHITECTURE_REPORT.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('**Target Systems:** UPI 2.0 Payment Rail, FedWire ISO-20022, Card Velocity Guard, Real-Time SOC',
                  '**Target Systems:** UPI 2.0 Payment Rail, FedWire ISO-20022, Honeypot Telemetry Sandbox, Real-Time SOC')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", p)


def update_flowchart():
    p = 'PROJECT_AEGIS_SYSTEM_FLOWCHART_ARCHITECTURE.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('**Target Systems:** UPI 2.0 Rails, Core Banking System (CBS), NPCI Switch, Ghost Honeypot Sandbox, Card Velocity Guard',
                  '**Target Systems:** UPI 2.0 Rails, Core Banking System (CBS), NPCI Switch, Ghost Honeypot Sandbox, Behavioral Biometrics Guard')
    c = c.replace('This comprehensive architecture diagram illustrates how the three operational pillars—**UPI 2.0 Payments**, **Deceptive Login Honeypot**, and **Card Velocity Guard**—unify',
                  'This comprehensive architecture diagram illustrates how the core operational pillars—**UPI 2.0 Payments**, **Deceptive Login Honeypot**, and **Behavioral Biometrics**—unify')
    c = c.replace('└── CHANNEL C: Credit Card Portal (Carding / Impossible Physical Velocity Vector)\n', '')
    c = c.replace('|  └── Haversine Velocity Engine: d=2R*asin(√a)           └── Neo4j Graph DB: Mule Account Fan-Out Velocity        |',
                  '|  └── Shannon Biometrics Engine: H(D)=-Σ P log P         └── Neo4j Graph DB: Mule Account Fan-Out Velocity        |')
    c = c.replace('|  ├── Model 2 (Card Classifier): Evaluates geographical displacement, elapsed seconds, and travel speed        |\n', '')
    
    old_cases = """▼ (Case 1: P < 0.30)                ▼ (Case 2: 0.30 <= P <= 0.70)       ▼ (Case 3: P > 0.70 OR Live Call)   ▼ (Case 4: Card >900km/h)
[ ZERO FRICTION CLEARANCE ]     [ DYNAMIC FRICTION SCREEN ]         [ UPSTREAM GATEWAY BLOCK ]          [ CARD VELOCITY FREEZE ]
• Dispatches native MPIN sheet  • Native FLAG_SECURE overlay        • Immediate HTTP 403 Forbidden      • Instant Card Freeze"""
    new_cases = """▼ (Case 1: P < 0.30)                ▼ (Case 2: 0.30 <= P <= 0.70)       ▼ (Case 3: P > 0.70 OR Live Call)
[ ZERO FRICTION CLEARANCE ]     [ DYNAMIC FRICTION SCREEN ]         [ UPSTREAM GATEWAY BLOCK ]
• Dispatches native MPIN sheet  • Native FLAG_SECURE overlay        • Immediate HTTP 403 Forbidden"""
    c = c.replace(old_cases, new_cases)

    card_table_row = "| **Card Velocity Guard** | Dual transactions at distinct coordinates | $< 2.0\\text{ms}$ | Haversine Formula $d = 2R \\arcsin(\\sqrt{a})$ | Rule-based automatic card freeze if travel velocity $v > 900\\text{ km/h}$ |\n"
    c = c.replace(card_table_row, "")

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", p)


def update_generate_pdf():
    p = 'generate_pdf_report.py'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('Paragraph("<b>Target Systems:</b> UPI 2.0 Rails, Card Velocity, SOC Engine", body_style),',
                  'Paragraph("<b>Target Systems:</b> UPI 2.0 Rails, Deceptive Honeypot, SOC Engine", body_style),')
    c = c.replace('"| - Deterministic Engines: Levenshtein Typo (<15ms) + Haversine Velocity Physics (>900 km/h)    |\\n"',
                  '"| - Deterministic Engines: Levenshtein Typo (<15ms) + Shannon Biometrics Engine (H<0.60)     |\\n"')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", p)


def update_generate_1page_pdf():
    p = os.path.join('scripts', 'generate_1page_pdf.py')
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    # Title
    c = c.replace('A Unified ML-Driven Fraud Detection and Deceptive Honeypot Defence Platform for UPI and Card Payments',
                  'A Unified ML-Driven Fraud Detection and Deceptive Honeypot Defence Platform for UPI Payments')

    # Replace Haversine engine
    old_haversine = """        Paragraph("<b>Haversine Spacetime Velocity Engine (<code>src/haversine_engine.py</code>)</b><br/>Calculates great-circle geodesic surface distance: <i>d = 2R &middot; arcsin(&radic;(sin&sup2;(&Delta;&phi;/2) + cos&phi;&sub1;cos&phi;&sub2;sin&sup2;(&Delta;&lambda;/2)))</i>. Computes required transit speed <i>v = d / &Delta;t</i>. Flags physical impossibility if <b>v &gt; 650 mph</b> (supersonic travel between cities).", style_body),"""
    new_haversine = """        Paragraph("<b>Typo-Squatting Wagner-Fischer Matrix (<code>src/levenshtein_engine.py</code>)</b><br/>Dynamic programming matrix calculating edit distance: <i>D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1]+&delta;)</i> against verified NPCI handle tokens. Flags brand similarity &ge; <b>0.75</b>.", style_body),"""
    c = c.replace(old_haversine, new_haversine)

    # Replace second Levenshtein box with Collect-Trap filter
    old_lev = """        Paragraph("<b>Levenshtein Typo-Squatting Engine (<code>src/levenshtein_engine.py</code>)</b><br/>Dynamic programming matrix calculating Wagner-Fischer edit distance: <i>D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1]+&delta;)</i>. Fuses with trigram Jaccard similarity against Indian NPCI whitelist (Paytm, PhonePe, GooglePay, BHIM). Flags brand similarity &ge; <b>0.75</b>.", style_body)"""
    new_lev = """        Paragraph("<b>Social Engineering Collect-Trap Filter (<code>src/inference_engine.py</code>)</b><br/>Monitors inbound collect requests, amount ratios (<i>amt / 2000</i>), and sender spam reputation. Instantly flags high-risk reverse-payment manipulation schemes.", style_body)"""
    c = c.replace(old_lev, new_lev)

    # Remove Card Velocity row from ML table
    card_ml_row = """        [
            Paragraph("<b>Card Velocity</b>", style_table_cell),
            Paragraph("<code>xgboost_card_velocity_model.json</code><br/>XGBoost Booster (LR=0.10)", style_table_cell),
            Paragraph("<code>card_velocity_telemetry.csv</code><br/>2,000 synthetic card transactions", style_table_cell),
            Paragraph("<b>99.95%</b>", style_table_cell_bold_center),
            Paragraph("99.89%", style_table_cell_center),
            Paragraph("100.0%", style_table_cell_center),
            Paragraph("<b>99.95%</b>", style_table_cell_bold_center),
            Paragraph("<b>1.0000</b>", style_table_cell_bold_center),
        ],
"""
    c = c.replace(card_ml_row, '')

    # Update dataset path in Login Telemetry row
    c = c.replace("<code>honeypot_login_telemetry.csv</code><br/>2,000 login sessions (Keystroke & Entropy)",
                  "<code>honeypot_login_training.csv</code><br/>2,000 login sessions (Keystroke & Entropy)")
    
    # Update Unified UPI Scam row feature count to 5 features
    c = c.replace("5,000 synthetic UPI records (6 features)", "5,000 synthetic UPI records (5 features)")

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", p)


if __name__ == '__main__':
    update_gap_analysis()
    update_system_architecture()
    update_flowchart()
    update_generate_pdf()
    update_generate_1page_pdf()
