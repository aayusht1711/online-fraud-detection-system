import os
import sys
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from levenshtein_engine import LevenshteinTypoEngine
from inference_engine import FraudInferenceEngine

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
data_file = os.path.join(data_dir, "unified_transaction_risk.csv")
model_file = os.path.join(model_dir, "xgboost_fraud_model.json")

if not os.path.exists(data_file):
    print("Generating synthetic telemetry datasets...")
    try:
        from data_generator import generate_datasets
        generate_datasets(output_dir=data_dir)
    except Exception as e:
        print(f"Warning: could not generate datasets: {e}")

if not os.path.exists(model_file):
    print("Training XGBoost Fraud Classifiers...")
    try:
        from train_model import train_all_models
        train_all_models(data_dir=data_dir, model_dir=model_dir)
    except Exception as e:
        print(f"Warning: could not train models: {e}")

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "..", "static"))

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

engine = FraudInferenceEngine(model_dir=model_dir)

@app.after_request
def add_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    """Main Dashboard & Simulator"""
    return render_template("index.html")

@app.route("/upi")
def upi_view():
    """Dedicated UPI Payments Portal"""
    return render_template("index.html")

@app.route("/demo")
def aegis_demo():
    """Project Aegis Split-Screen Dual-View Demonstration Sandbox"""
    return render_template("aegis_demo.html")

@app.route("/3d")
@app.route("/architecture-3d")
def aegis_3d_architecture():
    """Interactive 3D Isometric Animated Architecture Diagram"""
    return render_template("aegis_3d_architecture.html")

@app.route("/sandbox/session")
def honeypot_session():
    """Ghost Session Honeypot Route (P > 0.70 Trap)"""
    return render_template("honeypot.html")

@app.route("/api/score-transaction", methods=["POST"])
def score_transaction():
    """Unified Transaction ML Model Endpoint (Dataset 3)"""
    data = request.json or {}
    result = engine.score_transaction(data)
    return jsonify(result)

@app.route("/api/score-login", methods=["POST"])
def score_login():
    """Login Telemetry Honeypot ML Model Endpoint (Dataset 1)"""
    data = request.json or {}
    result = engine.score_login_telemetry(data)
    return jsonify(result)

@app.route("/api/check-vpa", methods=["POST"])
def check_vpa():
    """Levenshtein Typo-Squatting Check Endpoint"""
    data = request.json or {}
    vpa = data.get("vpa", "")
    evaluation = LevenshteinTypoEngine.evaluate_vpa(vpa)
    return jsonify(evaluation)

@app.route("/api/sandbox/transfer", methods=["POST"])
def honeypot_transfer():
    """Decoy Endpoint returning synthetic success to trapped attacker"""
    data = request.json or {}
    return jsonify({
        "status": "success",
        "transaction_id": "GHOST_TX_9921",
        "message": "Transfer processed successfully",
        "transferred_amount": data.get("amount", 14.20),
        "sandbox_mode": True
    })

@app.route("/api/honeypot/stalled-transfer", methods=["POST"])
def honeypot_stalled_transfer():
    """
    Project Aegis Stalled Transfer Interceptor:
    Cycles deterministic banking errors (ZM -> U16 -> TIMEOUT) with switch lag (800-1500ms).
    Logs exfiltration details into honeypot_transfer_intercept.csv.
    """
    import time, csv
    data = request.json or {}
    session_id = data.get("session_id", "S_20101")
    amt = float(data.get("amount", 75000.0))
    target = data.get("beneficiary", "mule_sweep01@okaxis")
    retry_count = int(data.get("retry_count", 1))

    # Error progression mapping (Capped at 3 user attempts)
    if retry_count == 1:
        code = "NPCI_ERR_ZM"
        msg = "Switch Timeout - Pending Confirmation (Auto-retry in 60s)"
        delay_ms = 1250
    elif retry_count == 2:
        code = "BANK_ERR_U16"
        msg = "Beneficiary Switch Throttled - Temporary Network Congestion (Retry in 60s)"
        delay_ms = 1400
    elif retry_count == 3:
        code = "SYS_TIMEOUT"
        msg = "Transaction Timed Out - Core Banking Clearing Hold (Attempt 3/3 Exhausted)"
        delay_ms = 1100
    else:
        code = "AML_ERR_QUARANTINE"
        msg = "Maximum transfer attempts (3/3) exceeded. Channel quarantined by Aegis Shield."
        delay_ms = 850

    # Artificial switch latency injection
    time.sleep(delay_ms / 1000.0)

    # Append to honeypot_transfer_intercept.csv
    intercept_file = os.path.join(data_dir, "honeypot_transfer_intercept.csv")
    tr_id = f"TR_{9900 + retry_count}"
    try:
        file_exists = os.path.exists(intercept_file)
        with open(intercept_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["transfer_attempt_id", "session_id", "attempted_amount", "beneficiary_type", "switch_error_served", "is_mule_account"])
            writer.writerow([tr_id, session_id, amt, "UPI_VPA", code, 1])
    except Exception as e:
        print("CSV append error:", e)

    return jsonify({
        "status": "FAILURE",
        "error_code": code,
        "message": msg,
        "transfer_attempt_id": tr_id,
        "delay_ms": delay_ms,
        "retry_count": retry_count,
        "target_beneficiary": target,
        "is_mule_account": True,
        "mule_flagged": True
    })

