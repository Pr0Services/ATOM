/* ═══════════════════════════════════════════════════════════════════════════════
 *
 *        ██████╗███████╗██████╗  ██████╗██╗     ███████╗
 *       ██╔════╝██╔════╝██╔══██╗██╔════╝██║     ██╔════╝
 *       ██║     █████╗  ██████╔╝██║     ██║     █████╗
 *       ██║     ██╔══╝  ██╔══██╗██║     ██║     ██╔══╝
 *       ╚██████╗███████╗██║  ██║╚██████╗███████╗███████╗
 *        ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝
 *
 *                 CERCLE DES FONDATEURS - AT.OM / CHE.NU V76
 *            Points de Lumiere Internationaux - Espace Communautaire
 *
 * ═══════════════════════════════════════════════════════════════════════════════ */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const FOUNDER_TYPES = {
  lumiere: { name: 'Point de Lumiere', icon: '🌟', color: '#FFD700' },
  gardien: { name: 'Gardien', icon: '🛡️', color: '#4A90D9' },
  architecte: { name: 'Architecte', icon: '🏛️', color: '#9B59B6' },
  tisserand: { name: 'Tisserand', icon: '🕸️', color: '#2ECC71' },
  porteur: { name: 'Porteur', icon: '🔥', color: '#E74C3C' }
};

const MESSAGE_TYPES = {
  sharing: { name: 'Partage', icon: '💬', color: '#6B7280' },
  gratitude: { name: 'Gratitude', icon: '🙏', color: '#F59E0B' },
  intention: { name: 'Intention', icon: '🎯', color: '#8B5CF6' },
  celebration: { name: 'Celebration', icon: '🎉', color: '#EC4899' },
  support: { name: 'Soutien', icon: '🤝', color: '#10B981' },
  announcement: { name: 'Annonce', icon: '📢', color: '#EF4444' }
};

