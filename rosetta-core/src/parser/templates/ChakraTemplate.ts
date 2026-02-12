/**
 * AT·OM -- ChakraTemplate
 * Traducteur Rosetta pour le domaine Chakra
 *
 * Convertit la logique de chakra_engine.js en un TranslatorTemplate
 * compatible avec le RosettaParser tri-dimensionnel.
 *
 * Cartographie des 7 Chakras sur les 9 niveaux AT·OM (111-999 Hz),
 * avec pont vers les frequences du Solfege sacre.
 *
 * Niveaux 8 et 9 sont des harmoniques etendues :
 *   - Level 8 (888Hz) -> Anahata harmonique (Coeur expanse)
 *   - Level 9 (999Hz) -> Sahasrara transcendant (Unite)
 */

import {
  type ResonanceLevel,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
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
// CHAKRA DATA -- Les 7 centres energetiques mappes aux 9 niveaux
// =================================================================

export interface ChakraDatum {
  level: ResonanceLevel;
  atomHz: number;
  chakraNumber: number;
  name: string;
  meaning: string;
  sanskrit: string;
  location: string;
  element: string;
  color: string;
  mantra: string;
  solfeggioHz: number;
  solfeggioMeaning: string;
  note: string;
  petals: number;
  symbol: string;
  gland: string;
  quality: string;
  shadow: string;
  affirmation: string;
  crystals: string[];
  oils: string[];
  yoga: string[];
  isCenter: boolean;
  isHarmonic: boolean;
}

export const CHAKRA_DATA: ChakraDatum[] = [
  // --- Level 1 (111Hz): Muladhara (Root) ---
  {
    level: 1 as ResonanceLevel,
    atomHz: 111,
    chakraNumber: 1,
    name: 'Muladhara',
    meaning: 'Racine / Fondation',
    sanskrit: '\u092E\u0942\u0932\u093E\u0927\u093E\u0930',
    location: 'Base de la colonne vertebrale',
    element: 'Earth',
    color: '#FF0000',
    mantra: 'LAM',
    solfeggioHz: 396,
    solfeggioMeaning: 'Liberation de la peur et de la culpabilite',
    note: 'Do',
    petals: 4,
    symbol: 'Carre (Prithvi Yantra)',
    gland: 'Surrenales',
    quality: 'Survie, ancrage, securite, stabilite',
    shadow: 'Peur, insecurite, deconnexion',
    affirmation: 'Je suis ancre et en securite',
    crystals: ['Jaspe rouge', 'Obsidienne', 'Hematite'],
    oils: ['Patchouli', 'Cedre', 'Vetiver'],
    yoga: ['Tadasana', 'Virabhadrasana'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 2 (222Hz): Svadhisthana (Sacral) ---
  {
    level: 2 as ResonanceLevel,
    atomHz: 222,
    chakraNumber: 2,
    name: 'Svadhisthana',
    meaning: 'Siege du Soi',
    sanskrit: '\u0938\u094D\u0935\u093E\u0927\u093F\u0937\u094D\u0920\u093E\u0928',
    location: 'Sous le nombril',
    element: 'Water',
    color: '#FF7F00',
    mantra: 'VAM',
    solfeggioHz: 417,
    solfeggioMeaning: 'Changement, defaire les situations',
    note: 'Re',
    petals: 6,
    symbol: 'Croissant de lune',
    gland: 'Gonades',
    quality: 'Creativite, emotions, sexualite, plaisir',
    shadow: 'Culpabilite, dependance, instabilite emotionnelle',
    affirmation: 'Je ressens et je cree librement',
    crystals: ['Cornaline', 'Pierre de lune', 'Ambre'],
    oils: ['Ylang-ylang', 'Orange', 'Santal'],
    yoga: ['Baddha Konasana', 'Utkata Konasana'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 3 (333Hz): Manipura (Solar Plexus) ---
  {
    level: 3 as ResonanceLevel,
    atomHz: 333,
    chakraNumber: 3,
    name: 'Manipura',
    meaning: 'Cite des Joyaux',
    sanskrit: '\u092E\u0923\u093F\u092A\u0942\u0930',
    location: 'Plexus solaire',
    element: 'Fire',
    color: '#FFFF00',
    mantra: 'RAM',
    solfeggioHz: 528,
    solfeggioMeaning: 'Transformation, reparation ADN (Frequence de l\'Amour)',
    note: 'Mi',
    petals: 10,
    symbol: 'Triangle inverse (Feu)',
    gland: 'Pancreas',
    quality: 'Volonte, pouvoir personnel, confiance, action',
    shadow: 'Honte, impuissance, controle excessif',
    affirmation: 'J\'agis avec confiance et determination',
    crystals: ['Citrine', 'Oeil de tigre', 'Ambre'],
    oils: ['Citron', 'Romarin', 'Gingembre'],
    yoga: ['Navasana', 'Kapalabhati'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 4 (444Hz): Anahata (Heart) -- CENTER / ANCHOR ---
  {
    level: 4 as ResonanceLevel,
    atomHz: 444,
    chakraNumber: 4,
    name: 'Anahata',
    meaning: 'Non-frappe (Son primordial)',
    sanskrit: '\u0905\u0928\u093E\u0939\u0924',
    location: 'Centre de la poitrine',
    element: 'Air',
    color: '#50C878',
    mantra: 'YAM',
    solfeggioHz: 639,
    solfeggioMeaning: 'Connexion, relations harmonieuses',
    note: 'Fa',
    petals: 12,
    symbol: 'Etoile a 6 branches (Hexagramme)',
    gland: 'Thymus',
    quality: 'Amour inconditionnel, compassion, harmonie',
    shadow: 'Chagrin, isolement, dependance affective',
    affirmation: 'J\'aime et je suis aime inconditionnellement',
    crystals: ['Quartz rose', 'Aventurine', 'Malachite'],
    oils: ['Rose', 'Geranium', 'Bergamote'],
    yoga: ['Ustrasana', 'Bhujangasana'],
    isCenter: true,
    isHarmonic: false,
  },
  // --- Level 5 (555Hz): Vishuddha (Throat) ---
  {
    level: 5 as ResonanceLevel,
    atomHz: 555,
    chakraNumber: 5,
    name: 'Vishuddha',
    meaning: 'Tres pur',
    sanskrit: '\u0935\u093F\u0936\u0941\u0926\u094D\u0927',
    location: 'Gorge',
    element: 'Ether',
    color: '#87CEEB',
    mantra: 'HAM',
    solfeggioHz: 741,
    solfeggioMeaning: 'Expression, solutions, nettoyage',
    note: 'Sol',
    petals: 16,
    symbol: 'Cercle dans un triangle',
    gland: 'Thyroide',
    quality: 'Communication, verite, expression authentique',
    shadow: 'Mensonge, peur de s\'exprimer, bavardage',
    affirmation: 'Je parle ma verite avec clarte et amour',
    crystals: ['Turquoise', 'Lapis-lazuli', 'Aigue-marine'],
    oils: ['Eucalyptus', 'Menthe poivree', 'Camomille'],
    yoga: ['Sarvangasana', 'Halasana'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 6 (666Hz): Ajna (Third Eye) ---
  {
    level: 6 as ResonanceLevel,
    atomHz: 666,
    chakraNumber: 6,
    name: 'Ajna',
    meaning: 'Commandement / Perception',
    sanskrit: '\u0906\u091C\u094D\u091E\u093E',
    location: 'Entre les sourcils',
    element: 'Light',
    color: '#4B0082',
    mantra: 'OM',
    solfeggioHz: 852,
    solfeggioMeaning: 'Intuition, eveil spirituel',
    note: 'La',
    petals: 96,
    symbol: 'Triangle inverse avec oeil',
    gland: 'Hypophyse (Pituitaire)',
    quality: 'Intuition, sagesse, vision interieure',
    shadow: 'Illusion, deni, confusion mentale',
    affirmation: 'Je vois clairement au-dela des apparences',
    crystals: ['Amethyste', 'Fluorite', 'Sodalite'],
    oils: ['Lavande', 'Encens', 'Sauge'],
    yoga: ['Balasana', 'Trataka'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 7 (777Hz): Sahasrara (Crown) ---
  {
    level: 7 as ResonanceLevel,
    atomHz: 777,
    chakraNumber: 7,
    name: 'Sahasrara',
    meaning: 'Mille petales',
    sanskrit: '\u0938\u0939\u0938\u094D\u0930\u093E\u0930',
    location: 'Sommet du crane',
    element: 'Cosmic',
    color: '#EE82EE',
    mantra: 'Silence',
    solfeggioHz: 963,
    solfeggioMeaning: 'Illumination, connexion divine',
    note: 'Si',
    petals: 1000,
    symbol: 'Lotus aux mille petales',
    gland: 'Epiphyse (Pineale)',
    quality: 'Illumination, connexion divine, transcendance',
    shadow: 'Deconnexion spirituelle, materialisme extreme',
    affirmation: 'Je suis un avec l\'univers',
    crystals: ['Quartz clair', 'Diamant', 'Selenite'],
    oils: ['Lotus', 'Encens', 'Myrrhe'],
    yoga: ['Savasana', 'Meditation'],
    isCenter: false,
    isHarmonic: false,
  },
  // --- Level 8 (888Hz): Anahata Harmonic (Heart expanded) ---
  {
    level: 8 as ResonanceLevel,
    atomHz: 888,
    chakraNumber: 4,
    name: 'Anahata',
    meaning: 'Coeur expanse -- harmonique superieure',
    sanskrit: '\u0905\u0928\u093E\u0939\u0924',
    location: 'Centre de la poitrine (rayonnement etendu)',
    element: 'Air',
    color: '#50C878',
    mantra: 'YAM',
    solfeggioHz: 639,
    solfeggioMeaning: 'Connexion, relations harmonieuses (octave superieure)',
    note: 'Fa',
    petals: 12,
    symbol: 'Etoile a 6 branches (Hexagramme)',
    gland: 'Thymus',
    quality: 'Amour cosmique, compassion universelle, infini',
    shadow: 'Attachement au materiel, fermeture du coeur',
    affirmation: 'Mon coeur rayonne l\'amour infini',
    crystals: ['Quartz rose', 'Aventurine', 'Malachite'],
    oils: ['Rose', 'Geranium', 'Bergamote'],
    yoga: ['Ustrasana', 'Bhujangasana'],
    isCenter: false,
    isHarmonic: true,
  },
  // --- Level 9 (999Hz): Sahasrara Transcendent (Unity) ---
  {
    level: 9 as ResonanceLevel,
    atomHz: 999,
    chakraNumber: 7,
    name: 'Sahasrara',
    meaning: 'Unite transcendante -- Conscience divine',
    sanskrit: '\u0938\u0939\u0938\u094D\u0930\u093E\u0930',
    location: 'Au-dela du sommet du crane (champ unifie)',
    element: 'Cosmic',
    color: '#EE82EE',
    mantra: 'Silence',
    solfeggioHz: 963,
    solfeggioMeaning: 'Illumination, connexion a la Source',
    note: 'Si',
    petals: 1000,
    symbol: 'Lotus aux mille petales',
    gland: 'Epiphyse (Pineale)',
    quality: 'Unite absolue, conscience universelle, Source',
    shadow: 'Deconnexion totale du physique',
    affirmation: 'Je suis la Source, la Source est moi',
    crystals: ['Quartz clair', 'Diamant', 'Selenite'],
    oils: ['Lotus', 'Encens', 'Myrrhe'],
    yoga: ['Savasana', 'Meditation profonde'],
    isCenter: false,
    isHarmonic: true,
  },
];

// =================================================================
// UTILITY: Harmonic Mean of AT-OM and Solfeggio frequencies
// =================================================================

/**
 * Computes the harmonic mean between an AT-OM frequency and a Solfeggio
 * frequency using the geometric mean formula: sqrt(atomHz * solfeggioHz).
 *
 * This creates the "bridge frequency" that unites the AT-OM vibrational
 * system with the ancient Solfeggio healing scale.
 */
export function harmonizeFrequency(atomHz: number, solfeggioHz: number): number {
  return Math.sqrt(atomHz * solfeggioHz);
}

// =================================================================
// CHAKRA INPUT TYPE
// =================================================================

export interface ChakraInput {
  /** Optional text to compute Arithmos resonance level */
  text?: string;
  /** Direct level input (1-9) */
  level?: ResonanceLevel;
  /** Include healing recommendations in output */
  include_healing?: boolean;
}

// =================================================================
// INTERNAL HELPERS
// =================================================================

/**
 * Resolves a ChakraInput to a concrete ResonanceLevel.
 * Priority: explicit level > computed Arithmos from text > default (4 = Heart).
 */
function resolveLevel(input: ChakraInput): ResonanceLevel {
  if (input.level !== undefined) {
    const clamped = Math.max(1, Math.min(9, input.level));
    return clamped as ResonanceLevel;
  }
  if (input.text) {
    return RosettaParser.computeArithmos(input.text);
  }
  // Default: Heart center (level 4)
  return 4 as ResonanceLevel;
}

/**
 * Retrieves the ChakraDatum for a given resonance level.
 */
function getChakraForLevel(level: ResonanceLevel): ChakraDatum {
  return CHAKRA_DATA.find(c => c.level === level) ?? CHAKRA_DATA[3]; // fallback: Heart
}

/**
 * Maps a resonance level to its SacredGeometryShape.
 */
function geometryForLevel(level: ResonanceLevel): SacredGeometryShape {
  return RosettaParser.geometryFor(level);
}

/**
 * Computes the energetic balance between the AT-OM Hz and the chakra's
 * native atom frequency. Returns 0..1 where 1 is perfect resonance.
 */
function computeBalance(atomHz: number, chakraAtomHz: number): number {
  const raw = 1 - Math.abs(atomHz - chakraAtomHz) / 888;
  return Math.max(0, Math.min(1, raw));
}

/**
 * Returns a healing recommendation object based on balance level.
 */
function getHealingGuidance(
  chakra: ChakraDatum,
  balance: number,
): { status: string; message: string; practice: string } {
  if (balance > 0.8) {
    return {
      status: 'Harmonise',
      message: `Votre ${chakra.name} est en resonance parfaite.`,
      practice: `Maintenez avec le mantra "${chakra.mantra}".`,
    };
  }
  if (balance > 0.5) {
    return {
      status: 'En equilibrage',
      message: `Votre ${chakra.name} s'harmonise progressivement.`,
      practice: `Pratiquez ${chakra.yoga[0]} et utilisez ${chakra.crystals[0]}.`,
    };
  }
  return {
    status: 'A renforcer',
    message: `Votre ${chakra.name} a besoin d'attention.`,
    practice: `Meditation sur le mantra ${chakra.mantra}, couleur ${chakra.color}.`,
  };
}

// =================================================================
// CHAKRA TEMPLATE -- TranslatorTemplate<ChakraInput>
// =================================================================

export const ChakraTemplate: TranslatorTemplate<ChakraInput> = {
  domain: 'chakra',

  // ---------------------------------------------------------------
  // TECH (Grec) -- Structured JSON for smart contracts / APIs
  // ---------------------------------------------------------------
  toTech(input: ChakraInput, ctx: ParserContext): TechPayload {
    const level = resolveLevel(input);
    const chakra = getChakraForLevel(level);
    const resonance = RESONANCE_MATRIX[level];
    const harmonicMean = harmonizeFrequency(chakra.atomHz, chakra.solfeggioHz);
    const balance = computeBalance(resonance.hz, chakra.atomHz);

    const values: Record<string, unknown> = {
      chakra_number: chakra.chakraNumber,
      chakra_name: chakra.name,
      sanskrit: chakra.sanskrit,
      resonance_level: level,
      atom_frequency_hz: chakra.atomHz,
      solfeggio_frequency_hz: chakra.solfeggioHz,
      harmonic_mean_hz: Math.round(harmonicMean * 100) / 100,
      element: chakra.element,
      color: chakra.color,
      mantra: chakra.mantra,
      note: chakra.note,
      location: chakra.location,
      is_center: chakra.isCenter,
      is_harmonic: chakra.isHarmonic,
      balance: Math.round(balance * 1000) / 1000,
      system_frequency: ctx.system_frequency,
      computed_from: input.text ?? null,
    };

    if (input.include_healing) {
      const guidance = getHealingGuidance(chakra, balance);
      values.healing = {
        status: guidance.status,
        crystals: chakra.crystals,
        essential_oils: chakra.oils,
        yoga_poses: chakra.yoga,
        affirmation: chakra.affirmation,
        practice: guidance.practice,
      };
    }

    return {
      schema_version: '1.0',
      data_type: 'chakra',
      values,
      timestamp: ctx.timestamp,
    };
  },

  // ---------------------------------------------------------------
  // PEOPLE (Demotique) -- Narrative in French with healing guidance
  // ---------------------------------------------------------------
  toPeople(input: ChakraInput, ctx: ParserContext): PeoplePayload {
    const level = resolveLevel(input);
    const chakra = getChakraForLevel(level);
    const harmonicMean = harmonizeFrequency(chakra.atomHz, chakra.solfeggioHz);
    const balance = computeBalance(RESONANCE_MATRIX[level].hz, chakra.atomHz);
    const guidance = getHealingGuidance(chakra, balance);

    // Build the main narrative
    const source = input.text
      ? `Le mot "${input.text}" vibre au niveau ${level}`
      : `Le niveau ${level}`;

    const centerNote = chakra.isCenter
      ? ' C\'est le point d\'ancrage central du systeme AT\u00B7OM, le coeur qui unit toutes les dimensions.'
      : '';

    const harmonicNote = chakra.isHarmonic
      ? ` Ce niveau est une harmonique superieure : ${chakra.meaning}.`
      : '';

    const narrative =
      `${source}, activant le chakra ${chakra.name} (${chakra.meaning}), ` +
      `situe au niveau de ${chakra.location.toLowerCase()}. ` +
      `Son element est ${chakra.element}, sa couleur ${chakra.color}. ` +
      `La frequence AT\u00B7OM de ${chakra.atomHz} Hz se marie avec le Solfege sacre ` +
      `a ${chakra.solfeggioHz} Hz (${chakra.solfeggioMeaning}), ` +
      `creant une frequence harmonisee de ${Math.round(harmonicMean * 10) / 10} Hz.` +
      centerNote +
      harmonicNote;

    const explanation =
      `Le chakra ${chakra.name} gouverne : ${chakra.quality}. ` +
      `Son ombre : ${chakra.shadow}. ` +
      `Affirmation : "${chakra.affirmation}".`;

    const guide_steps: string[] = [
      `Repetez le mantra "${chakra.mantra}" en vous concentrant sur ${chakra.location.toLowerCase()}.`,
      `Visualisez la couleur ${chakra.color} irradiant depuis ce centre.`,
      `Ecoutez la frequence harmonisee de ${Math.round(harmonicMean * 10) / 10} Hz.`,
    ];

    if (input.include_healing) {
      guide_steps.push(
        `Cristaux recommandes : ${chakra.crystals.join(', ')}.`,
        `Huiles essentielles : ${chakra.oils.join(', ')}.`,
        `Postures de yoga : ${chakra.yoga.join(', ')}.`,
        `Conseil : ${guidance.practice}`,
      );
    }

    // Determine emotional tone
    let emotional_tone: PeoplePayload['emotional_tone'];
    if (chakra.isCenter) {
      emotional_tone = 'sacre';
    } else if (balance > 0.8) {
      emotional_tone = 'celebratoire';
    } else if (balance > 0.5) {
      emotional_tone = 'encourageant';
    } else {
      emotional_tone = 'alerte';
    }

    return {
      narrative,
      explanation,
      guide_steps,
      emotional_tone,
      language: 'fr',
    };
  },

  // ---------------------------------------------------------------
  // SPIRIT (Hieroglyphe) -- Frequency, geometry, vibration signature
  // ---------------------------------------------------------------
  toSpirit(input: ChakraInput, _ctx: ParserContext): SpiritPayload {
    const level = resolveLevel(input);
    const chakra = getChakraForLevel(level);
    const resonance = RESONANCE_MATRIX[level];

    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: chakra.color,
      sacred_geometry: geometryForLevel(level),
      vibration_signature: [
        SACRED_FREQUENCIES.ATOM_M,   // 44.4   -- Masse / Matiere
        SACRED_FREQUENCIES.ATOM_P,   // 161.8  -- Puissance / Phi
        SACRED_FREQUENCIES.ATOM_I,   // 369    -- Intensite / Tesla
        SACRED_FREQUENCIES.ATOM_PO,  // 1728   -- Position / Polarite
      ],
      phi_ratio: SACRED_FREQUENCIES.PHI,
    };
  },
};
