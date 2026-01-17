/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                         AT·OM - INFRASTRUCTURE INVISIBLE                      ║
 * ║                                                                              ║
 * ║            PROPRIÉTÉ EXCLUSIVE DE JONATHAN EMMANUEL RODRIGUE                 ║
 * ║                    TOUS DROITS RÉSERVÉS - BREVET EN COURS                    ║
 * ║                                    2025                                       ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION SOUVERAINE
// ═══════════════════════════════════════════════════════════════════════════════

const CONFIG = {
    API_URL: 'https://api.atom-sovereign.com',
    FREQ_BASE: 432,
    FREQ_TARGET: 999,
    SCEAU_DURATION: 2000,
    TOTAL_AGENTS: 350,
    SPHERES: {
        personal:      { count: 28, color: '#4A90D9', name: 'Personnel' },
        business:      { count: 43, color: '#50C878', name: 'Business' },
        government:    { count: 18, color: '#9B59B6', name: 'Gouvernement' },
        creative:      { count: 42, color: '#F39C12', name: 'Créatif' },
        community:     { count: 12, color: '#E74C3C', name: 'Communauté' },
        social:        { count: 15, color: '#1ABC9C', name: 'Social' },
        entertainment: { count: 8,  color: '#E91E63', name: 'Divertissement' },
        team:          { count: 35, color: '#3498DB', name: 'Équipe' },
        scholar:       { count: 25, color: '#8E44AD', name: 'Éducation' },
        transport:     { count: 50, color: '#27AE60', name: 'Transport' },
        societal:      { count: 20, color: '#F1C40F', name: 'Sociétal' },
        environment:   { count: 25, color: '#2ECC71', name: 'Environnement' },
        privacy:       { count: 8,  color: '#95A5A6', name: 'Vie Privée' },
        jeunesse:      { count: 15, color: '#FF6B6B', name: 'Jeunesse' },
        dashboard:     { count: 6,  color: '#D4AF37', name: 'Tableau de Bord' }
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAT GLOBAL
// ═══════════════════════════════════════════════════════════════════════════════

const State = {
    isActivated: false,
    currentFrequency: CONFIG.FREQ_BASE,
    agents: [],
    selectedAgent: null,
    currentModule: null,
    touchStartTime: 0,
    isTouching: false,
    animationId: null,
    protocolTaps: 0,
    protocolTimer: null,
    selectedDispersion: null
};

// ═══════════════════════════════════════════════════════════════════════════════
// CACHE DOM
// ═══════════════════════════════════════════════════════════════════════════════

const DOM = {};

function cacheDOM() {
    DOM.sceauView = document.getElementById('sceau-view');
    DOM.essaimView = document.getElementById('essaim-view');
    DOM.moduleView = document.getElementById('module-view');
    DOM.protocolView = document.getElementById('protocol-view');
    DOM.sceau = document.getElementById('sceau');
    DOM.freqValue = document.getElementById('freq-value');
    DOM.freqIndicator = document.querySelector('.frequency-indicator');
    DOM.progressBar = document.getElementById('progress-bar');
    DOM.ringProgress = document.querySelector('.ring-progress');
    DOM.swarmCanvas = document.getElementById('swarm-canvas');
    DOM.swarmContainer = document.getElementById('swarm-container');
    DOM.agentCount = document.querySelector('.agent-count');
    DOM.liveFreq = document.getElementById('live-freq');
    DOM.agentPanel = document.getElementById('agent-panel');
    DOM.panelSphere = document.getElementById('panel-sphere');
    DOM.panelName = document.getElementById('panel-name');
    DOM.panelFunction = document.getElementById('panel-function');
    DOM.panelFreq = document.getElementById('panel-freq');
    DOM.moduleTitle = document.getElementById('module-title');
    DOM.moduleBody = document.getElementById('module-body');
    DOM.navModules = document.querySelectorAll('.nav-module');
    DOM.btnBack = document.getElementById('btn-back');
    DOM.dispersionLevels = document.querySelectorAll('.dispersion-level');
    DOM.confirmSection = document.getElementById('confirm-section');
    DOM.confirmInput = document.getElementById('confirm-input');
    DOM.btnExecute = document.getElementById('btn-execute');
    DOM.btnCancelProtocol = document.getElementById('btn-cancel-protocol');
    DOM.particlesContainer = document.getElementById('particles-container');
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE SCEAU - ENGAGEMENT SOUVERAIN
// ═══════════════════════════════════════════════════════════════════════════════

function initSceau() {
    const sceau = DOM.sceau;
    sceau.addEventListener('touchstart', onSceauStart, { passive: true });
    sceau.addEventListener('touchend', onSceauEnd);
    sceau.addEventListener('touchcancel', onSceauEnd);
    sceau.addEventListener('mousedown', onSceauStart);
    sceau.addEventListener('mouseup', onSceauEnd);
    sceau.addEventListener('mouseleave', onSceauEnd);
}

function onSceauStart(e) {
    if (State.isActivated) return;
    State.touchStartTime = performance.now();
    State.isTouching = true;
    DOM.sceau.classList.add('activating');
    DOM.freqIndicator.classList.add('active');
    animateSceau();
}

function onSceauEnd() {
    if (!State.isTouching) return;
    State.isTouching = false;
    const elapsed = performance.now() - State.touchStartTime;
    if (elapsed >= CONFIG.SCEAU_DURATION && !State.isActivated) {
        completeSceau();
    } else {
        resetSceau();
    }
}

function animateSceau() {
    if (!State.isTouching || State.isActivated) return;
    const elapsed = performance.now() - State.touchStartTime;
    const progress = Math.min(elapsed / CONFIG.SCEAU_DURATION, 1);

    State.currentFrequency = Math.round(CONFIG.FREQ_BASE + (CONFIG.FREQ_TARGET - CONFIG.FREQ_BASE) * progress);
    DOM.freqValue.textContent = State.currentFrequency;
    DOM.progressBar.style.width = `${progress * 100}%`;

    const circumference = 565.48;
    DOM.ringProgress.style.strokeDashoffset = circumference * (1 - progress);

    if (State.currentFrequency >= CONFIG.FREQ_TARGET) {
        DOM.freqIndicator.classList.add('harmony');
    }

    if (progress >= 1) {
        completeSceau();
    } else {
        State.animationId = requestAnimationFrame(animateSceau);
    }
}

function resetSceau() {
    if (State.animationId) cancelAnimationFrame(State.animationId);
    State.currentFrequency = CONFIG.FREQ_BASE;
    DOM.freqValue.textContent = CONFIG.FREQ_BASE;
    DOM.progressBar.style.width = '0%';
    DOM.ringProgress.style.strokeDashoffset = 565.48;
    DOM.sceau.classList.remove('activating');
    DOM.freqIndicator.classList.remove('active', 'harmony');
}

function completeSceau() {
    State.isActivated = true;
    State.isTouching = false;
    if (State.animationId) cancelAnimationFrame(State.animationId);

    DOM.sceau.classList.remove('activating');
    DOM.sceau.classList.add('success');
    DOM.sceauView.classList.add('completing');

    createExplosion(window.innerWidth / 2, window.innerHeight / 2);

    setTimeout(() => {
        switchView('essaim');
        initSwarm();
    }, 1200);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPLOSION PARTICLES
// ═══════════════════════════════════════════════════════════════════════════════

function createExplosion(x, y) {
    const container = DOM.particlesContainer;
    for (let i = 0; i < CONFIG.TOTAL_AGENTS; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const angle = (Math.PI * 2 * i) / CONFIG.TOTAL_AGENTS + (Math.random() - 0.5) * 0.5;
        const distance = 150 + Math.random() * 250;
        particle.style.cssText = `left:${x}px;top:${y}px;--tx:${Math.cos(angle)*distance}px;--ty:${Math.sin(angle)*distance}px;animation-delay:${Math.random()*0.2}s`;
        container.appendChild(particle);
        setTimeout(() => particle.remove(), 1500);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// L'ESSAIM - 350 AGENTS (CANVAS)
// ═══════════════════════════════════════════════════════════════════════════════

let canvas, ctx;

function initSwarm() {
    canvas = DOM.swarmCanvas;
    ctx = canvas.getContext('2d');
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    generateAgents();
    animateSwarm();
    canvas.addEventListener('click', onCanvasClick);
    DOM.liveFreq.addEventListener('click', onProtocolTap);
}

function resizeCanvas() {
    const container = DOM.swarmContainer;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = container.offsetWidth * dpr;
    canvas.height = container.offsetHeight * dpr;
    canvas.style.width = container.offsetWidth + 'px';
    canvas.style.height = container.offsetHeight + 'px';
    ctx.scale(dpr, dpr);
}

function generateAgents() {
    State.agents = [];
    let id = 0;
    const width = DOM.swarmContainer.offsetWidth;
    const height = DOM.swarmContainer.offsetHeight;
    const cx = width / 2, cy = height / 2;

    Object.entries(CONFIG.SPHERES).forEach(([sphere, data]) => {
        for (let i = 0; i < data.count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const radius = 50 + Math.random() * Math.min(width, height) * 0.35;
            State.agents.push({
                id: id++, sphere,
                name: `${data.name} #${i + 1}`,
                function: getAgentFunction(sphere, i),
                color: data.color,
                x: cx + Math.cos(angle) * radius,
                y: cy + Math.sin(angle) * radius,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: 4 + Math.random() * 3,
                frequency: CONFIG.FREQ_BASE + Math.random() * (CONFIG.FREQ_TARGET - CONFIG.FREQ_BASE)
            });
        }
    });
}

function getAgentFunction(sphere, i) {
    const f = {
        personal: ['Identité', 'Calendrier', 'Contacts', 'Notes', 'Préférences'],
        business: ['CRM', 'Facturation', 'Projets', 'Analytics', 'Pipeline'],
        government: ['Documents', 'Déclarations', 'Conformité', 'Archives'],
        creative: ['Assets', 'Design', 'Portfolio', 'Médias'],
        community: ['Forums', 'Événements', 'Groupes'],
        social: ['Publications', 'Analytics', 'Réputation'],
        entertainment: ['Streaming', 'Jeux', 'Musique'],
        team: ['Tâches', 'Réunions', 'Fichiers', 'Chat'],
        scholar: ['Recherche', 'Citations', 'Cours'],
        transport: ['Navigation', 'Flotte', 'Réservations', 'Trafic'],
        societal: ['Civique', 'Bénévolat', 'Initiatives'],
        environment: ['Carbone', 'Recyclage', 'Énergie', 'Biodiversité'],
        privacy: ['Audit', 'Consentements', 'Chiffrement'],
        jeunesse: ['Mentor', 'Clans', 'Jeux Éducatifs'],
        dashboard: ['Métriques', 'Santé', 'Rapports']
    };
    const list = f[sphere] || ['Agent'];
    return list[i % list.length];
}

function animateSwarm() {
    const w = DOM.swarmContainer.offsetWidth;
    const h = DOM.swarmContainer.offsetHeight;
    ctx.clearRect(0, 0, w, h);

    State.agents.forEach(a => {
        a.vx += (Math.random() - 0.5) * 0.1;
        a.vy += (Math.random() - 0.5) * 0.1;
        a.vx *= 0.98; a.vy *= 0.98;
        a.x += a.vx; a.y += a.vy;
        if (a.x < 20 || a.x > w - 20) a.vx *= -1;
        if (a.y < 20 || a.y > h - 20) a.vy *= -1;
        a.x = Math.max(20, Math.min(w - 20, a.x));
        a.y = Math.max(20, Math.min(h - 20, a.y));

        ctx.beginPath();
        ctx.arc(a.x, a.y, a.size, 0, Math.PI * 2);
        ctx.fillStyle = a.color;
        ctx.globalAlpha = 0.8;
        ctx.fill();
        ctx.globalAlpha = 1;
    });

    requestAnimationFrame(animateSwarm);
}

function onCanvasClick(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    let clicked = null, minD = 30;

    State.agents.forEach(a => {
        const d = Math.hypot(a.x - x, a.y - y);
        if (d < minD) { minD = d; clicked = a; }
    });

    if (clicked) showAgentPanel(clicked);
    else hideAgentPanel();
}

function showAgentPanel(a) {
    State.selectedAgent = a;
    DOM.panelSphere.textContent = CONFIG.SPHERES[a.sphere].name;
    DOM.panelName.textContent = a.name;
    DOM.panelFunction.textContent = a.function;
    DOM.panelFreq.textContent = Math.round(a.frequency);
    DOM.agentPanel.classList.remove('hidden');
    DOM.agentPanel.classList.add('visible');
}

function hideAgentPanel() {
    DOM.agentPanel.classList.remove('visible');
    DOM.agentPanel.classList.add('hidden');
    State.selectedAgent = null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MODULES
// ═══════════════════════════════════════════════════════════════════════════════

function initModules() {
    DOM.navModules.forEach(btn => {
        btn.addEventListener('click', () => openModule(btn.dataset.module));
    });
    DOM.btnBack.addEventListener('click', closeModule);
    document.querySelector('.panel-close')?.addEventListener('click', hideAgentPanel);
}

function openModule(m) {
    State.currentModule = m;
    const titles = { genie: 'GÉNIE', alchimie: 'ALCHIMIE', flux: 'FLUX', sante: 'SANTÉ' };
    DOM.moduleTitle.textContent = titles[m] || m.toUpperCase();
    DOM.moduleBody.innerHTML = getModuleContent(m);
    switchView('module');
}

function closeModule() {
    switchView('essaim');
    State.currentModule = null;
}

function getModuleContent(m) {
    const c = {
        genie: `<div class="module-card"><h3>Clans d'Apprentissage</h3><p>Groupes thématiques pour l'apprentissage collaboratif.</p></div>
                <div class="module-card"><h3>Agent Mentor</h3><p>Assistant IA respectant la souveraineté humaine (Rule #1).</p></div>
                <div class="module-card"><h3>Tableau Blanc ∞</h3><p>Espace de collaboration infini.</p></div>`,
        alchimie: `<div class="freq-display"><div class="value">${CONFIG.FREQ_TARGET}</div><div class="label">HARMONIE PARFAITE</div></div>
                   <input type="range" class="freq-slider" min="${CONFIG.FREQ_BASE}" max="${CONFIG.FREQ_TARGET}" value="${CONFIG.FREQ_TARGET}">
                   <div class="module-card"><h3>Spectrogramme</h3><p>Visualisation des fréquences 432-999Hz.</p></div>`,
        flux: `<div class="flow-container"><div class="flow-item"><div class="flow-arrow in">↑</div><div class="flow-label">ENTRÉES</div></div>
               <div class="flow-item"><div class="flow-arrow out">↓</div><div class="flow-label">SORTIES</div></div></div>
               <div class="equilibre-bar"><div class="equilibre-label">ÉQUILIBRE</div><div class="equilibre-track"><div class="equilibre-fill"></div></div></div>`,
        sante: `<div class="health-metrics"><div class="health-item"><div class="health-icon" style="color:#E74C3C">♥</div><div class="health-value">72</div><div class="health-label">BPM</div></div>
                <div class="health-item"><div class="health-icon" style="color:#3498DB">☁</div><div class="health-value" style="color:#10B981">Bas</div><div class="health-label">STRESS</div></div></div>
                <div class="module-card"><h3>Respiration</h3><div class="breathing-circle"></div><p class="breathing-text">Inspirez... Expirez...</p></div>`
    };
    return c[m] || '<p>Module en développement</p>';
}

// ═══════════════════════════════════════════════════════════════════════════════
// PROTOCOL-999 - BRISE-CIRCUIT
// ═══════════════════════════════════════════════════════════════════════════════

function onProtocolTap() {
    State.protocolTaps++;
    clearTimeout(State.protocolTimer);
    if (State.protocolTaps >= 3) {
        State.protocolTaps = 0;
        openProtocol();
    } else {
        State.protocolTimer = setTimeout(() => State.protocolTaps = 0, 500);
    }
}

function openProtocol() {
    State.selectedDispersion = null;
    DOM.confirmSection.classList.add('hidden');
    DOM.confirmInput.value = '';
    DOM.dispersionLevels.forEach(b => b.classList.remove('selected'));
    switchView('protocol');
}

function closeProtocol() { switchView('essaim'); }

function initProtocol() {
    DOM.dispersionLevels.forEach(btn => {
        btn.addEventListener('click', () => {
            DOM.dispersionLevels.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            State.selectedDispersion = btn.dataset.level;
            DOM.confirmSection.classList.remove('hidden');
        });
    });
    DOM.btnExecute.addEventListener('click', executeDispersion);
    DOM.btnCancelProtocol.addEventListener('click', closeProtocol);
}

function executeDispersion() {
    if (!DOM.confirmInput.value.trim()) { alert('Code requis'); return; }
    if (!State.selectedDispersion) { alert('Sélectionnez un niveau'); return; }

    const pct = { partial: 0.2, sectoral: 0.5, total: 1.0 }[State.selectedDispersion];
    const dispersed = Math.floor(CONFIG.TOTAL_AGENTS * pct);
    State.agents = State.agents.slice(dispersed);
    DOM.agentCount.textContent = State.agents.length;
    closeProtocol();
}

// ═══════════════════════════════════════════════════════════════════════════════
// NAVIGATION GESTUELLE
// ═══════════════════════════════════════════════════════════════════════════════

function initGestures() {
    let startX = 0;
    DOM.swarmContainer.addEventListener('touchstart', e => startX = e.touches[0].clientX, { passive: true });
    DOM.swarmContainer.addEventListener('touchend', e => {
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 80) {
            const modules = ['genie', 'alchimie', 'flux', 'sante'];
            const idx = modules.indexOf(State.currentModule);
            if (dx < 0) openModule(modules[idx < 0 ? 0 : (idx + 1) % modules.length]);
            else openModule(modules[idx < 0 ? modules.length - 1 : (idx - 1 + modules.length) % modules.length]);
        }
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// VIEW MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════════

function switchView(name) {
    ['sceau', 'essaim', 'module', 'protocol'].forEach(v => {
        document.getElementById(`${v}-view`)?.classList.toggle('active', v === name);
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════════

function init() {
    cacheDOM();
    initSceau();
    initModules();
    initProtocol();
    initGestures();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
