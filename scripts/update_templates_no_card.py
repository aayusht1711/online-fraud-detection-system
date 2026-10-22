import os
import re

def update_index_html():
    path = os.path.join('templates', 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Nav button
    target_nav = """            <button id="navCards" onclick="switchTab('cards')" class="tab-btn flex items-center gap-2">
                <i class="fa-solid fa-credit-card text-xs"></i> Card Security
            </button>\n"""
    if target_nav in content:
        content = content.replace(target_nav, "")

    # Stray buttons if any
    stray_btns = """            <a href="/3d" class="tab-btn flex items-center gap-2 text-cyan-400 hover:text-cyan-300 border border-cyan-500/30 bg-cyan-950/40 px-3 py-1.5 rounded-xl transition font-medium">
                <i class="fa-solid fa-cube text-xs text-cyan-400"></i> 3D Architecture
            </a>
            </button>
            </button>"""
    clean_btns = """            <a href="/3d" class="tab-btn flex items-center gap-2 text-cyan-400 hover:text-cyan-300 border border-cyan-500/30 bg-cyan-950/40 px-3 py-1.5 rounded-xl transition font-medium">
                <i class="fa-solid fa-cube text-xs text-cyan-400"></i> 3D Architecture
            </a>"""
    if stray_btns in content:
        content = content.replace(stray_btns, clean_btns)

    # 2. Bank nav credit cards
    target_bank_nav = """<button onclick="bankNavAction('Credit Cards')" class="w-full text-left px-4 py-2 hover:bg-blue-50 hover:text-blue-800 text-xs flex items-center gap-2 transition"><i class="fa-solid fa-credit-card text-blue-500 w-4"></i> Credit Cards</button>"""
    repl_bank_nav = """<button onclick="bankNavAction('Net Banking')" class="w-full text-left px-4 py-2 hover:bg-blue-50 hover:text-blue-800 text-xs flex items-center gap-2 transition"><i class="fa-solid fa-globe text-blue-500 w-4"></i> Net Banking</button>"""
    if target_bank_nav in content:
        content = content.replace(target_bank_nav, repl_bank_nav)

    # 3. Card POS
    content = content.replace('Today &bull; Card POS', 'Today &bull; Merchant POS')

    # 4. viewCards panel
    start_vc = content.find('<div id="viewCards"')
    if start_vc != -1:
        end_vc_str = '<!-- GLOBAL FOOTER BAR -->'
        end_vc = content.find(end_vc_str, start_vc)
        assert end_vc != -1, 'GLOBAL FOOTER BAR not found after viewCards'
        vc_block = content[start_vc:end_vc]
        content = content[:start_vc] + content[end_vc:]
        print(f"Removed viewCards block of length {len(vc_block)} in index.html")

    # 5. Footer & modal
    content = content.replace('UPI &bull; Cards &bull; Netbanking &bull; Wallets ↗', 'UPI 2.0 &bull; Decoy Honeypot &bull; Netbanking ↗')
    
    three_models_block = """                <div class="bg-blue-900/20 border border-blue-500/20 rounded-xl p-3 text-center">
                    <div class="text-blue-300 text-2xl font-bold font-mono">3</div>
                    <div class="text-slate-400 text-[10px] mt-1">Booster Models Active</div>
                </div>"""
    two_models_block = """                <div class="bg-blue-900/20 border border-blue-500/20 rounded-xl p-3 text-center">
                    <div class="text-blue-300 text-2xl font-bold font-mono">2</div>
                    <div class="text-slate-400 text-[10px] mt-1">Booster Models Active</div>
                </div>"""
    if three_models_block in content:
        content = content.replace(three_models_block, two_models_block)

    content = content.replace('Models: xgboost_fraud_model · xgboost_login_honeypot_model · xgboost_card_velocity_model &nbsp;|&nbsp; Runtime: native xgb.Booster + DMatrix',
                              'Models: xgboost_fraud_model · xgboost_login_honeypot_model &nbsp;|&nbsp; Runtime: native xgb.Booster + DMatrix')

    haversine_modal = """                <div class="flex items-center gap-3 bg-purple-900/20 border border-purple-500/20 rounded-xl px-4 py-3">
                    <i class="fa-solid fa-location-dot text-purple-400 w-5 text-center"></i>
                    <div><div class="text-white text-xs font-medium">Haversine Velocity Engine</div><div class="text-slate-400 text-[10px]">Flags physically impossible login velocity between geo-locations</div></div>
                    <span class="ml-auto text-emerald-400 text-[10px] font-mono bg-emerald-900/30 px-2 py-0.5 rounded-full">ACTIVE</span>
                </div>"""
    shannon_modal = """                <div class="flex items-center gap-3 bg-purple-900/20 border border-purple-500/20 rounded-xl px-4 py-3">
                    <i class="fa-solid fa-fingerprint text-purple-400 w-5 text-center"></i>
                    <div><div class="text-white text-xs font-medium">Shannon Behavioral Biometrics</div><div class="text-slate-400 text-[10px]">Flags robotic keystroke timing and zero-entropy mouse flight dynamics</div></div>
                    <span class="ml-auto text-emerald-400 text-[10px] font-mono bg-emerald-900/30 px-2 py-0.5 rounded-full">ACTIVE</span>
                </div>"""
    if haversine_modal in content:
        content = content.replace(haversine_modal, shannon_modal)

    # 6. JS cardMode and switchTab
    content = content.replace("let cardMode = 'normal';\n", "")
    content = content.replace("const vCards = document.getElementById('viewCards');\n", "")
    content = content.replace("const btnCards = document.getElementById('navCards');\n", "")
    content = content.replace("if (vCards) { vCards.style.display = 'none'; vCards.classList.add('hidden'); }\n", "")
    content = content.replace("if (btnCards) btnCards.className = 'tab-btn flex items-center gap-2';\n", "")

    cards_tab_block = """                } else if (tab === 'cards') {
                    if (vCards) { vCards.style.display = 'grid'; vCards.classList.remove('hidden'); }
                    if (btnCards) btnCards.className = 'tab-btn tab-btn-purple-active flex items-center gap-2';
                    if (subBanner) subBanner.innerHTML = 'Active Mode: Royal Purple Credit Card Portal &bull; Haversine Velocity Physics Defense';
                    if (subIcon) subIcon.className = 'fa-solid fa-circle-dot text-purple-400 text-xs';
                    if (brandLogo) brandLogo.className = 'w-8 h-8 rounded-lg bg-purple-600/25 border border-purple-500/40 flex items-center justify-center text-purple-300 text-sm transition';
                    if (userAvatar) userAvatar.className = 'w-7 h-7 rounded-full bg-purple-600/30 border border-purple-500/40 text-purple-200 flex items-center justify-center font-bold text-xs cursor-pointer';
                    if (body) body.className = 'min-h-screen flex flex-col justify-between purple-theme';
                    if (ambient) ambient.style.background = 'radial-gradient(circle at 50% -10%, rgba(124, 58, 237, 0.22) 0%, transparent 65%)';
                    window.location.hash = 'cards';
                    const cardScoreEl = document.getElementById('valCardScore');
                    const cVal = cardScoreEl ? parseInt(cardScoreEl.innerText) || 11 : 11;
                    drawArcGauge('canvasCardGauge', cVal, '#a855f7');"""
    if cards_tab_block in content:
        content = content.replace(cards_tab_block, "")

    # 7. Remove toggleCardNumberVisibility, toggleCardLock, setCardMode
    js_funcs_start = 'let isCardNumRevealed = false;'
    js_funcs_end = '// =====================================================================\n        // REALISTIC BANK LOGIN & DECOY DECEPTION FLOW'
    p1 = content.find(js_funcs_start)
    p2 = content.find(js_funcs_end)
    if p1 != -1 and p2 != -1:
        content = content[:p1] + content[p2:]
        print("Removed card helper JS functions in index.html")

    # 8. Remove payCardAction
    pca_start = '// INTEGRATED CREDIT CARD REAL-TIME VELOCITY & XGBOOST ML FLOW'
    pca_end = '// =====================================================================\n        // SOC SIMULATION TOGGLE'
    p1 = content.find(pca_start)
    p2 = content.find(pca_end)
    if p1 != -1 and p2 != -1:
        content = content[:p1] + content[p2:]
        print("Removed payCardAction JS in index.html")

    # 9. In window.onload:
    content = content.replace("drawArcGauge('canvasCardGauge', 11, '#a855f7');\n", "")
    card_route_block = """                } else if (hash === 'cards' || path.includes('/cards')) {
                    switchTab('cards');"""
    if card_route_block in content:
        content = content.replace(card_route_block, "")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("index.html successfully updated!")


def update_aegis_demo_html():
    path = os.path.join('templates', 'aegis_demo.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Nav button
    target_nav = """            <button id="navCards" onclick="switchTab('cards')" class="tab-btn flex items-center gap-2">
                <i class="fa-solid fa-credit-card text-xs"></i> Cards (Purple Theme)
            </button>\n"""
    if target_nav in content:
        content = content.replace(target_nav, "")

    # 2. Alert mentioning 3 XGBoost ML Models
    content = content.replace(
        "Running 3 XGBoost ML Models (Login Honeypot, Card Velocity, Unified Risk) with Haversine &amp; Levenshtein Engines",
        "Running 2 XGBoost ML Models (Login Honeypot, Unified UPI Risk) with Levenshtein Typo-Squatting Engine"
    )

    # 3. Card POS
    content = content.replace('Today &bull; Card POS', 'Today &bull; Merchant POS')

    # 4. viewCards panel
    start_vc = content.find('<div id="viewCards"')
    if start_vc != -1:
        end_vc_str = '<!-- GLOBAL FOOTER BAR -->'
        if end_vc_str not in content[start_vc:]:
            end_vc_str = '<!-- FOOTER -->'
        if end_vc_str not in content[start_vc:]:
            # find next major section or footer
            end_vc_str = '<footer'
        end_vc = content.find(end_vc_str, start_vc)
        assert end_vc != -1, 'End of viewCards not found in aegis_demo.html'
        vc_block = content[start_vc:end_vc]
        content = content[:start_vc] + content[end_vc:]
        print(f"Removed viewCards block of length {len(vc_block)} in aegis_demo.html")

    # 5. Footer mention
    content = content.replace('UPI &bull; Cards &bull; Netbanking &bull; Wallets', 'UPI 2.0 &bull; Decoy Honeypot &bull; Netbanking')

    # 6. JS in aegis_demo.html
    content = content.replace("let cardMode = 'normal';\n", "")
    content = content.replace("const vCards = document.getElementById('viewCards');\n", "")
    content = content.replace("const btnCards = document.getElementById('navCards');\n", "")
    content = content.replace("if (vCards) vCards.classList.add('hidden');\n", "")
    content = content.replace("if (btnCards) btnCards.className = 'tab-btn flex items-center gap-2';\n", "")

    cards_tab_block = """            } else if (tab === 'cards') {
                if (vCards) vCards.classList.remove('hidden');
                if (btnCards) btnCards.className = 'tab-btn tab-btn-purple-active flex items-center gap-2';
                if (subBanner) subBanner.innerHTML = 'Active Mode: Royal Purple Credit Card Portal &bull; Haversine Velocity Physics Defense';
                if (subIcon) subIcon.className = 'fa-solid fa-circle-dot text-purple-400 text-xs';
                if (brandLogo) brandLogo.className = 'w-8 h-8 rounded-lg bg-purple-600/25 border border-purple-500/40 flex items-center justify-center text-purple-300 text-sm transition';
                if (userAvatar) userAvatar.className = 'w-7 h-7 rounded-full bg-purple-600/30 border border-purple-500/40 text-purple-200 flex items-center justify-center font-bold text-xs cursor-pointer';
                if (body) body.className = 'min-h-screen flex flex-col justify-between purple-theme';
                if (ambient) ambient.style.background = 'radial-gradient(circle at 50% -10%, rgba(124, 58, 237, 0.22) 0%, transparent 65%)';
                window.location.hash = 'cards';
                const cardScoreEl = document.getElementById('valCardScore');
                const cVal = cardScoreEl ? parseInt(cardScoreEl.innerText) || 11 : 11;
                drawArcGauge('canvasCardGauge', cVal, '#a855f7');"""
    if cards_tab_block in content:
        content = content.replace(cards_tab_block, "")

    # 7. JS helpers
    js_funcs_start = 'let isCardNumRevealed = false;'
    js_funcs_end = '// =====================================================================\n    // REALISTIC BANK LOGIN & DECOY DECEPTION FLOW'
    p1 = content.find(js_funcs_start)
    p2 = content.find(js_funcs_end)
    if p1 != -1 and p2 != -1:
        content = content[:p1] + content[p2:]
        print("Removed card helper JS functions in aegis_demo.html")

    # 8. payCardAction
    pca_start = '// INTEGRATED CREDIT CARD REAL-TIME VELOCITY & XGBOOST ML FLOW'
    pca_end = '// =====================================================================\n    // SOC SIMULATION TOGGLE'
    p1 = content.find(pca_start)
    p2 = content.find(pca_end)
    if p1 != -1 and p2 != -1:
        content = content[:p1] + content[p2:]
        print("Removed payCardAction JS in aegis_demo.html")

    # 9. onload
    content = content.replace("drawArcGauge('canvasCardGauge', 11, '#a855f7');\n", "")
    card_route_block = """            } else if (hash === 'cards' || path.includes('/cards')) {
                switchTab('cards');"""
    if card_route_block in content:
        content = content.replace(card_route_block, "")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("aegis_demo.html successfully updated!")


def update_3d_architecture_html():
    path = os.path.join('templates', 'aegis_3d_architecture.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Title / Header labels
    content = content.replace('UPI 2.0 + CARDS + AUTH', 'UPI 2.0 + PASSIVE AUTH')
    content = content.replace('UPI + CARDS + AUTH', 'UPI + PASSIVE AUTH')
    content = content.replace("5. Card Cloned Travel Attack", "5. UPI Impersonation & Typo-Squatting")
    content = content.replace("V_in = [ V_login, V_upi, V_card ]", "V_in = [ V_login, V_upi, V_context ]")
    content = content.replace("['Web Auth Channel', 'UPI 2.0 Ingress', 'Credit Card Portal', 'Client Inbound Buffer']",
                              "['Web Auth Channel', 'UPI 2.0 Ingress', 'Dynamic QR Buffer', 'Client Inbound Buffer']")
    content = content.replace("XGBoost Model Suite (Login, Card Velocity, UPI Risk)",
                              "XGBoost Model Suite (Login Honeypot, Unified UPI Risk)")
    content = content.replace("Combines all signals from UPI, Cards, and Login and calculates a single risk score between 0% and 100%.",
                              "Combines all signals from UPI, Login Telemetry, and Biometrics and calculates a single risk score between 0% and 100%.")

    # 2. Node 6 definition: Replace Card Velocity with Levenshtein Typo Engine
    old_node6 = """      node6: {
        id: 'node6',
        stepPill: 'STEP 6 OF 10: VELOCITY PHYSICS',
        name: '6. SPEED CHECKER',
        shortName: '6. SPEED CHECK',
        domain: 'CARD FRAUD GUARD',
        subtitle: 'Impossible travel detection',
        summary: 'Detects if a card was used in two faraway locations too quickly to be humanly possible.',
        deepDetails: 'Haversine distance formula, automatic card freeze if speed exceeds 900 km/h in under 2ms.',
        color: 0xd946ef,
        hexColor: '#d946ef',
        pos: new THREE.Vector3(6, 0, -15), // Level Y=0 (NO LONGER HIGH IN AIR AT Y=14!)
        stat1: '< 2.0 ms',
        stat2: 'Great-Circle Arc',
        stat3: 'v > 900 km/h Cutoff',
        stat4: 'Instant Card Halt',
        tags: ['Haversine Formula', 'Great-Circle Distance', 'Speed Threshold v>900km/h', 'Card Velocity Guard', '< 2.0ms SLA'],
        mathTitle: 'HAVERSINE VELOCITY FORMULA',
        mathFormula: 'd = 2R · arcsin(√(sin²(Δφ/2) + cos φ₁ cos φ₂ sin²(Δλ/2)))',
        mathDesc: 'Physical velocity v = d / Δt. Detects cloned magnetic stripes and simultaneous distributed card testing.'
      },"""

    new_node6 = """      node6: {
        id: 'node6',
        stepPill: 'STEP 6 OF 10: TYPO-SQUATTING SCANNER',
        name: '6. LEVENSHTEIN FILTER',
        shortName: '6. VPA CHECK',
        domain: 'UPI VPA GUARD',
        subtitle: 'VPA typo-squatting detection',
        summary: 'Detects lookalike VPAs (e.g., ph0nepe@okaxis) impersonating verified merchant handles.',
        deepDetails: 'Wagner-Fischer dynamic programming matrix, trigram similarity scoring under 15ms.',
        color: 0xd946ef,
        hexColor: '#d946ef',
        pos: new THREE.Vector3(6, 0, -15), // Level Y=0
        stat1: '< 15 ms',
        stat2: 'Wagner-Fischer Matrix',
        stat3: 'Sim >= 0.75 Cutoff',
        stat4: 'Instant VPA Flag',
        tags: ['Levenshtein Distance', 'VPA Typo-Squatting', 'Collect Trap Detection', 'Sub-15ms Latency'],
        mathTitle: 'LEVENSHTEIN EDIT DISTANCE',
        mathFormula: 'D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1] + cost)',
        mathDesc: 'Minimum single-character edits required to transform raw sender/receiver handle into verified dictionary token.'
      },"""

    if old_node6 in content:
        content = content.replace(old_node6, new_node6)
        print("Replaced Node 6 in aegis_3d_architecture.html")
    else:
        print("WARNING: old_node6 exact match not found in aegis_3d_architecture.html, searching line by line")

    # 3. Path D in Node 8:
    content = content.replace("'Path D: Card Freeze'", "'Path D: Decoy Honeypot Tarpit'")

    # 4. Simulation scenario 5 log entries:
    content = content.replace(
        "[1. INBOUND] Credit Card payment initiated: Card ending in 4112 at Mumbai merchant",
        "[1. INBOUND] Collect request payment initiated: Target VPA 'paytm-refund@okaxis' for ₹4,999"
    )
    content = content.replace(
        "[6. SPEED CHECK] Haversine Engine: Last tx in London 12 mins ago -> v = 3,420 km/h (>900 km/h)",
        "[6. VPA CHECK] Levenshtein Engine: Similarity 0.94 against verified 'paytm' handle -> Typo-squatting alert"
    )
    content = content.replace(
        "[6. SPEED CHECK] Impossible travel speed detected -> Auto-freeze card at Core Banking layer",
        "[6. VPA CHECK] Impersonated brand handle confirmed -> Dispatch Tier 3 Upstream Gateway Rejection"
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("aegis_3d_architecture.html successfully updated!")


if __name__ == '__main__':
    update_index_html()
    update_aegis_demo_html()
    update_3d_architecture_html()
