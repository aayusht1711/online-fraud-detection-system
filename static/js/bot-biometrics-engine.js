/**
 * Project Aegis - Live Client-Side Bot Detection Engine
 * Computes Shannon directional entropy, cursor jump vectors, and keystroke flight latency in real time.
 */

class AegisBiometricsSensor {
  constructor() {
    this.mouseBuffer = [];
    this.bufferSize = 64;
    this.keyPressTimes = {};
    this.lastKeyUpTime = null;
    this.flightTimes = [];
    this.dwellHistory = [85, 92, 110, 78, 95];
    this.rapidInjectionStreak = 0;
    this.isBotSimActive = false;
    this.botSimTimeout = null;

    this.currentEntropy = 3.18;
    this.currentSpeed = 0;
    this.currentDwell = 88;
    this.currentWpm = 0;
    this.wavePhase = 0;

    this.initCanvasContexts();
    this.initListeners();
    this.initCustomCommandListener();
    this.startOscilloscopeLoop();
  }

  initCanvasContexts() {
    this.cvKey = document.getElementById('canvasKeyDynamics');
    this.cvMouse = document.getElementById('canvasMouseTrajectory');
    this.cvCursor = document.getElementById('canvasCursorEntropy');
    this.rhythmBars = document.getElementById('typingRhythmBars');

    this.ctxKey = this.cvKey ? this.cvKey.getContext('2d') : null;
    this.ctxMouse = this.cvMouse ? this.cvMouse.getContext('2d') : null;
    this.ctxCursor = this.cvCursor ? this.cvCursor.getContext('2d') : null;
  }

  initListeners() {
    // 1. Mouse Movement & Directional Entropy Listener (60 Hz Non-blocking)
    const onMove = (e) => {
      // STRICT LOCK: Hardware movements can NEVER overwrite active bot detection
      if (this.isBotSimActive) return;

      const now = performance.now();
      const pt = { x: e.clientX, y: e.clientY, t: now };

      // Teleport step jump detection (> 400px per tick)
      if (this.mouseBuffer.length > 0) {
        const last = this.mouseBuffer[this.mouseBuffer.length - 1];
        const dist = Math.hypot(pt.x - last.x, pt.y - last.y);
        const dt = Math.max(0.001, (now - last.t) / 1000);
        this.currentSpeed = dist / dt;

        if (dist > 400 && dt < 0.05) {
          this.flagTeleportJump(dist);
        }
      }

      this.mouseBuffer.push(pt);
      if (this.mouseBuffer.length > this.bufferSize) {
        this.mouseBuffer.shift();
      }

      if (this.mouseBuffer.length >= 16) {
        this.currentEntropy = this.calculatePathEntropy();
        this.updateMouseUI(this.currentEntropy);
      }
    };

    window.addEventListener('pointermove', onMove, { passive: true });
    window.addEventListener('mousemove', onMove, { passive: true });

    // 2. Keystroke Dynamics Listeners (Dwell Time & Flight Time)
    window.addEventListener('keydown', (e) => {
      if (this.isBotSimActive) return;

      const now = performance.now();
      const code = e.code || e.key;
      if (!this.keyPressTimes[code]) {
        this.keyPressTimes[code] = now;
      }

      if (this.lastKeyUpTime !== null) {
        const flightTime = now - this.lastKeyUpTime;
        this.flightTimes.push(flightTime);
        if (this.flightTimes.length > 16) this.flightTimes.shift();

        if (flightTime < 1500) {
          this.currentWpm = Math.min(180, Math.round(60000 / (Math.max(60, flightTime) * 5)));
        }

        this.evaluateTypingCadence(flightTime);
      }
      this.pulseEqualizerBars();
    }, { passive: true });

    window.addEventListener('keyup', (e) => {
      if (this.isBotSimActive) return;

      const now = performance.now();
      const code = e.code || e.key;

      if (this.keyPressTimes[code]) {
        const dwellTime = Math.round(now - this.keyPressTimes[code]);
        this.currentDwell = dwellTime;
        this.dwellHistory.push(dwellTime);
        if (this.dwellHistory.length > 20) this.dwellHistory.shift();
        delete this.keyPressTimes[code];
      }

      this.lastKeyUpTime = now;
      this.updateBiometricsBadges();
    }, { passive: true });
  }

