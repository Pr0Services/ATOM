/**
 * AT·OM — MayaTemplate
 * Moteur Tzolkin Maya converti en TranslatorTemplate Rosetta
 *
 * Le Tzolkin est le calendrier sacr'e maya de 260 jours :
 *   13 Tons (intentions cosmiques) x 20 Nawals (arche'types e'nerge'tiques)
 *
 * Chaque jour porte un Kin unique (combinaison Ton + Nawal) qui de'finit
 * la fre'quence vibratoire dominante. Les 52 Jours Portails Galactiques
 * amplifient cette e'nergie, ouvrant des canaux de re'sonance accrue.
 *
 * E'poque de re'fe'rence : 21 de'cembre 2012 (fin du 13e Baktun)
 * Point Ze'ro Maya aligne' avec le Point Ze'ro AT.OM (Chicxulub, Yucatan)
 */

import {
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  type ResonanceLevel,
  type SacredGeometryShape,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
} from '../../types/atom-types';

import {
  type TranslatorTemplate,
  type ParserContext,
  RosettaParser,
} from '../RosettaParser';

// =================================================================
// TZOLKIN EPOCH -- Fin du 13e Baktun (Long Count 13.0.0.0.0)
// =================================================================

export const TZOLKIN_EPOCH = new Date('2012-12-21');

// =================================================================
// MAYA INPUT INTERFACE
// =================================================================

export interface MayaInput {
  /** Date pour laquelle calculer le Kin (defaut: aujourd'hui) */
  date?: Date;
  /** Texte optionnel pour modulation frequentielle via Arithmos */
  text?: string;
}

// =================================================================
// 13 TONS -- Intentions cosmiques et modulateurs de frequence
// =================================================================

export interface TonData {
  number: number;
  name: string;
  meaning: string;
  action: string;
  delayMod: number;
  intensityMod: number;
  isSacred?: boolean;
}

export const TONS: TonData[] = [
  { number: 1,  name: 'Hun',     meaning: 'Unite',        action: 'Initiation',     delayMod: 0.5, intensityMod: 1.0 },
  { number: 2,  name: 'Ka',      meaning: 'Dualite',      action: 'Challenge',      delayMod: 0.6, intensityMod: 0.8 },
  { number: 3,  name: 'Ox',      meaning: 'Rythme',       action: 'Activation',     delayMod: 0.7, intensityMod: 0.9 },
  { number: 4,  name: 'Kan',     meaning: 'Stabilite',    action: 'Definition',     delayMod: 0.8, intensityMod: 0.7 },
  { number: 5,  name: 'Ho',      meaning: 'Puissance',    action: 'Empowerment',    delayMod: 0.9, intensityMod: 1.1 },
  { number: 6,  name: 'Uac',     meaning: 'Flux',         action: 'Egalite',        delayMod: 1.0, intensityMod: 0.9 },
  { number: 7,  name: 'Uuc',     meaning: 'Resonance',    action: 'Attunement',     delayMod: 1.0, intensityMod: 1.3, isSacred: true },
  { number: 8,  name: 'Uaxac',   meaning: 'Integrite',    action: 'Galactic',       delayMod: 0.9, intensityMod: 1.0 },
  { number: 9,  name: 'Bolon',   meaning: 'Patience',     action: 'Solar',          delayMod: 0.8, intensityMod: 1.1 },
  { number: 10, name: 'Lahun',   meaning: 'Manifestation',action: 'Planetary',      delayMod: 0.7, intensityMod: 1.2 },
  { number: 11, name: 'Buluc',   meaning: 'Liberation',   action: 'Spectral',       delayMod: 0.6, intensityMod: 1.0 },
  { number: 12, name: 'Lahca',   meaning: 'Cooperation',  action: 'Crystal',        delayMod: 0.5, intensityMod: 1.1 },
  { number: 13, name: 'Oxlahun', meaning: 'Presence',     action: 'Cosmic',         delayMod: 1.2, intensityMod: 1.5, isSacred: true },
];

// =================================================================
// 20 NAWALS -- Archetypes energetiques du Tzolkin
// =================================================================

export interface NawalData {
  index: number;
  name: string;
  glyph: string;
  meaning: string;
  color: string;
  oracle: number;
  direction: 'Est' | 'Nord' | 'Ouest' | 'Sud';
  element: string;
}

