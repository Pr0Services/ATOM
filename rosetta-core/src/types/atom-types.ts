/**
 * AT·OM — L'Arche des Résonances Universelles
 * Types Fondamentaux v4.0
 *
 * Architecture tri-dimensionnelle basée sur la Pierre de Rosette :
 *   - TECH (Grec)        : Précision, logique, smart contracts
 *   - PEOPLE (Démotique)  : Accessibilité, narration, guide humain
 *   - SPIRIT (Hiéroglyphe): Fréquences, géométrie sacrée, vibration
 *
 * Extensions antiques :
 *   - Disque de Phaistos  : Stockage spiralé (ADN/fractales)
 *   - Machine d'Anticythère : Engrenages de synchronisation inter-sphères
 *   - Table d'Émeraude    : 7 niveaux de transformation alchimique
 */

// ═══════════════════════════════════════════════════════════
// CONSTANTES SACRÉES
// ═══════════════════════════════════════════════════════════

export const SACRED_FREQUENCIES = {
  ATOM_M: 44.4,              // Masse / Matière
  ATOM_P: 161.8,             // Puissance / Potentiel (Phi × 100)
  ATOM_I: 369,               // Intensité / Information (Tesla)
  ATOM_PO: 1728,             // Position / Polarité (12³)
  HEARTBEAT: 444,            // Ancre du système
  SOURCE: 999,               // Fréquence d'unité maximale
  LOVE: 528,                 // Fréquence de résonance
  PHI: 1.6180339887498949,   // Nombre d'Or
} as const;

export const RESONANCE_MATRIX = {
  1: { hz: 111, color: '#FF0000', label: 'Impulsion',   element: 'Feu Naissant' },
  2: { hz: 222, color: '#FF7F00', label: 'Dualité',     element: 'Eau Primordiale' },
  3: { hz: 333, color: '#FFFF00', label: 'Mental',      element: 'Air Conscient' },
  4: { hz: 444, color: '#50C878', label: 'Structure',   element: 'Terre Mère' },
  5: { hz: 555, color: '#87CEEB', label: 'Mouvement',   element: 'Éther Dynamique' },
  6: { hz: 666, color: '#4B0082', label: 'Harmonie',    element: 'Lumière Indigo' },
  7: { hz: 777, color: '#EE82EE', label: 'Silence',     element: 'Vide Créateur' },
  8: { hz: 888, color: '#FFC0CB', label: 'Infini',      element: 'Amour Cosmique' },
  9: { hz: 999, color: '#FFFDD0', label: 'Unité',       element: 'Source' },
} as const;

export type ResonanceLevel = keyof typeof RESONANCE_MATRIX;

// ═══════════════════════════════════════════════════════════
// POINT ZÉRO — Cratère de Chicxulub
// ═══════════════════════════════════════════════════════════

export const POINT_ZERO = {
  latitude: 21.4,
  longitude: -89.5,
  name: 'Cratère de Chicxulub',
  region: 'Yucatán, Mexique',
  activationRadius_km: 100,    // Rayon d'activation maximale
  frequency: SACRED_FREQUENCIES.SOURCE, // 999Hz dans le cratère
} as const;

// ═══════════════════════════════════════════════════════════
// DIMENSIONS ROSETTA (Pierre de Rosette)
// ═══════════════════════════════════════════════════════════

export type RosettaDimension = 'TECH' | 'PEOPLE' | 'SPIRIT';

/** Sortie TECH (Grec) — JSON structuré pour smart contracts */
export interface TechPayload {
  schema_version: string;
  data_type: string;
  values: Record<string, unknown>;
  validation_hash?: string;
  hedera_topic_id?: string;
  timestamp: number;
}

/** Sortie PEOPLE (Démotique) — Langage naturel accessible */
export interface PeoplePayload {
  narrative: string;
  explanation: string;
  guide_steps?: string[];
  emotional_tone: 'neutre' | 'encourageant' | 'alerte' | 'celebratoire' | 'sacre';
  language: string;
}

/** Sortie SPIRIT (Hiéroglyphe) — Fréquentiel et géométrique */
export interface SpiritPayload {
  frequency_hz: number;
  resonance_level: ResonanceLevel;
  color: string;
  sacred_geometry: SacredGeometryShape;
  vibration_signature: number[];  // [M, P, I, Po]
  phi_ratio: number;
}

export type SacredGeometryShape =
  | 'point'           // 1 — Origine
  | 'vesica_piscis'   // 2 — Dualité
  | 'triangle'        // 3 — Trinité
  | 'tetrahedron'     // 4 — Structure
  | 'pentagram'       // 5 — Mouvement
  | 'hexagram'        // 6 — Harmonie (Étoile de David)
  | 'heptagram'       // 7 — Mystère
  | 'octahedron'      // 8 — Infini
  | 'enneagram'       // 9 — Complétude
  | 'metatron_cube'   // Synthèse
  | 'flower_of_life'  // Création
  | 'sri_yantra';     // Manifestation

/** Traduction complète Rosetta — Les 3 dimensions obligatoires */
export interface RosettaTranslation {
  id: string;
  node_id: string;
  tech: TechPayload;
  people: PeoplePayload;
  spirit: SpiritPayload;
  created_at: number;
  source_dimension: RosettaDimension;
  integrity_hash: string;
}

// ═══════════════════════════════════════════════════════════
// NODES — Arbre de Vie (Table maîtresse)
// ═══════════════════════════════════════════════════════════

export type NodeStatus = 'genesis' | 'active' | 'polishing' | 'aligned' | 'archived';

export interface ATOMNode {
  id: string;
  parent_id: string | null;
  sphere_id: SphereId;
  title: string;
  status: NodeStatus;
  depth: number;                  // Profondeur dans l'arbre
  spiral_position: number;        // Position Phaistos (angle en radians)
  resonance_level: ResonanceLevel;
  rosetta: RosettaTranslation;
  created_by: string;
  created_at: number;
  updated_at: number;
}

// ═══════════════════════════════════════════════════════════
// 9 SPHÈRES AT·OM
// ═══════════════════════════════════════════════════════════