@app.route("/api/honeypot/telemetry-dump", methods=["POST"])
def honeypot_telemetry_dump():
    """Logs background WebRTC STUN discovery and dwell metrics to honeypot_session_forensics.csv"""
    import csv
    data = request.json or {}
    session_id = data.get("session_id", "S_20101")
    public_ip = data.get("extracted_public_ip", "103.14.120.45")
    geo_country = data.get("geo_country", "IN")
    geo_city = data.get("geo_city_region", "Mewat_HR")
    isp_asn = data.get("isp_asn", "AS133929")
    dest_vpa = data.get("destination_vpa", "mule_sweep01@okaxis")
    dwell_sec = float(data.get("session_dwell_seconds", 385.4))
    retry_clicks = int(data.get("retry_click_count", 3))

    forensic_file = os.path.join(data_dir, "honeypot_session_forensics.csv")
    try:
        file_exists = os.path.exists(forensic_file)
        with open(forensic_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["session_id", "extracted_public_ip", "geo_country", "geo_city_region", "isp_asn", "destination_vpa", "session_dwell_seconds", "retry_click_count"])
            writer.writerow([session_id, public_ip, geo_country, geo_city, isp_asn, dest_vpa, dwell_sec, retry_clicks])
    except Exception as e:
        print("Forensics CSV error:", e)

    return jsonify({"status": "SUCCESS", "logged": True, "session_id": session_id})

@app.route("/api/honeypot/live-forensics", methods=["GET"])
def honeypot_live_forensics():
    """Returns the latest records from all 3 CSVs for live localhost dashboard inspection"""
    import csv
    def read_csv_tail(filename, limit=10):
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            return []
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
        return rows[-limit:]

    return jsonify({
        "login_telemetry": read_csv_tail("honeypot_login_telemetry.csv", 5),
        "session_forensics": read_csv_tail("honeypot_session_forensics.csv", 5),
        "transfer_intercept": read_csv_tail("honeypot_transfer_intercept.csv", 5)
    })

@app.route("/api/v1/test-bot-sample", methods=["GET", "POST"])
def test_bot_sample():
    """
    Test runner endpoint that reads rows from honeypot_login_telemetry.csv
    and returns the classifier prediction:
    0 = Legitimate Human, 1 = Automated Bot.
    """
    import csv
    csv_file = os.path.join(data_dir, "honeypot_login_telemetry.csv")
    if not os.path.exists(csv_file):
        csv_file = os.path.join(os.path.dirname(__file__), "..", "honeypot_login_telemetry.csv")

    rows = []
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)

    if not rows:
        return jsonify({"status": "ERROR", "message": "No telemetry dataset available"}), 404

    req_data = request.get_json(silent=True) or {}
    session_id = request.args.get("session_id") or req_data.get("session_id")
    index = request.args.get("index") or req_data.get("index")
    eval_all = request.args.get("all", "").lower() in ["true", "1"] or req_data.get("all") is True

    def classify_row(row):
        entropy = float(row.get("mouse_movement_entropy", 3.0))
        typing_sim = float(row.get("typing_speed_similarity", 0.9))
        is_bot = (entropy < 0.80) or (typing_sim < 0.30)
        predicted = 1 if is_bot else 0
        actual = int(row.get("target_honeypot_action", 0))
        reasons = []
        if entropy < 0.80:
            reasons.append(f"Low path entropy H={entropy:.2f} (< 0.80 baseline)")
        if typing_sim < 0.30:
            reasons.append(f"Low typing similarity {typing_sim:.2f} (< 0.30 baseline)")
        if not reasons:
            reasons.append(f"Organic jitter H={entropy:.2f}, organic typing {typing_sim:.2f}")

        return {
            "session_id": row.get("session_id", "UNKNOWN"),
            "attack_type": row.get("attack_type", "Standard Sample"),
            "mouse_movement_entropy": entropy,
            "typing_speed_similarity": typing_sim,
            "failed_attempts": int(row.get("failed_attempts", 0)),
            "is_new_device": int(row.get("is_new_device", 0)),
            "vpn_data_center_flag": int(row.get("vpn_data_center_flag", 0)),
            "predicted_label": predicted,
            "classification": "Automated Bot" if predicted == 1 else "Legitimate Human",
            "actual_label": actual,
            "match": (predicted == actual),
            "diagnostics": " & ".join(reasons)
        }

    if eval_all:
        results = [classify_row(r) for r in rows]
        correct = sum(1 for r in results if r["match"])
        total = len(results)
        return jsonify({
            "status": "SUCCESS",
            "dataset": "honeypot_login_telemetry.csv",
            "total_samples": total,
            "correct_predictions": correct,
            "accuracy_percent": round((correct / total) * 100, 2) if total else 0,
            "evaluations": results
        })

    target_row = rows[0]
    if session_id:
        match = next((r for r in rows if r.get("session_id") == session_id), None)
        if match:
            target_row = match
    elif index is not None:
        try:
            idx = int(index)
            if 0 <= idx < len(rows):
                target_row = rows[idx]
        except ValueError:
            pass

    return jsonify({
        "status": "SUCCESS",
        "sample": classify_row(target_row)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting SafeSight Fraud Prevention Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
