import os
import pandas as pd
import numpy as np
import xgboost as xgb
try:
    from levenshtein_engine import LevenshteinTypoEngine
except ImportError:
    from src.levenshtein_engine import LevenshteinTypoEngine

class FraudInferenceEngine:
    """
    Multi-Model ML Risk Pipeline & Inference Engine
    Loads the 2 active XGBoost models:
    1. Login Telemetry Model
    2. Unified Transaction Risk Model (unified_transaction_risk.csv)
    """
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        
        # Load Unified Transaction Model
        self.unified_model = xgb.Booster()
        u_path = os.path.join(model_dir, "xgboost_fraud_model.json")
        self.has_unified = os.path.exists(u_path)
        if self.has_unified:
            self.unified_model.load_model(u_path)

        # Load Login Telemetry Model
        self.login_model = xgb.Booster()
        l_path = os.path.join(model_dir, "xgboost_login_honeypot_model.json")
        self.has_login = os.path.exists(l_path)
        if self.has_login:
            self.login_model.load_model(l_path)

    def score_transaction(self, transaction_data: dict) -> dict:
        """Evaluates Unified Transaction Risk (Dataset 3 Model + Contextual Pre-PIN Interception Signals)"""
        feature_names = [
            'screen_sharing_active',
            'upi_brand_similarity',
            'is_collect_request',
            'sender_spam_score',
            'transaction_amount_ratio'
        ]

        screen_sharing = int(transaction_data.get('screen_sharing_active', 0))
        call_active = int(transaction_data.get('call_active', 0))
        qr_origin = str(transaction_data.get('qr_origin', 'camera')).lower()
        is_collect = int(transaction_data.get('is_collect_request', 0))
        brand_sim = float(transaction_data.get('upi_brand_similarity', 0.0))
        spam_score = float(transaction_data.get('sender_spam_score', 0.0))
        amt_ratio = float(transaction_data.get('transaction_amount_ratio', 1.0))

        features = {
            'screen_sharing_active': screen_sharing,
            'upi_brand_similarity': brand_sim,
            'is_collect_request': is_collect,
            'sender_spam_score': spam_score,
            'transaction_amount_ratio': amt_ratio
        }

        df_input = pd.DataFrame([features])[feature_names]

        if self.has_unified:
            dmat = xgb.DMatrix(df_input)
            raw_prob = float(self.unified_model.predict(dmat)[0])
        else:
            raw_prob = 0.85 if screen_sharing == 1 or brand_sim >= 0.75 else 0.10

        # Contextual fusion based on Section 6 Social Engineering & Pre-PIN Interception Architecture:
        prob = raw_prob
        # 1. Screen sharing + Active phone call = remote desktop coercion signature (AnyDesk / TeamViewer scam)
        if screen_sharing == 1 and call_active == 1:
            prob = max(prob, 0.992)
        # 2. Typo-Squatting VPA (brand_sim >= 0.75) = High Risk phishing
        elif brand_sim >= 0.75:
            prob = max(prob, 0.895)
        # 3. Collect Request Trap with active phone call
        elif is_collect == 1 and call_active == 1:
            prob = max(prob, 0.945)
        # 4. Screen sharing alone
        elif screen_sharing == 1:
            prob = max(prob, 0.880)
        # 5. Forwarded Gallery QR with active call
        elif qr_origin == 'gallery' and call_active == 1:
            prob = max(prob, 0.620)
        # 6. Forwarded Gallery QR alone (breaks live optics chain)
        elif qr_origin == 'gallery':
            prob = max(prob, 0.520)
        # 7. Active phone call during payment alone (potential social engineering)
        elif call_active == 1:
            prob = max(prob, 0.480)
        # 8. Collect request alone
        elif is_collect == 1:
            prob = max(prob, 0.420)

        prob = round(prob, 4)

        if prob < 0.30:
            action = "APPROVE"
            risk_tier = "Low Risk"
            recommendation = "Direct Execution: Zero-Friction Instant Payment Clearance via Native MPIN Sheet"
            intervention_type = "NONE"
        elif 0.30 <= prob <= 0.70:
            action = "DYNAMIC_FRICTION"
            risk_tier = "Medium Risk"
            recommendation = "Trigger Dynamic Friction Screen (5-sec Cooldown, Payee Verification, Active Call Alert)"
            intervention_type = "FRICTION_SCREEN"
        else:
            action = "UPSTREAM_GATEWAY_BLOCK"
            risk_tier = "High Risk"
            recommendation = "Upstream Gateway Interception: Pre-PIN Transaction Termination & Psychological Coercion Break"
            intervention_type = "GATEWAY_REJECTION"

        return {
            "risk_score_P": prob,
            "raw_ml_prob": round(raw_prob, 4),
            "risk_tier": risk_tier,
            "action": action,
            "recommendation": recommendation,
            "intervention_type": intervention_type,
            "features_evaluated": features,
            "contextual_signals": {
                "screen_sharing": bool(screen_sharing),
                "call_active": bool(call_active),
                "qr_origin": qr_origin,
                "is_collect": bool(is_collect),
                "brand_sim": brand_sim,
                "is_typo_squatting": brand_sim >= 0.75
            }
        }

    def score_login_telemetry(self, login_data: dict) -> dict:
        """Evaluates Login Session Telemetry (Dataset 1 Model)"""
        feature_names = [
            'failed_attempts',
            'typing_speed_similarity',
            'mouse_movement_entropy',
            'is_new_device',
            'vpn_data_center_flag'
        ]

        features = {
            'failed_attempts': int(login_data.get('failed_attempts', 0)),
            'typing_speed_similarity': float(login_data.get('typing_speed_similarity', 0.8)),
            'mouse_movement_entropy': float(login_data.get('mouse_movement_entropy', 2.5)),
            'is_new_device': int(login_data.get('is_new_device', 0)),
            'vpn_data_center_flag': int(login_data.get('vpn_data_center_flag', 0))
        }

        df_input = pd.DataFrame([features])[feature_names]

        if self.has_login:
            dmat = xgb.DMatrix(df_input)
            prob = float(self.login_model.predict(dmat)[0])
        else:
            prob = 0.90 if features['failed_attempts'] >= 3 and features['vpn_data_center_flag'] == 1 else 0.05

        prob = round(prob, 4)
        trigger_honeypot = prob >= 0.50

        return {
            "model_name": "Login Telemetry Honeypot Model (Dataset 1)",
            "honeypot_probability": prob,
            "trigger_honeypot": trigger_honeypot,
            "action": "ROUTE_TO_GHOST_SESSION" if trigger_honeypot else "ALLOW_LOGIN",
            "features_evaluated": features
        }
