/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗ ███████╗███████╗ ██████╗ ██╗███╗   ██╗███████╗
 *      ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║████╗  ██║██╔════╝
 *      ██████╔╝█████╗  ███████╗██║   ██║██║██╔██╗ ██║███████╗
 *      ██╔══██╗██╔══╝  ╚════██║██║   ██║██║██║╚██╗██║╚════██║
 *      ██████╔╝███████╗███████║╚██████╔╝██║██║ ╚████║███████║
 *      ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝
 *
 *                    MOTEUR DE BESOINS LOCAUX
 *              Plateforme de Signalement & Priorisation
 *                    Fonction de Civilisation
 *                        CHE·NU V76 - AT·OM
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { submitNeed, getLocalNeeds, voteForNeed } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CATÉGORIES DE BESOINS
// ═══════════════════════════════════════════════════════════════════════════════

const CATEGORIES = [
  { id: 'sante', name: 'Santé', icon: '🏥', color: 'text-red-400 bg-red-900/30 border-red-500/50' },
  { id: 'education', name: 'Éducation', icon: '📚', color: 'text-blue-400 bg-blue-900/30 border-blue-500/50' },
  { id: 'environnement', name: 'Environnement', icon: '🌿', color: 'text-green-400 bg-green-900/30 border-green-500/50' },
  { id: 'economie', name: 'Économie', icon: '💼', color: 'text-yellow-400 bg-yellow-900/30 border-yellow-500/50' },
  { id: 'logement', name: 'Logement', icon: '🏠', color: 'text-orange-400 bg-orange-900/30 border-orange-500/50' },
  { id: 'transport', name: 'Transport', icon: '🚌', color: 'text-purple-400 bg-purple-900/30 border-purple-500/50' },
  { id: 'securite', name: 'Sécurité', icon: '🛡️', color: 'text-gray-400 bg-gray-900/30 border-gray-500/50' },
  { id: 'culture', name: 'Culture', icon: '🎭', color: 'text-pink-400 bg-pink-900/30 border-pink-500/50' }
];

