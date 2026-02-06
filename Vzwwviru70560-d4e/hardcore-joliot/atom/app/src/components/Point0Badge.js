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
 *              💚 POINT 0 BADGE — Indicateur Universel 💚
 *       Composant React connectant chaque page au cœur du système
 *
 *   Ce badge s'affiche sur CHAQUE page pour montrer:
 *   1. La fréquence actuelle de l'utilisateur
 *   2. Sa distance au Point 0 (444 Hz)
 *   3. Son état d'harmonisation personnelle
 *   4. Sa connexion aux points lumineux géographiques
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  POINT_0,
  SIGNAL,
  RESONANCE_MATRIX,
  distanceToPoint0,
  pulseColor,
  point0Indicator,
  activeAnuhazi,
  POWER_BUTTONS
} from '../lib/point0';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: POINT 0 BADGE (Compact — pour Header/StatusBar)
// ═══════════════════════════════════════════════════════════════════════════════

export const Point0Badge = ({ frequency = 444, showLabel = true, size = 'sm' }) => {
  const [pulse, setPulse] = useState(false);
  const indicator = useMemo(() => point0Indicator(frequency), [frequency]);

  // Pulsation au rythme du système (4.44s)
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(true);
      setTimeout(() => setPulse(false), 500);
    }, SIGNAL.HEARTBEAT);
    return () => clearInterval(interval);
  }, []);

  const sizeClasses = {
    xs: 'text-xs px-1.5 py-0.5',
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2',
  };

  return (
    <div
      className={`inline-flex items-center gap-1.5 rounded-full border transition-all duration-300 ${sizeClasses[size]}`}
      style={{
        borderColor: `${indicator.color}40`,
        backgroundColor: `${indicator.color}10`,
        boxShadow: pulse && indicator.pulse ? `0 0 12px ${indicator.color}40` : 'none',
      }}
      title={`${indicator.text} | Harmonie: ${Math.round(distanceToPoint0(frequency).harmony * 100)}%`}
    >
      {/* Indicateur de pouls */}
      <div
        className={`rounded-full transition-all duration-300 ${
          size === 'xs' ? 'w-1.5 h-1.5' : 'w-2 h-2'
        }`}
        style={{
          backgroundColor: indicator.color,
          boxShadow: pulse ? `0 0 6px ${indicator.color}` : 'none',
          transform: pulse ? 'scale(1.3)' : 'scale(1)',
        }}
      />

      {/* Fréquence */}
      <span className="font-mono" style={{ color: indicator.color }}>
        {frequency}
      </span>

      {showLabel && (
        <span className="text-gray-500">Hz</span>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HARMONISATION PERSONNELLE
// Affiche l'état fréquentiel unique de chaque utilisateur
// ═══════════════════════════════════════════════════════════════════════════════

export const PersonalHarmonizer = ({ userFrequency = 444, userName = 'Utilisateur', location = null }) => {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [breathCycle, setBreathCycle] = useState(0);
  const indicator = useMemo(() => point0Indicator(userFrequency), [userFrequency]);
  const anuhazi = useMemo(() => activeAnuhazi(userFrequency), [userFrequency]);
  const resonance = useMemo(() => distanceToPoint0(userFrequency), [userFrequency]);

  // Cycle de respiration (8.88 secondes)
  useEffect(() => {
    const interval = setInterval(() => {
      setBreathCycle(prev => (prev + 1) % 100);
    }, SIGNAL.BREATH / 100);
    return () => clearInterval(interval);
  }, []);

  // Phase d'harmonisation (4 phases = 4 boutons Anuhazi)
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPhase(prev => (prev + 1) % 4);
    }, SIGNAL.INTERVAL);
    return () => clearInterval(interval);
  }, []);

  const harmonyPercent = Math.round(resonance.harmony * 100);

  return (
    <div className="bg-black/50 border border-gray-800 rounded-xl p-4 space-y-4">
      {/* En-tête: Nom + Fréquence */}
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-white font-medium text-sm">{userName}</h4>
          <p className="text-gray-500 text-xs">
            {location ? `📍 ${location}` : 'Harmonisation active'}
          </p>
        </div>
        <Point0Badge frequency={userFrequency} size="md" />
      </div>

      {/* Barre d'harmonie avec Point 0 */}
      <div>
        <div className="flex items-center justify-between mb-1">
          <span className="text-gray-500 text-xs">Harmonie au Point 0</span>
          <span className="font-mono text-xs" style={{ color: indicator.color }}>
            {harmonyPercent}%
          </span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden relative">
          {/* Marqueur Point 0 (444 Hz) au centre */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-emerald-400 z-10"
            style={{ left: `${((444 - 111) / (999 - 111)) * 100}%` }}
          />
          {/* Barre de fréquence utilisateur */}
          <div
            className="h-full rounded-full transition-all duration-1000"
            style={{
              width: `${((userFrequency - 111) / (999 - 111)) * 100}%`,
              backgroundColor: indicator.color,
            }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-700 mt-1">
          <span>111 Hz</span>
          <span className="text-emerald-400/50">444</span>
          <span>999 Hz</span>
        </div>
      </div>

      {/* 4 Boutons Anuhazi — Phase actuelle */}
      <div className="flex gap-1.5">
        {POWER_BUTTONS.map((btn, i) => (
          <div
            key={btn.id}
            className={`flex-1 text-center py-1.5 rounded-lg border transition-all duration-500 ${
              i === currentPhase
                ? 'border-current scale-105'
                : 'border-gray-800 opacity-40'
            }`}
            style={{
              borderColor: i === currentPhase ? btn.color : undefined,
              backgroundColor: i === currentPhase ? `${btn.color}15` : undefined,
            }}
          >
            <div className="text-sm" style={{ color: i === currentPhase ? btn.color : '#666' }}>
              {btn.symbol}
            </div>
            <div className="text-xs mt-0.5" style={{ color: i === currentPhase ? btn.color : '#444' }}>
              {btn.name}
            </div>
          </div>
        ))}
      </div>

      {/* Niveau de résonance */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-500">
          Résonance: <span style={{ color: resonance.resonanceLevel.color }}>
            {resonance.resonanceLevel.name}
          </span>
        </span>
        <span className="text-gray-600">
          {resonance.direction === 'ancré' ? '● Ancré' :
           resonance.direction === 'ascendant' ? '△ Ascendant' : '▽ Descendant'}
        </span>
      </div>

      {/* Cycle de respiration */}
      <div className="h-1 bg-gray-900 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500/30 rounded-full transition-all duration-100"
          style={{ width: `${breathCycle}%` }}
        />
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: RÉSONANCE MATRICE VISUELLE
// Affiche les 9 niveaux avec la position de l'utilisateur
// ═══════════════════════════════════════════════════════════════════════════════

export const ResonanceMatrix = ({ currentFrequency = 444, compact = false }) => {
  const closestLevel = useMemo(() => {
    return RESONANCE_MATRIX.reduce((prev, curr) =>
      Math.abs(curr.frequency - currentFrequency) < Math.abs(prev.frequency - currentFrequency) ? curr : prev
    );
  }, [currentFrequency]);

  if (compact) {
    return (
      <div className="flex items-center gap-1">
        {RESONANCE_MATRIX.map(level => (
          <div
            key={level.level}
            className={`w-2 h-2 rounded-full transition-all ${
              level.level === closestLevel.level ? 'scale-150 ring-1 ring-white/30' : 'opacity-30'
            }`}
            style={{ backgroundColor: level.color }}
            title={`${level.name} — ${level.frequency} Hz`}
          />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-9 gap-1">
      {RESONANCE_MATRIX.map(level => {
        const isActive = level.level === closestLevel.level;
        const isAnchor = level.isAnchor;

        return (
          <div
            key={level.level}
            className={`text-center py-2 rounded-lg border transition-all ${
              isActive ? 'scale-105 shadow-lg' :
              isAnchor ? 'border-emerald-500/30' : 'border-gray-800 opacity-50'
            }`}
            style={{
              borderColor: isActive ? level.color : undefined,
              backgroundColor: isActive ? `${level.color}15` : undefined,
              boxShadow: isActive ? `0 0 12px ${level.color}30` : undefined,
            }}
          >
            <div
              className={`text-lg font-bold ${isActive ? '' : 'text-gray-600'}`}
              style={{ color: isActive ? level.color : undefined }}
            >
              {level.level}
            </div>
            <div className="text-xs text-gray-500 mt-0.5">
              {level.frequency}
            </div>
            {isAnchor && (
              <div className="text-xs mt-0.5">💚</div>
            )}
          </div>
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: STATUS BAR POINT 0
// Barre de statut en bas de page montrant la connexion au Point 0
// ═══════════════════════════════════════════════════════════════════════════════

export const Point0StatusBar = ({ frequency = 444, pageName = '', version = 'CHE·NU V76' }) => {
  const indicator = useMemo(() => point0Indicator(frequency), [frequency]);
  const harmony = useMemo(() => distanceToPoint0(frequency).harmony, [frequency]);

  return (
    <div className="flex items-center justify-between px-4 py-1.5 bg-black/80 border-t border-gray-900 text-xs">
      {/* Gauche: Page + Point 0 */}
      <div className="flex items-center gap-3">
        {pageName && (
          <span className="text-gray-600">{pageName}</span>
        )}
        <Point0Badge frequency={frequency} size="xs" showLabel={false} />
      </div>

      {/* Centre: Protocoles */}
      <div className="flex items-center gap-2 text-gray-700">
        <span>≈ AQUA</span>
        <span>•</span>
        <span>◆ ADAMAS</span>
      </div>

      {/* Droite: Version + Harmonie */}
      <div className="flex items-center gap-3">
        <span className="text-gray-600 font-mono">
          ♡ {Math.round(harmony * 100)}%
        </span>
        <span className="text-gray-700">{version}</span>
      </div>
    </div>
  );
};

export default Point0Badge;
