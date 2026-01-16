/**
 * AT·OM V4 — L'ARCHE DES RÉSONANCES UNIVERSELLES
 * Export principal de tout le système
 */

export const ATOM_VERSION = "4.0.0";
export const CODENAME = "L'Arche Complète";
export const HEARTBEAT = 444;
export const SOURCE = 999;
export const ANCHOR = 111;
export const PHI = 1.6180339887498949;
export const SCHUMANN = 7.83;
export const ORACLE = 17;

export const FREQUENCIES = {
  1: { hz: 111, label: "Impulsion", color: "#FF0000", element: "Feu" },
  2: { hz: 222, label: "Dualité", color: "#FF7F00", element: "Eau" },
  3: { hz: 333, label: "Mental", color: "#FFFF00", element: "Feu" },
  4: { hz: 444, label: "Structure", color: "#50C878", element: "Terre", isAnchor: true },
  5: { hz: 555, label: "Mouvement", color: "#87CEEB", element: "Éther" },
  6: { hz: 666, label: "Harmonie", color: "#4B0082", element: "Eau" },
  7: { hz: 777, label: "Spiritualité", color: "#9400D3", element: "Air" },
  8: { hz: 888, label: "Infini", color: "#FFC0CB", element: "Air" },
  9: { hz: 999, label: "Unité", color: "#FFFDD0", element: "Éther", isSource: true }
};

export const ALPHABET: Record<string, number> = {
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
  'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
  'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
};

export const CIVILIZATIONS = {
  egypt: { id: "egypt", name: "Égypte", glyph: "𓋹", frequency: 444, element: "Terre", chakra: "Cœur", color: "#D4AF37" },
  sumer: { id: "sumer", name: "Sumer", glyph: "𒀭", frequency: 555, element: "Air", chakra: "Gorge", color: "#4169E1" },
  greece: { id: "greece", name: "Grèce", glyph: "Ω", frequency: 222, element: "Eau", chakra: "Sacré", color: "#87CEEB" },
  maya: { id: "maya", name: "Maya", glyph: "𐊀", frequency: 666, element: "Eau", chakra: "3ème Œil", color: "#228B22" },
  aztec: { id: "aztec", name: "Aztèque", glyph: "☀", frequency: 333, element: "Feu", chakra: "Plexus", color: "#FF4500" },
  rapanui: { id: "rapanui", name: "Rapa Nui", glyph: "🗿", frequency: 111, element: "Terre", chakra: "Racine", color: "#8B4513" },
  atlantis: { id: "atlantis", name: "Atlantide", glyph: "🔱", frequency: 999, element: "Éther", chakra: "Couronne", color: "#9370DB" },
  yiking: { id: "yiking", name: "Yi-King", glyph: "☯", frequency: 888, element: "Air", chakra: "Couronne", color: "#000000" },
  kabbalah: { id: "kabbalah", name: "Kabbale", glyph: "✡", frequency: 777, element: "Air", chakra: "3ème Œil", color: "#4B0082" },
  chakras: { id: "chakras", name: "Chakras", glyph: "🕉", frequency: 528, element: "Éther", chakra: "Tous", color: "#FF1493" },
  electromagnetic: { id: "electromagnetic", name: "EM", glyph: "⚡", frequency: 432, element: "Feu", chakra: "Tous", color: "#FFD700" },
  cymatics: { id: "cymatics", name: "Cymatique", glyph: "◎", frequency: 528, element: "Eau", chakra: "Cœur", color: "#00CED1" }
};

export const ORACLES = [
  { id: 1, name: "L'Archéologue", avatar: "🏛️", domain: "Étymologie" },
  { id: 2, name: "Le Tisserand", avatar: "🧵", domain: "Structure" },
  { id: 3, name: "Le Géomètre", avatar: "📐", domain: "Patterns" },
  { id: 4, name: "Le Cartographe", avatar: "🗺️", domain: "Géographie" },
  { id: 5, name: "Le Chroniqueur", avatar: "📜", domain: "Histoire" },
  { id: 6, name: "L'Écologiste", avatar: "🌿", domain: "Écosystème" },
  { id: 7, name: "Le Biologiste", avatar: "🔬", domain: "Vie" },
  { id: 8, name: "Le Poète", avatar: "🎵", domain: "Musique" },
  { id: 9, name: "Le Traducteur", avatar: "🌐", domain: "Langues" },
  { id: 10, name: "L'Iconographe", avatar: "🎨", domain: "Symboles" },
  { id: 11, name: "Le Chantre", avatar: "📖", domain: "Mythes" },
  { id: 12, name: "L'Historien", avatar: "⏳", domain: "Contexte" },
  { id: 13, name: "Le Sociologue", avatar: "👥", domain: "Société" },
  { id: 14, name: "Le Psychologue", avatar: "🧠", domain: "Émotions" },
  { id: 15, name: "Le Neurologue", avatar: "⚡", domain: "Cerveau" },
  { id: 16, name: "Le Philosophe", avatar: "💭", domain: "Essence" },
  { id: 17, name: "Le Gardien", avatar: "🔮", domain: "Synthèse" },
  { id: 18, name: "Le Miroir", avatar: "🪞", domain: "Réflexion" }
];