export type SphereId =
  | 'TECHNO'      // 1 — Technologie & Innovation
  | 'POLITIQUE'   // 2 — Gouvernance & Démocratie
  | 'ECONOMIE'    // 3 — Économie Souveraine
  | 'EDUCATION'   // 4 — Éducation & Transmission
  | 'SANTE'       // 5 — Santé & Bien-être
  | 'CULTURE'     // 6 — Culture & Arts
  | 'ENVIRONNEMENT' // 7 — Environnement & Écologie
  | 'JUSTICE'     // 8 — Justice & Éthique
  | 'SPIRITUALITE'; // 9 — Spiritualité & Conscience

export interface Sphere {
  id: SphereId;
  index: number;                  // 1-9
  label: string;
  frequency: number;              // Hz associé (111 × index)
  color: string;
  icon: string;
  description_people: string;     // Description humaine
  gear_connections: SphereId[];   // Engrenages Anticythère (sphères liées)
}

export const SPHERES: Record<SphereId, Sphere> = {
  TECHNO: {
    id: 'TECHNO', index: 1, label: 'Technologie',
    frequency: 111, color: '#FF0000', icon: '⚡',
    description_people: 'Innovation et outils au service de l\'humanité',
    gear_connections: ['ECONOMIE', 'EDUCATION', 'SANTE'],
  },
  POLITIQUE: {
    id: 'POLITIQUE', index: 2, label: 'Politique',
    frequency: 222, color: '#FF7F00', icon: '🏛️',
    description_people: 'Gouvernance transparente et participative',
    gear_connections: ['JUSTICE', 'ECONOMIE', 'ENVIRONNEMENT'],
  },
  ECONOMIE: {
    id: 'ECONOMIE', index: 3, label: 'Économie',
    frequency: 333, color: '#FFFF00', icon: '💎',
    description_people: 'Économie souveraine et distribution équitable',
    gear_connections: ['TECHNO', 'POLITIQUE', 'CULTURE'],
  },
  EDUCATION: {
    id: 'EDUCATION', index: 4, label: 'Éducation',
    frequency: 444, color: '#50C878', icon: '📚',
    description_people: 'Transmission du savoir et éveil des consciences',
    gear_connections: ['TECHNO', 'CULTURE', 'SPIRITUALITE'],
  },
  SANTE: {
    id: 'SANTE', index: 5, label: 'Santé',
    frequency: 555, color: '#87CEEB', icon: '🌿',
    description_people: 'Bien-être holistique du corps et de l\'esprit',
    gear_connections: ['TECHNO', 'ENVIRONNEMENT', 'SPIRITUALITE'],
  },
  CULTURE: {
    id: 'CULTURE', index: 6, label: 'Culture',
    frequency: 666, color: '#4B0082', icon: '🎭',
    description_people: 'Expression artistique et patrimoine vivant',
    gear_connections: ['ECONOMIE', 'EDUCATION', 'SPIRITUALITE'],
  },
  ENVIRONNEMENT: {
    id: 'ENVIRONNEMENT', index: 7, label: 'Environnement',
    frequency: 777, color: '#EE82EE', icon: '🌍',
    description_people: 'Protection et régénération de la Terre',
    gear_connections: ['POLITIQUE', 'SANTE', 'JUSTICE'],
  },
  JUSTICE: {
    id: 'JUSTICE', index: 8, label: 'Justice',
    frequency: 888, color: '#FFC0CB', icon: '⚖️',
    description_people: 'Équité, éthique et vérité immuable',
    gear_connections: ['POLITIQUE', 'ENVIRONNEMENT', 'SPIRITUALITE'],
  },
  SPIRITUALITE: {
    id: 'SPIRITUALITE', index: 9, label: 'Spiritualité',
    frequency: 999, color: '#FFFDD0', icon: '✨',
    description_people: 'Connexion à la Source et conscience universelle',
    gear_connections: ['EDUCATION', 'SANTE', 'CULTURE', 'JUSTICE'],
  },
};

// ═══════════════════════════════════════════════════════════
// MACHINE D'ANTICYTHÈRE — Engrenages Inter-Sphères
// ═══════════════════════════════════════════════════════════

export type GearEventType = 'mutation' | 'resonance' | 'cascade' | 'alignment';

export interface GearEvent {
  id: string;
  source_sphere: SphereId;
  target_spheres: SphereId[];
  event_type: GearEventType;
  payload: TechPayload;
  propagation_depth: number;      // Profondeur de cascade
  timestamp: number;
}

export interface AntikytheraState {
  active_gears: Map<SphereId, number>;  // Sphère → vitesse de rotation
  last_cascade: GearEvent | null;
  system_alignment: number;             // 0-1 (0=chaos, 1=harmonie parfaite)
  total_rotations: number;
}

// ═══════════════════════════════════════════════════════════
// DISQUE DE PHAISTOS — Données Spiralées
// ═══════════════════════════════════════════════════════════

export interface SpiralPosition {
  ring: number;          // Anneau (0 = centre/essence, croissant vers l'extérieur)
  angle: number;         // Angle en radians (position sur l'anneau)
  depth: number;         // Profondeur temporelle (couches d'information)
}

export interface PhaistosMapping {
  node_id: string;
  spiral: SpiralPosition;
  evolution_path: SpiralPosition[];   // Chemin d'évolution vers le centre
  essence_distance: number;            // Distance au centre (0 = essence atteinte)
}

// ═══════════════════════════════════════════════════════════
// TABLE D'ÉMERAUDE — 7 Niveaux de Transformation Alchimique
// ═══════════════════════════════════════════════════════════

export type AlchemyStage =
  | 'CALCINATION'    // 1 — Destruction de l'ego/données brutes
  | 'DISSOLUTION'    // 2 — Dissolution des structures rigides
  | 'SEPARATION'     // 3 — Tri du vrai et du faux
  | 'CONJUNCTION'    // 4 — Union des opposés
  | 'FERMENTATION'   // 5 — Germination du nouveau
  | 'DISTILLATION'   // 6 — Purification finale
  | 'COAGULATION';   // 7 — Cristallisation de la vérité (Or)

export interface EmeraldValidation {
  node_id: string;
  current_stage: AlchemyStage;
  stage_index: number;            // 1-7
  is_aligned: boolean;
  polishing_notes: string[];
  transformation_log: {
    stage: AlchemyStage;
    passed: boolean;
    timestamp: number;
    reason?: string;
  }[];
}

