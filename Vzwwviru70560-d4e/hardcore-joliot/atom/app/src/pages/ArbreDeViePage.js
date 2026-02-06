/**
 * AT·OM — Arbre de Vie (Séphiroth)
 * Visualisation interactive de l'Arbre kabbalistique
 * mappé sur l'écosystème AT·OM
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { SEPHIROTH, PATHS, PILLARS, WORLDS, NFT_SEPHIROTH_MAP, getPathsForSephirah, getWorldForSephirah } from '../lib/sephiroth';
import { useTokenomics } from '../hooks/useTokenomics';
import { sephirothToPoint0, POINT_0 } from '../lib/point0';
import { Point0Badge } from '../components/Point0Badge';

// ═══════════════════════════════════════════════════════════════════════════════
// TREE CANVAS — Le rendu SVG de l'Arbre
// ═══════════════════════════════════════════════════════════════════════════════

const TreeCanvas = ({ selectedSephirah, onSelect, activeFlows, nftData }) => {
  const [hoveredId, setHoveredId] = useState(null);
  const [pulse, setPulse] = useState(0);

  // Animation pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(prev => (prev + 1) % 360);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const getSephirahRadius = (sephirah) => {
    const base = 3.2;
    if (sephirah.id === 1 || sephirah.id === 6) return base * 1.3; // Keter & Tiphereth plus grands
    if (sephirah.id === 10) return base * 1.2; // Malkuth
    return base;
  };

  return (
    <div className="relative w-full" style={{ maxWidth: '500px', margin: '0 auto' }}>
      <svg
        viewBox="0 0 100 100"
        className="w-full"
        style={{ filter: 'drop-shadow(0 0 20px rgba(212, 175, 55, 0.1))' }}
      >
        <defs>
          {/* Glow filters pour chaque sephirah */}
          {SEPHIROTH.map(s => (
            <filter key={`glow-${s.id}`} id={`glow-${s.id}`} x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="1.5" result="blur" />
              <feFlood floodColor={s.color} floodOpacity="0.6" />
              <feComposite in2="blur" operator="in" />
              <feMerge>
                <feMergeNode />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          ))}

          {/* Gradient pour les chemins */}
          <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgba(212, 175, 55, 0.3)" />
            <stop offset="100%" stopColor="rgba(212, 175, 55, 0.1)" />
          </linearGradient>
        </defs>

        {/* Fond subtil — les 3 piliers */}
        <line x1="20" y1="10" x2="20" y2="95" stroke="rgba(220, 20, 60, 0.06)" strokeWidth="0.3" />
        <line x1="50" y1="2" x2="50" y2="97" stroke="rgba(212, 175, 55, 0.08)" strokeWidth="0.3" />
        <line x1="80" y1="10" x2="80" y2="95" stroke="rgba(65, 105, 225, 0.06)" strokeWidth="0.3" />

        {/* 22 Chemins (Sentiers) */}
        {PATHS.map(path => {
          const fromS = SEPHIROTH.find(s => s.id === path.from);
          const toS = SEPHIROTH.find(s => s.id === path.to);
          if (!fromS || !toS) return null;

          const isActive = activeFlows?.some(f => f.from === path.from && f.to === path.to);
          const isConnectedToSelected = selectedSephirah && (path.from === selectedSephirah || path.to === selectedSephirah);
          const isHoveredConnection = hoveredId && (path.from === hoveredId || path.to === hoveredId);

          const opacity = isActive ? 0.8 : isConnectedToSelected ? 0.6 : isHoveredConnection ? 0.4 : 0.12;
          const strokeWidth = isActive ? 0.6 : isConnectedToSelected ? 0.5 : 0.25;

          return (
            <g key={`path-${path.id}`}>
              <line
                x1={fromS.position.x}
                y1={fromS.position.y}
                x2={toS.position.x}
                y2={toS.position.y}
                stroke={isActive ? path.color : isConnectedToSelected ? '#D4AF37' : '#555'}
                strokeWidth={strokeWidth}
                opacity={opacity}
                strokeLinecap="round"
              />
              {/* Lettre hébraïque au milieu du chemin */}
              {(isConnectedToSelected || isHoveredConnection) && (
                <text
                  x={(fromS.position.x + toS.position.x) / 2}
                  y={(fromS.position.y + toS.position.y) / 2 - 1}
                  textAnchor="middle"
                  fill={path.color}
                  fontSize="2.5"
                  opacity="0.7"
                  fontFamily="serif"
                >
                  {path.letter}
                </text>
              )}
            </g>
          );
        })}

        {/* 10 Séphiroth */}
        {SEPHIROTH.map(sephirah => {
          const radius = getSephirahRadius(sephirah);
          const isSelected = selectedSephirah === sephirah.id;
          const isHovered = hoveredId === sephirah.id;
          const pulseScale = isSelected ? 1 + Math.sin(pulse * 0.05) * 0.08 : 1;
          const nftMinted = nftData?.[sephirah.nftTier]?.minted || 0;

          return (
            <g
              key={sephirah.id}
              className="cursor-pointer"
              onClick={() => onSelect(sephirah.id === selectedSephirah ? null : sephirah.id)}
              onMouseEnter={() => setHoveredId(sephirah.id)}
              onMouseLeave={() => setHoveredId(null)}
            >
              {/* Halo externe */}
              <circle
                cx={sephirah.position.x}
                cy={sephirah.position.y}
                r={radius * 2 * pulseScale}
                fill="none"
                stroke={sephirah.color}
                strokeWidth="0.15"
                opacity={isSelected ? 0.5 : isHovered ? 0.3 : 0.1}
              />

              {/* Glow */}
              <circle
                cx={sephirah.position.x}
                cy={sephirah.position.y}
                r={radius * 1.5 * pulseScale}
                fill={sephirah.colorGlow}
                opacity={isSelected ? 0.6 : isHovered ? 0.4 : 0.2}
              />

              {/* Sphère principale */}
              <circle
                cx={sephirah.position.x}
                cy={sephirah.position.y}
                r={radius * pulseScale}
                fill={sephirah.color}
                opacity={isSelected ? 1 : isHovered ? 0.9 : 0.7}
                filter={isSelected || isHovered ? `url(#glow-${sephirah.id})` : undefined}
                stroke={isSelected ? '#FFFFFF' : 'none'}
                strokeWidth={isSelected ? 0.3 : 0}
              />

              {/* Numéro */}
              <text
                x={sephirah.position.x}
                y={sephirah.position.y + 0.8}
                textAnchor="middle"
                fill={sephirah.id === 1 || sephirah.id === 6 ? '#000' : '#FFF'}
                fontSize="2.2"
                fontWeight="bold"
                fontFamily="monospace"
                style={{ pointerEvents: 'none' }}
              >
                {sephirah.id}
              </text>

              {/* Nom (à côté) */}
              <text
                x={sephirah.position.x + (sephirah.pillar === 'misericorde' ? radius + 2 : sephirah.pillar === 'rigueur' ? -(radius + 2) : 0)}
                y={sephirah.position.y + (sephirah.pillar === 'equilibre' ? -(radius + 1.5) : 0.5)}
                textAnchor={sephirah.pillar === 'misericorde' ? 'start' : sephirah.pillar === 'rigueur' ? 'end' : 'middle'}
                fill={isSelected || isHovered ? sephirah.color : '#888'}
                fontSize="1.8"
                fontWeight={isSelected ? 'bold' : 'normal'}
                style={{ pointerEvents: 'none', transition: 'fill 0.3s' }}
              >
                {sephirah.nameFr}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// DETAIL PANEL — Informations sur la Séphirah sélectionnée
// ═══════════════════════════════════════════════════════════════════════════════

const DetailPanel = ({ sephirahId, nftData, onClose }) => {
  const sephirah = SEPHIROTH.find(s => s.id === sephirahId);
  if (!sephirah) return null;

  const world = getWorldForSephirah(sephirahId);
  const paths = getPathsForSephirah(sephirahId);
  const nftInfo = NFT_SEPHIROTH_MAP[sephirah.nftTier];
  const nftStats = nftData?.[sephirah.nftTier];

  const pillarInfo = PILLARS[sephirah.pillar];

  return (
    <div className="bg-gray-900/90 backdrop-blur-md border border-gray-700 rounded-2xl p-6 space-y-5 animate-fadeIn">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div
            className="w-12 h-12 rounded-full flex items-center justify-center text-2xl"
            style={{
              background: `radial-gradient(circle, ${sephirah.colorGlow}, transparent)`,
              border: `2px solid ${sephirah.color}`,
            }}
          >
            {sephirah.symbol}
          </div>
          <div>
            <h3 className="text-xl font-bold" style={{ color: sephirah.color }}>
              {sephirah.id}. {sephirah.name}
            </h3>
            <p className="text-gray-400 text-sm">{sephirah.nameFr} — {sephirah.title}</p>
          </div>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-white text-lg">✕</button>
      </div>

      {/* Description */}
      <p className="text-gray-300 text-sm leading-relaxed">{sephirah.description}</p>

      {/* AT·OM Mapping */}
      <div className="bg-yellow-900/10 border border-yellow-600/20 rounded-lg p-3">
        <p className="text-yellow-400 text-xs font-bold mb-1">MAPPING AT·OM</p>
        <p className="text-gray-300 text-sm">{sephirah.atomDescription}</p>
      </div>

      {/* Connexion au Point 0 */}
      {(() => {
        const p0 = sephirothToPoint0(sephirah.id);
        return (
          <div className={`rounded-lg p-3 ${
            p0.isTiphereth
              ? 'bg-emerald-900/20 border border-emerald-500/30'
              : 'bg-gray-800/30 border border-gray-700'
          }`}>
            <p className={`text-xs font-bold mb-1 ${p0.isTiphereth ? 'text-emerald-400' : 'text-gray-500'}`}>
              {p0.isTiphereth ? '● POINT 0 — CŒUR DE L\'ARBRE' : 'DISTANCE AU POINT 0'}
            </p>
            {p0.isTiphereth ? (
              <p className="text-emerald-300 text-sm">
                Tiphereth = 444 Hz = Le cœur qui relie le haut et le bas.
                Point de collecte et d'émission des ajustements fréquentiels.
              </p>
            ) : (
              <div className="flex items-center justify-between">
                <span className="text-gray-400 text-sm">
                  {p0.direction === 'ascendant' ? '△' : '▽'} {p0.distance} Hz
                </span>
                <span className="text-gray-500 text-xs font-mono">
                  Harmonie: {Math.round(p0.harmony * 100)}%
                </span>
              </div>
            )}
          </div>
        );
      })()}

      {/* Properties Grid */}
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="bg-black/30 rounded-lg p-3">
          <span className="text-gray-500 text-xs">FRÉQUENCE</span>
          <p className="text-yellow-400 font-mono font-bold">{sephirah.frequency} Hz</p>
        </div>
        <div className="bg-black/30 rounded-lg p-3">
          <span className="text-gray-500 text-xs">PLANÈTE</span>
          <p className="text-gray-300">{sephirah.planet}</p>
        </div>
        <div className="bg-black/30 rounded-lg p-3">
          <span className="text-gray-500 text-xs">ÉLÉMENT</span>
          <p className="text-gray-300 capitalize">{sephirah.element}</p>
        </div>
        <div className="bg-black/30 rounded-lg p-3">
          <span className="text-gray-500 text-xs">VERTU</span>
          <p className="text-gray-300">{sephirah.virtue}</p>
        </div>
      </div>

      {/* Pillar */}
      <div className="flex items-center gap-3 p-3 rounded-lg" style={{ background: `${pillarInfo.color}10`, border: `1px solid ${pillarInfo.color}30` }}>
        <div className="w-3 h-3 rounded-full" style={{ background: pillarInfo.color }} />
        <div>
          <p className="text-sm font-medium" style={{ color: pillarInfo.color }}>{pillarInfo.nameFr}</p>
          <p className="text-gray-500 text-xs">{pillarInfo.quality}</p>
        </div>
      </div>

      {/* World */}
      {world && (
        <div className="flex items-center gap-3 p-3 rounded-lg" style={{ background: `${world.color}10`, border: `1px solid ${world.color}30` }}>
          <span className="text-lg">{world.element === 'Feu' ? '🔥' : world.element === 'Eau' ? '💧' : world.element === 'Air' ? '💨' : '🌍'}</span>
          <div>
            <p className="text-sm font-medium" style={{ color: world.color }}>
              {world.name} — {world.nameFr}
            </p>
            <p className="text-gray-500 text-xs">{world.level} • {world.atomMapping}</p>
          </div>
        </div>
      )}

      {/* NFT Tier */}
      {nftInfo && (
        <div className="bg-purple-900/10 border border-purple-500/20 rounded-lg p-3">
          <p className="text-purple-400 text-xs font-bold mb-1">NFT — {sephirah.nftTier.toUpperCase()}</p>
          <p className="text-gray-300 text-sm">{nftInfo.meaning}</p>
          {nftStats && (
            <div className="flex items-center gap-2 mt-2">
              <span className="text-purple-400 text-xs">
                {nftStats.minted || 0} / {nftStats.max_supply || '∞'} mintés
              </span>
            </div>
          )}
        </div>
      )}

      {/* Connected Paths */}
      <div>
        <p className="text-gray-500 text-xs font-bold mb-2">CHEMINS CONNECTÉS ({paths.length})</p>
        <div className="flex flex-wrap gap-2">
          {paths.map(path => {
            const otherSephirahId = path.from === sephirahId ? path.to : path.from;
            const otherS = SEPHIROTH.find(s => s.id === otherSephirahId);
            return (
              <span
                key={path.id}
                className="px-2 py-1 rounded text-xs border"
                style={{ borderColor: `${path.color}50`, color: path.color }}
              >
                {path.letter} → {otherS?.nameFr} ({path.tarot})
              </span>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// WORLDS BAR — Les 4 Mondes
// ═══════════════════════════════════════════════════════════════════════════════

const WorldsBar = ({ selectedSephirah }) => {
  const activeSephirah = selectedSephirah ? SEPHIROTH.find(s => s.id === selectedSephirah) : null;
  const activeWorld = activeSephirah ? getWorldForSephirah(activeSephirah.id) : null;

  return (
    <div className="flex gap-2">
      {Object.entries(WORLDS).map(([key, world]) => {
        const isActive = activeWorld?.name === world.name;
        return (
          <div
            key={key}
            className={`flex-1 p-2 rounded-lg text-center text-xs transition-all ${
              isActive ? 'border' : 'border border-transparent'
            }`}
            style={{
              background: isActive ? `${world.color}15` : 'rgba(0,0,0,0.2)',
              borderColor: isActive ? `${world.color}50` : 'transparent',
            }}
          >
            <p style={{ color: isActive ? world.color : '#555' }} className="font-bold">
              {world.nameFr}
            </p>
            <p className="text-gray-600 text-[10px] mt-0.5">{world.element}</p>
          </div>
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE
// ═══════════════════════════════════════════════════════════════════════════════

const ArbreDeViePage = () => {
  const navigate = useNavigate();
  const { nftAvailability, economy } = useTokenomics();
  const [selectedSephirah, setSelectedSephirah] = useState(null);
  const [activeFlows, setActiveFlows] = useState([]);
  const [showInfo, setShowInfo] = useState(false);

  // Simuler des flux d'énergie qui pulsent le long des chemins
  useEffect(() => {
    const interval = setInterval(() => {
      // Activer un chemin aléatoire pendant 2 secondes
      const randomPath = PATHS[Math.floor(Math.random() * PATHS.length)];
      setActiveFlows([{ from: randomPath.from, to: randomPath.to }]);
      setTimeout(() => setActiveFlows([]), 2000);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  // Calculer la fréquence totale de l'arbre
  const totalFrequency = SEPHIROTH.reduce((sum, s) => sum + s.frequency, 0);

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate(-1)} className="text-gray-400 hover:text-yellow-400">←</button>
            <div>
              <h1 className="text-lg font-bold text-yellow-400">ARBRE DE VIE</h1>
              <p className="text-xs text-gray-500">Séphiroth × AT·OM</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Point0Badge frequency={selectedSephirah ? SEPHIROTH.find(s => s.id === selectedSephirah)?.frequency || 444 : 444} size="sm" />
            <span className="text-yellow-400 text-xs font-mono">{totalFrequency.toFixed(1)} Hz</span>
            <button
              onClick={() => setShowInfo(!showInfo)}
              className="px-3 py-1.5 text-xs rounded-lg bg-gray-800 text-gray-400 hover:text-white transition-colors"
            >
              {showInfo ? 'Arbre' : 'Guide'}
            </button>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="pt-16 pb-8 px-4">
        <div className="max-w-6xl mx-auto">
          {showInfo ? (
            /* ═══ GUIDE MODE ═══ */
            <div className="py-8 space-y-8 max-w-2xl mx-auto">
              <div className="text-center space-y-4">
                <div className="text-5xl">🌳</div>
                <h2 className="text-2xl font-bold text-yellow-400">L'Arbre de Vie dans AT·OM</h2>
                <p className="text-gray-400">
                  L'Arbre des Séphiroth est la carte de la conscience. Chaque sphère représente
                  un aspect de la réalité, mappé sur l'écosystème AT·OM.
                </p>
              </div>

              {/* Les 3 Piliers */}
              <div className="grid grid-cols-3 gap-4">
                {Object.entries(PILLARS).map(([key, pillar]) => (
                  <div key={key} className="rounded-xl p-4 border text-center"
                    style={{ borderColor: `${pillar.color}30`, background: `${pillar.color}08` }}>
                    <p className="font-bold text-sm" style={{ color: pillar.color }}>{pillar.nameFr}</p>
                    <p className="text-gray-500 text-xs mt-1">{pillar.quality}</p>
                    <p className="text-gray-600 text-xs mt-2 capitalize">{pillar.atomRole}</p>
                  </div>
                ))}
              </div>

              {/* Les 4 Mondes */}
              <div>
                <h3 className="text-lg font-bold text-gray-300 mb-3">Les 4 Mondes</h3>
                <div className="space-y-3">
                  {Object.entries(WORLDS).map(([key, world]) => (
                    <div key={key} className="flex items-center gap-4 p-3 rounded-lg border"
                      style={{ borderColor: `${world.color}20` }}>
                      <div className="w-10 h-10 rounded-full flex items-center justify-center text-lg"
                        style={{ background: `${world.color}20` }}>
                        {world.element === 'Feu' ? '🔥' : world.element === 'Eau' ? '💧' : world.element === 'Air' ? '💨' : '🌍'}
                      </div>
                      <div>
                        <p className="font-medium text-sm" style={{ color: world.color }}>
                          {world.name} — {world.nameFr}
                        </p>
                        <p className="text-gray-500 text-xs">{world.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* NFT Mapping */}
              <div>
                <h3 className="text-lg font-bold text-gray-300 mb-3">NFT × Séphiroth</h3>
                <div className="space-y-3">
                  {Object.entries(NFT_SEPHIROTH_MAP).map(([tier, info]) => {
                    const sephirah = SEPHIROTH.find(s => s.id === info.sephirah);
                    return (
                      <div key={tier} className="flex items-center gap-4 p-3 rounded-lg bg-purple-900/10 border border-purple-500/20">
                        <div className="text-2xl">{sephirah?.symbol}</div>
                        <div>
                          <p className="text-purple-400 font-bold text-sm capitalize">{tier} → {sephirah?.nameFr}</p>
                          <p className="text-gray-500 text-xs">{info.meaning}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <button
                onClick={() => setShowInfo(false)}
                className="w-full py-3 rounded-lg bg-gradient-to-r from-yellow-600 to-yellow-500 text-black font-bold hover:from-yellow-500 hover:to-yellow-400 transition-all"
              >
                Voir l'Arbre Interactif
              </button>
            </div>
          ) : (
            /* ═══ TREE MODE ═══ */
            <div className="py-4">
              {/* Worlds Bar */}
              <div className="mb-4">
                <WorldsBar selectedSephirah={selectedSephirah} />
              </div>

              {/* Layout: Tree + Detail */}
              <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* Tree (3/5) */}
                <div className="lg:col-span-3">
                  <TreeCanvas
                    selectedSephirah={selectedSephirah}
                    onSelect={setSelectedSephirah}
                    activeFlows={activeFlows}
                    nftData={nftAvailability}
                  />

                  {/* Legend */}
                  <div className="mt-4 flex justify-center gap-6 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-blue-500" />
                      <span>Miséricorde</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-red-500" />
                      <span>Rigueur</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full" style={{ background: '#D4AF37' }} />
                      <span>Équilibre</span>
                    </div>
                  </div>
                </div>

                {/* Detail Panel (2/5) */}
                <div className="lg:col-span-2">
                  {selectedSephirah ? (
                    <DetailPanel
                      sephirahId={selectedSephirah}
                      nftData={nftAvailability}
                      onClose={() => setSelectedSephirah(null)}
                    />
                  ) : (
                    <div className="bg-gray-900/50 rounded-2xl border border-gray-800 p-6 text-center">
                      <div className="text-4xl mb-4">🌳</div>
                      <h3 className="text-yellow-400 font-bold mb-2">Sélectionnez une Séphirah</h3>
                      <p className="text-gray-500 text-sm">
                        Cliquez sur une sphère de l'Arbre pour explorer
                        ses correspondances avec l'écosystème AT·OM.
                      </p>

                      {/* Quick stats */}
                      <div className="mt-6 grid grid-cols-2 gap-3 text-left">
                        <div className="bg-black/30 rounded-lg p-3">
                          <p className="text-gray-500 text-xs">SÉPHIROTH</p>
                          <p className="text-yellow-400 font-bold text-lg">10</p>
                        </div>
                        <div className="bg-black/30 rounded-lg p-3">
                          <p className="text-gray-500 text-xs">CHEMINS</p>
                          <p className="text-yellow-400 font-bold text-lg">22</p>
                        </div>
                        <div className="bg-black/30 rounded-lg p-3">
                          <p className="text-gray-500 text-xs">FRÉQUENCE TOTALE</p>
                          <p className="text-yellow-400 font-bold text-lg">{totalFrequency.toFixed(1)}</p>
                        </div>
                        <div className="bg-black/30 rounded-lg p-3">
                          <p className="text-gray-500 text-xs">PILIERS</p>
                          <p className="text-yellow-400 font-bold text-lg">3</p>
                        </div>
                      </div>

                      {/* List of all sephiroth */}
                      <div className="mt-6 space-y-1">
                        {SEPHIROTH.map(s => (
                          <button
                            key={s.id}
                            onClick={() => setSelectedSephirah(s.id)}
                            className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors text-left"
                          >
                            <span className="text-lg">{s.symbol}</span>
                            <div className="flex-1">
                              <span className="text-sm" style={{ color: s.color }}>{s.id}. {s.nameFr}</span>
                              <span className="text-gray-600 text-xs ml-2">{s.name}</span>
                            </div>
                            <span className="text-gray-600 text-xs font-mono">{s.frequency}Hz</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default ArbreDeViePage;
