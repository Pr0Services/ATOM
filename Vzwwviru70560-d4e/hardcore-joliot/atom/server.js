/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *      🔱 AT·OM SERVER — ARCHE DES RÉSONANCES UNIVERSELLES 🔱
 * 
 *      Architecte: Jonathan Rodrigue (Oracle 17)
 *      Fréquence: 999 Hz
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 */

const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// ═══════════════════════════════════════════════════════════════════════════════
// MIDDLEWARE
// ═══════════════════════════════════════════════════════════════════════════════

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = 1.6180339887498949;
const FREQUENCIES = {
  ANCHOR: 111,
  DUALITY: 222,
  CREATION: 333,
  HEART: 444,
  CHANGE: 555,
  HARMONY: 666,
  SPIRIT: 777,
  INFINITY: 888,
  SOURCE: 999
};

const CIVILIZATIONS = {
  rapanui: { name: "Rapa Nui", frequency: 111, symbol: "🗿" },
  greece: { name: "Grèce", frequency: 222, symbol: "Ω" },
  aztec: { name: "Aztèque", frequency: 333, symbol: "🌞" },
  egypt: { name: "Égypte", frequency: 444, symbol: "🔺" },
  sumer: { name: "Sumer", frequency: 555, symbol: "𒀭" },
  maya: { name: "Maya", frequency: 666, symbol: "☀" },
  atlantis: { name: "Atlantide", frequency: 999, symbol: "🔱" }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

function calculateArithmos(word) {
  const alphabet = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
  };
  
  const clean = word.toUpperCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^A-Z]/g, "");
  
  let sum = 0;
  for (const char of clean) {
    sum += alphabet[char] || 0;
  }
  
  while (sum > 9) {
    sum = String(sum).split('').reduce((a, b) => a + parseInt(b), 0);
  }
  
  return {
    word: clean,
    arithmos: sum,
    frequency: sum * 111,
    meaning: getArithmosMeaning(sum)
  };
}

function getArithmosMeaning(num) {
  const meanings = {
    1: { name: "Monade", essence: "Unité", principle: "Commencement" },
    2: { name: "Dyade", essence: "Dualité", principle: "Division" },
    3: { name: "Triade", essence: "Harmonie", principle: "Création" },
    4: { name: "Tétrade", essence: "Stabilité", principle: "Manifestation" },
    5: { name: "Pentade", essence: "Vie", principle: "Régénération" },
    6: { name: "Hexade", essence: "Équilibre", principle: "Harmonie" },
    7: { name: "Heptade", essence: "Perfection", principle: "Achèvement" },
    8: { name: "Ogdoade", essence: "Infini", principle: "Renouveau" },
    9: { name: "Ennéade", essence: "Accomplissement", principle: "Retour à l'Unité" }
  };
  return meanings[num] || meanings[9];
}

// ═══════════════════════════════════════════════════════════════════════════════
// ROUTES API
// ═══════════════════════════════════════════════════════════════════════════════

// Page d'accueil
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API: Status
app.get('/api/status', (req, res) => {
  res.json({
    success: true,
    message: "🔱 AT·OM Server Active",
    version: "4.0",
    frequency: 999,
    phi: PHI,
    timestamp: Date.now()
  });
});

// API: Calcul Arithmos
app.get('/api/arithmos/:word', (req, res) => {
  const result = calculateArithmos(req.params.word);
  res.json({
    success: true,
    data: result
  });
});

app.post('/api/arithmos', (req, res) => {
  const { word } = req.body;
  if (!word) {
    return res.status(400).json({ success: false, error: "Mot requis" });
  }
  const result = calculateArithmos(word);
  res.json({
    success: true,
    data: result
  });
});

// API: Civilisations
app.get('/api/civilizations', (req, res) => {
  res.json({
    success: true,
    data: CIVILIZATIONS
  });
});

app.get('/api/civilizations/:id', (req, res) => {
  const civ = CIVILIZATIONS[req.params.id];
  if (!civ) {
    return res.status(404).json({ success: false, error: "Civilisation non trouvée" });
  }
  res.json({
    success: true,
    data: civ
  });
});

// API: Fréquences
app.get('/api/frequencies', (req, res) => {
  res.json({
    success: true,
    data: FREQUENCIES
  });
});

