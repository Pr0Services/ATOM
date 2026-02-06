/**
 * ===============================================================================
 *
 *       ██████╗ ██████╗ ██╗██████╗     ██████╗ ███████╗███████╗
 *      ██╔════╝ ██╔══██╗██║██╔══██╗    ██╔══██╗██╔════╝██╔════╝
 *      ██║  ███╗██████╔╝██║██║  ██║    ██║  ██║█████╗  ███████╗
 *      ██║   ██║██╔══██╗██║██║  ██║    ██║  ██║██╔══╝  ╚════██║
 *      ╚██████╔╝██║  ██║██║██████╔╝    ██████╔╝███████╗███████║
 *       ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝     ╚═════╝ ╚══════╝╚══════╝
 *
 *                 🌍 GRILLE DES FONDATEURS 🌍
 *            Réseau Planétaire de Conscience AT·OM
 *                    Phase I - Pre-Load
 *
 * ===============================================================================
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import CommunityChat from '../components/CommunityChat';
import PrivateThreads from '../components/PrivateThreads';

// Sacred constants
const SACRED = {
  M: 44.4,
  P: 161.8,
  I: 369,
  Po: 1728
};

const TARGET_FOUNDERS = 144; // Objectif de fondateurs

// ===============================================================================
// COMPOSANT: PLANÈTE TOURNANTE AVEC POINTS
// ===============================================================================

const PlanetGrid = ({ founders, onFounderHover, hoveredFounder }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const rotationRef = useRef(0);

  // Générer des positions sphériques pour chaque fondateur
  const getFounderPositions = useCallback(() => {
    return founders.map((founder, index) => {
      // Distribution de Fibonacci pour une répartition uniforme sur la sphère
      const phi = Math.acos(1 - 2 * (index + 0.5) / Math.max(founders.length, 1));
      const theta = Math.PI * (1 + Math.sqrt(5)) * (index + 0.5);
      return {
        ...founder,
        phi,
        theta,
        x: Math.sin(phi) * Math.cos(theta),
        y: Math.sin(phi) * Math.sin(theta),
        z: Math.cos(phi)
      };
    });
  }, [founders]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.offsetWidth * 2;
    const height = canvas.height = canvas.offsetHeight * 2;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    const positions = getFounderPositions();

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Fond étoilé subtil
      for (let i = 0; i < 100; i++) {
        const x = (Math.sin(i * 127.1) * 0.5 + 0.5) * width;
        const y = (Math.cos(i * 311.7) * 0.5 + 0.5) * height;
        const alpha = 0.1 + Math.sin(Date.now() / 1000 + i) * 0.05;
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
        ctx.beginPath();
        ctx.arc(x, y, 1, 0, Math.PI * 2);
        ctx.fill();
      }

      // Grille sphérique (lignes de latitude/longitude)
      ctx.strokeStyle = 'rgba(212, 175, 55, 0.1)';
      ctx.lineWidth = 1;

      // Lignes de longitude
      for (let i = 0; i < 12; i++) {
        const angle = (i / 12) * Math.PI * 2 + rotationRef.current;
        ctx.beginPath();
        for (let j = 0; j <= 32; j++) {
          const phi = (j / 32) * Math.PI;
          const x = centerX + Math.sin(phi) * Math.cos(angle) * radius;
          const y = centerY + Math.cos(phi) * radius;
          if (j === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // Lignes de latitude
      for (let i = 1; i < 6; i++) {
        const phi = (i / 6) * Math.PI;
        const r = Math.sin(phi) * radius;
        const y = centerY + Math.cos(phi) * radius;
        ctx.beginPath();
        ctx.ellipse(centerX, y, r, r * 0.3, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Glow central de la planète
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
      gradient.addColorStop(0, 'rgba(30, 58, 138, 0.3)');
      gradient.addColorStop(0.5, 'rgba(30, 58, 138, 0.1)');
      gradient.addColorStop(1, 'rgba(30, 58, 138, 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fill();

      // Points des fondateurs
      positions.forEach((founder, index) => {
        const rotatedX = founder.x * Math.cos(rotationRef.current) - founder.y * Math.sin(rotationRef.current);
        const rotatedY = founder.x * Math.sin(rotationRef.current) + founder.y * Math.cos(rotationRef.current);
        const z = founder.z;

        // Ne dessiner que les points visibles (devant)
        if (z > -0.3) {
          const screenX = centerX + rotatedX * radius;
          const screenY = centerY + z * radius;
          const scale = (rotatedY + 1) / 2; // 0 à 1 basé sur la profondeur
          const pointRadius = 4 + scale * 6;
          const alpha = 0.4 + scale * 0.6;

          const isHovered = hoveredFounder?.id === founder.id;

          // Glow du point
          const pointGradient = ctx.createRadialGradient(
            screenX, screenY, 0,
            screenX, screenY, pointRadius * 3
          );
          pointGradient.addColorStop(0, isHovered ? 'rgba(255, 255, 255, 0.8)' : `rgba(212, 175, 55, ${alpha})`);
          pointGradient.addColorStop(0.5, isHovered ? 'rgba(212, 175, 55, 0.4)' : `rgba(212, 175, 55, ${alpha * 0.3})`);
          pointGradient.addColorStop(1, 'rgba(212, 175, 55, 0)');

          ctx.fillStyle = pointGradient;
          ctx.beginPath();
          ctx.arc(screenX, screenY, pointRadius * 3, 0, Math.PI * 2);
          ctx.fill();

          // Point central
          ctx.fillStyle = isHovered ? '#FFFFFF' : '#D4AF37';
          ctx.beginPath();
          ctx.arc(screenX, screenY, pointRadius, 0, Math.PI * 2);
          ctx.fill();

          // Stocker la position pour la détection de hover
          founder.screenX = screenX / 2;
          founder.screenY = screenY / 2;
          founder.screenRadius = pointRadius * 2;
        }
      });

      rotationRef.current += 0.002;
      animationRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [founders, getFounderPositions, hoveredFounder]);

  // Détection du hover sur les points
  const handleMouseMove = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const positions = getFounderPositions();
    let found = null;

    for (const founder of positions) {
      if (founder.screenX && founder.screenY) {
        const dist = Math.sqrt(
          Math.pow(x - founder.screenX, 2) +
          Math.pow(y - founder.screenY, 2)
        );
        if (dist < founder.screenRadius + 10) {
          found = founder;
          break;
        }
      }
    }

    onFounderHover(found);
  };

  return (
    <div className="relative w-full aspect-square max-w-xl mx-auto">
      <canvas
        ref={canvasRef}
        className="w-full h-full cursor-crosshair"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => onFounderHover(null)}
      />

      {/* Tooltip du fondateur survolé */}
      {hoveredFounder && (
        <div
          className="absolute pointer-events-none bg-black/90 border border-yellow-500/50 rounded-lg p-3 transform -translate-x-1/2"
          style={{
            left: hoveredFounder.screenX,
            top: hoveredFounder.screenY - 80
          }}
        >
          <p className="text-yellow-400 font-bold text-sm">{hoveredFounder.full_name || 'Fondateur'}</p>
          <p className="text-gray-400 text-xs font-mono mt-1">
            {SACRED.M} | {SACRED.P} | {SACRED.I} | {SACRED.Po}
          </p>
          {hoveredFounder.hedera_account_id && (
            <p className="text-purple-400 text-xs mt-1">{hoveredFounder.hedera_account_id}</p>
          )}
        </div>
      )}
    </div>
  );
};

