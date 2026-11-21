# 🛡️ Project Aegis: Online Fraud Detection System
### *Unified ML-Driven Fraud Detection, BBPS Directory Verification & Deceptive Honeypot Platform for UPI Payments*

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-emerald.svg)](https://flask.palletsprojects.com/)
[![XGBoost](https://img.shields.io/badge/ML%20Engine-XGBoost%20%26%20Scikit--Learn-orange.svg)](https://xgboost.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-100%25%20Production%20Verified-brightgreen.svg)](#)
[![Compliance](https://img.shields.io/badge/Compliance-Sec%2065B%20IEA%20%7C%20Sec%2063%20BSA%202023-purple.svg)](#)

---

## 📌 Executive Summary

**Project Aegis** is an enterprise-grade, client-to-backend fraud prevention and cyber deception platform designed to neutralize high-velocity financial fraud, automated credential stuffing bots, remote access trojans (RATs / Screen Mirroring), and social engineering coercion across India's Unified Payments Interface (UPI) ecosystem.

Unlike conventional anti-fraud systems that analyze transactions *post-authorization* (after victim funds have already departed the bank), **Project Aegis intercepts fraud pre-authorization** before the user enters their MPIN. High-risk automated attacks are silently diverted into a cryptographic decoy honeypot, while coercion attempts trigger an authentic pre-PIN gateway block and generate a court-admissible **I4C Form 1930 Cybercrime Evidence Dossier (PDF)**.

---

## 🌟 Key Architectural Pillars

```
                    ┌────────────────────────────────────────────────────────┐
                    │               CLIENT INGRESS & TELEMETRY               │
                    │  [60Hz Pointer Dynamics] [Keystroke Flight] [Screen/Call]│
                    └──────────────────────────┬─────────────────────────────┘
                                               │ (Signed Encrypted Telemetry)
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │             AEGIS MULTI-MODEL RISK ENGINE              │
                    │  • BBPS Directory Verification (MCC 4900 vs 0000)       │
                    │  • Wagner-Fischer Levenshtein Typo Engine (<15ms)      │
                    │  • Contextual Coercion Override (Screen Share + Call)  │
                    │  • XGBoost Unified UPI Model (5 Calibrated Features)   │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                               ▼                               ▼
    [Tier 1: Risk P < 0.30]       [Tier 2: 0.30 <= P <= 0.70]       [Tier 3: Risk P > 0.70]
   ┌───────────────────────┐     ┌───────────────────────────┐    ┌───────────────────────────┐
   │  ZERO FRICTION PASS   │     │  DYNAMIC FRICTION SCREEN  │    │  UPSTREAM GATEWAY BLOCK   │
   │ Direct MPIN clearance │     │ 5-sec cooldown & warnings │    │ Pre-PIN Rejection (403)   │
   └───────────────────────┘     └───────────────────────────┘    └─────────────┬─────────────┘
                                                                                │
                                              ┌─────────────────────────────────┴─────────────────┐
                                              ▼                                                   ▼
                                ┌───────────────────────────┐                       ┌───────────────────────────┐
                                │  DECEPTIVE HONEYPOT TRAP  │                       │ 1-CLICK FORM 1930 DOSSIER │
                                │ • Ghost banking sandbox   │                       │ • MHA / I4C National Form │
                                │ • WebRTC real-IP unmasking│                       │ • Sec 65B BSA Certified   │
                                │ • Cryptographic PoW delay │                       │ • SHA-256 Chain of Custody│
                                └───────────────────────────┘                       └───────────────────────────┘
```

### 1. Pre-PIN UPI Transaction Scoring
* **5-Feature Calibrated Model:** Evaluates `screen_sharing_active`, `upi_brand_similarity`, `is_collect_request`, `sender_spam_score`, and `transaction_amount_ratio`.
* **Coercion Override:** When screen sharing and a live phone call are detected concurrently during a high-value payment, the system immediately forces Tier 3 Gateway Block ($P \ge 0.992$), preventing credential theft.

### 2. Central BBPS & Levenshtein Typo Engine (`src/levenshtein_engine.py`)
* Verifies VPAs against the Central **Bharat Bill Payment System (BBPS)** merchant registry:
  - Genuine Utilities (`elec.173@okaxis`): Verified Corporate Merchant (`MCC 4900`).
  - Scammer Look-Alikes (`elec.174@okaxis`): Unverified Private Savings Account (`MCC 0000`), flagged at **93.8% lexical similarity**.

### 3. 1-Click Court-Admissible Evidence Dossier (`src/dossier_generator.py`)
* Generates an official, 2-page **I4C Form 1930 Cybercrime Incident Report (PDF)**.
* Certified under **Section 65B of the Indian Evidence Act, 1872** and **Section 63 of Bharatiya Sakshya Adhiniyam, 2023 (BSA)**.
* Embeds verification QR codes, deterministic SHA-256 digital seals, and immediate bank freeze directives.

### 4. Ghost Honeypot Deception Sandbox (`/sandbox/session`)
* Traps botnet credentials in an isolated decoy banking dashboard.
* Uses WebRTC STUN discovery to unmask adversary real IPs behind commercial VPNs and rotating proxies.
* Implements a cryptographic Proof-of-Work (PoW) tarpit that stalls mule transfers and collapses scraper velocity.

---

## 📊 Machine Learning Models & Empirical Benchmarks

| Model Target | Model Artifact | Training Dataset | Features | Accuracy | Precision | Recall | ROC-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Unified UPI Scam** | `models/xgboost_fraud_model.json` | `data/unified_transaction_risk.csv` (5,000 rows) | 5 | **99.92%** | 98.36% | 100.0% | **1.0000** |
| **Login Honeypot** | `models/xgboost_login_honeypot_model.json` | `data/honeypot_login_training.csv` (2,000 rows) | 4 | **99.85%** | 99.60% | 100.0% | **0.9995** |
| **Biometric Bot Sensor** | Dual-Threshold Heuristic | `data/bot_telemetry_micro_samples.csv` | 2 | **100.0%** | 100.0% | 100.0% | **1.0000** |

---

## 📂 Structured Project Layout

```text
online-fraud-detection-system/
├── docs/                                    # Academic presentations & architectural reports
│   ├── presentations/                       # Defense and seminar decks (.pptx)
│   └── reports/                             # Gap analysis and system specifications (.md, .pdf)
├── src/                                     # Core production application
│   ├── app.py                               # Flask API gateway & microservice
│   ├── inference_engine.py                  # XGBoost multi-model risk fusion
│   ├── levenshtein_engine.py                # BBPS directory & typo-squatting engine
│   ├── dossier_generator.py                 # I4C Form 1930 PDF forensic generator
│   ├── data_generator.py                    # Telemetry dataset generator
│   └── train_model.py                       # Model training pipeline
├── data/                                    # Datasets and forensic CSV logs
│   ├── bot_telemetry_micro_samples.csv      # Key flight and cursor telemetry
│   ├── honeypot_login_telemetry.csv         # Bot sample records
│   ├── honeypot_login_training.csv          # 2,000 synthetic login rows
│   ├── honeypot_session_forensics.csv       # Decoy session capture and WebRTC logs
│   ├── honeypot_transfer_intercept.csv      # Intercepted mule VPAs and stalled transfers
│   └── unified_transaction_risk.csv         # 5,000 synthetic UPI records
├── models/                                  # Trained machine learning model artifacts
│   ├── xgboost_fraud_model.json             # 5-feature unified UPI fraud classifier
│   └── xgboost_login_honeypot_model.json    # Behavioral login honeypot classifier
├── static/                                  # Web static assets
│   ├── charts/                              # Model performance and confusion matrices
│   ├── dossiers/                            # Sample I4C Form 1930 PDF dossiers
│   ├── js/bot-biometrics-engine.js          # 60Hz Shannon entropy biometrics
│   └── aegis-upi-shield.apk                 # Native Android companion security APK
├── templates/                               # Jinja2 web templates
│   ├── index.html                           # Primary Banking Portal & Desktop UPI Checkout
│   ├── honeypot.html                        # Deceptive Ghost banking session
│   └── aegis_demo.html                      # Standalone presentation sandbox
├── tests/                                   # Unit and integration test suite
│   ├── test_engines.py                      # Multi-model unit tests
│   └── test_bot_csv.py                      # Telemetry validation tests
├── scripts/                                 # Build automation & utility scripts
├── requirements.txt                         # Python package dependencies
├── Procfile                                 # Production deployment configuration
├── run.bat                                  # 1-click startup launcher
└── README.md                                # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.11+
* Git

### 2. Clone Repository & Setup
```bash
git clone https://github.com/aayusht1711/online-fraud-detection-system.git
cd online-fraud-detection-system

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Platform
```bash
python src/app.py
```
Open your browser and navigate to:
* **UPI Security Dashboard:** [http://127.0.0.1:5000/upi](http://127.0.0.1:5000/upi)
* **Main Banking Portal:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* **Honeypot Sandbox:** [http://127.0.0.1:5000/sandbox/session](http://127.0.0.1:5000/sandbox/session)

### 4. Run Unit Tests
```bash
python -m unittest discover tests
```

---

## 📡 REST API Reference

### 1. Score UPI Transaction
* **Endpoint:** `POST /api/score-transaction`
* **Payload:**
```json
{
  "upi_brand_similarity": 0.938,
  "transaction_amount_ratio": 2.4,
  "is_collect_request": 1,
  "screen_sharing_active": 1,
  "call_active": 1
}
```
* **Response:**
```json
{
  "action": "GATEWAY_REJECTION",
  "risk_score_P": 0.992,
  "intervention_type": "GATEWAY_REJECTION",
  "reason": "Critical Coercion Risk: Active Screen Sharing & Phone Call detected."
}
```

### 2. Check VPA Against BBPS Central Directory
* **Endpoint:** `POST /api/check-vpa`
* **Payload:** `{"vpa": "elec.174@okaxis"}`
* **Response:**
```json
{
  "vpa": "elec.174@okaxis",
  "directory_status": "NOT_IN_BBPS_WHITELIST (UNVERIFIED_P2P_SAVINGS)",
  "is_bbps_verified": false,
  "is_typo_squatting": true,
  "max_similarity": 0.9375,
  "best_match": "elec.173",
  "impersonated_entity": "State Electricity Distribution Co. (DISCOM)"
}
```

### 3. Generate Court-Admissible Form 1930 Dossier
* **Endpoint:** `POST /api/generate-dossier`
* **Payload:** `{"attacker_vpa": "elec.174@okaxis", "amount": 4800}`
* **Response:**
```json
{
  "status": "SUCCESS",
  "incident_id": "I4C-2026-UP1930-AEGIS-88129",
  "sha256_hash": "8ABC711CF73740402D213E75855CF4A0668256378F68D92AB4E1546C925670C4",
  "download_url": "/static/dossiers/I4C_Form1930_Dossier_I4C-2026-UP1930-AEGIS-88129.pdf"
}
```
