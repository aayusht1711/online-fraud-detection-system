// ==UserScript==
// @name         Project Aegis - Automated Bot Attack Suite
// @namespace    http://tampermonkey.net/
// @version      2.1
// @description  Automated Selenium/Puppeteer style bot attack simulator for Project Aegis
// @author       Aegis Security Team
// @match        http://127.0.0.1:5000/*
// @match        http://localhost:5000/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.left = '20px';
    container.style.zIndex = '999999';
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.gap = '8px';
    container.style.fontFamily = 'monospace';

    // Button 1: Full Attack (Login + Wire Exfiltration Payment)
    const btnAttack = document.createElement('button');
    btnAttack.innerHTML = '🚨 BOT ATTACK (LOGIN + WIRE PAY)';
    btnAttack.style.padding = '9px 14px';
    btnAttack.style.background = '#e11d48';
    btnAttack.style.color = '#ffffff';
    btnAttack.style.border = '2px solid #fda4af';
    btnAttack.style.borderRadius = '9999px';
    btnAttack.style.fontSize = '11px';
    btnAttack.style.fontWeight = 'bold';
    btnAttack.style.boxShadow = '0 8px 20px rgba(225, 29, 72, 0.4)';
    btnAttack.style.cursor = 'pointer';

    btnAttack.onclick = function() {
        console.log("🚨 [Tampermonkey Bot] Triggering Full Headless Attack Vector...");
        window.aegisBotAutoRetry = true;

        if (window.aegisSensor) {
            window.aegisSensor.simulateBotAttack();
        }

        // Linear cursor sweep
        for (let i = 0; i < 48; i++) {
            window.dispatchEvent(new PointerEvent('pointermove', { clientX: 50 + (i * 15), clientY: 200, bubbles: true }));
        }

        // Credentials
        const email = document.getElementById('inputEmail') || document.getElementById('inputUser');
        const pass = document.getElementById('inputPass');
        if (email) email.value = 'admin_bot@crawler.net';
        if (pass) pass.value = 'ScriptPayload#99';

        // Auto Login
        setTimeout(() => {
            const loginBtn = document.getElementById('btnLogin');
            if (loginBtn) loginBtn.click();
        }, 500);

        // Auto Wire Payment
        setTimeout(() => {
            window.aegisBotAutoRetry = true;
            if (typeof window.triggerDecoyWireExfiltration === 'function') {
                window.triggerDecoyWireExfiltration();
            } else if (typeof window.execDecoyTransfer === 'function') {
                window.execDecoyTransfer();
            }
        }, 3600);
    };

    // Button 2: Wire Pay Only
    const btnPay = document.createElement('button');
    btnPay.innerHTML = '💸 BOT WIRE PAY (₹75k MULE)';
    btnPay.style.padding = '8px 12px';
    btnPay.style.background = '#d97706';
    btnPay.style.color = '#ffffff';
    btnPay.style.border = '1px solid #fde68a';
    btnPay.style.borderRadius = '9999px';
    btnPay.style.fontSize = '10px';
    btnPay.style.fontWeight = 'bold';
    btnPay.style.cursor = 'pointer';

    btnPay.onclick = function() {
        window.aegisBotAutoRetry = true;
        if (typeof window.triggerDecoyWireExfiltration === 'function') {
            window.triggerDecoyWireExfiltration();
        } else {
            const transferBox = document.getElementById('portalTransferBox');
            if (transferBox) {
                transferBox.style.display = 'block';
                transferBox.classList.remove('hidden');
                transferBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            if (typeof window.execDecoyTransfer === 'function') {
                window.execDecoyTransfer();
            }
        }
    };

    container.appendChild(btnAttack);
    container.appendChild(btnPay);
    document.body.appendChild(container);
})();
