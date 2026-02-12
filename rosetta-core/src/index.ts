/**
 * AT·OM — Rosetta Core
 * Point d'entrée principal — Vision Complète
 *
 * Exporte TOUTES les facettes du diamant :
 *
 *   FACETTE TECHNIQUE     → Types, Parser, Moteurs, Hedera
 *   FACETTE SPIRITUELLE   → Chakra, Kabbale, Maya, Yi-King, Cosmic
 *   FACETTE POLITIQUE     → GovernanceTemplate (vote, consensus, Conseil 144)
 *   FACETTE ÉCONOMIQUE    → EconomyTemplate (UR, FlowKeeper, NFT Tiers)
 *   FACETTE HISTORIQUE    → MappingTemplate (6 couches, patterns, cycles)
 *   FACETTE IDENTITAIRE   → IdentityTemplate (DID, souveraineté, credentials)
 *   FACETTE INSTITUTIONNELLE → RedemptionTemplate (PRI, audit, conversion)
 *
 *   + InformationFilter   → Tri de l'information (Ch.11 Vision)
 *   + IntentionGuard      → Filtre SERVIR vs EXTRAIRE
 *   + UniversalLawValidator → 7 Lois Universelles
 */

// ─── Types Fondamentaux ───────────────────────────────────
export * from './types/atom-types';

// ─── Parser (Pierre de Rosette) ──────────────────────────
export {
  RosettaParser,
  RosettaError,
  TalentTemplate,
  SphereEventTemplate,
  AlchemyTemplate,
  type TranslatorTemplate,
  type ParserContext,
  type RosettaEvent,
} from './parser/RosettaParser';

// ─── Templates Cosmologiques (Facette Spirituelle) ───────
export {
  ChakraTemplate,
  CHAKRA_DATA,
  harmonizeFrequency,
  type ChakraDatum,
} from './parser/templates/ChakraTemplate';

export {
  KabbaleTemplate,
  SEPHIROTH_DATA,
  PATHS,
  WORLDS,
  PILLARS,
} from './parser/templates/KabbaleTemplate';

export {
  MayaTemplate,
  getMayaKin,
  TONS,
  NAWALS,
  GALACTIC_PORTAL_DAYS,
} from './parser/templates/MayaTemplate';

export {
  YiKingTemplate,
  castHexagram,
  getHexagramFromWord,
  TRIGRAMS,
} from './parser/templates/YiKingTemplate';

// ─── Template Cosmique Unifié ────────────────────────────
export {
  CosmicTemplate,
  calculateCosmicFrequency,
  getDailyOracle,
  registerAllCosmicTemplates,
  type CosmicInput,
} from './parser/templates/CosmicTemplate';

// ─── Gouvernance Directe (Facette Politique) ─────────────
export {
  GovernanceTemplate,
  getStakeRequired,
  calculateVoteWeight,
  canPropose,
  checkQuorum,
  checkConsensus,
  type GovernanceInput,
} from './parser/templates/GovernanceTemplate';

// ─── Économie de Résonance (Facette Économique) ──────────
export {
  EconomyTemplate,
  FlowKeeperEngine,
  type TransactionType,
  type EconomyInput,
  type FlowKeeperAction,
} from './parser/templates/EconomyTemplate';

// ─── AT-OM Mapping (Facette Historique) ──────────────────
export {
  MappingTemplate,
  calculateSourceCredibility,
  detectPatterns,
  getEraFromDate,
  type HistoricalEra,
  type MappingInput,
} from './parser/templates/MappingTemplate';

// ─── Identité Souveraine (Facette Identitaire) ──────────
export {
  IdentityTemplate,
  isCredentialValid,
  getNFTTierFromContribution,
  canAccessVersion,
  generateSovereigntyReport,
  type IdentityAction,
  type IdentityInput,
} from './parser/templates/IdentityTemplate';

// ─── Module PRI (Passerelle de Rédemption Institutionnelle) ─
export {
  RedemptionTemplate,
  ALCHEMY_STAGES,
  calculateResonanceUnits,
  getRedemptionAlchemyStage,
  CONTRIBUTION_WEIGHTS,
  type ContributionType,
  type RedemptionStatus,
  type RedemptionInput,
} from './parser/templates/RedemptionTemplate';

// ─── Moteur Vibrationnel (enrichi Vision Complète) ───────
export {
  VibrationalMotor,
  type AnchorPoint,
} from './engines/VibrationalMotor';

// ─── Moteur de Polissage + Tri + Intention + Lois ────────
export {
  PolishingEngine,
  InformationFilter,
  IntentionGuard,
  UniversalLawValidator,
  type AlchemyRule,
  type PolishingInput,
  type PolishingResult,
  type PolishingProfile,
} from './engines/PolishingEngine';

// ─── Correcteur Quantique (Quantum Error Correction) ─────
// Pipeline en 5 etapes : DETECT → LOCALIZE → CORRECT → VALIDATE → LOG
// Exploite la redundance tri-dimensionnelle Rosetta (3 qubits)
export {
  QuantumCorrector,
} from './engines/QuantumCorrector';

// ─── Sentinelle Amygdalienne (Threat Detection) ──────────
// Double voie : Fast Path (instantane) + Deep Path (analyse complete)
// Niveaux : CALM → VIGILANT → ALERT → LOCKDOWN
export {
  ThreatAmygdala,
} from './engines/ThreatAmygdala';

// ─── Système Digestif (Arbre des Connaissances) ─────────
// Pipeline : INGEST → CHEW → DIGEST → ABSORB → ROUTE → STORE → ELIMINATE
// Chaque donnee Internet est digeree en nutriment (ATOMNode) ou dechet (archive)
export {
  DigestiveSystem,
} from './engines/DigestiveSystem';

export {
  KnowledgeTemplate,
} from './parser/templates/KnowledgeTemplate';

// ─── Hedera Bridge ───────────────────────────────────────
export { HederaBridge } from './hedera/HederaBridge';

// ─── React Context & Hooks ───────────────────────────────
export { ATOMProvider, useATOM } from './context/GlobalStateContext';

// ─── Layout Components ───────────────────────────────────
export { ATOMLayout } from './components/layout/ATOMLayout';
export { TopBar } from './components/layout/TopBar';
export { MainEngine } from './components/layout/MainEngine';
export { SphereNavigator } from './components/layout/SphereNavigator';
export { DataExplorer } from './components/layout/DataExplorer';
export { BottomTaskbar } from './components/layout/BottomTaskbar';
export { ContentArea } from './components/layout/ContentArea';
export { CommHub } from './components/layout/CommHub';

// ─── React Hooks (Consumer API) ──────────────────────────
// Chaque hook encapsule une facette du diamant
// et expose le même flux Rosetta (TECH / PEOPLE / SPIRIT)
export { useGovernance } from './hooks/useGovernance';
export { useEconomy } from './hooks/useEconomy';
export { useMapping } from './hooks/useMapping';
export { useIdentity } from './hooks/useIdentity';
export { useInformationFilter } from './hooks/useInformationFilter';
export { useResonance } from './hooks/useResonance';
export { useThreatMonitor } from './hooks/useThreatMonitor';
export { useDigestive } from './hooks/useDigestive';
export { useTabSystem } from './hooks/useTabSystem';
