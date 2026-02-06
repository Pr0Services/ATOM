/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ███████╗██╗     ██╗   ██╗██╗  ██╗
 *      ██╔════╝██║     ██║   ██║╚██╗██╔╝
 *      █████╗  ██║     ██║   ██║ ╚███╔╝ 
 *      ██╔══╝  ██║     ██║   ██║ ██╔██╗ 
 *      ██║     ███████╗╚██████╔╝██╔╝ ██╗
 *      ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
 *                                                                                          
 *                                    🌊 LE FLUX - L'EAU 🌊
 *                                      GRAPHIQUE DE RÉSONANCE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useMemo, useRef, useEffect } from 'react';
import { useATOMContext, PHI } from '../contexts/ATOMContext';
import { useArithmos } from '../hooks/useArithmos';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: GRAPHIQUE DE RÉSONANCE
// ═══════════════════════════════════════════════════════════════════════════════

const ResonanceGraph = ({ entries }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || entries.length === 0) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;
    const centerX = width / 2;
    const centerY = height / 2;

    // Effacer
    ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
    ctx.fillRect(0, 0, width, height);

    // Dessiner les cercles de référence pour chaque Arithmos
    for (let i = 1; i <= 9; i++) {
      const radius = (i / 9) * (Math.min(width, height) / 2 - 20);
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(212, 175, 55, 0.1)`;
      ctx.stroke();
      
      // Label
      ctx.fillStyle = 'rgba(212, 175, 55, 0.3)';
      ctx.font = '10px monospace';
      ctx.fillText(String(i), centerX + radius + 5, centerY);
    }

    // Positions des nœuds (basées sur l'Arithmos et l'ordre)
    const nodes = entries.map((entry, index) => {
      const angle = (index / entries.length) * Math.PI * 2 - Math.PI / 2;
      const radius = (entry.arithmos / 9) * (Math.min(width, height) / 2 - 40);
      
      return {
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        entry,
        angle,
        radius
      };
    });

    // Dessiner les connexions (mêmes Arithmos)
    nodes.forEach((node1, i) => {
      nodes.forEach((node2, j) => {
        if (i < j && node1.entry.arithmos === node2.entry.arithmos) {
          ctx.beginPath();
          ctx.moveTo(node1.x, node1.y);
          ctx.lineTo(node2.x, node2.y);
          ctx.strokeStyle = `rgba(212, 175, 55, 0.2)`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      });
    });

    // Dessiner les nœuds
    nodes.forEach(node => {
      // Cercle
      ctx.beginPath();
      ctx.arc(node.x, node.y, 8, 0, Math.PI * 2);
      
      const hue = node.entry.arithmos * 40;
      ctx.fillStyle = `hsla(${hue}, 70%, 50%, 0.8)`;
      ctx.fill();
      
      // Label
      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.font = '9px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(
        node.entry.word.substring(0, 8),
        node.x,
        node.y + 18
      );
    });

    // Centre
    ctx.beginPath();
    ctx.arc(centerX, centerY, 15, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(212, 175, 55, 0.5)';
    ctx.fill();
    ctx.fillStyle = '#D4AF37';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('∞', centerX, centerY);

  }, [entries]);

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={400}
      className="w-full max-w-md mx-auto rounded-lg border border-yellow-900/30"
      style={{ background: 'rgba(0,0,0,0.5)' }}
    />
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: COMPARAISON
// ═══════════════════════════════════════════════════════════════════════════════

const ComparisonTool = () => {
  const [word1, setWord1] = useState('');
  const [word2, setWord2] = useState('');
  const [result, setResult] = useState(null);
  const { calculateCompatibility } = useArithmos();

  const handleCompare = () => {
    if (word1.trim() && word2.trim()) {
      const comparison = calculateCompatibility(word1, word2);
      setResult(comparison);
    }
  };

  return (
    <div className="bg-black/50 rounded-lg border border-yellow-900/30 p-6">
      <h3 className="text-lg font-bold text-yellow-400 mb-4">🔗 Calculer la Résonance</h3>
      
      <div className="flex gap-4 mb-4">
        <input
          type="text"
          value={word1}
          onChange={(e) => setWord1(e.target.value)}
          placeholder="Premier mot..."
          className="flex-1 px-4 py-2 bg-black border border-yellow-900/50 rounded text-yellow-400 placeholder-yellow-600/50 outline-none"
        />
        <span className="text-yellow-400 self-center">↔</span>
        <input
          type="text"
          value={word2}
          onChange={(e) => setWord2(e.target.value)}
          placeholder="Second mot..."
          className="flex-1 px-4 py-2 bg-black border border-yellow-900/50 rounded text-yellow-400 placeholder-yellow-600/50 outline-none"
        />
      </div>
      
      <button
        onClick={handleCompare}
        disabled={!word1.trim() || !word2.trim()}
        className="w-full py-2 bg-yellow-600/20 border border-yellow-600 rounded text-yellow-400 hover:bg-yellow-600 hover:text-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Comparer
      </button>

      {result && (
        <div className="mt-6 space-y-4">
          {/* Résumé */}
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-3 bg-yellow-900/20 rounded">
              <p className="text-xl font-bold text-yellow-400">{result.word1.arithmos}</p>
              <p className="text-xs text-gray-500">{result.word1.originalInput}</p>
            </div>
            <div className="p-3 bg-yellow-900/20 rounded">
              <p className="text-xl font-bold text-yellow-400">{result.combinedArithmos}</p>
              <p className="text-xs text-gray-500">Combiné</p>
            </div>
            <div className="p-3 bg-yellow-900/20 rounded">
              <p className="text-xl font-bold text-yellow-400">{result.word2.arithmos}</p>
              <p className="text-xs text-gray-500">{result.word2.originalInput}</p>
            </div>
          </div>

          {/* Métriques */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Compatibilité</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-black rounded overflow-hidden">
                  <div 
                    className="h-full bg-yellow-500 transition-all"
                    style={{ width: `${result.compatibility}%` }}
                  />
                </div>
                <span className="text-yellow-400 text-sm">{result.compatibility}%</span>
              </div>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Harmonie Élémentaire</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-black rounded overflow-hidden">
                  <div 
                    className="h-full bg-green-500 transition-all"
                    style={{ width: `${result.elementHarmony}%` }}
                  />
                </div>
                <span className="text-green-400 text-sm">{result.elementHarmony}%</span>
              </div>
            </div>
          </div>

          {/* Résonance */}
          <div className="text-center p-4 bg-yellow-900/10 rounded">
            <p className="text-sm text-gray-500">Niveau de Résonance</p>
            <p className={`text-xl font-bold ${
              result.resonance === 'PARFAITE' ? 'text-green-400' :
              result.resonance === 'FORTE' ? 'text-yellow-400' :
              result.resonance === 'MODÉRÉE' ? 'text-orange-400' : 'text-red-400'
            }`}>
              {result.resonance}
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Fréquence combinée: {result.combinedFrequency} Hz
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: FLUX
// ═══════════════════════════════════════════════════════════════════════════════

const FluxPage = () => {
  const { annales } = useATOMContext();
  const [viewMode, setViewMode] = useState('graph');

  // Grouper par Arithmos
  const groupedByArithmos = useMemo(() => {
    const groups = {};
    annales.forEach(entry => {
      if (!groups[entry.arithmos]) {
        groups[entry.arithmos] = [];
      }
      groups[entry.arithmos].push(entry);
    });
    return groups;
  }, [annales]);

  // Statistiques de flux
  const flowStats = useMemo(() => {
    const connections = {};
    
    annales.forEach((entry1, i) => {
      annales.forEach((entry2, j) => {
        if (i < j && entry1.arithmos === entry2.arithmos) {
          const key = `${entry1.arithmos}`;
          connections[key] = (connections[key] || 0) + 1;
        }
      });
    });

    return connections;
  }, [annales]);

  return (
    <div className="min-h-[70vh] px-4 py-6">
      
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500 tracking-widest mb-2">
          🌊 LE FLUX
        </h1>
        <p className="text-gray-500 text-sm">L'Eau (Ouest) — Graphique de Résonance</p>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-2 mb-8">
        {[
          { id: 'graph', label: 'Graphique', icon: '🌐' },
          { id: 'compare', label: 'Comparer', icon: '🔗' },
          { id: 'groups', label: 'Groupes', icon: '📊' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setViewMode(tab.id)}
            className={`px-4 py-2 rounded-lg transition-all ${
              viewMode === tab.id
                ? 'bg-blue-500 text-white'
                : 'bg-blue-900/20 text-blue-400 hover:bg-blue-900/40'
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* Contenu */}
      
      {/* GRAPHIQUE */}
      {viewMode === 'graph' && (
        <div>
          {annales.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-4xl mb-4">🌐</p>
              <p>Aucune donnée pour le graphique</p>
              <p className="text-sm mt-2">Analysez des mots dans le Nexus</p>
            </div>
          ) : (
            <>
              <ResonanceGraph entries={annales.slice(0, 30)} />
              <p className="text-center text-xs text-gray-500 mt-4">
                Affichage des {Math.min(30, annales.length)} dernières entrées
              </p>
            </>
          )}
        </div>
      )}

      {/* COMPARER */}
      {viewMode === 'compare' && (
        <ComparisonTool />
      )}

      {/* GROUPES */}
      {viewMode === 'groups' && (
        <div className="space-y-4">
          {Object.entries(groupedByArithmos)
            .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
            .map(([arithmos, entries]) => (
              <div key={arithmos} className="bg-black/50 rounded-lg border border-yellow-900/30 p-4">
                <div className="flex justify-between items-center mb-3">
                  <div className="flex items-center gap-3">
                    <div 
                      className="w-10 h-10 rounded-full flex items-center justify-center text-lg font-bold"
                      style={{ 
                        backgroundColor: `hsla(${parseInt(arithmos) * 40}, 70%, 50%, 0.3)`,
                        color: `hsl(${parseInt(arithmos) * 40}, 70%, 50%)`
                      }}
                    >
                      {arithmos}
                    </div>
                    <div>
                      <p className="font-bold text-yellow-400">Arithmos {arithmos}</p>
                      <p className="text-xs text-gray-500">{entries.length} mots</p>
                    </div>
                  </div>
                  <span className="text-sm text-gray-500">{parseInt(arithmos) * 111} Hz</span>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  {entries.slice(0, 10).map((entry, i) => (
                    <span 
                      key={i}
                      className="px-2 py-1 bg-yellow-900/20 rounded text-sm text-yellow-400"
                    >
                      {entry.word}
                    </span>
                  ))}
                  {entries.length > 10 && (
                    <span className="px-2 py-1 text-sm text-gray-500">
                      +{entries.length - 10} autres
                    </span>
                  )}
                </div>
              </div>
            ))}
          
          {Object.keys(groupedByArithmos).length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p className="text-4xl mb-4">📊</p>
              <p>Aucun groupe à afficher</p>
            </div>
          )}
        </div>
      )}

    </div>
  );
};

export default FluxPage;