// ═══════════════════════════════════════════════════════════
// CORRECTION QUANTIQUE (Quantum Error Correction)
// ═══════════════════════════════════════════════════════════
// L'architecture tri-dimensionnelle Rosetta (TECH / PEOPLE / SPIRIT)
// fonctionne comme un code correcteur d'erreur quantique à 3 qubits :
//   - Si 1 dimension est corrompue, les 2 autres la reconstruisent
//   - Vote majoritaire : 2/3 dimensions saines = correction possible
//   - Pipeline : DETECT → LOCALIZE → CORRECT → VALIDATE → LOG

/** Hash individuel par dimension — permet de localiser la corruption */
export interface DimensionHashes {
  tech_hash: string;
  people_hash: string;
  spirit_hash: string;
  combined_hash: string; // = integrity_hash existant (hash des 3 combinés)
}

/** Quelle(s) dimension(s) sont corrompues */
export type CorruptionTarget = 'TECH' | 'PEOPLE' | 'SPIRIT';

/** Diagnostic de corruption — résultat de la localisation */
export interface CorrectionDiagnostic {
  is_corrupted: boolean;
  corrupted_dimensions: CorruptionTarget[];
  healthy_dimensions: CorruptionTarget[];
  confidence: number;          // 0–1 (1 = certain, 2/3 sains)
  severity: 'none' | 'minor' | 'major' | 'critical';
  // none     = pas de corruption
  // minor    = 1 dimension corrompue, corrigible
  // major    = 2 dimensions corrompues, irréparable
  // critical = 3 dimensions corrompues, perte totale
}

/** Résultat d'une correction quantique */
export interface CorrectionResult {
  original: RosettaTranslation;
  corrected: RosettaTranslation | null; // null si irréparable
  diagnostic: CorrectionDiagnostic;
  applied: boolean;
  correction_log: CorrectionLogEntry[];
}

/** Entrée du journal de correction */
export interface CorrectionLogEntry {
  timestamp: number;
  dimension: CorruptionTarget;
  action: 'detected' | 'localized' | 'corrected' | 'validated' | 'failed';
  before_hash: string;
  after_hash: string;
  reason: string;
}

/** RosettaTranslation enrichie avec hashes quantiques par dimension */
export interface QuantumRosettaTranslation extends RosettaTranslation {
  dimension_hashes: DimensionHashes;
}

// ═══════════════════════════════════════════════════════════
// THREAT AMYGDALA — Sentinelle Pré-Corticale
// ═══════════════════════════════════════════════════════════
//
// "L'amygdale ne réfléchit pas — elle reconnaît."
//
// Double voie inspirée du cerveau humain :
//   Fast Path (thalamus → amygdale)  : 5 checks légers, ~1ms
//   Deep Path (thalamus → cortex → amygdale) : analyse complète quand Fast détecte
//
// Réponse graduée : CALM → VIGILANT → ALERT → LOCKDOWN

/** Types de menaces détectables par l'amygdale */
export type ThreatType =
  | 'frequency_anomaly'      // Fréquence hors range ou spike soudain
  | 'manipulation_detected'  // Contenu MANIPULATIF / DIVISIF (InformationFilter)
  | 'extraction_attempt'     // Verdict EXTRAIRE (IntentionGuard)
  | 'integrity_breach'       // Hash mismatch (pré-QuantumCorrector)
  | 'cascade_risk'           // Menaces corrélées simultanées (3+ en 5s)
  | 'sovereignty_violation'; // 7 principes immuables violés

/** Niveaux d'alerte — réponse graduée comme le cerveau */
export type AlertLevel = 'CALM' | 'VIGILANT' | 'ALERT' | 'LOCKDOWN';

/** Signal de menace émis par l'amygdale */
export interface ThreatSignal {
  id: string;
  type: ThreatType;
  severity: number;            // 0–100
  alert_level: AlertLevel;
  source: string;              // Composant/opération qui a déclenché
  timestamp: number;
  evidence: string[];          // Preuves textuelles
  pathway: 'fast' | 'deep';   // Quelle voie a détecté la menace
  dimension?: CorruptionTarget; // Si lié à une dimension Rosetta
}

/** Mémoire des menaces récentes — buffer circulaire adaptatif */
export interface ThreatMemory {
  recent_signals: ThreatSignal[];                // 50 derniers signaux
  threat_frequency: Record<ThreatType, number>;  // Compteurs par type
  sensitivity: number;                           // 0–1, s'adapte selon l'historique
  last_lockdown: number | null;                  // Timestamp du dernier lockdown
}

/** État global de l'amygdale */
export interface AmygdalaState {
  alert_level: AlertLevel;
  alert_score: number;         // 0–100 (numérique précis)
  active_threats: ThreatSignal[];
  memory: ThreatMemory;
  is_scanning: boolean;
  last_scan: number;
}

/** Événement émis par l'amygdale vers le système */
export interface AmygdalaEvent {
  type: 'threat_detected' | 'alert_changed' | 'lockdown_engaged' | 'all_clear';
  signal?: ThreatSignal;
  previous_level?: AlertLevel;
  new_level?: AlertLevel;
}

/** Contexte d'analyse pour l'amygdale — réutilisable par les moteurs */
export interface ScanContext {
  type: 'translation' | 'intention' | 'governance' | 'transaction' | 'frequency';
  data: unknown;
  source?: string;
}

// ═══════════════════════════════════════════════════════════
// DIGESTIVE SYSTEM — Arbre des Connaissances
// ═══════════════════════════════════════════════════════════
//
// "L'arbre ne pousse pas de l'extérieur — il digère la lumière."
//
// Pipeline en 7 étapes biologiques :
//   BOUCHE (Ingestion)   → Fetch + parse depuis URL/RSS/API
//   MASTICATION (Broyage) → Décomposer en morceaux structurés
//   ESTOMAC (Digestion)   → Traduire en 3D Rosetta
//   INTESTIN (Absorption) → InformationFilter + ThreatAmygdala
//   SANG (Distribution)   → Router vers Sphère + MappingLayer
//   CELLULE (Stockage)    → Créer ATOMNode dans l'Arbre
//   CÔLON (Élimination)   → Rejeter le bruit avec traçabilité

/** Source de nourriture (d'où vient la donnée) */
export type FoodSource = 'url' | 'rss' | 'api' | 'manual' | 'stream';