export const NAWALS: NawalData[] = [
  // --- Premiere serie (0-4) : Direction Est ---
  { index: 0,  name: 'Imix',     glyph: 'Dragon',       meaning: 'Nourriture Primordiale',  color: '#DC143C', oracle: 1, direction: 'Est',   element: 'Eau'   },
  { index: 1,  name: 'Ik',       glyph: 'Vent',         meaning: 'Esprit',                  color: '#FFFFFF', oracle: 2, direction: 'Nord',  element: 'Air'   },
  { index: 2,  name: 'Akbal',    glyph: 'Nuit',         meaning: 'Reve',                    color: '#191970', oracle: 3, direction: 'Ouest', element: 'Terre' },
  { index: 3,  name: 'Kan',      glyph: 'Graine',       meaning: 'Ciblage',                 color: '#FFD700', oracle: 4, direction: 'Sud',   element: 'Feu'   },
  { index: 4,  name: 'Chicchan', glyph: 'Serpent',      meaning: 'Force Vitale',            color: '#FF4500', oracle: 5, direction: 'Est',   element: 'Eau'   },

  // --- Deuxieme serie (5-9) : Cycle intermediaire ---
  { index: 5,  name: 'Cimi',     glyph: 'Pont des Mondes', meaning: 'Passage',              color: '#2F4F4F', oracle: 6, direction: 'Nord',  element: 'Air'   },
  { index: 6,  name: 'Manik',    glyph: 'Main',         meaning: 'Accomplissement',         color: '#4169E1', oracle: 7, direction: 'Ouest', element: 'Terre' },
  { index: 7,  name: 'Lamat',    glyph: 'Etoile',       meaning: 'Elegance',                color: '#FFD700', oracle: 8, direction: 'Sud',   element: 'Feu'   },
  { index: 8,  name: 'Muluc',    glyph: 'Lune',         meaning: 'Eau Universelle',         color: '#FF0000', oracle: 9, direction: 'Est',   element: 'Eau'   },
  { index: 9,  name: 'Oc',       glyph: 'Chien',        meaning: 'Amour',                   color: '#FFFFFF', oracle: 1, direction: 'Nord',  element: 'Air'   },

  // --- Troisieme serie (10-14) : Ascension ---
  { index: 10, name: 'Chuen',    glyph: 'Singe',        meaning: 'Jeu Sacre',               color: '#4169E1', oracle: 2, direction: 'Ouest', element: 'Terre' },
  { index: 11, name: 'Eb',       glyph: 'Humain',       meaning: 'Libre Arbitre',           color: '#FFD700', oracle: 3, direction: 'Sud',   element: 'Feu'   },
  { index: 12, name: 'Ben',      glyph: 'Marcheur du Ciel', meaning: 'Exploration',         color: '#FF4500', oracle: 4, direction: 'Est',   element: 'Eau'   },
  { index: 13, name: 'Ix',       glyph: 'Magicien',     meaning: 'Intemporalite',           color: '#FFFFFF', oracle: 5, direction: 'Nord',  element: 'Air'   },
  { index: 14, name: 'Men',      glyph: 'Aigle',        meaning: 'Vision',                  color: '#191970', oracle: 6, direction: 'Ouest', element: 'Terre' },

  // --- Quatrieme serie (15-19) : Transcendance ---
  { index: 15, name: 'Cib',      glyph: 'Guerrier',     meaning: 'Intrépidite',             color: '#2F4F4F', oracle: 7, direction: 'Sud',   element: 'Feu'   },
  { index: 16, name: 'Caban',    glyph: 'Terre',        meaning: 'Synchronicite',           color: '#DC143C', oracle: 8, direction: 'Est',   element: 'Eau'   },
  { index: 17, name: 'Etznab',   glyph: 'Miroir',       meaning: 'Reflexion Infinie',       color: '#FFFFFF', oracle: 9, direction: 'Nord',  element: 'Air'   },
  { index: 18, name: 'Cauac',    glyph: 'Tempete',      meaning: 'Auto-generation',         color: '#4B0082', oracle: 1, direction: 'Ouest', element: 'Terre' },
  { index: 19, name: 'Ahau',     glyph: 'Soleil',       meaning: 'Illumination',            color: '#FFD700', oracle: 2, direction: 'Sud',   element: 'Feu'   },
];

