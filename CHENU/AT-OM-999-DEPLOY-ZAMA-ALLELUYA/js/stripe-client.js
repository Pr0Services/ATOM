/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM STRIPE CLIENT - CHE·NU™ V76
 * Intégration Paiements pour le Funder Portal
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Fonctionnalités:
 * - Checkout pour abonnements Funder
 * - Donations ponctuelles
 * - Gestion des plans (Citoyen, Collaborateur, Souverain)
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION STRIPE
// ═══════════════════════════════════════════════════════════════════════════════

const STRIPE_CONFIG = {
    publishableKey: 'pk_live_51St8CGBDYsAvhcuq2kRzqcm14rokBDDw5RYGG1xmT4zoHJr2gGUWyUbKsTEFXikOIPcSZt0Rds3SvN5OtkFX2a0T00MgxWuQej',

    // Plans Funder - 5 Niveaux (à créer dans Stripe Dashboard)
    // Citoyen (0$) -> Funder (44.40$) -> Argent (99$) -> Or (369$) -> Diamant (999$)
    plans: {
        citoyen: {
            name: 'Citoyen',
            emoji: '🌱',
            tagline: 'Bienvenue dans l\'Arche',
            description: 'Tu fais tes premiers pas vers la souveraineté. L\'Arche t\'accueille à bras ouverts.',
            frequency: 444,
            frequencyMeaning: 'Heartbeat - La fréquence du cœur',
            color: '#00FF88',
            features: [
                'Accès forum communautaire',
                'Vote sur les besoins locaux',
                'Calcul Arithmos illimité',
                'Connexion avec Nova, Aria et Orion'
            ],
            price: 0,
            priceId: 'price_1SvhPBBDYsAvhcuqTsSbCztu',
            cta: 'Rejoindre gratuitement'
        },
        funder: {
            name: 'Funder',
            emoji: '🔥',
            tagline: 'Soutien à l\'Arche',
            description: 'Tu soutiens activement le développement de l\'Arche et obtiens des avantages exclusifs.',
            frequency: 528,
            frequencyMeaning: 'Love - La fréquence de transformation',
            color: '#FF6B35',
            features: [
                'Tout Citoyen +',
                'Badge Funder distinctif',
                'Accès prioritaire aux nouveautés',
                'Support communautaire dédié'
            ],
            price: 44.40,
            priceId: 'price_1SvgdxBDYsAvhcuqD8yZ5EY1',
            cta: 'Devenir Funder'
        },
        argent: {
            name: 'Argent',
            emoji: '🥈',
            tagline: 'Explorateur avancé',
            description: 'Tu accèdes à la vue Civilisation complète avec 50 agents spécialisés.',
            frequency: 639,
            frequencyMeaning: 'Connection - La fréquence des relations',
            color: '#C0C0C0',
            features: [
                'Tout Funder +',
                'Vue Civil complète',
                '50 Agents accessibles',
                'Badge Argent'
            ],
            price: 99,
            priceId: 'price_1SvgemBDYsAvhcuq2WBcZDXo',
            cta: 'Passer Argent'
        },
        or: {
            name: 'Or',
            emoji: '🥇',
            tagline: 'Co-créateur Tesla',
            description: 'Tu accèdes à la vision duale (Civil + Mythique) avec 200 agents et l\'API.',
            frequency: 741,
            frequencyMeaning: 'Awakening - La fréquence de l\'éveil',
            color: '#FFD700',
            features: [
                'Tout Argent +',
                'Vue Duale (Civil + Mythique)',
                '200 Agents accessibles',
                'Accès API complet',
                'Badge Or'
            ],
            price: 369,
            priceId: 'price_1SvhNWBDYsAvhcuqKHPexnzV',
            cta: 'Passer Or'
        },
        diamant: {
            name: 'Diamant',
            emoji: '💎',
            tagline: 'Gardien Souverain',
            description: 'Tu incarnes la vision complète. Accès au Sanctuaire et NFT Souverain.',
            frequency: 999,
            frequencyMeaning: 'Source - La fréquence de l\'accomplissement',
            color: '#9333EA',
            features: [
                'Tout Or +',
                'Accès illimité',
                '400+ Agents',
                'XR/VR complet',
                'NFT Souverain (Hedera)',
                'Sanctuaire des Fondateurs'
            ],
            price: 999,
            priceId: 'price_1SvhQCBDYsAvhcuqr0Km0slq',
            cta: 'Devenir Souverain'
        }
    },

    // Donations
    donationAmounts: [9, 44, 99, 369, 444, 999],

    // URLs de redirection
    successUrl: window.location.origin + '/funder.html?success=true',
    cancelUrl: window.location.origin + '/funder.html?canceled=true'
};

