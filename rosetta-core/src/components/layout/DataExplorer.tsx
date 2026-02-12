/**
 * AT·OM — DataExplorer
 * Explorateur de données "Optimal vs Actuel"
 *
 * Affiche côte à côte :
 *   - Le Diamant Optimal (la structure parfaite)
 *   - Le Diamant Actuel (l'état réel via RosettaParser)
 *
 * 3 vues :
 *   📜 Rosetta  — Traduction tri-dimensionnelle (TECH/PEOPLE/SPIRIT)
 *   🌀 Phaistos — Anneaux concentriques des 9 sphères
 *   ⚗️ Émeraude — 7 étapes alchimiques (PolishingEngine)
 */

import React, { useState, useMemo } from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import {
  SPHERES,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
  type RosettaDimension,
  type RosettaTranslation,
  type SphereId,
  type ResonanceLevel,
  type ATOMNode,
  type EmeraldValidation,
} from '../../types/atom-types';
import { PolishingEngine } from '../../engines/PolishingEngine';

type ViewMode = 'rosetta' | 'spiral' | 'alchemy';

// ─── Helper : Seed Node pour la sphère active ──────────────
// Crée un ATOMNode minimal + RosettaTranslation pour alimenter les vues

function buildSeedForSphere(sphereId: SphereId, parser: any): {
  node: ATOMNode;
  translation: RosettaTranslation;
} {
  const sphere = SPHERES[sphereId];
  const level = sphere.index as ResonanceLevel;
  const resonance = RESONANCE_MATRIX[level];

  // Traduire via le SphereEventTemplate déjà enregistré
  const translation = parser.translate('sphere_event', {
    sphere: sphereId,
    event_name: 'sphere_inspection',
    data: {
      alignment: 0.85,
      active_nodes: 42,
      pending_polish: 7,
      last_cascade: Date.now() - 3600000,
    },
  }, 'TECH');

  const node: ATOMNode = {
    id: `seed_${sphereId}_${Date.now().toString(36)}`,
    parent_id: null,
    sphere_id: sphereId,
    title: `${sphere.label} — État Actuel`,
    status: 'active',
    depth: 0,
    spiral_position: (sphere.index / 9) * Math.PI * 2,
    resonance_level: level,
    rosetta: translation,
    created_by: 'system',
    created_at: Date.now(),
    updated_at: Date.now(),
  };

  return { node, translation };
}

// ─── Moteur de Polissage (singleton) ────────────────────────
const polishingEngine = new PolishingEngine();

// ═══════════════════════════════════════════════════════════
// DATA EXPLORER — Composant Principal
// ═══════════════════════════════════════════════════════════

export function DataExplorer() {
  const { state } = useATOM();
  const [viewMode, setViewMode] = useState<ViewMode>('rosetta');
  const [activeDimension, setActiveDimension] = useState<RosettaDimension>('TECH');

  const dimensions: { id: RosettaDimension; label: string; sublabel: string }[] = [
    { id: 'TECH', label: 'Technique', sublabel: 'Grec' },
    { id: 'PEOPLE', label: 'Humain', sublabel: 'Démotique' },
    { id: 'SPIRIT', label: 'Spirituel', sublabel: 'Hiéroglyphe' },
  ];

  const views: { id: ViewMode; label: string; icon: string }[] = [
    { id: 'rosetta', label: 'Rosetta', icon: '📜' },
    { id: 'spiral', label: 'Phaistos', icon: '🌀' },
    { id: 'alchemy', label: 'Émeraude', icon: '⚗️' },
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Header de l'explorateur */}
      <div
        className="flex items-center justify-between px-4 py-2 shrink-0"
        style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.06)' }}
      >
        {/* Sélecteur de vue */}
        <div className="flex gap-1">
          {views.map((v) => (
            <button
              key={v.id}
              onClick={() => setViewMode(v.id)}
              className="px-2.5 py-1 text-xs rounded transition-all duration-300"
              style={{
                background: viewMode === v.id ? `${state.resonance_color}15` : 'transparent',
                color: viewMode === v.id ? state.resonance_color : '#666',
                border: viewMode === v.id ? `1px solid ${state.resonance_color}33` : '1px solid transparent',
              }}
            >
              {v.icon} {v.label}
            </button>
          ))}
        </div>

        {/* Sélecteur de dimension (Rosetta) */}
        {viewMode === 'rosetta' && (
          <div className="flex gap-1">
            {dimensions.map((d) => (
              <button
                key={d.id}
                onClick={() => setActiveDimension(d.id)}
                className="px-2.5 py-1 text-xs rounded transition-all duration-300"
                style={{
                  background: activeDimension === d.id ? `${state.resonance_color}15` : 'transparent',
                  color: activeDimension === d.id ? state.resonance_color : '#555',
                }}
              >
                {d.label}
                <span className="text-gray-600 ml-1 text-[10px]">({d.sublabel})</span>
              </button>
            ))}
          </div>
        )}

        {/* Sphère active */}
        {state.active_sphere && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">Sphère:</span>
            <span
              className="text-xs font-medium"
              style={{ color: SPHERES[state.active_sphere].color }}
            >
              {SPHERES[state.active_sphere].icon} {SPHERES[state.active_sphere].label}
            </span>
          </div>
        )}
      </div>

      {/* Zone de contenu */}
      <div className="flex-1 overflow-y-auto p-4">
        {viewMode === 'rosetta' && <RosettaView dimension={activeDimension} />}
        {viewMode === 'spiral' && <PhaistosView />}
        {viewMode === 'alchemy' && <AlchemyView />}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// VUE ROSETTA — Diamant Optimal vs Diamant Actuel