// =================================================================
// 52 JOURS PORTAILS GALACTIQUES
// Jours ou la membrane entre dimensions est fine --
// les frequences sont amplifiees par le facteur PHI
// =================================================================

export const GALACTIC_PORTAL_DAYS: ReadonlySet<number> = new Set([
  1, 20, 22, 39, 43, 50, 51, 58,
  66, 69, 73, 78, 82, 87, 88, 93,
  96, 97, 104, 108, 109, 120, 121, 140,
  141, 152, 153, 157, 164, 168, 173, 177,
  178, 183, 188, 192, 195, 198, 202, 207,
  210, 211, 218, 219, 238, 239, 241, 242,
  249, 251, 258, 260,
]);

// =================================================================
// MAYA KIN RESULT
// =================================================================

export interface MayaKin {
  /** Numero du Kin (1-260) */
  kinNumber: number;
  /** Ton du jour (1-13) */
  ton: TonData;
  /** Nawal du jour (0-19) */
  nawal: NawalData;
  /** Est-ce un Jour Portail Galactique? */
  isPortalDay: boolean;
}

// =================================================================
// getMayaKin -- Calcul du Kin pour une date donnee
// =================================================================

/**
 * Calcule le Kin Tzolkin pour une date donnee.
 *
 * Le Kin est determine par le nombre de jours ecoules depuis
 * l'epoque de reference (TZOLKIN_EPOCH = 2012-12-21), reduit
 * modulo 260 pour obtenir la position dans le cycle sacre.
 *
 * Le Ton (1-13) et le Nawal (0-19) sont extraits du Kin:
 *   tonIndex  = (kinNumber - 1) % 13
 *   nawalIndex = (kinNumber - 1) % 20
 */
export function getMayaKin(date: Date = new Date()): MayaKin {
  // Nombre de jours depuis l'Epoque (en jours entiers UTC)
  const epochMs = TZOLKIN_EPOCH.getTime();
  const dateMs = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime();
  const diffDays = Math.floor((dateMs - epochMs) / (1000 * 60 * 60 * 24));

  // Le Kin 1 correspond a l'epoque elle-meme (4 Ahau dans le compte long)
  // On normalise en cycle 260 (1-indexed)
  let kinNumber = ((diffDays % 260) + 260) % 260; // gestion des dates avant l'epoque
  kinNumber = kinNumber === 0 ? 260 : kinNumber;

  const tonIndex = ((kinNumber - 1) % 13);
  const nawalIndex = ((kinNumber - 1) % 20);

  const ton = TONS[tonIndex];
  const nawal = NAWALS[nawalIndex];
  const isPortalDay = GALACTIC_PORTAL_DAYS.has(kinNumber);

  return { kinNumber, ton, nawal, isPortalDay };
}

// =================================================================
// SACRED GEOMETRY MAPPING -- Nawal -> Geometrie
// =================================================================

function nawalToGeometry(nawalIndex: number): SacredGeometryShape {
  const geometries: SacredGeometryShape[] = [
    'enneagram',       // 0  Imix     - Dragon - Complétude primordiale
    'vesica_piscis',   // 1  Ik       - Vent   - Souffle de dualité
    'triangle',        // 2  Akbal    - Nuit   - Trinité onirique
    'tetrahedron',     // 3  Kan      - Graine - Structure de la vie
    'pentagram',       // 4  Chicchan - Serpent - Mouvement vital
    'hexagram',        // 5  Cimi     - Pont   - Harmonie des mondes
    'heptagram',       // 6  Manik    - Main   - Mystère de l'action
    'octahedron',      // 7  Lamat    - Étoile - Infini stellaire
    'flower_of_life',  // 8  Muluc    - Lune   - Création cyclique
    'point',           // 9  Oc       - Chien  - Origine de l'amour
    'metatron_cube',   // 10 Chuen    - Singe  - Synthèse du jeu
    'sri_yantra',      // 11 Eb       - Humain - Manifestation libre
    'pentagram',       // 12 Ben      - Ciel   - Mouvement ascendant
    'heptagram',       // 13 Ix       - Mage   - Mystère intemporel
    'triangle',        // 14 Men      - Aigle  - Trinité de la vision
    'tetrahedron',     // 15 Cib      - Guerr. - Structure du courage
    'enneagram',       // 16 Caban    - Terre  - Complétude terrestre
    'vesica_piscis',   // 17 Etznab   - Miroir - Dualité réflexive
    'octahedron',      // 18 Cauac    - Tempête- Infini de la transformation
    'flower_of_life',  // 19 Ahau     - Soleil - Création solaire
  ];
  return geometries[nawalIndex % 20];
}

