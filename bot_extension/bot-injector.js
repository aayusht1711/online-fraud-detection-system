// Project Aegis - Content Script Bot Injector
console.log("[Aegis Bot Injector] Extension hooked into page:", window.location.href);

// Helper: Run JavaScript directly inside the page's MAIN world context
function runInMainWorld(codeStr) {
  try {
    const script = document.createElement('script');
    script.textContent = `(function() { try { ${codeStr} } catch(e) { console.error("[Aegis Bot Injector Error]", e); } })();`;
    (document.head || document.documentElement).appendChild(script);
    script.remove();
  } catch (err) {
    console.error("[Aegis Bot Injector Injection Error]:", err);
  }
}

// Listen for commands from extension popup
if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log("[Aegis Bot Injector] Received action:", request.action);

    // 1. Dispatch custom DOM event to page
    window.dispatchEvent(new CustomEvent('aegis-bot-command', { detail: { command: request.action } }));

    if (request.action === 'full_attack') {
      executeFullBotAttack();
      sendResponse({ status: "🚨 Full Bot Attack Executed (Tarpit + Wire Exfiltration)!" });
    } else if (request.action === 'wire_payment') {
      executeWireExfiltration();
      sendResponse({ status: "💸 Bot Wire Exfiltration Sent (Intercepted by NPCI Switch Trap)!" });
    } else if (request.action === 'upi_payment') {
      executeUpiPaymentAttack();
      sendResponse({ status: "⚡ Bot UPI Scam Payment Initiated (Pre-PIN Screen Active)!" });
    } else if (request.action === 'linear_cursor') {
      injectLinearCursor();
      sendResponse({ status: "🤖 Linear Cursor Injected & Locked (H=0.08)!" });
    } else if (request.action === 'reset_human') {
      resetToHuman();
      sendResponse({ status: "🛡️ Reset to Genuine Human (Live 60Hz Sensor Active)!" });
    }
    return true;
  });
}

// 1. Full Attack Flow: Lock Red Gauges -> Tarpit Login -> Decoy Sandbox -> Wire Transfer Payment
function executeFullBotAttack() {
  console.log("[Aegis Bot Injector] Executing full automated attack sequence...");

  // Run in main world: simulate bot attack immediately
  runInMainWorld(`
    window.aegisBotAutoRetry = true;
    if (window.aegisSensor) window.aegisSensor.simulateBotAttack();
    if (typeof window.triggerBiometricsSim === 'function') window.triggerBiometricsSim('bot');
  `);

  // Fill credentials directly
  injectCredentialsInstant();

  // Generate robotic straight-line pointer movements
  injectLinearCursor();

  // Step 1: Click "Login to Account"
  setTimeout(() => {
    const btn = document.getElementById('btnLogin');
    if (btn && !btn.disabled) {
      console.log("[Aegis Bot Injector] Bot clicking Login to Account...");
      btn.click();
    }
  }, 400);

  // Step 2: Auto execute Wire Payment inside sandbox after 3,600ms (after PoW tarpit completes)
  setTimeout(() => {
    console.log("[Aegis Bot Injector] Bot initiating automated Wire Exfiltration...");
    executeWireExfiltration();
  }, 3600);
}

// 2. Automated Wire Exfiltration Payment in Honeypot Sandbox
function executeWireExfiltration() {
  console.log("[Aegis Bot Injector] Executing wire exfiltration payment...");

  // Execute in main page world where all state and functions live
  runInMainWorld(`
    window.aegisBotAutoRetry = true;
    if (typeof window.triggerDecoyWireExfiltration === 'function') {
      window.triggerDecoyWireExfiltration();
    } else {
      const sm = document.getElementById('snowMountainPanel');
      const fern = document.getElementById('fernPostLoginPanel');
      if (sm) { sm.style.display = 'none'; sm.classList.add('hidden'); }
      if (fern) { fern.style.display = 'flex'; fern.classList.remove('hidden'); }

      const transferBox = document.getElementById('portalTransferBox');
      if (transferBox) {
        transferBox.style.display = 'block';
        transferBox.classList.remove('hidden');
        transferBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      const target = document.getElementById('decoyTargetAcc');
      const amt = document.getElementById('decoyAmt');
      if (target) target.value = 'mule_sweep01@okaxis';
      if (amt) amt.value = '75,000.00';

      if (typeof appendLogTerminal === 'function') {
        appendLogTerminal('BOT SCRIPT EXFILTRATION: Initiating wire payment of ₹ 75,000 to mule_sweep01@okaxis...');
      }

      setTimeout(() => {
        if (typeof execDecoyTransfer === 'function') {
          execDecoyTransfer();
        } else {
          const btnSend = document.getElementById('btnDecoySend');
          if (btnSend) btnSend.click();
        }
      }, 300);
    }
  `);
}

