# PROJECT AEGIS: COMPLETE SYSTEM FLOWCHART & ARCHITECTURE BLUEPRINT
**Document Reference:** AEG-FLOWCHART-SPEC-2026  
**Classification:** Confidential / Technical Architecture & Payment Flowchart Specification  
**Target Systems:** UPI 2.0 Rails, Core Banking System (CBS), NPCI Switch, Ghost Honeypot Sandbox, Behavioral Biometrics Guard  

---

## 1. DEDICATED UPI 2.0 PRE-PIN SHIELD & PAYMENT RAIL ARCHITECTURE FLOWCHART

This flowchart illustrates the end-to-end transaction lifecycle of a UPI payment from the instant the user interacts with a VPA or QR code to final NPCI settlement or pre-PIN upstream rejection.

```
===================================================================================================================
                       FLOWCHART 1: DEDICATED UPI 2.0 PRE-PIN DEFENSE & PAYMENT LIFECYCLE
===================================================================================================================

[ USER INITIATES UPI PAYMENT ]
  │
  ├──────────────────────────────────────────────────────┐
  ▼                                                      ▼
[ SCANS QR CODE ]                                      [ ENTERS DESTINATION VPA ]
  │                                                      (e.g., 'ph0nepe@okaxis', 'rahulgear@okaxis')
  ├────────────────────────────┬────────────────────────────┐
  │                            │                            │
  ▼                            ▼                            ▼
[ LIVE OPTICAL CAMERA ]     [ FORWARDED GALLERY IMAGE ]     │
  • Hardware Camera2 API      • Intent.ACTION_PICK          │
  • Continuous IMU tremor     • Static storage bitmap       │
  • Photon shot noise         • JPEG compression artifacts  │
  • Friction Weight: +0.00    • Friction Weight: +0.48      │
  │                            │                            │
  └────────────────────────────┴─────────────┬──────────────┘
                                             │
                                             ▼
                        [ LEVENSHTEIN TYPO-SQUATTING ENGINE ]
                        • Sub-15ms In-Memory Matrix + Redis Trie Whitelist
                        • Normalized Edit Distance: Sim(s1, s2) = (|s1|+|s2|-D)/(|s1|+|s2|)
                        • Checks brand spoofing (e.g., 'ph0nepe' -> 88% similarity)
                        • Checks scam affixes: 'support', 'kyc', 'refund', 'officer'
                                             │
                                             ▼
                        [ CLIENT-SIDE OS SIGNAL HARVESTERS ]
                        ├── AudioManager.mode: MODE_IN_CALL / MODE_IN_COMMUNICATION (Phone Call Active)
                        ├── DisplayManager / UIScreen.isCaptured: MediaProjection (AnyDesk Mirror Active)
                        └── Pointer & Touch Biometrics: Shannon Path Entropy H & Curvature κ
                                             │
                                             ▼
                        [ AEGIS CLIENT CRYPTO PACKAGER ]
                        • Compiles Telemetry Payload (Sensor metrics, Timestamps, Device Fingerprint)
                        • Generates Tamper-Proof JWT signed with Android Keystore / Apple Secure Enclave
                                             │
                                             ▼
[ TLS 1.3 / mTLS ENCRYPTED TRANSPORT: POST /api/v1/payments/transfer ]
  Header: X-Aegis-Telemetry-Token: eyJhbGciOiJFUzI1Ni...
                                             │
                                             ▼
[ UPSTREAM API GATEWAY / REVERSE PROXY (Envoy / Kong) ]
  • Validates JWT Hardware Signature via HSM Key Vault
  • Dispatches Telemetry to Aegis Risk Engine via gRPC (< 3.0ms SLA)
                                             │
                                             ▼
[ AEGIS UNIFIED RISK INFERENCE ENGINE (ONNX C++ Daemon) ]
  • Inputs: Levenshtein Score + Call Flag + Screen Share Flag + QR Origin + Amount Ratio + Biometrics
  • Evaluates XGBoost Model 3 Decision Boundary
  • Calculates Unified Calibrated Risk Probability: P ∈ [0.00, 1.00]
                                             │
                                             ▼
+────────────────────────────────────────────┴────────────────────────────────────────────+
|                                    DECISION ROUTER & ENVOY ENFORCEMENT SWITCH           |
+────────────────────────────────────┬────────────────────────────────────────────────────+
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           ▼                         ▼                         ▼
   [ LOW RISK: P < 0.30 ]   [ MEDIUM RISK: 0.30 <= P <= 0.70 ] [ HIGH RISK: P > 0.70 / IN-CALL ]
           │                         │                         │
           │ Action: APPROVE         │ Action: DYNAMIC FRICTION│ Action: GATEWAY BLOCK
           │                         │                         │
           ▼                         ▼                         ▼
   [ NATIVE HARDWARE MPIN ]  [ DYNAMIC FRICTION SCREEN ]       [ UPSTREAM REJECTION ]
   • Isolated MPIN sheet     • Injected via FLAG_SECURE        • Terminates at API Gateway
   • User inputs 4/6-digit   • 5-second mandatory cooldown     • Returns HTTP 403 Forbidden
     authentic banking PIN   • Active Phone Call Warning       • Code: Z9_SECURITY_COERCION
           │                 • Gallery QR Forward Warning      • Pre-PIN Entry Withheld
           │                 • Payee Verification Re-check     • Shifts blame to bank
           │                         │                         • Victim Safety Protected
           │                         ▼                         • Emergency 1930 / Freeze controls
           │                 [ USER WAITS 5s & CONFIRMS ]              │
           │                         │                                 │
           └─────────────────────────┼─────────────────────────────────┘
                                     │ (Clearance Granted)
                                     ▼
                      [ CORE BANKING SWITCH & NPCI RAILS ]
                      • Dispatches ISO 20022 XML Payment Initiation Message
                      • Cryptographic HSM Handshake with NPCI UPI Switch
                      • Real-Time Gross Settlement / IMPS Clearing
                                     │
                                     ▼
                      [ AUTHENTIC SETTLEMENT RECEIPT ]
                      • Transaction ID: UPI/2026/09/TRX_89210
                      • Bank Account Debited & Real Funds Transferred
===================================================================================================================
```