// ===============================================================================
// COMPOSANT: BARRE DE PROGRESSION DE LA GRILLE
// ===============================================================================

const GridProgress = ({ current, target }) => {
  const percentage = Math.min((current / target) * 100, 100);

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="flex justify-between items-center mb-2">
        <span className="text-gray-400 text-sm">GRID RESONANCE</span>
        <span className="text-yellow-400 font-bold">{current} / {target} FOUNDERS ACTIVATED</span>
      </div>
      <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 transition-all duration-1000"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-center text-gray-500 text-xs mt-2">
        {percentage < 100
          ? `${Math.ceil(target - current)} nodes remaining for full activation`
          : 'GRID FULLY ACTIVATED'
        }
      </p>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: CARTE D'UN FONDATEUR
// ===============================================================================

const FounderCard = ({ founder }) => (
  <div className="bg-gray-900/50 border border-cyan-500/30 rounded-xl p-4 hover:border-cyan-400/50 transition-all">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500/30 to-blue-600/30 flex items-center justify-center border border-cyan-500/30">
        <span className="text-cyan-400 text-sm">
          {(founder.full_name || 'F')[0].toUpperCase()}
        </span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-white font-medium truncate">{founder.full_name || 'Fondateur Anonyme'}</p>
        <p className="text-gray-500 text-xs">{founder.role || 'FOUNDER'}</p>
      </div>
    </div>
    <div className="mt-3 flex justify-between text-xs">
      <span className="text-yellow-400">{SACRED.M}</span>
      <span className="text-emerald-400">{SACRED.P}</span>
      <span className="text-blue-400">{SACRED.I}</span>
      <span className="text-purple-400">{SACRED.Po}</span>
    </div>
  </div>
);

// ===============================================================================
// COMPOSANT: FORMULAIRE D'ANCRAGE
// ===============================================================================

const AnchorForm = ({ onAnchor, isLoading }) => {
  const [name, setName] = useState('');
  const [intention, setIntention] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      onAnchor(name.trim(), intention.trim());
    }
  };

  return (
    <div className="bg-gradient-to-b from-gray-900/80 to-black border border-yellow-600/30 rounded-2xl p-6 max-w-md mx-auto">
      <div className="text-center mb-6">
        <span className="text-4xl">🔱</span>
        <h3 className="text-xl font-bold text-yellow-400 mt-2">S'ancrer au Réseau</h3>
        <p className="text-gray-500 text-sm mt-2">
          Devenez un Noeud Fondateur du réseau AT·OM
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-400 text-sm mb-2">Nom / Alias</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Votre nom dans le réseau"
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
            maxLength={50}
            required
          />
        </div>

        <div>
          <label className="block text-gray-400 text-sm mb-2">Intention (optionnel)</label>
          <textarea
            value={intention}
            onChange={(e) => setIntention(e.target.value)}
            placeholder="Pourquoi rejoignez-vous ce réseau?"
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50 resize-none h-20"
            maxLength={200}
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !name.trim()}
          className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
            isLoading || !name.trim()
              ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400'
          }`}
        >
          {isLoading ? 'Ancrage en cours...' : 'Rejoindre la Grille'}
        </button>
      </form>

      <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
        <p className="text-blue-400 text-xs text-center">
          En rejoignant, vous recevez votre <strong>Signature Fréquentielle</strong>
          <br />
          <span className="font-mono">M={SACRED.M} | P={SACRED.P} | I={SACRED.I} | Po={SACRED.Po}</span>
        </p>
      </div>
    </div>
  );
};

// ===============================================================================
// COMPOSANT: CONFIRMATION D'ANCRAGE
// ===============================================================================

const AnchorConfirmation = ({ founder }) => (
  <div className="bg-gradient-to-b from-gray-900/80 to-black border border-emerald-500/30 rounded-2xl p-8 max-w-md mx-auto text-center">
    <div className="text-6xl mb-4">✨</div>
    <h3 className="text-2xl font-bold text-emerald-400">Bienvenue, {founder.full_name}</h3>
    <p className="text-gray-400 mt-2">Vous êtes maintenant ancré au réseau AT·OM</p>

    <div className="mt-6 p-4 bg-black/50 rounded-xl border border-yellow-600/30">
      <p className="text-gray-500 text-sm mb-3">Votre Signature Fréquentielle</p>
      <div className="grid grid-cols-4 gap-2">
        <div className="text-center">
          <p className="text-yellow-400 text-2xl font-bold">{SACRED.M}</p>
          <p className="text-gray-600 text-xs">M</p>
        </div>
        <div className="text-center">
          <p className="text-emerald-400 text-2xl font-bold">{SACRED.P}</p>
          <p className="text-gray-600 text-xs">P</p>
        </div>
        <div className="text-center">
          <p className="text-blue-400 text-2xl font-bold">{SACRED.I}</p>
          <p className="text-gray-600 text-xs">I</p>
        </div>
        <div className="text-center">
          <p className="text-purple-400 text-2xl font-bold">{SACRED.Po}</p>
          <p className="text-gray-600 text-xs">Po</p>
        </div>
      </div>
    </div>

    <p className="text-gray-500 text-sm mt-6">
      La Grille se renforce avec chaque nouveau fondateur.
      <br />
      Partagez le lien avec votre Famille de Lumière.
    </p>
  </div>
);

// ===============================================================================
// PAGE PRINCIPALE: GRILLE DES FONDATEURS
// ===============================================================================

const GridPage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [founders, setFounders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hoveredFounder, setHoveredFounder] = useState(null);
  const [isAnchoring, setIsAnchoring] = useState(false);
  const [anchoredFounder, setAnchoredFounder] = useState(null);
  const [showChat, setShowChat] = useState(false);

  // Charger les fondateurs depuis Supabase
  useEffect(() => {
    const fetchFounders = async () => {
      if (!isSupabaseConfigured) {
        // Données de démonstration
        setFounders([
          { id: 1, full_name: 'Temple_Gardien', role: 'SOUVERAIN' },
          { id: 2, full_name: 'Amélie_Souveraine', role: 'FOUNDER' },
          { id: 3, full_name: 'Temple_Gardien', role: 'FOUNDER' },
        ]);
        setLoading(false);
        return;
      }

      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('id, full_name, role, hedera_account_id, created_at')
          .order('created_at', { ascending: true });

        if (error) throw error;
        setFounders(data || []);
      } catch (err) {
        console.error('[GRID] Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFounders();

    // Écouter les nouveaux fondateurs en temps réel
    if (isSupabaseConfigured) {
      const subscription = supabase
        .channel('founders')
        .on('postgres_changes', {
          event: 'INSERT',
          schema: 'public',
          table: 'profiles'
        }, (payload) => {
          setFounders(prev => [...prev, payload.new]);
        })
        .subscribe();

      return () => subscription.unsubscribe();
    }
  }, []);

  // Ancrer un nouveau fondateur
  const handleAnchor = async (name, intention) => {
    setIsAnchoring(true);

    try {
      if (!isSupabaseConfigured) {
        // Mode démo
        const newFounder = {
          id: Date.now(),
          full_name: name,
          role: 'FOUNDER',
          intention
        };
        setFounders(prev => [...prev, newFounder]);
        setAnchoredFounder(newFounder);
        setIsAnchoring(false);
        return;
      }

      // Créer le profil dans Supabase
      const { data, error } = await supabase
        .from('profiles')
        .insert({
          full_name: name,
          role: 'FOUNDER',
          frequency: SACRED.I,
          metadata: { intention, anchored_at: new Date().toISOString() }
        })
        .select()
        .single();

      if (error) throw error;

      setAnchoredFounder(data);
    } catch (err) {
      console.error('[ANCHOR] Erreur:', err);
      alert('Erreur lors de l\'ancrage. Veuillez réessayer.');
    } finally {
      setIsAnchoring(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl animate-pulse mb-4">🌍</div>
          <p className="text-yellow-400">Chargement de la Grille...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔱</span>
            <div>
              <h1 className="text-lg font-bold text-yellow-400">AT·OM</h1>
              <p className="text-xs text-gray-500">Phase I - Pre-Load Complete</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700 transition-colors"
            >
              💬 Community Chat
            </button>
            {isAuthenticated && (
              <button
                onClick={() => navigate('/tableau-de-bord')}
                className="px-4 py-2 bg-yellow-600/20 text-yellow-400 rounded-lg text-sm hover:bg-yellow-600/30 transition-colors"
              >
                Bureau →
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 pb-8 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Progress Bar */}
          <div className="mb-8">
            <GridProgress current={founders.length} target={TARGET_FOUNDERS} />
          </div>

          {/* Layout principal */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Colonne gauche - Chat ou Formulaire */}
            <div className="lg:col-span-1">
              {showChat ? (
                <div className="h-96">
                  <CommunityChat onClose={() => setShowChat(false)} />
                </div>
              ) : anchoredFounder ? (
                <AnchorConfirmation founder={anchoredFounder} />
              ) : (
                <AnchorForm onAnchor={handleAnchor} isLoading={isAnchoring} />
              )}
            </div>

            {/* Colonne centrale - Planète */}
            <div className="lg:col-span-1">
              <PlanetGrid
                founders={founders}
                onFounderHover={setHoveredFounder}
                hoveredFounder={hoveredFounder}
              />
            </div>

            {/* Colonne droite - Liste des threads/fondateurs */}
            <div className="lg:col-span-1">
              <div className="bg-gray-900/50 rounded-xl border border-gray-800 p-4">
                <h3 className="text-white font-medium mb-4 flex items-center gap-2">
                  <span>👥</span> PRIVATE THREADS
                </h3>

                <div className="mb-6">
                  <PrivateThreads compact={true} />
                </div>

                <div className="border-t border-gray-800 pt-4">
                  <h4 className="text-gray-400 text-sm mb-3">Noeuds Fondateurs ({founders.length})</h4>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {founders.slice(0, 10).map((founder) => (
                      <FounderCard key={founder.id} founder={founder} />
                    ))}
                    {founders.length > 10 && (
                      <p className="text-gray-500 text-xs text-center py-2">
                        + {founders.length - 10} autres fondateurs
                      </p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Message de la Phase */}
          <div className="mt-12 max-w-2xl mx-auto text-center">
            <p className="text-gray-500 text-sm leading-relaxed">
              Le plein potentiel de la plateforme AT·OM nécessite une masse critique de conscience.
              En vous ancrant aujourd'hui, vous devenez un <span className="text-yellow-400">Noeud Fondateur</span>.
              Dès que la Grille atteindra sa résonance optimale ({TARGET_FOUNDERS} membres),
              les modules de transmutation et l'interface HD seront activés pour tous.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-4 right-4">
        <span className="text-gray-800 text-sm">✧</span>
      </footer>
    </div>
  );
};

export default GridPage;
