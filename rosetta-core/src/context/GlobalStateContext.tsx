/**
 * AT·OM — GlobalStateContext
 * Le Bridge — Connexion entre TOUTES les couches du système
 *
 * "Ce qui est en haut est comme ce qui est en bas."
 *
 * Quand une donnée change dans une sphère, le RosettaParser
 * se déclenche pour mettre à jour :
 *   - La résonance visuelle (couleurs émeraude/or)
 *   - Le message humain associé (narration)
 *   - La fréquence vibratoire (Hz)
 *   - Les engrenages Anticythère (propagation)
 *
 * Le même flux circule à travers TOUTES les facettes :
 *   GOUVERNANCE  → Propositions, votes, consensus
 *   ÉCONOMIE     → Transactions UR, FlowKeeper
 *   MAPPING      → Couches historiques, patterns
 *   IDENTITÉ     → DID, souveraineté, credentials
 */

import React, { createContext, useContext, useReducer, useCallback, useRef, useEffect } from 'react';
import type {
  ATOMGlobalState,
  SphereId,
  ATOMNode,
  OSMode,
  HubTab,
  ResonanceLevel,
  RosettaTranslation,
  GearEvent,
  MappingLayer,
  MappingEntry,
  GovernanceProposal,
  SovereignIdentity,
  CommChannelId,
  ContentTab,
  TabSource,
  UserProfile,
  ThreatSignal,
  AmygdalaState,
  AmygdalaEvent,
  DigestiveStats,
  DigestiveEvent,
} from '../types/atom-types';
import { SACRED_FREQUENCIES, RESONANCE_MATRIX, SPHERES, COMM_CHANNELS } from '../types/atom-types';
import { RosettaParser, SphereEventTemplate, AlchemyTemplate } from '../parser/RosettaParser';
import { VibrationalMotor } from '../engines/VibrationalMotor';
import { InformationFilter, IntentionGuard, UniversalLawValidator } from '../engines/PolishingEngine';
import { ThreatAmygdala } from '../engines/ThreatAmygdala';
import { DigestiveSystem } from '../engines/DigestiveSystem';
import { GovernanceTemplate } from '../parser/templates/GovernanceTemplate';
import { EconomyTemplate, FlowKeeperEngine } from '../parser/templates/EconomyTemplate';
import { MappingTemplate } from '../parser/templates/MappingTemplate';
import { IdentityTemplate } from '../parser/templates/IdentityTemplate';
import { RedemptionTemplate } from '../parser/templates/RedemptionTemplate';
import { KnowledgeTemplate } from '../parser/templates/KnowledgeTemplate';
import { ChakraTemplate } from '../parser/templates/ChakraTemplate';

// ═══════════════════════════════════════════════════════════
// STATE INITIAL
// ═══════════════════════════════════════════════════════════