---

## 2. WHOLE PROJECT MASTER SYSTEM ARCHITECTURE FLOWCHART

This comprehensive architecture diagram illustrates how the core operational pillars—**UPI 2.0 Payments**, **Deceptive Login Honeypot**, and **Behavioral Biometrics**—unify into a single centralized threat intelligence and enforcement fabric.

```
===================================================================================================================
                                FLOWCHART 2: WHOLE PROJECT MASTER UNIFIED ARCHITECTURE
===================================================================================================================

[ ADVERSARY / CLIENT CHANNELS ]
  │
  ├── CHANNEL A: Web / Mobile Login Portal (Authentication Vector)
  ├── CHANNEL B: UPI 2.0 Payment Terminal (Social Engineering / Remote Coercion Vector)
    │
  ▼
+-----------------------------------------------------------------------------------------------------------------+
| CLIENT-SIDE SENSOR & TELEMETRY HARVESTING LAYER                                                                |
+-----------------------------------------------------------------------------------------------------------------+
| • Behavioral Biometrics: Pointer Path Entropy H(Θ) at 60 Hz, Curvature κ, Keystroke Dwell/Flight (performance.now)|
| • OS Signal Probes: Android AudioManager.mode (Call Hook), DisplayManager / UIScreen.isCaptured (Screen Share)  |
| • Hardware & Context Probes: Camera2 vs Gallery Bitmap Isolation, WebGL / Canvas Device Hash                   |
+-----------------------------------------------------------------------------------------------------------------+
  │
  ▼ (Client Packages Signed JWT Token: X-Aegis-Telemetry-Token)
+-----------------------------------------------------------------------------------------------------------------+
| UPSTREAM API GATEWAY & SHADOW ROUTER (Envoy / Kong Edge Reverse Proxy)                                         |
+-----------------------------------------------------------------------------------------------------------------+
| • Hardware Attestation & Device Keystore Signature Verification via HSM                                         |
| • Invariant Endpoint Routing: POST /api/v1/payments/transfer (Zero URL Leaks for Burp/Charles Proxy)           |
| • Inspects JWT Claims: 'routing_tier' (ghost_honeypot vs standard) & Threat Payload                             |
+-----------------------------------------------------------------------------------------------------------------+
  │
  ├─── IF 'routing_tier' == 'ghost_honeypot' (Tainted Login: 3 Failed Passwords OR H < 0.50)
  │    │
  │    ▼
  │  +-----------------------------------------------------------------------------------------------------------+
  │  | SUBSYSTEM 1: GHOST HONEYPOT SANDBOX POD (Isolated Threat Intelligence Microservice)                      |
  │  +-----------------------------------------------------------------------------------------------------------+
  │  | • Perceived Entry: Synthetic Luxury Banking Replica displaying ₹84,250.00 Balance (Ephemeral Redis 30m)   |
  │  | • Deterministic Stalling Engine: Artificial 800ms–1500ms Switch Lag                                       |
  │  | • Failure Cycle: NPCI_ERR_ZM (Timeout) -> BANK_ERR_U16 (Throttled) -> SYS_TIMEOUT (Clearing Hold)          |
  │  | • Background Forensic Beacon: Ephemeral WebRTC RTCPeerConnection harvests public STUN candidate IP        |
  │  | • Logs Data To: honeypot_login_telemetry.csv, honeypot_session_forensics.csv, honeypot_transfer_intercept.csv|
  │  | • Actions: Intercepted destination mule VPA forwarded to SOC to PROACTIVELY FREEZE MULE ACCOUNTS          |
  │  +-----------------------------------------------------------------------------------------------------------+
  │
  └─── IF 'routing_tier' == 'standard' (Active Customer Session)
       │
       ▼
+-----------------------------------------------------------------------------------------------------------------+
| AEGIS DISTRIBUTED INFERENCE & DETERMINISTIC EVALUATION FABRIC (gRPC < 3.0ms SLA)                               |
+-----------------------------------------------------------------------------------------------------------------+
|                                                                                                                 |
|  [ DETERMINISTIC SCANNERS ]                            [ DISTRIBUTED DATA & GRAPH FABRIC ]                      |
|  ├── Levenshtein Typo Engine: <15ms Fuzzy Match        ├── Redis Cluster: Brand Trie Whitelist & Cache          |
|  └── Shannon Biometrics Engine: H(D)=-Σ P log P         └── Neo4j Graph DB: Mule Account Fan-Out Velocity        |
|      Flags impossible relocation (>900 km/h)               (1-3 hops traversal within 5-min lookback)           |
|                                                                                                                 |
|  [ MACHINE LEARNING CLASSIFIER SUITE (ONNX Runtime C++ Sidecar Daemon with OpenMP Parallelization) ]           |
|  ├── Model 1 (Login Classifier): Evaluates failed attempts, typing cadence, and mouse entropy H                |
|  └── Model 3 (Unified UPI Classifier): Evaluates brand similarity, call active, screen share, and QR origin    |
|                                                                                                                 |
|  [ CALIBRATED RISK PROBABILITY CALCULATION ]                                                                    |
|  └── Generates Risk Score P ∈ [0.00, 1.00]                                                                      |
|                                                                                                                 |
+-----------------------------------------------------------------------------------------------------------------+
  │
  ▼
+-----------------------------------------------------------------------------------------------------------------+
| DECISION SWITCH & ENFORCEMENT ROUTER (Context-Sensitive Policy Matrix)                                         |
+-----------------------------------------------------------------------------------------------------------------+
  │
  │                                   │                                   │                                   │
  ├───────────────────────────────────┬───────────────────────────────────┐
  │                                   │                                   │
  ▼ (Case 1: P < 0.30)                ▼ (Case 2: 0.30 <= P <= 0.70)       ▼ (Case 3: P > 0.70 OR Live Call)
[ ZERO FRICTION CLEARANCE ]     [ DYNAMIC FRICTION SCREEN ]         [ UPSTREAM GATEWAY BLOCK ]
  • Dispatches native MPIN sheet  • Native FLAG_SECURE overlay        • Immediate HTTP 403 Forbidden
  • Connects to Core Banking      • 5s mandatory cooldown timer       • Error: Z9_SECURITY_COERCION
  • Forward to NPCI UPI Switch    • Active Call & Gallery QR Warn     • Pre-PIN Entry Withheld
  • Real settlement occurs        • Explicit voluntary re-affirm      • Victim Coercion Broken Safe
                                  • On complete -> proceed to MPIN    • Emergency 1930 Helpline Offered
                                                                      • Zero Real Funds Debited
===================================================================================================================
```