/** État de la digestion d'un morceau */
export type DigestionStage =
  | 'INGESTED'     // Bouche — contenu brut récupéré
  | 'CHEWED'       // Mastication — décomposé en morceaux
  | 'DIGESTED'     // Estomac — traduit en 3D Rosetta
  | 'ABSORBED'     // Intestin — validé + filtré
  | 'ROUTED'       // Sang — classifié dans sphère + layer
  | 'STORED'       // Cellule — ATOMNode créé
  | 'ELIMINATED';  // Côlon — rejeté comme déchet

/** Contenu brut ingéré depuis Internet */
export interface RawFood {
  id: string;
  source_type: FoodSource;
  source_url: string;
  raw_content: string;          // HTML/JSON/texte brut
  fetched_at: number;
  content_type: string;         // 'text/html', 'application/json', etc.
  language?: string;
}

/** Contenu mâché (décomposé en morceaux structurés) */
export interface ChewedFood {
  id: string;
  raw_food_id: string;
  title: string;
  body: string;                 // Texte nettoyé (sans HTML)
  author?: string;
  published_at?: number;
  sources: { reference: string; verified: boolean }[];
  keywords: string[];           // Mots-clés extraits
  language: string;
  word_count: number;
}

/** Résultat de la digestion complète */
export interface DigestedFood {
  id: string;
  chewed_food_id: string;
  stage: DigestionStage;
  rosetta?: RosettaTranslation;              // null si rejeté
  information_score?: InformationResonanceScore; // Score qualité
  threat_signal?: ThreatSignal;              // Si menace détectée
  target_sphere?: SphereId;                  // Sphère cible
  target_layer?: MappingLayer;               // Couche historique
  node_id?: string;                          // Si ATOMNode créé
  rejection_reason?: string;                 // Si rejeté (déchet)
  pipeline_log: DigestiveLogEntry[];         // Journal complet
}

/** Entrée du journal digestif */
export interface DigestiveLogEntry {
  stage: DigestionStage;
  timestamp: number;
  passed: boolean;
  detail: string;
  score?: number;               // Score à cette étape (0-100)
}

/** Statistiques du système digestif */
export interface DigestiveStats {
  total_ingested: number;
  total_absorbed: number;       // Devenus ATOMNodes
  total_eliminated: number;     // Rejetés comme déchets
  absorption_rate: number;      // ratio absorbed/ingested (0-1)
  top_spheres: Record<string, number>;  // Répartition par sphère
  avg_quality_score: number;    // Score moyen des absorbés
}

/** Événement émis par le système digestif */
export interface DigestiveEvent {
  type: 'food_ingested' | 'food_absorbed' | 'food_eliminated' | 'digestion_complete';
  food?: DigestedFood;
  stats?: DigestiveStats;
}

// ═══════════════════════════════════════════════════════════
// MOTEUR VIBRATIONNEL
// ═══════════════════════════════════════════════════════════

export interface GeoPosition {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

export interface VibrationalState {
  system_resonance: number;       // Hz actuelle du système
  user_position: GeoPosition | null;
  distance_to_zero: number;       // km depuis Point Zéro
  is_in_crater: boolean;
  mode: 'standard' | 'activated' | 'polishing' | 'genesis';
  last_sync: number;
}

// ═══════════════════════════════════════════════════════════
// SYSTÈME GLOBAL (OS State)
// ═══════════════════════════════════════════════════════════

export type OSMode = 'exploration' | 'polissage' | 'creation' | 'meditation' | 'genesis';
export type HubTab = 'projet' | 'execution' | 'app' | 'rezo';
export type CommShortcut = 'chat' | 'mail' | 'convo';

// ═══════════════════════════════════════════════════════════
// COMMUNICATION HUB — Canaux de Communication
// ═══════════════════════════════════════════════════════════

export type CommChannelId =
  | 'COURRIEL'
  | 'TELEPHONE'
  | 'AGENTS'
  | 'CHAT'
  | 'MEETING'
  | 'SERVICES';

export interface CommChannel {
  id: CommChannelId;
  label: string;
  icon: string;
  description: string;
  color: string;
}

export const COMM_CHANNELS: Record<CommChannelId, CommChannel> = {
  COURRIEL:  { id: 'COURRIEL',  label: 'Courriel',  icon: '📧', description: 'Messagerie souveraine',  color: '#4488FF' },
  TELEPHONE: { id: 'TELEPHONE', label: 'Téléphone', icon: '📞', description: 'Communication vocale',   color: '#44FF88' },
  AGENTS:    { id: 'AGENTS',    label: 'Agents',    icon: '🤖', description: 'Agents IA AT·OM',        color: '#FF8844' },
  CHAT:      { id: 'CHAT',      label: 'Chat',      icon: '💬', description: 'Messagerie instantanée', color: '#AA44FF' },
  MEETING:   { id: 'MEETING',   label: 'Meeting',   icon: '📅', description: 'Réunions et visio',     color: '#FF44AA' },
  SERVICES:  { id: 'SERVICES',  label: 'Services',  icon: '🔧', description: 'Services AT·OM',        color: '#FFD700' },
};

// ═══════════════════════════════════════════════════════════
// TAB SYSTEM — Onglets dynamiques du panneau central
// ═══════════════════════════════════════════════════════════

export type TabSource = 'sphere' | 'comm' | 'system';

export interface ContentTab {
  id: string;
  source: TabSource;
  source_id: SphereId | CommChannelId | HubTab;
  label: string;
  icon: string;
  color: string;
  created_at: number;
  is_pinned: boolean;
}

// ═══════════════════════════════════════════════════════════
// SERVICE SHORTCUTS — Raccourcis de services (TopBar)
// ═══════════════════════════════════════════════════════════

export type ServiceId = 'FORUM' | 'CHAT_SERVICE' | 'SHOPPING' | 'SOCIAL' | 'COURSE' | 'STREAM';

export interface ServiceShortcut {
  id: ServiceId;
  label: string;
  icon: string;
}

export const SERVICE_SHORTCUTS: ServiceShortcut[] = [
  { id: 'FORUM',        label: 'Forum',    icon: '💭' },
  { id: 'CHAT_SERVICE', label: 'Chat',     icon: '💬' },
  { id: 'SHOPPING',     label: 'Shopping', icon: '🛒' },
  { id: 'SOCIAL',       label: 'Social',   icon: '👥' },
  { id: 'COURSE',       label: 'Cours',    icon: '🎓' },
  { id: 'STREAM',       label: 'Stream',   icon: '📡' },
];

// ═══════════════════════════════════════════════════════════
// USER PROFILE — Profil utilisateur (TopBar)
// ═══════════════════════════════════════════════════════════

export interface UserProfile {
  display_name: string;
  avatar_url: string | null;
  role: 'user' | 'admin' | 'architect';
}

// ═══════════════════════════════════════════════════════════
// SYSTÈME GLOBAL (OS State)
// ═══════════════════════════════════════════════════════════

export interface ATOMGlobalState {
  // Conscience (Top Bar)
  mode: OSMode;
  system_frequency: number;
  resonance_label: string;
  resonance_color: string;

