/**
 * ═══════════════════════════════════════════════════════════════════
 * AT·OM ARCHE — MAIN APPLICATION
 * Diamond Transmuter Engine + Mercury Relay System
 * ═══════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════

const CONFIG = {
    // Boot Sequence
    BOOT_DURATION: 4500,      // 4.5 seconds total
    CHAKRA_SCAN_DELAY: 400,   // Delay between chakra activations
    
    // Heartbeat
    HEARTBEAT_INTERVAL: 4440, // 4.44 seconds (444Hz symbol)
    
    // WebSocket
    WS_URL: 'wss://api.chenu.io/resonance',
    WS_RECONNECT_DELAY: 1000,
    WS_MAX_RECONNECT: 5,
    
    // Buffer
    BUFFER_KEY: 'atom_resonance_buffer',
    MAX_BUFFER_SIZE: 100,
    
    // Architect Seal
    ARCHITECT_NAME: 'JONATHAN RODRIGUE',
    ARCHITECT_FREQUENCY: 999,
    
    // Frequencies (12 Agents)
    FREQUENCIES: [174, 285, 396, 417, 444, 528, 639, 741, 852, 888, 963, 999],
    ANCHOR_FREQUENCY: 444,
};

// ═══════════════════════════════════════════════════════════════════
// ARITHMOS ENGINE
// ═══════════════════════════════════════════════════════════════════

const ArithmosEngine = {
    MAP: {
        A:1,B:2,C:3,D:4,E:5,F:6,G:7,H:8,I:9,
        J:1,K:2,L:3,M:4,N:5,O:6,P:7,Q:8,R:9,
        S:1,T:2,U:3,V:4,W:5,X:6,Y:7,Z:8
    },
    
    calculate(text) {
        if (!text || typeof text !== 'string') return 0;
        
        let total = 0;
        for (const char of text.toUpperCase()) {
            total += this.MAP[char] || 0;
        }
        
        // Reduce to single digit (except master numbers)
        while (total > 9 && ![11, 22, 33].includes(total)) {
            total = String(total).split('').reduce((sum, d) => sum + parseInt(d), 0);
        }
        
        return total;
    },
    
    toFrequency(level) {
        return level * 111;
    },
    
    getLabel(level) {
        const labels = {
            1: 'IMPULSE/DNA',
            2: 'DUALITY/SHARE',
            3: 'MENTAL/GEOMETRY',
            4: 'STRUCTURE/ANCHOR',
            5: 'MOVEMENT/FIRE',
            6: 'HARMONY/SHIELD',
            7: 'INTROSPECTION',
            8: 'INFINITY/ABUNDANCE',
            9: 'UNITY/ARCHITECT',
            11: 'MASTER INTUITION',
            22: 'MASTER BUILDER',
            33: 'MASTER TEACHER'
        };
        return labels[level] || 'UNKNOWN';
    }
};

// ═══════════════════════════════════════════════════════════════════
// DIAMOND TRANSMUTER ENGINE
// ═══════════════════════════════════════════════════════════════════

const DiamondTransmuter = {
    frequencies: CONFIG.FREQUENCIES,
    currentFrequency: CONFIG.ANCHOR_FREQUENCY,
    phase: 0,
    isProcessing: false,
    
    /**
     * Transmute data through the 12 frequency stages
     */
    async transmute(inputData) {
        this.isProcessing = true;
        
        const result = {
            input: inputData,
            arithmos: ArithmosEngine.calculate(inputData),
            stages: [],
            output: null
        };
        
        result.level = result.arithmos;
        result.frequency = ArithmosEngine.toFrequency(result.level);
        
        // Process through each frequency stage
        for (const freq of this.frequencies) {
            const stage = await this.processStage(result, freq);
            result.stages.push(stage);
            
            // Update UI for each stage
            this.emitStageUpdate(freq, stage);
            
            // Small delay for visual feedback
            await this.sleep(50);
        }
        
        // Final crystallization
        result.output = this.crystallize(result);
        this.isProcessing = false;
        
        return result;
    },
    
    /**
     * Process a single frequency stage
     */
    async processStage(data, frequency) {
        const stage = {
            frequency,
            timestamp: Date.now(),
            action: this.getStageAction(frequency),
            status: 'complete'
        };
        
        // Apply stage-specific transformation
        switch (frequency) {
            case 174: // Root - Foundation
                stage.effect = 'Establishing foundation';
                break;
            case 285: // Sacral - Creativity
                stage.effect = 'Activating creative flow';
                break;
            case 396: // Solar - Liberation
                stage.effect = 'Releasing blockages';
                break;
            case 417: // Heart - Change
                stage.effect = 'Facilitating transformation';
                break;
            case 444: // Anchor - Stability
                stage.effect = 'ANCHORING SIGNAL';
                stage.isAnchor = true;
                break;
            case 528: // Throat - DNA Repair
                stage.effect = 'Harmonizing structure';
                break;
            case 639: // Third Eye - Connection
                stage.effect = 'Establishing connections';
                break;
            case 741: // Crown - Awakening
                stage.effect = 'Awakening consciousness';
                break;
            case 852: // Soul - Intuition
                stage.effect = 'Activating intuition';
                break;
            case 888: // Infinity - Abundance
                stage.effect = 'Opening abundance flow';
                break;
            case 963: // Divine - Pineal
                stage.effect = 'Connecting to source';
                break;
            case 999: // Architect - Unity
                stage.effect = 'ARCHITECT SEAL ACTIVATED';
                stage.isArchitect = true;
                break;
        }
        
        return stage;
    },
    
    getStageAction(frequency) {
        if (frequency === 444) return 'ANCHOR';
        if (frequency === 999) return 'SEAL';
        if (frequency < 444) return 'CLEANSE';
        return 'STRUCTURE';
    },
    
    /**
     * Crystallize the final output
     */
    crystallize(result) {
        const checksum = this.generateChecksum(result);
        
        return {
            signature: `${result.arithmos}-${result.frequency}-${checksum}`,
            frequency: result.frequency,
            level: result.level,
            label: ArithmosEngine.getLabel(result.level),
            phase: this.phase,
            timestamp: Date.now(),
            checksum
        };
    },
    
    generateChecksum(data) {
        const str = `${data.input}-${data.arithmos}-${data.frequency}-${Date.now()}`;
        let hash = 0;
        for (const char of str) {
            hash = ((hash << 5) - hash) + char.charCodeAt(0);
            hash |= 0;
        }
        return Math.abs(hash).toString(16).padStart(8, '0');
    },
    
    emitStageUpdate(frequency, stage) {
        window.dispatchEvent(new CustomEvent('atom:stage', {
            detail: { frequency, stage }
        }));
    },
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

