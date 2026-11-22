import sys
sys.path.insert(0, 'c:/Users/dell/Desktop/project 2')
from src.app import app

client = app.test_client()

print("1. Testing Check VPA for rahulgear@okaxis:")
res = client.post('/api/check-vpa', json={'vpa': 'rahulgear@okaxis'})
vpa_data = res.get_json()
print("   vpa_data:", vpa_data['risk_verdict'], "BBPS:", vpa_data['is_bbps_verified'])

print("\n2. Testing Score Transaction for Clean rahulgear@okaxis:")
res_tx = client.post('/api/score-transaction', json={
    'upi_brand_similarity': vpa_data['max_similarity'] if vpa_data['is_typo_squatting'] else 0.0,
    'is_bbps_verified': 1 if vpa_data['is_bbps_verified'] else 0,
    'is_typo_squatting': 1 if vpa_data['is_typo_squatting'] else 0,
    'transaction_amount_ratio': 1.0,
    'is_collect_request': 0,
    'screen_sharing_active': 0,
    'call_active': 0,
    'qr_origin': 'camera'
})
tx_data = res_tx.get_json()
print("   tx_data:", tx_data['risk_score_P'], tx_data['risk_tier'], tx_data['action'], tx_data['intervention_type'])
assert tx_data['intervention_type'] == 'NONE', "Clean payment must have intervention_type NONE!"
assert tx_data['action'] == 'APPROVE', "Clean payment must be APPROVED!"

print("\n3. Testing Wire Transfer (/api/sandbox/transfer) for legitimate user:")
res_wire = client.post('/api/sandbox/transfer', json={
    'amount': 1500.0,
    'beneficiary': 'sarah.partner@icici',
    'is_legitimate': True
})
wire_data = res_wire.get_json()
print("   wire_data:", wire_data['status'], wire_data['transaction_id'], wire_data['message'])
assert wire_data['status'] == 'success', "Wire transfer must succeed!"

print("\n4. Testing Attack UPI Scam (ph0nepe@okaxis with screen share + call):")
res_ph0nepe = client.post('/api/check-vpa', json={'vpa': 'ph0nepe@okaxis'})
vpa_ph0nepe = res_ph0nepe.get_json()
res_attack = client.post('/api/score-transaction', json={
    'upi_brand_similarity': vpa_ph0nepe['max_similarity'],
    'is_bbps_verified': 0,
    'is_typo_squatting': 1,
    'transaction_amount_ratio': 24.0,
    'is_collect_request': 1,
    'screen_sharing_active': 1,
    'call_active': 1,
    'qr_origin': 'gallery'
})
attack_data = res_attack.get_json()
print("   attack_data:", attack_data['risk_score_P'], attack_data['risk_tier'], attack_data['action'], attack_data['intervention_type'])
assert attack_data['intervention_type'] == 'GATEWAY_REJECTION', "Attack must trigger GATEWAY_REJECTION!"

print("\n5. Testing Honeypot Stalled Transfer (/api/honeypot/stalled-transfer):")
res_stall = client.post('/api/honeypot/stalled-transfer', json={
    'amount': 75000.0,
    'beneficiary': 'mule_sweep01@okaxis',
    'retry_count': 1
})
stall_data = res_stall.get_json()
print("   stall_data:", stall_data['status'], stall_data['error_code'], stall_data['message'])
assert stall_data['error_code'] == 'NPCI_ERR_ZM', "Honeypot stall error must be NPCI_ERR_ZM!"

print("\nALL FLASK ROUTE INTEGRATION TESTS PASSED 100%!")
