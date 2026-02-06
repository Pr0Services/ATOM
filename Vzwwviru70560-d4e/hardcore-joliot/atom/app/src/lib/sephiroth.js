/**
 * AT·OM — Arbre de Séphiroth (Structure de Données)
 * Mapping complet entre la Kabbale et l'écosystème AT·OM
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 10 SÉPHIROTH — Structure fondamentale
// ═══════════════════════════════════════════════════════════════════════════════

export const SEPHIROTH = [
  {
    id: 1,
    name: 'Keter',
    nameFr: 'Couronne',
    title: 'La Source',
    pillar: 'equilibre',     // Pilier central
    world: 'atziluth',       // Monde de l'Émanation
    position: { x: 50, y: 5 },  // Position SVG (%)
    frequency: 999,
    color: '#FFFFFF',
    colorGlow: 'rgba(255, 255, 255, 0.4)',
    atomSphere: 'source',
    atomRole: 'souverain',
    nftTier: 'arbre',        // Plus haut niveau
    element: 'lumiere',
    planet: 'Neptune (Primum Mobile)',
    virtue: 'Accomplissement',
    symbol: '👑',
    description: 'Le point de contact avec l\'Infini. La volonté pure qui précède toute manifestation.',
    atomDescription: 'L\'Oracle 17 — Point d\'origine de toute résonance dans l\'Arche.',
  },
  {
    id: 2,
    name: 'Chokmah',
    nameFr: 'Sagesse',
    title: 'La Force Créatrice',
    pillar: 'misericorde',   // Pilier droit
    world: 'atziluth',
    position: { x: 80, y: 15 },
    frequency: 528,
    color: '#87CEEB',
    colorGlow: 'rgba(135, 206, 235, 0.4)',
    atomSphere: 'sagesse',
    atomRole: 'collaborateur',
    nftTier: 'racine',
    element: 'feu',
    planet: 'Uranus (Zodiaque)',
    virtue: 'Dévotion',
    symbol: '✨',
    description: 'La sagesse primordiale, l\'éclair de l\'inspiration. Le père cosmique.',
    atomDescription: 'Sphère Sagesse — La vision qui guide les décisions souveraines.',
  },
  {
    id: 3,
    name: 'Binah',
    nameFr: 'Intelligence',
    title: 'La Forme',
    pillar: 'rigueur',       // Pilier gauche
    world: 'atziluth',
    position: { x: 20, y: 15 },
    frequency: 444,
    color: '#1E3A5F',
    colorGlow: 'rgba(30, 58, 95, 0.5)',
    atomSphere: 'justice',
    atomRole: 'collaborateur',
    nftTier: 'racine',
    element: 'eau',
    planet: 'Saturne',
    virtue: 'Silence',
    symbol: '⚖️',
    description: 'L\'intelligence structurante, la mère cosmique. Comprendre par la forme.',
    atomDescription: 'Sphère Justice — La structure qui donne forme à la vision.',
  },
  {
    id: 4,
    name: 'Chesed',
    nameFr: 'Bonté',
    title: 'La Miséricorde',
    pillar: 'misericorde',
    world: 'briah',          // Monde de la Création
    position: { x: 80, y: 35 },
    frequency: 432,
    color: '#4169E1',
    colorGlow: 'rgba(65, 105, 225, 0.4)',
    atomSphere: 'vie',
    atomRole: 'citoyen',
    nftTier: 'branche',
    element: 'eau',
    planet: 'Jupiter',
    virtue: 'Obéissance',
    symbol: '💙',
    description: 'L\'amour inconditionnel, l\'expansion. La bonté qui donne sans limite.',
    atomDescription: 'Sphère Vie — L\'abondance partagée entre tous les êtres.',
  },
  {
    id: 5,
    name: 'Gevurah',
    nameFr: 'Rigueur',
    title: 'La Force',
    pillar: 'rigueur',
    world: 'briah',
    position: { x: 20, y: 35 },
    frequency: 396,
    color: '#DC143C',
    colorGlow: 'rgba(220, 20, 60, 0.4)',
    atomSphere: 'terre',
    atomRole: 'citoyen',
    nftTier: 'branche',
    element: 'feu',
    planet: 'Mars',
    virtue: 'Courage',
    symbol: '🔥',
    description: 'La discipline, le discernement. La force qui purifie et protège.',
    atomDescription: 'Sphère Terre — L\'ancrage et la protection des ressources.',
  },
  {
    id: 6,
    name: 'Tiphereth',
    nameFr: 'Beauté',
    title: 'Le Cœur',
    pillar: 'equilibre',
    world: 'briah',
    position: { x: 50, y: 42 },
    frequency: 369,
    color: '#D4AF37',
    colorGlow: 'rgba(212, 175, 55, 0.5)',
    atomSphere: 'graine',
    atomRole: 'souverain',
    nftTier: 'branche',
    element: 'air',
    planet: 'Soleil',
    virtue: 'Dévotion au Grand Œuvre',
    symbol: '☀️',
    description: 'Le centre de l\'Arbre. L\'harmonie parfaite. Le fils, le médiateur, le soleil intérieur.',
    atomDescription: 'Sphère Graine — Le cœur de l\'AT·OM, point d\'équilibre entre tous les flux.',
  },
  {
    id: 7,
    name: 'Netzach',
    nameFr: 'Victoire',
    title: 'L\'Éternité',
    pillar: 'misericorde',
    world: 'yetzirah',      // Monde de la Formation
    position: { x: 80, y: 58 },
    frequency: 285,
    color: '#2ECC71',
    colorGlow: 'rgba(46, 204, 113, 0.4)',
    atomSphere: 'tech',
    atomRole: 'collaborateur',
    nftTier: 'pousse',
    element: 'feu',
    planet: 'Vénus',
    virtue: 'Abnégation',
    symbol: '🌿',
    description: 'La victoire de l\'esprit, l\'endurance, l\'art. La nature qui persévère.',
    atomDescription: 'Sphère Tech — L\'innovation qui transcende les limites.',
  },
  {
    id: 8,
    name: 'Hod',
    nameFr: 'Splendeur',
    title: 'La Gloire',
    pillar: 'rigueur',
    world: 'yetzirah',
    position: { x: 20, y: 58 },
    frequency: 741,
    color: '#FF8C00',
    colorGlow: 'rgba(255, 140, 0, 0.4)',
    atomSphere: 'communication',
    atomRole: 'collaborateur',
    nftTier: 'pousse',
    element: 'eau',
    planet: 'Mercure',
    virtue: 'Véracité',
    symbol: '📡',
    description: 'L\'intellect, la communication, la splendeur de la pensée logique.',
    atomDescription: 'Communication — La transmission et le partage de connaissance.',
  },
  {
    id: 9,
    name: 'Yesod',
    nameFr: 'Fondation',
    title: 'Le Pont',
    pillar: 'equilibre',
    world: 'yetzirah',
    position: { x: 50, y: 72 },
    frequency: 161.8,
    color: '#9B59B6',
    colorGlow: 'rgba(155, 89, 182, 0.4)',
    atomSphere: 'flux',
    atomRole: 'citoyen',
    nftTier: 'pousse',
    element: 'air',
    planet: 'Lune',
    virtue: 'Indépendance',
    symbol: '🌙',
    description: 'La fondation, le pont entre le visible et l\'invisible. Le rêve et l\'astral.',
    atomDescription: 'Flow Keeper — Le pont qui relie l\'intention à la manifestation.',
  },
  {
    id: 10,
    name: 'Malkuth',
    nameFr: 'Royaume',
    title: 'Le Monde',
    pillar: 'equilibre',
    world: 'assiah',         // Monde de l'Action
    position: { x: 50, y: 92 },
    frequency: 44.4,
    color: '#8B4513',
    colorGlow: 'rgba(139, 69, 19, 0.4)',
    atomSphere: 'manifestation',
    atomRole: 'citoyen',
    nftTier: 'graine',
    element: 'terre',
    planet: 'Terre',
    virtue: 'Discernement',
    symbol: '🌍',
    description: 'Le Royaume terrestre. Où tout se manifeste. La matière sacrée.',
    atomDescription: 'CHE·NU — Le monde actuel, base de la transformation.',
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 22 CHEMINS (Sentiers) — Connexions entre les Séphiroth
// ═══════════════════════════════════════════════════════════════════════════════

export const PATHS = [
  // Les 3 horizontaux
  { id: 1,  from: 2, to: 3,  letter: 'א', letterName: 'Aleph',   element: 'Air',     tarot: 'Le Mat',             color: '#FFFF00' },
  { id: 2,  from: 4, to: 5,  letter: 'ט', letterName: 'Teth',    element: 'Feu',     tarot: 'La Force',           color: '#FF4500' },
  { id: 3,  from: 7, to: 8,  letter: 'פ', letterName: 'Pé',      element: 'Feu',     tarot: 'La Tour',            color: '#DC143C' },

  // Les 7 verticaux
  { id: 4,  from: 1, to: 6,  letter: 'ג', letterName: 'Gimel',   element: 'Eau',     tarot: 'La Papesse',         color: '#4169E1' },
  { id: 5,  from: 2, to: 4,  letter: 'ו', letterName: 'Vav',     element: 'Terre',   tarot: 'Le Hiérophante',     color: '#8B4513' },
  { id: 6,  from: 3, to: 5,  letter: 'ח', letterName: 'Cheth',   element: 'Eau',     tarot: 'Le Chariot',         color: '#4682B4' },
  { id: 7,  from: 4, to: 7,  letter: 'כ', letterName: 'Kaph',    element: 'Feu',     tarot: 'La Roue de Fortune', color: '#9400D3' },
  { id: 8,  from: 5, to: 8,  letter: 'מ', letterName: 'Mem',     element: 'Eau',     tarot: 'Le Pendu',           color: '#1E90FF' },
  { id: 9,  from: 6, to: 9,  letter: 'ס', letterName: 'Samekh',  element: 'Feu',     tarot: 'Tempérance',         color: '#4169E1' },
  { id: 10, from: 9, to: 10, letter: 'ת', letterName: 'Tav',     element: 'Terre',   tarot: 'Le Monde',           color: '#228B22' },

  // Les 12 diagonaux
  { id: 11, from: 1, to: 2,  letter: 'ה', letterName: 'Hé',      element: 'Feu',     tarot: 'L\'Empereur',        color: '#FF6347' },
  { id: 12, from: 1, to: 3,  letter: 'ב', letterName: 'Beth',    element: 'Mercure', tarot: 'Le Bateleur',        color: '#FFD700' },
  { id: 13, from: 2, to: 6,  letter: 'ז', letterName: 'Zayin',   element: 'Air',     tarot: 'Les Amoureux',       color: '#FF69B4' },
  { id: 14, from: 3, to: 6,  letter: 'י', letterName: 'Yod',     element: 'Terre',   tarot: 'L\'Ermite',          color: '#556B2F' },
  { id: 15, from: 4, to: 6,  letter: 'ל', letterName: 'Lamed',   element: 'Air',     tarot: 'La Justice',         color: '#2E8B57' },
  { id: 16, from: 5, to: 6,  letter: 'נ', letterName: 'Nun',     element: 'Eau',     tarot: 'La Mort',            color: '#191970' },
  { id: 17, from: 6, to: 7,  letter: 'ע', letterName: 'Ayin',    element: 'Terre',   tarot: 'Le Diable',          color: '#2F4F4F' },
  { id: 18, from: 6, to: 8,  letter: 'צ', letterName: 'Tsadé',   element: 'Air',     tarot: 'L\'Étoile',          color: '#00BFFF' },
  { id: 19, from: 7, to: 9,  letter: 'ק', letterName: 'Qoph',    element: 'Eau',     tarot: 'La Lune',            color: '#7B68EE' },
  { id: 20, from: 8, to: 9,  letter: 'ר', letterName: 'Resh',    element: 'Feu',     tarot: 'Le Soleil',          color: '#FFA500' },
  { id: 21, from: 7, to: 10, letter: 'ש', letterName: 'Shin',    element: 'Feu',     tarot: 'Le Jugement',        color: '#FF0000' },
  { id: 22, from: 8, to: 10, letter: 'ד', letterName: 'Daleth',  element: 'Vénus',   tarot: 'L\'Impératrice',     color: '#32CD32' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 3 PILIERS
// ═══════════════════════════════════════════════════════════════════════════════

export const PILLARS = {
  misericorde: {
    name: 'Pilier de Miséricorde',
    nameFr: 'Miséricorde',
    side: 'right',
    quality: 'Expansion',
    atomRole: 'citoyen',
    sephiroth: [2, 4, 7],
    color: '#4169E1',
    description: 'Le pilier de l\'amour, de la grâce et de l\'expansion. Force masculine active.',
  },
  rigueur: {
    name: 'Pilier de Rigueur',
    nameFr: 'Rigueur',
    side: 'left',
    quality: 'Contraction',
    atomRole: 'collaborateur',
    sephiroth: [3, 5, 8],
    color: '#DC143C',
    description: 'Le pilier de la force, de la structure et de la discipline. Force féminine réceptive.',
  },
  equilibre: {
    name: 'Pilier de l\'Équilibre',
    nameFr: 'Équilibre',
    side: 'center',
    quality: 'Harmonie',
    atomRole: 'souverain',
    sephiroth: [1, 6, 9, 10],
    color: '#D4AF37',
    description: 'Le pilier central, la voie du milieu. L\'union des opposés. Le chemin de la flèche.',
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 4 MONDES
// ═══════════════════════════════════════════════════════════════════════════════

export const WORLDS = {
  atziluth: {
    name: 'Atziluth',
    nameFr: 'Émanation',
    level: 'Archétypal',
    sephiroth: [1, 2, 3],
    color: '#FF4500',
    element: 'Feu',
    atomMapping: 'Vision & Architecture',
    description: 'Le monde le plus élevé. Pure émanation divine. Le plan des archétypes.',
  },
  briah: {
    name: 'Briah',
    nameFr: 'Création',
    level: 'Créatif',
    sephiroth: [4, 5, 6],
    color: '#4169E1',
    element: 'Eau',
    atomMapping: 'Développement & Structure',
    description: 'Le monde de la création. Où les archétypes prennent forme.',
  },
  yetzirah: {
    name: 'Yetzirah',
    nameFr: 'Formation',
    level: 'Formatif',
    sephiroth: [7, 8, 9],
    color: '#9B59B6',
    element: 'Air',
    atomMapping: 'Opérations & Communication',
    description: 'Le monde de la formation. Les patterns et les processus.',
  },
  assiah: {
    name: 'Assiah',
    nameFr: 'Action',
    level: 'Matériel',
    sephiroth: [10],
    color: '#228B22',
    element: 'Terre',
    atomMapping: 'Manifestation & Communauté',
    description: 'Le monde de l\'action. La réalité manifestée. Le royaume terrestre.',
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAPPING NFT ↔ SÉPHIROTH
// ═══════════════════════════════════════════════════════════════════════════════

export const NFT_SEPHIROTH_MAP = {
  graine: {
    sephirah: 10,       // Malkuth
    level: 'Royaume',
    meaning: 'L\'entrée dans l\'Arche. La graine plantée dans le sol du Royaume.',
    evolution: 'De Malkuth, la graine peut monter vers Yesod (Fondation).',
  },
  pousse: {
    sephirah: 9,        // Yesod
    level: 'Fondation',
    meaning: 'La pousse qui s\'élève depuis la fondation. Le pont entre visible et invisible.',
    evolution: 'De Yesod, la pousse se ramifie vers Netzach ou Hod.',
  },
  branche: {
    sephirah: 6,        // Tiphereth
    level: 'Beauté',
    meaning: 'La branche qui touche le cœur de l\'Arbre. L\'harmonie atteinte.',
    evolution: 'De Tiphereth, la branche rayonne dans toutes les directions.',
  },
  racine: {
    sephirah: 3,        // Binah
    level: 'Intelligence',
    meaning: 'Les racines profondes qui comprennent la structure. La sagesse incarnée.',
    evolution: 'De Binah, les racines touchent le monde archétypal.',
  },
  arbre: {
    sephirah: 1,        // Keter
    level: 'Couronne',
    meaning: 'L\'Arbre de Vie complet. La couronne qui touche l\'Infini. L\'accomplissement total.',
    evolution: 'Keter est l\'accomplissement. L\'Arbre est complet.',
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

/** Get a Sephirah by ID */
export const getSephirah = (id) => SEPHIROTH.find(s => s.id === id);