// ═══════════════════════════════════════════════════════════════════════════════
// STRIPE LOADER
// ═══════════════════════════════════════════════════════════════════════════════

let stripeInstance = null;
let stripeLoaded = false;

/**
 * Charger le SDK Stripe
 */
function loadStripeSDK() {
    return new Promise((resolve, reject) => {
        if (stripeLoaded && stripeInstance) {
            resolve(stripeInstance);
            return;
        }

        // Vérifier si déjà chargé
        if (window.Stripe) {
            stripeInstance = window.Stripe(STRIPE_CONFIG.publishableKey);
            stripeLoaded = true;
            resolve(stripeInstance);
            return;
        }

        // Charger le script
        const script = document.createElement('script');
        script.src = 'https://js.stripe.com/v3/';
        script.async = true;

        script.onload = () => {
            stripeInstance = window.Stripe(STRIPE_CONFIG.publishableKey);
            stripeLoaded = true;
            console.log('%c[Stripe] SDK loaded successfully', 'color: #00FF88;');
            resolve(stripeInstance);
        };

        script.onerror = () => {
            console.error('[Stripe] Failed to load SDK');
            reject(new Error('Failed to load Stripe SDK'));
        };

        document.head.appendChild(script);
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKOUT FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Créer une session de checkout pour un plan
 * Note: Nécessite un backend pour créer la session
 * Pour l'instant, utilise Stripe Payment Links
 */
async function checkoutPlan(planId) {
    const plan = STRIPE_CONFIG.plans[planId];

    if (!plan) {
        console.error('[Stripe] Plan not found:', planId);
        return { success: false, error: 'Plan not found' };
    }

    if (plan.price === 0) {
        // Plan gratuit - pas de paiement nécessaire
        console.log('[Stripe] Free plan selected:', planId);
        return { success: true, free: true, plan: plan };
    }

    if (!plan.priceId) {
        // Price ID non configuré - afficher message
        console.warn('[Stripe] Price ID not configured for plan:', planId);
        showStripeModal(plan);
        return { success: false, error: 'Price not configured' };
    }

    try {
        const stripe = await loadStripeSDK();

        // Rediriger vers Checkout
        const { error } = await stripe.redirectToCheckout({
            lineItems: [{ price: plan.priceId, quantity: 1 }],
            mode: 'subscription',
            successUrl: STRIPE_CONFIG.successUrl,
            cancelUrl: STRIPE_CONFIG.cancelUrl
        });

        if (error) {
            console.error('[Stripe] Checkout error:', error);
            return { success: false, error: error.message };
        }

        return { success: true };
    } catch (err) {
        console.error('[Stripe] Error:', err);
        return { success: false, error: err.message };
    }
}

/**
 * Créer une donation ponctuelle
 */
async function createDonation(amount) {
    if (!STRIPE_CONFIG.donationAmounts.includes(amount)) {
        // Montant personnalisé accepté
    }

    try {
        const stripe = await loadStripeSDK();

        // Pour les donations, on utilise Payment Links ou un backend
        // Ici on affiche le modal avec instructions
        showDonationModal(amount);

        return { success: true, amount: amount };
    } catch (err) {
        console.error('[Stripe] Donation error:', err);
        return { success: false, error: err.message };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Afficher modal Stripe (temporaire avant backend)
 */
function showStripeModal(plan) {
    const modal = document.createElement('div');
    modal.className = 'stripe-modal-overlay';
    modal.innerHTML = `
        <div class="stripe-modal">
            <div class="stripe-modal-header">
                <span style="font-size: 2rem;">${plan.emoji || '💎'}</span>
                <h2>Plan ${plan.name}</h2>
                <button class="stripe-modal-close" onclick="this.closest('.stripe-modal-overlay').remove()">×</button>
            </div>
            <div class="stripe-modal-body">
                <p class="stripe-tagline">${plan.tagline || ''}</p>
                <p class="stripe-description">${plan.description || ''}</p>
                <p class="stripe-price">$${plan.price.toFixed(2)} <span>/mois</span></p>
                <p class="stripe-freq">${plan.frequency} Hz - ${plan.frequencyMeaning || ''}</p>
                <ul class="stripe-features">
                    ${plan.features.map(f => `<li>✓ ${f}</li>`).join('')}
                </ul>
                <div class="stripe-notice">
                    <p>🚧 Configuration en cours</p>
                    <p>Les paiements seront disponibles très bientôt.</p>
                    <p>Contacte <strong>contact@at-om.ai</strong> pour un accès anticipé.</p>
                </div>
            </div>
            <div class="stripe-modal-footer">
                <button class="stripe-btn-secondary" onclick="this.closest('.stripe-modal-overlay').remove()">Fermer</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    // Animation
    requestAnimationFrame(() => modal.classList.add('visible'));
}

/**
 * Afficher modal donation
 */
function showDonationModal(amount) {
    const modal = document.createElement('div');
    modal.className = 'stripe-modal-overlay';
    modal.innerHTML = `
        <div class="stripe-modal">
            <div class="stripe-modal-header">
                <span style="font-size: 2rem;">🙏</span>
                <h2>Donation $${amount}</h2>
                <button class="stripe-modal-close" onclick="this.closest('.stripe-modal-overlay').remove()">×</button>
            </div>
            <div class="stripe-modal-body">
                <p class="stripe-freq">Merci pour ton soutien à ${amount} Hz!</p>
                <div class="stripe-notice">
                    <p>🚧 Système de donation en préparation</p>
                    <p>Pour faire une donation maintenant, contacte:</p>
                    <p><strong>contact@at-om.ai</strong></p>
                </div>
            </div>
            <div class="stripe-modal-footer">
                <button class="stripe-btn-secondary" onclick="this.closest('.stripe-modal-overlay').remove()">Fermer</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    requestAnimationFrame(() => modal.classList.add('visible'));
}

/**
 * Injecter les styles CSS
 */
function injectStripeStyles() {
    if (document.getElementById('stripe-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'stripe-styles';
    styles.textContent = `
        .stripe-modal-overlay {
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
            transition: opacity 0.3s ease;
        }
        .stripe-modal-overlay.visible {
            opacity: 1;
        }
        .stripe-modal {
            background: linear-gradient(135deg, #1a1a2e, #0a0a0f);
            border: 2px solid #D4AF37;
            border-radius: 16px;
            max-width: 450px;
            width: 90%;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        .stripe-modal-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px;
            background: rgba(212, 175, 55, 0.1);
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        }
        .stripe-modal-header h2 {
            flex: 1;
            margin: 0;
            color: #D4AF37;
            font-size: 1.25rem;
        }
        .stripe-modal-close {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stripe-modal-close:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        .stripe-modal-body {
            padding: 24px;
            color: white;
        }
        .stripe-price {
            font-size: 2.5rem;
            font-weight: bold;
            color: #D4AF37;
            margin: 0 0 8px 0;
        }
        .stripe-price span {
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.5);
        }
        .stripe-tagline {
            font-size: 1.1rem;
            font-weight: bold;
            color: #D4AF37;
            margin-bottom: 12px;
            font-style: italic;
        }
        .stripe-description {
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: left;
        }
        .stripe-freq {
            color: #00FF88;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        .stripe-features {
            list-style: none;
            padding: 0;
            margin: 0 0 20px 0;
        }
        .stripe-features li {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.8);
        }
        .stripe-features li:last-child {
            border-bottom: none;
        }
        .stripe-notice {
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        .stripe-notice p {
            margin: 8px 0;
            color: rgba(255, 255, 255, 0.7);
        }
        .stripe-modal-footer {
            padding: 16px 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            gap: 12px;
            justify-content: flex-end;
        }
        .stripe-btn-primary {
            padding: 12px 24px;
            background: linear-gradient(135deg, #D4AF37, #aa8a2e);
            border: none;
            border-radius: 8px;
            color: black;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .stripe-btn-primary:hover {
            transform: translateY(-2px);
        }
        .stripe-btn-secondary {
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            cursor: pointer;
            transition: all 0.2s;
        }
        .stripe-btn-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    `;
    document.head.appendChild(styles);
}

// ═══════════════════════════════════════════════════════════════════════════════
// PLAN CARDS GENERATOR
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Générer les cartes de plans pour le Funder Portal
 */
function generatePlanCards(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const plans = Object.entries(STRIPE_CONFIG.plans);

    container.innerHTML = plans.map(([id, plan]) => `
        <div class="plan-card" style="--plan-color: ${plan.color}">
            <div class="plan-header">
                <div class="plan-emoji">${plan.emoji || '💎'}</div>
                <div class="plan-freq">${plan.frequency} Hz</div>
                <h3 class="plan-name">${plan.name}</h3>
                <p class="plan-tagline">${plan.tagline || ''}</p>
            </div>
            <div class="plan-price">
                ${plan.price === 0
                    ? '<span class="price-free">Gratuit</span>'
                    : `<span class="price-amount">$${plan.price.toFixed(2)}</span><span class="price-period">/mois</span>`
                }
            </div>
            <p class="plan-freq-meaning">${plan.frequencyMeaning || ''}</p>
            <p class="plan-desc">${plan.description}</p>
            <ul class="plan-features">
                ${plan.features.map(f => `<li>✓ ${f}</li>`).join('')}
            </ul>
            <button class="plan-btn" onclick="selectPlan('${id}')">
                ${plan.cta || (plan.price === 0 ? 'Commencer' : 'Choisir ce plan')}
            </button>
        </div>
    `).join('');
}

/**
 * Sélectionner un plan
 */
async function selectPlan(planId) {
    console.log('[Stripe] Plan selected:', planId);

    // Vérifier gouvernance si disponible
    if (typeof window.executeWithGovernance === 'function') {
        const action = {
            type: 'subscription',
            operation: 'checkout',
            target: planId,
            estimatedImpact: 0.8
        };

        await window.executeWithGovernance(action, () => {
            checkoutPlan(planId);
        });
    } else {
        checkoutPlan(planId);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Initialiser le client Stripe
 */
function initStripeClient() {
    injectStripeStyles();

    // Précharger le SDK
    loadStripeSDK().catch(() => {
        console.warn('[Stripe] SDK preload failed, will retry on demand');
    });

    console.log('%c[Stripe] Client initialized', 'color: #D4AF37;');
    console.log('%c[Stripe] Plans: Citoyen (Free) | Collaborateur ($44.40) | Souverain ($99.90)', 'color: #00FF88;');

    return {
        checkout: checkoutPlan,
        donate: createDonation,
        generateCards: generatePlanCards,
        config: STRIPE_CONFIG
    };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof window !== 'undefined') {
    window.STRIPE_CONFIG = STRIPE_CONFIG;
    window.initStripeClient = initStripeClient;
    window.checkoutPlan = checkoutPlan;
    window.createDonation = createDonation;
    window.selectPlan = selectPlan;
    window.generatePlanCards = generatePlanCards;

    // Auto-init
    document.addEventListener('DOMContentLoaded', () => {
        initStripeClient();
    });
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        STRIPE_CONFIG,
        initStripeClient,
        checkoutPlan,
        createDonation
    };
}
