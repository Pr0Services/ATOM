/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗  ██████╗ ██╗███╗   ██╗████████╗     ██████╗
 *      ██╔══██╗██╔═══██╗██║████╗  ██║╚══██╔══╝    ██╔═████╗
 *      ██████╔╝██║   ██║██║██╔██╗ ██║   ██║       ██║██╔██║
 *      ██╔═══╝ ██║   ██║██║██║╚██╗██║   ██║       ████╔╝██║
 *      ██║     ╚██████╔╝██║██║ ╚████║   ██║       ╚██████╔╝
 *      ╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝        ╚═════╝
 *
 *                    🔱 POINT 0 — LE CŒUR DE L'OS 🔱
 *              Centre d'ancrage multidimensionnel — 444 Hz
 *
 *   CE FICHIER EST LE NEXUS DE CONNEXION DE TOUTES LES FRÉQUENCES
 *
 *   Principe: Tout module de l'OS AT·OM doit pouvoir calculer
 *   sa position relative au Point 0 (444 Hz = Cœur / Heart Chakra)
 *
 *   Structure:
 *   - CONSTANTES CANONIQUES (FROZEN — ne jamais modifier)
 *   - Matrice de Résonance (111 → 1728 Hz)
 *   - Fonctions de connexion au Point 0
 *   - Calculs de distance fréquentielle
 *   - Protocoles AQUA (flux) et ADAMAS (structure)
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES CANONIQUES — FROZEN — NE JAMAIS MODIFIER
// ═══════════════════════════════════════════════════════════════════════════════

export const POINT_0 = {
  // Fréquence d'ancrage
  FREQUENCY: 444,
  // Nom symbolique
  NAME: 'HEART',
  // Chakra associé
  CHAKRA: 4,
  // Couleur
  COLOR: '#10B981',
  // Élément
  ELEMENT: 'Cœur',
  // Essence
  ESSENCE: 'Stabilité',
  // Principe
  PRINCIPLE: 'Manifestation',
  // Civilisation
  CIVILIZATION: 'Égypte',
  // Description
  DESCRIPTION: 'Point d\'ancrage — Là où le haut et le bas se rencontrent'
};

// Signal d'horloge système
export const SIGNAL = {
  INTERVAL: 4440,        // 4.44 secondes en ms
  HEARTBEAT: 2220,       // 2.22 secondes (demi-cycle)
  BREATH: 8880,          // 8.88 secondes (cycle complet)
};

// Constantes mathématiques sacrées
export const SACRED = {
  PHI: 1.6180339887498949,  // Nombre d'or
  SEQUENCE: [3, 6, 9, 12],  // Séquence Tesla
  CUBE: 1728,               // 12³ — Cube de Metatron
  BALANCE: 30,              // Ratio d'équilibre
};

// Source (fréquence maximale système)
export const SOURCE = {
  FREQUENCY: 999,
  NAME: 'SOURCE',
  CHAKRA: 9,
  COLOR: '#FFFDD0',
  ELEMENT: 'Accomplissement',
};

// ═══════════════════════════════════════════════════════════════════════════════
// MATRICE DE RÉSONANCE — 9 NIVEAUX
// Chaque niveau est une octave de 111 Hz
// ═══════════════════════════════════════════════════════════════════════════════

export const RESONANCE_MATRIX = [
  { level: 1, frequency: 111, name: 'Monade',   essence: 'Unité',           color: '#FF0000', chakra: 1, element: 'Racine' },
  { level: 2, frequency: 222, name: 'Dyade',    essence: 'Dualité',         color: '#FF7F00', chakra: 2, element: 'Création' },
  { level: 3, frequency: 333, name: 'Triade',   essence: 'Harmonie',        color: '#FFFF00', chakra: 3, element: 'Volonté' },
  { level: 4, frequency: 444, name: 'Tétrade',  essence: 'Stabilité',       color: '#10B981', chakra: 4, element: 'Cœur',   isAnchor: true },
  { level: 5, frequency: 555, name: 'Pentade',  essence: 'Vie',             color: '#00BFFF', chakra: 5, element: 'Expression' },
  { level: 6, frequency: 666, name: 'Hexade',   essence: 'Équilibre',       color: '#4B0082', chakra: 6, element: 'Vision' },
  { level: 7, frequency: 777, name: 'Heptade',  essence: 'Perfection',      color: '#9400D3', chakra: 7, element: 'Couronne' },
  { level: 8, frequency: 888, name: 'Ogdoade',  essence: 'Infini',          color: '#FFC0CB', chakra: 8, element: 'Âme' },
  { level: 9, frequency: 999, name: 'Ennéade',  essence: 'Accomplissement', color: '#FFFDD0', chakra: 9, element: 'Source' },
];