/** Get a Sephirah by name */
export const getSephirahByName = (name) => SEPHIROTH.find(s => s.name.toLowerCase() === name.toLowerCase());

/** Get all paths connecting to a Sephirah */
export const getPathsForSephirah = (sephirahId) =>
  PATHS.filter(p => p.from === sephirahId || p.to === sephirahId);

/** Get the NFT tier for a Sephirah */
export const getNFTForSephirah = (sephirahId) => {
  const sephirah = getSephirah(sephirahId);
  if (!sephirah) return null;
  return { tier: sephirah.nftTier, ...NFT_SEPHIROTH_MAP[sephirah.nftTier] };
};

/** Get the world for a Sephirah */
export const getWorldForSephirah = (sephirahId) => {
  return Object.values(WORLDS).find(w => w.sephiroth.includes(sephirahId));
};

/** Get the pillar for a Sephirah */
export const getPillarForSephirah = (sephirahId) => {
  const sephirah = getSephirah(sephirahId);
  if (!sephirah) return null;
  return PILLARS[sephirah.pillar];
};

/** Calculate total frequency of the tree */
export const getTotalFrequency = () =>
  SEPHIROTH.reduce((sum, s) => sum + s.frequency, 0);

export default {
  SEPHIROTH,
  PATHS,
  PILLARS,
  WORLDS,
  NFT_SEPHIROTH_MAP,
  getSephirah,
  getSephirahByName,
  getPathsForSephirah,
  getNFTForSephirah,
  getWorldForSephirah,
  getPillarForSephirah,
  getTotalFrequency,
};
