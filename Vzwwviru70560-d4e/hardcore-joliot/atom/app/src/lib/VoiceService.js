/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
 *      ██║   ██║██╔═══██╗██║██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
 *      ██║   ██║██║   ██║██║██║     █████╗      ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
 *      ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
 *       ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
 *        ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝
 *
 *                              🎤 SERVICE VOCAL COMPLET CHE·NU 🎤
 *                   Reconnaissance vocale + Synthèse vocale + Commandes vocales
 *
 *   FONCTIONNALITÉS:
 *   ├── Speech Recognition (Web Speech API)
 *   ├── Speech Synthesis (TTS)
 *   ├── Voice Commands
 *   ├── Multi-language support
 *   └── Audio Visualization
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const VOICE_CONFIG = {
  recognition: {
    lang: 'fr-FR',
    continuous: false,
    interimResults: true,
    maxAlternatives: 3
  },
  synthesis: {
    lang: 'fr-FR',
    rate: 1.0,
    pitch: 1.0,
    volume: 1.0
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: RECONNAISSANCE VOCALE
// ═══════════════════════════════════════════════════════════════════════════════

export class SpeechRecognitionService {
  constructor() {
    this.recognition = null;
    this.isListening = false;
    this.isSupported = false;
    this.callbacks = {
      onResult: null,
      onInterim: null,
      onStart: null,
      onEnd: null,
      onError: null
    };

    this.initialize();
  }

  initialize() {
    // Vérifier le support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.warn('[VoiceService] Speech Recognition not supported');
      this.isSupported = false;
      return;
    }

    this.isSupported = true;
    this.recognition = new SpeechRecognition();

    // Configuration
    this.recognition.lang = VOICE_CONFIG.recognition.lang;
    this.recognition.continuous = VOICE_CONFIG.recognition.continuous;
    this.recognition.interimResults = VOICE_CONFIG.recognition.interimResults;
    this.recognition.maxAlternatives = VOICE_CONFIG.recognition.maxAlternatives;

    // Event handlers
    this.recognition.onstart = () => {
      this.isListening = true;
      console.log('[VoiceService] Recognition started');
      this.callbacks.onStart?.();
    };

    this.recognition.onend = () => {
      this.isListening = false;
      console.log('[VoiceService] Recognition ended');
      this.callbacks.onEnd?.();
    };

    this.recognition.onresult = (event) => {
      const results = [];
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        const transcript = result[0].transcript;
        const confidence = result[0].confidence;

        if (result.isFinal) {
          finalTranscript += transcript;
          results.push({ transcript, confidence, isFinal: true });
        } else {
          interimTranscript += transcript;
          this.callbacks.onInterim?.(interimTranscript);
        }
      }

      if (finalTranscript) {
        console.log('[VoiceService] Final result:', finalTranscript);
        this.callbacks.onResult?.({
          transcript: finalTranscript.trim(),
          confidence: results[0]?.confidence || 0,
          alternatives: results
        });
      }
    };

    this.recognition.onerror = (event) => {
      console.error('[VoiceService] Recognition error:', event.error);
      this.isListening = false;

      let errorMessage;
      switch (event.error) {
        case 'no-speech':
          errorMessage = 'Aucune parole détectée';
          break;
        case 'audio-capture':
          errorMessage = 'Microphone non disponible';
          break;
        case 'not-allowed':
          errorMessage = 'Permission microphone refusée';
          break;
        case 'network':
          errorMessage = 'Erreur réseau';
          break;
        default:
          errorMessage = `Erreur: ${event.error}`;
      }

      this.callbacks.onError?.({ code: event.error, message: errorMessage });
    };
  }

  // Démarrer l'écoute
  start(options = {}) {
    if (!this.isSupported) {
      console.error('[VoiceService] Speech Recognition not supported');
      return false;
    }

    if (this.isListening) {
      console.warn('[VoiceService] Already listening');
      return false;
    }

    // Appliquer les options
    if (options.lang) this.recognition.lang = options.lang;
    if (options.continuous !== undefined) this.recognition.continuous = options.continuous;

    try {
      this.recognition.start();
      return true;
    } catch (error) {
      console.error('[VoiceService] Failed to start:', error);
      return false;
    }
  }

  // Arrêter l'écoute
  stop() {
    if (!this.isSupported || !this.isListening) return;

    try {
      this.recognition.stop();
    } catch (error) {
      console.error('[VoiceService] Failed to stop:', error);
    }
  }

  // Annuler l'écoute
  abort() {
    if (!this.isSupported) return;

    try {
      this.recognition.abort();
      this.isListening = false;
    } catch (error) {
      console.error('[VoiceService] Failed to abort:', error);
    }
  }

  // Définir les callbacks
  on(event, callback) {
    if (this.callbacks.hasOwnProperty(`on${event.charAt(0).toUpperCase() + event.slice(1)}`)) {
      this.callbacks[`on${event.charAt(0).toUpperCase() + event.slice(1)}`] = callback;
    }
  }

  // Changer la langue
  setLanguage(lang) {
    if (this.recognition) {
      this.recognition.lang = lang;
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: SYNTHÈSE VOCALE
// ═══════════════════════════════════════════════════════════════════════════════

export class SpeechSynthesisService {
  constructor() {
    this.synth = window.speechSynthesis;
    this.voices = [];
    this.isSupported = !!this.synth;
    this.isSpeaking = false;
    this.currentUtterance = null;
    this.queue = [];

    if (this.isSupported) {
      this.loadVoices();
    }
  }

  loadVoices() {
    return new Promise((resolve) => {
      const loadVoicesList = () => {
        this.voices = this.synth.getVoices();
        resolve(this.voices);
      };

      if (this.synth.onvoiceschanged !== undefined) {
        this.synth.onvoiceschanged = loadVoicesList;
      }

      loadVoicesList();
    });
  }

  // Obtenir les voix disponibles
  getVoices(lang = null) {
    if (lang) {
      return this.voices.filter(v => v.lang.startsWith(lang));
    }
    return this.voices;
  }

  // Obtenir une voix par nom
  getVoiceByName(name) {
    return this.voices.find(v => v.name === name);
  }

  // Obtenir les voix françaises
  getFrenchVoices() {
    return this.voices.filter(v => v.lang.startsWith('fr'));
  }

  // Parler
  speak(text, options = {}) {
    return new Promise((resolve, reject) => {
      if (!this.isSupported) {
        reject(new Error('Speech synthesis not supported'));
        return;
      }

      // Annuler si déjà en cours
      if (options.interrupt && this.isSpeaking) {
        this.stop();
      }

      const utterance = new SpeechSynthesisUtterance(text);

      // Configuration
      utterance.lang = options.lang || VOICE_CONFIG.synthesis.lang;
      utterance.rate = options.rate || VOICE_CONFIG.synthesis.rate;
      utterance.pitch = options.pitch || VOICE_CONFIG.synthesis.pitch;
      utterance.volume = options.volume || VOICE_CONFIG.synthesis.volume;

      // Sélectionner la voix
      if (options.voice) {
        const voice = typeof options.voice === 'string'
          ? this.getVoiceByName(options.voice)
          : options.voice;
        if (voice) utterance.voice = voice;
      } else {
        // Voix française par défaut
        const frenchVoice = this.getFrenchVoices()[0];
        if (frenchVoice) utterance.voice = frenchVoice;
      }

      // Events
      utterance.onstart = () => {
        this.isSpeaking = true;
        this.currentUtterance = utterance;
        options.onStart?.();
      };

      utterance.onend = () => {
        this.isSpeaking = false;
        this.currentUtterance = null;
        options.onEnd?.();
        resolve();
      };

      utterance.onerror = (event) => {
        this.isSpeaking = false;
        this.currentUtterance = null;
        options.onError?.(event);
        reject(new Error(`Speech synthesis error: ${event.error}`));
      };

      utterance.onpause = () => options.onPause?.();
      utterance.onresume = () => options.onResume?.();

      // Boundary events pour lip-sync
      utterance.onboundary = (event) => {
        options.onBoundary?.({
          name: event.name,
          charIndex: event.charIndex,
          charLength: event.charLength
        });
      };

      this.synth.speak(utterance);
    });
  }

  // Mettre en pause
  pause() {
    if (this.isSupported && this.isSpeaking) {
      this.synth.pause();
    }
  }

  // Reprendre
  resume() {
    if (this.isSupported) {
      this.synth.resume();
    }
  }

  // Arrêter
  stop() {
    if (this.isSupported) {
      this.synth.cancel();
      this.isSpeaking = false;
      this.currentUtterance = null;
    }
  }

  // Parler avec une file d'attente
  async speakQueue(texts, options = {}) {
    for (const text of texts) {
      await this.speak(text, options);
      if (options.delay) {
        await new Promise(resolve => setTimeout(resolve, options.delay));
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: COMMANDES VOCALES
// ═══════════════════════════════════════════════════════════════════════════════

export class VoiceCommandService {
  constructor(recognitionService) {
    this.recognition = recognitionService;
    this.commands = new Map();
    this.isActive = false;
    this.wakeWord = 'nova';
    this.isAwake = false;
    this.awakeTimeout = null;
    this.awakeDelay = 10000; // 10 secondes

    this.setupRecognition();
  }

  setupRecognition() {
    this.recognition.on('result', (result) => {
      this.processCommand(result.transcript.toLowerCase());
    });
  }

  // Enregistrer une commande
  register(phrase, callback, options = {}) {
    const normalizedPhrase = phrase.toLowerCase().trim();
    this.commands.set(normalizedPhrase, {
      callback,
      aliases: options.aliases || [],
      description: options.description || '',
      requiresWake: options.requiresWake !== false
    });
  }

  // Supprimer une commande
  unregister(phrase) {
    this.commands.delete(phrase.toLowerCase().trim());
  }

  // Traiter une commande
  processCommand(text) {
    console.log('[VoiceCommand] Processing:', text);

    // Vérifier le wake word
    if (text.includes(this.wakeWord)) {
      this.wake();
      // Retirer le wake word du texte
      text = text.replace(this.wakeWord, '').trim();
    }

    // Chercher une commande correspondante
    for (const [phrase, command] of this.commands) {
      // Vérifier si le texte contient la phrase ou un alias
      const allPhrases = [phrase, ...command.aliases];

      for (const p of allPhrases) {
        if (text.includes(p)) {
          // Vérifier si wake word requis
          if (command.requiresWake && !this.isAwake) {
            console.log('[VoiceCommand] Wake word required');
            return;
          }

          // Extraire les arguments (tout ce qui vient après la commande)
          const args = text.replace(p, '').trim();

          console.log('[VoiceCommand] Executing:', phrase, 'with args:', args);
          command.callback(args, text);
          return;
        }
      }
    }

    console.log('[VoiceCommand] No matching command found');
  }

  // Activer avec wake word
  wake() {
    this.isAwake = true;
    console.log('[VoiceCommand] Woke up!');

    // Reset le timeout
    if (this.awakeTimeout) {
      clearTimeout(this.awakeTimeout);
    }

    this.awakeTimeout = setTimeout(() => {
      this.sleep();
    }, this.awakeDelay);
  }

  // Désactiver
  sleep() {
    this.isAwake = false;
    console.log('[VoiceCommand] Going to sleep');
    if (this.awakeTimeout) {
      clearTimeout(this.awakeTimeout);
      this.awakeTimeout = null;
    }
  }

  // Démarrer l'écoute des commandes
  start() {
    this.isActive = true;
    this.recognition.start({ continuous: true });
  }

  // Arrêter l'écoute
  stop() {
    this.isActive = false;
    this.recognition.stop();
    this.sleep();
  }

  // Lister les commandes
  listCommands() {
    return Array.from(this.commands.entries()).map(([phrase, cmd]) => ({
      phrase,
      aliases: cmd.aliases,
      description: cmd.description,
      requiresWake: cmd.requiresWake
    }));
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: VISUALISATION AUDIO
// ═══════════════════════════════════════════════════════════════════════════════

export class AudioVisualizer {
  constructor() {
    this.audioContext = null;
    this.analyser = null;
    this.source = null;
    this.dataArray = null;
    this.isActive = false;
    this.animationId = null;
  }

  async initialize() {
    try {
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);

      // Obtenir le flux microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.source = this.audioContext.createMediaStreamSource(stream);
      this.source.connect(this.analyser);

      console.log('[AudioVisualizer] Initialized');
      return true;
    } catch (error) {
      console.error('[AudioVisualizer] Failed to initialize:', error);
      return false;
    }
  }

  // Obtenir les données de fréquence
  getFrequencyData() {
    if (!this.analyser) return null;
    this.analyser.getByteFrequencyData(this.dataArray);
    return this.dataArray;
  }

  // Obtenir le niveau audio moyen
  getAverageLevel() {
    const data = this.getFrequencyData();
    if (!data) return 0;
    const sum = data.reduce((a, b) => a + b, 0);
    return sum / data.length;
  }

  // Démarrer la visualisation
  start(callback) {
    if (!this.analyser) return;

    this.isActive = true;

    const animate = () => {
      if (!this.isActive) return;

      const frequencyData = this.getFrequencyData();
      const averageLevel = this.getAverageLevel();

      callback({
        frequencyData: Array.from(frequencyData),
        averageLevel,
        timestamp: Date.now()
      });

      this.animationId = requestAnimationFrame(animate);
    };

    animate();
  }

  // Arrêter la visualisation
  stop() {
    this.isActive = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  // Nettoyer
  dispose() {
    this.stop();
    if (this.source) {
      this.source.disconnect();
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVICE VOCAL UNIFIÉ
// ═══════════════════════════════════════════════════════════════════════════════

class VoiceService {
  constructor() {
    this.recognition = new SpeechRecognitionService();
    this.synthesis = new SpeechSynthesisService();
    this.commands = new VoiceCommandService(this.recognition);
    this.visualizer = new AudioVisualizer();

    this.isSupported = {
      recognition: this.recognition.isSupported,
      synthesis: this.synthesis.isSupported
    };

    this.registerDefaultCommands();
  }

  // Commandes par défaut
  registerDefaultCommands() {
    // Navigation
    this.commands.register('aller à', (args) => {
      const routes = {
        'accueil': '/',
        'tableau de bord': '/tableau-de-bord',
        'admin': '/admin',
        'entrée': '/entree'
      };
      const route = routes[args];
      if (route) {
        window.location.href = route;
      }
    }, { description: 'Naviguer vers une page', aliases: ['ouvre', 'montre'] });

    // Agents
    this.commands.register('parle à', (args) => {
      const agents = ['nova', 'aria', 'orion', 'sage'];
      const agent = agents.find(a => args.includes(a));
      if (agent) {
        window.dispatchEvent(new CustomEvent('voice:agent', { detail: { agentId: agent } }));
      }
    }, { description: 'Ouvrir une conversation avec un agent', aliases: ['appelle', 'contact'] });

    // Contrôles
    this.commands.register('arrête', () => {
      this.synthesis.stop();
      this.recognition.stop();
    }, { description: 'Arrêter toute activité vocale', aliases: ['stop', 'silence'] });

    this.commands.register('aide', () => {
      const commands = this.commands.listCommands();
      const helpText = commands.map(c => `${c.phrase}: ${c.description}`).join('. ');
      this.synthesis.speak(`Commandes disponibles: ${helpText}`);
    }, { description: 'Liste des commandes disponibles' });
  }

  // Écouter et répondre
  async listenAndRespond(responseCallback) {
    return new Promise((resolve, reject) => {
      this.recognition.on('result', async (result) => {
        const response = await responseCallback(result.transcript);
        if (response) {
          await this.synthesis.speak(response);
        }
        resolve(result);
      });

      this.recognition.on('error', (error) => {
        reject(error);
      });

      this.recognition.start();
    });
  }

  // Initialiser le visualiseur
  async initializeVisualizer() {
    return this.visualizer.initialize();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════════════════

const voiceService = new VoiceService();

export {
  voiceService,
  SpeechRecognitionService,
  SpeechSynthesisService,
  VoiceCommandService,
  AudioVisualizer
};

export default voiceService;