const initialState: ATOMGlobalState = {
  // Conscience (Top Bar)
  mode: 'exploration',
  system_frequency: SACRED_FREQUENCIES.HEARTBEAT,
  resonance_label: RESONANCE_MATRIX[4].label,
  resonance_color: RESONANCE_MATRIX[4].color,

  // Navigation (Main Engine)
  active_sphere: null,
  active_node: null,
  sphere_navigator_open: true,

  // Exécution (Bottom Taskbar)
  active_tab: 'projet',
  command_history: [],

  // Tab System (Panneau Central)
  tabs: [],
  active_tab_id: null,

  // Communication Hub (Panneau Droit)
  active_comm_channel: null,
  comm_hub_open: true,

  // Profil Utilisateur
  user_profile: null,

  // Moteurs
  vibrational: {
    system_resonance: SACRED_FREQUENCIES.HEARTBEAT,
    user_position: null,
    distance_to_zero: Infinity,
    is_in_crater: false,
    mode: 'standard',
    last_sync: Date.now(),
  },
  antikythera: {
    active_gears: new Map(),
    last_cascade: null,
    system_alignment: 0,
    total_rotations: 0,
  },

  // Utilisateur
  user_id: null,
  is_sovereign: false,
  is_architect: false,

  // Infrastructure (Bridge)
  is_online: true,

  // ─── Facette Politique — Gouvernance Directe ────────────
  governance: {
    proposals: [],
    active_proposal: null,
    council_count: 0,
  },

  // ─── Facette Économique — Économie de Résonance ─────────
  economy: {
    balance_ur: 0,
    flow_keeper_status: 'EQUILIBRE',
    total_supply: 0,
    velocity_30d: 0,
  },

  // ─── Facette Historique — AT-OM Mapping ─────────────────
  mapping: {
    current_layer: 'EVENEMENTS' as MappingLayer,
    active_entry: null,
    patterns_detected: 0,
  },

  // ─── Facette Identitaire — Identité Souveraine ─────────
  identity: {
    sovereign_identity: null,
    credentials_count: 0,
    sovereignty_status: 'NON_SOUVERAIN',
  },

  // ─── Facette Digestive — Arbre des Connaissances ───────
  digestion: {
    total_ingested: 0,
    total_absorbed: 0,
    total_eliminated: 0,
    absorption_rate: 0,
    top_spheres: {},
    avg_quality_score: 0,
  },

  // ─── Facette Défensive — Amygdale (Sentinelle) ────────
  threats: {
    alert_level: 'CALM',
    alert_score: 0,
    active_threats: [],
    memory: {
      recent_signals: [],
      threat_frequency: {
        frequency_anomaly: 0,
        manipulation_detected: 0,
        extraction_attempt: 0,
        integrity_breach: 0,
        cascade_risk: 0,
        sovereignty_violation: 0,
      },
      sensitivity: 0.5,
      last_lockdown: null,
    },
    is_scanning: false,
    last_scan: Date.now(),
  },
};

// ═══════════════════════════════════════════════════════════
// ACTIONS
// Le même pattern pour toutes les facettes —
// le flux circule de la même façon à tous les niveaux
// ═══════════════════════════════════════════════════════════

type ATOMAction =
  // Actions de base
  | { type: 'SET_MODE'; mode: OSMode }
  | { type: 'SET_FREQUENCY'; frequency: number }
  | { type: 'SELECT_SPHERE'; sphere: SphereId | null }
  | { type: 'SELECT_NODE'; node: ATOMNode | null }
  | { type: 'SET_TAB'; tab: HubTab }
  | { type: 'TOGGLE_NAVIGATOR' }
  | { type: 'ADD_COMMAND'; command: string }
  // Moteurs
  | { type: 'UPDATE_VIBRATIONAL'; payload: Partial<ATOMGlobalState['vibrational']> }
  | { type: 'GEAR_CASCADE'; event: GearEvent }
  | { type: 'SET_USER'; user_id: string; is_sovereign: boolean; is_architect: boolean }
  | { type: 'ROSETTA_UPDATE'; translation: RosettaTranslation }
  // Facettes du Diamant — même pattern que UPDATE_VIBRATIONAL
  | { type: 'GOVERNANCE_UPDATE'; payload: Partial<ATOMGlobalState['governance']> }
  | { type: 'ECONOMY_UPDATE'; payload: Partial<ATOMGlobalState['economy']> }
  | { type: 'MAPPING_UPDATE'; payload: Partial<ATOMGlobalState['mapping']> }
  | { type: 'IDENTITY_UPDATE'; payload: Partial<ATOMGlobalState['identity']> }
  // Tab System — Onglets dynamiques du panneau central
  | { type: 'OPEN_TAB'; tab: ContentTab }
  | { type: 'CLOSE_TAB'; tab_id: string }
  | { type: 'ACTIVATE_TAB'; tab_id: string }
  | { type: 'PIN_TAB'; tab_id: string; pinned: boolean }
  // Communication Hub
  | { type: 'SELECT_COMM_CHANNEL'; channel: CommChannelId | null }
  | { type: 'TOGGLE_COMM_HUB' }
  // Profil
  | { type: 'SET_PROFILE'; profile: UserProfile }
  // Bridge (Infrastructure ↔ Core)
  | { type: 'SET_ONLINE_STATUS'; isOnline: boolean }
  | { type: 'SYNC_IDENTITY'; did: string; display_name: string; is_sovereign: boolean }
  // Amygdale (Sentinelle)
  | { type: 'THREAT_DETECTED'; signal: ThreatSignal }
  | { type: 'THREAT_UPDATE'; payload: Partial<AmygdalaState> }
  // Système Digestif (Arbre des Connaissances)
  | { type: 'DIGESTION_UPDATE'; payload: Partial<DigestiveStats> }
  | { type: 'FOOD_ABSORBED'; food_id: string; sphere: SphereId };

