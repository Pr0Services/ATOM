/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗ ██████╗  ██████╗  ██████╗ ██████╗ ███████╗███████╗ ██████╗
 *      ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔════╝██╔════╝██╔═══██╗
 *      ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝█████╗  ███████╗██║   ██║
 *      ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══╝  ╚════██║██║   ██║
 *      ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████╗███████║╚██████╔╝
 *      ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝
 *
 *                         🔱 AT·OM - LANDING PAGE PROGRESO 2026 🔱
 *                              "La technologie retrouve son âme"
 *
 *   SYSTÈME DE SOUVERAINETÉ MONDIALE - 9 SPHÈRES - 7 LOIS UNIVERSELLES
 *
 *   3 LISTES DE PRÉ-INSCRIPTION SÉPARÉES:
 *   - CITOYENS: Prêts à joindre et partager la vision (souverains de leurs données)
 *   - FONDATEURS: Talents pour construire/développer avant le lancement (NFT Graine offert)
 *   - INVESTISSEURS: Fonds via Flow Keeper + Jetons de Transition (JT → UR)
 *
 *   SECTIONS:
 *   - Hero: Vision principale + 3 CTAs
 *   - Momentum Bar: Progression live Phase I
 *   - Vision: Ce que nous construisons
 *   - 9 Sphères: JE (1-3) / NOUS (4-6) / L'ARCHE (7-9)
 *   - 7 Lois Universelles: Principes fondateurs
 *   - Moteur Vivant: Ce que le système fait pour vous
 *   - Connexions: Comment tout est relié
 *   - 6 Facettes: Angles de perception
 *   - Flow Keeper: Contribution consciente
 *   - Participation & Reconnaissance: 5 niveaux NFT
 *   - AT·OM$ Valeur en temps réel
 *   - Choisissez votre rôle: Transition vers les formulaires
 *   - 3 Formulaires: Citoyen / Fondateur / Investisseur
 *   - FAQ enrichie
 *   - Footer
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useRef } from 'react';
import { supabase } from '../lib/supabase';
import { useTokenomics } from '../hooks/useTokenomics';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const WAITLIST_TYPES = {
  CITIZEN: 'citizen',
  FOUNDER: 'founder',
  INVESTOR: 'investor'
};

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: 9 SPHÈRES
// ═══════════════════════════════════════════════════════════════════════════════

const SPHERES = {
  JE: [
    { num: 1, name: 'IDENTITÉ', icon: '👤', desc: 'Votre profil souverain, vos données vous appartiennent' },
    { num: 2, name: 'SANTÉ', icon: '💚', desc: 'Bien-être physique, mental, spirituel intégré' },
    { num: 3, name: 'SAVOIR', icon: '📚', desc: 'Accès à la connaissance purifiée et vérifiée' }
  ],
  NOUS: [
    { num: 4, name: 'ÉCONOMIE', icon: '💰', desc: 'L\'Unité de Résonance (UR) — monnaie stable et équitable' },
    { num: 5, name: 'GOUVERNANCE', icon: '⚖️', desc: 'Démocratie directe, transparence totale, sans chef' },
    { num: 6, name: 'ÉDUCATION', icon: '🎓', desc: 'Transmission intergénérationnelle des sagesses' }
  ],
  ARCHE: [
    { num: 7, name: 'INTELLIGENCE', icon: '🤖', desc: 'IA au service de l\'humain, jamais l\'inverse' },
    { num: 8, name: 'INFRASTRUCTURE', icon: '🏗️', desc: 'Technologie éthique, décentralisée, souveraine' },
    { num: 9, name: 'ÉQUILIBRE', icon: '☯️', desc: 'Harmonie planétaire, régénération, cycles naturels' }
  ]
};

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: 7 LOIS UNIVERSELLES
// ═══════════════════════════════════════════════════════════════════════════════

