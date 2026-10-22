import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

def train_all_models(data_dir: str = "data", model_dir: str = "models"):
    """
    Trains dedicated XGBoost Classifiers for Project Aegis (UPI Fraud + Honeypot):
    1. Honeypot Login Telemetry Model (honeypot_login_training.csv)
    2. Unified UPI Transaction Risk Classifier (unified_transaction_risk.csv)
    """
    os.makedirs(model_dir, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # Model 1: Login Telemetry Honeypot Classifier
    # -------------------------------------------------------------------------
    login_training_path = os.path.join(data_dir, "honeypot_login_training.csv")
    login_fallback_path = os.path.join(data_dir, "honeypot_login_telemetry.csv")
    login_path = login_training_path if os.path.exists(login_training_path) else login_fallback_path

    if os.path.exists(login_path):
        print("\n=======================================================")
        print(f"1. Training Login Telemetry Honeypot Model ({os.path.basename(login_path)})...")
        print("=======================================================")
        df_login = pd.read_csv(login_path)
        
        # Drop non-numeric columns (e.g. session_id, attack_type)
        numeric_cols = [c for c in df_login.select_dtypes(include=[np.number]).columns]
        df_login = df_login[numeric_cols]
            
        X1 = df_login.drop(columns=['target_honeypot_action'])
        y1 = df_login['target_honeypot_action']
        
        X1_train, X1_test, y1_train, y1_test = train_test_split(
            X1, y1, test_size=0.20, random_state=42, stratify=y1
        )
        
        pos_weight1 = (len(y1_train) - sum(y1_train)) / max(sum(y1_train), 1)
        model1 = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            scale_pos_weight=pos_weight1,
            eval_metric='logloss',
            random_state=42
        )
        model1.fit(X1_train, y1_train)
        
        preds1 = model1.predict(X1_test)
        probs1 = model1.predict_proba(X1_test)[:, 1]
        auc1 = roc_auc_score(y1_test, probs1)
        print(classification_report(y1_test, preds1))
        print(f"Login Honeypot Model ROC-AUC: {auc1:.4f}")
        
        model1_path = os.path.join(model_dir, "xgboost_login_honeypot_model.json")
        model1.save_model(model1_path)
        print(f"Saved to {model1_path}")

    # -------------------------------------------------------------------------
    # Model 2: Unified UPI Transaction Risk Classifier
    # -------------------------------------------------------------------------
    unified_path = os.path.join(data_dir, "unified_transaction_risk.csv")
    if os.path.exists(unified_path):
        print("\n=======================================================")
        print("2. Training Unified UPI Transaction Risk Model...")
        print("=======================================================")
        df_unified = pd.read_csv(unified_path)
        if 'record_id' in df_unified.columns:
            df_unified = df_unified.drop(columns=['record_id'])
            
        # Ensure only numeric columns are used
        numeric_cols = [c for c in df_unified.select_dtypes(include=[np.number]).columns]
        df_unified = df_unified[numeric_cols]

        X2 = df_unified.drop(columns=['is_fraud'])
        y2 = df_unified['is_fraud']
        
        X2_train, X2_test, y2_train, y2_test = train_test_split(
            X2, y2, test_size=0.20, random_state=42, stratify=y2
        )
        
        pos_weight2 = (len(y2_train) - sum(y2_train)) / max(sum(y2_train), 1)
        model2 = XGBClassifier(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            scale_pos_weight=pos_weight2,
            eval_metric='logloss',
            random_state=42
        )
        model2.fit(X2_train, y2_train)
        
        preds2 = model2.predict(X2_test)
        probs2 = model2.predict_proba(X2_test)[:, 1]
        auc2 = roc_auc_score(y2_test, probs2)
        print(classification_report(y2_test, preds2))
        print(f"Unified UPI Model ROC-AUC: {auc2:.4f}")
        
        model2_path = os.path.join(model_dir, "xgboost_fraud_model.json")
        model2.save_model(model2_path)
        print(f"Saved to {model2_path}")

    print("\nAll active ML models (Login Honeypot & Unified UPI) trained and saved successfully!")

if __name__ == "__main__":
    train_all_models()