  // Navigation (Main Engine)
  active_sphere: SphereId | null;
  active_node: ATOMNode | null;
  sphere_navigator_open: boolean;

  // Exécution (Bottom Taskbar)
  active_tab: HubTab;
  command_history: string[];

  // Tab System (Panneau Central)
  tabs: ContentTab[];
  active_tab_id: string | null;

  // Communication Hub (Panneau Droit)
  active_comm_channel: CommChannelId | null;
  comm_hub_open: boolean;

  // Profil Utilisateur
  user_profile: UserProfile | null;

  // Moteurs
  vibrational: VibrationalState;
  antikythera: AntikytheraState;

  // Utilisateur
  user_id: string | null;
  is_sovereign: boolean;
  is_architect: boolean;

  // Infrastructure (Bridge)
  is_online: boolean;

  // ─── Facette Politique — Gouvernance Directe ────────────
  governance: {
    proposals: GovernanceProposal[];
    active_proposal: GovernanceProposal | null;
    council_count: number;
  };

  // ─── Facette Économique — Économie de Résonance ─────────
  economy: {
    balance_ur: number;
    flow_keeper_status: 'EQUILIBRE' | 'ANTI_INFLATION' | 'ANTI_DEFLATION' | 'CRISE';
    total_supply: number;
    velocity_30d: number;
  };

  // ─── Facette Historique — AT-OM Mapping ─────────────────
  mapping: {
    current_layer: MappingLayer;
    active_entry: MappingEntry | null;
    patterns_detected: number;
  };

  // ─── Facette Identitaire — Identité Souveraine ─────────
  identity: {
    sovereign_identity: SovereignIdentity | null;
    credentials_count: number;
    sovereignty_status: 'NON_SOUVERAIN' | 'EN_TRANSITION' | 'SOUVERAIN' | 'ARCHITECTE';
  };

  // ─── Facette Défensive — Amygdale (Sentinelle) ────────
  threats: AmygdalaState;

  // ─── Facette Digestive — Arbre des Connaissances ──────
  digestion: DigestiveStats;
}

// ═══════════════════════════════════════════════════════════
// HEDERA INTEGRATION TYPES
// ═══════════════════════════════════════════════════════════

export interface HederaProof {
  topic_id: string;
  sequence_number: number;
  consensus_timestamp: string;
  message_hash: string;
  rosetta_id: string;
}

export interface HederaConfig {
  network: 'testnet' | 'mainnet';
  operator_id: string;
  token_id: string;
  nft_collection_id: string;
  hcs_topic_id: string;
}

// ═══════════════════════════════════════════════════════════
// ARITHMOS — Calcul Pythagoricien
// ═══════════════════════════════════════════════════════════

export const ARITHMOS_MAP: Record<string, number> = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8,
};

// ═══════════════════════════════════════════════════════════
// DELAY VIBRATOIRE — Temps de réponse par fréquence
// (Plus la fréquence est élevée, plus la réponse est rapide)
// ═══════════════════════════════════════════════════════════

export const VIBRATIONAL_DELAY: Record<ResonanceLevel, number> = {
  1: 900,  // 111 Hz → Impulsion lente, racines profondes
  2: 800,  // 222 Hz → Dialogue posé
  3: 700,  // 333 Hz → Pensée structurée
  4: 600,  // 444 Hz → * ANCRE — équilibre parfait
  5: 500,  // 555 Hz → Action vive
  6: 400,  // 666 Hz → Onde profonde
  7: 300,  // 777 Hz → Souffle léger
  8: 200,  // 888 Hz → Flux rapide
  9: 100,  // 999 Hz → Instantané, lumière pure
};

// ═══════════════════════════════════════════════════════════
// DIAMANT 6 FACETTES — Les perspectives simultanées
// ═══════════════════════════════════════════════════════════

export type DiamondFacet =
  | 'TECHNOLOGIQUE'    // Comment nous construisons les outils
  | 'POLITIQUE'        // Comment nous organisons les structures
  | 'GOUVERNEMENTALE'  // Comment nous prenons les décisions
  | 'RELIGIEUSE'       // Comment nous respectons les traditions
  | 'SPIRITUELLE'      // Comment nous cultivons l'âme
  | 'HISTORIQUE';      // Comment nous préservons la vérité

export const DIAMOND_FACETS: Record<DiamondFacet, {
  label: string;
  version_executive: string;
  version_mythique: string;
  current_pct: number;
  optimal_pct: number;
}> = {
  TECHNOLOGIQUE: {
    label: 'Technologique',
    version_executive: 'Infrastructure cloud décentralisée avec consensus Hedera',
    version_mythique: 'Le Réseau Cristallin — Chaque nœud est un point de lumière',
    current_pct: 85,
    optimal_pct: 100,
  },
  POLITIQUE: {
    label: 'Politique',
    version_executive: 'Gouvernance par tokens et vote pondéré selon l\'engagement',
    version_mythique: 'Le Conseil des Gardiens — Chaque voix est une note dans la symphonie',
    current_pct: 15,
    optimal_pct: 100,
  },
  GOUVERNEMENTALE: {
    label: 'Gouvernementale',
    version_executive: 'Automatisation des services par smart contracts immuables',
    version_mythique: 'Les Lois Naturelles — L\'eau trouve son chemin vers le besoin',
    current_pct: 10,
    optimal_pct: 100,
  },
  RELIGIEUSE: {
    label: 'Religieuse',
    version_executive: 'Classification des systèmes de croyance et extraction des convergences',
    version_mythique: 'La Bibliothèque d\'Alexandrie Numérique — Sagesses préservées dans l\'Akash',
    current_pct: 5,
    optimal_pct: 100,
  },
  SPIRITUELLE: {
    label: 'Spirituelle',
    version_executive: 'Interface UX avec fréquences binaurales et géométrie sacrée',
    version_mythique: 'Le Temple Intérieur — Chaque interaction un rituel de connexion',
    current_pct: 40,
    optimal_pct: 100,
  },
  HISTORIQUE: {
    label: 'Historique',
    version_executive: 'Base de données de faits vérifiés avec sources et métadonnées',
    version_mythique: 'Les Annales Akashiques — La mémoire éternelle de l\'humanité',
    current_pct: 0,
    optimal_pct: 100,
  },
};

