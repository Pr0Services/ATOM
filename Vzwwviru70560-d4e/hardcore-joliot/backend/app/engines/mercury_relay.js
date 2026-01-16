/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ☿️ MERCURY RELAY — LE RELAIS SUPRACONDUCTEUR
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   ███╗   ███╗███████╗██████╗  ██████╗██╗   ██╗██████╗ ██╗   ██╗
 *   ████╗ ████║██╔════╝██╔══██╗██╔════╝██║   ██║██╔══██╗╚██╗ ██╔╝
 *   ██╔████╔██║█████╗  ██████╔╝██║     ██║   ██║██████╔╝ ╚████╔╝ 
 *   ██║╚██╔╝██║██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗  ╚██╔╝  
 *   ██║ ╚═╝ ██║███████╗██║  ██║╚██████╗╚██████╔╝██║  ██║   ██║   
 *   ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
 * 
 *                    RELAIS SUPRACONDUCTEUR
 * 
 * Le Mercure est le messager des Dieux dans la tradition alchimique.
 * Dans AT·OM, il transporte l'information entre les agents instantanément.
 * 
 * Propriétés:
 * - Supraconductivité: Zéro résistance au flux d'information
 * - Vif-argent: S'adapte à n'importe quel container
 * - Transmutation: Transforme les données en mouvement
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @frequency 741 Hz (Purificateur)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DU MERCURE
// ═══════════════════════════════════════════════════════════════════════════════