---

## 3. TECHNICAL SEQUENCE DIAGRAM: UPI PRE-PIN INTERCEPTION VS SETTLEMENT

Below is the message-level sequence diagram detailing how telemetry tokens, gateway evaluation, dynamic friction, and settlement operate across time:

```
Victim / Client App            Envoy Gateway            Aegis Risk Engine         NPCI / CBS Switch
        │                              │                        │                         │
        │ 1. User Scans Gallery QR     │                        │                         │
        │    & Enters UPI Amount       │                        │                         │
        │─────────────────────────────>│                        │                         │
        │    (POST /payments/transfer  │                        │                         │
        │     + Signed Telemetry JWT)  │                        │                         │
        │                              │ 2. gRPC Risk Probe     │                         │
        │                              │───────────────────────>│                         │
        │                              │                        │ 3. Run Levenshtein      │
        │                              │                        │    + Screen Share Probe │
        │                              │                        │    + XGBoost Model 3    │
        │                              │                        │    Score: P = 0.62      │
        │                              │                        │    (Medium Friction)    │
        │                              │ 4. Return P=0.62       │                         │
        │                              │<───────────────────────│                         │
        │ 5. HTTP 200 (Action: FRICTION)                        │                         │
        │<─────────────────────────────│                        │                         │
        │                              │                        │                         │
        │ 6. Inject 5s Cooldown Modal  │                        │                         │
        │    "Warning: Gallery QR"     │                        │                         │
        │    (Victim Reviews & Verifies)                        │                         │
        │                              │                        │                         │
        │ 7. Friction Complete:        │                        │                         │
        │    User Enters Native MPIN   │                        │                         │
        │─────────────────────────────>│                        │                         │
        │                              │ 8. Forward to NPCI     │                         │
        │                              │─────────────────────────────────────────────────>│
        │                              │                        │                         │ 9. Execute Clearing
        │                              │                        │                         │    & Settlement
        │                              │ 10. Clearing Response (ISO-20022 XML: Success)   │
        │                              │<─────────────────────────────────────────────────│
        │ 11. Display Authentic Receipt│                        │                         │
        │<─────────────────────────────│                        │                         │
```