function atomReducer(state: ATOMGlobalState, action: ATOMAction): ATOMGlobalState {
  switch (action.type) {
    case 'SET_MODE':
      return { ...state, mode: action.mode };

    case 'SET_FREQUENCY': {
      const level = Math.max(1, Math.min(9, Math.round(action.frequency / 111))) as ResonanceLevel;
      const resonance = RESONANCE_MATRIX[level];
      return {
        ...state,
        system_frequency: action.frequency,
        resonance_label: resonance.label,
        resonance_color: resonance.color,
      };
    }

    case 'SELECT_SPHERE': {
      if (!action.sphere) {
        return { ...state, active_sphere: null };
      }
      const sphere = SPHERES[action.sphere];
      const level = sphere.index as ResonanceLevel;
      const resonance = RESONANCE_MATRIX[level];
      return {
        ...state,
        active_sphere: action.sphere,
        system_frequency: sphere.frequency,
        resonance_label: resonance.label,
        resonance_color: resonance.color,
      };
    }

    case 'SELECT_NODE':
      return { ...state, active_node: action.node };

    case 'SET_TAB':
      return { ...state, active_tab: action.tab };

    case 'TOGGLE_NAVIGATOR':
      return { ...state, sphere_navigator_open: !state.sphere_navigator_open };

    case 'ADD_COMMAND':
      return {
        ...state,
        command_history: [...state.command_history.slice(-49), action.command],
      };

    case 'UPDATE_VIBRATIONAL':
      return {
        ...state,
        vibrational: { ...state.vibrational, ...action.payload },
      };

    case 'GEAR_CASCADE': {
      const newGears = new Map(state.antikythera.active_gears);
      newGears.set(action.event.source_sphere, Date.now());
      for (const target of action.event.target_spheres) {
        newGears.set(target, Date.now());
      }
      return {
        ...state,
        antikythera: {
          ...state.antikythera,
          active_gears: newGears,
          last_cascade: action.event,
          total_rotations: state.antikythera.total_rotations + 1,
        },
      };
    }

    case 'SET_USER':
      return {
        ...state,
        user_id: action.user_id,
        is_sovereign: action.is_sovereign,
        is_architect: action.is_architect,
      };

    case 'ROSETTA_UPDATE': {
      const { spirit } = action.translation;
      return {
        ...state,
        system_frequency: spirit.frequency_hz,
        resonance_label: RESONANCE_MATRIX[spirit.resonance_level].label,
        resonance_color: spirit.color,
      };
    }

    // ─── Facettes du Diamant ─────────────────────────────
    // Le même pattern circule identiquement à travers chaque facette

    case 'GOVERNANCE_UPDATE':
      return {
        ...state,
        governance: { ...state.governance, ...action.payload },
      };

    case 'ECONOMY_UPDATE':
      return {
        ...state,
        economy: { ...state.economy, ...action.payload },
      };

    case 'MAPPING_UPDATE':
      return {
        ...state,
        mapping: { ...state.mapping, ...action.payload },
      };

    case 'IDENTITY_UPDATE':
      return {
        ...state,
        identity: { ...state.identity, ...action.payload },
      };

    // ─── Tab System — Onglets dynamiques ───────────────────

    case 'OPEN_TAB': {
      const existing = state.tabs.find(t => t.source_id === action.tab.source_id);
      if (existing) {
        return { ...state, active_tab_id: existing.id };
      }
      return {
        ...state,
        tabs: [...state.tabs, action.tab],
        active_tab_id: action.tab.id,
      };
    }

    case 'CLOSE_TAB': {
      const remaining = state.tabs.filter(t => t.id !== action.tab_id);
      const needsNewActive = state.active_tab_id === action.tab_id;
      return {
        ...state,
        tabs: remaining,
        active_tab_id: needsNewActive
          ? remaining[remaining.length - 1]?.id ?? null
          : state.active_tab_id,
      };
    }

    case 'ACTIVATE_TAB':
      return { ...state, active_tab_id: action.tab_id };

    case 'PIN_TAB':
      return {
        ...state,
        tabs: state.tabs.map(t =>
          t.id === action.tab_id ? { ...t, is_pinned: action.pinned } : t
        ),
      };

    // ─── Communication Hub ─────────────────────────────────

    case 'SELECT_COMM_CHANNEL':
      return { ...state, active_comm_channel: action.channel };

    case 'TOGGLE_COMM_HUB':
      return { ...state, comm_hub_open: !state.comm_hub_open };

    // ─── Profil ────────────────────────────────────────────

    case 'SET_PROFILE':
      return { ...state, user_profile: action.profile };

    // ─── Bridge (Infrastructure ↔ Core) ─────────────────────

    case 'SET_ONLINE_STATUS':
      return { ...state, is_online: action.isOnline };

    case 'SYNC_IDENTITY':
      return {
        ...state,
        is_sovereign: action.is_sovereign,
        identity: {
          ...state.identity,
          sovereign_identity: {
            ...state.identity.sovereign_identity!,
            did: action.did,
            display_name: action.display_name,
            is_sovereign: action.is_sovereign,
          },
          sovereignty_status: action.is_sovereign ? 'SOUVERAIN' : 'EN_TRANSITION',
        },
      };

    // ─── Amygdale (Sentinelle) ─────────────────────────────

    case 'THREAT_DETECTED':
      return {
        ...state,
        threats: {
          ...state.threats,
          active_threats: [...state.threats.active_threats, action.signal],
        },
      };

    case 'THREAT_UPDATE':
      return {
        ...state,
        threats: { ...state.threats, ...action.payload },
      };

    // ─── Système Digestif (Arbre des Connaissances) ──────

    case 'DIGESTION_UPDATE':
      return {
        ...state,
        digestion: { ...state.digestion, ...action.payload },
      };

    case 'FOOD_ABSORBED':
      return {
        ...state,
        digestion: {
          ...state.digestion,
          total_absorbed: state.digestion.total_absorbed + 1,
          top_spheres: {
            ...state.digestion.top_spheres,
            [action.sphere]: ((state.digestion.top_spheres as Record<string, number>)[action.sphere] ?? 0) + 1,
          },
        },
      };

    default:
      return state;
  }
}

