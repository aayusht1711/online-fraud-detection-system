import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from levenshtein_engine import LevenshteinTypoEngine
from inference_engine import FraudInferenceEngine
from app import app

class TestSafeSightEngines(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        cls.engine = FraudInferenceEngine(model_dir=cls.model_dir)
        cls.client = app.test_client()

    def test_levenshtein_typo(self):
        # Exact whitelist brand match
        res_exact = LevenshteinTypoEngine.evaluate_vpa("paytm@upi")
        self.assertEqual(res_exact["max_similarity"], 1.0)
        self.assertFalse(res_exact["is_typo_squatting"])

        # Typo-squatting handle
        res_typo = LevenshteinTypoEngine.evaluate_vpa("paytmm@upi")
        self.assertGreater(res_typo["max_similarity"], 0.75)
        self.assertTrue(res_typo["is_typo_squatting"])

    def test_tier_thresholds(self):
        # 1. Tier 1: Low Risk (P < 0.30) -> APPROVE
        clean_payload = {
            "screen_sharing_active": 0,
            "call_active": 0,
            "qr_origin": "camera",
            "upi_brand_similarity": 0.05,
            "is_collect_request": 0,
            "sender_spam_score": 0.02,
            "transaction_amount_ratio": 1.0
        }
        res_low = self.engine.score_transaction(clean_payload)
        self.assertEqual(res_low["action"], "APPROVE")
        self.assertEqual(res_low["risk_tier"], "Low Risk")
        self.assertEqual(res_low["intervention_type"], "NONE")
        self.assertLess(res_low["risk_score_P"], 0.30)

        # 2. Tier 2: Medium Risk (0.30 <= P <= 0.70) -> DYNAMIC_FRICTION
        # Forwarded gallery QR with active call creates social-engineering friction
        friction_payload = {
            "screen_sharing_active": 0,
            "call_active": 1,
            "qr_origin": "gallery",
            "upi_brand_similarity": 0.10,
            "is_collect_request": 0,
            "sender_spam_score": 0.15,
            "transaction_amount_ratio": 1.2
        }
        res_med = self.engine.score_transaction(friction_payload)
        self.assertEqual(res_med["action"], "DYNAMIC_FRICTION")
        self.assertEqual(res_med["risk_tier"], "Medium Risk")
        self.assertEqual(res_med["intervention_type"], "FRICTION_SCREEN")
        self.assertGreaterEqual(res_med["risk_score_P"], 0.30)
        self.assertLessEqual(res_med["risk_score_P"], 0.70)

        # 3. Tier 3: High Risk (P > 0.70) -> UPSTREAM_GATEWAY_BLOCK
        block_payload = {
            "screen_sharing_active": 0,
            "call_active": 0,
            "qr_origin": "camera",
            "upi_brand_similarity": 0.95,  # High typo-squatting
            "is_collect_request": 1,
            "sender_spam_score": 0.85,
            "transaction_amount_ratio": 4.5
        }
        res_high = self.engine.score_transaction(block_payload)
        self.assertEqual(res_high["action"], "UPSTREAM_GATEWAY_BLOCK")
        self.assertEqual(res_high["risk_tier"], "High Risk")
        self.assertEqual(res_high["intervention_type"], "GATEWAY_REJECTION")
        self.assertGreater(res_high["risk_score_P"], 0.70)

    def test_screen_sharing_with_call_forces_block(self):
        # AnyDesk / TeamViewer remote coercion signature (Section 6)
        coercion_payload = {
            "screen_sharing_active": 1,
            "call_active": 1,
            "upi_brand_similarity": 0.10,
            "is_collect_request": 0,
            "sender_spam_score": 0.10,
            "transaction_amount_ratio": 1.0
        }
        res = self.engine.score_transaction(coercion_payload)
        self.assertEqual(res["action"], "UPSTREAM_GATEWAY_BLOCK")
        self.assertEqual(res["risk_tier"], "High Risk")
        self.assertEqual(res["intervention_type"], "GATEWAY_REJECTION")
        self.assertGreaterEqual(res["risk_score_P"], 0.992)

    def test_stalled_transfer_quarantine_at_retry_4(self):
        # Cycle 1 -> NPCI_ERR_ZM / BANK_ERR_U16
        res1 = self.client.post("/api/honeypot/stalled-transfer", json={
            "session_id": "S_TEST",
            "amount": 75000,
            "beneficiary": "mule_sweep01@okaxis",
            "retry_count": 1
        })
        self.assertEqual(res1.status_code, 200)
        data1 = res1.get_json()
        self.assertIn(data1["error_code"], ["NPCI_ERR_ZM", "BANK_ERR_U16"])

        # Cycle 4 -> AML_ERR_QUARANTINE (Channel Quarantined / Hard Lock)
        res4 = self.client.post("/api/honeypot/stalled-transfer", json={
            "session_id": "S_TEST",
            "amount": 75000,
            "beneficiary": "mule_sweep01@okaxis",
            "retry_count": 4
        })
        self.assertEqual(res4.status_code, 200)
        data4 = res4.get_json()
        self.assertEqual(data4["error_code"], "AML_ERR_QUARANTINE")
        self.assertIn("exceeded", data4["message"].lower())
        self.assertEqual(data4["retry_count"], 4)

if __name__ == "__main__":
    unittest.main()