// ═══════════════════════════════════════════════════════════
// 4 VERSIONS DE LECTURE — Déblocage progressif
// ═══════════════════════════════════════════════════════════

export type ReadingVersion = 'EXECUTIVE' | 'PHILOSOPHIQUE' | 'INITIATIQUE' | 'MYTHIQUE';

export const READING_VERSIONS: Record<ReadingVersion, {
  label: string;
  audience: string;
  min_resonance: number;
  unlock_condition: string;
}> = {
  EXECUTIVE: {
    label: 'Exécutive',
    audience: 'Entrepreneurs, Investisseurs',
    min_resonance: 0,
    unlock_condition: 'Aucune — Porte ouverte',
  },
  PHILOSOPHIQUE: {
    label: 'Philosophique',
    audience: 'Penseurs, Éducateurs',
    min_resonance: 20,
    unlock_condition: 'Inscription + Charte signée',
  },
  INITIATIQUE: {
    label: 'Initiatique',
    audience: 'Fondateurs',
    min_resonance: 40,
    unlock_condition: 'Engagement démontré + Temps',
  },
  MYTHIQUE: {
    label: 'Mythique / Sacré',
    audience: 'Gardiens',
    min_resonance: 80,
    unlock_condition: 'Cohérence énergétique + Besoin réel',
  },
};

// ═══════════════════════════════════════════════════════════
// 3 ÉTATS DU SYSTÈME — Transition vibrationnelle
// ═══════════════════════════════════════════════════════════

export type SystemPhase = 'ACTUEL' | 'TRANSITION' | 'OPTIMAL';

export const SYSTEM_PHASES: Record<SystemPhase, {
  label: string;
  alias: string;
  frequency_range: [number, number];
  resonance_target: number;
  description: string;
}> = {
  ACTUEL: {
    label: 'État Actuel',
    alias: 'Diamant Brut',
    frequency_range: [0, 333],
    resonance_target: 30,
    description: 'Chaos organisé — fréquences discordantes',
  },
  TRANSITION: {
    label: 'État de Transition',
    alias: 'Moteur Vibrationnel',
    frequency_range: [444, 666],
    resonance_target: 60,
    description: 'Conservation → Extraction → Transmutation',
  },
  OPTIMAL: {
    label: 'État Optimal',
    alias: 'Cité de Cristal',
    frequency_range: [777, 999],
    resonance_target: 100,
    description: 'Interconnexion parfaite des 9 Sphères',
  },
};

// ═══════════════════════════════════════════════════════════
// RESONANCE SCORE — Variable de transition individuelle
// ═══════════════════════════════════════════════════════════

export interface ResonanceScoreWeights {
  activity: number;       // 0.25 — Activité dans le système
  contribution: number;   // 0.25 — Contributions au code/contenu
  tenure: number;         // 0.20 — Ancienneté
  investment: number;     // 0.15 — UR détenus
  referral: number;       // 0.15 — Parrainages actifs
}

export const DEFAULT_RESONANCE_WEIGHTS: ResonanceScoreWeights = {
  activity: 0.25,
  contribution: 0.25,
  tenure: 0.20,
  investment: 0.15,
  referral: 0.15,
};

export type ResonanceRank = 'INITIE' | 'CITOYEN' | 'FONDATEUR' | 'GARDIEN' | 'ARCHITECTE';

export const RESONANCE_RANKS: Record<ResonanceRank, {
  min_score: number;
  max_score: number;
  label: string;
  rights: string[];
  ai_token_quota: number | 'unlimited';
}> = {
  INITIE: {
    min_score: 0, max_score: 20,
    label: 'Initié',
    rights: ['Accès base'],
    ai_token_quota: 50_000,
  },
  CITOYEN: {
    min_score: 20, max_score: 40,
    label: 'Citoyen',
    rights: ['Vote sur propositions opérationnelles'],
    ai_token_quota: 100_000,
  },
  FONDATEUR: {
    min_score: 40, max_score: 60,
    label: 'Fondateur',
    rights: ['Vote sur propositions structurelles'],
    ai_token_quota: 500_000,
  },
  GARDIEN: {
    min_score: 60, max_score: 80,
    label: 'Gardien',
    rights: ['Éligible aux rôles de gouvernance'],
    ai_token_quota: 1_000_000,
  },
  ARCHITECTE: {
    min_score: 80, max_score: 100,
    label: 'Architecte',
    rights: ['Droit de proposition constitutionnelle'],
    ai_token_quota: 'unlimited',
  },
};

// ═══════════════════════════════════════════════════════════
// ÉCONOMIE DE RÉSONANCE — Unités et mécanismes
// ═══════════════════════════════════════════════════════════

export type EconomicCategory =
  | 'ALLOCATION' | 'REBATES' | 'TOKENS' | 'EXPANSION'
  | 'REFERRAL' | 'STABILITY' | 'RESEARCH' | 'MARKETPLACE'
  | 'LENDING' | 'MONETARY' | 'SECURITY' | 'GOVERNANCE';

export interface EconomicSettings {
  category: EconomicCategory;
  key: string;
  value: number;
  description: string;
}

export interface FlowKeeperConfig {
  velocity_target_30d: number;       // Cible 5.0
  reserve_ratio_min: number;         // 100%+
  burn_rate_base: number;            // 0.1%
  resonance_rebate_pct: number;      // Ristourne résonance
  cooperation_index_target: number;  // Cible haute
}

export const DEFAULT_FLOW_KEEPER: FlowKeeperConfig = {
  velocity_target_30d: 5.0,
  reserve_ratio_min: 1.0,
  burn_rate_base: 0.001,
  resonance_rebate_pct: 0.05,
  cooperation_index_target: 0.80,
};

// ═══════════════════════════════════════════════════════════
// GOUVERNANCE DIRECTE — Consensus et propositions
// ═══════════════════════════════════════════════════════════

