/**
 * ===============================================================================
 *
 *      ███████╗ ██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗
 *      ██╔════╝██╔═══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
 *      █████╗  ██║   ██║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
 *      ██╔══╝  ██║   ██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
 *      ██║     ╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║
 *      ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
 *
 *                 🏛️ AT·OM FOUNDER 🏛️
 *          Page Entreprise - Phase Fondatrice
 *
 *   Onglets: [ Vision | Réseau | Discussions | Archives | Activité ]
 *
 *   Ces onglets SIMULENT les fonctions des sphères CHE-NU
 *   sans exposer leur complexité. Espace transitoire.
 *
 * ===============================================================================
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import {
  UXObserverAgent,
  FeedbackAnalystAgent,
  StructureArchitectAgent,
  CoherenceGuardianAgent
} from '../services/FounderAdaptiveAgents';

// ===============================================================================
// CONSTANTES
// ===============================================================================

const SACRED = { M: 44.4, P: 161.8, I: 369, Po: 1728 };
const TARGET_FOUNDERS = 144;

// Onglets internes (style page entreprise)
const TABS = [
  { id: 'vision', label: 'Vision', description: 'Mission & Phase' },
  { id: 'reseau', label: 'Réseau', description: 'Membres' },
  { id: 'discussions', label: 'Discussions', description: 'Chat & Threads' },
  { id: 'archives', label: 'Archives', description: 'Documents' },
  { id: 'activite', label: 'Activité', description: 'Updates' }
];

// ===============================================================================
// NAVIGATION INTERNE (Onglets simples, style entreprise)
// ===============================================================================

const InternalTabs = ({ activeTab, onTabChange }) => (
  <nav className="border-b border-gray-800 bg-gray-950/50">
    <div className="max-w-5xl mx-auto px-4">
      <div className="flex gap-1 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`px-5 py-3 text-sm font-medium whitespace-nowrap transition-all border-b-2 ${
              activeTab === tab.id
                ? 'text-yellow-400 border-yellow-400'
                : 'text-gray-400 border-transparent hover:text-white hover:border-gray-600'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  </nav>
);

// ===============================================================================
// ONGLET 1: VISION - Mission, Phase Founder, Progression
// ===============================================================================

const VisionTab = ({ founders, currentUser, onAnchor, isAnchoring }) => {
  const [showAnchorForm, setShowAnchorForm] = useState(false);
  const [anchorName, setAnchorName] = useState('');
  const percentage = Math.min((founders.length / TARGET_FOUNDERS) * 100, 100);

  const handleAnchor = (e) => {
    e.preventDefault();
    if (anchorName.trim()) {
      onAnchor(anchorName.trim());
      setShowAnchorForm(false);
      setAnchorName('');
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <span className="text-5xl">🔱</span>
        <h1 className="text-3xl font-bold text-white mt-4">AT·OM</h1>
        <p className="text-yellow-400 mt-2">L'Arche des Résonances Universelles</p>
      </div>

      {/* Mission */}
      <section className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Notre Mission</h2>
        <p className="text-gray-300 leading-relaxed">
          AT·OM est une infrastructure souveraine pour la conscience collective.
          Nous construisons les fondations d'une économie alignée sur les fréquences
          sacrées : <span className="text-yellow-400 font-mono">{SACRED.M}</span> |
          <span className="text-yellow-400 font-mono"> {SACRED.P}</span> |
          <span className="text-yellow-400 font-mono"> {SACRED.I}</span> |
          <span className="text-yellow-400 font-mono"> {SACRED.Po}</span>
        </p>
      </section>

      {/* Phase actuelle */}
      <section className="bg-gradient-to-r from-yellow-900/20 to-gray-900/50 border border-yellow-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-3 h-3 rounded-full bg-yellow-500 animate-pulse" />
          <h2 className="text-lg font-bold text-yellow-400">Phase I — Fondation</h2>
        </div>
        <p className="text-gray-300 mb-4">
          Nous recrutons les 144 premiers fondateurs. Cette phase est réservée aux
          pionniers qui ancrent leur présence dans le réseau avant l'ouverture publique.
        </p>
        <div className="bg-black/30 rounded-lg p-4">
          <p className="text-sm text-gray-400 mb-2">Pourquoi tout est verrouillé ?</p>
          <p className="text-gray-500 text-sm">
            Les sphères complètes (Communication, Scholar, Mémoire...) seront déverrouillées
            progressivement. Pour l'instant, Founder centralise les fonctions essentielles.
          </p>
        </div>
      </section>

      {/* Progression */}
      <section className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Progression du Réseau</h2>
        <div className="flex items-end justify-between mb-3">
          <div>
            <span className="text-4xl font-bold text-yellow-400">{founders.length}</span>
            <span className="text-2xl text-gray-500"> / {TARGET_FOUNDERS}</span>
          </div>
          <span className="text-gray-500">{percentage.toFixed(1)}%</span>
        </div>
        <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 transition-all duration-1000"
            style={{ width: `${percentage}%` }}
          />
        </div>
        <p className="text-gray-500 text-sm mt-3 text-center">
          {percentage < 100
            ? `${TARGET_FOUNDERS - founders.length} fondateurs restants pour l'activation complète`
            : '✨ Grille fondatrice activée'}
        </p>
      </section>

      {/* CTA Ancrage */}
      {!currentUser && (
        <section className="text-center py-6">
          {!showAnchorForm ? (
            <button
              onClick={() => setShowAnchorForm(true)}
              className="px-8 py-4 bg-gradient-to-r from-yellow-600 to-yellow-500 text-black font-bold rounded-xl hover:from-yellow-500 hover:to-yellow-400 transition-all text-lg"
            >
              Rejoindre les Fondateurs
            </button>
          ) : (
            <form onSubmit={handleAnchor} className="max-w-sm mx-auto space-y-4">
              <input
                type="text"
                value={anchorName}
                onChange={(e) => setAnchorName(e.target.value)}
                placeholder="Ton nom ou alias"
                className="w-full px-4 py-3 bg-black border border-yellow-500/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-yellow-500"
                autoFocus
              />
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowAnchorForm(false)}
                  className="flex-1 py-3 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  disabled={isAnchoring || !anchorName.trim()}
                  className="flex-1 py-3 bg-yellow-600 text-black rounded-lg font-bold hover:bg-yellow-500 disabled:opacity-50"
                >
                  {isAnchoring ? 'Ancrage...' : 'Confirmer'}
                </button>
              </div>
            </form>
          )}
        </section>
      )}

      {/* Vidéo intro placeholder */}
      <section className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Vidéo d'Introduction</h2>
        <div className="aspect-video bg-gray-800 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <span className="text-4xl">▶️</span>
            <p className="text-gray-500 mt-2">Vidéo à venir</p>
          </div>
        </div>
      </section>
    </div>
  );
};

