/**
 * AT·OM -- KabbaleTemplate
 * Moteur Kabbalistique traduit en TranslatorTemplate Rosetta
 *
 * Cartographie des 10 Sephiroth sur les 9 niveaux AT·OM (Arithmos 1-9).
 * Yesod (Fondation) est absorbe dans Malkhut, comprimant l'Arbre
 * classique en 9 echelons resonants.
 *
 * 22 Sentiers relient les Sephiroth (Arcanes Majeurs / lettres hebraiques).
 * 3 Piliers : Severite (gauche), Misericorde (droite), Equilibre (centre).
 * 4 Mondes  : Atziluth, Briah, Yetzirah, Assiah.
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
// TYPES KABBALISTIQUES
// =================================================================

export type Pillar = 'SEVERITY' | 'MERCY' | 'EQUILIBRIUM';
export type World = 'ATZILUTH' | 'BRIAH' | 'YETZIRAH' | 'ASSIAH';

export interface Sephirah {
  index: number;           // 1-10 classique (Malkuth=10 .. Kether=1)
  arithmos: ResonanceLevel; // Niveau AT·OM 1-9
  name: string;
  nameHebrew: string;
  meaning: string;
  color: string;
  pillar: Pillar;
  world: World;
  position: { x: number; y: number }; // Coordonnees SVG normalisees (0-100)
  divineName: string;
  archangel: string;
  quality: string;
  shadow: string;
}

export interface KabbalePath {
  index: number;           // 1-22
  from: number;            // Sephirah classique index (1-10)
  to: number;              // Sephirah classique index (1-10)
  hebrewLetter: string;
  letterName: string;
  tarot: string;
}

export interface KabbaleInput {
  text?: string;
  level?: ResonanceLevel;
  include_paths?: boolean;
}

// =================================================================
// PILIERS
// =================================================================

export const PILLARS: Record<Pillar, {
  name: string;
  nameFr: string;
  polarity: string;
  description: string;
}> = {
  SEVERITY: {
    name: 'Pillar of Severity',
    nameFr: 'Pilier de la Severite',
    polarity: 'feminine',
    description: 'Force restrictive, forme, jugement, structure. Le pilier gauche canalise et delimite.',
  },
  MERCY: {
    name: 'Pillar of Mercy',
    nameFr: 'Pilier de la Misericorde',
    polarity: 'masculine',
    description: 'Force expansive, grace, abondance, ouverture. Le pilier droit donne et rayonne.',
  },
  EQUILIBRIUM: {
    name: 'Pillar of Equilibrium',
    nameFr: 'Pilier de l\'Equilibre',
    polarity: 'balance',
    description: 'Conscience unificatrice, synthese, chemin du milieu. Le pilier central harmonise.',
  },
};

// =================================================================
// 4 MONDES
// =================================================================

export const WORLDS: Record<World, {
  name: string;
  nameFr: string;
  element: string;
  description: string;
  sephirothRange: string;
}> = {
  ATZILUTH: {
    name: 'Atziluth',
    nameFr: 'Atziluth -- Monde de l\'Emanation',
    element: 'Feu',
    description: 'Le plan divin, monde archetypal des causes premieres. Pure volonte creatrice.',
    sephirothRange: 'Kether, Chokmah, Binah',
  },
  BRIAH: {
    name: 'Briah',
    nameFr: 'Briah -- Monde de la Creation',
    element: 'Eau',
    description: 'Le plan creatif, monde des archanges et des grandes idees. Intelligence formatrice.',
    sephirothRange: 'Chesed, Geburah, Tiphereth',
  },
  YETZIRAH: {
    name: 'Yetzirah',
    nameFr: 'Yetzirah -- Monde de la Formation',
    element: 'Air',
    description: 'Le plan astral et emotionnel, monde des anges. Les formes se precisent.',
    sephirothRange: 'Netzach, Hod, (Yesod)',
  },
  ASSIAH: {
    name: 'Assiah',
    nameFr: 'Assiah -- Monde de l\'Action',
    element: 'Terre',
    description: 'Le plan physique et materiel. Manifestation concrete dans la realite tangible.',
    sephirothRange: 'Malkhut',
  },
};

// =================================================================
// 10 SEPHIROTH (mappes sur 9 niveaux AT·OM)
// =================================================================

export const SEPHIROTH_DATA: Sephirah[] = [
  {
    index: 10,
    arithmos: 1 as ResonanceLevel,
    name: 'Malkhut',
    nameHebrew: '\u05DE\u05DC\u05DB\u05D5\u05EA',
    meaning: 'Kingdom',
    color: '#000000',
    pillar: 'EQUILIBRIUM',
    world: 'ASSIAH',
    position: { x: 50, y: 95 },
    divineName: 'Adonai Ha-Aretz',
    archangel: 'Sandalphon',
    quality: 'Ancrage, manifestation, presence physique',
    shadow: 'Inertie, materialisme excessif, deconnexion du sacre',
  },
  {
    index: 9,
    arithmos: 2 as ResonanceLevel,
    name: 'Netzach',
    nameHebrew: '\u05E0\u05E6\u05D7',
    meaning: 'Victory',
    color: '#00FF00',
    pillar: 'MERCY',
    world: 'YETZIRAH',
    position: { x: 75, y: 72 },
    divineName: 'YHVH Tzabaoth',
    archangel: 'Haniel',
    quality: 'Amour, passion, creativite artistique, desir',
    shadow: 'Luxure, dependance affective, illusions romantiques',
  },
  {
    index: 8,
    arithmos: 3 as ResonanceLevel,
    name: 'Hod',
    nameHebrew: '\u05D4\u05D5\u05D3',
    meaning: 'Splendor',
    color: '#FF8C00',
    pillar: 'SEVERITY',
    world: 'YETZIRAH',
    position: { x: 25, y: 72 },
    divineName: 'Elohim Tzabaoth',
    archangel: 'Michael',
    quality: 'Intellect, communication, analyse, magie pratique',
    shadow: 'Sur-intellectualisation, malhonnetete, manipulation mentale',
  },
  {
    index: 6,
    arithmos: 4 as ResonanceLevel,
    name: 'Tiphereth',
    nameHebrew: '\u05EA\u05E4\u05D0\u05E8\u05EA',
    meaning: 'Beauty',
    color: '#FFD700',
    pillar: 'EQUILIBRIUM',
    world: 'BRIAH',
    position: { x: 50, y: 50 },
    divineName: 'YHVH Eloah Va-Daath',
    archangel: 'Raphael',
    quality: 'Harmonie, beaute, equilibre du coeur, compassion',
    shadow: 'Orgueil spirituel, inflation de l\'ego, fausse lumiere',
  },
  {
    index: 5,
    arithmos: 5 as ResonanceLevel,
    name: 'Geburah',
    nameHebrew: '\u05D2\u05D1\u05D5\u05E8\u05D4',
    meaning: 'Strength',
    color: '#FF0000',
    pillar: 'SEVERITY',
    world: 'BRIAH',
    position: { x: 25, y: 42 },
    divineName: 'Elohim Gibor',
    archangel: 'Khamael',
    quality: 'Force, justice, courage, purification',
    shadow: 'Cruaute, destruction aveugle, colere incontr\u00f4lee',
  },
  {
    index: 4,
    arithmos: 6 as ResonanceLevel,
    name: 'Chesed',
    nameHebrew: '\u05D7\u05E1\u05D3',
    meaning: 'Mercy',
    color: '#0000FF',
    pillar: 'MERCY',
    world: 'BRIAH',
    position: { x: 75, y: 42 },
    divineName: 'El',
    archangel: 'Tzadkiel',
    quality: 'Misericorde, abondance, generosite, vision',
    shadow: 'Exces de permissivite, gaspillage, faiblesse devant le mal',
  },
  {
    index: 3,
    arithmos: 7 as ResonanceLevel,
    name: 'Binah',
    nameHebrew: '\u05D1\u05D9\u05E0\u05D4',
    meaning: 'Understanding',
    color: '#000000',
    pillar: 'SEVERITY',
    world: 'ATZILUTH',
    position: { x: 25, y: 15 },
    divineName: 'YHVH Elohim',
    archangel: 'Tzaphkiel',
    quality: 'Comprehension profonde, matrice universelle, silence',
    shadow: 'Rigidite, tristesse cosmique, limitation excessive',
  },
  {
    index: 2,
    arithmos: 8 as ResonanceLevel,
    name: 'Chokmah',
    nameHebrew: '\u05D7\u05DB\u05DE\u05D4',
    meaning: 'Wisdom',
    color: '#808080',
    pillar: 'MERCY',
    world: 'ATZILUTH',
    position: { x: 75, y: 15 },
    divineName: 'Yah',
    archangel: 'Raziel',
    quality: 'Sagesse primordiale, eclair de genie, force vitale',
    shadow: 'Chaos, energie non canalisee, force brute sans direction',
  },
  {
    index: 1,
    arithmos: 9 as ResonanceLevel,
    name: 'Kether',
    nameHebrew: '\u05DB\u05EA\u05E8',
    meaning: 'Crown',
    color: '#FFFFFF',
    pillar: 'EQUILIBRIUM',
    world: 'ATZILUTH',
    position: { x: 50, y: 2 },
    divineName: 'Ehyeh Asher Ehyeh',
    archangel: 'Metatron',
    quality: 'Unite absolue, source de toute emanation, couronne divine',
    shadow: 'Neant, dissolution totale de l\'individualite',
  },
];

// =================================================================
// 22 SENTIERS (Arcanes Majeurs / Lettres hebraiques)
// =================================================================

export const PATHS: KabbalePath[] = [
  { index: 1,  from: 1,  to: 2,  hebrewLetter: '\u05D0', letterName: 'Aleph',   tarot: 'Le Mat' },
  { index: 2,  from: 1,  to: 3,  hebrewLetter: '\u05D1', letterName: 'Beth',    tarot: 'Le Bateleur' },
  { index: 3,  from: 1,  to: 6,  hebrewLetter: '\u05D2', letterName: 'Gimel',   tarot: 'La Papesse' },
  { index: 4,  from: 2,  to: 3,  hebrewLetter: '\u05D3', letterName: 'Daleth',  tarot: 'L\'Imperatrice' },
  { index: 5,  from: 2,  to: 6,  hebrewLetter: '\u05D4', letterName: 'He',      tarot: 'L\'Empereur' },
  { index: 6,  from: 2,  to: 4,  hebrewLetter: '\u05D5', letterName: 'Vav',     tarot: 'Le Pape' },
  { index: 7,  from: 3,  to: 6,  hebrewLetter: '\u05D6', letterName: 'Zayin',   tarot: 'L\'Amoureux' },
  { index: 8,  from: 3,  to: 5,  hebrewLetter: '\u05D7', letterName: 'Cheth',   tarot: 'Le Chariot' },
  { index: 9,  from: 4,  to: 5,  hebrewLetter: '\u05D8', letterName: 'Teth',    tarot: 'La Justice' },
  { index: 10, from: 4,  to: 6,  hebrewLetter: '\u05D9', letterName: 'Yod',     tarot: 'L\'Ermite' },
  { index: 11, from: 4,  to: 9,  hebrewLetter: '\u05DA', letterName: 'Kaph',    tarot: 'La Roue de Fortune' },
  { index: 12, from: 5,  to: 6,  hebrewLetter: '\u05DC', letterName: 'Lamed',   tarot: 'La Force' },
  { index: 13, from: 5,  to: 8,  hebrewLetter: '\u05DE', letterName: 'Mem',     tarot: 'Le Pendu' },
  { index: 14, from: 6,  to: 9,  hebrewLetter: '\u05E0', letterName: 'Nun',     tarot: 'La Mort' },
  { index: 15, from: 6,  to: 8,  hebrewLetter: '\u05E1', letterName: 'Samekh',  tarot: 'La Temperance' },
  { index: 16, from: 8,  to: 9,  hebrewLetter: '\u05E2', letterName: 'Ayin',    tarot: 'Le Diable' },
  { index: 17, from: 9,  to: 10, hebrewLetter: '\u05E4', letterName: 'Pe',      tarot: 'La Maison Dieu' },
  { index: 18, from: 9,  to: 8,  hebrewLetter: '\u05E6', letterName: 'Tsade',   tarot: 'L\'Etoile' },
  { index: 19, from: 9,  to: 10, hebrewLetter: '\u05E7', letterName: 'Qoph',    tarot: 'La Lune' },
  { index: 20, from: 8,  to: 10, hebrewLetter: '\u05E8', letterName: 'Resh',    tarot: 'Le Soleil' },
  { index: 21, from: 6,  to: 10, hebrewLetter: '\u05E9', letterName: 'Shin',    tarot: 'Le Jugement' },
  { index: 22, from: 3,  to: 4,  hebrewLetter: '\u05EA', letterName: 'Tav',     tarot: 'Le Monde' },
];

// =================================================================
// HELPERS INTERNES
// =================================================================

/** Trouve la Sephirah correspondant a un niveau AT·OM (arithmos 1-9) */
function sephirahByArithmos(level: ResonanceLevel): Sephirah {
  const found = SEPHIROTH_DATA.find(s => s.arithmos === level);
  if (!found) {
    // Fallback : Malkhut pour tout niveau non mappe
    return SEPHIROTH_DATA[0];
  }
  return found;
}