// 3. Automated UPI Scam Payment Attempt
function executeUpiPaymentAttack() {
  console.log("[Aegis Bot Injector] Targeting UPI Instant Pay gateway with scam VPA...");

  runInMainWorld(`
    if (typeof window.triggerBotUpiPayment === 'function') {
      window.triggerBotUpiPayment();
    } else {
      if (typeof switchTab === 'function') switchTab('upi');
      if (typeof setUpiProfile === 'function') setUpiProfile('coercion');

      const vpaInput = document.getElementById('inputUpiTargetVPA');
      const amtInput = document.getElementById('inputUpiVal');
      if (vpaInput) {
        vpaInput.value = 'ph0nepe@okaxis';
        vpaInput.dispatchEvent(new Event('input', { bubbles: true }));
        vpaInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      if (amtInput) {
        amtInput.value = '48,000';
        amtInput.dispatchEvent(new Event('input', { bubbles: true }));
      }

      setTimeout(() => {
        const btnPay = document.getElementById('btnInitUpiPay');
        if (btnPay) btnPay.click();
      }, 400);
    }
  `);
}

// 4. Synthetic Linear Cursor Movement (Shannon Entropy H < 0.10)
function injectLinearCursor() {
  runInMainWorld(`
    if (window.aegisSensor) window.aegisSensor.simulateBotAttack();
    if (typeof window.triggerBiometricsSim === 'function') window.triggerBiometricsSim('bot');
  `);

  const steps = 48;
  const startX = 60;
  const endX = 700;
  const y = 240; // perfectly constant Y = zero vertical variation

  for (let i = 0; i < steps; i++) {
    const x = startX + (i * ((endX - startX) / steps));
    const event = new PointerEvent('pointermove', {
      clientX: x,
      clientY: y,
      bubbles: true,
      cancelable: true,
      pointerType: 'mouse'
    });
    window.dispatchEvent(event);
  }
}

// 5. Instant Credential Stuffing (0ms Flight Time)
function injectCredentialsInstant() {
  const emailInput = document.getElementById('inputEmail') || document.getElementById('inputUser');
  const passInput = document.getElementById('inputPass');

  if (emailInput) {
    emailInput.value = 'admin_bot@crawler.net';
    emailInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
  if (passInput) {
    passInput.value = 'ScriptPayload#99';
    passInput.dispatchEvent(new Event('input', { bubbles: true }));
  }

  const keyEvent = new KeyboardEvent('keydown', { key: '9', bubbles: true });
  window.dispatchEvent(keyEvent);
}

// 6. Reset to Human
function resetToHuman() {
  runInMainWorld(`
    window.aegisBotAutoRetry = false;
    if (window.aegisBotRetryTimeout) {
      clearTimeout(window.aegisBotRetryTimeout);
      window.aegisBotRetryTimeout = null;
    }
    if (window.aegisSensor) window.aegisSensor.resetLiveSensor();
    if (typeof window.triggerBiometricsSim === 'function') window.triggerBiometricsSim('human');
  `);

  const emailInput = document.getElementById('inputEmail') || document.getElementById('inputUser');
  const passInput = document.getElementById('inputPass');
  if (emailInput) {
    emailInput.value = 'alex.morgan@fintech.io';
    emailInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
  if (passInput) {
    passInput.value = '';
    passInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
}

// Expose on window for easy DevTools invocation too!
window.aegisBotAttacker = {
  attack: executeFullBotAttack,
  payWire: executeWireExfiltration,
  payUpi: executeUpiPaymentAttack,
  linearMove: injectLinearCursor,
  injectCreds: injectCredentialsInstant,
  reset: resetToHuman
};

// Check if Autonomous Auto-Bot Mode is active
function checkAndRunAutoBot() {
  const localFlag = localStorage.getItem('aegis_auto_attack') === '1';
  if (localFlag) {
    console.log("⚡ [Aegis Bot Injector] Autonomous Bot Mode is ENABLED. Launching attack in 1.2s...");
    setTimeout(executeFullBotAttack, 1200);
    return;
  }

  if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
    chrome.storage.local.get(['aegisAutoAttack'], function(res) {
      if (res && res.aegisAutoAttack) {
        console.log("⚡ [Aegis Bot Injector] Autonomous Bot Mode is ENABLED (storage). Launching attack in 1.2s...");
        setTimeout(executeFullBotAttack, 1200);
      }
    });
  }
}

if (document.readyState === 'complete') {
  checkAndRunAutoBot();
} else {
  window.addEventListener('load', checkAndRunAutoBot);
}