const PRIORITIES = [
  { id: 'urgent', name: 'Urgent', color: 'text-red-500' },
  { id: 'high', name: 'Élevé', color: 'text-orange-400' },
  { id: 'medium', name: 'Moyen', color: 'text-yellow-400' },
  { id: 'low', name: 'Faible', color: 'text-gray-400' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CARTE DE BESOIN
// ═══════════════════════════════════════════════════════════════════════════════

const NeedCard = ({ need, onVote }) => {
  const category = CATEGORIES.find(c => c.id === need.category) || CATEGORIES[0];
  const priority = PRIORITIES.find(p => p.id === need.priority) || PRIORITIES[2];

  return (
    <div className="bg-black/50 border border-yellow-900/30 rounded-xl p-4 hover:border-yellow-600/50 transition-all">
      {/* En-tête */}
      <div className="flex items-start justify-between mb-3">
        <div className={`px-2 py-1 rounded-lg border text-xs ${category.color}`}>
          {category.icon} {category.name}
        </div>
        <span className={`text-xs ${priority.color}`}>
          ● {priority.name}
        </span>
      </div>

      {/* Titre */}
      <h3 className="text-yellow-400 font-bold mb-2">{need.title}</h3>

      {/* Description */}
      <p className="text-gray-400 text-sm mb-4 line-clamp-3">{need.description}</p>

      {/* Localisation */}
      <div className="flex items-center gap-2 text-xs text-gray-500 mb-4">
        <span>📍</span>
        <span>{need.location || 'Québec'}</span>
      </div>

      {/* Pied de carte */}
      <div className="flex items-center justify-between pt-3 border-t border-yellow-900/30">
        {/* Votes */}
        <button
          onClick={() => onVote(need.id)}
          className="flex items-center gap-2 px-3 py-1 bg-yellow-600/20 border border-yellow-600/50 rounded-lg hover:bg-yellow-600/40 transition-all"
        >
          <span>👍</span>
          <span className="text-yellow-400 font-mono">{need.votes || 0}</span>
        </button>

        {/* Date */}
        <span className="text-xs text-gray-600">
          {new Date(need.created_at).toLocaleDateString('fr-FR')}
        </span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FORMULAIRE DE SOUMISSION
// ═══════════════════════════════════════════════════════════════════════════════

const SubmitNeedForm = ({ onSubmit, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('sante');
  const [priority, setPriority] = useState('medium');
  const [location, setLocation] = useState('Québec');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) return;

    setLoading(true);
    await onSubmit({ title, description, category, priority, location });
    setLoading(false);
  };

  return (
    <div className="bg-black/70 border border-yellow-600/50 rounded-xl p-6 mb-6">
      <h3 className="text-yellow-400 font-bold text-lg mb-4 flex items-center gap-2">
        <span>📝</span>
        Soumettre un Besoin Local
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Titre */}
        <div>
          <label className="block text-gray-400 text-sm mb-2">Titre du besoin</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Ex: Amélioration de l'accès aux soins..."
            className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none focus:border-yellow-500"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-gray-400 text-sm mb-2">Description détaillée</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Décrivez le besoin, son contexte et son impact..."
            className="w-full h-24 px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 resize-none focus:outline-none focus:border-yellow-500"
            required
          />
        </div>

        {/* Catégorie & Priorité */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-400 text-sm mb-2">Catégorie</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 focus:outline-none focus:border-yellow-500"
            >
              {CATEGORIES.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.icon} {cat.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-2">Priorité</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 focus:outline-none focus:border-yellow-500"
            >
              {PRIORITIES.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Localisation */}
        <div>
          <label className="block text-gray-400 text-sm mb-2">Localisation</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Ville, région..."
            className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none focus:border-yellow-500"
          />
        </div>

        {/* Boutons */}
        <div className="flex gap-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 py-3 bg-gradient-to-r from-yellow-600 to-yellow-500 text-black font-bold rounded-lg hover:from-yellow-500 hover:to-yellow-400 transition-all disabled:opacity-50"
          >
            {loading ? 'Soumission...' : 'Soumettre le Besoin'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 bg-gray-800 text-gray-400 rounded-lg hover:bg-gray-700 transition-all"
          >
            Annuler
          </button>
        </div>
      </form>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: BESOINS LOCAUX
// ═══════════════════════════════════════════════════════════════════════════════

const BesoinsPage = () => {
  const { isAuthenticated, user } = useAuth();
  const [needs, setNeeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [localNeeds, setLocalNeeds] = useState([]); // Pour mode hors-ligne

  // Charger les besoins
  useEffect(() => {
    const loadNeeds = async () => {
      setLoading(true);
      const result = await getLocalNeeds({ category: selectedCategory });

      if (result.success) {
        setNeeds(result.data || []);
      } else {
        // Fallback localStorage pour mode hors-ligne
        try {
          const stored = localStorage.getItem('atom_local_needs');
          if (stored) setLocalNeeds(JSON.parse(stored));
        } catch (e) {
          console.warn('[BESOINS] Erreur localStorage:', e);
        }
      }
      setLoading(false);
    };

    loadNeeds();
  }, [selectedCategory]);

  // Soumettre un besoin
  const handleSubmit = useCallback(async (need) => {
    if (isAuthenticated) {
      const result = await submitNeed(need);
      if (result.success) {
        setNeeds(prev => [result.data[0], ...prev]);
        setShowForm(false);
      }
    } else {
      // Mode hors-ligne: localStorage
      const newNeed = {
        ...need,
        id: Date.now(),
        votes: 0,
        created_at: new Date().toISOString()
      };
      const updated = [newNeed, ...localNeeds];
      setLocalNeeds(updated);
      localStorage.setItem('atom_local_needs', JSON.stringify(updated));
      setShowForm(false);
    }
  }, [isAuthenticated, localNeeds]);

  // Voter pour un besoin
  const handleVote = useCallback(async (needId) => {
    if (isAuthenticated) {
      await voteForNeed(needId);
      setNeeds(prev => prev.map(n =>
        n.id === needId ? { ...n, votes: (n.votes || 0) + 1 } : n
      ));
    } else {
      // Mode hors-ligne
      setLocalNeeds(prev => prev.map(n =>
        n.id === needId ? { ...n, votes: (n.votes || 0) + 1 } : n
      ));
    }
  }, [isAuthenticated]);

  // Liste à afficher
  const displayNeeds = isAuthenticated ? needs : localNeeds;

  return (
    <div className="flex flex-col min-h-[70vh] px-4">
      {/* Titre */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold tracking-widest mb-2 text-yellow-500">
          📊 BESOINS LOCAUX
        </h1>
        <p className="text-gray-500 text-sm">Moteur de Civilisation — Signalement & Priorisation</p>
      </div>

      {/* Bouton d'ajout */}
      {!showForm && (
        <button
          onClick={() => setShowForm(true)}
          className="w-full py-4 mb-6 bg-yellow-600/20 border border-yellow-600/50 rounded-xl text-yellow-400 hover:bg-yellow-600/40 transition-all flex items-center justify-center gap-2"
        >
          <span className="text-xl">➕</span>
          <span>Signaler un Besoin</span>
        </button>
      )}

      {/* Formulaire */}
      {showForm && (
        <SubmitNeedForm
          onSubmit={handleSubmit}
          onCancel={() => setShowForm(false)}
        />
      )}

      {/* Filtres par catégorie */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedCategory(null)}
          className={`px-3 py-1 rounded-lg text-sm transition-all ${
            selectedCategory === null
              ? 'bg-yellow-600 text-black'
              : 'bg-yellow-900/20 text-yellow-400 hover:bg-yellow-900/40'
          }`}
        >
          Tous
        </button>
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`px-3 py-1 rounded-lg text-sm transition-all ${
              selectedCategory === cat.id
                ? 'bg-yellow-600 text-black'
                : 'bg-yellow-900/20 text-yellow-400 hover:bg-yellow-900/40'
            }`}
          >
            {cat.icon} {cat.name}
          </button>
        ))}
      </div>

      {/* Indicateur mode hors-ligne */}
      {!isAuthenticated && (
        <div className="mb-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg text-blue-400 text-sm text-center">
          Mode Souverain — Données stockées localement. Connectez-vous pour synchroniser.
        </div>
      )}

      {/* Liste des besoins */}
      {loading ? (
        <div className="text-center py-12 text-gray-500">
          <div className="animate-spin text-4xl mb-4">🔱</div>
          Chargement des besoins...
        </div>
      ) : displayNeeds.length > 0 ? (
        <div className="grid gap-4">
          {displayNeeds.map(need => (
            <NeedCard key={need.id} need={need} onVote={handleVote} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          <div className="text-4xl mb-4">📭</div>
          Aucun besoin signalé pour le moment.
          <br />
          Soyez le premier à contribuer !
        </div>
      )}

      {/* Statistiques */}
      <div className="mt-8 p-4 bg-black/50 border border-yellow-900/30 rounded-xl">
        <h4 className="text-yellow-400 font-bold mb-3">Statistiques de Civilisation</h4>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-mono text-yellow-400">{displayNeeds.length}</div>
            <div className="text-xs text-gray-500">Besoins signalés</div>
          </div>
          <div>
            <div className="text-2xl font-mono text-emerald-400">
              {displayNeeds.reduce((acc, n) => acc + (n.votes || 0), 0)}
            </div>
            <div className="text-xs text-gray-500">Votes totaux</div>
          </div>
          <div>
            <div className="text-2xl font-mono text-blue-400">
              {new Set(displayNeeds.map(n => n.category)).size}
            </div>
            <div className="text-xs text-gray-500">Catégories actives</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BesoinsPage;
