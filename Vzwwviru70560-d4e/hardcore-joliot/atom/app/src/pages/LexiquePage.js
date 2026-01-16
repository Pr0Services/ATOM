/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ██╗     ███████╗██╗  ██╗██╗ ██████╗ ██╗   ██╗███████╗
 *      ██║     ██╔════╝╚██╗██╔╝██║██╔═══██╗██║   ██║██╔════╝
 *      ██║     █████╗   ╚███╔╝ ██║██║   ██║██║   ██║█████╗  
 *      ██║     ██╔══╝   ██╔██╗ ██║██║▄▄ ██║██║   ██║██╔══╝  
 *      ███████╗███████╗██╔╝ ██╗██║╚██████╔╝╚██████╔╝███████╗
 *      ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝
 *                                                                                          
 *                                    💨 LE LEXIQUE - L'AIR 💨
 *                                      ORACLES ET FRÉQUENCES
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState } from 'react';
import { useArithmos } from '../hooks/useArithmos';

const LexiquePage = () => {
  const { getAllArithmos } = useArithmos();
  const [selectedArithmos, setSelectedArithmos] = useState(null);
  const [activeTab, setActiveTab] = useState('arithmos');

  const arithmosData = getAllArithmos();

  // Les 18 Oracles
  const oracles = [
    { id: 1, name: "Oracle de l'Origine", arithmos: 1, domain: "Commencements, Leadership", symbol: "☀️" },
    { id: 2, name: "Oracle de l'Équilibre", arithmos: 2, domain: "Partenariats, Diplomatie", symbol: "☯" },
    { id: 3, name: "Oracle de la Création", arithmos: 3, domain: "Expression, Joie", symbol: "△" },
    { id: 4, name: "Oracle de la Structure", arithmos: 4, domain: "Fondation, Discipline", symbol: "□" },
    { id: 5, name: "Oracle du Changement", arithmos: 5, domain: "Liberté, Aventure", symbol: "☿" },
    { id: 6, name: "Oracle de l'Harmonie", arithmos: 6, domain: "Amour, Famille", symbol: "✡" },
    { id: 7, name: "Oracle de la Sagesse", arithmos: 7, domain: "Spiritualité, Mystère", symbol: "🌙" },
    { id: 8, name: "Oracle de l'Abondance", arithmos: 8, domain: "Pouvoir, Succès", symbol: "∞" },
    { id: 9, name: "Oracle de la Source", arithmos: 9, domain: "Achèvement, Transcendance", symbol: "⊕" },
    { id: 10, name: "Oracle du Feu", element: "Feu", domain: "Transformation, Énergie", symbol: "🔥" },
    { id: 11, name: "Oracle de l'Eau", element: "Eau", domain: "Émotions, Intuition", symbol: "🌊" },
    { id: 12, name: "Oracle de l'Air", element: "Air", domain: "Pensée, Communication", symbol: "💨" },
    { id: 13, name: "Oracle de la Terre", element: "Terre", domain: "Stabilité, Matière", symbol: "🌍" },
    { id: 14, name: "Oracle de l'Éther", element: "Éther", domain: "Connexion, Conscience", symbol: "✨" },
    { id: 15, name: "Oracle du Temps", domain: "Cycles, Patience", symbol: "⏳" },
    { id: 16, name: "Oracle de l'Espace", domain: "Expansion, Possibilités", symbol: "🌌" },
    { id: 17, name: "Oracle de l'Architecte", domain: "Vision, Création", symbol: "🔱", special: true },
    { id: 18, name: "Oracle du Silence", domain: "Méditation, Paix", symbol: "☯" }
  ];

  // Fréquences Solfège
  const solfeggioFrequencies = [
    { note: "UT", hz: 396, intention: "Libération de la peur et de la culpabilité", chakra: "Racine" },
    { note: "RE", hz: 417, intention: "Facilitation du changement", chakra: "Sacré" },
    { note: "MI", hz: 528, intention: "Transformation et miracles (Réparation ADN)", chakra: "Plexus" },
    { note: "FA", hz: 639, intention: "Connexion et relations", chakra: "Cœur" },
    { note: "SOL", hz: 741, intention: "Éveil de l'intuition", chakra: "Gorge" },
    { note: "LA", hz: 852, intention: "Retour à l'ordre spirituel", chakra: "3ème œil" },
    { note: "SI", hz: 963, intention: "Connexion à la lumière", chakra: "Couronne" }
  ];

  // Fréquences AT·OM
  const atomFrequencies = [
    { name: "ANCHOR", hz: 111, description: "Ancrage, Racine, Stabilité" },
    { name: "DUALITY", hz: 222, description: "Dualité, Miroir, Partenariat" },
    { name: "CREATION", hz: 333, description: "Création, Mental, Géométrie" },
    { name: "HEART", hz: 444, description: "Cœur, Structure, Amour", special: true },
    { name: "CHANGE", hz: 555, description: "Changement, Mouvement, Liberté" },
    { name: "HARMONY", hz: 666, description: "Harmonie, Équilibre, Protection" },
    { name: "SPIRIT", hz: 777, description: "Esprit, Spiritualité, Sagesse" },
    { name: "INFINITY", hz: 888, description: "Infini, Abondance, Pouvoir" },
    { name: "SOURCE", hz: 999, description: "Source, Unité, Transcendance", special: true }
  ];

  return (
    <div className="min-h-[70vh] px-4 py-6">
      
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500 tracking-widest mb-2">
          💨 LE LEXIQUE
        </h1>
        <p className="text-gray-500 text-sm">L'Air (Est) — Oracles et Fréquences</p>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-2 mb-8">
        {[
          { id: 'arithmos', label: 'Arithmos', icon: '🔢' },
          { id: 'oracles', label: 'Oracles', icon: '🔮' },
          { id: 'frequencies', label: 'Fréquences', icon: '〰️' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-yellow-500 text-black'
                : 'bg-yellow-900/20 text-yellow-400 hover:bg-yellow-900/40'
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* Contenu selon l'onglet */}
      
      {/* ARITHMOS */}
      {activeTab === 'arithmos' && (
        <div className="grid md:grid-cols-3 gap-4">
          {Object.entries(arithmosData).map(([num, data]) => (
            <div
              key={num}
              onClick={() => setSelectedArithmos(selectedArithmos === num ? null : num)}
              className={`p-4 rounded-lg border cursor-pointer transition-all hover:scale-[1.02] ${
                selectedArithmos === num
                  ? 'bg-yellow-500/20 border-yellow-500'
                  : 'bg-black/50 border-yellow-900/30 hover:border-yellow-600'
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <div 
                  className="w-12 h-12 rounded-full flex items-center justify-center text-2xl font-bold"
                  style={{ 
                    backgroundColor: data.color + '30',
                    color: data.color
                  }}
                >
                  {num}
                </div>
                <span className="text-sm text-gray-500">{data.frequency} Hz</span>
              </div>
              
              <h3 className="text-lg font-bold text-yellow-400">{data.name}</h3>
              <p className="text-sm text-gray-400">{data.essence}</p>
              
              {selectedArithmos === num && (
                <div className="mt-4 pt-4 border-t border-yellow-900/30 space-y-2 text-sm">
                  <p><span className="text-gray-500">Principe:</span> <span className="text-yellow-400">{data.principle}</span></p>
                  <p><span className="text-gray-500">Élément:</span> <span className="text-yellow-400">{data.element}</span></p>
                  <p><span className="text-gray-500">Planète:</span> <span className="text-yellow-400">{data.planet}</span></p>
                  <p><span className="text-gray-500">Civilisation:</span> <span className="text-yellow-400">{data.civilization}</span></p>
                  <p className="text-gray-500 italic mt-2">"{data.description}"</p>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {data.keywords.map((kw, i) => (
                      <span key={i} className="px-2 py-1 bg-yellow-900/30 rounded text-xs text-yellow-400">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ORACLES */}
      {activeTab === 'oracles' && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {oracles.map(oracle => (
            <div
              key={oracle.id}
              className={`p-4 rounded-lg border transition-all hover:scale-[1.02] ${
                oracle.special
                  ? 'bg-white/5 border-white/50'
                  : 'bg-black/50 border-yellow-900/30 hover:border-yellow-600'
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{oracle.symbol}</span>
                <div>
                  <h3 className={`font-bold ${oracle.special ? 'text-white' : 'text-yellow-400'}`}>
                    {oracle.name}
                  </h3>
                  <p className="text-xs text-gray-500">Oracle #{oracle.id}</p>
                </div>
              </div>
              
              <p className="text-sm text-gray-400">{oracle.domain}</p>
              
              {oracle.arithmos && (
                <p className="text-xs text-gray-500 mt-2">
                  Arithmos associé: <span className="text-yellow-400">{oracle.arithmos}</span>
                </p>
              )}
              {oracle.element && (
                <p className="text-xs text-gray-500 mt-2">
                  Élément: <span className="text-yellow-400">{oracle.element}</span>
                </p>
              )}
              
              {oracle.special && (
                <div className="mt-2 text-xs text-white/70">
                  ★ Oracle Spécial
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* FRÉQUENCES */}
      {activeTab === 'frequencies' && (
        <div className="space-y-8">
          
          {/* Fréquences AT·OM */}
          <div>
            <h2 className="text-xl font-bold text-yellow-400 mb-4">Fréquences AT·OM</h2>
            <div className="grid md:grid-cols-3 gap-4">
              {atomFrequencies.map(freq => (
                <div
                  key={freq.hz}
                  className={`p-4 rounded-lg border ${
                    freq.special
                      ? 'bg-yellow-500/20 border-yellow-500'
                      : 'bg-black/50 border-yellow-900/30'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <h3 className="font-bold text-yellow-400">{freq.name}</h3>
                    <span className={`text-xl font-mono ${freq.special ? 'text-yellow-300' : 'text-yellow-500'}`}>
                      {freq.hz} Hz
                    </span>
                  </div>
                  <p className="text-sm text-gray-400 mt-2">{freq.description}</p>
                  {freq.special && (
                    <span className="inline-block mt-2 text-xs bg-yellow-500/30 px-2 py-1 rounded text-yellow-300">
                      Fréquence Clé
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Fréquences Solfège */}
          <div>
            <h2 className="text-xl font-bold text-yellow-400 mb-4">Solfège Sacré</h2>
            <div className="space-y-3">
              {solfeggioFrequencies.map(freq => (
                <div
                  key={freq.hz}
                  className="p-4 rounded-lg bg-black/50 border border-yellow-900/30 flex items-center gap-4"
                >
                  <div className="w-16 h-16 rounded-full bg-yellow-900/30 flex items-center justify-center">
                    <span className="text-xl font-bold text-yellow-400">{freq.note}</span>
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <span className="font-mono text-yellow-500">{freq.hz} Hz</span>
                      <span className="text-xs text-gray-500">Chakra: {freq.chakra}</span>
                    </div>
                    <p className="text-sm text-gray-400 mt-1">{freq.intention}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};

export default LexiquePage;
