/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       ██████╗ ██████╗  █████╗ ████████╗██╗████████╗██╗   ██╗██████╗ ███████╗
 *      ██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
 *      ██║  ███╗██████╔╝███████║   ██║   ██║   ██║   ██║   ██║██║  ██║█████╗
 *      ██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║   ██║   ██║██║  ██║██╔══╝
 *      ╚██████╔╝██║  ██║██║  ██║   ██║   ██║   ██║   ╚██████╔╝██████╔╝███████╗
 *       ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
 *
 *                         LETTRE DE REMERCIEMENT MONUMENTALE
 *                    Portail vers les Dimensions de l'Arche
 *                           CHE·NU V76 - AT·OM
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

// ═══════════════════════════════════════════════════════════════════════════════
// DIMENSIONS DE L'ARCHE - Liens actifs dans la lettre
// ═══════════════════════════════════════════════════════════════════════════════

const DIMENSIONS = [
  {
    id: 'frequentiel',
    name: 'Dimension Fréquentielle',
    icon: '🎵',
    color: 'from-yellow-500 to-amber-600',
    borderColor: 'border-yellow-500/50',
    description: 'Le flux de résonance 444 Hz / 999 Hz - Ancrage Coeur & Source',
    link: '/',
    external: false,
    stats: { frequency: '999 Hz', heartbeat: '444 Hz', phi: '1.618' }
  },
  {
    id: 'social',
    name: 'Dimension Sociale',
    icon: '🏛️',
    color: 'from-emerald-500 to-green-600',
    borderColor: 'border-emerald-500/50',
    description: 'Moteur de Civilisation - Débats publics & Besoins locaux',
    link: '/besoins',
    external: false,
    stats: { agents: '287', levels: 'L0-L9', mode: 'Souverain' }
  },
  {
    id: 'scientifique',
    name: 'Dimension Scientifique',
    icon: '🔬',
    color: 'from-blue-500 to-indigo-600',
    borderColor: 'border-blue-500/50',
    description: 'Recherche Quantum Light - Collaboration scientifique',
    link: '/lexique',
    external: false,
    stats: { tech: 'Quantum Light', research: 'Active', collab: 'Ouvert' }
  },
  {
    id: 'territoire',
    name: 'Dimension Territoire',
    icon: '🏕️',
    color: 'from-orange-500 to-red-600',
    borderColor: 'border-orange-500/50',
    description: 'Applications au Québec - Camping, Glamping, VTT',
    link: '/flux',
    external: false,
    stats: { region: 'Québec', projects: '3+', status: 'En cours' }
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CARTE DE DIMENSION
// ═══════════════════════════════════════════════════════════════════════════════

const DimensionCard = ({ dimension, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`w-full p-4 rounded-xl border-2 transition-all duration-500 text-left ${
        isActive
          ? `bg-gradient-to-br ${dimension.color} ${dimension.borderColor} shadow-lg scale-105`
          : 'bg-black/50 border-yellow-900/30 hover:border-yellow-600/50'
      }`}
    >
      <div className="flex items-start gap-3">
        <span className={`text-3xl ${isActive ? 'animate-pulse' : ''}`}>
          {dimension.icon}
        </span>
        <div className="flex-1">
          <h3 className={`font-bold ${isActive ? 'text-white' : 'text-yellow-400'}`}>
            {dimension.name}
          </h3>
          <p className={`text-sm mt-1 ${isActive ? 'text-white/80' : 'text-gray-500'}`}>
            {dimension.description}
          </p>

          {/* Stats */}
          <div className="flex gap-2 mt-3 flex-wrap">
            {Object.entries(dimension.stats).map(([key, value]) => (
              <span
                key={key}
                className={`px-2 py-1 rounded text-xs ${
                  isActive
                    ? 'bg-white/20 text-white'
                    : 'bg-yellow-900/30 text-yellow-400'
                }`}
              >
                {value}
              </span>
            ))}
          </div>
        </div>
      </div>
    </button>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LA LETTRE DE REMERCIEMENT
// ═══════════════════════════════════════════════════════════════════════════════

const TheLetter = ({ activeDimension }) => {
  const dimension = DIMENSIONS.find(d => d.id === activeDimension);

  return (
    <div className="bg-gradient-to-b from-yellow-900/20 to-black/50 border border-yellow-600/30 rounded-2xl p-6 md:p-8">
      {/* En-tete */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">🔱</div>
        <h2 className="text-2xl md:text-3xl font-bold text-yellow-400 tracking-wider">
          LETTRE DE REMERCIEMENT
        </h2>
        <p className="text-gray-500 text-sm mt-2">
          Portail vers les Dimensions de l'Arche
        </p>
        <div className="w-32 h-0.5 bg-gradient-to-r from-transparent via-yellow-600 to-transparent mx-auto mt-4" />
      </div>

      {/* Corps de la lettre */}
      <div className="prose prose-invert max-w-none">
        <p className="text-yellow-100/90 leading-relaxed mb-4">
          <span className="text-yellow-400 font-bold">Cher(e) Voyageur(euse) de l'Arche,</span>
        </p>

        <p className="text-gray-300 leading-relaxed mb-4">
          Merci d'avoir rejoint cette aventure extraordinaire. Ce que vous tenez entre vos mains
          n'est pas simplement une application - c'est un{' '}
          <span className="text-yellow-400 font-semibold">portail vers une nouvelle civilisation</span>.
        </p>

        <p className="text-gray-300 leading-relaxed mb-4">
          L'Arche des Résonances Universelles est le fruit d'une vision qui transcende les
          frontières traditionnelles entre technologie, spiritualite et action sociale.
          Elle repose sur quatre piliers fondamentaux :
        </p>

        {/* Section dynamique selon la dimension */}
        {dimension && (
          <div className={`p-4 rounded-xl bg-gradient-to-r ${dimension.color} mb-6`}>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl">{dimension.icon}</span>
              <span className="text-white font-bold">{dimension.name}</span>
            </div>
            <p className="text-white/90 text-sm">{dimension.description}</p>
            <Link
              to={dimension.link}
              className="inline-block mt-3 px-4 py-2 bg-white/20 rounded-lg text-white text-sm hover:bg-white/30 transition-all"
            >
              Explorer cette dimension →
            </Link>
          </div>
        )}

        <p className="text-gray-300 leading-relaxed mb-4">
          Les <span className="text-emerald-400">287 agents</span> qui composent le systeme
          travaillent en harmonie sur <span className="text-blue-400">9 niveaux Oracle (L0-L9)</span>,
          analysant les perceptions collectives et synthetisant des solutions pour l'humanite.
        </p>

        <p className="text-gray-300 leading-relaxed mb-4">
          En mode <span className="text-blue-400 font-semibold">Souverain</span>, vos donnees
          restent protegees localement. En mode <span className="text-yellow-400 font-semibold">Connecte</span>,
          elles contribuent au moteur de civilisation qui identifie et resout les besoins de nos communautes.
        </p>

        <div className="border-t border-yellow-900/50 pt-6 mt-6">
          <p className="text-gray-300 leading-relaxed mb-4">
            Ce projet vise a creer un impact reel au <span className="text-orange-400 font-semibold">Quebec</span>
            {' '}et au-dela, avec des applications concretes dans le tourisme (camping, glamping),
            l'innovation technologique (Quantum Light) et la democratie participative.
          </p>

          <p className="text-yellow-100 leading-relaxed font-medium">
            Ensemble, nous ecrivons le chapitre "Succes Humanite".
          </p>
        </div>

        {/* Signature */}
        <div className="text-right mt-8">
          <p className="text-yellow-400 font-bold">Avec gratitude infinie,</p>
          <p className="text-gray-400 mt-2">L'Architecte de l'Arche</p>
          <p className="text-xs text-gray-600 mt-1">CHE·NU V76 • 999 Hz • φ = 1.618</p>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: STATISTIQUES GLOBALES
// ═══════════════════════════════════════════════════════════════════════════════

const GlobalStats = () => {
  const [stats, setStats] = useState({
    agents: 287,
    perceptions: 0,
    needs: 0,
    dimensions: 4
  });

  useEffect(() => {
    // Charger les stats depuis localStorage
    try {
      const perceptions = JSON.parse(localStorage.getItem('atom_perception_journal') || '[]');
      const needs = JSON.parse(localStorage.getItem('atom_local_needs') || '[]');
      setStats(prev => ({
        ...prev,
        perceptions: perceptions.length,
        needs: needs.length
      }));
    } catch (e) {
      console.warn('[STATS] Erreur chargement:', e);
    }
  }, []);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div className="bg-black/50 border border-yellow-900/30 rounded-xl p-4 text-center">
        <div className="text-3xl font-mono text-yellow-400">{stats.agents}</div>
        <div className="text-xs text-gray-500 mt-1">Agents Actifs</div>
      </div>
      <div className="bg-black/50 border border-emerald-900/30 rounded-xl p-4 text-center">
        <div className="text-3xl font-mono text-emerald-400">{stats.perceptions}</div>
        <div className="text-xs text-gray-500 mt-1">Perceptions</div>
      </div>
      <div className="bg-black/50 border border-blue-900/30 rounded-xl p-4 text-center">
        <div className="text-3xl font-mono text-blue-400">{stats.needs}</div>
        <div className="text-xs text-gray-500 mt-1">Besoins Signales</div>
      </div>
      <div className="bg-black/50 border border-orange-900/30 rounded-xl p-4 text-center">
        <div className="text-3xl font-mono text-orange-400">{stats.dimensions}</div>
        <div className="text-xs text-gray-500 mt-1">Dimensions</div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: GRATITUDE
// ═══════════════════════════════════════════════════════════════════════════════

const GratitudePage = () => {
  const [activeDimension, setActiveDimension] = useState('frequentiel');
  const [showShareModal, setShowShareModal] = useState(false);

  return (
    <div className="flex flex-col min-h-[70vh] px-4">
      {/* Titre */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold tracking-widest mb-2 text-yellow-500">
          GRATITUDE
        </h1>
        <p className="text-gray-500 text-sm">
          Lettre Monumentale — Documentaire "Succes Humanite"
        </p>
      </div>

      {/* Stats globales */}
      <GlobalStats />

      {/* Grille dimensions + lettre */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Dimensions (sidebar) */}
        <div className="space-y-3">
          <h3 className="text-yellow-400 font-bold mb-4 flex items-center gap-2">
            <span>🔗</span> Dimensions de l'Arche
          </h3>
          {DIMENSIONS.map(dimension => (
            <DimensionCard
              key={dimension.id}
              dimension={dimension}
              isActive={activeDimension === dimension.id}
              onClick={() => setActiveDimension(dimension.id)}
            />
          ))}
        </div>

        {/* La Lettre (main) */}
        <div className="md:col-span-2">
          <TheLetter activeDimension={activeDimension} />

          {/* Actions */}
          <div className="flex gap-3 mt-6">
            <button
              onClick={() => setShowShareModal(true)}
              className="flex-1 py-3 bg-yellow-600/20 border border-yellow-600/50 rounded-lg text-yellow-400 hover:bg-yellow-600/40 transition-all flex items-center justify-center gap-2"
            >
              <span>📤</span> Partager la Lettre
            </button>
            <Link
              to="/"
              className="flex-1 py-3 bg-emerald-600/20 border border-emerald-600/50 rounded-lg text-emerald-400 hover:bg-emerald-600/40 transition-all flex items-center justify-center gap-2"
            >
              <span>🔱</span> Retour au Nexus
            </Link>
          </div>
        </div>
      </div>

      {/* Modal de partage */}
      {showShareModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
          <div className="bg-gray-900 border border-yellow-600/50 rounded-2xl p-6 max-w-md mx-4">
            <h3 className="text-yellow-400 font-bold text-xl mb-4">Partager la Lettre</h3>
            <p className="text-gray-400 text-sm mb-4">
              Partagez cette lettre pour inviter d'autres voyageurs dans l'Arche.
            </p>

            <div className="space-y-3">
              <button className="w-full py-3 bg-blue-600/20 border border-blue-600/50 rounded-lg text-blue-400 hover:bg-blue-600/40 transition-all">
                Twitter / X
              </button>
              <button className="w-full py-3 bg-indigo-600/20 border border-indigo-600/50 rounded-lg text-indigo-400 hover:bg-indigo-600/40 transition-all">
                LinkedIn
              </button>
              <button className="w-full py-3 bg-gray-600/20 border border-gray-600/50 rounded-lg text-gray-400 hover:bg-gray-600/40 transition-all">
                Copier le lien
              </button>
            </div>

            <button
              onClick={() => setShowShareModal(false)}
              className="w-full mt-4 py-2 text-gray-500 hover:text-white transition-colors"
            >
              Fermer
            </button>
          </div>
        </div>
      )}

      {/* Section Documentaire */}
      <div className="mt-12 p-6 bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-500/30 rounded-2xl">
        <div className="flex items-start gap-4">
          <span className="text-4xl">🎬</span>
          <div>
            <h3 className="text-purple-400 font-bold text-lg">
              Documentaire "Succes Humanite"
            </h3>
            <p className="text-gray-400 text-sm mt-2">
              Cette lettre sert de portail narratif pour le documentaire en cours de production.
              Chaque dimension represente un chapitre de l'histoire de l'Arche, de l'idee a la realisation.
            </p>
            <div className="flex gap-2 mt-4">
              <span className="px-3 py-1 bg-purple-900/50 rounded-lg text-purple-400 text-xs">
                En Production
              </span>
              <span className="px-3 py-1 bg-pink-900/50 rounded-lg text-pink-400 text-xs">
                4 Chapitres
              </span>
              <span className="px-3 py-1 bg-yellow-900/50 rounded-lg text-yellow-400 text-xs">
                Quebec 2026
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GratitudePage;