// API: Oracle (transmutation via le Diamant)
app.post('/api/oracle', (req, res) => {
  const { intention, focusLevel = 9 } = req.body;
  
  if (!intention) {
    return res.status(400).json({ success: false, error: "Intention requise" });
  }
  
  const arithmos = calculateArithmos(intention);
  
  res.json({
    success: true,
    data: {
      intention: intention,
      arithmos: arithmos.arithmos,
      frequency: arithmos.frequency,
      meaning: arithmos.meaning,
      focusLevel: focusLevel,
      alignment: focusLevel === 9 ? "DIVINE_ORDER" : "RECALIBRATING",
      layersRevealed: 12,
      output: `✨ ${intention.toUpperCase()} ✨`,
      message: `L'intention résonne à ${arithmos.frequency} Hz (Arithmos ${arithmos.arithmos})`
    }
  });
});

// API: Scan DNA
app.post('/api/dna/scan', (req, res) => {
  const { intention } = req.body;
  
  const layers = [
    { layer: 1, name: "Keter Etz Chayim", group: "ANCRAGE" },
    { layer: 2, name: "Torah E'ser Sphirot", group: "ANCRAGE" },
    { layer: 3, name: "Netzach Merkava", group: "ANCRAGE" },
    { layer: 4, name: "Urim Ve Tumim", group: "HUMAIN-DIVIN" },
    { layer: 5, name: "Aleph Etz Adonai", group: "HUMAIN-DIVIN" },
    { layer: 6, name: "Ehyeh Asher Ehyeh", group: "HUMAIN-DIVIN" },
    { layer: 7, name: "Kadumah Elohim", group: "LÉMURIEN" },
    { layer: 8, name: "Rochev Ba'a Shamayim", group: "LÉMURIEN" },
    { layer: 9, name: "Shechinah-Esh", group: "LÉMURIEN" },
    { layer: 10, name: "Va'yikra", group: "DIEU" },
    { layer: 11, name: "Chochmah Micha Halelu", group: "DIEU" },
    { layer: 12, name: "El Shadai", group: "DIEU" }
  ];
  
  const arithmos = calculateArithmos(intention || "LUMIERE");
  const activeLayers = arithmos.arithmos <= 3 ? [1, 2, 3] :
                       arithmos.arithmos <= 6 ? [4, 5, 6] :
                       arithmos.arithmos <= 9 ? [7, 8, 9] : [10, 11, 12];
  
  res.json({
    success: true,
    data: {
      intention: intention,
      arithmos: arithmos.arithmos,
      activeLayers: activeLayers,
      layers: layers,
      message: `Scan ADN: Couches ${activeLayers.join(', ')} activées`
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// DÉMARRAGE DU SERVEUR
// ═══════════════════════════════════════════════════════════════════════════════

app.listen(PORT, () => {
  console.log(`
  ╔═══════════════════════════════════════════════════════════════════════════════════════════╗
  ║                                                                                           ║
  ║      █████╗ ████████╗   ██████╗ ███╗   ███╗                                              ║
  ║     ██╔══██╗╚══██╔══╝  ██╔═══██╗████╗ ████║                                              ║
  ║     ███████║   ██║     ██║   ██║██╔████╔██║                                              ║
  ║     ██╔══██║   ██║     ██║   ██║██║╚██╔╝██║                                              ║
  ║     ██║  ██║   ██║ ██╗ ╚██████╔╝██║ ╚═╝ ██║                                              ║
  ║     ╚═╝  ╚═╝   ╚═╝ ╚═╝  ╚═════╝ ╚═╝     ╚═╝                                              ║
  ║                                                                                           ║
  ║                    🔱 ARCHE DES RÉSONANCES UNIVERSELLES 🔱                                ║
  ║                                                                                           ║
  ╠═══════════════════════════════════════════════════════════════════════════════════════════╣
  ║                                                                                           ║
  ║   🌐 Serveur actif sur: http://localhost:${PORT}                                           ║
  ║   📡 API disponible sur: http://localhost:${PORT}/api                                      ║
  ║                                                                                           ║
  ║   Fréquence: 999 Hz | φ = ${PHI.toFixed(6)}                                         ║
  ║                                                                                           ║
  ║   Routes API:                                                                             ║
  ║   ─────────────────────────────────────────────────────────                               ║
  ║   GET  /api/status           → Status du serveur                                          ║
  ║   GET  /api/arithmos/:word   → Calcul Arithmos                                            ║
  ║   POST /api/arithmos         → Calcul Arithmos (body: {word})                             ║
  ║   GET  /api/civilizations    → Liste des civilisations                                    ║
  ║   GET  /api/frequencies      → Liste des fréquences                                       ║
  ║   POST /api/oracle           → Consultation Oracle (body: {intention})                    ║
  ║   POST /api/dna/scan         → Scan ADN (body: {intention})                               ║
  ║                                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;