  initCustomCommandListener() {
    window.addEventListener('aegis-bot-command', (e) => {
      const cmd = e.detail && e.detail.command;
      if (cmd === 'attack' || cmd === 'full_attack') {
        this.simulateBotAttack();
        if (typeof window.triggerFullBotWorkflow === 'function') {
          window.triggerFullBotWorkflow();
        }
      } else if (cmd === 'wire_payment') {
        this.simulateBotAttack();
        if (typeof window.triggerDecoyWireExfiltration === 'function') {
          window.triggerDecoyWireExfiltration();
        }
      } else if (cmd === 'upi_payment') {
        if (typeof window.triggerBotUpiPayment === 'function') {
          window.triggerBotUpiPayment();
        }
      } else if (cmd === 'linear_cursor') {
        this.simulateBotAttack();
      } else if (cmd === 'reset_human') {
        this.resetLiveSensor();
      }
    });
  }

  // Calculate Shannon directional entropy across 8 compass octants:
  // H(D) = -SUM(p(k) * log2(p(k)))
  calculatePathEntropy() {
    const octants = new Array(8).fill(0);
    let totalVectors = 0;

    for (let i = 1; i < this.mouseBuffer.length; i++) {
      const dx = this.mouseBuffer[i].x - this.mouseBuffer[i - 1].x;
      const dy = this.mouseBuffer[i].y - this.mouseBuffer[i - 1].y;

      if (Math.hypot(dx, dy) < 2) continue;

      let angle = Math.atan2(dy, dx); // Range -PI to +PI
      if (angle < 0) angle += 2 * Math.PI;

      const octantIndex = Math.min(Math.floor((angle / (2 * Math.PI)) * 8), 7);
      octants[octantIndex]++;
      totalVectors++;
    }

    if (totalVectors < 8) return 2.85; // Human baseline default

    let entropy = 0.0;
    for (let count of octants) {
      if (count > 0) {
        const p = count / totalVectors;
        entropy -= p * Math.log2(p);
      }
    }
    return parseFloat(Math.min(5.0, Math.max(0.05, entropy)).toFixed(2));
  }

  evaluateTypingCadence(flightTime) {
    if (this.isBotSimActive) return;
    // Flight time <= 2.5ms indicates automated clipboard/script injection
    if (flightTime <= 2.5) {
      this.rapidInjectionStreak++;
    } else {
      this.rapidInjectionStreak = Math.max(0, this.rapidInjectionStreak - 1);
    }

    const isInjection = this.rapidInjectionStreak >= 3 || flightTime < 1.0;
    this.updateKeystrokeUI(flightTime, isInjection);
  }

  flagTeleportJump(dist) {
    if (this.isBotSimActive) return;
    if (typeof appendLogTerminal === 'function') {
      appendLogTerminal(`REMOTE DESKTOP TELEPORT DETECTED: Step jump of ${Math.round(dist)}px. Flagged AnyDesk/TeamViewer lag.`);
    }
    const detMouse = document.getElementById('detMouseBadge');
    if (detMouse) {
      detMouse.innerText = 'ALERT (Teleport)';
      detMouse.className = 'px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono text-[9px] font-bold';
    }
  }