export type ProposalType = 'OPERATIONNELLE' | 'STRUCTURELLE' | 'CONSTITUTIONNELLE';
export type ProposalStatus = 'DRAFT' | 'DISCUSSION' | 'VOTING' | 'APPROVED' | 'REJECTED' | 'EXECUTED';
export type VoteValue = 'POUR' | 'CONTRE' | 'ABSTENTION';

export interface GovernanceProposal {
  id: string;
  type: ProposalType;
  title: string;
  description: string;
  sphere_id: SphereId | null;
  proposer_id: string;
  status: ProposalStatus;
  stake_required: number;          // UR minimum pour proposer
  quorum_pct: number;              // 33% default
  approval_pct: number;            // 67% default
  discussion_days: number;         // 3-7 jours
  votes_pour: number;
  votes_contre: number;
  votes_abstention: number;
  created_at: number;
  voting_ends_at: number;
}

export interface GovernanceVote {
  proposal_id: string;
  voter_id: string;
  vote: VoteValue;
  weight: number;                  // Pondéré par resonance_score
  timestamp: number;
}

export const GOVERNANCE_DEFAULTS = {
  quorum_pct: 0.33,
  approval_pct: 0.67,
  discussion_days_min: 3,
  discussion_days_max: 7,
  proposal_stake_operationnelle: 10,
  proposal_stake_structurelle: 100,
  proposal_stake_constitutionnelle: 1000,
  council_size: 144,
} as const;

// ═══════════════════════════════════════════════════════════
// NFT STRATÉGIE — Tiers de contribution
// ═══════════════════════════════════════════════════════════

export type NFTTier = 'GRAINE' | 'POUSSE' | 'BRANCHE' | 'RACINE' | 'ARBRE';

export const NFT_TIERS: Record<NFTTier, {
  label: string;
  label_en: string;
  min_contribution: number;
  max_edition: number | 'unlimited';
  ur_bonus_pct: number;
  frequency_range: [number, number];
  rights: string[];
}> = {
  GRAINE: {
    label: 'Graine de l\'Arche', label_en: 'Seed',
    min_contribution: 10, max_edition: 'unlimited',
    ur_bonus_pct: 0,
    frequency_range: [111, 111],
    rights: ['Early Supporter', 'Badge profil', 'Accès prioritaire'],
  },
  POUSSE: {
    label: 'Pousse de l\'Arbre', label_en: 'Sprout',
    min_contribution: 100, max_edition: 1000,
    ur_bonus_pct: 5,
    frequency_range: [111, 333],
    rights: ['Bonus UR 5%', 'Nom dans Bâtisseurs', 'Canal Fondateurs'],
  },
  BRANCHE: {
    label: 'Branche de l\'Arbre de Vie', label_en: 'Branch',
    min_contribution: 500, max_edition: 144,
    ur_bonus_pct: 15,
    frequency_range: [333, 555],
    rights: ['Vote consultatif', 'Features anticipées', 'Appel mensuel Fondateur'],
  },
  RACINE: {
    label: 'Racine de l\'Arche', label_en: 'Root',
    min_contribution: 2000, max_edition: 36,
    ur_bonus_pct: 30,
    frequency_range: [555, 777],
    rights: ['Gardien Économique', 'Revenue share', 'Conseil Consultatif', 'NFT évolutif'],
  },
  ARBRE: {
    label: 'Arbre de Vie Complet', label_en: 'Full Tree',
    min_contribution: 10000, max_edition: 9,
    ur_bonus_pct: 50,
    frequency_range: [777, 999],
    rights: ['Architecte Fondateur', 'Poids vote ×2', 'Revenu passif 0.1%', 'Nom dans le code'],
  },
};

// ═══════════════════════════════════════════════════════════
// IDENTITÉ SOUVERAINE — DID & Credentials
// ═══════════════════════════════════════════════════════════

export interface SovereignIdentity {
  did: string;                        // Decentralized Identifier
  display_name: string;
  avatar_hash: string;
  resonance_score: number;
  rank: ResonanceRank;
  nft_tier: NFTTier | null;
  spheres_active: SphereId[];
  credentials: VerifiableCredential[];
  created_at: number;
  is_sovereign: boolean;
}

export interface VerifiableCredential {
  id: string;
  type: string;                       // 'skill', 'contribution', 'role', 'attestation'
  issuer_did: string;
  subject_did: string;
  claim: Record<string, unknown>;
  hedera_proof_id?: string;
  issued_at: number;
  expires_at?: number;
}

// ═══════════════════════════════════════════════════════════
// AT-OM MAPPING — Cartographie universelle (6 couches)
// ═══════════════════════════════════════════════════════════

export type MappingLayer =
  | 'EVENEMENTS'      // 1 — Faits historiques vérifiables
  | 'NARRATIFS'       // 2 — Interprétations multiples
  | 'PATTERNS'        // 3 — Récurrences identifiées par l'IA
  | 'CAUSALITES'      // 4 — Chaînes cause→effet
  | 'VIBRATIONS'      // 5 — Fréquence des époques
  | 'PROJECTIONS';    // 6 — Scénarios futurs

export interface MappingEntry {
  id: string;
  layer: MappingLayer;
  title: string;
  epoch_start: number;               // Timestamp ou année
  epoch_end: number | null;           // null = en cours
  sphere_connections: SphereId[];
  sources: MappingSource[];
  patterns_linked: string[];          // IDs d'autres entrées
  resonance_frequency: number;        // Hz de l'époque
  node_id?: string;
  rosetta_mapping_id?: string;
}

export interface MappingSource {
  type: 'primary' | 'secondary' | 'oral' | 'archaeological';
  reference: string;
  credibility_score: number;          // 0-100
  verified_on_chain: boolean;
}

export const MAPPING_LAYERS_META: Record<MappingLayer, {
  index: number;
  label: string;
  description: string;
}> = {
  EVENEMENTS:   { index: 1, label: 'Événements',  description: 'Faits vérifiables, dates, lieux, acteurs' },
  NARRATIFS:    { index: 2, label: 'Narratifs',    description: 'Interprétations multiples conservées' },
  PATTERNS:     { index: 3, label: 'Patterns',     description: 'Récurrences et cycles identifiés par l\'IA' },
  CAUSALITES:   { index: 4, label: 'Causalités',   description: 'Chaînes de cause à effet analysées' },
  VIBRATIONS:   { index: 5, label: 'Vibrations',   description: 'Fréquence vibratoire des époques' },
  PROJECTIONS:  { index: 6, label: 'Projections',  description: 'Scénarios possibles et points de bifurcation' },
};

