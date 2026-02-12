/**
 * AT·OM — useMapping
 * Hook de cartographie universelle — 6 couches, patterns, sources
 *
 * "Nous ne réécrivons pas l'histoire. Nous la DÉCHIFFRONS."
 *
 * Le même flux Rosetta circule ici :
 *   TECH   → Payload JSON (couche, entrée, sources, chaînes causales)
 *   PEOPLE → Narration historique multi-perspective
 *   SPIRIT → Fréquence de l'époque cartographiée
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import {
  calculateSourceCredibility,
  detectPatterns,
  getEraFromDate,
} from '../parser/templates/MappingTemplate';
import type {
  MappingLayer,
  MappingEntry,
  MappingSource,
  SphereId,
} from '../types/atom-types';
import { MAPPING_LAYERS_META } from '../types/atom-types';

export function useMapping() {
  const { state, dispatch, parser } = useATOM();
  const { mapping } = state;

  // ─── Changer de couche ──────────────────────────────────
  const setLayer = useCallback((layer: MappingLayer) => {
    dispatch({
      type: 'MAPPING_UPDATE',
      payload: { current_layer: layer },
    });
  }, [dispatch]);

  // ─── Créer une entrée ──────────────────────────────────
  const createEntry = useCallback((params: {
    layer: MappingLayer;
    title: string;
    epoch_start: number;
    epoch_end?: number;
    sphere_connections: SphereId[];
    sources: MappingSource[];
    resonance_frequency?: number;
  }) => {
    const entry: MappingEntry = {
      id: `map_${Date.now().toString(36)}`,
      layer: params.layer,
      title: params.title,
      epoch_start: params.epoch_start,
      epoch_end: params.epoch_end ?? null,
      sphere_connections: params.sphere_connections,
      sources: params.sources,
      patterns_linked: [],
      resonance_frequency: params.resonance_frequency ?? 444,
    };

    // Traduire par Rosetta (3 dimensions)
    parser.translate('mapping', {
      layer: params.layer,
      title: params.title,
      epoch_start: params.epoch_start,
      epoch_end: params.epoch_end,
      sphere_connections: params.sphere_connections,
      sources: params.sources,
    }, 'TECH', entry.id);

    dispatch({
      type: 'MAPPING_UPDATE',
      payload: { active_entry: entry },
    });

    return { success: true, entry };
  }, [dispatch, parser]);

  // ─── Sélectionner une entrée ────────────────────────────
  const selectEntry = useCallback((entry: MappingEntry | null) => {
    dispatch({
      type: 'MAPPING_UPDATE',
      payload: { active_entry: entry },
    });
  }, [dispatch]);

  // ─── Détection de patterns ──────────────────────────────
  const analyzePatterns = useCallback((entries: MappingEntry[]) => {
    const patterns = detectPatterns(entries);
    dispatch({
      type: 'MAPPING_UPDATE',
      payload: { patterns_detected: patterns.recurring_causes.length },
    });
    return patterns;
  }, [dispatch]);

  // ─── Métadonnées de couche ──────────────────────────────
  const currentLayerMeta = useMemo(() =>
    MAPPING_LAYERS_META[mapping.current_layer],
  [mapping.current_layer]);

  return {
    // État
    currentLayer: mapping.current_layer,
    activeEntry: mapping.active_entry,
    patternsDetected: mapping.patterns_detected,
    currentLayerMeta,

    // Actions
    setLayer,
    createEntry,
    selectEntry,
    analyzePatterns,

    // Utilitaires
    calculateSourceCredibility,
    detectPatterns,
    getEraFromDate,
    layersMeta: MAPPING_LAYERS_META,
  };
}