// ═══════════════════════════════════════════════════════════
// CONTEXT
// ═══════════════════════════════════════════════════════════

interface ATOMContextValue {
  state: ATOMGlobalState;
  dispatch: React.Dispatch<ATOMAction>;

  // Moteurs principaux
  parser: RosettaParser;
  motor: VibrationalMotor;
  flowKeeper: FlowKeeperEngine;

  // Filtres (classes statiques — Vision Complète Ch.11)
  informationFilter: typeof InformationFilter;
  intentionGuard: typeof IntentionGuard;
  universalLawValidator: typeof UniversalLawValidator;

  // Sentinelle (Amygdale — détection pré-corticale)
  amygdala: ThreatAmygdala;

  // Système Digestif (Arbre des Connaissances)
  digestive: DigestiveSystem;

  // Raccourcis d'actions
  selectSphere: (sphere: SphereId | null) => void;
  setMode: (mode: OSMode) => void;
  setTab: (tab: HubTab) => void;
  executeCommand: (command: string) => void;

  // Tab System
  openTab: (source: TabSource, sourceId: SphereId | CommChannelId | HubTab, label: string, icon: string, color: string) => void;
  closeTab: (tabId: string) => void;
  activateTab: (tabId: string) => void;

  // Communication Hub
  selectCommChannel: (channel: CommChannelId | null) => void;
}