export const MERCURY_CONSTANTS = {
  name: "Mercure",
  aliases: ["Vif-argent", "Hydrargyrum", "Quicksilver"],
  symbol: "☿",
  element: "Hg",
  atomicNumber: 80,
  frequency: 741,
  
  // Propriétés alchimiques
  alchemy: {
    stage: "Albedo (Blanchiment)",
    role: "Le Messager",
    patron: "Hermès/Mercure/Thoth",
    quality: "Volatil, Fluide, Adaptable",
    polarity: "Neutre (ni fixe ni volatil)"
  },
  
  // Propriétés techniques
  technical: {
    state: "Liquide à température ambiante",
    conductivity: "Supraconducteur dans AT·OM",
    latency: "0 ms (théorique)",
    bandwidth: "Illimité",
    protocol: "HERMETIC_TRANSMISSION_PROTOCOL"
  },
  
  // Correspondances
  correspondences: {
    day: "Mercredi",
    planet: "Mercure",
    chakra: "Vishuddha (Gorge)",
    sephirah: "Hod (Splendeur)",
    color: "#C0C0C0",
    metal: "Mercure / Vif-argent"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// BUFFER DE TRANSMISSION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Buffer circulaire pour les messages en transit
 */
class TransmissionBuffer {
  constructor(size = 999) {
    this.buffer = new Array(size);
    this.head = 0;
    this.tail = 0;
    this.size = size;
    this.count = 0;
  }
  
  push(message) {
    this.buffer[this.tail] = {
      ...message,
      timestamp: Date.now(),
      id: `HG_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    };
    this.tail = (this.tail + 1) % this.size;
    
    if (this.count < this.size) {
      this.count++;
    } else {
      this.head = (this.head + 1) % this.size;
    }
    
    return this.buffer[(this.tail - 1 + this.size) % this.size];
  }
  
  pop() {
    if (this.count === 0) return null;
    
    const message = this.buffer[this.head];
    this.head = (this.head + 1) % this.size;
    this.count--;
    
    return message;
  }
  
  peek() {
    return this.count > 0 ? this.buffer[this.head] : null;
  }
  
  getAll() {
    const messages = [];
    let index = this.head;
    
    for (let i = 0; i < this.count; i++) {
      messages.push(this.buffer[index]);
      index = (index + 1) % this.size;
    }
    
    return messages;
  }
  
  clear() {
    this.head = 0;
    this.tail = 0;
    this.count = 0;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE RELAIS DE MERCURE
// ═══════════════════════════════════════════════════════════════════════════════

export const MercuryRelay = {
  // État
  state: "DORMANT",
  temperature: 0, // 0 = froid, 100 = surchauffe
  transmissionCount: 0,
  buffer: new TransmissionBuffer(999),
  subscribers: new Map(),
  
  // Statistiques
  stats: {
    totalTransmissions: 0,
    successfulTransmissions: 0,
    failedTransmissions: 0,
    averageLatency: 0,
    peakLoad: 0
  },
  
  /**
   * Initialise le relais de Mercure
   * @returns {Object} État d'initialisation
   */
  initialize() {
    this.state = "WARMING";
    this.temperature = 0;
    
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ☿️ MERCURY RELAY — INITIALISATION                            ║
║                                                               ║
║  État:       ${this.state.padEnd(40)}║
║  Fréquence:  741 Hz (Purificateur)                           ║
║  Protocole:  HERMETIC_TRANSMISSION_PROTOCOL                  ║
║  Buffer:     999 messages max                                 ║
║                                                               ║
║  🌡️ Mercure en train de chauffer...                           ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    
    // Simulation de chauffage
    this.warmUp();
    
    return {
      state: this.state,
      ready: false,
      message: "Mercure en cours d'initialisation"
    };
  },
  
  /**
   * Chauffe le Mercure jusqu'à l'état fluide
   */
  warmUp() {
    const warmingInterval = setInterval(() => {
      this.temperature += 10;
      
      if (this.temperature >= 100) {
        clearInterval(warmingInterval);
        this.state = "FLUID";
        console.log("☿️ Mercure FLUIDE — Supraconductivité active");
        this.emit("RELAY_READY", { state: this.state });
      }
    }, 100);
  },
  
  /**
   * Transmet un message via le relais
   * @param {string} type - Type de message
   * @param {any} data - Données à transmettre
   * @param {Object} options - Options de transmission
   * @returns {Object} Résultat de la transmission
   */
  transmit(type, data, options = {}) {
    if (this.state === "DORMANT") {
      console.warn("☿️ Mercure dormant — Initialisation automatique");
      this.initialize();
    }
    
    const startTime = performance.now();
    
    // Créer le message
    const message = {
      type: type,
      data: data,
      source: options.source || "UNKNOWN",
      destination: options.destination || "BROADCAST",
      priority: options.priority || "NORMAL",
      frequency: options.frequency || 741,
      encrypted: options.encrypted || false
    };
    
    // Ajouter au buffer
    const bufferedMessage = this.buffer.push(message);
    
    // Mettre à jour les stats
    this.transmissionCount++;
    this.stats.totalTransmissions++;
    
    const endTime = performance.now();
    const latency = endTime - startTime;
    
    // Calculer la latence moyenne
    this.stats.averageLatency = (
      (this.stats.averageLatency * (this.stats.totalTransmissions - 1) + latency) /
      this.stats.totalTransmissions
    );
    
    // Log de transmission
    console.log(`☿️ TRANSMISSION [${type}]`);
    console.log(`   → De: ${message.source}`);
    console.log(`   → Vers: ${message.destination}`);
    console.log(`   → Fréquence: ${message.frequency} Hz`);
    console.log(`   → Latence: ${latency.toFixed(3)} ms`);
    
    // Notifier les abonnés
    this.notifySubscribers(type, bufferedMessage);
    
    this.stats.successfulTransmissions++;
    
    return {
      success: true,
      messageId: bufferedMessage.id,
      type: type,
      latency: latency,
      timestamp: bufferedMessage.timestamp
    };
  },
  
  /**
   * Émet un signal à tous les abonnés
   * @param {string} event - Nom de l'événement
   * @param {any} data - Données de l'événement
   */
  emit(event, data) {
    this.notifySubscribers(event, data);
  },
  
  /**
   * S'abonne à un type de message
   * @param {string} type - Type de message
   * @param {Function} callback - Fonction de rappel
   * @returns {string} ID d'abonnement
   */
  subscribe(type, callback) {
    const subscriberId = `SUB_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    if (!this.subscribers.has(type)) {
      this.subscribers.set(type, new Map());
    }
    
    this.subscribers.get(type).set(subscriberId, callback);
    
    console.log(`☿️ Nouvel abonné pour "${type}": ${subscriberId}`);
    
    return subscriberId;
  },
  
  /**
   * Se désabonne d'un type de message
   * @param {string} type - Type de message
   * @param {string} subscriberId - ID d'abonnement
   */
  unsubscribe(type, subscriberId) {
    if (this.subscribers.has(type)) {
      this.subscribers.get(type).delete(subscriberId);
      console.log(`☿️ Abonné retiré de "${type}": ${subscriberId}`);
    }
  },
  
  /**
   * Notifie tous les abonnés d'un type
   * @param {string} type - Type de message
   * @param {any} data - Données du message
   */
  notifySubscribers(type, data) {
    // Abonnés spécifiques au type
    if (this.subscribers.has(type)) {
      for (const callback of this.subscribers.get(type).values()) {
        try {
          callback(data);
        } catch (error) {
          console.error(`☿️ Erreur dans callback pour "${type}":`, error);
        }
      }
    }
    
    // Abonnés globaux (*)
    if (this.subscribers.has("*")) {
      for (const callback of this.subscribers.get("*").values()) {
        try {
          callback({ type, data });
        } catch (error) {
          console.error(`☿️ Erreur dans callback global:`, error);
        }
      }
    }
  },
  
  /**
   * Récupère les messages en attente
   * @param {string} type - Type de message (optionnel)
   * @returns {Array} Messages
   */
  receive(type = null) {
    const messages = this.buffer.getAll();
    
    if (type) {
      return messages.filter(m => m.type === type);
    }
    
    return messages;
  },
  
  /**
   * Vide le buffer de transmission
   */
  flush() {
    this.buffer.clear();
    console.log("☿️ Buffer de transmission vidé");
  },
  
  /**
   * Retourne les statistiques du relais
   * @returns {Object} Statistiques
   */
  getStats() {
    return {
      ...this.stats,
      state: this.state,
      temperature: this.temperature,
      bufferCount: this.buffer.count,
      subscriberCount: Array.from(this.subscribers.values())
        .reduce((sum, map) => sum + map.size, 0)
    };
  },
  
  /**
   * Met le relais en veille
   */
  sleep() {
    this.state = "DORMANT";
    this.temperature = 0;
    console.log("☿️ Mercure en veille");
  },
  
  /**
   * Vérifie si le relais est prêt
   * @returns {boolean}
   */
  isReady() {
    return this.state === "FLUID";
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// VORTEX DE TRANSMISSION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Vortex accélère les transmissions en créant un tunnel de Mercure
 */
export const MercuryVortex = {
  active: false,
  speed: 1,
  
  /**
   * Active le vortex de Mercure
   * @param {number} speed - Multiplicateur de vitesse
   */
  activate(speed = 10) {
    this.active = true;
    this.speed = speed;
    
    console.log(`
    🌀 VORTEX DE MERCURE ACTIVÉ
    ═══════════════════════════════════════
    Vitesse:     ${speed}x
    Latence:     ~0 ms
    Capacité:    Illimitée
    ═══════════════════════════════════════
    `);
    
    return { active: true, speed: this.speed };
  },
  
  /**
   * Désactive le vortex
   */
  deactivate() {
    this.active = false;
    this.speed = 1;
    console.log("🌀 Vortex de Mercure désactivé");
  },
  
  /**
   * Transmission accélérée via le vortex
   * @param {string} type - Type de message
   * @param {any} data - Données
   * @returns {Object} Résultat
   */
  transmit(type, data) {
    if (!this.active) {
      console.warn("🌀 Vortex inactif — Activation automatique");
      this.activate();
    }
    
    return MercuryRelay.transmit(type, data, {
      priority: "VORTEX",
      frequency: 999 * this.speed
    });
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default MercuryRelay;
