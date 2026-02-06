/**
 * ===============================================================================
 *
 *      ████████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ ███████╗
 *      ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝
 *         ██║   ███████║██████╔╝█████╗  ███████║██║  ██║███████╗
 *         ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══██║██║  ██║╚════██║
 *         ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝███████║
 *         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
 *
 *                   🔒 PRIVATE THREADS 🔒
 *             Discussions privées entre fondateurs
 *                    CHE·NU V76 - AT·OM
 *
 * ===============================================================================
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';

// ===============================================================================
// COMPOSANT: LISTE DES THREADS
// ===============================================================================

const ThreadList = ({ threads, selectedThread, onSelect, onCreateNew }) => (
  <div className="space-y-2">
    {/* Bouton nouveau thread */}
    <button
      onClick={onCreateNew}
      className="w-full p-3 border border-dashed border-gray-700 rounded-lg text-gray-500
        hover:border-yellow-500/50 hover:text-yellow-400 transition-all flex items-center justify-center gap-2"
    >
      <span>+</span> Nouveau Thread
    </button>

    {/* Liste des threads */}
    {threads.map((thread) => (
      <button
        key={thread.id}
        onClick={() => onSelect(thread)}
        className={`w-full p-3 rounded-lg text-left transition-all ${
          selectedThread?.id === thread.id
            ? 'bg-yellow-900/30 border border-yellow-500/50'
            : 'bg-gray-800/50 border border-gray-700 hover:border-gray-600'
        }`}
      >
        <div className="flex items-center justify-between">
          <span className={`font-medium ${
            selectedThread?.id === thread.id ? 'text-yellow-400' : 'text-white'
          }`}>
            {thread.title}
          </span>
          {thread.unread_count > 0 && (
            <span className="px-2 py-0.5 bg-yellow-500 text-black text-xs rounded-full">
              {thread.unread_count}
            </span>
          )}
        </div>
        <p className="text-gray-500 text-xs mt-1 truncate">
          {thread.participants_count} participants • {thread.messages_count || 0} messages
        </p>
      </button>
    ))}

    {threads.length === 0 && (
      <p className="text-gray-600 text-sm text-center py-4">
        Aucun thread privé
      </p>
    )}
  </div>
);

// ===============================================================================
// COMPOSANT: MESSAGE DE THREAD
// ===============================================================================

