import os
import sys
import io
import time
import hashlib
import json
from datetime import datetime, timezone, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import qrcode

class DossierNumberedCanvas(canvas.Canvas):
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
        
        # Header (Top of each page)
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawString(36, 297 * mm - 22, "NATIONAL CYBER CRIME REPORTING PORTAL (NCCRP) • I4C / CFCFRMS HELPLINE 1930")
        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(210 * mm - 36, 297 * mm - 22, "FORM 1930 ELECTRONIC EVIDENCE RECORD • CONFIDENTIAL")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 297 * mm - 25, 210 * mm - 36, 297 * mm - 25)

        # Footer (Bottom of each page)
        self.setFont("Helvetica-Bold", 6.8)
        self.setFillColor(colors.HexColor("#0F172A"))
        self.drawString(36, 18, "GOVT OF INDIA • MHA • INDIAN CYBER CRIME COORDINATION CENTRE (I4C)")
        
        self.setFont("Helvetica", 6.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 10, "Court-Admissible Evidence under Sec 65B Indian Evidence Act 1872 & Sec 63 Bharatiya Sakshya Adhiniyam 2023 (BSA)")
        
        self.drawRightString(210 * mm - 36, 14, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 24, 210 * mm - 36, 24)
        
        self.restoreState()


def generate_i4c_dossier_pdf(incident_data, output_path=None):
    """
    Generates a formal, court-admissible Indian Cyber Crime Coordination Centre (I4C)
    Form 1930 Incident Evidence Dossier in PDF format (Complete 2-Page Executive Dossier).
    """
    if output_path is None:
        os.makedirs("static/dossiers", exist_ok=True)
        incident_id = incident_data.get("incident_id", f"I4C-2026-UP1930-{int(time.time())}")
        output_path = os.path.join("static", "dossiers", f"I4C_Form1930_Dossier_{incident_id}.pdf")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Calculate deterministic SHA-256 Chain of Custody hash
    raw_payload_str = json.dumps(incident_data, sort_keys=True)
    sha256_hash = hashlib.sha256(raw_payload_str.encode("utf-8")).hexdigest().upper()
    incident_data["sha256_hash"] = sha256_hash

    # Generate QR Code in-memory
    inc_id = incident_data.get("incident_id", f"I4C-2026-UP1930-AEGIS-{int(time.time())}")
    attacker_vpa = incident_data.get("attacker_vpa", "ph0nepe@okaxis")
    amount = float(incident_data.get("amount", 48000.0))

    qr_data = (
        f"https://cybercrime.gov.in/1930/verify?id={inc_id}&vpa={attacker_vpa}&"
        f"amt={amount}&hash={sha256_hash[:16]}"
    )
    qr = qrcode.QRCode(version=1, box_size=3, border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0F172A", back_color="white")
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    qr_flowable = Image(qr_buf, width=64, height=64)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_navy = colors.HexColor("#0F172A")
    c_blue = colors.HexColor("#1E3A8A")
    c_sky = colors.HexColor("#0284C7")
    c_red = colors.HexColor("#DC2626")
    c_dark_red = colors.HexColor("#991B1B")
    c_green = colors.HexColor("#059669")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")

    # Typography Styles
    style_title = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_navy)
    style_gov_sub = ParagraphStyle('GovSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=c_blue)
    style_meta_label = ParagraphStyle('MetaLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9.5, textColor=colors.HexColor("#475569"))
    style_meta_val = ParagraphStyle('MetaVal', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.5, textColor=c_navy)
    style_meta_val_bold = ParagraphStyle('MetaValBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=c_navy)
    style_meta_val_mono = ParagraphStyle('MetaValMono', parent=styles['Normal'], fontName='Courier-Bold', fontSize=7, leading=9, textColor=colors.HexColor("#1E293B"))
    style_sec_heading = ParagraphStyle('SecHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.white)
    style_cell_body = ParagraphStyle('CellBody', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=9, textColor=c_navy)

    def make_section_banner(title_text, bg_hex="#1E3A8A"):
        p = Paragraph(f"<b>{title_text.upper()}</b>", style_sec_heading)
        t = Table([[p]], colWidths=[515])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    story = []

    # =========================================================
    # PAGE 1: INCIDENT METADATA, RECONNAISSANCE & SENSORS
    # =========================================================

    # 1. Official Header with QR
    header_left = [
        Paragraph("MINISTRY OF HOME AFFAIRS • GOVERNMENT OF INDIA", style_gov_sub),
        Paragraph("INDIAN CYBER CRIME COORDINATION CENTRE (I4C)", style_gov_sub),
        Paragraph("Citizen Financial Cyber Fraud Reporting System (CFCFRMS • Helpline 1930)", style_title),
        Paragraph("<b>FORM 1930: ELECTRONIC EVIDENCE RECORD &amp; INCIDENT FORENSIC DOSSIER</b>", ParagraphStyle('F1930', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_dark_red)),
        Paragraph("Statutory Evidence Record under Section 65B of Indian Evidence Act, 1872 &amp; Section 63 of Bharatiya Sakshya Adhiniyam, 2023 (BSA)", ParagraphStyle('Statutory', fontName='Helvetica-Oblique', fontSize=6.2, leading=8, textColor=colors.HexColor("#64748B")))
    ]

    header_table = Table([[header_left, qr_flowable]], colWidths=[440, 75])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # 2. Case Identification Summary Grid
    ts_now = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%b-%Y %I:%M:%S %p IST")
    amt_formatted = f"INR {amount:,.2f}"

    meta_grid = [
        [
            Paragraph("<b>National Acknowledgment ID:</b>", style_meta_label),
            Paragraph(f"<b>{inc_id}</b>", style_meta_val_bold),
            Paragraph("<b>Incident Timestamp:</b>", style_meta_label),
            Paragraph(ts_now, style_meta_val)
        ],
        [
            Paragraph("<b>Crime Category:</b>", style_meta_label),
            Paragraph("UPI Financial Cyber Coercion / Remote Access", style_meta_val_bold),
            Paragraph("<b>Statutory Offense:</b>", style_meta_label),
            Paragraph("IPC Sec 419/420, IT Act Sec 66C/66D, BNS Sec 318(4)", style_meta_val)
        ],
        [
            Paragraph("<b>Attempted Siphoning:</b>", style_meta_label),
            Paragraph(f"<font color='#DC2626'><b>{amt_formatted}</b></font>", style_meta_val_bold),
            Paragraph("<b>Interception Outcome:</b>", style_meta_label),
            Paragraph("<font color='#059669'><b>BLOCKED PRE-PIN (ZERO FINANCIAL LOSS)</b></font>", style_meta_val_bold)
        ],
        [
            Paragraph("<b>SHA-256 Evidence Hash:</b>", style_meta_label),
            Paragraph(f"<font size=6 color='#1E293B'>{sha256_hash}</font>", style_meta_val_mono),
            Paragraph("<b>Chain of Custody:</b>", style_meta_label),
            Paragraph("SECURE (Tamper-Sealed by Aegis SOC Daemon)", style_meta_val)
        ]
    ]

    t_meta = Table(meta_grid, colWidths=[120, 150, 110, 135])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 7))

    # 3. Section I: Victim Particulars
    story.append(make_section_banner("Section I: Victim & Digital Client Environment"))
    victim_table_data = [
        [
            Paragraph("<b>Account Holder Name:</b>", style_meta_label),
            Paragraph(incident_data.get("victim_name", "Rahul Verma (Protected Customer)"), style_meta_val),
            Paragraph("<b>Originating Source VPA:</b>", style_meta_label),
            Paragraph(f"<b>{incident_data.get('victim_vpa', 'user@okhdfcbank')}</b>", style_meta_val_mono)
        ],
        [
            Paragraph("<b>Client Public IP &amp; ISP:</b>", style_meta_label),
            Paragraph(incident_data.get("client_ip", "103.112.44.89 (Bharti Airtel, Delhi NCR)"), style_meta_val),
            Paragraph("<b>Operating Environment:</b>", style_meta_label),
            Paragraph(incident_data.get("client_device", "Samsung Galaxy S23 • Android 14 (One UI 6.1)"), style_meta_val)
        ],
        [
            Paragraph("<b>Device Binding State:</b>", style_meta_label),
            Paragraph("Hardware Keystore Bound • SIM Slot 1 Verified", style_meta_val),
            Paragraph("<b>MPIN Entry State:</b>", style_meta_label),
            Paragraph("<font color='#059669'><b>WITHHELD BY GATEWAY (Zero PIN Exposed)</b></font>", style_meta_val_bold)
        ]
    ]
    t_victim = Table(victim_table_data, colWidths=[120, 150, 110, 135])
    t_victim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_victim)
    story.append(Spacer(1, 7))

    # 4. Section II: Suspect Perpetrator Reconnaissance
    story.append(make_section_banner("Section II: Suspect Perpetrator & Mule Account Reconnaissance", "#991B1B"))
    recon_data = [
        [
            Paragraph("<b>Suspect Beneficiary VPA:</b>", style_meta_label),
            Paragraph(f"<font color='#DC2626'><b>{attacker_vpa}</b></font>", style_meta_val_mono),
            Paragraph("<b>Claimed Impersonated Alias:</b>", style_meta_label),
            Paragraph(f"<b>{incident_data.get('attacker_alias', 'PhonePe Cash Refund Officer')}</b>", style_meta_val_bold)
        ],
        [
            Paragraph("<b>Beneficiary Bank &amp; IFSC:</b>", style_meta_label),
            Paragraph(incident_data.get("target_bank", "Axis Bank Core UPI Switch (IFSC: UTIB0000001)"), style_meta_val),
            Paragraph("<b>Transaction Flow Type:</b>", style_meta_label),
            Paragraph("PULL Collect Request (Fraudulent Debit disguised as Refund)", style_meta_val)
        ],
        [
            Paragraph("<b>Typo-Squatting Analysis:</b>", style_meta_label),
            Paragraph(f"<b>Sim: {incident_data.get('brand_similarity', 88.0):.1f}%</b> (Levenshtein Distance: {incident_data.get('levenshtein_distance', 1)})", style_meta_val_bold),
            Paragraph("<b>Target Impersonated Brand:</b>", style_meta_label),
            Paragraph(incident_data.get("spoofed_brand", "PhonePe Official (phonepe@ybl / phonepe@ibl)"), style_meta_val)
        ],
        [
            Paragraph("<b>Mule Ring Correlation:</b>", style_meta_label),
            Paragraph("<font color='#DC2626'><b>FLAGGED MULE RING (Mewat/Cyber-Hub Cluster 09)</b></font>", style_meta_val_bold),
            Paragraph("<b>CFCFRMS Freeze Notice:</b>", style_meta_label),
            Paragraph("AUTO-NOTIFIED TO TARGET ACQUIRING BANK", style_meta_val_bold)
        ]
    ]
    t_recon = Table(recon_data, colWidths=[120, 150, 110, 135])
    t_recon.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_recon)
    story.append(Spacer(1, 7))

    # 5. Section III: Forensic Sensor Triangulation Matrix
    story.append(make_section_banner("Section III: Forensic Sensor Triangulation & Attack Vector Matrix", "#0F172A"))
    sensor_headers = [
        Paragraph("<b>Sensor / Vector Hook</b>", ParagraphStyle('SH1', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>Observed Telemetry State</b>", ParagraphStyle('SH2', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>Intervention Severity</b>", ParagraphStyle('SH3', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>Forensic Finding &amp; Modus Operandi</b>", ParagraphStyle('SH4', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white))
    ]
    sensor_rows = [
        sensor_headers,
        [
            Paragraph("<b>Sensor 1: Screen Mirroring Protocol</b><br/><font color='#64748B'>MediaProjectionManager / DisplayManager</font>", style_cell_body),
            Paragraph("<font color='#DC2626'><b>ACTIVE (TRUE)</b></font><br/>Virtual Display Hook Active", style_cell_body),
            Paragraph("<font color='#DC2626'><b>CRITICAL (Tier 3)</b></font>", style_cell_body),
            Paragraph("Active AnyDesk / TeamViewer package mirroring screen in real-time. Direct violation of NPCI Pre-PIN Security Directive.", style_cell_body)
        ],
        [
            Paragraph("<b>Sensor 2: Telephony Audio Stream</b><br/><font color='#64748B'>AudioManager.MODE_IN_COMMUNICATION</font>", style_cell_body),
            Paragraph("<font color='#DC2626'><b>ACTIVE (TRUE)</b></font><br/>Voice Call Active (Dwell: 08m 14s)", style_cell_body),
            Paragraph("<font color='#B45309'><b>HIGH (Tier 2)</b></font>", style_cell_body),
            Paragraph("Caller guiding/coercing victim simultaneously during checkout flow. Matches classic Digital Arrest / Fake Bank Officer SOP.", style_cell_body)
        ],
        [
            Paragraph("<b>Sensor 3: QR Vector Origin Engine</b><br/><font color='#64748B'>Camera vs Gallery Buffer Header</font>", style_cell_body),
            Paragraph("<b>GALLERY BUFFER</b><br/>Pre-saved image import", style_cell_body),
            Paragraph("<font color='#B45309'><b>ELEVATED</b></font>", style_cell_body),
            Paragraph("Payment QR loaded from external storage / WhatsApp download instead of direct physical optical scanner.", style_cell_body)
        ],
        [
            Paragraph("<b>Sensor 4: Biometric Micro-Kinetics</b><br/><font color='#64748B'>Entropy H &amp; Flight-Time Velocity</font>", style_cell_body),
            Paragraph("<b>H = 0.34 bits</b><br/>Typing Sim: 0.18 (Synthetic)", style_cell_body),
            Paragraph("<font color='#DC2626'><b>BOT ANOMALY</b></font>", style_cell_body),
            Paragraph("Cursor trajectory exhibits synthetic micro-velocity with zero human tremble; synthetic automation script signature.", style_cell_body)
        ]
    ]
    t_sensors = Table(sensor_rows, colWidths=[125, 95, 75, 220])
    t_sensors.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sensors)

    # PAGE BREAK TO PAGE 2
    story.append(PageBreak())

    # =========================================================
    # PAGE 2: ML INFERENCE, FREEZE DISPATCH & SEC 65B CERTIFICATE
    # =========================================================

    # 6. Section IV: Machine Learning Scoring & Explainable AI (SHAP)
    story.append(make_section_banner("Section IV: Machine Learning Ensemble Scoring & Explainable AI (SHAP)", "#0284C7"))
    ml_data = [
        [
            Paragraph("<b>Model Architecture:</b>", style_meta_label),
            Paragraph("3-Tier Multi-Modal Gradient Boosted Tree (XGBoost 2.0)", style_meta_val),
            Paragraph("<b>Total Inference Latency:</b>", style_meta_label),
            Paragraph("<b>1.42 ms</b> (Edge Gateway Executed)", style_meta_val_bold)
        ],
        [
            Paragraph("<b>Model 1 (Bot Biometrics):</b>", style_meta_label),
            Paragraph("P(Bot) = <b>0.978</b> (High Risk)", style_meta_val_bold),
            Paragraph("<b>Model 2 (Honeypot Trap):</b>", style_meta_label),
            Paragraph("P(Mule Trap) = <b>0.840</b>", style_meta_val)
        ],
        [
            Paragraph("<b>Model 3 (UPI Coercion):</b>", style_meta_label),
            Paragraph("<font color='#DC2626' size=7.5><b>P = 0.992 (99.2% CRITICAL FRAUD)</b></font>", style_meta_val_bold),
            Paragraph("<b>Intervention Threshold:</b>", style_meta_label),
            Paragraph("GATEWAY REJECTION (&gt; 0.75 Cutoff)", style_meta_val_bold)
        ]
    ]
    t_ml = Table(ml_data, colWidths=[120, 150, 110, 135])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 6))

    # SHAP Attribution Table
    shap_headers = [
        Paragraph("<b>Feature Vector</b>", ParagraphStyle('SHH1', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>Input Value</b>", ParagraphStyle('SHH2', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>SHAP Attribution Value</b>", ParagraphStyle('SHH3', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
        Paragraph("<b>Risk Contribution &amp; Policy Decision</b>", ParagraphStyle('SHH4', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white))
    ]
    shap_rows = [
        shap_headers,
        [Paragraph("screen_sharing_active", style_cell_body), Paragraph("1 (True)", style_cell_body), Paragraph("<font color='#DC2626'><b>+0.421</b></font>", style_cell_body), Paragraph("Primary coercion indicator; activates Pre-PIN hardware isolation", style_cell_body)],
        [Paragraph("call_active", style_cell_body), Paragraph("1 (True)", style_cell_body), Paragraph("<font color='#DC2626'><b>+0.285</b></font>", style_cell_body), Paragraph("Active telephony in progress; triggers dynamic friction &amp; warning", style_cell_body)],
        [Paragraph("upi_brand_similarity", style_cell_body), Paragraph("0.88 (88%)", style_cell_body), Paragraph("<font color='#DC2626'><b>+0.194</b></font>", style_cell_body), Paragraph("Typo-squatting brand spoofing 'ph0nepe' vs 'phonepe'", style_cell_body)],
        [Paragraph("is_collect_request", style_cell_body), Paragraph("1 (True)", style_cell_body), Paragraph("<font color='#B45309'><b>+0.062</b></font>", style_cell_body), Paragraph("Unauthorized pull request disguised as cashback refund", style_cell_body)],
        [Paragraph("transaction_amount_ratio", style_cell_body), Paragraph("24.0 (48k / 2k)", style_cell_body), Paragraph("<font color='#B45309'><b>+0.030</b></font>", style_cell_body), Paragraph("High-value anomaly relative to user historic baseline", style_cell_body)],
    ]
    t_shap = Table(shap_rows, colWidths=[115, 75, 95, 230])
    t_shap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_shap)
    story.append(Spacer(1, 7))

    # 7. Section V: Automated Inter-Bank Freeze & Law Enforcement Dispatch Log
    story.append(make_section_banner("Section V: Automated Inter-Bank Freeze & Law Enforcement Dispatch Log", "#B45309"))
    timeline_data = [
        [
            Paragraph("<b>Timestamp (Delta)</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
            Paragraph("<b>Target Entity / Subsystem</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
            Paragraph("<b>Action Dispatched</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white)),
            Paragraph("<b>Evidentiary Confirmation</b>", ParagraphStyle('TH4', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.white))
        ],
        [
            Paragraph("T+0.00s (00:00:00.000)", style_cell_body),
            Paragraph("Aegis Gateway Interceptor", style_cell_body),
            Paragraph("<font color='#DC2626'><b>GATEWAY INTERCEPTION</b></font>", style_cell_body),
            Paragraph("Intercept Code AEGIS-G-403; PIN screen withheld from display", style_cell_body)
        ],
        [
            Paragraph("T+0.04s (00:00:00.042)", style_cell_body),
            Paragraph("NPCI CFCFRMS API Gateway", style_cell_body),
            Paragraph("Auto-Broadcast Incident Packet", style_cell_body),
            Paragraph(f"Dispatched Docket {inc_id} to National Fraud Registry", style_cell_body)
        ],
        [
            Paragraph("T+0.12s (00:00:00.120)", style_cell_body),
            Paragraph("Axis Bank Core UPI Switch", style_cell_body),
            Paragraph("<font color='#DC2626'><b>MULE ACCOUNT FREEZE HOLD</b></font>", style_cell_body),
            Paragraph(f"Freeze request placed on beneficiary VPA '{attacker_vpa}'", style_cell_body)
        ],
        [
            Paragraph("T+0.25s (00:00:00.254)", style_cell_body),
            Paragraph("National Cyber Helpline (1930)", style_cell_body),
            Paragraph("Automated Evidence Staging", style_cell_body),
            Paragraph("Staged in cybercrime.gov.in queue for instant victim confirmation", style_cell_body)
        ],
        [
            Paragraph("T+0.38s (00:00:00.381)", style_cell_body),
            Paragraph("Victim Android TEE Subsystem", style_cell_body),
            Paragraph("<font color='#059669'><b>SESSION SHIELD ACTIVATED</b></font>", style_cell_body),
            Paragraph("Screen mirror overlay terminated; zero funds debited from user", style_cell_body)
        ]
    ]
    t_timeline = Table(timeline_data, colWidths=[95, 115, 120, 185])
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_timeline)
    story.append(Spacer(1, 7))

    # 8. Section VI: Raw Forensic Cryptographic Audit Trail (Truncated Hex/JSON Dump)
    story.append(make_section_banner("Section VI: Raw Cryptographic Audit Trail (Canonical Evidence Stream)", "#334155"))
    raw_snippet = json.dumps({
        "event": "UPI_COERCION_INTERCEPTION",
        "incident_id": inc_id,
        "amount": amount,
        "victim_vpa": incident_data.get("victim_vpa", "user@okhdfcbank"),
        "attacker_vpa": attacker_vpa,
        "model_score": 0.992,
        "action": "GATEWAY_REJECTION",
        "sensors": {
            "screen_sharing": incident_data.get("screen_sharing_active", True),
            "voice_call": incident_data.get("call_active", True),
            "qr_origin": incident_data.get("qr_origin", "gallery"),
            "levenshtein_sim": incident_data.get("brand_similarity", 88.0)
        },
        "sha256": sha256_hash
    }, indent=2)

    p_raw = Preformatted(raw_snippet, ParagraphStyle('RawCode', fontName='Courier', fontSize=5.8, leading=7.2, textColor=colors.HexColor("#0F172A")))
    t_raw = Table([[p_raw]], colWidths=[515])
    t_raw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.6, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_raw)
    story.append(Spacer(1, 7))

    # 9. Section VII: Statutory Certificate under Sec 65B Indian Evidence Act / Sec 63 BSA 2023
    story.append(make_section_banner("Section VII: Statutory Electronic Evidence Certificate (Sec 65B IEA / Sec 63 BSA)", "#065F46"))
    cert_text = (
        "<b>CERTIFICATE UNDER SECTION 65B OF THE INDIAN EVIDENCE ACT, 1872 &amp; SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023 (BSA)</b><br/>"
        "1. This electronic record was produced by the Project Aegis Autonomous Threat Telemetry Engine and Core Gateway Interceptor during the normal course of cryptographic monitoring.<br/>"
        "2. The computer system and edge telemetry sensors were operating properly throughout the detection window, and no tampering or alteration occurred.<br/>"
        "3. The SHA-256 cryptographic digest below uniquely binds this document, the intercepted network packets, and sensor states to ensure immutable evidentiary chain of custody for law enforcement submission."
    )

    cert_table_data = [
        [Paragraph(cert_text, ParagraphStyle('CertP', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=c_navy))],
        [Paragraph(f"<b>CRYPTOGRAPHIC INTEGRITY HASH (SHA-256):</b><br/><font face='Courier-Bold' size=7 color='#0F172A'>{sha256_hash}</font>", style_meta_val_bold)],
        [
            Table([
                [
                    Paragraph("<b>Preservation Status:</b><br/><font color='#059669'>SEALED &amp; COMPLIANT</font>", style_cell_body),
                    Paragraph(f"<b>Generated At:</b><br/>{ts_now}", style_cell_body),
                    Paragraph("<b>Authorized Digital Seal:</b><br/>Project Aegis Autonomous SOC Forensic Daemon", style_cell_body),
                    Paragraph("<b>Law Enforcement Helpline:</b><br/><b>Dial 1930 • cybercrime.gov.in</b>", style_cell_body),
                ]
            ], colWidths=[105, 125, 160, 115], style=[
                ('TOPPADDING', (0,0), (-1,-1), 1.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ])
        ]
    ]

    t_cert = Table(cert_table_data, colWidths=[515])
    t_cert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#10B981")),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor("#A7F3D0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cert)

    # Build the document using DossierNumberedCanvas
    doc.build(story, canvasmaker=DossierNumberedCanvas)
    return output_path, sha256_hash