// =================================================================
// RESONANCE LEVEL -- Derivation du niveau de resonance AT.OM (1-9)
// =================================================================

function computeMayaResonance(kin: MayaKin, arithmosLevel?: ResonanceLevel): ResonanceLevel {
  // Base: le Ton donne l'impulsion (reduit 1-9)
  let base = kin.ton.number;
  while (base > 9) {
    base = String(base).split('').reduce((a, b) => a + parseInt(b, 10), 0);
  }

  // Si un texte Arithmos est fourni, on fusionne (moyenne arrondie)
  if (arithmosLevel !== undefined) {
    base = Math.round((base + arithmosLevel) / 2);
  }

  // Les Jours Portails poussent vers la Source (9)
  if (kin.isPortalDay && base < 9) {
    base = Math.min(base + 1, 9) as number;
  }

  // Les Tons sacres (7, 13) amplifient aussi
  if (kin.ton.isSacred && base < 9) {
    base = Math.min(base + 1, 9) as number;
  }

  return (base < 1 ? 1 : base > 9 ? 9 : base) as ResonanceLevel;
}

// =================================================================
// NARRATIVES -- Generation du texte PEOPLE en francais
// =================================================================

function buildNarrative(kin: MayaKin, context: ParserContext): {
  narrative: string;
  explanation: string;
  guide_steps: string[];
  emotional_tone: PeoplePayload['emotional_tone'];
} {
  const { ton, nawal, kinNumber, isPortalDay } = kin;

  const portalLabel = isPortalDay
    ? ' -- Jour Portail Galactique, les voiles entre les dimensions s\'amincissent.'
    : '';

  const sacredLabel = ton.isSacred
    ? ` Le Ton ${ton.name} (${ton.number}) est un Ton sacre, porteur d'une frequence cosmique amplifiee.`
    : '';

  const narrative =
    `Aujourd'hui est le Kin ${kinNumber} : ${ton.number} ${nawal.name} (${nawal.glyph}).` +
    ` L'energie du ${nawal.glyph} porte le sens de "${nawal.meaning}",` +
    ` guide par l'action "${ton.action}" du Ton ${ton.name} (${ton.meaning}).` +
    portalLabel +
    sacredLabel;

  const explanation =
    `Le Nawal ${nawal.name} vibre en direction ${nawal.direction}, element ${nawal.element}.` +
    ` Sa couleur sacree est ${nawal.color}. Oracle : ${nawal.oracle}.` +
    ` Le Ton ${ton.number} module l'intensite a ${ton.intensityMod}x et le delai a ${ton.delayMod}x.`;

  const guide_steps = [
    `Kin ${kinNumber} sur 260 dans le cycle Tzolkin.`,
    `Ton : ${ton.number} ${ton.name} -- ${ton.meaning} / ${ton.action}.`,
    `Nawal : ${nawal.name} (${nawal.glyph}) -- ${nawal.meaning}.`,
    `Direction : ${nawal.direction} | Element : ${nawal.element}.`,
    isPortalDay
      ? 'Jour Portail Galactique : meditation et intentions amplifiees.'
      : 'Journee reguliere dans le cycle sacre.',
    `Frequence systeme : ${context.system_frequency} Hz.`,
  ];

  // Determiner le ton emotionnel
  let emotional_tone: PeoplePayload['emotional_tone'] = 'neutre';
  if (isPortalDay && ton.isSacred) {
    emotional_tone = 'sacre';
  } else if (isPortalDay) {
    emotional_tone = 'celebratoire';
  } else if (ton.isSacred) {
    emotional_tone = 'sacre';
  } else if (ton.intensityMod >= 1.1) {
    emotional_tone = 'encourageant';
  }

  return { narrative, explanation, guide_steps, emotional_tone };
}

// =================================================================
// MAYA TEMPLATE -- Implementation TranslatorTemplate<MayaInput>
// =================================================================