  updateMouseUI(entropy) {
    if (this.isBotSimActive) return;

    // Support data attributes and direct element IDs
    const entropyDataBadge = document.querySelector('[data-metric="cursor-entropy"]');
    const mouseDataBadge = document.querySelector('[data-status="mouse-movement"]');
    const badgeCursor = document.getElementById('badgeCursor');
    const badgeMouse = document.getElementById('badgeMouse');
    const detMouse = document.getElementById('detMouseBadge');

    const entropyText = `H: ${entropy.toFixed(2)}`;
    if (entropyDataBadge) entropyDataBadge.innerText = entropyText;
    if (badgeCursor) {
      badgeCursor.innerText = entropyText;
      badgeCursor.className = entropy < 0.80
        ? 'text-rose-400 font-bold bg-rose-500/10 px-1.5 py-0.2 rounded border border-rose-500/30 text-[8px] animate-pulse'
        : 'text-cyan-400 font-medium bg-cyan-500/10 px-1.5 py-0.2 rounded border border-cyan-500/20 text-[8px]';
    }

    // Human baseline 2.4 - 3.8, Bot < 0.80
    const isBot = entropy < 0.80;
    if (mouseDataBadge) {
      mouseDataBadge.innerText = isBot ? 'BOT (Linear)' : 'Safe';
      mouseDataBadge.className = isBot ? 'text-xs font-bold text-red-500 animate-pulse' : 'text-xs text-emerald-400';
    }

    if (badgeMouse) {
      if (isBot) {
        badgeMouse.innerText = 'LINEAR VECTOR';
        badgeMouse.className = 'text-rose-400 font-bold bg-rose-500/10 px-1.5 py-0.2 rounded border border-rose-500/30 text-[8px] animate-pulse';
      } else {
        badgeMouse.innerText = this.currentSpeed > 2500 ? 'High Speed' : (this.currentSpeed > 50 ? 'Human Active' : 'Resting');
        badgeMouse.className = this.currentSpeed > 2500
          ? 'text-amber-400 font-medium bg-amber-500/10 px-1.5 py-0.2 rounded border border-amber-500/20 text-[8px]'
          : 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
      }
    }

    if (detMouse) {
      if (isBot) {
        detMouse.innerText = 'FLAGGED: BOT';
        detMouse.className = 'px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono text-[9px] font-bold';
      } else {
        detMouse.innerText = 'Safe';
        detMouse.className = 'px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono text-[9px]';
      }
    }
  }

  updateKeystrokeUI(flightTime, isInjection) {
    if (this.isBotSimActive) return;

    const keyDataBadge = document.querySelector('[data-status="keystroke-dynamics"]');
    const badgeKey = document.getElementById('badgeKey');
    const badgeTyping = document.getElementById('badgeTyping');
    const detKey = document.getElementById('detKeyBadge');

    if (keyDataBadge) {
      keyDataBadge.innerText = isInjection ? 'BOT (Injected)' : 'Safe';
      keyDataBadge.className = isInjection ? 'text-xs font-bold text-red-500 animate-pulse' : 'text-xs text-emerald-400';
    }

    if (badgeKey) {
      if (isInjection) {
        badgeKey.innerText = 'BOT INJECTION (0ms)';
        badgeKey.className = 'text-rose-400 font-bold bg-rose-500/10 px-1.5 py-0.2 rounded border border-rose-500/30 text-[8px] animate-pulse';
      } else {
        badgeKey.innerText = `${this.currentDwell}ms • Normal`;
        badgeKey.className = 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
      }
    }

    if (badgeTyping) {
      badgeTyping.innerText = isInjection ? 'AUTOMATED' : (this.currentWpm > 0 ? `${this.currentWpm} WPM` : 'Organic');
      badgeTyping.className = isInjection
        ? 'text-rose-400 font-bold bg-rose-500/10 px-1.5 py-0.2 rounded border border-rose-500/30 text-[8px] animate-pulse'
        : 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
    }

    if (detKey) {
      if (isInjection) {
        detKey.innerText = 'FLAGGED: BOT';
        detKey.className = 'px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono text-[9px] font-bold';
      } else {
        detKey.innerText = 'Safe';
        detKey.className = 'px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono text-[9px]';
      }
    }
  }

  updateBiometricsBadges() {
    if (this.isBotSimActive) return;
    this.updateMouseUI(this.currentEntropy);
    this.updateKeystrokeUI(this.flightTimes[this.flightTimes.length - 1] || 120, false);
  }