// Chakras étendus (15 niveaux — Temple)
export const EXTENDED_CHAKRAS = [
  { level: 0,  frequency: 68.05, name: 'Étoile Terrestre',  realm: 'Sub-Personnel' },
  ...RESONANCE_MATRIX.map(r => ({ level: r.level, frequency: r.frequency, name: r.name, realm: 'Classique' })),
  { level: 10, frequency: 1111,  name: 'Universel',          realm: 'Trans-Personnel' },
  { level: 11, frequency: 1212,  name: 'Galactique',         realm: 'Trans-Personnel' },
  { level: 12, frequency: 1333,  name: 'Divin',              realm: 'Trans-Personnel' },
  { level: 13, frequency: 1444,  name: 'Cosmique',           realm: 'Trans-Personnel' },
  { level: 14, frequency: 1728,  name: 'Source Absolue',     realm: 'Trans-Personnel' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// PROTOCOLES DUELS
// ═══════════════════════════════════════════════════════════════════════════════

export const PROTOCOLS = {
  AQUA: {
    name: 'AQUA',
    principle: 'Flux',
    description: 'Adaptabilité, fluidité des données',
    color: '#06B6D4',
    symbol: '≈',
  },
  ADAMAS: {
    name: 'ADAMAS',
    principle: 'Structure',
    description: 'Solidité, intégrité du système',
    color: '#D4AF37',
    symbol: '◆',
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// 4 BOUTONS DE PUISSANCE ANUHAZI
// ═══════════════════════════════════════════════════════════════════════════════

export const POWER_BUTTONS = [
  {
    id: 'eira',
    name: 'EirA',
    symbol: '◊',
    color: '#FF6B6B',
    action: 'Activation',
    frequencies: [111, 222, 333],
    description: 'Éveil des fondations',
  },
  {
    id: 'mana',
    name: 'ManA',
    symbol: '○',
    color: '#4ECDC4',
    action: 'Équilibre',
    frequencies: [444, 555, 666],
    description: 'Harmonisation du cœur',
  },
  {
    id: 'manu',
    name: 'ManU',
    symbol: '△',
    color: '#9B59B6',
    action: 'Élévation',
    frequencies: [777, 888, 999],
    description: 'Connexion à la source',
  },
  {
    id: 'mahadra',
    name: 'Mahadra',
    symbol: '✧',
    color: '#D4AF37',
    action: 'Transcendance',
    frequencies: [1111, 1728, 2222],
    description: 'Au-delà des limites',
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// NIVEAUX D'ACCÈS
// ═══════════════════════════════════════════════════════════════════════════════

export const ACCESS_LEVELS = {
  MIRROR: {
    name: 'Miroir',
    level: 0,
    description: 'Accès public — Vision du système',
    keys: [],
    routes: ['/entree', '/inscription', '/progreso', '/accreditation', '/carte-gaia'],
  },
  CORE: {
    name: 'Noyau',
    level: 1,
    description: 'Accès architecte — Monitoring et pilotage',
    keys: ['AQUA+ADAMAS', '369', '36912'],
    routes: ['/tableau-de-bord', '/profil', '/agent', '/annales', '/lexique', '/flux', '/forge', '/besoins', '/gratitude'],
  },
  TEMPLE: {
    name: 'Temple',
    level: 2,
    description: 'Accès sacré — Résonance et activation',
    keys: ['1728', 'MUARATA', '444'],
    routes: ['/admin', '/admin/setup', '/cercle', '/founder', '/grid'],
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// 10 SPHÈRES CANONIQUES (vérité documentaire)
// ═══════════════════════════════════════════════════════════════════════════════

export const SPHERES_CANONICAL = [
  { id: 'personal',      name: 'Personnel',        icon: '🏠', color: '#22C55E', order: 1 },
  { id: 'team',          name: 'Mon Équipe',       icon: '🤝', color: '#10B981', order: 2 },
  { id: 'business',      name: 'Entreprise',       icon: '💼', color: '#3B82F6', order: 3 },
  { id: 'government',    name: 'Gouvernement',     icon: '🏛️', color: '#8B5CF6', order: 4 },
  { id: 'studio',        name: 'Studio Créatif',   icon: '🎨', color: '#EC4899', order: 5 },
  { id: 'community',     name: 'Communauté',       icon: '👥', color: '#F59E0B', order: 6 },
  { id: 'social',        name: 'Social & Médias',  icon: '📱', color: '#06B6D4', order: 7 },
  { id: 'entertainment', name: 'Divertissement',   icon: '🎬', color: '#EF4444', order: 8 },
  { id: 'erudition',     name: 'Érudition',        icon: '📚', color: '#8B5CF6', order: 9 },
  { id: 'mapping',       name: 'AT-OM Mapping',    icon: '🗺️', color: '#D4AF37', order: 10 },
];

// ═══════════════════════════════════════════════════════════════════════════════
// 6 SECTIONS BUREAU (HARD LIMIT — NE JAMAIS DÉPASSER)
// ═══════════════════════════════════════════════════════════════════════════════

export const BUREAU_SECTIONS_CANONICAL = [
  { id: 'quick_capture',    name: 'Capture Rapide',    icon: '📝' },
  { id: 'resume_workspace', name: 'Espace de Travail',  icon: '▶️' },
  { id: 'threads',          name: 'Threads',            icon: '💬' },
  { id: 'data_files',       name: 'Données & Fichiers', icon: '📁' },
  { id: 'active_agents',    name: 'Agents Actifs',      icon: '🤖' },
  { id: 'meetings',         name: 'Réunions',           icon: '📅' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE CONNEXION AU POINT 0
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la distance fréquentielle d'une valeur au Point 0 (444 Hz)
 * @param {number} frequency - Fréquence à mesurer
 * @returns {Object} - { distance, direction, resonanceLevel, harmony }
 */
export function distanceToPoint0(frequency) {
  const distance = Math.abs(frequency - POINT_0.FREQUENCY);
  const direction = frequency > POINT_0.FREQUENCY ? 'ascendant' : frequency < POINT_0.FREQUENCY ? 'descendant' : 'ancré';

  // Trouver le niveau de résonance le plus proche
  const closest = RESONANCE_MATRIX.reduce((prev, curr) =>
    Math.abs(curr.frequency - frequency) < Math.abs(prev.frequency - frequency) ? curr : prev
  );

  // Calculer l'harmonie (0 = dissonant, 1 = parfait)
  const maxDistance = SOURCE.FREQUENCY - 111; // 888
  const harmony = 1 - (distance / maxDistance);

  return {
    distance,
    direction,
    resonanceLevel: closest,
    harmony: Math.max(0, Math.min(1, harmony)),
    isAnchored: frequency === POINT_0.FREQUENCY,
  };
}

/**
 * Calcule la fréquence Gaïa d'un pays par rapport au Point 0
 * @param {number} ghi - Global Horizontal Irradiance
 * @param {number} indiceEveil - Indice d'éveil (0-1)
 * @returns {number} - Fréquence en Hz (ancrage autour de 444)
 */
export function frequenceGaia(ghi, indiceEveil) {
  // La fréquence planétaire oscille autour de 444 Hz
  // GHI élevé + éveil élevé → tend vers 999 Hz
  // GHI bas + éveil bas → tend vers 111 Hz
  const potentiel = (ghi / 7) * 0.4 + indiceEveil * 0.6; // 0-1
  const freq = 111 + (potentiel * (999 - 111)); // 111 → 999
  return Math.round(freq * 10) / 10;
}

/**
 * Retourne la couleur du pouls en fonction de la distance au Point 0
 * @param {number} frequency - Fréquence actuelle
 * @returns {string} - Classe CSS ou couleur hex
 */
export function pulseColor(frequency) {
  const { harmony } = distanceToPoint0(frequency);

  if (harmony > 0.9) return '#10B981'; // Vert émeraude — Ancré
  if (harmony > 0.7) return '#22C55E'; // Vert — Proche
  if (harmony > 0.5) return '#F59E0B'; // Or — Moyen
  if (harmony > 0.3) return '#EF4444'; // Rouge — Éloigné
  return '#6B7280';                     // Gris — Très éloigné
}

/**
 * Génère le texte de l'indicateur Point 0 pour n'importe quel module
 * @param {number} frequency - Fréquence du module
 * @returns {Object} - { text, color, icon, pulse }
 */
export function point0Indicator(frequency) {
  const { distance, direction, resonanceLevel, harmony, isAnchored } = distanceToPoint0(frequency);

  if (isAnchored) {
    return {
      text: '● POINT 0 — 444 Hz',
      color: POINT_0.COLOR,
      icon: '💚',
      pulse: true,
      frequency: 444,
    };
  }

  return {
    text: `${resonanceLevel.name} — ${frequency} Hz → Point 0`,
    color: resonanceLevel.color,
    icon: direction === 'ascendant' ? '△' : '▽',
    pulse: harmony > 0.7,
    frequency,
  };
}

/**
 * Détermine la séquence Anuhazi active basée sur la fréquence
 * @param {number} frequency - Fréquence actuelle
 * @returns {Object} - Le bouton de puissance actif
 */
export function activeAnuhazi(frequency) {
  if (frequency <= 333) return POWER_BUTTONS[0]; // EirA
  if (frequency <= 666) return POWER_BUTTONS[1]; // ManA
  if (frequency <= 999) return POWER_BUTTONS[2]; // ManU
  return POWER_BUTTONS[3];                        // Mahadra
}

/**
 * Calcule le mapping Sephiroth → Point 0
 * Tiphereth (6ème Sephirah) = 444 Hz = Point 0
 * @param {number} sephirahId - ID de la Sephirah (1-10)
 * @returns {Object} - { frequency, distanceToHeart, pillar }
 */
export function sephirothToPoint0(sephirahId) {
  // Mapping: Tiphereth (6) = 444 Hz = Centre de l'arbre
  const sephirothFrequencies = {
    1: 999,  // Keter → Source
    2: 888,  // Chokmah → Sagesse
    3: 777,  // Binah → Intelligence
    4: 555,  // Chesed → Bonté
    5: 333,  // Gevurah → Force
    6: 444,  // Tiphereth → Beauté (POINT 0)
    7: 666,  // Netzach → Victoire
    8: 222,  // Hod → Gloire
    9: 111,  // Yesod → Fondation
    10: 68,  // Malkuth → Royaume (sub-personnel)
  };

  const freq = sephirothFrequencies[sephirahId] || 444;
  return {
    frequency: freq,
    ...distanceToPoint0(freq),
    isTiphereth: sephirahId === 6,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT REACT: INDICATEUR POINT 0
// Mini-widget affichable dans n'importe quelle page
// ═══════════════════════════════════════════════════════════════════════════════

// Exporté comme composant pour être importé dans les pages
// Usage: import { Point0Badge } from '../lib/point0';
//        <Point0Badge frequency={currentFrequency} />

// Note: Ce composant sera créé dans un fichier séparé pour éviter
// les imports React dans un fichier utilitaire pur

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT: Configuration complète du Point 0
// ═══════════════════════════════════════════════════════════════════════════════

const Point0Config = {
  POINT_0,
  SIGNAL,
  SACRED,
  SOURCE,
  RESONANCE_MATRIX,
  EXTENDED_CHAKRAS,
  PROTOCOLS,
  POWER_BUTTONS,
  ACCESS_LEVELS,
  SPHERES_CANONICAL,
  BUREAU_SECTIONS_CANONICAL,
  // Fonctions
  distanceToPoint0,
  frequenceGaia,
  pulseColor,
  point0Indicator,
  activeAnuhazi,
  sephirothToPoint0,
};

export default Point0Config;