const ThreadMessage = ({ message, isOwn }) => {
  const time = new Date(message.created_at).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`flex gap-3 ${isOwn ? 'flex-row-reverse' : ''}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${
        isOwn ? 'bg-yellow-500/20 text-yellow-400' : 'bg-purple-500/20 text-purple-400'
      }`}>
        {(message.sender_name || 'A')[0].toUpperCase()}
      </div>
      <div className={`max-w-[70%] ${isOwn ? 'text-right' : ''}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className={`text-xs font-medium ${isOwn ? 'text-yellow-400' : 'text-purple-400'}`}>
            {message.sender_name}
          </span>
          <span className="text-gray-600 text-xs">{time}</span>
        </div>
        <div className={`px-3 py-2 rounded-lg ${
          isOwn ? 'bg-yellow-900/30 text-yellow-100' : 'bg-purple-900/30 text-purple-100'
        }`}>
          <p className="text-sm break-words">{message.content}</p>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: VUE DU THREAD
// ===============================================================================

const ThreadView = ({ thread, currentUserId, currentUserName, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // Charger les messages du thread
  useEffect(() => {
    const fetchMessages = async () => {
      if (!isSupabaseConfigured || !thread) {
        setLoading(false);
        return;
      }

      try {
        const { data, error } = await supabase
          .from('thread_messages')
          .select('*')
          .eq('thread_id', thread.id)
          .order('created_at', { ascending: true });

        if (error) throw error;
        setMessages(data || []);
      } catch (err) {
        console.error('[THREAD] Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, [thread]);

  // Écouter les nouveaux messages
  useEffect(() => {
    if (!isSupabaseConfigured || !thread) return;

    const subscription = supabase
      .channel(`thread_${thread.id}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'thread_messages',
        filter: `thread_id=eq.${thread.id}`
      }, (payload) => {
        setMessages(prev => [...prev, payload.new]);
        scrollToBottom();
      })
      .subscribe();

    return () => subscription.unsubscribe();
  }, [thread, scrollToBottom]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    const content = newMessage.trim();
    setNewMessage('');
    setSending(true);

    try {
      if (!isSupabaseConfigured) {
        setMessages(prev => [...prev, {
          id: Date.now(),
          thread_id: thread.id,
          content,
          sender_name: currentUserName,
          sender_id: currentUserId,
          created_at: new Date().toISOString()
        }]);
        setSending(false);
        return;
      }

      const { error } = await supabase
        .from('thread_messages')
        .insert({
          thread_id: thread.id,
          content,
          sender_name: currentUserName,
          sender_id: currentUserId
        });

      if (error) throw error;
    } catch (err) {
      console.error('[THREAD] Erreur envoi:', err);
      setNewMessage(content);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header du thread */}
      <div className="p-4 border-b border-gray-800 bg-black/30">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="text-gray-500 hover:text-white transition-colors"
          >
            ←
          </button>
          <div>
            <h4 className="text-white font-medium">{thread.title}</h4>
            <p className="text-gray-500 text-xs">{thread.participants_count} participants</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {loading ? (
          <p className="text-gray-500 text-center">Chargement...</p>
        ) : messages.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-3xl">🔒</span>
            <p className="text-gray-500 mt-2">Thread privé créé</p>
            <p className="text-gray-600 text-sm">Commencez la discussion</p>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <ThreadMessage
                key={msg.id}
                message={msg}
                isOwn={msg.sender_id === currentUserId}
              />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="p-4 border-t border-gray-800 bg-black/30">
        <div className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Message privé..."
            className="flex-1 px-4 py-2 bg-black/50 border border-gray-700 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-purple-500/50"
            maxLength={500}
            disabled={sending}
          />
          <button
            type="submit"
            disabled={!newMessage.trim() || sending}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              !newMessage.trim() || sending
                ? 'bg-gray-800 text-gray-600 cursor-not-allowed'
                : 'bg-purple-600 text-white hover:bg-purple-500'
            }`}
          >
            →
          </button>
        </div>
      </form>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: MODAL CRÉATION DE THREAD
// ===============================================================================

const CreateThreadModal = ({ onClose, onCreate, founders }) => {
  const [title, setTitle] = useState('');
  const [selectedParticipants, setSelectedParticipants] = useState([]);
  const [creating, setCreating] = useState(false);

  const toggleParticipant = (founderId) => {
    setSelectedParticipants(prev =>
      prev.includes(founderId)
        ? prev.filter(id => id !== founderId)
        : [...prev, founderId]
    );
  };

  const handleCreate = async () => {
    if (!title.trim() || selectedParticipants.length === 0) return;

    setCreating(true);
    await onCreate(title.trim(), selectedParticipants);
    setCreating(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="w-full max-w-md bg-gray-900 border border-gray-700 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>🔒</span> Nouveau Thread Privé
        </h3>

        <div className="space-y-4">
          {/* Titre */}
          <div>
            <label className="block text-gray-400 text-sm mb-2">Titre du thread</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Ex: Projet Collaboration"
              className="w-full px-4 py-2 bg-black/50 border border-gray-700 rounded-lg text-white
                placeholder-gray-600 focus:outline-none focus:border-purple-500/50"
              maxLength={100}
            />
          </div>

          {/* Participants */}
          <div>
            <label className="block text-gray-400 text-sm mb-2">
              Inviter des fondateurs ({selectedParticipants.length} sélectionnés)
            </label>
            <div className="max-h-48 overflow-y-auto space-y-2 bg-black/30 rounded-lg p-2">
              {founders.map((founder) => (
                <button
                  key={founder.id}
                  onClick={() => toggleParticipant(founder.id)}
                  className={`w-full p-2 rounded-lg text-left transition-all flex items-center gap-3 ${
                    selectedParticipants.includes(founder.id)
                      ? 'bg-purple-900/30 border border-purple-500/50'
                      : 'bg-gray-800/50 hover:bg-gray-700/50'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm ${
                    selectedParticipants.includes(founder.id)
                      ? 'bg-purple-500/30 text-purple-400'
                      : 'bg-gray-700 text-gray-400'
                  }`}>
                    {(founder.full_name || 'F')[0].toUpperCase()}
                  </div>
                  <span className={selectedParticipants.includes(founder.id) ? 'text-purple-300' : 'text-white'}>
                    {founder.full_name || 'Fondateur'}
                  </span>
                  {selectedParticipants.includes(founder.id) && (
                    <span className="ml-auto text-purple-400">✓</span>
                  )}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3 mt-6">
          <button
            onClick={onClose}
            className="flex-1 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700 transition-colors"
          >
            Annuler
          </button>
          <button
            onClick={handleCreate}
            disabled={!title.trim() || selectedParticipants.length === 0 || creating}
            className={`flex-1 py-2 rounded-lg font-medium transition-all ${
              !title.trim() || selectedParticipants.length === 0 || creating
                ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                : 'bg-purple-600 text-white hover:bg-purple-500'
            }`}
          >
            {creating ? 'Création...' : 'Créer'}
          </button>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// COMPOSANT PRINCIPAL: PRIVATE THREADS
// ===============================================================================

const PrivateThreads = ({ founders = [] }) => {
  const { user } = useAuth();
  const [threads, setThreads] = useState([]);
  const [selectedThread, setSelectedThread] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(true);

  const currentUserId = user?.id || `guest_${Date.now()}`;
  const currentUserName = user?.user_metadata?.display_name || 'Invité';

  // Charger les threads
  useEffect(() => {
    const fetchThreads = async () => {
      if (!isSupabaseConfigured) {
        setThreads([
          {
            id: 1,
            title: 'Projet Collaboration',
            participants_count: 3,
            messages_count: 12,
            unread_count: 2
          }
        ]);
        setLoading(false);
        return;
      }

      try {
        const { data, error } = await supabase
          .from('private_threads')
          .select('*')
          .contains('participant_ids', [currentUserId])
          .order('updated_at', { ascending: false });

        if (error) throw error;
        setThreads(data || []);
      } catch (err) {
        console.error('[THREADS] Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchThreads();
  }, [currentUserId]);

  // Créer un nouveau thread
  const handleCreateThread = async (title, participantIds) => {
    try {
      if (!isSupabaseConfigured) {
        const newThread = {
          id: Date.now(),
          title,
          participant_ids: [currentUserId, ...participantIds],
          participants_count: participantIds.length + 1,
          messages_count: 0,
          created_by: currentUserId,
          created_at: new Date().toISOString()
        };
        setThreads(prev => [newThread, ...prev]);
        setSelectedThread(newThread);
        return;
      }

      const { data, error } = await supabase
        .from('private_threads')
        .insert({
          title,
          participant_ids: [currentUserId, ...participantIds],
          participants_count: participantIds.length + 1,
          created_by: currentUserId
        })
        .select()
        .single();

      if (error) throw error;
      setThreads(prev => [data, ...prev]);
      setSelectedThread(data);
    } catch (err) {
      console.error('[THREADS] Erreur création:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Chargement des threads...</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden h-96">
      {selectedThread ? (
        <ThreadView
          thread={selectedThread}
          currentUserId={currentUserId}
          currentUserName={currentUserName}
          onBack={() => setSelectedThread(null)}
        />
      ) : (
        <div className="p-4">
          <h3 className="text-white font-medium mb-4 flex items-center gap-2">
            <span>🔒</span> PRIVATE THREADS
          </h3>
          <ThreadList
            threads={threads}
            selectedThread={selectedThread}
            onSelect={setSelectedThread}
            onCreateNew={() => setShowCreateModal(true)}
          />
        </div>
      )}

      {/* Modal création */}
      {showCreateModal && (
        <CreateThreadModal
          onClose={() => setShowCreateModal(false)}
          onCreate={handleCreateThread}
          founders={founders.filter(f => f.id !== currentUserId)}
        />
      )}
    </div>
  );
};

export default PrivateThreads;