const LOIS_UNIVERSELLES = [
  { num: 1, name: 'Mentalisme', principe: 'Tout est esprit' },
  { num: 2, name: 'Correspondance', principe: 'Ce qui est en haut est en bas' },
  { num: 3, name: 'Vibration', principe: 'Tout vibre' },
  { num: 4, name: 'Polarité', principe: 'Tout a deux pôles' },
  { num: 5, name: 'Rythme', principe: 'Tout flux et reflux' },
  { num: 6, name: 'Cause & Effet', principe: 'Toute cause a son effet' },
  { num: 7, name: 'Genre', principe: 'Équilibre action et réception' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: 6 FACETTES DU DIAMANT
// ═══════════════════════════════════════════════════════════════════════════════

const FACETTES = [
  { icon: '💻', name: 'Technologique', desc: 'Une infrastructure qui protège vos données et sert l\'humain' },
  { icon: '🏛️', name: 'Politique', desc: 'Chaque personne est souveraine de ses choix et de sa voix' },
  { icon: '⚖️', name: 'Gouvernementale', desc: 'Des services publics transparents, gérés par ceux qui les utilisent' },
  { icon: '📖', name: 'Sagesse', desc: 'Les connaissances de l\'humanité, accessibles et unifiées' },
  { icon: '🧘', name: 'Spirituelle', desc: 'L\'alignement entre ce que vous êtes et ce que vous faites' },
  { icon: '📜', name: 'Historique', desc: 'Une mémoire collective qui ne peut être altérée' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: TIERS NFT
// ═══════════════════════════════════════════════════════════════════════════════

const NFT_TIERS = [
  { name: 'GRAINE', symbol: '🌰', max: null },
  { name: 'POUSSE', symbol: '🌱', max: 1000 },
  { name: 'BRANCHE', symbol: '🌿', max: 144 },
  { name: 'RACINE', symbol: '🌳', max: 36 },
  { name: 'ARBRE', symbol: '🌲', max: 9 }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: FLOW KEEPER (6 TYPES DE FLUX)
// ═══════════════════════════════════════════════════════════════════════════════

const FLOW_TYPES = [
  { name: 'TECH', icon: '💻', desc: 'Infrastructure, développement, innovation' },
  { name: 'VIE', icon: '🌱', desc: 'Santé, alimentation, bien-être' },
  { name: 'SAGESSE', icon: '📚', desc: 'Éducation, recherche, transmission' },
  { name: 'JUSTICE', icon: '⚖️', desc: 'Médiation, gouvernance, équité' },
  { name: 'GRAINE', icon: '🌰', desc: 'Nouveaux projets, entrepreneurs' },
  { name: 'TERRE', icon: '🌍', desc: 'Environnement, régénération' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES: FAQ
// ═══════════════════════════════════════════════════════════════════════════════

const FAQS = [
  {
    q: 'C\'est une crypto?',
    a: 'Non. L\'Unité de Résonance (UR) est une monnaie interne stable, pas spéculative. Elle ne fluctue pas comme Bitcoin. Sa valeur est ancrée dans la contribution réelle à la communauté.'
  },
  {
    q: 'C\'est une secte?',
    a: 'Non. AT-OM est une infrastructure technologique, pas une croyance. Vous pouvez partir quand vous voulez, avec toutes vos données. Aucun gourou, aucune hiérarchie pyramidale.'
  },
  {
    q: 'C\'est légal?',
    a: 'Oui. Structure coopérative internationale, respect des lois locales, transparence totale. Chaque transaction est traçable sur Hedera Hashgraph, blockchain certifiée conforme.'
  },
  {
    q: 'Qu\'est-ce que Hedera Hashgraph?',
    a: 'Une technologie de registre distribué (DLT) utilisée par Google, IBM, Boeing. Plus rapide et écologique que Bitcoin. Nous l\'utilisons pour garantir l\'immutabilité de vos données et contributions.'
  },
  {
    q: 'Comment mes données sont protégées?',
    a: 'Vos données sont chiffrées, stockées de manière décentralisée, et vous en restez propriétaire. Vous pouvez les exporter ou les supprimer à tout moment. Aucune vente à des tiers.'
  },
  {
    q: 'Comment fonctionne la gouvernance?',
    a: 'Démocratie directe: chaque citoyen peut proposer et voter. Pas de représentants, pas de politiciens. Les décisions sont exécutées automatiquement par smart contracts.'
  },
  {
    q: 'Puis-je récupérer mon investissement?',
    a: 'Les Jetons de Transition (JT) sont convertibles en UR au lancement. L\'UR peut être utilisée dans l\'écosystème ou échangée selon les mécanismes de la coopérative. Ce n\'est pas un investissement spéculatif.'
  },
  {
    q: 'Où en êtes-vous?',
    a: 'Phase I en cours. L\'architecture est en place, les 9 Sphères sont définies, et nous recrutons les premiers fondateurs pour la Phase II. Inscrivez-vous pour suivre l\'avancement.'
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HERO SECTION
// ═══════════════════════════════════════════════════════════════════════════════

const HeroSection = ({ onScrollToCitizen, onScrollToFounder, onScrollToInvestor }) => (
  <section className="min-h-screen flex flex-col items-center justify-center relative px-4 py-20">
    <div className="absolute inset-0 bg-gradient-to-b from-yellow-900/20 via-black to-black" />

    <div className="relative z-10 text-center max-w-3xl mx-auto">
      <div className="text-6xl mb-6">🔱</div>

      <h1 className="text-4xl md:text-5xl font-bold text-yellow-500 mb-4 tracking-wider">
        AT·OM
      </h1>

      <p className="text-xl text-white/80 mb-2">
        Système de Souveraineté Mondiale
      </p>

      <p className="text-lg text-yellow-400/60 italic mb-6">
        "La technologie retrouve son âme."
      </p>

      {/* 3 Promesses */}
      <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-6 mb-8">
        <div className="grid md:grid-cols-3 gap-4 text-left">
          <div className="flex items-start gap-2">
            <span className="text-emerald-400">✓</span>
            <p className="text-white/90">Vos <span className="text-yellow-400 font-semibold">données</span> vous appartiennent</p>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-400">✓</span>
            <p className="text-white/90">Votre <span className="text-yellow-400 font-semibold">temps</span> n'est plus à vendre</p>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-400">✓</span>
            <p className="text-white/90">Votre <span className="text-yellow-400 font-semibold">contribution</span> est valorisée</p>
          </div>
        </div>
      </div>

      {/* Statistiques clés */}
      <div className="grid grid-cols-3 gap-4 mb-8 text-center">
        <div>
          <p className="text-3xl font-bold text-yellow-400">9</p>
          <p className="text-gray-500 text-sm">Sphères</p>
        </div>
        <div>
          <p className="text-3xl font-bold text-yellow-400">7</p>
          <p className="text-gray-500 text-sm">Lois Universelles</p>
        </div>
        <div>
          <p className="text-3xl font-bold text-yellow-400">∞</p>
          <p className="text-gray-500 text-sm">Souveraineté</p>
        </div>
      </div>

      {/* 3 CTAs */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={onScrollToCitizen}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition-all"
        >
          <span aria-hidden="true">👤 </span>Devenir Citoyen
        </button>
        <button
          onClick={onScrollToFounder}
          className="px-6 py-3 bg-yellow-600 hover:bg-yellow-500 text-black font-semibold rounded-lg transition-all"
        >
          <span aria-hidden="true">⚡ </span>Devenir Fondateur
        </button>
        <button
          onClick={onScrollToInvestor}
          className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg transition-all"
        >
          <span aria-hidden="true">💎 </span>Devenir Investisseur
        </button>
      </div>

      <div className="mt-12 animate-bounce text-yellow-500/50 motion-reduce:animate-none" aria-hidden="true">
        <span className="text-2xl">↓</span>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: VISION SECTION
// ═══════════════════════════════════════════════════════════════════════════════

const VisionSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-yellow-900/10" aria-labelledby="section-vision">
    <div className="max-w-4xl mx-auto">
      <h2 id="section-vision" className="text-3xl font-bold text-center text-white mb-4">
        Ce que nous construisons
      </h2>
      <p className="text-gray-400 text-center mb-12">
        Un environnement souverain qui change votre rapport au monde
      </p>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl mb-4">🏛️</div>
          <h3 className="text-xl font-semibold text-white mb-2">Un Refuge Numérique</h3>
          <p className="text-gray-400">Où vos données vous appartiennent. Où votre temps n'est plus à vendre.</p>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl mb-4">🔄</div>
          <h3 className="text-xl font-semibold text-white mb-2">Fin des Cycles</h3>
          <p className="text-gray-400">L'humanité répète les mêmes erreurs. L'Arche brise ce cercle vicieux.</p>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl mb-4">🌱</div>
          <h3 className="text-xl font-semibold text-white mb-2">L'Épanouissement</h3>
          <p className="text-gray-400">De la compétition à la coopération. Votre croissance devient la priorité.</p>
        </div>
      </div>

      {/* Comparison */}
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-red-900/10 border border-red-500/20 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-red-400 mb-4 text-center">AUJOURD'HUI</h3>
          <ul className="space-y-3 text-gray-400">
            <li>→ Données dispersées sur 100 plateformes</li>
            <li>→ Temps vendu aux annonceurs</li>
            <li>→ Seul face aux corporations</li>
            <li>→ Cycles répétitifs sans fin</li>
          </ul>
        </div>

        <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-yellow-400 mb-4 text-center">DANS L'ARCHE</h3>
          <ul className="space-y-3 text-yellow-200/80">
            <li>✓ Un profil souverain que VOUS contrôlez</li>
            <li>✓ Temps investi dans votre épanouissement</li>
            <li>✓ Communauté de bâtisseurs engagés</li>
            <li>✓ Économie qui circule et récompense</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LES 9 SPHÈRES
// ═══════════════════════════════════════════════════════════════════════════════

const SpheresSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-purple-900/10" aria-labelledby="section-spheres">
    <div className="max-w-5xl mx-auto">
      <h2 id="section-spheres" className="text-3xl font-bold text-center text-white mb-4">
        Les 9 Sphères de l'Arche
      </h2>
      <p className="text-gray-500 text-center mb-12 max-w-2xl mx-auto">
        Chaque sphère gère un aspect essentiel de votre vie souveraine — de l'identité individuelle à l'équilibre planétaire.
      </p>

      {/* JE - Sphères 1-3 */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold">JE</div>
          <h3 className="text-xl font-semibold text-blue-400">Sphères Individuelles (1-3)</h3>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {SPHERES.JE.map((s) => (
            <div key={s.num} className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-3xl">{s.icon}</span>
                <span className="text-blue-400 font-mono text-sm">Sphère {s.num}</span>
              </div>
              <h4 className="text-white font-semibold mb-2">{s.num}. {s.name}</h4>
              <p className="text-gray-400 text-sm">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* NOUS - Sphères 4-6 */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-yellow-600 flex items-center justify-center text-sm font-bold text-black">NOUS</div>
          <h3 className="text-xl font-semibold text-yellow-400">Sphères Collectives (4-6)</h3>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {SPHERES.NOUS.map((s) => (
            <div key={s.num} className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-3xl">{s.icon}</span>
                <span className="text-yellow-400 font-mono text-sm">Sphère {s.num}</span>
              </div>
              <h4 className="text-white font-semibold mb-2">{s.num}. {s.name}</h4>
              <p className="text-gray-400 text-sm">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* L'ARCHE - Sphères 7-9 */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-sm font-bold">∞</div>
          <h3 className="text-xl font-semibold text-purple-400">Sphères Systémiques (7-9)</h3>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {SPHERES.ARCHE.map((s) => (
            <div key={s.num} className="bg-purple-900/20 border border-purple-500/30 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-3xl">{s.icon}</span>
                <span className="text-purple-400 font-mono text-sm">Sphère {s.num}</span>
              </div>
              <h4 className="text-white font-semibold mb-2">{s.num}. {s.name}</h4>
              <p className="text-gray-400 text-sm">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: 7 LOIS UNIVERSELLES — Principes fondateurs (concis)
// ═══════════════════════════════════════════════════════════════════════════════

const LoisSection = () => (
  <section className="py-12 px-4 bg-black" aria-labelledby="section-lois">
    <div className="max-w-4xl mx-auto">
      <h2 id="section-lois" className="text-2xl font-bold text-center text-white mb-3">
        7 Lois Universelles
      </h2>
      <p className="text-gray-500 text-center mb-8 text-sm">
        Les principes qui gouvernent l'architecture du système
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        {LOIS_UNIVERSELLES.map((loi) => (
          <div key={loi.num} className="flex items-center gap-2 px-4 py-2 bg-gray-900/50 border border-yellow-500/10 rounded-full hover:border-yellow-500/30 transition-all">
            <span className="text-yellow-400 font-mono text-xs">{loi.num}</span>
            <span className="text-white text-sm font-medium">{loi.name}</span>
            <span className="text-gray-600 text-xs hidden sm:inline">— {loi.principe}</span>
          </div>
        ))}
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LE MOTEUR VIVANT — Ce que le système fait pour VOUS
// ═══════════════════════════════════════════════════════════════════════════════

const MoteurVivantSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-emerald-900/10" aria-labelledby="section-moteur">
    <div className="max-w-5xl mx-auto">
      <h2 id="section-moteur" className="text-3xl font-bold text-center text-white mb-4">
        Un système qui s'adapte à vous
      </h2>
      <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
        AT·OM n'est pas un outil de plus. C'est un environnement vivant qui apprend,
        s'harmonise et évolue avec chaque personne qui y entre.
      </p>

      {/* Les 4 effets concrets */}
      <div className="grid md:grid-cols-2 gap-6 mb-12">
        {/* 1. Il vous connaît */}
        <div className="bg-gray-900/50 border border-emerald-500/20 rounded-xl p-6 hover:border-emerald-500/40 transition-all">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-2xl">🫀</div>
            <h3 className="text-xl font-semibold text-emerald-400">Il s'adapte à vous</h3>
          </div>
          <p className="text-gray-300 mb-3">
            Dès votre entrée, le système analyse votre profil et crée un environnement
            personnalisé. Pas de taille unique — chaque interface, chaque suggestion,
            chaque connexion est calibrée pour <span className="text-emerald-400">votre</span> situation.
          </p>
          <p className="text-gray-500 text-sm">
            Ce que ça change : vous ne perdez plus de temps dans du bruit. Tout ce que vous voyez est pertinent pour vous.
          </p>
        </div>

        {/* 2. Il connecte */}
        <div className="bg-gray-900/50 border border-cyan-500/20 rounded-xl p-6 hover:border-cyan-500/40 transition-all">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-cyan-500/20 flex items-center justify-center text-2xl">🔗</div>
            <h3 className="text-xl font-semibold text-cyan-400">Il connecte tout</h3>
          </div>
          <p className="text-gray-300 mb-3">
            Vos besoins personnels sont reliés aux besoins de votre communauté locale.
            Ce que vous cherchez peut déjà être offert par quelqu'un près de chez vous.
            Le système fait le pont automatiquement.
          </p>
          <p className="text-gray-500 text-sm">
            Ce que ça change : les problèmes locaux trouvent des solutions locales, sans bureaucratie.
          </p>
        </div>

        {/* 3. Il harmonise */}
        <div className="bg-gray-900/50 border border-purple-500/20 rounded-xl p-6 hover:border-purple-500/40 transition-all">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center text-2xl">🌊</div>
            <h3 className="text-xl font-semibold text-purple-400">Il harmonise les flux</h3>
          </div>
          <p className="text-gray-300 mb-3">
            Le moteur d'harmonisation analyse en continu l'équilibre entre ce qui est donné
            et ce qui est reçu — à l'échelle individuelle, communautaire et planétaire.
            Quand un déséquilibre apparaît, le système ajuste les priorités.
          </p>
          <p className="text-gray-500 text-sm">
            Ce que ça change : les ressources vont naturellement là où elles sont les plus nécessaires.
          </p>
        </div>

        {/* 4. Il grandit avec vous */}
        <div className="bg-gray-900/50 border border-yellow-500/20 rounded-xl p-6 hover:border-yellow-500/40 transition-all">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-yellow-500/20 flex items-center justify-center text-2xl">🌱</div>
            <h3 className="text-xl font-semibold text-yellow-400">Il grandit avec vous</h3>
          </div>
          <p className="text-gray-300 mb-3">
            Plus vous contribuez, plus le système vous ouvre de possibilités.
            Pas par restriction — par expansion naturelle. Comme un arbre qui
            développe de nouvelles branches à mesure qu'il grandit.
          </p>
          <p className="text-gray-500 text-sm">
            Ce que ça change : votre engagement est reconnu et amplifié, pas exploité.
          </p>
        </div>
      </div>

      {/* La boucle */}
      <div className="bg-gradient-to-r from-emerald-900/20 via-yellow-900/20 to-purple-900/20 border border-yellow-500/20 rounded-xl p-8 text-center">
        <h3 className="text-xl font-semibold text-white mb-4">La boucle vertueuse</h3>
        <div className="flex flex-wrap items-center justify-center gap-3 text-lg mb-4">
          <span className="px-4 py-2 bg-emerald-900/30 rounded-lg text-emerald-400">Vous contribuez</span>
          <span className="text-yellow-400">→</span>
          <span className="px-4 py-2 bg-cyan-900/30 rounded-lg text-cyan-400">Le système s'adapte</span>
          <span className="text-yellow-400">→</span>
          <span className="px-4 py-2 bg-purple-900/30 rounded-lg text-purple-400">Votre communauté grandit</span>
          <span className="text-yellow-400">→</span>
          <span className="px-4 py-2 bg-yellow-900/30 rounded-lg text-yellow-400">Vous en bénéficiez</span>
        </div>
        <p className="text-gray-500 text-sm max-w-lg mx-auto">
          Pas de hiérarchie pyramidale. Pas de PDG qui profite pendant que vous travaillez.
          L'énergie que vous mettez dans le système revient vers vous — amplifiée.
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LES CONNEXIONS — Comment tout est relié
// ═══════════════════════════════════════════════════════════════════════════════

const ConnexionsSection = () => (
  <section className="py-20 px-4 bg-black" aria-labelledby="section-connexions">
    <div className="max-w-5xl mx-auto">
      <h2 id="section-connexions" className="text-3xl font-bold text-center text-white mb-4">
        Tout est connecté
      </h2>
      <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
        Dans le monde actuel, chaque aspect de votre vie est géré par une application différente
        qui ne parle pas aux autres. AT·OM unifie tout en un seul environnement cohérent.
      </p>

      {/* Exemple de connexion concrète */}
      <div className="space-y-6 mb-12">
        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
          <h3 className="text-yellow-400 font-semibold mb-3">Exemple : Un besoin dans votre quartier</h3>
          <div className="grid md:grid-cols-4 gap-4 text-sm">
            <div className="bg-blue-900/20 border border-blue-500/20 rounded-lg p-3 text-center">
              <p className="text-blue-400 font-semibold mb-1">1. Vous identifiez</p>
              <p className="text-gray-400">Un parc a besoin d'entretien dans votre quartier</p>
            </div>
            <div className="bg-yellow-900/20 border border-yellow-500/20 rounded-lg p-3 text-center">
              <p className="text-yellow-400 font-semibold mb-1">2. Le système relie</p>
              <p className="text-gray-400">Des bénévoles et des entreprises locales sont identifiés</p>
            </div>
            <div className="bg-emerald-900/20 border border-emerald-500/20 rounded-lg p-3 text-center">
              <p className="text-emerald-400 font-semibold mb-1">3. L'action se forme</p>
              <p className="text-gray-400">Les contributeurs coordonnent via l'espace commun</p>
            </div>
            <div className="bg-purple-900/20 border border-purple-500/20 rounded-lg p-3 text-center">
              <p className="text-purple-400 font-semibold mb-1">4. Tous bénéficient</p>
              <p className="text-gray-400">Chaque contributeur reçoit une reconnaissance permanente</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
          <h3 className="text-cyan-400 font-semibold mb-3">Exemple : Votre savoir-faire est recherché</h3>
          <div className="grid md:grid-cols-4 gap-4 text-sm">
            <div className="bg-cyan-900/20 border border-cyan-500/20 rounded-lg p-3 text-center">
              <p className="text-cyan-400 font-semibold mb-1">1. Votre profil</p>
              <p className="text-gray-400">Vos compétences sont enregistrées (vous décidez quoi partager)</p>
            </div>
            <div className="bg-yellow-900/20 border border-yellow-500/20 rounded-lg p-3 text-center">
              <p className="text-yellow-400 font-semibold mb-1">2. Un besoin émerge</p>
              <p className="text-gray-400">Quelqu'un dans la communauté a besoin de vos talents</p>
            </div>
            <div className="bg-emerald-900/20 border border-emerald-500/20 rounded-lg p-3 text-center">
              <p className="text-emerald-400 font-semibold mb-1">3. Le pont se fait</p>
              <p className="text-gray-400">Le système vous notifie, vous choisissez d'accepter ou non</p>
            </div>
            <div className="bg-purple-900/20 border border-purple-500/20 rounded-lg p-3 text-center">
              <p className="text-purple-400 font-semibold mb-1">4. La valeur circule</p>
              <p className="text-gray-400">Votre contribution est valorisée et tracée pour toujours</p>
            </div>
          </div>
        </div>
      </div>

      {/* Le principe */}
      <div className="text-center max-w-2xl mx-auto">
        <p className="text-gray-400 leading-relaxed">
          Chaque interaction dans AT·OM crée un lien. Chaque lien renforce le réseau.
          Plus le réseau est fort, plus chaque personne en bénéficie.
          C'est le principe de <span className="text-yellow-400 font-semibold">dualité</span> :
          ce que vous donnez au système, il vous le rend — transformé et amplifié.
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LES 6 FACETTES
// ═══════════════════════════════════════════════════════════════════════════════

const FacettesSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-yellow-900/10" aria-labelledby="section-facettes">
    <div className="max-w-4xl mx-auto">
      <h2 id="section-facettes" className="text-3xl font-bold text-center text-white mb-4">
        Les 6 Facettes du Diamant
      </h2>
      <p className="text-gray-400 text-center mb-12 max-w-xl mx-auto">
        Un seul système. Six dimensions de votre vie. Toutes connectées.
      </p>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {FACETTES.map((facette) => (
          <div key={facette.name} className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 hover:border-yellow-500/30 transition-all group">
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">{facette.icon}</div>
            <h3 className="font-semibold text-yellow-400 mb-2">{facette.name}</h3>
            <p className="text-gray-400 text-sm">{facette.desc}</p>
          </div>
        ))}
      </div>

      {/* Répercussion */}
      <div className="mt-12 text-center">
        <p className="text-gray-500 max-w-lg mx-auto">
          Peu importe votre angle d'entrée — la technologie, la politique, la sagesse —
          vous accédez au même système complet.
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FLOW KEEPER (SYSTÈME DE STIMULUS)
// ═══════════════════════════════════════════════════════════════════════════════

const FlowKeeperSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-emerald-900/10" aria-labelledby="section-flowkeeper">
    <div className="max-w-5xl mx-auto">
      <h2 id="section-flowkeeper" className="text-3xl font-bold text-center text-white mb-4">
        Le Flow Keeper
      </h2>
      <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
        Un système de contribution consciente où vous choisissez où va votre énergie —
        et chaque action est reconnue pour toujours.
      </p>

      {/* Ce que ça change */}
      <div className="grid md:grid-cols-2 gap-8 mb-12">
        <div className="bg-red-900/10 border border-red-500/20 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-red-400 mb-4 text-center">Aujourd'hui</h3>
          <ul className="space-y-3 text-gray-400">
            <li className="flex items-start gap-2"><span className="text-red-400">✗</span> Vous ne savez pas où va votre argent</li>
            <li className="flex items-start gap-2"><span className="text-red-400">✗</span> Aucune reconnaissance de vos contributions</li>
            <li className="flex items-start gap-2"><span className="text-red-400">✗</span> Intermédiaires opaques entre vous et l'impact</li>
          </ul>
        </div>

        <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-emerald-400 mb-4 text-center">Avec le Flow Keeper</h3>
          <ul className="space-y-3 text-emerald-200/80">
            <li className="flex items-start gap-2"><span className="text-emerald-400">✓</span> Vous choisissez exactement où contribuer</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">✓</span> Chaque action génère une preuve permanente</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">✓</span> Traçabilité complète, de bout en bout</li>
          </ul>
        </div>
      </div>

      {/* 6 Directions de flux */}
      <h3 className="text-xl font-semibold text-white mb-6 text-center">Choisissez votre direction</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {FLOW_TYPES.map((flow) => (
          <div key={flow.name} className="bg-gray-900/50 border border-gray-800 rounded-xl p-4 text-center hover:border-emerald-500/30 transition-all">
            <div className="text-2xl mb-2">{flow.icon}</div>
            <h4 className="text-emerald-400 font-semibold text-sm mb-1">{flow.name}</h4>
            <p className="text-gray-500 text-xs">{flow.desc}</p>
          </div>
        ))}
      </div>

      {/* Répercussion */}
      <div className="bg-gradient-to-r from-emerald-900/20 to-yellow-900/20 border border-emerald-500/20 rounded-xl p-6 text-center">
        <p className="text-gray-300 max-w-xl mx-auto">
          <span className="text-emerald-400 font-semibold">La répercussion :</span> un monde où chaque contribution
          est visible, permanente, et retourne naturellement vers ceux qui donnent.
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: NFT & JETONS DE TRANSITION
// ═══════════════════════════════════════════════════════════════════════════════

const NFTSection = () => (
  <section className="py-20 px-4 bg-black" aria-labelledby="section-participation">
    <div className="max-w-5xl mx-auto">
      <h2 id="section-participation" className="text-3xl font-bold text-center text-white mb-4">
        Participation & Reconnaissance
      </h2>
      <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
        Chaque participant reçoit une reconnaissance permanente et proportionnelle à son engagement.
        Pas de spéculation — de la valeur réelle, traçable et équitable.
      </p>

      {/* Comment ça fonctionne — concis */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="bg-gray-900/50 border border-emerald-500/20 rounded-xl p-6 text-center">
          <div className="text-3xl mb-3">🌱</div>
          <h3 className="text-emerald-400 font-semibold mb-2">Vous participez</h3>
          <p className="text-gray-400 text-sm">
            Par votre talent, votre temps ou votre capital — chaque forme de contribution compte.
          </p>
        </div>
        <div className="bg-gray-900/50 border border-yellow-500/20 rounded-xl p-6 text-center">
          <div className="text-3xl mb-3">🏆</div>
          <h3 className="text-yellow-400 font-semibold mb-2">Vous êtes reconnu</h3>
          <p className="text-gray-400 text-sm">
            Un NFT unique et une reconnaissance permanente gravée sur la blockchain.
          </p>
        </div>
        <div className="bg-gray-900/50 border border-purple-500/20 rounded-xl p-6 text-center">
          <div className="text-3xl mb-3">♻️</div>
          <h3 className="text-purple-400 font-semibold mb-2">La valeur circule</h3>
          <p className="text-gray-400 text-sm">
            L'économie interne récompense la contribution. Plus vous donnez, plus vous recevez.
          </p>
        </div>
      </div>

      {/* 5 niveaux — simplifié, pas de montants exposés */}
      <div className="bg-gray-900/30 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 text-center">5 niveaux de participation</h3>
        <div className="flex flex-wrap justify-center gap-4">
          {NFT_TIERS.map((tier) => (
            <div key={tier.name} className="flex items-center gap-2 px-4 py-2 bg-black/50 rounded-full border border-gray-700">
              <span className="text-xl">{tier.symbol}</span>
              <span className="text-white font-semibold text-sm">{tier.name}</span>
              {tier.max && <span className="text-gray-600 text-xs">(limité)</span>}
            </div>
          ))}
        </div>
        <p className="text-gray-600 text-xs text-center mt-4">
          Détails disponibles dans les sections d'inscription ci-dessous
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// STYLES FORMULAIRE
// ═══════════════════════════════════════════════════════════════════════════════

const COLOR_CLASSES = {
  blue: { bg: 'bg-blue-900/20', border: 'border-blue-500/30', btn: 'bg-blue-600 hover:bg-blue-500 text-white' },
  yellow: { bg: 'bg-yellow-900/20', border: 'border-yellow-500/30', btn: 'bg-yellow-600 hover:bg-yellow-500 text-black' },
  emerald: { bg: 'bg-emerald-900/20', border: 'border-emerald-500/30', btn: 'bg-emerald-600 hover:bg-emerald-500 text-white' }
};

const emptyFields = (fields) => fields.reduce((acc, f) => ({ ...acc, [f.name]: '' }), {});

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FORMULAIRE GÉNÉRIQUE
// ═══════════════════════════════════════════════════════════════════════════════

const RegistrationForm = ({ type, color, fields }) => {
  const colorClasses = COLOR_CLASSES[color];
  const [formData, setFormData] = useState({ name: '', email: '', phone: '', ...emptyFields(fields) });
  const [formStatus, setFormStatus] = useState({ result: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFormStatus({ result: '', message: '' });

    try {
      if (!formData.name || !formData.email) {
        throw new Error('Nom et email requis');
      }

      const { error } = await supabase
        .from('progreso_waitlist')
        .insert([{
          name: formData.name,
          email: formData.email,
          phone: formData.phone || null,
          type: type,
          skills: formData.skills || null,
          motivation: formData.motivation || null,
          support_type: formData.support_type || null,
          source: 'progreso_2026',
          created_at: new Date().toISOString()
        }]);

      if (error) {
        if (error.code === '23505') throw new Error('Cet email est déjà inscrit.');
        console.error('Supabase error:', error);
        throw new Error('Une erreur est survenue. Veuillez réessayer.');
      }

      const typeLabel = type === 'citizen' ? 'Citoyen' : type === 'founder' ? 'Fondateur' : 'Investisseur';
      setFormStatus({
        result: 'success',
        message: `Bienvenue ${formData.name}! Vous êtes inscrit en tant que ${typeLabel}. Nous vous contacterons bientôt.`
      });

      setFormData({ name: '', email: '', phone: '', ...emptyFields(fields) });

    } catch (err) {
      setFormStatus({ result: 'error', message: err.message || 'Erreur lors de l\'inscription.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto">
      <form onSubmit={handleSubmit} className={`${colorClasses.bg} border ${colorClasses.border} rounded-xl p-6 space-y-4`}>
        <label className="block">
          <span className="text-gray-400 text-sm mb-1 block">Nom *</span>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Votre nom"
            required
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white/30"
          />
        </label>

        <label className="block">
          <span className="text-gray-400 text-sm mb-1 block">Email *</span>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Votre email"
            required
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white/30"
          />
        </label>

        <label className="block">
          <span className="text-gray-400 text-sm mb-1 block">Téléphone (optionnel)</span>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            placeholder="Téléphone"
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white/30"
          />
        </label>

        {fields.map((field) => (
          <label key={field.name} className="block">
            <span className="text-gray-400 text-sm mb-1 block">{field.label || field.placeholder}</span>
            <textarea
              name={field.name}
              value={formData[field.name]}
              onChange={handleChange}
              placeholder={field.placeholder}
              rows={3}
              className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white/30 resize-none"
            />
          </label>
        ))}

        {formStatus.message && (
          <div role="alert" className={`p-4 rounded-lg ${formStatus.result === 'success' ? 'bg-green-900/30 border border-green-500/30 text-green-400' : 'bg-red-900/30 border border-red-500/30 text-red-400'}`}>
            {formStatus.message}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full px-6 py-4 font-bold rounded-lg transition-all ${isSubmitting ? 'bg-gray-700 text-gray-400 cursor-not-allowed' : colorClasses.btn}`}
        >
          {isSubmitting ? 'Inscription...' : 'S\'inscrire'}
        </button>
      </form>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION CITOYEN
// ═══════════════════════════════════════════════════════════════════════════════

const CitizenSection = ({ refProp }) => (
  <section ref={refProp} className="py-16 px-4 bg-blue-900/10">
    <div className="max-w-4xl mx-auto">
      {/* Explication du rôle */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">👤</div>
        <h2 className="text-2xl font-bold text-blue-400 mb-2">DEVENIR CITOYEN</h2>
        <p className="text-white/80 font-medium mb-2">Souverain de vos données, maître de votre temps</p>
      </div>

      {/* Avantages */}
      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">🔐</div>
          <h4 className="text-blue-400 font-semibold mb-1">Données Souveraines</h4>
          <p className="text-gray-400 text-sm">Vos données vous appartiennent. Exportables, supprimables, portables.</p>
        </div>
        <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">🗳️</div>
          <h4 className="text-blue-400 font-semibold mb-1">Droit de Vote</h4>
          <p className="text-gray-400 text-sm">Participez aux décisions. Démocratie directe sur toutes les propositions.</p>
        </div>
        <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">💰</div>
          <h4 className="text-blue-400 font-semibold mb-1">Économie UR</h4>
          <p className="text-gray-400 text-sm">Gagnez des Unités de Résonance en contribuant à la communauté.</p>
        </div>
      </div>

      {/* Sphères accessibles */}
      <div className="bg-black/30 border border-blue-500/20 rounded-xl p-4 mb-8 text-center">
        <p className="text-gray-400 text-sm">
          <span className="text-blue-400 font-semibold">Sphères accessibles:</span> Identité (1), Santé (2), Savoir (3), Économie (4), Gouvernance (5)
        </p>
      </div>

      {/* Formulaire */}
      <RegistrationForm
        type={WAITLIST_TYPES.CITIZEN}
        color="blue"
        fields={[
          { name: 'motivation', label: 'Motivation (optionnel)', placeholder: 'Qu\'est-ce qui vous attire dans cette vision?' }
        ]}
      />
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION FONDATEUR - Avec explication complète du rôle
// ═══════════════════════════════════════════════════════════════════════════════

const FounderSection = ({ refProp }) => (
  <section ref={refProp} className="py-16 px-4 bg-yellow-900/10">
    <div className="max-w-4xl mx-auto">
      {/* Explication du rôle */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">⚡</div>
        <h2 className="text-2xl font-bold text-yellow-400 mb-2">DEVENIR FONDATEUR</h2>
        <p className="text-white/80 font-medium mb-2">Bâtissez l'Arche avant son ouverture</p>
        <p className="text-yellow-400/60 text-sm">Phase I: Nous recrutons les 144 premiers fondateurs</p>
      </div>

      {/* Avantages */}
      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">🌰</div>
          <h4 className="text-yellow-400 font-semibold mb-1">NFT Graine Offert</h4>
          <p className="text-gray-400 text-sm">Votre contribution de talent = NFT Graine équivalent à 100 UR minimum.</p>
        </div>
        <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">🏛️</div>
          <h4 className="text-yellow-400 font-semibold mb-1">Cercle Privé</h4>
          <p className="text-gray-400 text-sm">Accès au cercle des fondateurs. Discussions stratégiques exclusives.</p>
        </div>
        <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-xl p-4 text-center">
          <div className="text-xl mb-2">⭐</div>
          <h4 className="text-yellow-400 font-semibold mb-1">Nom Gravé</h4>
          <p className="text-gray-400 text-sm">Votre nom dans le Mur des Fondateurs. Reconnaissance éternelle.</p>
        </div>
      </div>

      {/* Talents recherchés */}
      <div className="bg-black/30 border border-yellow-500/20 rounded-xl p-4 mb-8">
        <p className="text-center text-gray-400 text-sm mb-3">
          <span className="text-yellow-400 font-semibold">Talents recherchés:</span>
        </p>
        <div className="flex flex-wrap justify-center gap-2">
          {['Développeurs', 'Designers', 'Légistes', 'Communicateurs', 'Marketeurs', 'Philosophes', 'Traducteurs', 'Vidéastes', 'Community Managers'].map(t => (
            <span key={t} className="px-3 py-1 bg-yellow-900/30 text-yellow-400/80 rounded-full text-xs">{t}</span>
          ))}
        </div>
      </div>

      {/* Formulaire */}
      <RegistrationForm
        type={WAITLIST_TYPES.FOUNDER}
        color="yellow"
        fields={[
          { name: 'skills', label: 'Compétences', placeholder: 'Dev, design, légal, finance, communication, stratégie...' },
          { name: 'motivation', label: 'Contribution souhaitée', placeholder: 'Comment voulez-vous contribuer à la construction?' }
        ]}
      />
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION INVESTISSEUR - Avec explication complète
// ═══════════════════════════════════════════════════════════════════════════════

const InvestorSection = ({ refProp }) => (
  <section ref={refProp} className="py-16 px-4 bg-emerald-900/10">
    <div className="max-w-4xl mx-auto">
      {/* Explication du rôle */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">💎</div>
        <h2 className="text-2xl font-bold text-emerald-400 mb-2">DEVENIR INVESTISSEUR</h2>
        <p className="text-white/80 font-medium mb-2">Propulsez la nouvelle économie de coopération</p>
        <p className="text-emerald-400/60 text-sm">Jetons de Transition (JT) → Unités de Résonance (UR) au lancement</p>
      </div>

      {/* Avantages par tier */}
      <div className="grid md:grid-cols-2 gap-4 mb-8">
        <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-xl p-4">
          <h4 className="text-emerald-400 font-semibold mb-3">💰 Jetons de Transition</h4>
          <ul className="space-y-2 text-gray-400 text-sm">
            <li className="flex items-start gap-2"><span className="text-emerald-400">→</span> Conversion garantie 1 JT = 1 UR</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">→</span> Pas de spéculation, valeur stable</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">→</span> Utilisable dès le lancement</li>
          </ul>
        </div>
        <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-xl p-4">
          <h4 className="text-emerald-400 font-semibold mb-3">🏆 NFT selon votre tier</h4>
          <ul className="space-y-2 text-gray-400 text-sm">
            <li className="flex items-start gap-2"><span className="text-emerald-400">🌰</span> Graine: $10 - $99</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">🌱</span> Pousse: $100 - $499 (max 1,000)</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">🌿</span> Branche: $500 - $1,999 (max 144)</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">🌳</span> Racine: $2,000 - $9,999 (max 36)</li>
            <li className="flex items-start gap-2"><span className="text-emerald-400">🌲</span> Arbre: $10,000+ (max 9)</li>
          </ul>
        </div>
      </div>

      {/* Flow Keeper */}
      <div className="bg-gradient-to-r from-emerald-900/20 to-yellow-900/20 border border-emerald-500/30 rounded-xl p-4 mb-8 text-center">
        <p className="text-gray-400 text-sm">
          <span className="text-emerald-400 font-semibold">Flow Keeper:</span> Choisissez où va votre énergie (Tech, Vie, Sagesse, Justice, Graine, Terre).
          <br/>100% va à la communauté. 0% à l'infrastructure. Token Souvenir gravé sur Hedera.
        </p>
      </div>

      {/* Formulaire */}
      <RegistrationForm
        type={WAITLIST_TYPES.INVESTOR}
        color="emerald"
        fields={[
          { name: 'support_type', label: 'Type de support', placeholder: 'Capital, infrastructure, réseau, expertise...' },
          { name: 'motivation', label: 'Motivation', placeholder: 'Pourquoi souhaitez-vous investir dans ce projet?' }
        ]}
      />
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FAQ SECTION
// ═══════════════════════════════════════════════════════════════════════════════

const FAQSection = () => (
  <section className="py-20 px-4 bg-gradient-to-b from-black to-gray-900/30" aria-labelledby="section-faq">
    <div className="max-w-3xl mx-auto">
      <h2 id="section-faq" className="text-3xl font-bold text-center text-white mb-4">
        Questions fréquentes
      </h2>
      <p className="text-gray-500 text-center mb-12">
        Les réponses aux questions que vous n'avez pas encore posées.
      </p>
      <div className="space-y-4">
        {FAQS.map((faq) => (
          <div key={faq.q} className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-yellow-500/30 transition-all">
            <h3 className="text-lg font-semibold text-yellow-400 mb-3">{faq.q}</h3>
            <p className="text-gray-400">{faq.a}</p>
          </div>
        ))}
      </div>

      {/* Contact */}
      <div className="mt-12 text-center">
        <p className="text-gray-500">
          Une autre question?{' '}
          <a href="mailto:contact@at-om.org" className="text-yellow-400 hover:underline">
            Contactez-nous
          </a>
        </p>
      </div>
    </div>
  </section>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FOOTER
// ═══════════════════════════════════════════════════════════════════════════════

const Footer = () => (
  <footer className="py-16 px-4 bg-black border-t border-yellow-900/30">
    <div className="max-w-5xl mx-auto">
      {/* Logo et citation */}
      <div className="text-center mb-12">
        <div className="text-5xl mb-4">🔱</div>
        <p className="text-yellow-500 font-bold text-2xl mb-2">AT·OM</p>
        <p className="text-white/60 italic mb-4">
          "Nous ne construisons pas pour nous.<br/>
          Nous construisons pour ceux qui viendront."
        </p>
      </div>

      {/* Liens rapides */}
      <div className="grid md:grid-cols-3 gap-8 mb-12 text-center md:text-left">
        <div>
          <h4 className="text-white font-semibold mb-3">L'Arche</h4>
          <ul className="space-y-2 text-gray-500 text-sm">
            <li>9 Sphères</li>
            <li>7 Lois Universelles</li>
            <li>6 Facettes du Diamant</li>
            <li>Encyclopédie AT-OM</li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Économie</h4>
          <ul className="space-y-2 text-gray-500 text-sm">
            <li>Unité de Résonance (UR)</li>
            <li>Jetons de Transition (JT)</li>
            <li>Flow Keeper</li>
            <li>NFT Tiers</li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Technologie</h4>
          <ul className="space-y-2 text-gray-500 text-sm">
            <li>Hedera Hashgraph</li>
            <li>Smart Contracts</li>
            <li>Données Souveraines</li>
            <li>IA Éthique</li>
          </ul>
        </div>
      </div>

      {/* Copyright */}
      <div className="text-center border-t border-gray-900 pt-8">
        <p className="text-gray-700 text-sm">
          Progreso 2026 | Souveraineté Mondiale | L'Arche des Résonances
        </p>
        <p className="text-gray-800 text-xs mt-2">
          © {new Date().getFullYear()} AT·OM — Tous droits réservés à l'humanité
        </p>
      </div>
    </div>
  </footer>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MOMENTUM BAR — Barre de progression live
// ═══════════════════════════════════════════════════════════════════════════════

const MomentumBar = ({ momentum, nftAvailability, loading }) => {
  if (loading || !momentum) return null;

  const pct = parseFloat(momentum.percentage || 0);
  const raised = parseFloat(momentum.raised_usd || 0);
  const goal = parseFloat(momentum.goal_usd || 100000);

  return (
    <section className="py-8 px-4 bg-gradient-to-r from-yellow-900/10 to-emerald-900/10 border-b border-yellow-500/20">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-bold text-yellow-400">Momentum Phase I</h3>
          <span className="text-emerald-400 font-mono text-sm">
            ${raised.toLocaleString()} / ${goal.toLocaleString()}
          </span>
        </div>

        {/* Progress bar */}
        <div className="w-full h-3 bg-gray-800 rounded-full overflow-hidden mb-4" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label={`Progression Phase I: ${pct.toFixed(1)}%`}>
          <div
            className="h-full bg-gradient-to-r from-yellow-500 to-emerald-500 rounded-full transition-all duration-1000"
            style={{ width: `${Math.min(pct, 100)}%` }}
          />
        </div>

        {/* NFT availability row */}
        {nftAvailability && (
          <div className="flex flex-wrap justify-center gap-3">
            {Object.entries(nftAvailability).map(([key, tier]) => (
              <div key={key} className="flex items-center gap-1.5 px-3 py-1 bg-black/30 rounded-full border border-gray-800">
                <span className="text-sm">{tier.symbol}</span>
                <span className="text-xs text-gray-400">{tier.name?.split(' ')[0]}</span>
                <span className={`text-xs font-mono ${tier.sold_out ? 'text-red-400' : 'text-emerald-400'}`}>
                  {tier.max_supply ? `${tier.minted}/${tier.max_supply}` : `${tier.minted}`}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Contributors count */}
        <div className="text-center mt-3">
          <span className="text-gray-500 text-xs">
            {momentum.contributors || 0} contributeur{(momentum.contributors || 0) !== 1 ? 's' : ''} | {pct.toFixed(1)}% de l'objectif
          </span>
        </div>
      </div>
    </section>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ATOM PRICE DISPLAY — Bonding curve live
// ═══════════════════════════════════════════════════════════════════════════════

const AtomPriceDisplay = ({ atomState }) => {
  if (!atomState) return null;

  const price = parseFloat(atomState.price || 0.01);
  const supply = parseFloat(atomState.supply || 0);
  const maxSupply = parseFloat(atomState.max_supply || 9990000);
  const reserve = parseFloat(atomState.reserve || 0);

  return (
    <section className="py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">AT·OM$ — Valeur en temps réel</h2>
          <p className="text-gray-500 text-sm">Un prix qui grandit avec l'adoption — pas de spéculation, de la valeur réelle</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-b from-yellow-900/20 to-black rounded-xl p-4 border border-yellow-500/20 text-center">
            <p className="text-xs text-gray-500 mb-1">Prix actuel</p>
            <p className="text-2xl font-bold text-yellow-400">${price.toFixed(4)}</p>
          </div>
          <div className="bg-gradient-to-b from-emerald-900/20 to-black rounded-xl p-4 border border-emerald-500/20 text-center">
            <p className="text-xs text-gray-500 mb-1">Supply</p>
            <p className="text-2xl font-bold text-emerald-400">{supply.toLocaleString()}</p>
            <p className="text-xs text-gray-600">/ {(maxSupply/1000000).toFixed(1)}M max</p>
          </div>
          <div className="bg-gradient-to-b from-blue-900/20 to-black rounded-xl p-4 border border-blue-500/20 text-center">
            <p className="text-xs text-gray-500 mb-1">Reserve</p>
            <p className="text-2xl font-bold text-blue-400">${reserve.toLocaleString()}</p>
          </div>
          <div className="bg-gradient-to-b from-purple-900/20 to-black rounded-xl p-4 border border-purple-500/20 text-center">
            <p className="text-xs text-gray-500 mb-1">Market Cap</p>
            <p className="text-2xl font-bold text-purple-400">${(price * supply).toLocaleString()}</p>
          </div>
        </div>

        {process.env.REACT_APP_HEDERA_TOKEN_ID && (
          <div className="mt-4 text-center">
            <a
              href={`https://hashscan.io/${process.env.REACT_APP_HEDERA_NETWORK || 'mainnet'}/token/${process.env.REACT_APP_HEDERA_TOKEN_ID}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 bg-purple-900/20 border border-purple-500/20 rounded-lg text-purple-400 hover:bg-purple-900/30 transition-all text-sm"
            >
              Voir sur Hedera Hashscan <span className="sr-only">(ouvre un nouvel onglet)</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        )}
      </div>
    </section>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE
// ═══════════════════════════════════════════════════════════════════════════════

const ProgresoPage = () => {
  const citizenRef = useRef(null);
  const founderRef = useRef(null);
  const investorRef = useRef(null);

  // Connect to live tokenomics data
  const {
    momentum, nftAvailability, atomState,
    loading, isSimulation
  } = useTokenomics();

  const scrollTo = (ref) => ref.current?.scrollIntoView({ behavior: 'smooth' });

  return (
    <main className="min-h-screen bg-black text-white">
      {/* Simulation mode indicator */}
      {isSimulation && (
        <div className="bg-yellow-900/30 border-b border-yellow-500/30 py-2 px-4 text-center" role="status">
          <span className="text-yellow-400 text-xs">Mode simulation — Données de test</span>
        </div>
      )}

      {/* 1. Hero — Vision principale */}
      <HeroSection
        onScrollToCitizen={() => scrollTo(citizenRef)}
        onScrollToFounder={() => scrollTo(founderRef)}
        onScrollToInvestor={() => scrollTo(investorRef)}
      />

      {/* 2. Momentum Bar — Progression live */}
      <MomentumBar momentum={momentum} nftAvailability={nftAvailability} loading={loading} />

      {/* 3. Vision — Ce que nous construisons */}
      <VisionSection />

      {/* 4. Les 9 Sphères */}
      <SpheresSection />

      {/* 5. 7 Lois Universelles */}
      <LoisSection />

      {/* 6. Le Moteur Vivant */}
      <MoteurVivantSection />

      {/* 7. Connexions */}
      <ConnexionsSection />

      {/* 8. Les 6 Facettes du Diamant */}
      <FacettesSection />

      {/* 9. Flow Keeper */}
      <FlowKeeperSection />

      {/* 10. Participation & Reconnaissance */}
      <NFTSection />

      {/* 11. AT·OM$ — Valeur en temps réel */}
      <AtomPriceDisplay atomState={atomState} />

      {/* 12. Choisissez votre rôle */}
      <section className="py-12 px-4 bg-gradient-to-b from-black to-gray-900/30" aria-labelledby="section-roles">
        <div className="max-w-4xl mx-auto text-center">
          <h2 id="section-roles" className="text-3xl font-bold text-white mb-4">Choisissez votre rôle</h2>
          <p className="text-gray-500 mb-6">Trois façons de rejoindre l'Arche</p>
          <div className="flex flex-wrap justify-center gap-4">
            <button onClick={() => scrollTo(citizenRef)} className="px-4 py-2 bg-blue-600/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-600/30">
              <span aria-hidden="true">👤 </span>Citoyen — Rejoindre
            </button>
            <button onClick={() => scrollTo(founderRef)} className="px-4 py-2 bg-yellow-600/20 border border-yellow-500/30 rounded-lg text-yellow-400 hover:bg-yellow-600/30">
              <span aria-hidden="true">⚡ </span>Fondateur — Construire
            </button>
            <button onClick={() => scrollTo(investorRef)} className="px-4 py-2 bg-emerald-600/20 border border-emerald-500/30 rounded-lg text-emerald-400 hover:bg-emerald-600/30">
              <span aria-hidden="true">💎 </span>Investisseur — Propulser
            </button>
          </div>
        </div>
      </section>

      {/* 13. Formulaire Citoyen */}
      <CitizenSection refProp={citizenRef} />

      {/* 14. Formulaire Fondateur */}
      <FounderSection refProp={founderRef} />

      {/* 15. Formulaire Investisseur */}
      <InvestorSection refProp={investorRef} />

      {/* 16. FAQ */}
      <FAQSection />

      {/* 17. Footer */}
      <Footer />
    </main>
  );
};

export default ProgresoPage;