---

## 4. SUBSYSTEM MATRIX: COMPLETE ENGINE CAPABILITIES

| Subsystem Component | Operational Triggers | Latency / SLA | Primary Mathematical Model | Regulatory / Enforcement Output |
| :--- | :--- | :--- | :--- | :--- |
| **UPI Pre-PIN Shield** | Target VPA input, QR code scan | $< 15\text{ms}$ | Levenshtein Distance & XGBoost Model 3 | Upstream Gateway Rejection ($P > 0.70$) or 5s Dynamic Friction ($0.30 \le P \le 0.70$) |
| **Ghost Honeypot Sandbox** | 3 failed passwords + anomalous $H < 0.50$ | Ephemeral (30-min TTL) | Shannon Path Entropy $H(\Theta) = -\sum p_k \log_2(p_k)$ | Synthetic ₹84,250 balance, 800–1500ms stalling delays, WebRTC public IP harvest |
| **Mule Graph Engine** | Intercepted beneficiary VPA | $< 15\text{ms}$ | Neo4j Cypher multi-hop fan-out traversal | Real-time proactive freeze dispatched to Central Fraud Engine / 1930 Portal |

---
**Report Compiled by:** Google DeepMind Advanced Agentic Coding Pair (Project Aegis Architecture Team)  
**Status:** Flowchart Specifications Complete • Ready for Enterprise Implementation