const ELEMENTS = {
  feu: '🔥', eau: '💧', terre: '🌍', air: '💨', ether: '✨'
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: CERCLE DES FONDATEURS
// ═══════════════════════════════════════════════════════════════════════════════

const CerclePage = () => {
  const { user } = useAuth();

  // Etats
  const [view, setView] = useState('members'); // members | messages | profile
  const [founders, setFounders] = useState([]);
  const [messages, setMessages] = useState([]);
  const [myProfile, setMyProfile] = useState(null);
  const [selectedFounder, setSelectedFounder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isFounder, setIsFounder] = useState(false);

  // Message input
  const [newMessage, setNewMessage] = useState('');
  const [messageType, setMessageType] = useState('sharing');

  // ═══════════════════════════════════════════════════════════════════════════════
  // CHARGEMENT DES DONNEES
  // ═══════════════════════════════════════════════════════════════════════════════

  const loadData = useCallback(async () => {
    if (!user) return;

    setLoading(true);
    try {
      // Verifier si l'utilisateur est fondateur
      const { data: founderData, error: founderError } = await supabase
        .from('founders')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (founderError && founderError.code !== 'PGRST116') {
        console.error('Erreur verification fondateur:', founderError);
      }

      if (founderData) {
        setIsFounder(true);
        setMyProfile(founderData);

        // Charger tous les fondateurs avec leurs profils
        const { data: allFounders, error: foundersError } = await supabase
          .from('founders')
          .select(`
            *,
            profiles:user_id (
              display_name,
              avatar_url
            )
          `)
          .eq('is_active', true)
          .order('founder_number', { ascending: true });

        if (foundersError) throw foundersError;
        setFounders(allFounders || []);

        // Charger les messages
        const { data: messagesData, error: messagesError } = await supabase
          .from('founder_messages')
          .select(`
            *,
            author:author_id (
              display_name,
              avatar_url
            ),
            founder:author_id (
              founder_type,
              founder_number
            )
          `)
          .order('created_at', { ascending: false })
          .limit(50);

        if (messagesError) throw messagesError;
        setMessages(messagesData || []);
      }
    } catch (err) {
      console.error('Erreur chargement donnees:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // ENVOI DE MESSAGE
  // ═══════════════════════════════════════════════════════════════════════════════

  const sendMessage = async () => {
    if (!newMessage.trim() || !user) return;

    try {
      const { data, error } = await supabase
        .from('founder_messages')
        .insert({
          author_id: user.id,
          content: newMessage.trim(),
          message_type: messageType
        })
        .select(`
          *,
          author:author_id (
            display_name,
            avatar_url
          )
        `)
        .single();

      if (error) throw error;

      setMessages(prev => [data, ...prev]);
      setNewMessage('');
    } catch (err) {
      console.error('Erreur envoi message:', err);
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: NON FONDATEUR
  // ═══════════════════════════════════════════════════════════════════════════════

  if (!loading && !isFounder) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="max-w-md w-full text-center">
          <div className="text-6xl mb-6">🔒</div>
          <h1 className="text-2xl font-bold text-white mb-4">
            Cercle des Fondateurs
          </h1>
          <p className="text-gray-400 mb-8">
            Cet espace est reserve aux membres fondateurs.
            Si tu as recu une invitation, utilise ton code pour rejoindre le cercle.
          </p>
          <a
            href="/invitation"
            className="inline-block px-6 py-3 bg-yellow-600 text-black font-bold
              rounded-lg hover:bg-yellow-500 transition-colors"
          >
            J'ai un Code d'Invitation
          </a>
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: CHARGEMENT
  // ═══════════════════════════════════════════════════════════════════════════════

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl animate-pulse mb-4">🌟</div>
          <p className="text-gray-400">Chargement du Cercle...</p>
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU PRINCIPAL
  // ═══════════════════════════════════════════════════════════════════════════════

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="bg-gradient-to-b from-gray-900 to-black border-b border-yellow-600/30">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <span className="text-3xl">🌟</span>
                Cercle des Fondateurs
              </h1>
              <p className="text-gray-400 mt-1">
                {founders.length} membres fondateurs
              </p>
            </div>

            {/* Mon profil rapide */}
            {myProfile && (
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="text-white font-medium">
                    Fondateur #{myProfile.founder_number}
                  </div>
                  <div className="text-sm" style={{ color: FOUNDER_TYPES[myProfile.founder_type]?.color }}>
                    {FOUNDER_TYPES[myProfile.founder_type]?.icon} {FOUNDER_TYPES[myProfile.founder_type]?.name}
                  </div>
                </div>
                <div className="w-12 h-12 rounded-full bg-yellow-600/20 flex items-center justify-center text-2xl">
                  {FOUNDER_TYPES[myProfile.founder_type]?.icon || '🌟'}
                </div>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="flex gap-2 mt-6">
            <button
              onClick={() => setView('members')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                view === 'members'
                  ? 'bg-yellow-600 text-black'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              👥 Membres
            </button>
            <button
              onClick={() => setView('messages')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                view === 'messages'
                  ? 'bg-yellow-600 text-black'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              💬 Cercle de Parole
            </button>
            <button
              onClick={() => setView('profile')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                view === 'profile'
                  ? 'bg-yellow-600 text-black'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              ⚙️ Mon Profil
            </button>
          </div>
        </div>
      </header>

      {/* Contenu principal */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* VUE: MEMBRES */}
        {view === 'members' && (
          <div>
            {/* Grille des membres */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {founders.map(founder => {
                const type = FOUNDER_TYPES[founder.founder_type] || FOUNDER_TYPES.lumiere;
                const displayName = founder.profiles?.display_name || `Fondateur #${founder.founder_number}`;

                return (
                  <div
                    key={founder.id}
                    onClick={() => setSelectedFounder(founder)}
                    className="bg-gradient-to-b from-gray-900 to-black border border-gray-800
                      rounded-xl p-6 cursor-pointer hover:border-yellow-600/50 transition-all"
                  >
                    {/* Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-12 h-12 rounded-full flex items-center justify-center text-2xl"
                          style={{ backgroundColor: `${type.color}20` }}
                        >
                          {type.icon}
                        </div>
                        <div>
                          <div className="text-white font-medium">{displayName}</div>
                          <div className="text-sm" style={{ color: type.color }}>
                            {type.name} #{founder.founder_number}
                          </div>
                        </div>
                      </div>
                      {founder.element && (
                        <span className="text-xl">{ELEMENTS[founder.element]}</span>
                      )}
                    </div>

                    {/* Localisation */}
                    {(founder.location_country || founder.location_city) && (
                      <div className="text-gray-500 text-sm mb-3">
                        📍 {[founder.location_city, founder.location_country].filter(Boolean).join(', ')}
                      </div>
                    )}

                    {/* Intention */}
                    {founder.intention && (
                      <p className="text-gray-400 text-sm line-clamp-2 mb-3">
                        "{founder.intention}"
                      </p>
                    )}

                    {/* Dons */}
                    {founder.gifts && founder.gifts.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {founder.gifts.slice(0, 3).map((gift, i) => (
                          <span
                            key={i}
                            className="px-2 py-0.5 bg-yellow-600/10 text-yellow-500 rounded text-xs"
                          >
                            {gift}
                          </span>
                        ))}
                        {founder.gifts.length > 3 && (
                          <span className="text-gray-500 text-xs">
                            +{founder.gifts.length - 3}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Modal detail fondateur */}
            {selectedFounder && (
              <div
                className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80"
                onClick={() => setSelectedFounder(null)}
              >
                <div
                  className="bg-gray-900 border border-yellow-600/30 rounded-2xl p-6 max-w-lg w-full max-h-[90vh] overflow-y-auto"
                  onClick={e => e.stopPropagation()}
                >
                  {(() => {
                    const f = selectedFounder;
                    const type = FOUNDER_TYPES[f.founder_type] || FOUNDER_TYPES.lumiere;
                    const displayName = f.profiles?.display_name || `Fondateur #${f.founder_number}`;

                    return (
                      <>
                        {/* Header */}
                        <div className="flex items-center gap-4 mb-6">
                          <div
                            className="w-16 h-16 rounded-full flex items-center justify-center text-4xl"
                            style={{ backgroundColor: `${type.color}20` }}
                          >
                            {type.icon}
                          </div>
                          <div>
                            <h2 className="text-xl font-bold text-white">{displayName}</h2>
                            <p style={{ color: type.color }}>
                              {type.name} #{f.founder_number}
                            </p>
                          </div>
                          <button
                            onClick={() => setSelectedFounder(null)}
                            className="ml-auto text-gray-500 hover:text-white text-2xl"
                          >
                            x
                          </button>
                        </div>

                        {/* Infos */}
                        <div className="space-y-4">
                          {(f.location_country || f.location_city) && (
                            <div>
                              <div className="text-gray-500 text-sm mb-1">Localisation</div>
                              <div className="text-white">
                                📍 {[f.location_city, f.location_country].filter(Boolean).join(', ')}
                              </div>
                            </div>
                          )}

                          {f.element && (
                            <div>
                              <div className="text-gray-500 text-sm mb-1">Element</div>
                              <div className="text-white text-xl">
                                {ELEMENTS[f.element]} {f.element.charAt(0).toUpperCase() + f.element.slice(1)}
                              </div>
                            </div>
                          )}

                          {f.spirit_animal && (
                            <div>
                              <div className="text-gray-500 text-sm mb-1">Animal Totem</div>
                              <div className="text-white">🦁 {f.spirit_animal}</div>
                            </div>
                          )}

                          {f.story && (
                            <div>
                              <div className="text-gray-500 text-sm mb-1">Histoire</div>
                              <p className="text-gray-300">{f.story}</p>
                            </div>
                          )}

                          {f.intention && (
                            <div>
                              <div className="text-gray-500 text-sm mb-1">Intention</div>
                              <p className="text-gray-300 italic">"{f.intention}"</p>
                            </div>
                          )}

                          {f.gifts && f.gifts.length > 0 && (
                            <div>
                              <div className="text-gray-500 text-sm mb-2">Dons a partager</div>
                              <div className="flex flex-wrap gap-2">
                                {f.gifts.map((gift, i) => (
                                  <span
                                    key={i}
                                    className="px-3 py-1 bg-yellow-600/20 text-yellow-400 rounded-full text-sm"
                                  >
                                    {gift}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {f.seeking && f.seeking.length > 0 && (
                            <div>
                              <div className="text-gray-500 text-sm mb-2">Recherche</div>
                              <div className="flex flex-wrap gap-2">
                                {f.seeking.map((item, i) => (
                                  <span
                                    key={i}
                                    className="px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full text-sm"
                                  >
                                    {item}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Actions */}
                        <div className="mt-6 pt-6 border-t border-gray-800">
                          <button className="w-full py-3 bg-yellow-600 text-black font-medium rounded-lg hover:bg-yellow-500">
                            Envoyer une Resonance 🌟
                          </button>
                        </div>
                      </>
                    );
                  })()}
                </div>
              </div>
            )}
          </div>
        )}

        {/* VUE: MESSAGES */}
        {view === 'messages' && (
          <div className="max-w-2xl mx-auto">
            {/* Zone de saisie */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 mb-6">
              <div className="flex gap-2 mb-3">
                {Object.entries(MESSAGE_TYPES).map(([key, type]) => (
                  <button
                    key={key}
                    onClick={() => setMessageType(key)}
                    className={`px-3 py-1 rounded-full text-sm transition-colors ${
                      messageType === key
                        ? 'bg-gray-700 text-white'
                        : 'bg-gray-800 text-gray-500 hover:text-gray-300'
                    }`}
                  >
                    {type.icon}
                  </button>
                ))}
              </div>

              <textarea
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder={`Partager ${MESSAGE_TYPES[messageType].name.toLowerCase()}...`}
                rows={3}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg
                  text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500
                  resize-none"
              />

              <div className="flex justify-between items-center mt-3">
                <span className="text-gray-500 text-sm">
                  {MESSAGE_TYPES[messageType].icon} {MESSAGE_TYPES[messageType].name}
                </span>
                <button
                  onClick={sendMessage}
                  disabled={!newMessage.trim()}
                  className="px-6 py-2 bg-yellow-600 text-black font-medium rounded-lg
                    hover:bg-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Partager
                </button>
              </div>
            </div>

            {/* Liste des messages */}
            <div className="space-y-4">
              {messages.map(msg => {
                const type = MESSAGE_TYPES[msg.message_type] || MESSAGE_TYPES.sharing;
                const authorName = msg.author?.display_name || 'Fondateur';

                return (
                  <div
                    key={msg.id}
                    className="bg-gray-900/50 border border-gray-800 rounded-xl p-4"
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className="w-10 h-10 rounded-full flex items-center justify-center text-lg shrink-0"
                        style={{ backgroundColor: `${type.color}20` }}
                      >
                        {type.icon}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-white font-medium">{authorName}</span>
                          <span className="text-gray-600 text-sm">
                            {new Date(msg.created_at).toLocaleDateString('fr-FR', {
                              day: 'numeric',
                              month: 'short',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        </div>
                        <p className="text-gray-300">{msg.content}</p>
                      </div>
                    </div>
                  </div>
                );
              })}

              {messages.length === 0 && (
                <div className="text-center py-12">
                  <div className="text-4xl mb-4">💬</div>
                  <p className="text-gray-500">
                    Le cercle de parole attend sa premiere voix...
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* VUE: MON PROFIL */}
        {view === 'profile' && myProfile && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-6">Mon Profil Fondateur</h2>

              {/* Affichage du profil actuel */}
              <div className="space-y-4">
                <div className="flex items-center gap-4 p-4 bg-black/50 rounded-lg">
                  <div className="text-4xl">
                    {FOUNDER_TYPES[myProfile.founder_type]?.icon}
                  </div>
                  <div>
                    <div className="text-white font-medium">
                      Fondateur #{myProfile.founder_number}
                    </div>
                    <div style={{ color: FOUNDER_TYPES[myProfile.founder_type]?.color }}>
                      {FOUNDER_TYPES[myProfile.founder_type]?.name}
                    </div>
                  </div>
                </div>

                {myProfile.intention && (
                  <div className="p-4 bg-black/50 rounded-lg">
                    <div className="text-gray-500 text-sm mb-1">Mon Intention</div>
                    <p className="text-gray-300">"{myProfile.intention}"</p>
                  </div>
                )}

                {myProfile.gifts && myProfile.gifts.length > 0 && (
                  <div className="p-4 bg-black/50 rounded-lg">
                    <div className="text-gray-500 text-sm mb-2">Mes Dons</div>
                    <div className="flex flex-wrap gap-2">
                      {myProfile.gifts.map((gift, i) => (
                        <span
                          key={i}
                          className="px-3 py-1 bg-yellow-600/20 text-yellow-400 rounded-full text-sm"
                        >
                          {gift}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="pt-4 border-t border-gray-800">
                  <p className="text-gray-500 text-sm text-center">
                    Membre depuis le {new Date(myProfile.joined_at).toLocaleDateString('fr-FR', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default CerclePage;