// ═══════════════════════════════════════════════════════════

function RosettaView({ dimension }: { dimension: RosettaDimension }) {
  const { state, parser } = useATOM();

  // Générer la traduction seed pour la sphère active
  const seedData = useMemo(() => {
    if (!state.active_sphere) return null;
    try {
      return buildSeedForSphere(state.active_sphere, parser);
    } catch {
      return null;
    }
  }, [state.active_sphere, parser]);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        {/* Diamant Optimal */}
        <div
          className="rounded-lg p-4"
          style={{
            background: 'rgba(80, 200, 120, 0.05)',
            border: '1px solid rgba(80, 200, 120, 0.15)',
          }}
        >
          <h4 className="text-xs font-bold uppercase tracking-wider mb-3" style={{ color: '#50C878' }}>
            Diamant Optimal
          </h4>
          <OptimalDiamond dimension={dimension} frequency={state.system_frequency} color={state.resonance_color} />
        </div>

        {/* Diamant Actuel */}
        <div
          className="rounded-lg p-4"
          style={{
            background: 'rgba(255, 165, 0, 0.05)',
            border: '1px solid rgba(255, 165, 0, 0.15)',
          }}
        >
          <h4 className="text-xs font-bold uppercase tracking-wider mb-3" style={{ color: '#FFA500' }}>
            Diamant Actuel
          </h4>
          {seedData ? (
            <ActualDiamond dimension={dimension} translation={seedData.translation} />
          ) : (
            <div className="text-xs text-gray-500 italic">
              Sélectionne une sphère pour voir son état actuel
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function OptimalDiamond({ dimension, frequency, color }: { dimension: RosettaDimension; frequency: number; color: string }) {
  if (dimension === 'TECH') {
    return (
      <pre className="font-mono text-[10px] text-gray-400 overflow-x-auto">
{`{
  "schema_version": "1.0",
  "data_type": "sphere_state",
  "values": {
    "alignment": 1.0,
    "frequency": ${frequency},
    "status": "aligned",
    "integrity": "verified"
  },
  "validation_hash": "optimal"
}`}
      </pre>
    );
  }
  if (dimension === 'PEOPLE') {
    return (
      <p className="text-xs text-gray-400 leading-relaxed">
        Toutes les sphères vibrent en harmonie. Chaque donnée est traduite,
        vérifiée et cristallisée. Le système est en état de résonance optimale.
        Les engrenages tournent sans friction.
      </p>
    );
  }
  // SPIRIT
  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className="w-16 h-16 rounded-full flex items-center justify-center text-xl"
        style={{ background: `${color}22`, border: `2px solid ${color}` }}
      >
        ✦
      </div>
      <span className="text-xs" style={{ color }}>{frequency}Hz — Aligné</span>
      <span className="text-[10px] text-gray-600">Géométrie: enneagram</span>
    </div>
  );
}

function ActualDiamond({ dimension, translation }: { dimension: RosettaDimension; translation: RosettaTranslation }) {
  if (dimension === 'TECH') {
    return (
      <pre className="font-mono text-[10px] text-gray-400 overflow-x-auto">
        {JSON.stringify(translation.tech, null, 2)}
      </pre>
    );
  }
  if (dimension === 'PEOPLE') {
    const { narrative, explanation, emotional_tone } = translation.people;
    const toneColors: Record<string, string> = {
      neutre: '#888', encourageant: '#50C878', alerte: '#FFA500', celebratoire: '#D4AF37', sacre: '#9B59B6',
    };
    return (
      <div className="space-y-2">
        <p className="text-xs text-gray-300 leading-relaxed">{narrative}</p>
        {explanation && (
          <p className="text-xs text-gray-500 leading-relaxed">{explanation}</p>
        )}
        <div className="flex items-center gap-2 mt-2">
          <div
            className="w-2 h-2 rounded-full"
            style={{ background: toneColors[emotional_tone] ?? '#888' }}
          />
          <span className="text-[10px] text-gray-600">Ton: {emotional_tone}</span>
        </div>
      </div>
    );
  }
  // SPIRIT
  const { frequency_hz, resonance_level, color, sacred_geometry, vibration_signature, phi_ratio } = translation.spirit;
  return (
    <div className="flex flex-col items-center gap-3">
      <div
        className="w-16 h-16 rounded-full flex items-center justify-center text-xl"
        style={{ background: `${color}22`, border: `2px solid ${color}` }}
      >
        {resonance_level}
      </div>
      <span className="text-xs font-medium" style={{ color }}>{frequency_hz}Hz</span>
      <div className="text-[10px] text-gray-500 text-center space-y-0.5">
        <div>Géométrie: {sacred_geometry}</div>
        <div>Phi: {phi_ratio.toFixed(4)}</div>
        <div className="flex gap-1 justify-center">
          {['M', 'P', 'I', 'Po'].map((label, i) => (
            <span key={label} className="px-1 rounded" style={{ background: `${color}15` }}>
              {label}:{vibration_signature[i]}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// VUE PHAISTOS — Anneaux Concentriques des 9 Sphères
// ═══════════════════════════════════════════════════════════

function PhaistosView() {
  const { state, selectSphere } = useATOM();
  const sphereList = Object.values(SPHERES).sort((a, b) => b.index - a.index); // 9→1

  const maxSize = 320;
  const stepSize = maxSize / (sphereList.length + 1);

  return (
    <div className="flex items-center justify-center h-full">
      <div className="relative" style={{ width: maxSize, height: maxSize }}>
        {/* Anneaux concentriques (9 → 1) */}
        {sphereList.map((sphere) => {
          const size = stepSize * (sphere.index + 0.5);
          const isActive = state.active_sphere === sphere.id;
          const resonance = RESONANCE_MATRIX[sphere.index as ResonanceLevel];

          return (
            <button
              key={sphere.id}
              onClick={() => selectSphere(sphere.id)}
              className="absolute rounded-full flex items-center justify-center transition-all duration-500 group"
              style={{
                width: size,
                height: size,
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                border: `${isActive ? 2 : 1}px solid ${isActive ? sphere.color : `${sphere.color}33`}`,
                background: isActive ? `${sphere.color}08` : 'transparent',
                boxShadow: isActive ? `0 0 20px ${sphere.color}22, inset 0 0 15px ${sphere.color}08` : 'none',
                zIndex: 10 - sphere.index,
              }}
              title={`${sphere.label} — ${resonance.hz}Hz`}
            >
              {/* Label sur l'anneau (positionné en haut) */}
              <span
                className="absolute text-[9px] font-medium transition-all duration-300"
                style={{
                  top: -1,
                  color: isActive ? sphere.color : `${sphere.color}66`,
                  transform: 'translateY(-50%)',
                  background: '#050505',
                  padding: '0 4px',
                }}
              >
                {sphere.icon} {sphere.label} {resonance.hz}Hz
              </span>
            </button>
          );
        })}

        {/* Centre — Point Zéro */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center z-20"
          style={{ width: stepSize * 0.8, height: stepSize * 0.8 }}
        >
          <span className="text-lg" style={{ color: state.resonance_color }}>✦</span>
          <span className="text-[9px] font-mono font-bold" style={{ color: state.resonance_color }}>
            {state.system_frequency}Hz
          </span>
          <span className="text-[8px] text-gray-600">Point Zéro</span>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// VUE ÉMERAUDE — 7 Étapes Alchimiques (PolishingEngine)
// ═══════════════════════════════════════════════════════════

function AlchemyView() {
  const { state, parser } = useATOM();

  const stages = [
    { name: 'Calcination', icon: '🔥', color: '#FF4444', index: 1 },
    { name: 'Dissolution', icon: '💧', color: '#4488FF', index: 2 },
    { name: 'Séparation', icon: '⚔️', color: '#FFAA00', index: 3 },
    { name: 'Conjonction', icon: '🤝', color: '#44FF88', index: 4 },
    { name: 'Fermentation', icon: '🌱', color: '#88FF44', index: 5 },
    { name: 'Distillation', icon: '⚗️', color: '#AA44FF', index: 6 },
    { name: 'Coagulation', icon: '💎', color: '#FFD700', index: 7 },
  ];

  // Obtenir la validation alchimique pour la sphère active
  const validation = useMemo<EmeraldValidation | null>(() => {
    if (!state.active_sphere) return null;
    try {
      const { node, translation } = buildSeedForSphere(state.active_sphere, parser);
      return polishingEngine.polishData({ node, rosetta: translation });
    } catch {
      return null;
    }
  }, [state.active_sphere, parser]);

  return (
    <div className="space-y-2">
      <h3 className="text-xs text-gray-500 uppercase tracking-wider mb-3">
        7 Étapes de Transformation — Table d'Émeraude
      </h3>

      {/* Barre de progression globale */}
      {validation && (
        <div className="mb-4 space-y-1">
          <div className="flex justify-between text-[10px]">
            <span className="text-gray-500">Progression</span>
            <span style={{ color: validation.is_aligned ? '#50C878' : '#FFA500' }}>
              {validation.stage_index}/7 — {validation.current_stage}
            </span>
          </div>
          <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{
                width: `${(validation.stage_index / 7) * 100}%`,
                background: validation.is_aligned
                  ? 'linear-gradient(90deg, #50C878, #FFD700)'
                  : 'linear-gradient(90deg, #FFA500, #FF4444)',
              }}
            />
          </div>
        </div>
      )}

      {stages.map((stage) => {
        // Déterminer le statut de cette étape
        let status: 'passed' | 'current' | 'pending' = 'pending';
        let note = '';

        if (validation) {
          const logEntry = validation.transformation_log.find(
            (l) => l.stage === stage.name.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
          ) ?? validation.transformation_log[stage.index - 1];

          if (logEntry) {
            if (logEntry.passed) {
              status = 'passed';
            } else {
              status = 'current';
              note = logEntry.reason ?? '';
            }
          } else if (stage.index <= validation.stage_index) {
            status = validation.stage_index === stage.index ? 'current' : 'passed';
          }
        }

        const statusConfig = {
          passed: { label: 'Validé', badge: '✅', bgOpacity: '12', borderOpacity: '33' },
          current: { label: 'En cours', badge: '🔄', bgOpacity: '08', borderOpacity: '22' },
          pending: { label: 'En attente', badge: '⏳', bgOpacity: '04', borderOpacity: '11' },
        };

        const cfg = statusConfig[status];

        return (
          <div
            key={stage.name}
            className="flex items-center gap-3 px-3 py-2 rounded-md transition-all duration-300"
            style={{
              background: `${stage.color}${cfg.bgOpacity}`,
              border: `1px solid ${stage.color}${cfg.borderOpacity}`,
              opacity: status === 'pending' ? 0.5 : 1,
            }}
          >
            <span className="text-sm">{stage.icon}</span>
            <span className="text-xs font-medium" style={{ color: stage.color }}>
              {stage.index}. {stage.name}
            </span>
            <div className="flex-1" />
            {note && (
              <span className="text-[9px] text-gray-500 max-w-[150px] truncate" title={note}>
                {note}
              </span>
            )}
            <span className="text-[10px]">{cfg.badge}</span>
            <span className="text-[10px] text-gray-600 w-16 text-right">{cfg.label}</span>
          </div>
        );
      })}

      {/* Notes de polissage */}
      {validation && validation.polishing_notes.length > 0 && (
        <div className="mt-4 p-3 rounded-lg" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
          <h4 className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">Notes de Polissage</h4>
          {validation.polishing_notes.map((note, i) => (
            <p key={i} className="text-[10px] text-gray-400 mb-1">• {note}</p>
          ))}
        </div>
      )}
    </div>
  );
}
