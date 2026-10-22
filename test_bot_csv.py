import os
import pandas as pd
import numpy as np

def evaluate_bot_telemetry(csv_path="honeypot_login_telemetry.csv"):
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "data", "honeypot_login_telemetry.csv")

    df = pd.read_csv(csv_path)
    print("=" * 65)
    print("      PROJECT AEGIS: TELEMETRY BOT EVALUATION TEST")
    print("=" * 65)
    
    correct_predictions = 0
    total = len(df)

    for idx, row in df.iterrows():
        # Heuristic rules derived from our biometrics model:
        # 1. Entropy < 0.80 indicates straight-line robotic cursor
        # 2. Typing similarity < 0.30 indicates bot injection / stolen profile
        # 3. Failed attempts >= 2 with new device
        is_bot_detected = (
            (row['mouse_movement_entropy'] < 0.80) or 
            (row['typing_speed_similarity'] < 0.30)
        )
        predicted_label = 1 if is_bot_detected else 0
        actual_label = int(row['target_honeypot_action'])
        
        status = "[MATCH]" if predicted_label == actual_label else "[MISMATCH]"
        if predicted_label == actual_label:
            correct_predictions += 1
            
        print(f"[{row['session_id']}] {row['attack_type']:<30} | Predicted: {predicted_label} | Actual: {actual_label} | {status}")

    accuracy = (correct_predictions / total) * 100
    print("=" * 65)
    print(f"Evaluation Accuracy: {accuracy:.2f}% ({correct_predictions}/{total} records)")
    print("=" * 65)

if __name__ == "__main__":
    evaluate_bot_telemetry()
