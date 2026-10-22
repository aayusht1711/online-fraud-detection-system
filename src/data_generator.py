import os
import numpy as np
import pandas as pd

def generate_datasets(output_dir: str = "data"):
    """
    Generates synthetic tabular datasets for Project Aegis (UPI Fraud + Deceptive Honeypot).
    Creates:
    1. honeypot_login_training.csv (2,000 rows for ML model training)
    2. unified_transaction_risk.csv (5,000 rows for UPI ML model training)
    Note: honeypot_login_telemetry.csv is preserved intact for demo testing endpoints.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)

    # -------------------------------------------------------------
    # Dataset 1: honeypot_login_training.csv (2,000 synthetic rows)
    # -------------------------------------------------------------
    n_login = 2000
    failed_attempts = np.random.choice([0, 1, 2, 3, 4, 5], size=n_login, p=[0.55, 0.25, 0.10, 0.05, 0.03, 0.02])
    typing_speed = np.random.uniform(0.0, 1.0, size=n_login)
    mouse_entropy = np.random.uniform(0.0, 5.0, size=n_login)
    is_new_device = np.random.choice([0, 1], size=n_login, p=[0.70, 0.30])
    vpn_flag = np.random.choice([0, 1], size=n_login, p=[0.85, 0.15])

    # Rule logic for honeypot login trigger:
    # 3+ failed attempts AND (low entropy or new device or vpn)
    honeypot_action = (
        (failed_attempts >= 3) & 
        ((mouse_entropy < 0.5) | (is_new_device == 1) | (vpn_flag == 1) | (typing_speed < 0.3))
    ).astype(int)

    login_df = pd.DataFrame({
        'session_id': [f"S_{1000 + i}" for i in range(n_login)],
        'failed_attempts': failed_attempts,
        'typing_speed_similarity': np.round(typing_speed, 2),
        'mouse_movement_entropy': np.round(mouse_entropy, 2),
        'is_new_device': is_new_device,
        'vpn_data_center_flag': vpn_flag,
        'target_honeypot_action': honeypot_action
    })
    login_training_path = os.path.join(output_dir, "honeypot_login_training.csv")
    login_df.to_csv(login_training_path, index=False)
    print(f"Dataset 1 (Login Training) generated: {login_training_path} ({len(login_df)} rows)")

    # -------------------------------------------------------------
    # Dataset 2: unified_transaction_risk.csv (5,000 synthetic rows)
    # -------------------------------------------------------------
    n_records = 5000
    screen_share = np.random.choice([0, 1], size=n_records, p=[0.94, 0.06])
    brand_sim = np.random.uniform(0.0, 1.0, size=n_records)
    is_collect = np.random.choice([0, 1], size=n_records, p=[0.85, 0.15])
    spam_score = np.random.uniform(0.0, 1.0, size=n_records)
    amount_ratio = np.random.lognormal(mean=0.0, sigma=0.75, size=n_records)

    # Social engineering APP scams (remote screen share, brand spoofing, collect request trap, high spam)
    social_eng_fraud = (
        ((screen_share == 1) & (is_collect == 1) & (spam_score > 0.40)) |
        ((brand_sim > 0.75) & (is_collect == 1) & (spam_score > 0.40)) |
        ((screen_share == 1) & (brand_sim > 0.70)) |
        ((screen_share == 1) & (amount_ratio > 3.0))
    )

    labels = social_eng_fraud.astype(int)

    unified_df = pd.DataFrame({
        'record_id': [f"REC_{i+1:03d}" for i in range(n_records)],
        'screen_sharing_active': screen_share,
        'upi_brand_similarity': np.round(brand_sim, 2),
        'is_collect_request': is_collect,
        'sender_spam_score': np.round(spam_score, 2),
        'transaction_amount_ratio': np.round(amount_ratio, 2),
        'is_fraud': labels
    })
    unified_path = os.path.join(output_dir, "unified_transaction_risk.csv")
    unified_df.to_csv(unified_path, index=False)
    print(f"Dataset 2 (Unified UPI) generated: {unified_path} ({len(unified_df)} rows, {np.sum(labels)} fraud instances)")

if __name__ == "__main__":
    generate_datasets()
