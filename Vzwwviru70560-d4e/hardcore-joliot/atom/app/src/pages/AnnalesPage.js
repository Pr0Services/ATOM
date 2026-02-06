/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *       █████╗ ███╗   ██╗███╗   ██╗ █████╗ ██╗     ███████╗███████╗
 *      ██╔══██╗████╗  ██║████╗  ██║██╔══██╗██║     ██╔════╝██╔════╝
 *      ███████║██╔██╗ ██║██╔██╗ ██║███████║██║     █████╗  ███████╗
 *      ██╔══██║██║╚██╗██║██║╚██╗██║██╔══██║██║     ██╔══╝  ╚════██║
 *      ██║  ██║██║ ╚████║██║ ╚████║██║  ██║███████╗███████╗███████║
 *      ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
 *                                                                                          
 *                                    🌍 LES ANNALES - LA TERRE 🌍
 *                                      HISTORIQUE DES MOTS TESTÉS
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useMemo } from 'react';
import { useATOMContext } from '../contexts/ATOMContext';

const AnnalesPage = () => {
  const { annales, setAnnales } = useATOMContext();
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Filtrage et recherche
  const filteredAnnales = useMemo(() => {
    let filtered = annales;

    // Filtre par Arithmos
    if (filter !== 'all') {
      filtered = filtered.filter(entry => entry.arithmos === parseInt(filter));
    }

    // Recherche
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(entry => 
        entry.word.toLowerCase().includes(term)
      );
    }

    return filtered;
  }, [annales, filter, searchTerm]);

  // Statistiques
  const stats = useMemo(() => {
    const arithmosCounts = {};
    const civilizationCounts = {};
    
    annales.forEach(entry => {
      arithmosCounts[entry.arithmos] = (arithmosCounts[entry.arithmos] || 0) + 1;
      if (entry.civilization) {
        civilizationCounts[entry.civilization] = (civilizationCounts[entry.civilization] || 0) + 1;
      }
    });

    const mostCommonArithmos = Object.entries(arithmosCounts)
      .sort((a, b) => b[1] - a[1])[0];

    return {
      total: annales.length,
      arithmosCounts,
      civilizationCounts,
      mostCommonArithmos: mostCommonArithmos ? mostCommonArithmos[0] : null,
      architectCount: annales.filter(e => e.isArchitect).length
    };
  }, [annales]);

  // Effacer l'historique
  const clearAnnales = () => {
    if (window.confirm('Effacer tout l\'historique des Annales ?')) {
      setAnnales([]);
      localStorage.removeItem('atom_annales');
    }
  };

  // Formatage de la date
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-[70vh] px-4 py-6">
      
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500 tracking-widest mb-2">
          🌍 LES ANNALES
        </h1>
        <p className="text-gray-500 text-sm">La Terre (Sud) — Historique des Mots</p>
      </div>

      {/* Statistiques */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-yellow-900/20 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-400">{stats.total}</p>
          <p className="text-xs text-gray-500">Mots analysés</p>
        </div>
        <div className="bg-yellow-900/20 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-400">
            {stats.mostCommonArithmos || '-'}
          </p>
          <p className="text-xs text-gray-500">Arithmos dominant</p>
        </div>
        <div className="bg-yellow-900/20 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-400">{stats.architectCount}</p>
          <p className="text-xs text-gray-500">Sceaux Architecte</p>
        </div>
        <div className="bg-yellow-900/20 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-400">
            {Object.keys(stats.civilizationCounts).length}
          </p>
          <p className="text-xs text-gray-500">Civilisations</p>
        </div>
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-4 mb-6">
        {/* Recherche */}
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Rechercher un mot..."
          className="flex-1 min-w-[200px] px-4 py-2 bg-black border border-yellow-900/50 rounded-lg text-yellow-400 placeholder-yellow-600/50 outline-none focus:border-yellow-500"
        />
        
        {/* Filtre par Arithmos */}
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 bg-black border border-yellow-900/50 rounded-lg text-yellow-400 outline-none focus:border-yellow-500"
        >
          <option value="all">Tous les Arithmos</option>
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
            <option key={n} value={n}>Arithmos {n}</option>
          ))}
        </select>

        {/* Bouton effacer */}
        {annales.length > 0 && (
          <button
            onClick={clearAnnales}
            className="px-4 py-2 bg-red-900/20 border border-red-600/50 rounded-lg text-red-400 hover:bg-red-600 hover:text-white transition-all"
          >
            Effacer
          </button>
        )}
      </div>

      {/* Liste des Annales */}
      {filteredAnnales.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="text-4xl mb-4">📜</p>
          <p>Aucune entrée dans les Annales</p>
          <p className="text-sm mt-2">Retournez au Nexus pour analyser des mots</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredAnnales.map((entry, index) => (
            <div
              key={entry.id || index}
              className={`p-4 rounded-lg border transition-all hover:scale-[1.01] ${
                entry.isArchitect 
                  ? 'bg-white/5 border-white/50' 
                  : 'bg-yellow-900/10 border-yellow-900/30'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className={`text-xl font-bold ${
                      entry.isArchitect ? 'text-white' : 'text-yellow-400'
                    }`}>
                      {entry.word}
                    </span>
                    {entry.isArchitect && (
                      <span className="text-xs bg-white/20 px-2 py-1 rounded text-white">
                        ★ ARCHITECTE
                      </span>
                    )}
                  </div>
                  
                  <div className="flex flex-wrap gap-4 mt-2 text-sm text-gray-400">
                    <span>
                      Arithmos: <span className="text-yellow-400">{entry.arithmos}</span>
                    </span>
                    <span>
                      {entry.frequency} Hz
                    </span>
                    {entry.essence && (
                      <span className="text-gray-500">{entry.essence}</span>
                    )}
                    {entry.civilization && (
                      <span className="text-gray-500">{entry.civilization}</span>
                    )}
                  </div>
                </div>
                
                <div className="text-right text-xs text-gray-600">
                  {formatDate(entry.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Distribution des Arithmos */}
      {annales.length > 0 && (
        <div className="mt-8 p-6 bg-yellow-900/10 rounded-lg">
          <h3 className="text-lg font-bold text-yellow-400 mb-4">Distribution des Arithmos</h3>
          <div className="flex gap-2 flex-wrap">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => {
              const count = stats.arithmosCounts[n] || 0;
              const percentage = stats.total > 0 ? (count / stats.total) * 100 : 0;
              
              return (
                <div key={n} className="flex-1 min-w-[60px]">
                  <div className="text-center mb-1">
                    <span className="text-yellow-400 font-bold">{n}</span>
                  </div>
                  <div className="h-20 bg-black/50 rounded relative overflow-hidden">
                    <div 
                      className="absolute bottom-0 left-0 right-0 bg-yellow-500/50 transition-all"
                      style={{ height: `${percentage}%` }}
                    />
                  </div>
                  <div className="text-center mt-1 text-xs text-gray-500">
                    {count}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
};

export default AnnalesPage;