const ATOMContext = createContext<ATOMContextValue | null>(null);

// ═══════════════════════════════════════════════════════════
// PROVIDER
// ═══════════════════════════════════════════════════════════

export function ATOMProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(atomReducer, initialState);
  const parserRef = useRef(new RosettaParser());
  const motorRef = useRef(new VibrationalMotor());
  const flowKeeperRef = useRef(new FlowKeeperEngine());
  const amygdalaRef = useRef(new ThreatAmygdala(parserRef.current));
  const digestiveRef = useRef(new DigestiveSystem(parserRef.current, amygdalaRef.current));

  // ─── Enregistrer les templates des 4 facettes ──────────
  // Le même RosettaParser traduit TOUTES les facettes
  // dans les 3 dimensions (TECH / PEOPLE / SPIRIT)
  useEffect(() => {
    const parser = parserRef.current;
    parser.registerTemplate(GovernanceTemplate);
    parser.registerTemplate(EconomyTemplate);
    parser.registerTemplate(MappingTemplate);
    parser.registerTemplate(IdentityTemplate);
    parser.registerTemplate(SphereEventTemplate);
    parser.registerTemplate(AlchemyTemplate);
    parser.registerTemplate(RedemptionTemplate);
    parser.registerTemplate(KnowledgeTemplate);
    parser.registerTemplate(ChakraTemplate);
  }, []);

  // Connecter le moteur vibrationnel au state
  useEffect(() => {
    const unsubscribe = motorRef.current.onStateChange((vibrational) => {
      dispatch({ type: 'UPDATE_VIBRATIONAL', payload: vibrational });
      dispatch({ type: 'SET_FREQUENCY', frequency: vibrational.system_resonance });
    });
    return unsubscribe;
  }, []);

  // Connecter le parser au système d'engrenages
  useEffect(() => {
    const unsubscribe = parserRef.current.on((event) => {
      if (event.type === 'translation_complete' && event.translation) {
        dispatch({ type: 'ROSETTA_UPDATE', translation: event.translation });

        // Scanner chaque traduction via l'amygdale (sentinelle pré-corticale)
        amygdalaRef.current.scan({
          type: 'translation',
          data: event.translation,
          source: 'RosettaParser',
        });
      }
      if (event.type === 'gear_triggered' && event.gear_event) {
        dispatch({ type: 'GEAR_CASCADE', event: event.gear_event });
      }
    });
    return unsubscribe;
  }, []);

  // Connecter l'amygdale au state (sentinelle → dispatch)
  useEffect(() => {
    const unsubscribe = amygdalaRef.current.onThreat((event) => {
      if (event.type === 'threat_detected' && event.signal) {
        dispatch({ type: 'THREAT_DETECTED', signal: event.signal });
      }
      // Synchroniser l'état complet de l'amygdale
      dispatch({ type: 'THREAT_UPDATE', payload: amygdalaRef.current.getState() });
    });
    return unsubscribe;
  }, []);

  // Connecter le système digestif au state (digestion → dispatch)
  useEffect(() => {
    const unsubscribe = digestiveRef.current.onDigest((event: DigestiveEvent) => {
      if (event.type === 'food_absorbed' && event.food?.target_sphere) {
        dispatch({ type: 'FOOD_ABSORBED', food_id: event.food.id, sphere: event.food.target_sphere });
      }
      // Synchroniser les stats digestives
      dispatch({ type: 'DIGESTION_UPDATE', payload: digestiveRef.current.getStats() });
    });
    return unsubscribe;
  }, []);

  // ─── Tab System ─────────────────────────────────────────

  const openTab = useCallback((
    source: TabSource,
    sourceId: SphereId | CommChannelId | HubTab,
    label: string,
    icon: string,
    color: string,
  ) => {
    const tab: ContentTab = {
      id: `tab_${source}_${sourceId}_${Date.now().toString(36)}`,
      source,
      source_id: sourceId,
      label,
      icon,
      color,
      created_at: Date.now(),
      is_pinned: false,
    };
    dispatch({ type: 'OPEN_TAB', tab });
  }, []);

  const closeTab = useCallback((tabId: string) => {
    dispatch({ type: 'CLOSE_TAB', tab_id: tabId });
  }, []);

  const activateTab = useCallback((tabId: string) => {
    dispatch({ type: 'ACTIVATE_TAB', tab_id: tabId });
  }, []);

  // ─── Communication Hub ─────────────────────────────────

  const selectCommChannel = useCallback((channel: CommChannelId | null) => {
    dispatch({ type: 'SELECT_COMM_CHANNEL', channel });
    if (channel) {
      const ch = COMM_CHANNELS[channel];
      openTab('comm', channel, ch.label, ch.icon, ch.color);
    }
  }, [openTab]);

  // ─── Raccourcis d'actions existants ────────────────────

  const selectSphere = useCallback((sphere: SphereId | null) => {
    dispatch({ type: 'SELECT_SPHERE', sphere });
    if (sphere) {
      const s = SPHERES[sphere];
      const resonance = RESONANCE_MATRIX[s.index as ResonanceLevel];
      openTab('sphere', sphere, s.label, s.icon, resonance.color);
      // Déclencher la propagation Anticythère
      parserRef.current.propagateGearChange(sphere, {
        schema_version: '1.0',
        data_type: 'sphere_selection',
        values: { sphere },
        timestamp: Date.now(),
      });
    }
  }, [openTab]);

  const setMode = useCallback((mode: OSMode) => {
    dispatch({ type: 'SET_MODE', mode });
    if (mode === 'genesis') {
      motorRef.current.setMode('genesis');
    }
  }, []);

  const setTab = useCallback((tab: HubTab) => {
    dispatch({ type: 'SET_TAB', tab });
  }, []);

  const executeCommand = useCallback((command: string) => {
    dispatch({ type: 'ADD_COMMAND', command });
  }, []);

  const value: ATOMContextValue = {
    state,
    dispatch,

    // Moteurs
    parser: parserRef.current,
    motor: motorRef.current,
    flowKeeper: flowKeeperRef.current,

    // Filtres (Vision Complète)
    informationFilter: InformationFilter,
    intentionGuard: IntentionGuard,
    universalLawValidator: UniversalLawValidator,

    // Sentinelle (Amygdale)
    amygdala: amygdalaRef.current,

    // Système Digestif (Arbre des Connaissances)
    digestive: digestiveRef.current,

    // Raccourcis
    selectSphere,
    setMode,
    setTab,
    executeCommand,

    // Tab System
    openTab,
    closeTab,
    activateTab,

    // Communication Hub
    selectCommChannel,
  };

  return (
    <ATOMContext.Provider value={value}>
      {children}
    </ATOMContext.Provider>
  );
}

// ═══════════════════════════════════════════════════════════
// HOOK
// ═══════════════════════════════════════════════════════════

export function useATOM(): ATOMContextValue {
  const context = useContext(ATOMContext);
  if (!context) {
    throw new Error('useATOM doit être utilisé dans un <ATOMProvider>');
  }
  return context;
}