/** Retourne les sentiers connectes a une Sephirah (par index classique) */
function pathsForSephirah(sephirahIndex: number): KabbalePath[] {
  return PATHS.filter(p => p.from === sephirahIndex || p.to === sephirahIndex);
}

/** Mappe le nombre de Sephiroth (10) sur les geometries sacrees */
function geometryForSephirothCount(count: number): SacredGeometryShape {
  const map: Record<number, SacredGeometryShape> = {
    1: 'point',
    2: 'vesica_piscis',
    3: 'triangle',
    4: 'tetrahedron',
    5: 'pentagram',
    6: 'hexagram',
    7: 'heptagram',
    8: 'octahedron',
    9: 'enneagram',
    10: 'metatron_cube',
  };
  return map[count] ?? 'flower_of_life';
}

/** Determine le niveau (arithmos) depuis le texte ou la valeur explicite */
function resolveLevel(input: KabbaleInput): ResonanceLevel {
  if (input.level) {
    return input.level;
  }
  if (input.text) {
    return RosettaParser.computeArithmos(input.text);
  }
  return 1 as ResonanceLevel;
}

// =================================================================
// KABBALE TEMPLATE -- Implementation TranslatorTemplate
// =================================================================

export const KabbaleTemplate: TranslatorTemplate<KabbaleInput> = {
  domain: 'kabbale',

  // ---------------------------------------------------------------
  // TECH -- Donnees structurees pour smart contracts / API
  // ---------------------------------------------------------------
  toTech(input: KabbaleInput, context: ParserContext): TechPayload {
    const level = resolveLevel(input);
    const sephirah = sephirahByArithmos(level);
    const connectedPaths = pathsForSephirah(sephirah.index);
    const worldData = WORLDS[sephirah.world];
    const pillarData = PILLARS[sephirah.pillar];

    const values: Record<string, unknown> = {
      sephirah: {
        index: sephirah.index,
        arithmos: sephirah.arithmos,
        name: sephirah.name,
        nameHebrew: sephirah.nameHebrew,
        meaning: sephirah.meaning,
        color: sephirah.color,
      },
      world: {
        name: sephirah.world,
        element: worldData.element,
      },
      pillar: {
        name: sephirah.pillar,
        polarity: pillarData.polarity,
      },
      position: sephirah.position,
      divine_name: sephirah.divineName,
      archangel: sephirah.archangel,
      source_text: input.text ?? null,
      computed_level: level,
    };

    if (input.include_paths) {
      values.connected_paths = connectedPaths.map(p => ({
        index: p.index,
        from: p.from,
        to: p.to,
        letter: p.hebrewLetter,
        letter_name: p.letterName,
        tarot: p.tarot,
      }));
      values.path_count = connectedPaths.length;
    }

    return {
      schema_version: '1.0',
      data_type: 'kabbale_sephirah',
      values,
      timestamp: context.timestamp,
    };
  },

  // ---------------------------------------------------------------
  // PEOPLE -- Recit narratif en francais
  // ---------------------------------------------------------------
  toPeople(input: KabbaleInput, _context: ParserContext): PeoplePayload {
    const level = resolveLevel(input);
    const sephirah = sephirahByArithmos(level);
    const worldData = WORLDS[sephirah.world];
    const pillarData = PILLARS[sephirah.pillar];
    const connectedPaths = pathsForSephirah(sephirah.index);

    const textIntro = input.text
      ? `Le mot "${input.text}" vibre au niveau ${level}, resonant avec la Sephirah ${sephirah.name}.`
      : `Au niveau ${level} de l'Arbre de Vie se tient la Sephirah ${sephirah.name}.`;

    const narrative = [
      textIntro,
      `${sephirah.name} (${sephirah.nameHebrew}) signifie "${sephirah.meaning}" -- ${sephirah.quality}.`,
      `Elle appartient au ${pillarData.nameFr} et au monde de ${worldData.nameFr}.`,
      `Son Nom Divin est ${sephirah.divineName}, et son Archange est ${sephirah.archangel}.`,
    ].join(' ');

    const guide_steps = [
      `Sephirah : ${sephirah.name} -- ${sephirah.meaning} (Arithmos ${level})`,
      `Pilier : ${pillarData.nameFr} (${pillarData.polarity})`,
      `Monde : ${worldData.nameFr} -- Element ${worldData.element}`,
      `Qualite lumineuse : ${sephirah.quality}`,
      `Ombre a transmuter : ${sephirah.shadow}`,
      `Guidance : Meditez sur le Nom Divin "${sephirah.divineName}" pour activer cette Sephirah. Invoquez ${sephirah.archangel} pour recevoir son aide.`,
    ];

    if (input.include_paths && connectedPaths.length > 0) {
      guide_steps.push(
        `Sentiers connectes (${connectedPaths.length}) : ` +
        connectedPaths.map(p => `${p.letterName} (${p.hebrewLetter}) -- ${p.tarot}`).join(', ')
      );
    }

    // Tone depends on position in the Tree
    let tone: PeoplePayload['emotional_tone'];
    if (sephirah.world === 'ATZILUTH') {
      tone = 'sacre';
    } else if (sephirah.world === 'BRIAH') {
      tone = 'celebratoire';
    } else if (sephirah.world === 'YETZIRAH') {
      tone = 'encourageant';
    } else {
      tone = 'neutre';
    }

    return {
      narrative,
      explanation: `${sephirah.name} est la ${sephirah.index}e Sephirah de l'Arbre de Vie, mappee au niveau ${level} dans le systeme AT\u00b7OM. ${worldData.description}`,
      guide_steps,
      emotional_tone: tone,
      language: 'fr',
    };
  },

  // ---------------------------------------------------------------
  // SPIRIT -- Frequences, geometrie sacree, signature vibratoire
  // ---------------------------------------------------------------
  toSpirit(input: KabbaleInput, _context: ParserContext): SpiritPayload {
    const level = resolveLevel(input);
    const sephirah = sephirahByArithmos(level);
    const resonance = RESONANCE_MATRIX[level];

    // Frequence = niveau x 111 (alignee sur la matrice de resonance AT·OM)
    const frequency = level * 111;

    // Geometrie sacree mappee sur le nombre de Sephiroth dans l'Arbre (10 = Metatron Cube)
    // On utilise aussi le niveau individuel pour la forme de la Sephirah
    const geometry = geometryForSephirothCount(sephirah.index);

    // Signature vibratoire [M, P, I, Po] modulee par la position dans l'Arbre
    const positionFactor = sephirah.position.y / 100; // 0 (haut/Kether) -> 1 (bas/Malkhut)
    const vibration_signature: [number, number, number, number] = [
      SACRED_FREQUENCIES.ATOM_M * (1 + (1 - positionFactor)),
      SACRED_FREQUENCIES.ATOM_P * (1 + positionFactor * SACRED_FREQUENCIES.PHI),
      SACRED_FREQUENCIES.ATOM_I * level,
      SACRED_FREQUENCIES.ATOM_PO / (sephirah.index || 1),
    ];

    return {
      frequency_hz: frequency,
      resonance_level: level,
      color: sephirah.color,
      sacred_geometry: geometry,
      vibration_signature,
      phi_ratio: SACRED_FREQUENCIES.PHI,
    };
  },
};
