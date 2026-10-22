function sendAction(action) {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || !tabs[0]) return;
    const tab = tabs[0];
    const box = document.getElementById('statusBox');

    // Method 1: Execute directly in the tab using chrome.scripting.executeScript (100% reliable)
    if (chrome.scripting && chrome.scripting.executeScript) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (act) => {
          console.log("[Aegis Popup Injector] Executing action:", act);
          window.dispatchEvent(new CustomEvent('aegis-bot-command', { detail: { command: act } }));

          if (act === 'full_attack') {
            window.aegisBotAutoRetry = true;
            if (typeof window.triggerFullBotWorkflow === 'function') {
              window.triggerFullBotWorkflow();
            } else if (typeof window.triggerBiometricsSim === 'function') {
              window.triggerBiometricsSim('bot');
            }
          } else if (act === 'wire_payment') {
            window.aegisBotAutoRetry = true;
            if (typeof window.triggerDecoyWireExfiltration === 'function') {
              window.triggerDecoyWireExfiltration();
            }
          } else if (act === 'upi_payment') {
            if (typeof window.triggerBotUpiPayment === 'function') {
              window.triggerBotUpiPayment();
            }
          } else if (act === 'linear_cursor') {
            if (typeof window.triggerBiometricsSim === 'function') {
              window.triggerBiometricsSim('bot');
            }
          } else if (act === 'reset_human') {
            window.aegisBotAutoRetry = false;
            if (window.aegisBotRetryTimeout) {
              clearTimeout(window.aegisBotRetryTimeout);
              window.aegisBotRetryTimeout = null;
            }
            if (typeof window.triggerBiometricsSim === 'function') {
              window.triggerBiometricsSim('human');
            }
          }
        },
        args: [action]
      }, () => {
        if (chrome.runtime.lastError) {
          console.warn("Scripting notice:", chrome.runtime.lastError.message);
        }
      });
    }

    // Method 2: Also send via message to content script
    chrome.tabs.sendMessage(tab.id, { action: action }, function(response) {
      if (chrome.runtime.lastError) {
        if (box) box.innerText = `🚨 Action sent to page! (${action})`;
      } else if (response && response.status) {
        if (box) box.innerText = response.status;
      }
    });

    // Instant status feedback
    if (box) {
      if (action === 'full_attack') box.innerText = "🚨 Full Bot Attack Executed!";
      else if (action === 'wire_payment') box.innerText = "💸 Wire Exfiltration Sent!";
      else if (action === 'upi_payment') box.innerText = "⚡ UPI Scam Initiated!";
      else if (action === 'linear_cursor') box.innerText = "🤖 Linear Vector Locked (H=0.08)!";
      else if (action === 'reset_human') box.innerText = "🛡️ Reset to Genuine Human!";
    }
  });
}

// Manage Autonomous Auto-Bot Toggle
const toggle = document.getElementById('toggleAutoAttack');
if (toggle) {
  // Load saved state
  if (chrome.storage && chrome.storage.local) {
    chrome.storage.local.get(['aegisAutoAttack'], function(result) {
      toggle.checked = Boolean(result.aegisAutoAttack);
    });
  }

  toggle.addEventListener('change', function() {
    const isAuto = toggle.checked;
    if (chrome.storage && chrome.storage.local) {
      chrome.storage.local.set({ aegisAutoAttack: isAuto });
    }

    // Update active tab setting
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      if (!tabs || !tabs[0]) return;
      const tab = tabs[0];

      if (chrome.scripting && chrome.scripting.executeScript) {
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (enabled) => {
            localStorage.setItem('aegis_auto_attack', enabled ? '1' : '0');
            console.log(`[Aegis Extension] Autonomous Bot Mode: ${enabled ? 'ENABLED' : 'DISABLED'}`);
          },
          args: [isAuto]
        });
      }

      const box = document.getElementById('statusBox');
      if (box) {
        box.innerText = isAuto ? "⚡ Autonomous Bot Mode: ON (Attacks on load)" : "🛡️ Autonomous Bot Mode: OFF (Manual only)";
      }
    });
  });
}

// Button Bindings
document.getElementById('btnFullAttack').addEventListener('click', function() {
  sendAction('full_attack');
});

document.getElementById('btnWirePayment').addEventListener('click', function() {
  sendAction('wire_payment');
});

document.getElementById('btnUpiPayment').addEventListener('click', function() {
  sendAction('upi_payment');
});

document.getElementById('btnLinearCursor').addEventListener('click', function() {
  sendAction('linear_cursor');
});

document.getElementById('btnResetHuman').addEventListener('click', function() {
  sendAction('reset_human');
});
