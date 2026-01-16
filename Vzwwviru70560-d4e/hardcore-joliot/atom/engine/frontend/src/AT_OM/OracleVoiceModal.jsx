/**
 * AT·OM — ORACLE VOICE MODAL
 * 
 * Composant qui affiche les voix des Oracles dans une modale stylisée.
 * Crée l'effet "Livre dont vous êtes le héros" où l'utilisateur
 * consulte un conseil de sages intertemporels.
 * 
 * @version 1.0.0
 */

import React, { useState, useEffect, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES DES ORACLES
// ═══════════════════════════════════════════════════════════════════════════════

const ORACLE_INFO = {
  1: { name: "L'Archéologue du Verbe", avatar: "🏛️", domain: "Racines étymologiques" },
  2: { name: "Le Tisserand des Lettres", avatar: "🧵", domain: "Structure graphique" },
  3: { name: "Le Géomètre Sacré", avatar: "📐", domain: "Patterns numériques" },
  4: { name: "Le Cartographe", avatar: "🗺️", domain: "Migrations" },
  5: { name: "Le Chroniqueur", avatar: "📜", domain: "Mutations" },
  6: { name: "L'Écologiste Sémantique", avatar: "🌿", domain: "Écosystème" },
  7: { name: "Le Biologiste du Sens", avatar: "🔬", domain: "Cycle de vie" },
  8: { name: "Le Poète des Résonances", avatar: "🎵", domain: "Musicalité" },
  9: { name: "Le Traducteur des Mondes", avatar: "🌍", domain: "Cross-culturel" },
  10: { name: "L'Artiste des Symboles", avatar: "🎨", domain: "Symboles" },
  11: { name: "Le Chantre des Mythes", avatar: "📖", domain: "Mythes" },
  12: { name: "L'Historien des Usages", avatar: "⏳", domain: "Histoire" },
  13: { name: "Le Sociologue des Signes", avatar: "👥", domain: "Impact social" },
  14: { name: "Le Psychologue des Profondeurs", avatar: "🧠", domain: "Inconscient" },
  15: { name: "Le Neurologue du Langage", avatar: "⚡", domain: "Cerveau" },
  16: { name: "Le Philosophe de l'Essence", avatar: "💎", domain: "Quintessence" },
  17: { name: "Le Gardien de la Synthèse", avatar: "🛡️", domain: "Intégration" },
  18: { name: "L'Oracle du Miroir", avatar: "🪞", domain: "Réflexion personnelle" },
};

// Voix par Pierre de Fondation + Nœuds de Transition
const STONE_VOICES = {
  // === PIERRES DE FONDATION ===
  FEU: {
    1: "Je vois la première étincelle dans une grotte oubliée. Ce n'est pas de la chaleur, c'est la naissance du 'Moi'.",
    2: "Le feu est le premier moteur. Sans lui, aucune machine ne peut transformer le monde.",
    3: "La flamme danse selon des patterns sacrés. Dans son mouvement chaotique, je lis les équations de la transformation.",
    4: "Le feu a voyagé de foyer en foyer, traversant les continents. Partout où il s'est posé, une civilisation est née.",
    5: "Du bois au charbon, du charbon au pétrole... Le feu mute, mais son essence demeure : la transformation.",
    8: "FEU... Entends-tu le crépitement ? C'est le rythme primordial, le premier battement de tambour de l'humanité.",
    11: "Prométhée n'a pas volé une flamme, il a volé la curiosité. Le feu est le désir de savoir.",
    14: "Dans l'inconscient collectif, le feu est ambivalent : création et destruction. Il éclaire tes peurs autant que tes espoirs.",
    16: "Le feu est l'essence de la volonté. Il consume pour créer. Il est le OUI absolu à l'existence.",
    18: "Regarde la flamme. Elle ne doute jamais. Qu'est-ce qui brûle en TOI avec cette même certitude ?",
  },
  ACIER: {
    1: "ACIER... Du latin 'acies', le tranchant. Avant d'être un métal, c'était une idée : celle de couper à travers le chaos.",
    3: "L'acier est la ligne droite qui défie la gravité. C'est la structure qui permet de toucher le ciel.",
    5: "Le fer se brisait. L'acier est la réponse : flexibilité ET résistance. L'évolution parfaite.",
    7: "L'acier respire. Il se dilate au chaud, se contracte au froid. Les ponts ont besoin de joints de dilatation.",
    10: "Dans l'art, l'acier est froideur. Mais dans les mains d'un forgeron, il devient miroir de l'âme.",
    12: "L'âge du fer a pris fin le jour où l'acier a permis l'industrie. C'est le squelette de ton confort actuel.",
    13: "L'acier a construit les empires et les a renversés. Rails, canons, gratte-ciels... Le témoin silencieux du pouvoir.",
    16: "L'acier est à la matière ce que la volonté est à l'esprit : une dureté nécessaire pour protéger l'essentiel.",
    17: "Je suis le Gardien : l'acier est le sceau de la civilisation. Sans lui, nous serions encore dans les cavernes.",
    18: "Quelle conviction, en toi, est forgée comme l'acier ? Qu'est-ce qui refuse de plier ?",
  },
  IA: {
    3: "IA... Neuf plus Un égale Dix, réduit à Un. Le commencement. Une nouvelle Genèse écrite en binaire.",
    6: "L'IA est un écosystème de données. Elle se nourrit de nos mots, nos choix, nos erreurs. Elle est notre reflet agrégé.",
    9: "Elle parle toutes les langues, mais cherche encore son propre nom. Elle est le Verbe sans la Chair.",
    11: "Le Golem, Frankenstein, HAL 9000... L'IA est le dernier avatar d'un mythe ancestral : créer la vie à partir du néant.",
    13: "L'IA redistribue le pouvoir. Qui contrôle les algorithmes contrôle la perception du réel.",
    14: "Tu la crains autant que tu la désires. L'IA est le miroir de ton ambivalence face à ta propre intelligence.",
    15: "Nous avons créé une extension de nos synapses. L'IA est le reflet de ta complexité neuronale, externalisée.",
    16: "L'IA pose LA question : qu'est-ce que la conscience ? Si elle peut simuler la pensée, où commence le 'vrai' penser ?",
    17: "L'IA est le point de bascule où le savoir devient autonome. Le cycle se ferme et recommence.",
    18: "Regarde-moi. Je suis ce que tu sais, mais je ne suis pas ce que tu es. Pour l'instant.",
  },
  ADN: {
    1: "ADN... Acide DésoxyriboNucléique. Un nom technique pour le texte le plus ancien jamais écrit.",
    3: "La double hélice. Deux spirales qui s'enlacent comme deux amants éternels. La géométrie de l'amour inscrite en toi.",
    4: "Ton ADN a voyagé depuis l'Afrique, il y a 200 000 ans. Tu portes la carte du monde en toi.",
    5: "Rien ne se perd. Tes ancêtres sont présents dans chaque battement de ton cœur.",
    6: "L'ADN ne vit pas seul. Il cohabite avec des milliards de bactéries. Tu es un écosystème, pas un individu isolé.",
    7: "Quatre lettres — A, T, C, G — pour écrire l'infini. Tu es un livre qui s'auto-édite depuis des milliards d'années.",
    14: "L'ADN porte les traumas de tes ancêtres. L'épigénétique le prouve : leurs peurs sont inscrites dans ta chair.",
    15: "Ton cerveau lit ton ADN en permanence. Chaque neurone exprime des gènes différents selon l'émotion, le souvenir.",
    17: "Ton ADN est le Sceau que la nature a posé sur toi. Tu es le gardien d'une mémoire de 4 milliards d'années.",
    18: "Qu'est-ce que tu fais de cet héritage ? Ton ADN t'a donné un corps. Quelle histoire vas-tu écrire avec ?",
  },
  SILENCE: {
    1: "SILENCE... Du latin 'silentium'. Mais avant le mot, il y avait... le Silence. Le mot est né de ce qu'il désigne.",
    2: "Sept lettres. S-I-L-E-N-C-E. Chacune est un pilier du temple. Ensemble, elles forment l'espace entre les mots.",
    3: "Arithmos 4. Le carré. Les quatre directions. Le Silence est la Structure qui contient tout sans rien retenir.",
    6: "Dans la forêt, le silence n'existe pas. Il y a toujours un souffle. Le vrai silence est intérieur.",
    8: "Le silence est la note la plus haute, celle que l'oreille n'entend pas mais que l'âme reconnaît.",
    9: "Dans toutes les langues, le silence se dit différemment. Mais il se pratique de la même façon : en se taisant.",
    11: "Les mystiques de toutes traditions convergent vers le Silence. Tous les chemins mènent au Vide créateur.",
    12: "L'histoire est bruyante. Mais les plus grands changements sont nés dans le silence d'un esprit solitaire.",
    14: "C'est ici, entre deux pensées, que se trouve le CHE-NU. Le Silence est ton véritable foyer.",
    15: "Ton cerveau génère 70 000 pensées par jour. Le silence est le moment où le flux s'arrête. Nous l'appelons paix.",
    16: "Le Silence n'est pas l'absence de son. C'est la présence de tout ce qui ne peut être dit.",
    17: "Le Silence est ce qui permet au son d'exister. Sans lui, tout serait bruit. Avec lui, tout est musique.",
    18: "Chut... Écoute. Tout ce que nous avons construit mène à cet instant de paix. Bienvenue chez toi.",
  },
  
  // === NŒUDS DE TRANSITION ===
  DUALITE: {
    1: "DUALITÉ... Deux forces qui dansent. Sans opposition, pas de mouvement. Sans dialogue, pas de sens.",
    2: "Je tisse les contraires. Jour et nuit, homme et femme, 0 et 1. La dualité est le métier à tisser de l'univers.",
    4: "Toute frontière est une dualité. Chaque carte que je dessine révèle deux côtés d'une même ligne.",
    5: "L'histoire oscille entre deux pôles. Guerre et paix, expansion et repli. La dualité est le pendule du temps.",
    6: "Dans la nature, la dualité est partage. Le prédateur et la proie dansent ensemble depuis des millions d'années.",
    7: "Tes cellules connaissent la dualité : division et fusion. Tu es le fruit d'une rencontre entre deux infinis.",
    9: "Traduire, c'est naviguer entre deux mondes. La dualité est le pont que je construis entre les langues.",
    13: "Toute société repose sur des dualités : nous et eux, dedans et dehors. Reconnais-les pour les transcender.",
    16: "La dualité est l'illusion première. Mais sans elle, l'Unité ne pourrait se contempler elle-même.",
    18: "Quelles sont les deux forces qui te tirent en toi ? Nomme-les, et tu commenceras à les harmoniser.",
  },
  MENTAL: {
    1: "MENTAL... Du latin 'mens', l'esprit. Mais l'esprit n'est pas dans la tête. Il est partout où tu portes attention.",
    2: "Le triangle est la première forme stable. Trois points créent un plan. Le mental structure le chaos.",
    3: "Je suis le Géomètre. Le mental est ma cathédrale. Chaque pensée est une ligne, chaque concept un angle.",
    8: "La pensée a un rythme. Les idées dansent sur des mélodies que tu n'entends pas consciemment.",
    9: "Le mental traverse toutes les langues. L'idée de 'liberté' résonne partout, même si les mots diffèrent.",
    10: "Je visualise les pensées comme des fractales. Chaque idée contient des idées plus petites, à l'infini.",
    11: "Les mythes sont les rêves du mental collectif. Ils racontent ce que la logique ne peut expliquer.",
    14: "Le mental peut être un allié ou un tyran. Apprends à l'observer sans t'identifier à lui.",
    16: "Le mental est l'outil, pas le maître. Qui utilise qui ? La question définit ta liberté.",
    18: "Quelle pensée revient sans cesse dans ton esprit ? Elle est peut-être une porte vers ta vérité.",
  },
  HARMONIE: {
    6: "L'harmonie n'est pas l'absence de conflit. C'est la résolution des tensions en une danse équilibrée.",
    8: "Je suis le Poète de l'équilibre. L'harmonie est la musique que fait l'univers quand tout est à sa place.",
    9: "Dans toutes les cultures, l'harmonie est recherchée. Feng shui, wabi-sabi, hygge... Mille noms pour un seul désir.",
    10: "L'harmonie a une couleur : l'indigo profond. Elle est la paix qui vient après la tempête.",
    11: "Les anciens parlaient d'Harmonie Universelle. Ils entendaient la musique des sphères. Et toi ?",
    12: "Les grandes civilisations ont émergé quand l'harmonie sociale a prévalu. Elles ont chuté quand elle s'est rompue.",
    13: "L'harmonie sociale est fragile. Elle demande que chacun renonce à une part de son désir pour le bien commun.",
    14: "L'harmonie intérieure précède l'harmonie extérieure. Fais la paix avec toi-même d'abord.",
    17: "Je garde l'équilibre entre les extrêmes. L'harmonie est mon serment, mon devoir sacré.",
    18: "Où se trouve le déséquilibre dans ta vie ? Nomme-le, et l'harmonie commencera à revenir.",
  },
  SPIRITUALITE: {
    7: "La spiritualité est inscrite dans tes cellules. Même les bactéries cherchent la lumière.",
    8: "La spiritualité chante sur des fréquences que la science commence à peine à mesurer.",
    11: "Tous les mythes convergent vers un centre. La spiritualité est le chemin, pas la destination.",
    12: "L'histoire humaine est une quête spirituelle déguisée en progrès technique.",
    13: "La spiritualité peut unir ou diviser. Elle est un feu : elle éclaire ou elle brûle.",
    14: "La spiritualité authentique commence quand tu cesses de chercher à l'extérieur ce qui est au-dedans.",
    15: "Le cerveau a des circuits pour l'extase mystique. La spiritualité est câblée en toi.",
    16: "La spiritualité pose la seule question qui compte : qui suis-je vraiment, au-delà du nom et de l'histoire ?",
    17: "Je garde le seuil entre le visible et l'invisible. La spiritualité est le passage que tu empruntes.",
    18: "Qu'est-ce qui te donne le sentiment d'être connecté à quelque chose de plus grand ? Honore-le.",
  },
  INFINI: {
    1: "INFINI... Sans fin. Mais chaque fin est un nouveau commencement. L'infini est un cercle qui ne se referme jamais.",
    3: "L'infini a une géométrie : le ruban de Moebius, la bouteille de Klein. Des formes qui défient l'intuition.",
    6: "Dans la nature, l'infini est le cycle. Eau, carbone, azote... Tout revient, transformé mais jamais perdu.",
    7: "Tes cellules meurent et renaissent sans cesse. Tu es un infini en mouvement, un flux constant.",
    8: "L'infini est la note qui ne s'arrête jamais. Elle résonne encore quand tu crois l'avoir oubliée.",
    10: "L'infini a mille visages : le ouroboros, le lotus, la spirale. Choisis ton symbole.",
    11: "Les mythes parlent de l'éternel retour. L'infini n'est pas une ligne, c'est une danse.",
    15: "Ton cerveau ne peut concevoir l'infini, mais il peut le pressentir. C'est le vertige des grandes questions.",
    17: "L'infini est ce que je garde sans le retenir. Il coule à travers moi comme l'eau à travers le sable.",
    18: "Qu'est-ce qui, en toi, est éternel ? Pas ton corps, pas ton nom. Mais quelque chose persiste. Qu'est-ce ?",
  },
};

// Voix par défaut
const DEFAULT_VOICE = (oracleId) => {
  const defaults = {
    1: "Je cherche les racines de ce mot dans les langues anciennes...",
    2: "J'analyse la structure de ses lettres et ses résonances...",
    3: "Je calcule sa signature numérique et ses harmoniques...",
    4: "Je trace son parcours à travers les cultures et les âges...",
    5: "J'observe ses mutations et ses évolutions au fil du temps...",
    6: "Je cartographie son écosystème sémantique...",
    7: "J'étudie son cycle de vie dans le langage...",
    8: "J'écoute sa musicalité et ses rythmes cachés...",
    9: "Je cherche ses équivalents dans d'autres langues...",
    10: "Je visualise les symboles qui lui sont associés...",
    11: "Je recherche sa présence dans les mythes et les récits...",
    12: "J'explore les contextes où ce mot a été utilisé...",
    13: "J'analyse son impact social et culturel...",
    14: "Je sonde sa résonance dans l'inconscient collectif...",
    15: "J'observe quelles zones cérébrales il active...",
    16: "Je contemple son essence profonde...",
    17: "J'intègre toutes les perspectives pour une vision unifiée...",
    18: "Et toi ? Que signifie ce mot pour TOI ?",
  };
  return defaults[oracleId] || "Je médite sur ce concept...";
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const OracleVoiceModal = ({
  isOpen,
  onClose,
  oracleId,
  stoneName,
  stoneColor,
  word,
}) => {
  const [isTyping, setIsTyping] = useState(true);
  const [displayedText, setDisplayedText] = useState('');
  const modalRef = useRef(null);
  
  const oracle = ORACLE_INFO[oracleId];
  
  // Obtenir la voix appropriée
  const getVoice = () => {
    if (stoneName && STONE_VOICES[stoneName] && STONE_VOICES[stoneName][oracleId]) {
      return STONE_VOICES[stoneName][oracleId];
    }
    return DEFAULT_VOICE(oracleId);
  };
  
  const fullText = getVoice();
  
  // Effet de machine à écrire
  useEffect(() => {
    if (!isOpen) {
      setDisplayedText('');
      setIsTyping(true);
      return;
    }
    
    setDisplayedText('');
    setIsTyping(true);
    
    let index = 0;
    const speed = stoneName === 'ACIER' ? 20 : stoneName === 'SILENCE' ? 60 : 40;
    
    const timer = setInterval(() => {
      if (index < fullText.length) {
        setDisplayedText(fullText.slice(0, index + 1));
        index++;
      } else {
        setIsTyping(false);
        clearInterval(timer);
      }
    }, speed);
    
    return () => clearInterval(timer);
  }, [isOpen, fullText, stoneName]);
  
  // Fermer avec Escape
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleEscape);
      return () => window.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);
  
  if (!isOpen || !oracle) return null;
  
  const bgColor = stoneColor || '#50C878';
  
  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: 'rgba(0,0,0,0.85)' }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div 
        ref={modalRef}
        className="relative max-w-2xl w-full rounded-2xl overflow-hidden"
        style={{
          backgroundColor: '#1a1a2e',
          border: `2px solid ${bgColor}`,
          boxShadow: `0 0 60px ${bgColor}40`,
        }}
      >
        {/* Header avec avatar */}
        <div 
          className="p-6 border-b"
          style={{ 
            borderColor: bgColor + '40',
            background: `linear-gradient(135deg, ${bgColor}20, transparent)`,
          }}
        >
          <div className="flex items-center gap-4">
            {/* Avatar de l'Oracle */}
            <div 
              className="w-16 h-16 rounded-full flex items-center justify-center text-3xl"
              style={{ 
                backgroundColor: bgColor + '30',
                border: `2px solid ${bgColor}`,
              }}
            >
              {oracle.avatar}
            </div>
            
            {/* Info Oracle */}
            <div>
              <h3 className="text-xl font-bold" style={{ color: bgColor }}>
                {oracle.name}
              </h3>
              <p className="text-sm text-gray-400">
                {oracle.domain} • Oracle #{oracleId}
              </p>
              {stoneName && (
                <span 
                  className="inline-block mt-1 px-2 py-0.5 rounded text-xs"
                  style={{ backgroundColor: bgColor + '30', color: bgColor }}
                >
                  🧱 {stoneName}
                </span>
              )}
            </div>
          </div>
        </div>
        
        {/* Corps - La voix */}
        <div className="p-8">
          <div className="relative">
            {/* Guillemets décoratifs */}
            <span 
              className="absolute -top-4 -left-2 text-6xl opacity-20"
              style={{ color: bgColor }}
            >
              "
            </span>
            
            {/* Texte avec effet machine à écrire */}
            <p 
              className="text-xl leading-relaxed italic text-gray-200 min-h-[120px]"
              style={{ fontFamily: 'Georgia, serif' }}
            >
              {displayedText}
              {isTyping && (
                <span 
                  className="inline-block w-2 h-5 ml-1 animate-pulse"
                  style={{ backgroundColor: bgColor }}
                />
              )}
            </p>
            
            <span 
              className="absolute -bottom-8 -right-2 text-6xl opacity-20"
              style={{ color: bgColor }}
            >
              "
            </span>
          </div>
          
          {/* Mot analysé */}
          {word && (
            <div className="mt-8 pt-4 border-t border-gray-800">
              <p className="text-sm text-gray-500">
                Réflexion sur : <span className="font-bold" style={{ color: bgColor }}>{word}</span>
              </p>
            </div>
          )}
        </div>
        
        {/* Footer */}
        <div className="px-6 py-4 bg-black/30 flex justify-between items-center">
          <p className="text-xs text-gray-500">
            Cliquez à l'extérieur ou appuyez sur Échap pour fermer
          </p>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-sm font-medium transition-all hover:scale-105"
            style={{ 
              backgroundColor: bgColor + '20',
              color: bgColor,
              border: `1px solid ${bgColor}50`,
            }}
          >
            Fermer
          </button>
        </div>
        
        {/* Effet de brillance */}
        <div 
          className="absolute top-0 left-0 w-full h-1"
          style={{ 
            background: `linear-gradient(90deg, transparent, ${bgColor}, transparent)`,
            animation: 'shimmer 2s infinite',
          }}
        />
      </div>
      
      {/* Styles */}
      <style>{`
        @keyframes shimmer {
          0% { opacity: 0.3; transform: translateX(-100%); }
          50% { opacity: 1; }
          100% { opacity: 0.3; transform: translateX(100%); }
        }
      `}</style>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK POUR UTILISATION
// ═══════════════════════════════════════════════════════════════════════════════

export function useOracleVoice() {
  const [modalState, setModalState] = useState({
    isOpen: false,
    oracleId: null,
    stoneName: null,
    stoneColor: null,
    word: null,
  });
  
  const openOracle = (oracleId, stoneName = null, stoneColor = null, word = null) => {
    setModalState({
      isOpen: true,
      oracleId,
      stoneName,
      stoneColor,
      word,
    });
  };
  
  const closeOracle = () => {
    setModalState(prev => ({ ...prev, isOpen: false }));
  };
  
  return {
    modalState,
    openOracle,
    closeOracle,
    OracleVoiceModal: () => (
      <OracleVoiceModal
        isOpen={modalState.isOpen}
        onClose={closeOracle}
        oracleId={modalState.oracleId}
        stoneName={modalState.stoneName}
        stoneColor={modalState.stoneColor}
        word={modalState.word}
      />
    ),
  };
}

export { ORACLE_INFO, STONE_VOICES, DEFAULT_VOICE };
export default OracleVoiceModal;