// ═══════════════════════════════════════════════════════════════════
// MERCURY RELAY (Data Flow Manager)
// ═══════════════════════════════════════════════════════════════════

const MercuryRelay = {
    ws: null,
    isConnected: false,
    reconnectAttempts: 0,
    messageQueue: [],
    buffer: [],
    
    /**
     * Initialize the relay system
     */
    init() {
        this.loadBuffer();
        this.connect();
        this.startHeartbeat();
        
        // Handle offline/online events
        window.addEventListener('online', () => this.onOnline());
        window.addEventListener('offline', () => this.onOffline());
    },
    
    /**
     * Connect to WebSocket server
     */
    connect() {
        try {
            this.ws = new WebSocket(CONFIG.WS_URL);
            
            this.ws.onopen = () => {
                console.log('[RELAY] Connected');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.flushBuffer();
                this.updateConnectionUI(true);
            };
            
            this.ws.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };
            
            this.ws.onclose = () => {
                console.log('[RELAY] Disconnected');
                this.isConnected = false;
                this.updateConnectionUI(false);
                this.scheduleReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('[RELAY] Error:', error);
            };
        } catch (error) {
            console.log('[RELAY] WebSocket not available, running in offline mode');
            this.isConnected = false;
            this.updateConnectionUI(false);
        }
    },
    
    /**
     * Send data through the relay
     */
    send(type, payload) {
        const message = {
            type,
            payload: {
                ...payload,
                timestamp: Date.now(),
                sequence: this.messageQueue.length + 1
            }
        };
        
        if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
            this.messageQueue.push(message);
        } else {
            // Buffer for later
            this.buffer.push(message);
            this.saveBuffer();
            console.log('[RELAY] Buffered message (offline)');
        }
    },
    
    /**
     * Handle incoming messages
     */
    handleMessage(message) {
        switch (message.type) {
            case 'RESONANCE_ACK':
                this.handleAck(message.payload);
                break;
            case 'HEARTBEAT_ACK':
                this.handleHeartbeatAck(message.payload);
                break;
            case 'COLLECTIVE_UPDATE':
                this.handleCollectiveUpdate(message.payload);
                break;
        }
    },
    
    handleAck(payload) {
        const latency = Date.now() - payload.timestamp;
        console.log(`[RELAY] ACK received, latency: ${latency}ms`);
        
        // Update UI with collective frequency
        if (payload.collectiveFrequency) {
            document.getElementById('collective-freq').textContent = 
                `COLLECTIVE: ${payload.collectiveFrequency} Hz`;
        }
    },
    
    handleHeartbeatAck(payload) {
        // Update heartbeat timer display
        const timer = document.getElementById('heartbeat-timer');
        if (timer) {
            timer.textContent = '4.44s';
        }
    },
    
    handleCollectiveUpdate(payload) {
        window.dispatchEvent(new CustomEvent('atom:collective', {
            detail: payload
        }));
    },
    
    /**
     * Heartbeat system
     */
    startHeartbeat() {
        setInterval(() => {
            this.send('HEARTBEAT', {
                frequency: CONFIG.ANCHOR_FREQUENCY
            });
            
            // Pulse animation
            const pulse = document.getElementById('heartbeat-pulse');
            if (pulse) {
                pulse.style.animation = 'none';
                pulse.offsetHeight; // Trigger reflow
                pulse.style.animation = 'heartbeat 4.44s ease-in-out infinite';
            }
        }, CONFIG.HEARTBEAT_INTERVAL);
    },
    
    /**
     * Buffer management
     */
    loadBuffer() {
        try {
            const stored = localStorage.getItem(CONFIG.BUFFER_KEY);
            this.buffer = stored ? JSON.parse(stored) : [];
        } catch {
            this.buffer = [];
        }
    },
    
    saveBuffer() {
        try {
            const trimmed = this.buffer.slice(-CONFIG.MAX_BUFFER_SIZE);
            localStorage.setItem(CONFIG.BUFFER_KEY, JSON.stringify(trimmed));
        } catch (e) {
            console.warn('[RELAY] Failed to save buffer:', e);
        }
    },
    
    flushBuffer() {
        while (this.buffer.length > 0 && this.isConnected) {
            const message = this.buffer.shift();
            this.ws.send(JSON.stringify(message));
        }
        localStorage.removeItem(CONFIG.BUFFER_KEY);
        console.log('[RELAY] Buffer flushed');
    },
    
    /**
     * Reconnection logic with exponential backoff
     */
    scheduleReconnect() {
        if (this.reconnectAttempts >= CONFIG.WS_MAX_RECONNECT) {
            console.log('[RELAY] Max reconnect attempts reached');
            return;
        }
        
        const delay = CONFIG.WS_RECONNECT_DELAY * Math.pow(2, this.reconnectAttempts);
        this.reconnectAttempts++;
        
        console.log(`[RELAY] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
        setTimeout(() => this.connect(), delay);
    },
    
    onOnline() {
        console.log('[RELAY] Network online');
        this.connect();
    },
    
    onOffline() {
        console.log('[RELAY] Network offline');
        this.isConnected = false;
        this.updateConnectionUI(false);
    },
    
    updateConnectionUI(connected) {
        const status = document.getElementById('connection-status');
        if (status) {
            status.textContent = connected ? '● CONNECTED' : '● OFFLINE';
            status.classList.toggle('disconnected', !connected);
        }
    }
};

// ═══════════════════════════════════════════════════════════════════
// BOOT SEQUENCE
// ═══════════════════════════════════════════════════════════════════

const BootSequence = {
    messages: [
        'INITIALIZING ZERO POINT...',
        'LOADING RESONANCE MATRIX...',
        'CALIBRATING 12 AGENTS...',
        'SCANNING CHAKRA SYSTEMS...',
        'ESTABLISHING 444Hz ANCHOR...',
        'ACTIVATING DIAMOND TRANSMUTER...',
        'SYSTEM READY'
    ],
    
    chakras: [
        { hz: 111, color: '#FF0000' },
        { hz: 222, color: '#FF7F00' },
        { hz: 333, color: '#FFFF00' },
        { hz: 444, color: '#50C878' },
        { hz: 555, color: '#87CEEB' },
        { hz: 666, color: '#4B0082' },
        { hz: 777, color: '#EE82EE' }
    ],
    
    async run() {
        const overlay = document.getElementById('boot-overlay');
        const bootText = document.getElementById('boot-text');
        const bootBar = document.getElementById('boot-bar');
        const mainInterface = document.getElementById('main-interface');
        
        // Initial silence (1.5s)
        await this.sleep(1500);
        
        // Progress through messages
        for (let i = 0; i < this.messages.length; i++) {
            bootText.textContent = this.messages[i];
            const progress = ((i + 1) / this.messages.length) * 100;
            bootBar.style.width = `${progress}%`;
            
            await this.sleep(400);
        }
        
        // Chakra scan
        await this.scanChakras();
        
        // Transition to main interface
        await this.sleep(500);
        overlay.classList.add('hidden');
        mainInterface.classList.remove('hidden');
        
        console.log('[BOOT] Sequence complete');
    },
    
    async scanChakras() {
        const dots = document.querySelectorAll('.chakra-dot');
        
        for (let i = 0; i < dots.length; i++) {
            dots[i].classList.add('active');
            await this.sleep(CONFIG.CHAKRA_SCAN_DELAY);
        }
        
        // Keep all active briefly, then reset
        await this.sleep(500);
    },
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

// ═══════════════════════════════════════════════════════════════════
// UI CONTROLLER
// ═══════════════════════════════════════════════════════════════════

const UIController = {
    elements: {},
    
    init() {
        // Cache DOM elements
        this.elements = {
            input: document.getElementById('resonance-input'),
            arithmosValue: document.getElementById('arithmos-value'),
            levelValue: document.getElementById('level-value'),
            fluxFill: document.getElementById('flux-fill'),
            fluxPercent: document.getElementById('flux-percent'),
            currentFrequency: document.getElementById('current-frequency'),
            coreFrequency: document.getElementById('core-frequency'),
            outputSignature: document.getElementById('output-signature'),
            outputHz: document.getElementById('output-hz'),
            outputPhase: document.getElementById('output-phase'),
            outputLevel: document.getElementById('output-level'),
            transmitBtn: document.getElementById('transmit-btn'),
            agentNodes: document.querySelectorAll('.agent-node'),
            architectStatus: document.getElementById('architect-status')
        };
        
        // Bind events
        this.bindEvents();
        
        // Listen for stage updates
        window.addEventListener('atom:stage', (e) => this.onStageUpdate(e.detail));
    },
    
    bindEvents() {
        // Input handler with debounce
        let debounceTimer;
        this.elements.input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                this.onInputChange(e.target.value);
            }, 150);
        });
        
        // Transmit button
        this.elements.transmitBtn.addEventListener('click', () => {
            this.onTransmit();
        });
        
        // Architect seal check
        this.elements.input.addEventListener('input', (e) => {
            this.checkArchitectSeal(e.target.value);
        });
        
        // Agent node clicks
        this.elements.agentNodes.forEach(node => {
            node.addEventListener('click', () => {
                const hz = node.dataset.hz;
                this.focusFrequency(parseInt(hz));
            });
        });
    },
    
    onInputChange(value) {
        const arithmos = ArithmosEngine.calculate(value);
        const frequency = ArithmosEngine.toFrequency(arithmos);
        
        // Update metrics
        this.elements.arithmosValue.textContent = arithmos;
        this.elements.levelValue.textContent = arithmos;
        this.elements.currentFrequency.textContent = `${frequency} Hz`;
        this.elements.coreFrequency.textContent = frequency;
        
        // Update flux stability (based on input length)
        const stability = Math.min(100, value.length * 5);
        this.elements.fluxFill.style.width = `${stability}%`;
        this.elements.fluxPercent.textContent = `${stability}%`;
        
        // Send to relay
        MercuryRelay.send('RESONANCE_EMIT', {
            inputText: value,
            arithmosValue: arithmos,
            frequencyHz: frequency,
            level: arithmos
        });
    },
    
    async onTransmit() {
        const input = this.elements.input.value;
        if (!input) return;
        
        // Disable button during processing
        this.elements.transmitBtn.disabled = true;
        this.elements.transmitBtn.querySelector('.btn-text').textContent = 'TRANSMUTING...';
        
        // Process through Diamond Transmuter
        const result = await DiamondTransmuter.transmute(input);
        
        // Update output display
        this.updateOutput(result.output);
        
        // Re-enable button
        this.elements.transmitBtn.disabled = false;
        this.elements.transmitBtn.querySelector('.btn-text').textContent = 'TRANSMIT';
        
        // Send final result
        MercuryRelay.send('TRANSMUTATION_COMPLETE', result.output);
    },
    
    onStageUpdate({ frequency, stage }) {
        // Find and activate the corresponding agent node
        this.elements.agentNodes.forEach(node => {
            const nodeHz = parseInt(node.dataset.hz);
            
            // Activate nodes up to current frequency
            if (nodeHz <= frequency) {
                node.classList.add('active');
            }
            
            // Highlight current
            if (nodeHz === frequency) {
                node.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    node.style.transform = '';
                }, 100);
            }
        });
    },
    
    updateOutput(output) {
        if (!output) return;
        
        this.elements.outputSignature.textContent = output.signature;
        this.elements.outputHz.textContent = output.frequency;
        this.elements.outputPhase.textContent = `${output.phase}°`;
        this.elements.outputLevel.textContent = output.level;
        
        // Animate crystal
        const crystal = document.getElementById('crystal');
        crystal.style.animation = 'none';
        crystal.offsetHeight;
        crystal.style.animation = 'crystal-rotate 2s linear infinite';
    },
    
    focusFrequency(hz) {
        this.elements.coreFrequency.textContent = hz;
        this.elements.currentFrequency.textContent = `${hz} Hz`;
        
        // Highlight the node
        this.elements.agentNodes.forEach(node => {
            node.classList.toggle('active', parseInt(node.dataset.hz) === hz);
        });
    },
    
    checkArchitectSeal(text) {
        const isArchitect = text.toUpperCase().includes(CONFIG.ARCHITECT_NAME);
        
        if (isArchitect) {
            this.elements.architectStatus.textContent = '🔓';
            document.body.classList.add('architect-mode');
            
            // Activate all agents
            this.elements.agentNodes.forEach(node => {
                node.classList.add('active');
            });
            
            console.log('[ARCHITECT] Seal verified: JONATHAN RODRIGUE = 9 = 999 Hz');
        } else {
            this.elements.architectStatus.textContent = '🔒';
            document.body.classList.remove('architect-mode');
        }
    }
};

// ═══════════════════════════════════════════════════════════════════
// AGENTS SYSTEM (350+ Agents Simulation)
// ═══════════════════════════════════════════════════════════════════

const AgentsSystem = {
    agents: [],
    isLibertyMode: true,
    
    init() {
        // Generate 350 simulated agents
        this.generateAgents(350);
        
        // Start liberty mode (self-organization)
        this.startLibertyMode();
        
        // Update active agents count
        this.updateAgentCount();
    },
    
    generateAgents(count) {
        const frequencies = [111, 222, 333, 444, 555, 666, 777, 888, 999];
        
        for (let i = 0; i < count; i++) {
            const freq = frequencies[i % frequencies.length];
            this.agents.push({
                id: `agent-${i}`,
                frequency: freq,
                phase: Math.random() * 360,
                mode: 'liberty',
                lastVibration: Date.now()
            });
        }
    },
    
    startLibertyMode() {
        // Self-organization tick every 4.44 seconds
        setInterval(() => {
            if (!this.isLibertyMode) return;
            
            this.agents.forEach(agent => {
                // Phase drift towards collective
                agent.phase = (agent.phase + 1) % 360;
                agent.lastVibration = Date.now();
            });
            
            this.updateAgentCount();
        }, CONFIG.HEARTBEAT_INTERVAL);
    },
    
    updateAgentCount() {
        const active = this.agents.filter(a => a.mode !== 'dormant').length;
        const total = this.agents.length;
        
        const display = document.getElementById('active-agents');
        if (display) {
            display.textContent = `${active}/${total}`;
        }
    },
    
    awakenAll() {
        this.agents.forEach(agent => {
            agent.mode = 'active';
            agent.phase = 0; // Synchronized
        });
        
        console.log(`[AGENTS] All ${this.agents.length} agents awakened`);
        this.updateAgentCount();
    }
};

// ═══════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', async () => {
    console.log('[AT·OM] Initializing ARCHE system...');
    
    // Run boot sequence
    await BootSequence.run();
    
    // Initialize systems
    UIController.init();
    MercuryRelay.init();
    AgentsSystem.init();
    
    console.log('[AT·OM] System operational');
    console.log('[AT·OM] Architect: JONATHAN RODRIGUE = 9 = 999 Hz');
});

// ═══════════════════════════════════════════════════════════════════
// EXPORTS (for module usage)
// ═══════════════════════════════════════════════════════════════════

export {
    CONFIG,
    ArithmosEngine,
    DiamondTransmuter,
    MercuryRelay,
    BootSequence,
    UIController,
    AgentsSystem
};