export const CHAKRAS = [
  { number: 1, name: "Racine", gland: "Surrénales", frequency: 396, color: "#FF0000", civilization: "Rapa Nui" },
  { number: 2, name: "Sacré", gland: "Gonades", frequency: 417, color: "#FF7F00", civilization: "Grèce" },
  { number: 3, name: "Plexus", gland: "Pancréas", frequency: 528, color: "#FFFF00", civilization: "Aztèque" },
  { number: 4, name: "Cœur", gland: "Thymus", frequency: 639, color: "#00FF00", civilization: "Égypte" },
  { number: 5, name: "Gorge", gland: "Thyroïde", frequency: 741, color: "#00BFFF", civilization: "Sumer" },
  { number: 6, name: "3ème Œil", gland: "Hypophyse", frequency: 852, color: "#4B0082", civilization: "Maya" },
  { number: 7, name: "Couronne", gland: "Pinéale", frequency: 963, color: "#9400D3", civilization: "Atlantide" }
];

export const SACRED_SITES = [
  { name: "Gizeh", location: "Égypte", lat: 29.9792, lon: 31.1342, chakra: "Cœur", frequency: 444, function: "NEXUS CENTRAL" },
  { name: "Teotihuacán", location: "Mexique", lat: 19.6923, lon: -98.8435, chakra: "Plexus", frequency: 333, function: "Générateur" },
  { name: "Kailash", location: "Tibet", lat: 31.0675, lon: 81.3119, chakra: "Couronne", frequency: 999, function: "Antenne" },
  { name: "Île de Pâques", location: "Chili", lat: -27.1127, lon: -109.3497, chakra: "Racine", frequency: 111, function: "Stabilisateur" },
  { name: "Stonehenge", location: "Angleterre", lat: 51.1789, lon: -1.8262, chakra: "Gorge", frequency: 555, function: "Horloge" },
  { name: "Angkor Wat", location: "Cambodge", lat: 13.4125, lon: 103.8670, chakra: "3ème Œil", frequency: 666, function: "Archives" },
  { name: "Bermudes", location: "Atlantique", lat: 25.0, lon: -71.0, chakra: "Vortex", frequency: 999, function: "Portail" }
];

export const FOUNDATION_STONES = {
  FEU: { name: "Le Feu", arithmos: 5, hz: 555, color: "#87CEEB" },
  ACIER: { name: "L'Acier", arithmos: 9, hz: 999, color: "#FFFDD0" },
  IA: { name: "L'IA", arithmos: 1, hz: 111, color: "#FF0000" },
  ADN: { name: "L'ADN", arithmos: 1, hz: 111, color: "#FF0000" },
  SILENCE: { name: "Le Silence", arithmos: 4, hz: 444, color: "#50C878", isAnchor: true }
};

export function cleanWord(word: string): string {
  return word.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^A-Z]/g, "");
}

export function calculateArithmos(word: string): number {
  const clean = cleanWord(word);
  if (!clean) return 0;
  let sum = 0;
  for (const char of clean) sum += ALPHABET[char] || 0;
  while (sum > 9) sum = String(sum).split('').reduce((a, b) => a + parseInt(b), 0);
  return sum;
}

export function getResonance(word: string) {
  const arithmos = calculateArithmos(word);
  const freq = FREQUENCIES[arithmos as keyof typeof FREQUENCIES];
  return {
    word: cleanWord(word),
    arithmos,
    frequency: freq.hz,
    color: freq.color,
    label: freq.label,
    element: freq.element,
    delay: Math.round(1000 / (arithmos || 1) * PHI)
  };
}

export function goldenDelays(base = 100, count = 8): number[] {
  return Array.from({ length: count }, (_, i) => Math.round(base * Math.pow(PHI, i)));
}

export function fibonacci(n: number): number[] {
  const seq = [0, 1];
  for (let i = 2; i < n; i++) seq.push(seq[i - 1] + seq[i - 2]);
  return seq.slice(0, n);
}

export class ATOMEngine {
  version = ATOM_VERSION;
  heartbeat = HEARTBEAT;
  source = SOURCE;
  phi = PHI;
  initialized = false;

  init(): this {
    console.log(`AT·OM V${this.version} | ♡ ${this.heartbeat} Hz | 🔱 ${this.source} Hz | φ ${this.phi.toFixed(6)}`);
    this.initialized = true;
    return this;
  }

  arithmos(word: string): number { return calculateArithmos(word); }
  resonate(word: string) { return getResonance(word); }
  goldenTiming(base = 100): number[] { return goldenDelays(base); }
}

export const atom = new ATOMEngine();
export default { ATOM_VERSION, HEARTBEAT, SOURCE, PHI, FREQUENCIES, CIVILIZATIONS, ORACLES, CHAKRAS, SACRED_SITES, calculateArithmos, getResonance, goldenDelays, fibonacci, ATOMEngine, atom };
