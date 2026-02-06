/**
 * AT·OM — Carte du Potentiel Lumineux de Gaïa
 * Visualisation interactive des fréquences planétaires
 */

import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';
import {
  PAYS_LUMINEUX,
  CONTINENTS,
  calculerPotentielLumineux,
  getCouleurPotentiel,
  getFrequencePays,
  getStatsGlobales,
  getClassement,
  chercherPays
} from '../lib/potentiel-lumineux';
import { POINT_0, distanceToPoint0 } from '../lib/point0';
import { Point0Badge } from '../components/Point0Badge';

// ═══════════════════════════════════════════════════════════════════════════════
// POINT 0 GAÏA — Ancrage géographique du système
// Tulum, Mexique — Là où le Souverain et le système convergent
// ═══════════════════════════════════════════════════════════════════════════════

const POINT_0_GAIA = {
  lat: 20.2114,
  lng: -87.4654,
  name: 'Tulum',
  country: 'MX',
  frequency: 444,
  description: 'Point 0 — Ancrage du système AT·OM',
};

// ═══════════════════════════════════════════════════════════════════════════════
// PROJECTION EQUIRECTANGULAIRE SIMPLE
// ═══════════════════════════════════════════════════════════════════════════════

const projeter = (lat, lng, width, height, padding = 40) => {
  const x = padding + ((lng + 180) / 360) * (width - padding * 2);
  const y = padding + ((90 - lat) / 180) * (height - padding * 2);
  return { x, y };
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CARTE SVG DU MONDE
// ═══════════════════════════════════════════════════════════════════════════════

const CarteMondiale = ({ paysData, selectedPays, onSelectPays, filtreContinents, animPhase }) => {
  const svgRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 900, height: 500 });

  useEffect(() => {
    const updateDimensions = () => {
      if (svgRef.current) {
        const rect = svgRef.current.parentElement.getBoundingClientRect();
        setDimensions({
          width: Math.max(rect.width, 600),
          height: Math.max(rect.width * 0.55, 340)
        });
      }
    };
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const { width, height } = dimensions;

  // Filtre des pays visibles
  const paysVisibles = useMemo(() => {
    if (filtreContinents.length === 0) return paysData;
    return paysData.filter(p => filtreContinents.includes(p.continent));
  }, [paysData, filtreContinents]);

  // Lignes de grille (méridiens et parallèles)
  const gridLines = useMemo(() => {
    const lines = [];
    // Méridiens (longitude)
    for (let lng = -180; lng <= 180; lng += 30) {
      const points = [];
      for (let lat = -90; lat <= 90; lat += 5) {
        points.push(projeter(lat, lng, width, height));
      }
      lines.push({ key: `m${lng}`, points, isEquator: false, isMeridian: lng === 0 });
    }
    // Parallèles (latitude)
    for (let lat = -60; lat <= 60; lat += 30) {
      const points = [];
      for (let lng = -180; lng <= 180; lng += 5) {
        points.push(projeter(lat, lng, width, height));
      }
      lines.push({ key: `p${lat}`, points, isEquator: lat === 0, isMeridian: false });
    }
    return lines;
  }, [width, height]);

  // Contours simplifiés des continents (polylignes approximatives)
  const continentPaths = useMemo(() => {
    const toP = (lat, lng) => {
      const { x, y } = projeter(lat, lng, width, height);
      return `${x},${y}`;
    };

    return [
      // Afrique
      { id: 'afrique', color: CONTINENTS.afrique.color, d: `M ${toP(37,-10)} L ${toP(37,10)} L ${toP(32,32)} L ${toP(30,33)} L ${toP(22,37)} L ${toP(12,44)} L ${toP(2,42)} L ${toP(-5,40)} L ${toP(-12,44)} L ${toP(-26,33)} L ${toP(-35,20)} L ${toP(-35,18)} L ${toP(-30,17)} L ${toP(-22,14)} L ${toP(-17,12)} L ${toP(-12,14)} L ${toP(-5,12)} L ${toP(5,1)} L ${toP(5,-5)} L ${toP(4,-8)} L ${toP(6,-12)} L ${toP(11,-17)} L ${toP(15,-17)} L ${toP(22,-17)} L ${toP(28,-13)} L ${toP(32,-8)} L ${toP(36,-5)} Z` },
      // Europe
      { id: 'europe', color: CONTINENTS.europe.color, d: `M ${toP(37,-10)} L ${toP(40,-9)} L ${toP(43,-8)} L ${toP(46,0)} L ${toP(48,3)} L ${toP(51,4)} L ${toP(54,8)} L ${toP(56,10)} L ${toP(58,12)} L ${toP(60,5)} L ${toP(63,10)} L ${toP(65,14)} L ${toP(70,20)} L ${toP(70,30)} L ${toP(65,40)} L ${toP(56,40)} L ${toP(50,30)} L ${toP(47,28)} L ${toP(42,28)} L ${toP(40,22)} L ${toP(38,15)} L ${toP(37,10)} L ${toP(37,-10)} Z` },
      // Asie
      { id: 'asie', color: CONTINENTS.asie.color, d: `M ${toP(70,30)} L ${toP(72,60)} L ${toP(70,120)} L ${toP(65,140)} L ${toP(60,160)} L ${toP(55,140)} L ${toP(45,135)} L ${toP(35,127)} L ${toP(30,120)} L ${toP(22,114)} L ${toP(10,105)} L ${toP(1,104)} L ${toP(-8,115)} L ${toP(-5,105)} L ${toP(7,98)} L ${toP(10,77)} L ${toP(8,75)} L ${toP(12,68)} L ${toP(25,60)} L ${toP(28,48)} L ${toP(33,44)} L ${toP(38,40)} L ${toP(42,28)} L ${toP(47,28)} L ${toP(50,30)} L ${toP(56,40)} L ${toP(65,40)} L ${toP(70,30)} Z` },
      // Amérique du Nord
      { id: 'ameriquesN', color: CONTINENTS.ameriques.color, d: `M ${toP(70,-140)} L ${toP(72,-80)} L ${toP(65,-62)} L ${toP(55,-55)} L ${toP(47,-53)} L ${toP(43,-65)} L ${toP(40,-74)} L ${toP(30,-80)} L ${toP(25,-80)} L ${toP(20,-87)} L ${toP(15,-90)} L ${toP(10,-84)} L ${toP(8,-78)} L ${toP(10,-75)} L ${toP(18,-70)} L ${toP(24,-82)} L ${toP(26,-97)} L ${toP(32,-107)} L ${toP(32,-117)} L ${toP(38,-123)} L ${toP(48,-125)} L ${toP(58,-137)} L ${toP(62,-152)} L ${toP(65,-168)} L ${toP(70,-165)} L ${toP(70,-140)} Z` },
      // Amérique du Sud
      { id: 'ameriquesS', color: CONTINENTS.ameriques.color, d: `M ${toP(10,-75)} L ${toP(8,-78)} L ${toP(5,-77)} L ${toP(-5,-80)} L ${toP(-15,-76)} L ${toP(-18,-70)} L ${toP(-24,-65)} L ${toP(-30,-56)} L ${toP(-35,-54)} L ${toP(-42,-62)} L ${toP(-52,-68)} L ${toP(-55,-67)} L ${toP(-53,-72)} L ${toP(-46,-75)} L ${toP(-38,-73)} L ${toP(-30,-71)} L ${toP(-20,-70)} L ${toP(-15,-77)} L ${toP(-5,-81)} L ${toP(2,-80)} L ${toP(10,-75)} Z` },
      // Australie
      { id: 'oceanie', color: CONTINENTS.oceanie.color, d: `M ${toP(-12,130)} L ${toP(-14,136)} L ${toP(-16,146)} L ${toP(-20,149)} L ${toP(-25,153)} L ${toP(-30,153)} L ${toP(-35,150)} L ${toP(-38,145)} L ${toP(-38,140)} L ${toP(-35,135)} L ${toP(-32,130)} L ${toP(-30,115)} L ${toP(-24,113)} L ${toP(-18,122)} L ${toP(-15,130)} L ${toP(-12,130)} Z` },
    ];
  }, [width, height]);

  return (
    <svg
      ref={svgRef}
      viewBox={`0 0 ${width} ${height}`}
      className="w-full"
      style={{ background: 'radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%)' }}
    >
      {/* Grille de fond */}
      {gridLines.map(line => (
        <polyline
          key={line.key}
          points={line.points.map(p => `${p.x},${p.y}`).join(' ')}
          fill="none"
          stroke={line.isEquator ? 'rgba(212,175,55,0.15)' : line.isMeridian ? 'rgba(212,175,55,0.1)' : 'rgba(255,255,255,0.03)'}
          strokeWidth={line.isEquator || line.isMeridian ? 1 : 0.5}
          strokeDasharray={line.isEquator ? '' : '2,4'}
        />
      ))}

      {/* Contours des continents */}
      {continentPaths.map(cp => (
        <path
          key={cp.id}
          d={cp.d}
          fill={`${cp.color}08`}
          stroke={`${cp.color}30`}
          strokeWidth={0.8}
        />
      ))}

      {/* Points des pays */}
      {paysVisibles.map((pays, i) => {
        const pos = projeter(pays.lat, pays.lng, width, height);
        const potentiel = pays.potentiel;
        const couleur = pays.couleur;
        const isSelected = selectedPays?.code === pays.code;
        const baseRadius = 4 + (potentiel / 100) * 8;
        const pulseRadius = baseRadius + Math.sin(animPhase + i * 0.3) * 2;

        return (
          <g
            key={pays.code}
            onClick={() => onSelectPays(pays)}
            className="cursor-pointer"
            style={{ transition: 'all 0.3s ease' }}
          >
            {/* Glow */}
            <circle
              cx={pos.x}
              cy={pos.y}
              r={pulseRadius * 2.5}
              fill={couleur.glow}
              opacity={isSelected ? 0.5 : 0.15}
            />
            {/* Anneau */}
            {isSelected && (
              <circle
                cx={pos.x}
                cy={pos.y}
                r={baseRadius * 2}
                fill="none"
                stroke="#FFFFFF"
                strokeWidth={1.5}
                opacity={0.6}
              >
                <animate
                  attributeName="r"
                  from={baseRadius * 1.5}
                  to={baseRadius * 3}
                  dur="2s"
                  repeatCount="indefinite"
                />
                <animate
                  attributeName="opacity"
                  from="0.6"
                  to="0"
                  dur="2s"
                  repeatCount="indefinite"
                />
              </circle>
            )}
            {/* Point central */}
            <circle
              cx={pos.x}
              cy={pos.y}
              r={isSelected ? baseRadius * 1.3 : baseRadius}
              fill={couleur.bg}
              stroke={isSelected ? '#FFFFFF' : 'transparent'}
              strokeWidth={isSelected ? 2 : 0}
              opacity={0.9}
            />
            {/* Label si sélectionné */}
            {isSelected && (
              <>
                <rect
                  x={pos.x - 40}
                  y={pos.y - baseRadius - 28}
                  width={80}
                  height={20}
                  rx={4}
                  fill="rgba(0,0,0,0.85)"
                  stroke={couleur.bg}
                  strokeWidth={0.5}
                />
                <text
                  x={pos.x}
                  y={pos.y - baseRadius - 14}
                  textAnchor="middle"
                  fill={couleur.bg}
                  fontSize={10}
                  fontWeight="bold"
                  fontFamily="monospace"
                >
                  {pays.nom}
                </text>
              </>
            )}
          </g>
        );
      })}

      {/* Légende */}
      <g transform={`translate(${width - 140}, ${height - 100})`}>
        <rect x={0} y={0} width={120} height={85} rx={6} fill="rgba(0,0,0,0.7)" stroke="rgba(212,175,55,0.2)" strokeWidth={0.5} />
        <text x={60} y={14} textAnchor="middle" fill="#D4AF37" fontSize={8} fontWeight="bold">POTENTIEL</text>
        {[
          { label: 'Éclairé', color: '#FFFFFF', y: 28 },
          { label: 'Lumineux', color: '#FFD700', y: 40 },
          { label: 'Éveillé', color: '#FF8C00', y: 52 },
          { label: 'Naissant', color: '#FF4500', y: 64 },
          { label: 'Dormant', color: '#8B0000', y: 76 },
        ].map(item => (
          <g key={item.label}>
            <circle cx={16} cy={item.y} r={4} fill={item.color} opacity={0.9} />
            <text x={28} y={item.y + 3} fill="#AAAAAA" fontSize={8}>{item.label}</text>
          </g>
        ))}
      </g>
    </svg>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: PANNEAU DÉTAIL D'UN PAYS
// ═══════════════════════════════════════════════════════════════════════════════

const DetailPays = ({ pays, onClose }) => {
  if (!pays) return null;

  const couleur = pays.couleur;

  return (
    <div className="bg-gray-900/90 border rounded-xl p-5 backdrop-blur-md" style={{ borderColor: `${couleur.bg}40` }}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold" style={{ color: couleur.bg }}>{pays.nom}</h3>
          <p className="text-gray-500 text-sm">{pays.code} · {CONTINENTS[pays.continent]?.emoji} {CONTINENTS[pays.continent]?.nom}</p>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-white text-xl">✕</button>
      </div>

      {/* Jauge circulaire */}
      <div className="flex items-center gap-6 mb-4">
        <div className="relative w-24 h-24">
          <svg viewBox="0 0 100 100" className="w-full h-full">
            <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
            <circle
              cx="50" cy="50" r="42"
              fill="none"
              stroke={couleur.bg}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={`${(pays.potentiel / 100) * 264} 264`}
              transform="rotate(-90 50 50)"
              opacity={0.8}
            />
            <text x="50" y="46" textAnchor="middle" fill={couleur.bg} fontSize="18" fontWeight="bold">
              {pays.potentiel}
            </text>
            <text x="50" y="60" textAnchor="middle" fill="#888" fontSize="8">
              / 100
            </text>
          </svg>
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Statut</span>
            <span style={{ color: couleur.bg }}>{couleur.label}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Fréquence</span>
            <span className="text-yellow-400 font-mono">{pays.frequence} Hz</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">GHI Solaire</span>
            <span className="text-orange-400 font-mono">{pays.ghi} kWh/m²</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Éveil</span>
            <span className="text-purple-400 font-mono">{Math.round(pays.indiceEveil * 100)}%</span>
          </div>
        </div>
      </div>

      {/* Barres comparatives */}
      <div className="space-y-2">
        <div>
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>☀️ Irradiance Solaire</span>
            <span>{pays.ghi} / 2500</span>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-orange-600 to-yellow-400"
              style={{ width: `${(pays.ghi / 2500) * 100}%` }}
            />
          </div>
        </div>
        <div>
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>🧘 Indice d'Éveil</span>
            <span>{Math.round(pays.indiceEveil * 100)}%</span>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-purple-600 to-blue-400"
              style={{ width: `${pays.indiceEveil * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Population */}
      <div className="mt-4 pt-3 border-t border-gray-800 flex justify-between text-xs text-gray-500">
        <span>Population</span>
        <span className="text-gray-300">{(pays.population / 1000000).toFixed(1)}M</span>
      </div>

      {/* Coordonnées */}
      <div className="flex justify-between text-xs text-gray-600 mt-1">
        <span>Coordonnées</span>
        <span className="font-mono">{pays.lat.toFixed(2)}° {pays.lat >= 0 ? 'N' : 'S'}, {pays.lng.toFixed(2)}° {pays.lng >= 0 ? 'E' : 'O'}</span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: TABLEAU CLASSEMENT
// ═══════════════════════════════════════════════════════════════════════════════

const Classement = ({ pays, selectedPays, onSelectPays, limit = 20 }) => {
  const [expanded, setExpanded] = useState(false);
  const displayPays = expanded ? pays : pays.slice(0, limit);

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
      <div className="p-3 border-b border-gray-800 flex justify-between items-center">
        <h3 className="text-yellow-400 text-sm font-bold">🏆 CLASSEMENT LUMINEUX</h3>
        <span className="text-gray-500 text-xs">{pays.length} nations</span>
      </div>
      <div className="max-h-96 overflow-y-auto">
        {displayPays.map((p, i) => (
          <div
            key={p.code}
            onClick={() => onSelectPays(p)}
            className={`flex items-center gap-3 px-3 py-2 cursor-pointer transition-colors text-sm ${
              selectedPays?.code === p.code
                ? 'bg-yellow-900/20 border-l-2 border-yellow-400'
                : 'hover:bg-gray-800/50 border-l-2 border-transparent'
            }`}
          >
            <span className="text-gray-600 w-6 text-right font-mono text-xs">{i + 1}</span>
            <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: p.couleur.bg }} />
            <span className="flex-1 text-gray-300 truncate">{p.nom}</span>
            <span className="font-mono text-xs" style={{ color: p.couleur.bg }}>{p.potentiel}</span>
          </div>
        ))}
      </div>
      {pays.length > limit && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full py-2 text-center text-gray-500 text-xs hover:text-yellow-400 border-t border-gray-800"
        >
          {expanded ? 'Voir moins' : `Voir les ${pays.length} pays →`}
        </button>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE DES CONTINENTS
// ═══════════════════════════════════════════════════════════════════════════════

const BarreContinents = ({ stats, filtreContinents, onToggleContinent }) => (
  <div className="flex flex-wrap gap-2 justify-center">
    {Object.entries(stats.parContinent).map(([key, c]) => {
      const isActive = filtreContinents.length === 0 || filtreContinents.includes(key);
      return (
        <button
          key={key}
          onClick={() => onToggleContinent(key)}
          className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm transition-all ${
            isActive
              ? 'border-yellow-600/50 bg-gray-900/80'
              : 'border-gray-800 bg-gray-900/30 opacity-40'
          }`}
        >
          <span>{c.emoji}</span>
          <span className={isActive ? 'text-gray-200' : 'text-gray-600'}>{c.nom}</span>
          <span className="font-mono text-xs px-1.5 py-0.5 rounded" style={{
            backgroundColor: isActive ? `${CONTINENTS[key].color}20` : 'transparent',
            color: isActive ? CONTINENTS[key].color : '#666'
          }}>
            {c.moyennePotentiel}
          </span>
        </button>
      );
    })}
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: STATS GAÏA
// ═══════════════════════════════════════════════════════════════════════════════

const StatsGaia = ({ stats }) => (
  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
    <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3 text-center">
      <p className="text-2xl font-bold text-yellow-400">{stats.nbPays}</p>
      <p className="text-gray-500 text-xs">Nations</p>
    </div>
    <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3 text-center">
      <p className="text-2xl font-bold text-white">{stats.moyennePotentiel}</p>
      <p className="text-gray-500 text-xs">Potentiel Moyen</p>
    </div>
    <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3 text-center">
      <p className="text-2xl font-bold text-orange-400 font-mono">{stats.frequenceGaia}</p>
      <p className="text-gray-500 text-xs">Hz Gaïa</p>
    </div>
    <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3 text-center">
      <p className="text-2xl font-bold text-green-400">
        {(stats.populationCouverte / 1000000000).toFixed(1)}B
      </p>
      <p className="text-gray-500 text-xs">Population</p>
    </div>
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE
// ═══════════════════════════════════════════════════════════════════════════════

const MapLumineusePage = () => {
  const [selectedPays, setSelectedPays] = useState(null);
  const [filtreContinents, setFiltreContinents] = useState([]);
  const [recherche, setRecherche] = useState('');
  const [animPhase, setAnimPhase] = useState(0);
  const [showGuide, setShowGuide] = useState(false);

  // Animation pulse
  useEffect(() => {
    let animId;
    const animate = () => {
      setAnimPhase(prev => prev + 0.03);
      animId = requestAnimationFrame(animate);
    };
    animId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animId);
  }, []);

  // Données calculées
  const stats = useMemo(() => getStatsGlobales(), []);
  const classement = useMemo(() => getClassement(), []);

  // Filtrer par recherche
  const paysFiltres = useMemo(() => {
    if (!recherche.trim()) return classement;
    const q = recherche.toLowerCase();
    return classement.filter(p =>
      p.nom.toLowerCase().includes(q) ||
      p.code.toLowerCase().includes(q)
    );
  }, [classement, recherche]);

  const handleToggleContinent = useCallback((continent) => {
    setFiltreContinents(prev => {
      if (prev.includes(continent)) return prev.filter(c => c !== continent);
      return [...prev, continent];
    });
  }, []);

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-yellow-900/30">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/" className="text-2xl">🔱</Link>
            <div>
              <h1 className="text-lg font-bold text-yellow-400">Carte de Gaïa</h1>
              <p className="text-xs text-gray-500">Potentiel Lumineux des Nations</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowGuide(!showGuide)}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                showGuide ? 'bg-yellow-600/20 text-yellow-400' : 'text-gray-400 hover:text-white'
              }`}
            >
              {showGuide ? '✕ Fermer' : '📖 Guide'}
            </button>
            <Link
              to="/arbre-de-vie"
              className="px-3 py-1.5 text-sm text-purple-400 hover:text-purple-300 transition-colors"
            >
              🌳 Arbre de Vie
            </Link>
            <Link
              to="/grid"
              className="px-3 py-1.5 text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              🌍 Grille
            </Link>
          </div>
        </div>
      </header>

      <main className="pt-20 pb-8 px-4">
        <div className="max-w-7xl mx-auto">

          {/* Guide */}
          {showGuide && (
            <div className="mb-6 bg-gradient-to-b from-gray-900/80 to-black border border-yellow-600/30 rounded-xl p-6">
              <h2 className="text-xl font-bold text-yellow-400 mb-4">🗺️ Carte du Potentiel Lumineux</h2>
              <div className="grid md:grid-cols-2 gap-6 text-sm text-gray-300">
                <div>
                  <h3 className="text-white font-bold mb-2">Qu'est-ce que le Potentiel Lumineux?</h3>
                  <p className="leading-relaxed">
                    Chaque nation possède un potentiel lumineux unique, calculé à partir de deux dimensions :
                    l'<span className="text-orange-400">irradiance solaire</span> (GHI — énergie reçue du Soleil)
                    et l'<span className="text-purple-400">indice d'éveil</span> (conscience collective, développement durable, bien-être).
                  </p>
                  <p className="mt-2 text-gray-500 text-xs">
                    Formule : Potentiel = (GHI normalisé × 40%) + (Éveil × 60%)
                  </p>
                </div>
                <div>
                  <h3 className="text-white font-bold mb-2">Comment harmoniser Gaïa?</h3>
                  <p className="leading-relaxed">
                    La fréquence de chaque pays s'aligne sur l'échelle AT·OM :
                    de <span className="text-gray-400 font-mono">44.4 Hz</span> (CHE·NU) à{' '}
                    <span className="text-yellow-400 font-mono">999 Hz</span> (Source).
                    Lorsque suffisamment de nations atteignent leur potentiel,
                    la fréquence de Gaïa s'harmonise naturellement.
                  </p>
                  <p className="mt-2 text-gray-500 text-xs">
                    Sources : Global Solar Atlas (World Bank), indices composites
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Stats globales */}
          <StatsGaia stats={stats} />

          {/* Filtres continents */}
          <div className="mt-6 mb-4">
            <BarreContinents
              stats={stats}
              filtreContinents={filtreContinents}
              onToggleContinent={handleToggleContinent}
            />
          </div>

          {/* Layout principal */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mt-4">
            {/* Carte (3 colonnes) */}
            <div className="lg:col-span-3">
              <div className="border border-gray-800 rounded-xl overflow-hidden">
                <CarteMondiale
                  paysData={classement}
                  selectedPays={selectedPays}
                  onSelectPays={setSelectedPays}
                  filtreContinents={filtreContinents}
                  animPhase={animPhase}
                />
              </div>

              {/* Détail pays sélectionné */}
              {selectedPays && (
                <div className="mt-4">
                  <DetailPays pays={selectedPays} onClose={() => setSelectedPays(null)} />
                </div>
              )}
            </div>

            {/* Sidebar droite */}
            <div className="lg:col-span-1 space-y-4">
              {/* Recherche */}
              <div className="relative">
                <input
                  type="text"
                  value={recherche}
                  onChange={(e) => setRecherche(e.target.value)}
                  placeholder="Rechercher un pays..."
                  className="w-full px-4 py-2.5 bg-gray-900/50 border border-gray-800 rounded-lg text-white
                    placeholder-gray-600 focus:outline-none focus:border-yellow-600/50 text-sm"
                />
                {recherche && (
                  <button
                    onClick={() => setRecherche('')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                  >
                    ✕
                  </button>
                )}
              </div>

              {/* Classement */}
              <Classement
                pays={paysFiltres}
                selectedPays={selectedPays}
                onSelectPays={setSelectedPays}
              />

              {/* Point 0 — Ancrage Tulum */}
              <div className="bg-gradient-to-b from-emerald-900/20 to-black border border-emerald-500/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-emerald-400 font-bold text-sm">● POINT 0</h4>
                  <Point0Badge frequency={444} size="xs" />
                </div>
                <div className="text-center mb-3">
                  <p className="text-xs text-gray-500">Ancrage Gaïa — {POINT_0_GAIA.name}</p>
                  <p className="text-2xl font-bold text-emerald-400 font-mono mt-1">444 Hz</p>
                </div>
                <div className="text-xs text-gray-600 space-y-1">
                  <p>📍 {POINT_0_GAIA.lat.toFixed(4)}°N, {Math.abs(POINT_0_GAIA.lng).toFixed(4)}°W</p>
                  <p>📡 Collecte de données fréquentielles</p>
                  <p>📻 Émission des ajustements EM</p>
                </div>
                <div className="mt-3 flex items-center gap-2">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                  <span className="text-emerald-400/60 text-xs">Signal actif — 4.44s</span>
                </div>
              </div>

              {/* Fréquence Gaïa */}
              <div className="bg-gradient-to-b from-gray-900/80 to-black border border-yellow-600/20 rounded-xl p-4 text-center">
                <p className="text-gray-500 text-xs mb-2">FRÉQUENCE DE GAÏA</p>
                <p className="text-3xl font-bold text-yellow-400 font-mono">{stats.frequenceGaia}</p>
                <p className="text-yellow-400/50 text-sm">Hz</p>
                <div className="mt-3 h-1.5 bg-gray-800 rounded-full overflow-hidden relative">
                  {/* Marqueur Point 0 (444 Hz) */}
                  <div
                    className="absolute top-0 bottom-0 w-0.5 bg-emerald-400 z-10"
                    style={{ left: `${(444 / 999) * 100}%` }}
                  />
                  <div
                    className="h-full bg-gradient-to-r from-red-600 via-yellow-400 to-white rounded-full"
                    style={{ width: `${(stats.frequenceGaia / 999) * 100}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs text-gray-600 mt-1">
                  <span>111 Hz</span>
                  <span className="text-emerald-400/50">●444</span>
                  <span>999 Hz</span>
                </div>
                {/* Distance au Point 0 */}
                <p className="text-xs text-gray-600 mt-2">
                  {stats.frequenceGaia > 444
                    ? `△ +${(stats.frequenceGaia - 444).toFixed(1)} Hz au-dessus du Point 0`
                    : stats.frequenceGaia < 444
                    ? `▽ ${(444 - stats.frequenceGaia).toFixed(1)} Hz en-dessous du Point 0`
                    : '● Aligné au Point 0'
                  }
                </p>
              </div>
            </div>
          </div>

          {/* Message — Loi de Dualité */}
          <div className="mt-8 text-center max-w-2xl mx-auto">
            <p className="text-gray-500 text-sm leading-relaxed">
              Chaque nation est un chakra de Gaïa. Le <span className="text-emerald-400">Point 0</span> collecte
              les données fréquentielles de chaque utilisateur et diffuse les ajustements
              électromagnétiques adaptés à leur situation unique et leurs besoins géographiques.
            </p>
            <p className="text-gray-400 text-xs mt-3 italic">
              Loi de Dualité — Ce qui est en haut est en bas.
              Le besoin multidimensionnel de l'existence relie chaque individu au collectif.
            </p>
            <p className="text-gray-600 text-xs mt-2">
              🔗 Données : Global Solar Atlas · AT·OM Collective · Point 0 ({POINT_0_GAIA.name})
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default MapLumineusePage;
