import sys
sys.path.insert(0, 'c:/Users/dell/Desktop/project 2')
from src.inference_engine import FraudInferenceEngine
from src.levenshtein_engine import LevenshteinTypoEngine

engine = FraudInferenceEngine('c:/Users/dell/Desktop/project 2/models')

def test_tx(vpa, screen=0, call=0, collect=0, qr='camera'):
    v = LevenshteinTypoEngine.evaluate_vpa(vpa)
    res = engine.score_transaction({
        'upi_brand_similarity': v['max_similarity'],
        'is_bbps_verified': v['is_bbps_verified'],
        'is_typo_squatting': v['is_typo_squatting'],
        'screen_sharing_active': screen,
        'call_active': call,
        'is_collect_request': collect,
        'transaction_amount_ratio': 1.0,
        'qr_origin': qr
    })
    print(f"{vpa:22} -> risk: {res['risk_score_P']:<6} ({res['risk_tier']:<12}) action: {res['action']:<25} intervention: {res['intervention_type']}")

print("--- Clean Transactions ---")
test_tx('rahulgear@okaxis')
test_tx('elec.173@okaxis')
test_tx('sharma.kirana@okaxis')

print("\n--- Attacks / Threats ---")
test_tx('elec.174@okaxis', call=1, qr='gallery')
test_tx('ph0nepe@okaxis', screen=1, call=1, collect=1, qr='gallery')