  pulseEqualizerBars() {
    if (!this.rhythmBars) return;
    const bars = this.rhythmBars.children;
    for (let i = 0; i < bars.length; i++) {
      const h = Math.floor(Math.random() * 18) + 8;
      bars[i].style.height = `${h}px`;
    }
  }

  // Triggered by the "Bot Sim" button
  simulateBotAttack() {
    this.isBotSimActive = true;
    clearTimeout(this.botSimTimeout);
    this.botSimTimeout = null;

    this.mouseBuffer = [];

    // a) Cursor Telemetry: Inject a perfectly straight linear coordinate vector with entropy H = 0.08
    for (let i = 0; i < 48; i++) {
      this.mouseBuffer.push({ x: 50 + i * 18, y: 150, t: performance.now() + i * 8 });
    }

    this.currentEntropy = 0.08;
    this.currentSpeed = 9800;
    this.currentDwell = 0;
    this.currentWpm = 450;

    // b) Credential Telemetry: Inject credentials with 0ms flight time (simulated clipboard/script injection)
    const userInput = document.getElementById('inputEmail') || document.getElementById('inputUser');
    const passInput = document.getElementById('inputPass');
    if (userInput) {
      userInput.value = 'admin_bot@crawler.net';
      userInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
    if (passInput) {
      passInput.value = 'ScriptPayload#99';
      passInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // c) Instantly trigger SOC Console "Bot Detected" visual states
    const bKey = document.getElementById('badgeKey');
    const bMouse = document.getElementById('badgeMouse');
    const bTyping = document.getElementById('badgeTyping');
    const bCursor = document.getElementById('badgeCursor');
    const detKey = document.getElementById('detKeyBadge');
    const detMouse = document.getElementById('detMouseBadge');
    const systemState = document.querySelector('[data-metric="system-state"]');
    const stateTitle = document.getElementById('stateTitleText');
    const stateSub = document.getElementById('stateSubText');
    const stateIcon = document.getElementById('stateIconBox');
    const riskVal = document.getElementById('socValRisk');
    const riskBadge = document.getElementById('socBadgeRisk');
    const entropyDataBadge = document.querySelector('[data-metric="cursor-entropy"]');
    const mouseDataBadge = document.querySelector('[data-status="mouse-movement"]');
    const keyDataBadge = document.querySelector('[data-status="keystroke-dynamics"]');

    // Keystroke Dynamics Widget: Highlight "0ms Flight Time" & "FLAGGED: SCRIPT INJECTION" [red]
    if (bKey) { 
      bKey.innerText = '0ms Flight Time'; 
      bKey.className = 'text-rose-400 font-bold bg-rose-500/15 px-1.5 py-0.2 rounded border border-rose-500/40 text-[8px] animate-pulse'; 
    }
    if (keyDataBadge) {
      keyDataBadge.innerText = 'BOT (Injected)';
      keyDataBadge.className = 'text-xs font-bold text-rose-500 animate-pulse';
    }
    if (detKey) { 
      detKey.innerText = 'FLAGGED: SCRIPT INJECTION'; 
      detKey.className = 'px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 font-mono text-[9px] font-bold animate-pulse'; 
    }

    // Mouse Trajectory Widget: Render rigid flat straight line & "BOT (Linear Vector)" [red]
    if (bMouse) { 
      bMouse.innerText = 'BOT (Linear Vector)'; 
      bMouse.className = 'text-rose-400 font-bold bg-rose-500/15 px-1.5 py-0.2 rounded border border-rose-500/40 text-[8px] animate-pulse'; 
    }
    if (mouseDataBadge) {
      mouseDataBadge.innerText = 'BOT (Linear)';
      mouseDataBadge.className = 'text-xs font-bold text-rose-500 animate-pulse';
    }
    if (detMouse) { 
      detMouse.innerText = 'FLAGGED: BOT'; 
      detMouse.className = 'px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 font-mono text-[9px] font-bold animate-pulse'; 
    }

    // Cursor Movement Metric: Update entropy display to "H: 0.08" [red]
    if (bCursor) { 
      bCursor.innerText = 'H: 0.08'; 
      bCursor.className = 'text-rose-400 font-bold bg-rose-500/15 px-1.5 py-0.2 rounded border border-rose-500/40 text-[8px] animate-pulse'; 
    }
    if (entropyDataBadge) entropyDataBadge.innerText = 'H: 0.08';

    if (bTyping) { 
      bTyping.innerText = 'CLIPBOARD INJECTION'; 
      bTyping.className = 'text-rose-400 font-bold bg-rose-500/15 px-1.5 py-0.2 rounded border border-rose-500/40 text-[8px] animate-pulse'; 
    }

    // System State: Flip status badge to "HONEYPOT TARPIT ENGAGED" in bold flashing red
    if (systemState) {
      systemState.innerText = 'HONEYPOT TARPIT ENGAGED';
      systemState.className = 'text-sm font-bold font-mono text-rose-400 animate-pulse tracking-wider';
    }
    if (stateTitle) {
      stateTitle.innerText = 'HONEYPOT TARPIT ENGAGED';
      stateTitle.className = 'text-sm font-bold text-rose-400 tracking-wider animate-pulse';
    }
    if (stateSub) {
      stateSub.innerText = 'Deception Tarpit Active (Bot Trapped)';
    }
    if (stateIcon) {
      stateIcon.className = 'w-8 h-8 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-400 flex items-center justify-center text-sm mx-auto mb-1.5 animate-pulse';
      stateIcon.innerHTML = '<i class="fa-solid fa-robot"></i>';
    }

    // XGBoost Risk Score: Animate circular gauge up to 96% in pulsing red
    if (riskVal) {
      riskVal.innerText = '96%';
      riskVal.className = 'text-2xl font-bold text-rose-400 font-mono animate-pulse';
    }
    if (riskBadge) {
      riskBadge.innerText = 'HIGH RISK (AUTOMATED BOT SCRIPT)';
      riskBadge.className = 'text-[10px] font-bold block uppercase text-rose-400 tracking-wider';
    }
    if (typeof drawArcGauge === 'function') {
      drawArcGauge('canvasRiskGauge', 96, '#f43f5e');
    }

    if (this.rhythmBars) {
      const bars = this.rhythmBars.children;
      for (let b of bars) {
        b.style.height = '24px';
        b.className = 'bg-rose-500 w-2 h-6 rounded-t';
      }
    }

    // Live Event Log: Prepend real-time event
    if (typeof appendLogTerminal === 'function') {
      appendLogTerminal('🚨 BOT DETECTED: Linear vector (H: 0.08) + 0ms injection -> Sandboxed in Honeypot Tarpit');
    }

    // LATCH: The bot detected state is 100% persistent. No automatic timeout.
    // It remains in red until user explicitly clicks "Live Sensor".
  }

  // Triggered by the "Live Sensor" button
  resetLiveSensor() {
    this.isBotSimActive = false;
    clearTimeout(this.botSimTimeout);
    this.botSimTimeout = null;
    this.mouseBuffer = [];
    this.currentEntropy = 3.24;
    this.currentSpeed = 120;
    this.currentDwell = 86;
    this.currentWpm = 0;

    const userInput = document.getElementById('inputEmail') || document.getElementById('inputUser');
    const passInput = document.getElementById('inputPass');
    if (userInput && userInput.value === 'admin_bot@crawler.net') {
      userInput.value = 'alex.morgan@fintech.io';
      userInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
    if (passInput && passInput.value === 'ScriptPayload#99') {
      passInput.value = '';
      passInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    const systemState = document.querySelector('[data-metric="system-state"]');
    const stateTitle = document.getElementById('stateTitleText');
    const stateSub = document.getElementById('stateSubText');
    const stateIcon = document.getElementById('stateIconBox');
    const riskVal = document.getElementById('socValRisk');
    const riskBadge = document.getElementById('socBadgeRisk');
    const detKey = document.getElementById('detKeyBadge');
    const detMouse = document.getElementById('detMouseBadge');
    const bKey = document.getElementById('badgeKey');
    const bMouse = document.getElementById('badgeMouse');
    const bTyping = document.getElementById('badgeTyping');
    const bCursor = document.getElementById('badgeCursor');
    const entropyDataBadge = document.querySelector('[data-metric="cursor-entropy"]');
    const mouseDataBadge = document.querySelector('[data-status="mouse-movement"]');
    const keyDataBadge = document.querySelector('[data-status="keystroke-dynamics"]');

    if (systemState) {
      systemState.innerText = 'NORMAL';
      systemState.className = 'text-xl font-bold font-mono text-blue-400';
    }
    if (stateTitle) {
      stateTitle.innerText = 'NORMAL';
      stateTitle.className = 'text-sm font-bold text-blue-400 tracking-wider';
    }
    if (stateSub) {
      stateSub.innerText = 'Legitimate User Behavior';
    }
    if (stateIcon) {
      stateIcon.className = 'w-8 h-8 rounded-full bg-blue-950/60 border border-blue-800/50 text-blue-400 flex items-center justify-center text-sm mx-auto mb-1.5';
      stateIcon.innerHTML = '<i class="fa-solid fa-shield-check"></i>';
    }
    if (riskVal) {
      riskVal.innerText = '12%';
      riskVal.className = 'text-2xl font-bold text-blue-400 font-mono';
    }
    if (riskBadge) {
      riskBadge.innerText = 'LOW RISK';
      riskBadge.className = 'text-[10px] font-medium block uppercase text-blue-400';
    }

    if (bKey) {
      bKey.innerText = 'Normal (85ms)';
      bKey.className = 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
    }
    if (keyDataBadge) {
      keyDataBadge.innerText = 'Safe';
      keyDataBadge.className = 'text-xs text-emerald-400';
    }
    if (bMouse) {
      bMouse.innerText = 'Normal';
      bMouse.className = 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
    }
    if (mouseDataBadge) {
      mouseDataBadge.innerText = 'Safe';
      mouseDataBadge.className = 'text-xs text-emerald-400';
    }
    if (bTyping) {
      bTyping.innerText = 'Normal';
      bTyping.className = 'text-blue-400 font-medium bg-blue-500/10 px-1.5 py-0.2 rounded border border-blue-500/20 text-[8px]';
    }
    if (bCursor) {
      bCursor.innerText = 'H: 3.12';
      bCursor.className = 'text-cyan-400 font-medium bg-cyan-500/10 px-1.5 py-0.2 rounded border border-cyan-500/20 text-[8px]';
    }
    if (entropyDataBadge) entropyDataBadge.innerText = 'H: 3.12';

    if (detKey) {
      detKey.innerText = 'Safe';
      detKey.className = 'px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono text-[9px]';
    }
    if (detMouse) {
      detMouse.innerText = 'Safe';
      detMouse.className = 'px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono text-[9px]';
    }

    if (typeof drawArcGauge === 'function') {
      drawArcGauge('canvasRiskGauge', 12, '#3b82f6');
    }

    if (this.rhythmBars) {
      const bars = this.rhythmBars.children;
      for (let b of bars) {
        b.className = 'bg-gradient-to-t from-blue-600 to-cyan-400 w-2 h-3.5 rounded-t transition-all duration-150';
      }
    }

    if (typeof appendLogTerminal === 'function') {
      appendLogTerminal('BEHAVIORAL BIOMETRICS: Live hardware sensor re-engaged. 60 Hz sampling active.');
    }
  }

  startOscilloscopeLoop() {
    const loop = () => {
      this.wavePhase += 0.05;

      // 1. Keystroke Dynamics Wave
      if (this.ctxKey && this.cvKey) {
        this.ctxKey.clearRect(0, 0, this.cvKey.width, this.cvKey.height);
        this.ctxKey.lineWidth = 1.8;
        this.ctxKey.strokeStyle = this.isBotSimActive ? '#f43f5e' : '#3b82f6';
        this.ctxKey.beginPath();
        const w1 = this.cvKey.width;
        const h1 = this.cvKey.height;
        for (let x = 0; x < w1; x++) {
          let y;
          if (this.isBotSimActive) {
            y = h1 / 2 + (Math.sin(x * 0.15 + this.wavePhase * 3) > 0 ? 8 : -8);
          } else {
            const jitter = (Math.sin(x * 0.4 + this.wavePhase) * 1.5) * (this.currentSpeed > 50 ? 1.5 : 0.5);
            y = (h1 / 2) + Math.sin(x * 0.08 + this.wavePhase) * 7 + Math.cos(x * 0.03 - this.wavePhase * 0.5) * 3 + jitter;
          }
          if (x === 0) this.ctxKey.moveTo(x, y);
          else this.ctxKey.lineTo(x, y);
        }
        this.ctxKey.stroke();
      }

      // 2. Mouse Trajectory Vector / Trail
      if (this.ctxMouse && this.cvMouse) {
        this.ctxMouse.clearRect(0, 0, this.cvMouse.width, this.cvMouse.height);
        this.ctxMouse.lineWidth = 1.8;
        this.ctxMouse.strokeStyle = this.isBotSimActive ? '#fb7185' : '#38bdf8';
        this.ctxMouse.beginPath();
        const w2 = this.cvMouse.width;
        const h2 = this.cvMouse.height;
        if (this.isBotSimActive) {
          this.ctxMouse.moveTo(4, h2 - 6);
          this.ctxMouse.lineTo(w2 - 4, 6);
        } else {
          for (let x = 0; x < w2; x++) {
            const y = (h2 / 2) + Math.sin(x * 0.06 - this.wavePhase * 1.2) * 8 + Math.sin(x * 0.14 + this.wavePhase * 0.8) * 3;
            if (x === 0) this.ctxMouse.moveTo(x, y);
            else this.ctxMouse.lineTo(x, y);
          }
        }
        this.ctxMouse.stroke();
      }

      // 3. Cursor Movement & Shannon Directional Entropy Curve
      if (this.ctxCursor && this.cvCursor) {
        this.ctxCursor.clearRect(0, 0, this.cvCursor.width, this.cvCursor.height);
        this.ctxCursor.lineWidth = 1.8;
        this.ctxCursor.strokeStyle = this.isBotSimActive ? '#f43f5e' : (this.currentEntropy < 1.0 ? '#f59e0b' : '#34d399');
        this.ctxCursor.beginPath();
        const w4 = this.cvCursor.width;
        const h4 = this.cvCursor.height;
        for (let x = 0; x < w4; x++) {
          let y;
          if (this.isBotSimActive) {
            y = h4 / 2;
          } else {
            const amp = Math.min(10, Math.max(3, this.currentEntropy * 2.5));
            y = (h4 / 2) + Math.sin(x * 0.1 + this.wavePhase * 1.5) * amp;
          }
          if (x === 0) this.ctxCursor.moveTo(x, y);
          else this.ctxCursor.lineTo(x, y);
        }
        this.ctxCursor.stroke();
      }

      requestAnimationFrame(loop);
    };

    requestAnimationFrame(loop);
  }
}

// Global initialization & event hookups
function initAegisSensor() {
  if (!window.aegisSensor) {
    try {
      window.aegisSensor = new AegisBiometricsSensor();
      console.log("✅ [Aegis Sensor] Behavioral Biometrics Engine Active (60 Hz Hardware Tracking)");
    } catch(err) {
      console.error("❌ [Aegis Sensor Init Error]:", err);
    }
  }
}

// Backward compatibility hook for inline button onclick="triggerBiometricsSim('bot'|'human')"
window.triggerBiometricsSim = function(mode) {
  initAegisSensor();
  if (!window.aegisSensor) return;
  if (mode === 'bot') {
    window.aegisSensor.simulateBotAttack();
  } else {
    window.aegisSensor.resetLiveSensor();
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAegisSensor);
} else {
  // DOM is already parsed! Initialize immediately
  initAegisSensor();
}