// ===============================================================================
// ONGLET 2: RÉSEAU - Planète + Membres
// ===============================================================================

const PlanetCanvas = ({ founders, onFounderClick }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const rotationRef = useRef(0);
  const [hovered, setHovered] = useState(null);

  const getPositions = useCallback(() => {
    return founders.map((f, i) => {
      const phi = Math.acos(1 - 2 * (i + 0.5) / Math.max(founders.length, 1));
      const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 0.5);
      return { ...f, x: Math.sin(phi) * Math.cos(theta), y: Math.sin(phi) * Math.sin(theta), z: Math.cos(phi) };
    });
  }, [founders]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.offsetWidth * 2;
    const h = canvas.height = canvas.offsetHeight * 2;
    const cx = w / 2, cy = h / 2, r = Math.min(w, h) * 0.38;
    const positions = getPositions();

    const draw = () => {
      ctx.clearRect(0, 0, w, h);

      // Stars
      for (let i = 0; i < 60; i++) {
        const sx = (Math.sin(i * 127) * 0.5 + 0.5) * w;
        const sy = (Math.cos(i * 311) * 0.5 + 0.5) * h;
        ctx.fillStyle = `rgba(255,255,255,${0.05 + Math.sin(Date.now() / 1000 + i) * 0.03})`;
        ctx.beginPath();
        ctx.arc(sx, sy, 1, 0, Math.PI * 2);
        ctx.fill();
      }

      // Planet glow
      const glow = ctx.createRadialGradient(cx, cy, r * 0.8, cx, cy, r * 1.2);
      glow.addColorStop(0, 'rgba(30, 58, 138, 0.15)');
      glow.addColorStop(1, 'rgba(30, 58, 138, 0)');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(cx, cy, r * 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Grid
      ctx.strokeStyle = 'rgba(212, 175, 55, 0.05)';
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2 + rotationRef.current;
        ctx.beginPath();
        for (let j = 0; j <= 24; j++) {
          const p = (j / 24) * Math.PI;
          const x = cx + Math.sin(p) * Math.cos(a) * r;
          const y = cy + Math.cos(p) * r;
          j === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // Points
      positions.forEach((f) => {
        const rx = f.x * Math.cos(rotationRef.current) - f.y * Math.sin(rotationRef.current);
        const ry = f.x * Math.sin(rotationRef.current) + f.y * Math.cos(rotationRef.current);
        if (f.z > -0.2) {
          const sx = cx + rx * r;
          const sy = cy + f.z * r;
          const scale = (ry + 1) / 2;
          const pr = 2 + scale * 4;
          const alpha = 0.3 + scale * 0.7;
          const isHov = hovered?.id === f.id;
          const isCreator = f.is_active_creator || f.youtube_channel_url;

          if (isCreator) {
            const pa = 0.2 + Math.sin(Date.now() / 1000 * 2 + (f.id || 0)) * 0.15;
            const aura = ctx.createRadialGradient(sx, sy, 0, sx, sy, pr * 5);
            aura.addColorStop(0, `rgba(255,215,0,${pa})`);
            aura.addColorStop(1, 'rgba(255,165,0,0)');
            ctx.fillStyle = aura;
            ctx.beginPath();
            ctx.arc(sx, sy, pr * 5, 0, Math.PI * 2);
            ctx.fill();
          }

          ctx.fillStyle = isHov ? '#FFF' : (isCreator ? '#FFD700' : '#D4AF37');
          ctx.beginPath();
          ctx.arc(sx, sy, pr, 0, Math.PI * 2);
          ctx.fill();

          f.screenX = sx / 2;
          f.screenY = sy / 2;
          f.screenR = pr * 2;
        }
      });

      rotationRef.current += 0.001;
      animationRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animationRef.current);
  }, [founders, getPositions, hovered]);

  const handleMove = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    const positions = getPositions();
    for (const f of positions) {
      if (f.screenX && Math.hypot(x - f.screenX, y - f.screenY) < (f.screenR || 15) + 10) {
        setHovered(f);
        return;
      }
    }
    setHovered(null);
  };

  return (
    <div className="relative aspect-square max-w-md mx-auto">
      <canvas
        ref={canvasRef}
        className="w-full h-full cursor-crosshair"
        onMouseMove={handleMove}
        onMouseLeave={() => setHovered(null)}
        onClick={() => hovered && onFounderClick?.(hovered)}
      />
      {hovered && (
        <div
          className="absolute pointer-events-none bg-black/95 border border-yellow-500/30 rounded-lg p-3 transform -translate-x-1/2"
          style={{ left: hovered.screenX, top: hovered.screenY - 80 }}
        >
          <p className="text-yellow-400 font-bold text-sm">{hovered.full_name}</p>
          <p className="text-gray-500 text-xs">{hovered.role || 'FOUNDER'}</p>
          {(hovered.is_active_creator || hovered.youtube_channel_url) && (
            <p className="text-red-400 text-xs mt-1">📺 Créateur</p>
          )}
        </div>
      )}
    </div>
  );
};