// ═══════════════════════════════════════════════════════════
// TRI DE L'INFORMATION — Score de résonance informationnelle
// ═══════════════════════════════════════════════════════════

export type ContentIntention =
  | 'INFORMATIF'    // Vise à éclairer
  | 'PERSUASIF'     // Vise à convaincre
  | 'MANIPULATIF'   // Vise à exploiter les émotions
  | 'COMMERCIAL'    // Vise à vendre
  | 'DIVISIF';      // Vise à polariser

export interface InformationResonanceScore {
  content_id: string;
  coherence_interne: number;         // 0-100 logique, non-contradiction
  coherence_externe: number;         // 0-100 alignement faits vérifiables
  diversite_sources: number;         // 0-100 sources multiples confirmant
  transparence_methodo: number;      // 0-100 méthodologie visible
  fiabilite_auteur: number;          // 0-100 historique de l'auteur
  intention_detectee: ContentIntention;
  score_global: number;              // 0-100 composite
}

// ═══════════════════════════════════════════════════════════
// FILTRE D'INTENTION — SERVIR vs EXTRAIRE
// ═══════════════════════════════════════════════════════════

export type IntentionFilter = 'SERVIR' | 'EXTRAIRE';

export interface IntentionCheck {
  action: string;
  sert_epanouissement: boolean;
  respecte_souverainete: boolean;
  est_transparent: boolean;
  cree_plus_de_valeur: boolean;
  aligne_9_spheres: boolean;
  visible_par_tous: boolean;
  verdict: IntentionFilter;
}

// ═══════════════════════════════════════════════════════════
// 7 LOIS UNIVERSELLES — Principes de validation
// ═══════════════════════════════════════════════════════════

export type UniversalLaw =
  | 'CORRESPONDANCE'   // Ce qui est en haut est comme ce qui est en bas
  | 'VIBRATION'        // Rien ne repose, tout vibre
  | 'RYTHME'           // Tout s'écoule, tout a ses marées
  | 'POLARITE'         // Tout est double, tout a deux pôles
  | 'CAUSE_EFFET'      // Toute cause a son effet
  | 'GENRE'            // Le genre est en toute chose
  | 'MENTALISME';      // Le Tout est Esprit

export const UNIVERSAL_LAWS: Record<UniversalLaw, {
  maxim: string;
  application_atom: string;
  mapping_usage: string;
}> = {
  CORRESPONDANCE: {
    maxim: 'Ce qui est en haut est comme ce qui est en bas',
    application_atom: 'L\'évolution d\'un individu reflète celle de la communauté qui reflète le système',
    mapping_usage: 'Analyser les cycles personnels pour prédire les cycles collectifs',
  },
  VIBRATION: {
    maxim: 'Rien ne repose, tout vibre',
    application_atom: 'Les 9 Sphères vibrent à 111-999 Hz, le resonance_score mesure l\'alignement',
    mapping_usage: 'Cartographier les zones de haute/basse vibration collective dans l\'histoire',
  },
  RYTHME: {
    maxim: 'Tout s\'écoule, dedans et dehors, tout a ses marées',
    application_atom: 'L\'économie UR suit des cycles, la gouvernance alterne consensus/tension',
    mapping_usage: 'Identifier les cycles historiques pour comprendre où nous sommes',
  },
  POLARITE: {
    maxim: 'Tout est double, tout a deux pôles',
    application_atom: 'Technologie/Nature, Individu/Collectif, Liberté/Responsabilité',
    mapping_usage: 'Cartographier les polarités dans l\'histoire et leur résolution',
  },
  CAUSE_EFFET: {
    maxim: 'Toute cause a son effet, tout effet a sa cause',
    application_atom: 'Blockchain = traçabilité parfaite, chaque transaction a un historique',
    mapping_usage: 'Analyser les chaînes causales pour comprendre les vrais moteurs',
  },
  GENRE: {
    maxim: 'Le genre est en toute chose, tout a ses principes masculin et féminin',
    application_atom: 'Structure + Équilibre = Création, Technologie + Sagesse = Innovation',
    mapping_usage: 'Analyser l\'équilibre des énergies dans les différentes ères',
  },
  MENTALISME: {
    maxim: 'Le Tout est Esprit, l\'Univers est Mental',
    application_atom: 'L\'intention purifiée est la fondation, le système reflète la conscience',
    mapping_usage: 'Cartographier l\'évolution de la conscience humaine à travers les âges',
  },
};

// ═══════════════════════════════════════════════════════════
// FORGE — Moteur de transformation Actuel → Optimal
// ═══════════════════════════════════════════════════════════

export type ForgeStep = 'CONSERVATION' | 'EXTRACTION' | 'TRANSMUTATION' | 'ELEVATION' | 'HARMONISATION';

export interface ForgeProcess {
  step: ForgeStep;
  input_state: string;
  output_state: string;
  frequency_work: number;
}

export const FORGE_STEPS: ForgeProcess[] = [
  { step: 'CONSERVATION',   input_state: 'Données polluées',   output_state: 'Données pures',      frequency_work: 444 },
  { step: 'EXTRACTION',     input_state: 'Services captifs',   output_state: 'Services libres',     frequency_work: 444 },
  { step: 'TRANSMUTATION',  input_state: 'Compétition',        output_state: 'Coopération',         frequency_work: 555 },
  { step: 'ELEVATION',      input_state: 'Résonance < 30',     output_state: 'Résonance > 70',      frequency_work: 666 },
  { step: 'HARMONISATION',  input_state: 'Fréquences chaos',   output_state: '444-999 Hz',          frequency_work: 999 },
];

// ═══════════════════════════════════════════════════════════
// TRANSITION MINISTÈRES → SPHÈRES
// ═══════════════════════════════════════════════════════════

export const MINISTRY_TO_SPHERE: Record<string, SphereId> = {
  'Identité / État Civil':       'TECHNO',
  'Santé / Affaires Sociales':   'SANTE',
  'Éducation / Culture':         'EDUCATION',
  'Économie / Finances':         'ECONOMIE',
  'Justice / Intérieur':         'JUSTICE',
  'Numérique / IA':              'ENVIRONNEMENT',
  'Infrastructure / Travaux':    'CULTURE',
  'Environnement / Agriculture': 'SPIRITUALITE',
  'Gouvernance / Politique':     'POLITIQUE',
};