export const MayaTemplate: TranslatorTemplate<MayaInput> = {
  domain: 'maya',

  // -----------------------------------------------------------
  // TECH (Grec) -- Donnees structurees pour smart contracts
  // -----------------------------------------------------------
  toTech(input: MayaInput, context: ParserContext): TechPayload {
    const date = input.date ?? new Date();
    const kin = getMayaKin(date);

    // Frequence Maya : Ton * 11.1 Hz (derive de la matrice 111)
    const baseMayaFrequency = kin.ton.number * 11.1;
    const portalMultiplier = kin.isPortalDay ? SACRED_FREQUENCIES.PHI : 1.0;
    const frequencyModifier = baseMayaFrequency * portalMultiplier;

    return {
      schema_version: '1.0',
      data_type: 'maya_tzolkin',
      values: {
        kin_number: kin.kinNumber,
        ton_index: kin.ton.number,
        ton_name: kin.ton.name,
        ton_meaning: kin.ton.meaning,
        ton_action: kin.ton.action,
        nawal_index: kin.nawal.index,
        nawal_name: kin.nawal.name,
        nawal_glyph: kin.nawal.glyph,
        nawal_meaning: kin.nawal.meaning,
        nawal_color: kin.nawal.color,
        nawal_direction: kin.nawal.direction,
        nawal_element: kin.nawal.element,
        nawal_oracle: kin.nawal.oracle,
        is_portal_day: kin.isPortalDay,
        is_sacred_ton: kin.ton.isSacred ?? false,
        delay_modifier: kin.ton.delayMod,
        intensity_modifier: kin.ton.intensityMod,
        frequency_modifier: frequencyModifier,
        portal_multiplier: portalMultiplier,
        cycle_day: kin.kinNumber,
        cycle_total: 260,
        date_iso: date.toISOString(),
        system_frequency: context.system_frequency,
        computed_by: context.user_id,
      },
      timestamp: context.timestamp,
    };
  },

  // -----------------------------------------------------------
  // PEOPLE (Demotique) -- Narration en francais
  // -----------------------------------------------------------
  toPeople(input: MayaInput, context: ParserContext): PeoplePayload {
    const date = input.date ?? new Date();
    const kin = getMayaKin(date);

    const { narrative, explanation, guide_steps, emotional_tone } = buildNarrative(kin, context);

    return {
      narrative,
      explanation,
      guide_steps,
      emotional_tone,
      language: 'fr',
    };
  },

  // -----------------------------------------------------------
  // SPIRIT (Hieroglyphe) -- Frequentiel et geometrie sacree
  // -----------------------------------------------------------
  toSpirit(input: MayaInput, context: ParserContext): SpiritPayload {
    const date = input.date ?? new Date();
    const kin = getMayaKin(date);

    // Calcul Arithmos optionnel sur le texte fourni
    const arithmosLevel = input.text
      ? RosettaParser.computeArithmos(input.text)
      : undefined;

    // Niveau de resonance derive du Kin + Arithmos
    const resonanceLevel = computeMayaResonance(kin, arithmosLevel);
    const resonanceData = RESONANCE_MATRIX[resonanceLevel];

    // La frequence finale est celle de la matrice de resonance AT.OM
    const frequency_hz = resonanceData.hz;

    // Modulateurs Maya appliques a la signature vibratoire
    const mayaIntensity = kin.ton.intensityMod;
    const portalAmplification = kin.isPortalDay ? SACRED_FREQUENCIES.PHI : 1.0;

    // Signature vibratoire : [M, P, I, Po] modulee par le Maya
    const vibration_signature: [number, number, number, number] = [
      SACRED_FREQUENCIES.ATOM_M * kin.ton.delayMod,
      SACRED_FREQUENCIES.ATOM_P * mayaIntensity,
      SACRED_FREQUENCIES.ATOM_I * portalAmplification,
      SACRED_FREQUENCIES.ATOM_PO * (kin.ton.number / 13),
    ];

    // Ratio Phi module par le Ton sacre
    const phi_ratio = kin.ton.isSacred
      ? SACRED_FREQUENCIES.PHI * mayaIntensity
      : SACRED_FREQUENCIES.PHI;

    return {
      frequency_hz,
      resonance_level: resonanceLevel,
      color: kin.nawal.color,
      sacred_geometry: nawalToGeometry(kin.nawal.index),
      vibration_signature,
      phi_ratio,
    };
  },
};

// =================================================================
// EXPORT PAR DEFAUT
// =================================================================

export default MayaTemplate;