const ReseauTab = ({ founders, currentUser, onProfileClick }) => {
  const [selectedMember, setSelectedMember] = useState(null);
  const [view, setView] = useState('planet'); // 'planet' | 'list'

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-white">Réseau des Fondateurs</h2>
          <p className="text-gray-500">{founders.length} membres connectés</p>
        </div>
        <div className="flex gap-2 bg-gray-800 rounded-lg p-1">
          <button
            onClick={() => setView('planet')}
            className={`px-3 py-1 rounded text-sm ${view === 'planet' ? 'bg-yellow-600 text-black' : 'text-gray-400'}`}
          >
            🌍 Planète
          </button>
          <button
            onClick={() => setView('list')}
            className={`px-3 py-1 rounded text-sm ${view === 'list' ? 'bg-yellow-600 text-black' : 'text-gray-400'}`}
          >
            📋 Liste
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Vue principale */}
        <div className="lg:col-span-2">
          {view === 'planet' ? (
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
              <PlanetCanvas founders={founders} onFounderClick={setSelectedMember} />
            </div>
          ) : (
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4 max-h-[500px] overflow-y-auto">
              <div className="grid grid-cols-2 gap-3">
                {founders.map((f) => (
                  <div
                    key={f.id}
                    onClick={() => setSelectedMember(f)}
                    className="flex items-center gap-3 p-3 bg-black/30 rounded-lg hover:bg-gray-800/50 cursor-pointer transition-all"
                  >
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center overflow-hidden ${
                      f.is_active_creator ? 'ring-2 ring-yellow-500' : ''
                    } ${f.avatar_url ? '' : 'bg-gray-800'}`}>
                      {f.avatar_url ? (
                        <img src={f.avatar_url} alt="" className="w-full h-full object-cover" />
                      ) : (
                        <span className="text-yellow-400">{(f.full_name || 'F')[0]}</span>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white font-medium truncate">{f.full_name}</p>
                      <p className="text-gray-500 text-xs">{f.role || 'FOUNDER'}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Panneau latéral - Membre sélectionné */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
          {selectedMember ? (
            <div className="text-center">
              <div className={`w-20 h-20 mx-auto rounded-full flex items-center justify-center overflow-hidden mb-4 ${
                selectedMember.is_active_creator ? 'ring-2 ring-yellow-500' : ''
              } ${selectedMember.avatar_url ? '' : 'bg-gray-800'}`}>
                {selectedMember.avatar_url ? (
                  <img src={selectedMember.avatar_url} alt="" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-3xl text-yellow-400">{(selectedMember.full_name || 'F')[0]}</span>
                )}
              </div>
              <h3 className="text-white font-bold text-lg">{selectedMember.full_name}</h3>
              <p className="text-yellow-400 text-sm">{selectedMember.role || 'FOUNDER'}</p>
              {selectedMember.bio && (
                <p className="text-gray-400 text-sm mt-3">{selectedMember.bio}</p>
              )}
              <div className="flex gap-2 mt-4 justify-center">
                {selectedMember.youtube_channel_url && (
                  <a
                    href={selectedMember.youtube_channel_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-red-600/20 text-red-400 rounded-lg text-sm hover:bg-red-600/30"
                  >
                    📺 YouTube
                  </a>
                )}
                {selectedMember.facebook_url && (
                  <a
                    href={selectedMember.facebook_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-blue-600/20 text-blue-400 rounded-lg text-sm hover:bg-blue-600/30"
                  >
                    📘 Facebook
                  </a>
                )}
              </div>
              {selectedMember.id !== currentUser?.id && (
                <button className="mt-4 px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700 w-full">
                  💬 Message privé
                </button>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-600">
              <span className="text-4xl">👆</span>
              <p className="mt-3">Clique sur un membre pour voir son profil</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// ONGLET 3: DISCUSSIONS - Chat, Threads, Agents
// ===============================================================================

const DiscussionsTab = ({ currentUser }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [threads, setThreads] = useState([]);
  const [activeView, setActiveView] = useState('chat'); // 'chat' | 'threads'
  const messagesEndRef = useRef(null);

  // Load messages
  useEffect(() => {
    const fetch = async () => {
      if (!isSupabaseConfigured) {
        setMessages([{ id: 1, content: 'Bienvenue dans le chat!', sender_name: 'System', created_at: new Date().toISOString() }]);
        return;
      }
      const { data } = await supabase.from('community_messages').select('*').eq('room', 'global').order('created_at').limit(100);
      setMessages(data || []);
    };
    fetch();
  }, []);

  // Realtime
  useEffect(() => {
    if (!isSupabaseConfigured) return;
    const sub = supabase.channel('chat').on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'community_messages', filter: 'room=eq.global' }, (p) => {
      setMessages(prev => [...prev, p.new].slice(-100));
    }).subscribe();
    return () => sub.unsubscribe();
  }, []);

  // Load threads
  useEffect(() => {
    const fetch = async () => {
      if (!isSupabaseConfigured || !currentUser?.id) return;
      const { data } = await supabase.from('private_threads').select('*').contains('participants', [currentUser.id]).order('updated_at', { ascending: false });
      setThreads(data || []);
    };
    fetch();
  }, [currentUser]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;
    const content = newMessage.trim();
    setNewMessage('');
    setSending(true);
    try {
      if (isSupabaseConfigured) {
        await supabase.from('community_messages').insert({
          content,
          sender_name: currentUser?.full_name || 'Invité',
          sender_id: currentUser?.id || `guest_${Date.now()}`,
          room: 'global',
          origin_context: 'founder',
          future_sphere: 'communication'
        });
      } else {
        setMessages(prev => [...prev, { id: Date.now(), content, sender_name: currentUser?.full_name || 'Invité', sender_id: currentUser?.id, created_at: new Date().toISOString() }]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* View toggle */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">Discussions</h2>
        <div className="flex gap-2 bg-gray-800 rounded-lg p-1">
          <button
            onClick={() => setActiveView('chat')}
            className={`px-4 py-1 rounded text-sm ${activeView === 'chat' ? 'bg-yellow-600 text-black' : 'text-gray-400'}`}
          >
            💬 Chat Global
          </button>
          <button
            onClick={() => setActiveView('threads')}
            className={`px-4 py-1 rounded text-sm ${activeView === 'threads' ? 'bg-yellow-600 text-black' : 'text-gray-400'}`}
          >
            🔐 Threads ({threads.length})
          </button>
        </div>
      </div>

      {activeView === 'chat' ? (
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
          {/* Messages */}
          <div className="h-96 overflow-y-auto p-4 space-y-3">
            {messages.map((m) => (
              <div key={m.id} className={`flex gap-3 ${m.sender_id === currentUser?.id ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-sm ${
                  m.sender_id === currentUser?.id ? 'bg-yellow-500/20 text-yellow-400' : 'bg-gray-800 text-gray-400'
                }`}>
                  {(m.sender_name || 'A')[0]}
                </div>
                <div className={`max-w-[70%] ${m.sender_id === currentUser?.id ? 'text-right' : ''}`}>
                  <p className="text-gray-500 text-xs mb-1">{m.sender_name}</p>
                  <div className={`px-3 py-2 rounded-xl text-sm ${
                    m.sender_id === currentUser?.id ? 'bg-yellow-900/30 text-yellow-100' : 'bg-gray-800/50 text-gray-200'
                  }`}>
                    {m.content}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="p-4 border-t border-gray-800 bg-black/30">
            <div className="flex gap-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Écrire un message..."
                className="flex-1 px-4 py-3 bg-black border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
                maxLength={500}
              />
              <button
                type="submit"
                disabled={!newMessage.trim() || sending}
                className="px-5 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 disabled:opacity-50"
              >
                →
              </button>
            </div>
          </form>
        </div>
      ) : (
        <div className="space-y-4">
          {threads.length > 0 ? (
            threads.map((t) => (
              <div key={t.id} className="p-4 bg-gray-900/50 border border-gray-800 rounded-xl hover:border-purple-500/30 cursor-pointer transition-all">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400">💬</div>
                  <div className="flex-1">
                    <p className="text-white font-medium">{t.title}</p>
                    <p className="text-gray-500 text-xs">{t.participants?.length || 1} participant(s)</p>
                  </div>
                  <span className="text-gray-600">→</span>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 text-gray-600">
              <span className="text-4xl">🔐</span>
              <p className="mt-3">Aucun thread privé</p>
              <button className="mt-4 px-4 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700">
                + Créer un thread
              </button>
            </div>
          )}
        </div>
      )}

      {/* Agent placeholder */}
      <div className="mt-6 p-4 bg-gray-900/30 border border-dashed border-gray-700 rounded-xl">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🤖</span>
          <div>
            <p className="text-gray-400">Agents IA</p>
            <p className="text-gray-600 text-sm">Bientôt disponible : invitez un agent pour faciliter vos discussions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// ONGLET 4: ARCHIVES - Documents, Vidéos, Mémoire
// ===============================================================================

const ArchivesTab = ({ founders }) => {
  const [archives, setArchives] = useState([]);
  const youtubeCreators = founders.filter(f => f.youtube_channel_url);

  useEffect(() => {
    setArchives([
      { id: 1, title: 'Introduction AT·OM', type: 'video', creator: 'Architecte', date: '2026-01-20' },
      { id: 2, title: 'Guide des Fréquences Sacrées', type: 'pdf', creator: 'System', date: '2026-01-18' },
      { id: 3, title: 'Protocole de Résonance', type: 'pdf', creator: 'System', date: '2026-01-15' }
    ]);
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-xl font-bold text-white mb-6">Archives & Ressources</h2>

      {/* Créateurs YouTube */}
      {youtubeCreators.length > 0 && (
        <section className="mb-8">
          <h3 className="text-white font-medium mb-4">📺 Créateurs du Réseau</h3>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {youtubeCreators.map((c) => (
              <a
                key={c.id}
                href={c.youtube_channel_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-shrink-0 w-24 text-center group"
              >
                <div className={`w-16 h-16 mx-auto rounded-full overflow-hidden border-2 ${
                  c.is_active_creator ? 'border-yellow-500' : 'border-gray-700'
                } group-hover:border-red-500 transition-colors`}>
                  {c.avatar_url ? (
                    <img src={c.avatar_url} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-red-600 flex items-center justify-center">
                      <span className="text-white">▶</span>
                    </div>
                  )}
                </div>
                <p className="text-xs text-gray-400 mt-2 truncate group-hover:text-red-400">{c.full_name}</p>
              </a>
            ))}
          </div>
        </section>
      )}

      {/* Documents */}
      <section>
        <h3 className="text-white font-medium mb-4">📁 Documents & Vidéos</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {archives.map((a) => (
            <div key={a.id} className="p-4 bg-gray-900/50 border border-gray-800 rounded-xl hover:border-yellow-500/30 cursor-pointer transition-all">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{a.type === 'video' ? '🎬' : '📄'}</span>
                <div className="flex-1">
                  <p className="text-white font-medium">{a.title}</p>
                  <p className="text-gray-500 text-xs">{a.creator} • {a.date}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Mémoire validée */}
      <section className="mt-8">
        <h3 className="text-white font-medium mb-4">🧠 Mémoire Validée</h3>
        <div className="p-6 bg-gray-900/30 border border-dashed border-gray-700 rounded-xl text-center">
          <span className="text-3xl">📋</span>
          <p className="text-gray-500 mt-3">Les synthèses validées par les agents apparaîtront ici</p>
          <p className="text-gray-600 text-sm mt-1">Migration future → Sphère Scholar</p>
        </div>
      </section>
    </div>
  );
};

// ===============================================================================
// ONGLET 5: ACTIVITÉ - Flux d'updates
// ===============================================================================

const ActiviteTab = ({ founders }) => {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    const acts = founders.slice(0, 15).map((f, i) => ({
      id: f.id || i,
      type: 'joined',
      user: f.full_name,
      avatar: f.avatar_url,
      time: f.created_at || new Date(Date.now() - i * 3600000).toISOString()
    }));
    setActivities(acts);

    // Load from DB
    const fetch = async () => {
      if (!isSupabaseConfigured) return;
      const { data } = await supabase.from('activity_feed').select('*').order('created_at', { ascending: false }).limit(20);
      if (data?.length) setActivities(prev => [...data, ...prev].slice(0, 20));
    };
    fetch();
  }, [founders]);

  const formatTime = (t) => {
    const diff = Date.now() - new Date(t).getTime();
    const h = Math.floor(diff / 3600000);
    const d = Math.floor(h / 24);
    if (d > 0) return `${d}j`;
    if (h > 0) return `${h}h`;
    return 'maintenant';
  };

  const getIcon = (type) => {
    switch (type) {
      case 'joined': return '🌟';
      case 'message': return '💬';
      case 'video_upload': return '🎬';
      case 'thread_created': return '📝';
      default: return '⚡';
    }
  };

  const getMessage = (type) => {
    switch (type) {
      case 'joined': return 'a rejoint le réseau';
      case 'message': return 'a envoyé un message';
      case 'video_upload': return 'a partagé une vidéo';
      case 'thread_created': return 'a créé un thread';
      default: return 'activité';
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-xl font-bold text-white mb-6">Activité du Réseau</h2>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-yellow-400">{founders.length}</p>
          <p className="text-gray-500 text-sm">Fondateurs</p>
        </div>
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-cyan-400">{activities.length}</p>
          <p className="text-gray-500 text-sm">Activités</p>
        </div>
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-emerald-400">{Math.round((founders.length / TARGET_FOUNDERS) * 100)}%</p>
          <p className="text-gray-500 text-sm">Progression</p>
        </div>
      </div>

      {/* Feed */}
      <div className="space-y-2">
        {activities.map((a, i) => (
          <div key={a.id || i} className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-900/30 transition-colors">
            <div className="w-10 h-10 rounded-full flex items-center justify-center overflow-hidden bg-gray-800">
              {a.avatar ? (
                <img src={a.avatar} alt="" className="w-full h-full object-cover" />
              ) : (
                <span className="text-lg">{getIcon(a.type || a.activity_type)}</span>
              )}
            </div>
            <div className="flex-1">
              <p className="text-sm">
                <span className="text-yellow-400 font-medium">{a.user || a.user_name}</span>
                <span className="text-gray-400"> {getMessage(a.type || a.activity_type)}</span>
              </p>
            </div>
            <span className="text-gray-600 text-xs">{formatTime(a.time || a.created_at)}</span>
          </div>
        ))}
      </div>

      {activities.length === 0 && (
        <div className="text-center py-12 text-gray-600">
          <span className="text-4xl">🌙</span>
          <p className="mt-3">Le flux est calme...</p>
        </div>
      )}
    </div>
  );
};

// ===============================================================================
// MODAL: PROFIL
// ===============================================================================

const ProfileModal = ({ user, onUpdate, onClose }) => {
  const [name, setName] = useState(user?.full_name || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [youtube, setYoutube] = useState(user?.youtube_channel_url || '');
  const [facebook, setFacebook] = useState(user?.facebook_url || '');
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const fileRef = useRef(null);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file || !isSupabaseConfigured) return;
    setUploading(true);
    try {
      const path = `avatars/${user.id}.${file.name.split('.').pop()}`;
      await supabase.storage.from('zama-assets').upload(path, file, { upsert: true });
      const { data } = supabase.storage.from('zama-assets').getPublicUrl(path);
      if (data?.publicUrl) {
        await supabase.from('profiles').update({ avatar_url: data.publicUrl }).eq('id', user.id);
        onUpdate({ ...user, avatar_url: data.publicUrl });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const isCreator = youtube?.includes('youtube.com');
      if (isSupabaseConfigured) {
        await supabase.from('profiles').update({
          full_name: name, bio, youtube_channel_url: youtube, facebook_url: facebook, is_active_creator: isCreator
        }).eq('id', user.id);
      }
      onUpdate({ ...user, full_name: name, bio, youtube_channel_url: youtube, facebook_url: facebook, is_active_creator: isCreator });
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90" onClick={onClose}>
      <div className="w-full max-w-md bg-gray-900 border border-gray-700 rounded-xl p-6 max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white">Mon Profil</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-2xl">×</button>
        </div>

        <div className="flex items-center gap-4 mb-6">
          <div className="relative">
            <div className={`w-20 h-20 rounded-full bg-gray-800 overflow-hidden border-2 ${user?.is_active_creator ? 'border-yellow-500' : 'border-gray-700'}`}>
              {user?.avatar_url ? <img src={user.avatar_url} alt="" className="w-full h-full object-cover" /> : <div className="w-full h-full flex items-center justify-center text-3xl">👤</div>}
            </div>
            <button onClick={() => fileRef.current?.click()} disabled={uploading} className="absolute -bottom-1 -right-1 w-8 h-8 bg-yellow-600 rounded-full flex items-center justify-center text-black hover:bg-yellow-500">
              {uploading ? '...' : '📷'}
            </button>
            <input ref={fileRef} type="file" accept="image/*" onChange={handleUpload} className="hidden" />
          </div>
          <div>
            <p className="text-white font-medium">{user?.full_name || 'Fondateur'}</p>
            {user?.is_active_creator && <p className="text-yellow-400 text-xs">✨ Créateur</p>}
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-gray-400 text-sm mb-2">Nom</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full px-4 py-2 bg-black border border-gray-700 rounded-lg text-white focus:outline-none focus:border-yellow-500/50" />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Bio</label>
            <textarea value={bio} onChange={e => setBio(e.target.value)} className="w-full px-4 py-2 bg-black border border-gray-700 rounded-lg text-white focus:outline-none focus:border-yellow-500/50 resize-none h-20" maxLength={200} />
          </div>
          <div className="p-3 bg-red-900/10 border border-red-500/20 rounded-lg">
            <label className="block text-red-400 text-sm mb-2">📺 YouTube</label>
            <input type="url" value={youtube} onChange={e => setYoutube(e.target.value)} placeholder="https://youtube.com/@..." className="w-full px-4 py-2 bg-black border border-red-500/30 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-red-500/50" />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">📘 Facebook</label>
            <input type="url" value={facebook} onChange={e => setFacebook(e.target.value)} placeholder="https://facebook.com/..." className="w-full px-4 py-2 bg-black border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500/50" />
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 py-3 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700">Annuler</button>
          <button onClick={handleSave} disabled={saving} className="flex-1 py-3 bg-yellow-600 text-black rounded-lg font-bold hover:bg-yellow-500 disabled:opacity-50">
            {saving ? 'Sauvegarde...' : 'Sauvegarder'}
          </button>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// PANNEAU ADMIN: UX/STRUCTURE (Propositions des agents)
// ===============================================================================

const UXStructurePanel = ({ isOpen, onClose, currentUser }) => {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeProposal, setActiveProposal] = useState(null);
  const [rejectReason, setRejectReason] = useState('');

  // Charger les propositions
  useEffect(() => {
    const fetchProposals = async () => {
      if (!isSupabaseConfigured) {
        setProposals([
          {
            proposal_id: 'founder-ux-001',
            trigger_reason: 'Confusion répétée sur la navigation',
            observed_signals: ['5 messages de type "où trouver..."', 'Archives consultées par 12%'],
            problem: 'Les ressources sont difficiles à localiser',
            suggested_change: 'Remonter Archives au-dessus de Discussions',
            expected_effect: 'Meilleure visibilité des contenus structurants',
            confidence: 'élevé',
            status: 'pending',
            created_at: new Date().toISOString()
          }
        ]);
        setLoading(false);
        return;
      }
      try {
        const { data } = await supabase
          .from('founder_layout_proposals')
          .select('*')
          .order('created_at', { ascending: false });
        setProposals(data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    if (isOpen) fetchProposals();
  }, [isOpen]);

  const handleRespond = async (proposalId, action) => {
    if (!isSupabaseConfigured) {
      setProposals(prev => prev.map(p =>
        p.proposal_id === proposalId ? { ...p, status: action === 'approve' ? 'approved' : 'rejected' } : p
      ));
      setActiveProposal(null);
      return;
    }
    try {
      await supabase.rpc('respond_to_proposal', {
        p_proposal_id: proposalId,
        p_action: action,
        p_reason: action === 'reject' ? rejectReason : null
      });
      setProposals(prev => prev.map(p =>
        p.proposal_id === proposalId ? { ...p, status: action === 'approve' ? 'approved' : 'rejected' } : p
      ));
      setActiveProposal(null);
      setRejectReason('');
    } catch (err) {
      console.error(err);
    }
  };

  if (!isOpen) return null;

  const pendingCount = proposals.filter(p => p.status === 'pending').length;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90" onClick={onClose}>
      <div className="w-full max-w-2xl bg-gray-900 border border-gray-700 rounded-xl overflow-hidden max-h-[85vh]" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="p-4 border-b border-gray-800 flex items-center justify-between bg-gray-950">
          <div className="flex items-center gap-3">
            <span className="text-xl">🏗️</span>
            <div>
              <h2 className="text-white font-bold">UX / Structure</h2>
              <p className="text-gray-500 text-xs">Propositions des agents adaptatifs</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {pendingCount > 0 && (
              <span className="px-2 py-1 bg-yellow-600/20 text-yellow-400 text-xs rounded-full">
                {pendingCount} en attente
              </span>
            )}
            <button onClick={onClose} className="text-gray-500 hover:text-white text-xl">×</button>
          </div>
        </div>

        {/* Contenu */}
        <div className="p-4 overflow-y-auto max-h-[calc(85vh-120px)]">
          {loading ? (
            <div className="text-center py-8 text-gray-500">Chargement...</div>
          ) : proposals.length === 0 ? (
            <div className="text-center py-12">
              <span className="text-4xl">✨</span>
              <p className="text-gray-400 mt-4">Aucune proposition pour le moment</p>
              <p className="text-gray-600 text-sm mt-2">
                Les agents analysent l'usage toutes les 4 heures
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {proposals.map((p) => (
                <div
                  key={p.proposal_id}
                  className={`p-4 rounded-xl border transition-all ${
                    p.status === 'pending'
                      ? 'bg-yellow-900/10 border-yellow-500/30 hover:border-yellow-500/50'
                      : p.status === 'approved'
                      ? 'bg-green-900/10 border-green-500/30'
                      : 'bg-red-900/10 border-red-500/30 opacity-60'
                  }`}
                >
                  {/* Header de la proposition */}
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        p.confidence === 'élevé' ? 'bg-green-500/20 text-green-400' :
                        p.confidence === 'moyen' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {p.confidence}
                      </span>
                      <span className="text-gray-600 text-xs ml-2">{p.proposal_id}</span>
                    </div>
                    <span className={`text-xs ${
                      p.status === 'pending' ? 'text-yellow-400' :
                      p.status === 'approved' ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {p.status === 'pending' ? 'En attente' :
                       p.status === 'approved' ? 'Approuvé' : 'Rejeté'}
                    </span>
                  </div>

                  {/* Raison du déclenchement */}
                  <p className="text-yellow-400 text-sm font-medium mb-2">{p.trigger_reason}</p>

                  {/* Signaux observés */}
                  <div className="mb-3 pl-3 border-l-2 border-gray-700">
                    {(p.observed_signals || []).map((s, i) => (
                      <p key={i} className="text-gray-500 text-xs">• {s}</p>
                    ))}
                  </div>

                  {/* Proposition */}
                  <div className="bg-black/30 rounded-lg p-3 mb-3">
                    <p className="text-white text-sm mb-1"><strong>Problème:</strong> {p.problem}</p>
                    <p className="text-cyan-400 text-sm mb-1"><strong>Suggestion:</strong> {p.suggested_change}</p>
                    <p className="text-gray-400 text-xs"><strong>Effet attendu:</strong> {p.expected_effect}</p>
                  </div>

                  {/* Actions (seulement si pending) */}
                  {p.status === 'pending' && (
                    <div className="flex gap-2">
                      {activeProposal === p.proposal_id ? (
                        <div className="flex-1 space-y-2">
                          <textarea
                            value={rejectReason}
                            onChange={e => setRejectReason(e.target.value)}
                            placeholder="Raison du rejet (optionnel)"
                            className="w-full px-3 py-2 bg-black border border-red-500/30 rounded text-white text-sm placeholder-gray-600 resize-none h-16"
                          />
                          <div className="flex gap-2">
                            <button
                              onClick={() => setActiveProposal(null)}
                              className="flex-1 py-2 bg-gray-800 text-gray-300 rounded text-sm hover:bg-gray-700"
                            >
                              Annuler
                            </button>
                            <button
                              onClick={() => handleRespond(p.proposal_id, 'reject')}
                              className="flex-1 py-2 bg-red-600/20 text-red-400 rounded text-sm hover:bg-red-600/30"
                            >
                              Confirmer rejet
                            </button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <button
                            onClick={() => handleRespond(p.proposal_id, 'approve')}
                            className="flex-1 py-2 bg-green-600/20 text-green-400 rounded-lg text-sm hover:bg-green-600/30"
                          >
                            Approuver
                          </button>
                          <button
                            onClick={() => setActiveProposal(p.proposal_id)}
                            className="flex-1 py-2 bg-red-600/20 text-red-400 rounded-lg text-sm hover:bg-red-600/30"
                          >
                            Rejeter
                          </button>
                          <button className="px-3 py-2 bg-gray-800 text-gray-400 rounded-lg text-sm hover:bg-gray-700">
                            Discuter
                          </button>
                        </>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="p-3 border-t border-gray-800 bg-gray-950/50 text-center">
          <p className="text-gray-600 text-xs">
            Les agents observent, analysent, proposent — mais n'agissent jamais sans validation humaine
          </p>
        </div>
      </div>
    </div>
  );
};

// ===============================================================================
// PAGE PRINCIPALE: FOUNDER
// ===============================================================================

const FounderPage = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('vision');
  const [founders, setFounders] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAnchoring, setIsAnchoring] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showUXPanel, setShowUXPanel] = useState(false);

  // Agents adaptatifs
  const uxObserverRef = useRef(null);
  const feedbackAnalystRef = useRef(null);

  // Initialiser les agents
  useEffect(() => {
    uxObserverRef.current = new UXObserverAgent();
    feedbackAnalystRef.current = new FeedbackAnalystAgent();

    // Cleanup à la fin de session
    return () => {
      if (uxObserverRef.current) {
        uxObserverRef.current.endSession();
      }
    };
  }, []);

  // Tracker les changements d'onglet
  useEffect(() => {
    if (uxObserverRef.current) {
      uxObserverRef.current.enterSection(activeTab);
    }
  }, [activeTab]);

  // Load founders
  useEffect(() => {
    const fetch = async () => {
      if (!isSupabaseConfigured) {
        setFounders([
          { id: 1, full_name: 'Architecte', role: 'SOUVERAIN', is_active_creator: true },
          { id: 2, full_name: 'Temple_Gardien', role: 'FOUNDER' },
          { id: 3, full_name: 'Lumière_369', role: 'FOUNDER', youtube_channel_url: 'https://youtube.com/@example' }
        ]);
        setLoading(false);
        return;
      }
      try {
        const { data } = await supabase.from('profiles').select('*').order('created_at');
        setFounders(data || []);
        if (user?.id) {
          const found = data?.find(f => f.id === user.id);
          if (found) setCurrentUser(found);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetch();

    if (isSupabaseConfigured) {
      const sub = supabase.channel('founders').on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'profiles' }, (p) => {
        setFounders(prev => [...prev, p.new]);
      }).subscribe();
      return () => sub.unsubscribe();
    }
  }, [user]);

  // Anchor
  const handleAnchor = async (name) => {
    setIsAnchoring(true);
    try {
      if (!isSupabaseConfigured) {
        const nf = { id: Date.now(), full_name: name, role: 'FOUNDER' };
        setFounders(prev => [...prev, nf]);
        setCurrentUser(nf);
      } else {
        const { data } = await supabase.from('profiles').insert({
          full_name: name, role: 'FOUNDER', frequency: SACRED.I,
          origin_context: 'founder', migration_status: 'pending'
        }).select().single();
        if (data) setCurrentUser(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsAnchoring(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="text-5xl animate-pulse mb-4">🏛️</div>
          <p className="text-yellow-400">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/95 border-b border-gray-800">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔱</span>
            <div>
              <span className="text-yellow-400 font-bold">AT·OM</span>
              <span className="text-gray-500 text-sm ml-2">Founder</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {/* Bouton UX/Structure (admin only) */}
            {currentUser && ['SOUVERAIN', 'admin', 'architect'].includes(currentUser.role) && (
              <button
                onClick={() => setShowUXPanel(true)}
                className="p-2 text-gray-500 hover:text-yellow-400 hover:bg-gray-900 rounded-lg transition-colors"
                title="UX / Structure"
              >
                🏗️
              </button>
            )}
            {currentUser && (
              <button onClick={() => setShowProfile(true)} className="flex items-center gap-2 px-3 py-1.5 bg-gray-900 rounded-full hover:bg-gray-800">
                <div className="w-7 h-7 rounded-full bg-yellow-500/20 flex items-center justify-center overflow-hidden">
                  {currentUser.avatar_url ? <img src={currentUser.avatar_url} alt="" className="w-full h-full object-cover" /> : <span className="text-yellow-400 text-xs">{currentUser.full_name?.[0]}</span>}
                </div>
                <span className="text-sm text-gray-300 hidden sm:inline">{currentUser.full_name}</span>
              </button>
            )}
          </div>
        </div>

        {/* Onglets internes */}
        <InternalTabs activeTab={activeTab} onTabChange={setActiveTab} />
      </header>

      {/* Contenu (avec offset pour header fixe) */}
      <main className="pt-28">
        {activeTab === 'vision' && (
          <VisionTab founders={founders} currentUser={currentUser} onAnchor={handleAnchor} isAnchoring={isAnchoring} />
        )}
        {activeTab === 'reseau' && (
          <ReseauTab founders={founders} currentUser={currentUser} onProfileClick={() => setShowProfile(true)} />
        )}
        {activeTab === 'discussions' && (
          <DiscussionsTab currentUser={currentUser} />
        )}
        {activeTab === 'archives' && (
          <ArchivesTab founders={founders} />
        )}
        {activeTab === 'activite' && (
          <ActiviteTab founders={founders} />
        )}
      </main>

      {/* Footer */}
      <footer className="py-8 text-center border-t border-gray-900 mt-12">
        <p className="text-gray-700 text-sm">
          🔱 AT·OM • Phase I Founder • {SACRED.M} | {SACRED.P} | {SACRED.I} | {SACRED.Po}
        </p>
        <p className="text-gray-800 text-xs mt-2">Espace transitoire • Migration future vers sphères CHE-NU</p>
      </footer>

      {/* Profile Modal */}
      {showProfile && currentUser && (
        <ProfileModal user={currentUser} onUpdate={setCurrentUser} onClose={() => setShowProfile(false)} />
      )}

      {/* UX/Structure Panel (admin) */}
      <UXStructurePanel
        isOpen={showUXPanel}
        onClose={() => setShowUXPanel(false)}
        currentUser={currentUser}
      />
    </div>
  );
};

export default FounderPage;
