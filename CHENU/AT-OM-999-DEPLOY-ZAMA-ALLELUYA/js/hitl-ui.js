/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM HITL UI - CHE·NU™ V76
 * Interface Utilisateur pour Approbation des Checkpoints
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Composants:
 * - Modal d'approbation
 * - Toast notifications
 * - Badge compteur pending
 * - Panel historique
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// STYLES CSS INJECTES
// ═══════════════════════════════════════════════════════════════════════════════

const HITL_STYLES = `
/* ═══════════════════════════════════════════════════════════════════════════════
   HITL UI STYLES - AT-OM CHE·NU™ V76
   ═══════════════════════════════════════════════════════════════════════════════ */

.hitl-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(8px);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.hitl-overlay.visible {
    opacity: 1;
    visibility: visible;
}

.hitl-modal {
    background: linear-gradient(135deg, #1a1a2e, #0a0a0f);
    border: 2px solid #D4AF37;
    border-radius: 16px;
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    overflow: hidden;
    transform: scale(0.9);
    transition: transform 0.3s ease;
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.3);
}

.hitl-overlay.visible .hitl-modal {
    transform: scale(1);
}

.hitl-header {
    padding: 1.5rem;
    background: rgba(212, 175, 55, 0.1);
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.hitl-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.hitl-icon.hitl { background: rgba(147, 51, 234, 0.2); border: 2px solid #9333EA; }
.hitl-icon.approval { background: rgba(212, 175, 55, 0.2); border: 2px solid #D4AF37; }
.hitl-icon.threshold { background: rgba(255, 215, 0, 0.2); border: 2px solid #FFD700; }

.hitl-title {
    flex: 1;
}

.hitl-title h3 {
    margin: 0;
    color: #D4AF37;
    font-size: 1.1rem;
}

.hitl-title p {
    margin: 0.25rem 0 0;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
}

.hitl-close {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hitl-close:hover {
    background: rgba(255, 107, 107, 0.3);
}

.hitl-body {
    padding: 1.5rem;
    max-height: 300px;
    overflow-y: auto;
}

.hitl-section {
    margin-bottom: 1.25rem;
}

.hitl-section-title {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

.hitl-action-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 1rem;
}

.hitl-action-name {
    font-weight: 600;
    color: white;
    margin-bottom: 0.5rem;
}

.hitl-action-detail {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.hitl-action-detail span {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.hitl-impact-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 0.75rem;
}

.hitl-impact-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}

.hitl-impact-fill.low { background: #00FF88; }
.hitl-impact-fill.medium { background: #FFD700; }
.hitl-impact-fill.high { background: #FF6B6B; }

.hitl-timer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.5);
}

.hitl-timer-value {
    font-family: monospace;
    color: #D4AF37;
}

.hitl-notes {
    width: 100%;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    font-size: 0.9rem;
    resize: vertical;
    min-height: 60px;
}

.hitl-notes:focus {
    outline: none;
    border-color: #D4AF37;
}

.hitl-footer {
    padding: 1rem 1.5rem;
    background: rgba(0, 0, 0, 0.3);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
}

.hitl-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hitl-btn-approve {
    background: linear-gradient(135deg, #00FF88, #00AA55);
    border: none;
    color: #000;
}

.hitl-btn-approve:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
}

.hitl-btn-reject {
    background: transparent;
    border: 2px solid #FF6B6B;
    color: #FF6B6B;
}

.hitl-btn-reject:hover {
    background: rgba(255, 107, 107, 0.2);
}

.hitl-btn-escalate {
    background: transparent;
    border: 2px solid #FFD700;
    color: #FFD700;
}

.hitl-btn-escalate:hover {
    background: rgba(255, 215, 0, 0.2);
}

/* Toast Notifications */
.hitl-toast-container {
    position: fixed;
    top: 80px;
    right: 24px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.hitl-toast {
    background: rgba(10, 10, 15, 0.95);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    min-width: 300px;
    max-width: 400px;
    transform: translateX(120%);
    transition: transform 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.hitl-toast.visible {
    transform: translateX(0);
}

.hitl-toast-icon {
    font-size: 1.25rem;
}

.hitl-toast-content {
    flex: 1;
}

.hitl-toast-title {
    font-weight: 600;
    color: white;
    font-size: 0.9rem;
}

.hitl-toast-message {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 0.2rem;
}

.hitl-toast-action {
    padding: 0.4rem 0.8rem;
    background: #D4AF37;
    border: none;
    border-radius: 6px;
    color: #000;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
}

.hitl-toast.warning { border-left: 4px solid #FFD700; }
.hitl-toast.critical { border-left: 4px solid #FF6B6B; }
.hitl-toast.success { border-left: 4px solid #00FF88; }

/* Pending Badge */
.hitl-pending-badge {
    position: fixed;
    bottom: 100px;
    right: 24px;
    background: #FF6B6B;
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: bold;
    z-index: 1001;
    animation: pulse-badge 2s infinite;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.5);
}

.hitl-pending-badge.hidden {
    display: none;
}

@keyframes pulse-badge {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Mobile */
@media (max-width: 480px) {
    .hitl-modal {
        width: 95%;
        max-height: 90vh;
    }

    .hitl-footer {
        flex-direction: column;
    }

    .hitl-btn {
        width: 100%;
        justify-content: center;
    }

    .hitl-toast {
        min-width: unset;
        max-width: calc(100vw - 48px);
    }
}
`;

