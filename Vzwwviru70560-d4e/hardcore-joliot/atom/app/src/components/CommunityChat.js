/**
 * ===============================================================================
 *
 *       ██████╗██╗  ██╗ █████╗ ████████╗
 *      ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
 *      ██║     ███████║███████║   ██║
 *      ██║     ██╔══██║██╔══██║   ██║
 *      ╚██████╗██║  ██║██║  ██║   ██║
 *       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
 *
 *              💬 COMMUNITY CHAT 💬
 *          Chat temps réel avec Supabase
 *                 CHE·NU V76 - AT·OM
 *
 * ===============================================================================
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';

// ===============================================================================
// COMPOSANT: MESSAGE UNIQUE
// ===============================================================================

const ChatMessage = ({ message, isOwn }) => {
  const time = new Date(message.created_at).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`flex gap-3 ${isOwn ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${
        isOwn
          ? 'bg-yellow-500/20 text-yellow-400'
          : 'bg-cyan-500/20 text-cyan-400'
      }`}>
        {(message.sender_name || 'A')[0].toUpperCase()}
      </div>

      {/* Contenu */}
      <div className={`max-w-[70%] ${isOwn ? 'text-right' : ''}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className={`text-xs font-medium ${isOwn ? 'text-yellow-400' : 'text-cyan-400'}`}>
            {message.sender_name || 'Anonyme'}
          </span>
          <span className="text-gray-600 text-xs">{time}</span>
        </div>
        <div className={`px-3 py-2 rounded-lg ${
          isOwn
            ? 'bg-yellow-900/30 text-yellow-100'
            : 'bg-gray-800 text-gray-200'
        }`}>
          <p className="text-sm break-words">{message.content}</p>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: INDICATEUR DE FRAPPE
// ===============================================================================

const TypingIndicator = ({ typers }) => {
  if (typers.length === 0) return null;

  return (
    <div className="flex items-center gap-2 px-4 py-2 text-gray-500 text-xs">
      <div className="flex gap-1">
        <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <span>
        {typers.length === 1
          ? `${typers[0]} écrit...`
          : `${typers.length} personnes écrivent...`
        }
      </span>
    </div>
  );
};

// ===============================================================================
// COMPOSANT PRINCIPAL: COMMUNITY CHAT
// ===============================================================================

const CommunityChat = ({ onClose, senderName }) => {
  const { user, isAuthenticated } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [typers, setTypers] = useState([]);
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const currentUserName = senderName ||
    user?.user_metadata?.display_name ||
    user?.email?.split('@')[0] ||
    'Invité';

  const currentUserId = user?.id || `guest_${Date.now()}`;

  // Scroll vers le bas
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // Charger les messages initiaux
  useEffect(() => {
    const fetchMessages = async () => {
      if (!isSupabaseConfigured) {
        setMessages([
          {
            id: 1,
            content: 'Bienvenue dans le chat de la communauté AT·OM!',
            sender_name: 'System',
            sender_id: 'system',
            created_at: new Date().toISOString()
          }
        ]);
        setLoading(false);
        return;
      }

      try {
        const { data, error } = await supabase
          .from('community_messages')
          .select('*')
          .order('created_at', { ascending: true })
          .limit(100);

        if (error) throw error;
        setMessages(data || []);
      } catch (err) {
        console.error('[CHAT] Erreur chargement:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, []);

  // Écouter les nouveaux messages en temps réel
  useEffect(() => {
    if (!isSupabaseConfigured) return;

    const subscription = supabase
      .channel('community_chat')
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'community_messages'
      }, (payload) => {
        setMessages(prev => [...prev, payload.new]);
        scrollToBottom();
      })
      .subscribe();

    return () => subscription.unsubscribe();
  }, [scrollToBottom]);

  // Scroll automatique quand nouveaux messages
  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Envoyer un message
  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    const messageContent = newMessage.trim();
    setNewMessage('');
    setSending(true);

    try {
      if (!isSupabaseConfigured) {
        // Mode démo
        setMessages(prev => [...prev, {
          id: Date.now(),
          content: messageContent,
          sender_name: currentUserName,
          sender_id: currentUserId,
          created_at: new Date().toISOString()
        }]);
        setSending(false);
        return;
      }

      const { error } = await supabase
        .from('community_messages')
        .insert({
          content: messageContent,
          sender_name: currentUserName,
          sender_id: currentUserId
        });

      if (error) throw error;
    } catch (err) {
      console.error('[CHAT] Erreur envoi:', err);
      // Remettre le message en cas d'erreur
      setNewMessage(messageContent);
    } finally {
      setSending(false);
    }
  };

  // Gérer la saisie (indicateur de frappe)
  const handleTyping = (e) => {
    setNewMessage(e.target.value);

    // Broadcast typing indicator (optionnel, utilise Supabase Presence)
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    typingTimeoutRef.current = setTimeout(() => {
      // Stop typing indicator
    }, 2000);
  };

  return (
    <div className="flex flex-col h-full bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-gray-800 flex items-center justify-between bg-black/30">
        <div className="flex items-center gap-3">
          <span className="text-xl">💬</span>
          <div>
            <h3 className="text-white font-medium">COMMUNITY CHAT</h3>
            <p className="text-gray-500 text-xs">{messages.length} messages</p>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-white transition-colors p-2"
          >
            ✕
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Chargement des messages...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <span className="text-4xl mb-4">🌟</span>
            <p className="text-gray-400">Soyez le premier à écrire!</p>
            <p className="text-gray-600 text-sm mt-2">
              Partagez vos pensées avec la communauté
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                isOwn={message.sender_id === currentUserId}
              />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Indicateur de frappe */}
      <TypingIndicator typers={typers} />

      {/* Input */}
      <form onSubmit={handleSend} className="p-4 border-t border-gray-800 bg-black/30">
        <div className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={handleTyping}
            placeholder={`Écrire en tant que ${currentUserName}...`}
            className="flex-1 px-4 py-2 bg-black/50 border border-gray-700 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
            maxLength={500}
            disabled={sending}
          />
          <button
            type="submit"
            disabled={!newMessage.trim() || sending}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              !newMessage.trim() || sending
                ? 'bg-gray-800 text-gray-600 cursor-not-allowed'
                : 'bg-yellow-600 text-black hover:bg-yellow-500'
            }`}
          >
            {sending ? '...' : '→'}
          </button>
        </div>
      </form>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: CHAT POPUP (pour intégration dans d'autres pages)
// ===============================================================================

export const ChatPopup = ({ isOpen, onClose, senderName }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-md h-[600px]">
        <CommunityChat onClose={onClose} senderName={senderName} />
      </div>
    </div>
  );
};

export default CommunityChat;