// ═══════════════════════════════════════════════════════════════════════════════
// HITL UI MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

class HITLUI {
    constructor(checkpointManager) {
        this.checkpointManager = checkpointManager;
        this.currentCheckpoint = null;
        this.toasts = [];
        this.timerInterval = null;

        // Injecte les styles
        this._injectStyles();

        // Cree les containers
        this._createContainers();

        // Bind les callbacks du CheckpointManager
        if (checkpointManager) {
            checkpointManager.onApprovalRequired = (cp) => this.showApprovalModal(cp);
            checkpointManager.onCheckpointResolved = (cp, resolution) => this._onResolved(cp, resolution);
        }

        console.log('%c[HITL UI] Initialized', 'color: #9333EA;');
    }

    /**
     * Injecte les styles CSS
     */
    _injectStyles() {
        if (document.getElementById('hitl-styles')) return;

        const style = document.createElement('style');
        style.id = 'hitl-styles';
        style.textContent = HITL_STYLES;
        document.head.appendChild(style);
    }

    /**
     * Cree les containers DOM
     */
    _createContainers() {
        // Container pour les toasts
        if (!document.getElementById('hitl-toast-container')) {
            const toastContainer = document.createElement('div');
            toastContainer.id = 'hitl-toast-container';
            toastContainer.className = 'hitl-toast-container';
            document.body.appendChild(toastContainer);
        }

        // Badge pending
        if (!document.getElementById('hitl-pending-badge')) {
            const badge = document.createElement('div');
            badge.id = 'hitl-pending-badge';
            badge.className = 'hitl-pending-badge hidden';
            badge.onclick = () => this._showPendingList();
            document.body.appendChild(badge);
        }

        // Overlay modal
        if (!document.getElementById('hitl-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'hitl-overlay';
            overlay.className = 'hitl-overlay';
            overlay.onclick = (e) => {
                if (e.target === overlay) this.hideModal();
            };
            document.body.appendChild(overlay);
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // APPROVAL MODAL
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Affiche le modal d'approbation
     */
    showApprovalModal(checkpoint) {
        this.currentCheckpoint = checkpoint;
        const overlay = document.getElementById('hitl-overlay');

        const impactClass = checkpoint.estimatedImpact > 0.7 ? 'high' :
            checkpoint.estimatedImpact > 0.4 ? 'medium' : 'low';

        const iconType = checkpoint.type === 'hitl' ? 'hitl' :
            checkpoint.type === 'approval' ? 'approval' : 'threshold';

        overlay.innerHTML = `
            <div class="hitl-modal">
                <div class="hitl-header">
                    <div class="hitl-icon ${iconType}">
                        ${checkpoint.type === 'hitl' ? '🔐' : checkpoint.type === 'approval' ? '✋' : '⚡'}
                    </div>
                    <div class="hitl-title">
                        <h3>Approbation Requise</h3>
                        <p>Checkpoint ${checkpoint.type.toUpperCase()} - ${checkpoint.id.slice(0, 12)}</p>
                    </div>
                    <button class="hitl-close" onclick="window.hitlUI.hideModal()">×</button>
                </div>

                <div class="hitl-body">
                    <div class="hitl-section">
                        <div class="hitl-section-title">Action Demandee</div>
                        <div class="hitl-action-card">
                            <div class="hitl-action-name">${checkpoint.action?.name || 'Action'}</div>
                            <div class="hitl-action-detail">
                                <span>📁 Type: ${checkpoint.action?.type || 'N/A'}</span>
                                <span>🤖 Agent: ${checkpoint.agentId}</span>
                            </div>
                            <div class="hitl-impact-bar">
                                <div class="hitl-impact-fill ${impactClass}"
                                     style="width: ${checkpoint.estimatedImpact * 100}%"></div>
                            </div>
                            <div style="margin-top: 0.5rem; font-size: 0.8rem; color: rgba(255,255,255,0.5);">
                                Impact estime: ${(checkpoint.estimatedImpact * 100).toFixed(0)}%
                            </div>
                        </div>
                    </div>

                    <div class="hitl-section">
                        <div class="hitl-section-title">Temps Restant</div>
                        <div class="hitl-timer">
                            <span>⏱</span>
                            <span class="hitl-timer-value" id="hitl-timer">--:--</span>
                        </div>
                    </div>

                    <div class="hitl-section">
                        <div class="hitl-section-title">Notes (optionnel)</div>
                        <textarea class="hitl-notes" id="hitl-notes"
                                  placeholder="Ajouter une note de resolution..."></textarea>
                    </div>
                </div>

                <div class="hitl-footer">
                    <button class="hitl-btn hitl-btn-escalate" onclick="window.hitlUI.escalate()">
                        ↗ Escalader
                    </button>
                    <button class="hitl-btn hitl-btn-reject" onclick="window.hitlUI.reject()">
                        ✕ Rejeter
                    </button>
                    <button class="hitl-btn hitl-btn-approve" onclick="window.hitlUI.approve()">
                        ✓ Approuver
                    </button>
                </div>
            </div>
        `;

        overlay.classList.add('visible');
        this._startTimer(checkpoint);
        this._updatePendingBadge();
    }

    /**
     * Cache le modal
     */
    hideModal() {
        const overlay = document.getElementById('hitl-overlay');
        overlay.classList.remove('visible');
        this.currentCheckpoint = null;

        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    /**
     * Demarre le timer
     */
    _startTimer(checkpoint) {
        const timerEl = document.getElementById('hitl-timer');
        if (!timerEl) return;

        const updateTimer = () => {
            const remaining = checkpoint.expiresAt - Date.now();
            if (remaining <= 0) {
                timerEl.textContent = 'EXPIRE';
                timerEl.style.color = '#FF6B6B';
                clearInterval(this.timerInterval);
                return;
            }

            const minutes = Math.floor(remaining / 60000);
            const seconds = Math.floor((remaining % 60000) / 1000);
            timerEl.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        };

        updateTimer();
        this.timerInterval = setInterval(updateTimer, 1000);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ACTIONS
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Approuve le checkpoint courant
     */
    approve() {
        if (!this.currentCheckpoint || !this.checkpointManager) return;

        const notes = document.getElementById('hitl-notes')?.value || '';
        this.checkpointManager.approveCheckpoint(
            this.currentCheckpoint.id,
            'user',
            notes
        );

        this.showToast('success', 'Approuve', 'L\'action a ete autorisee');
        this.hideModal();
    }

    /**
     * Rejette le checkpoint courant
     */
    reject() {
        if (!this.currentCheckpoint || !this.checkpointManager) return;

        const notes = document.getElementById('hitl-notes')?.value || '';
        this.checkpointManager.rejectCheckpoint(
            this.currentCheckpoint.id,
            'user',
            notes
        );

        this.showToast('warning', 'Rejete', 'L\'action a ete bloquee');
        this.hideModal();
    }

    /**
     * Escalade le checkpoint courant
     */
    escalate() {
        if (!this.currentCheckpoint || !this.checkpointManager) return;

        const notes = document.getElementById('hitl-notes')?.value || '';
        this.checkpointManager.escalateCheckpoint(
            this.currentCheckpoint.id,
            'admin',
            notes
        );

        this.showToast('warning', 'Escalade', 'Transfere au niveau superieur');
        this.hideModal();
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // TOASTS
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Affiche un toast
     */
    showToast(type, title, message, action = null) {
        const container = document.getElementById('hitl-toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `hitl-toast ${type}`;

        const icon = type === 'success' ? '✅' :
            type === 'warning' ? '⚠️' :
                type === 'critical' ? '🚨' : 'ℹ️';

        toast.innerHTML = `
            <span class="hitl-toast-icon">${icon}</span>
            <div class="hitl-toast-content">
                <div class="hitl-toast-title">${title}</div>
                <div class="hitl-toast-message">${message}</div>
            </div>
            ${action ? `<button class="hitl-toast-action" onclick="${action.onclick}">${action.label}</button>` : ''}
        `;

        container.appendChild(toast);

        // Animation entree
        setTimeout(() => toast.classList.add('visible'), 10);

        // Auto-remove
        setTimeout(() => {
            toast.classList.remove('visible');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    /**
     * Notification de checkpoint en attente
     */
    notifyPending(checkpoint) {
        this.showToast('critical', 'Approbation Requise', `Action "${checkpoint.action?.name}" en attente`, {
            label: 'Voir',
            onclick: `window.hitlUI.showApprovalModal(window.getATOMCheckpointManager().getCheckpoint('${checkpoint.id}'))`
        });
        this._updatePendingBadge();
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // PENDING BADGE
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Met a jour le badge pending
     */
    _updatePendingBadge() {
        const badge = document.getElementById('hitl-pending-badge');
        if (!badge || !this.checkpointManager) return;

        const pending = this.checkpointManager.getPending();
        if (pending.length > 0) {
            badge.textContent = pending.length > 9 ? '9+' : pending.length;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }

    /**
     * Affiche la liste des checkpoints en attente
     */
    _showPendingList() {
        if (!this.checkpointManager) return;

        const pending = this.checkpointManager.getPending();
        if (pending.length === 0) return;

        // Affiche le premier en attente
        this.showApprovalModal(pending[0]);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CALLBACKS
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Callback quand un checkpoint est resolu
     */
    _onResolved(checkpoint, resolution) {
        this._updatePendingBadge();

        if (resolution === 'timeout') {
            this.showToast('warning', 'Checkpoint Expire', `Action "${checkpoint.action?.name}" a expire`);
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════════

let hitlUIInstance = null;

function initHITLUI(checkpointManager = null) {
    if (!checkpointManager && typeof getATOMCheckpointManager !== 'undefined') {
        checkpointManager = getATOMCheckpointManager();
    }

    hitlUIInstance = new HITLUI(checkpointManager);
    window.hitlUI = hitlUIInstance;

    return hitlUIInstance;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { HITLUI, initHITLUI };
}

if (typeof window !== 'undefined') {
    window.HITLUI = HITLUI;
    window.initHITLUI = initHITLUI;
}

console.log('%c[AT-OM] HITL UI loaded - Human approval interface ready', 'color: #9333EA;');
