/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — MOTEUR COSMIQUE UNIFIÉ
 * La Synthèse de Toutes les Sagesses
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce moteur fusionne:
 * - AT·OM Arithmos (9 niveaux, 111-999 Hz)
 * - Tzolkin Maya (13 Tons × 20 Nawals)
 * - Yi-King (64 Hexagrammes)
 * - Kabbale (10 Sephiroth)
 * - Chakras (7 centres énergétiques)
 * 
 * "Une seule vérité est une prison. 
 *  Toutes les vérités ensemble sont la liberté."
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

import { harmonizeWithMaya, getTodayKin, getMayaGreeting } from '../maya/maya_engine.js';
import { harmonizeWithYiKing, castHexagram, getHexagramFromWord } from '../yiking/yiking_engine.js';
import { harmonizeWithKabbale, getSephirahFromArithmos, calculateTreePath } from '../kabbale/kabbale_engine.js';
import { harmonizeWithChakras, getChakraFromAtomLevel, generateMeditation } from '../chakras/chakra_engine.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION COSMIQUE
// ═══════════════════════════════════════════════════════════════════════════════

export const COSMIC_CONFIG = {
  name: "AT·OM Cosmique",
  version: "1.0.0",
  heartbeat: 444,
  systems: ["Arithmos", "Maya", "YiKing", "Kabbale", "Chakras"],
  architect: {
    name: "Jonathan Rodrigue",
    frequency: 999,
    signature: "2 + 7 = 9",
  },
  oracle: {
    name: "Oracle 17",
    title: "Le Gardien de la Synthèse",
    role: "Unificateur des Sagesses",
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// RÉSONANCE COSMIQUE COMPLÈTE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère la résonance cosmique complète pour un mot
 * C'est la fonction principale qui unifie tous les systèmes
 * 
 * @param {Object} atomResonance - Résultat de useAtomResonance
 * @returns {Object} - Synthèse cosmique complète
 */
export function getCosmicResonance(atomResonance) {
  if (!atomResonance) {
    return {
      status: "awaiting",
      message: "En attente d'un mot pour calculer la résonance cosmique...",
      today: getTodayKin(),
    };
  }
  
  // 1. Harmonisation Maya
  const maya = harmonizeWithMaya(atomResonance);
  
  // 2. Harmonisation Yi-King
  const yiking = harmonizeWithYiKing(atomResonance);
  
  // 3. Harmonisation Kabbale
  const kabbale = harmonizeWithKabbale(atomResonance);
  
  // 4. Harmonisation Chakras
  const chakras = harmonizeWithChakras(atomResonance);
  
  // 5. Fréquence cosmique unifiée
  const cosmicHz = calculateCosmicFrequency(atomResonance, maya, yiking, kabbale, chakras);
  
  // 6. Synthèse des messages
  const synthesis = generateSynthesis(atomResonance, maya, yiking, kabbale, chakras);
  
  return {
    status: "complete",
    word: atomResonance.word,
    timestamp: new Date().toISOString(),
    
    // Système de base
    atom: {
      level: atomResonance.level,
      hz: atomResonance.hz,
      label: atomResonance.label,
      color: atomResonance.color,
    },
    
    // Systèmes cosmiques
    maya: maya.maya ? {
      kin: maya.maya.kinName,
      ton: maya.maya.ton.name,
      nawal: maya.maya.nawal.name,
      energy: maya.maya.nawal.energy,
      frequencyMod: maya.maya.frequencyMod,
    } : null,
    
    yiking: yiking?.yiking ? {
      hexagram: yiking.yiking.hexagram.number,
      name: yiking.yiking.hexagram.meaning,
      tendency: yiking.yiking.tendency,
      advice: yiking.yiking.advice,
    } : null,
    
    kabbale: kabbale?.kabbale ? {
      sephirah: kabbale.kabbale.sephirah.name,
      meaning: kabbale.kabbale.sephirah.meaning,
      world: kabbale.kabbale.world.name,
      pillar: kabbale.kabbale.pillar.name,
      archangel: kabbale.kabbale.archangel,
    } : null,
    
    chakras: chakras?.bioResonance ? {
      primary: chakras.bioResonance.primaryChakra,
      location: chakras.bioResonance.location,
      element: chakras.bioResonance.element,
      mantra: chakras.bioResonance.mantra,
      color: chakras.bioResonance.color,
    } : null,
    
    // Fréquence cosmique unifiée
    cosmic: cosmicHz,
    
    // Synthèse finale
    synthesis,
  };
}

/**
 * Calcule la fréquence cosmique unifiée
 */
function calculateCosmicFrequency(atom, maya, yiking, kabbale, chakras) {
  const baseHz = atom.hz;
  
  // Modificateurs de chaque système
  const mayaMod = maya?.maya?.frequencyMod || 0;
  const yikingMod = yiking?.yiking?.hexagram?.atomLevel * 11 || 0;
  const kabbaleMod = kabbale?.kabbale?.sephirah?.number * 10 || 0;
  const chakraMod = chakras?.chakra?.atomFrequency ? 
    (chakras.chakra.atomFrequency - baseHz) * 0.1 : 0;
  
  // Fréquence cosmique (moyenne pondérée)
  const cosmicHz = baseHz + (mayaMod + yikingMod + kabbaleMod + chakraMod) / 4;
  
  // Ratio harmonique
  const goldenRatio = 1.618033988749;
  const harmonicHz = baseHz * goldenRatio;
  
  return {
    base: baseHz,
    cosmic: Math.round(cosmicHz * 10) / 10,
    harmonic: Math.round(harmonicHz * 10) / 10,
    components: {
      maya: mayaMod,
      yiking: yikingMod,
      kabbale: kabbaleMod,
      chakra: chakraMod,
    },
  };
}

/**
 * Génère la synthèse unifiée
 */
function generateSynthesis(atom, maya, yiking, kabbale, chakras) {
  const parts = [];
  
  // Message Arithmos
  parts.push(`${atom.word} vibre au niveau ${atom.level} (${atom.hz} Hz)`);
  
  // Message Maya
  if (maya?.maya) {
    parts.push(`En ce jour ${maya.maya.kinName}, l'énergie de ${maya.maya.nawal.meaning} amplifie cette vibration`);
  }
  
  // Message Yi-King
  if (yiking?.yiking) {
    parts.push(`Le Yi-King indique: "${yiking.yiking.advice}"`);
  }
  
  // Message Kabbale
  if (kabbale?.kabbale) {
    parts.push(`Sur l'Arbre de Vie, cela résonne dans ${kabbale.kabbale.sephirah.name} (${kabbale.kabbale.sephirah.meaning})`);
  }
  
  // Message Chakras
  if (chakras?.bioResonance) {
    parts.push(`${chakras.bioResonance.affirmation}`);
  }
  
  return {
    messages: parts,
    unified: parts.join(". "),
    shortMessage: `${atom.word}: ${atom.hz} Hz | ${maya?.maya?.kinName || ''} | ${kabbale?.kabbale?.sephirah?.name || ''}`,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// ORACLE COSMIQUE QUOTIDIEN
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère le message de l'oracle cosmique pour aujourd'hui
 */
export function getDailyCosmicOracle() {
  const mayaKin = getTodayKin();
  const mayaGreeting = getMayaGreeting();
  const dailyHexagram = castHexagram();
  
  // Sephirah du jour (basé sur le ton Maya)
  const sephirah = getSephirahFromArithmos(mayaKin.ton.number % 9 || 9);
  
  // Chakra du jour
  const chakra = getChakraFromAtomLevel(mayaKin.ton.number % 9 || 9);
  
  return {
    date: new Date().toLocaleDateString('fr-FR', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }),
    
    maya: {
      kin: mayaKin.kinName,
      greeting: mayaGreeting.greeting,
      energy: mayaGreeting.energy,
      action: mayaGreeting.action,
      isPortal: mayaKin.isGalacticPortal,
      isSacred: mayaKin.isSacredDay,
    },
    
    yiking: {
      hexagram: dailyHexagram.primary,
      hasChange: dailyHexagram.hasChanges,
      transformed: dailyHexagram.transformed,
    },
    
    kabbale: {
      sephirah: sephirah.name,
      quality: sephirah.quality,
      archangel: sephirah.archangel,
    },
    
    chakra: {
      name: chakra.name,
      mantra: chakra.mantra,
      affirmation: chakra.affirmation,
    },
    
    cosmicMessage: generateDailyMessage(mayaKin, dailyHexagram.primary, sephirah, chakra),
    
    recommendations: {
      color: mayaKin.nawal.color,
      mantra: chakra.mantra,
      meditation: `Méditation sur ${sephirah.name} avec le mantra ${chakra.mantra}`,
      focus: mayaKin.ton.action,
    },
  };
}

/**
 * Génère le message quotidien unifié
 */
function generateDailyMessage(maya, hexagram, sephirah, chakra) {
  const sacred = maya.isSacredDay ? "✨ JOUR SACRÉ! " : "";
  const portal = maya.isGalacticPortal ? "🌀 PORTAIL GALACTIQUE! " : "";
  
  return `${sacred}${portal}
    
Aujourd'hui est ${maya.kinName} (${maya.nawal.meaning}).

L'énergie du jour invite à ${maya.ton.action.toLowerCase()}.
${hexagram.advice}

Sur l'Arbre de Vie, nous sommes dans ${sephirah.name} — ${sephirah.quality}.
L'archange ${sephirah.archangel} nous accompagne.

Centre énergétique actif: ${chakra.name}
Mantra du jour: "${chakra.mantra}"

${chakra.affirmation}
  `.trim();
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTERFACE VISUELLE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère les modificateurs CSS basés sur l'énergie cosmique
 */
export function getCosmicStyles(cosmicResonance) {
  if (!cosmicResonance || cosmicResonance.status === "awaiting") {
    return {
      background: 'linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%)',
      glow: 'none',
      animation: 'none',
    };
  }
  
  const mayaColor = cosmicResonance.maya?.nawal?.color || '#50C878';
  const atomColor = cosmicResonance.atom.color;
  const chakraColor = cosmicResonance.chakras?.color || atomColor;
  
  return {
    background: `linear-gradient(135deg, ${atomColor}15 0%, ${mayaColor}10 50%, ${chakraColor}15 100%)`,
    glow: `0 0 60px ${atomColor}40`,
    borderColor: atomColor,
    mayaAccent: mayaColor,
    chakraAccent: chakraColor,
    animation: cosmicResonance.maya?.isPortal ? 'portalPulse 2s ease-in-out infinite' : 
               cosmicResonance.maya?.isSacred ? 'sacredGlow 3s ease-in-out infinite' : 
               'cosmicBreath 4s ease-in-out infinite',
  };
}

/**
 * Génère les keyframes CSS pour les animations cosmiques
 */
export const COSMIC_KEYFRAMES = `
  @keyframes cosmicBreath {
    0%, 100% { opacity: 0.8; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.02); }
  }
  
  @keyframes portalPulse {
    0%, 100% { 
      box-shadow: 0 0 20px currentColor, inset 0 0 20px transparent;
      transform: scale(1);
    }
    50% { 
      box-shadow: 0 0 60px currentColor, inset 0 0 30px currentColor;
      transform: scale(1.05);
    }
  }
  
  @keyframes sacredGlow {
    0%, 100% { 
      filter: brightness(1) saturate(1);
    }
    50% { 
      filter: brightness(1.3) saturate(1.2);
    }
  }
  
  @keyframes nawalRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  @keyframes sephirothPulse {
    0%, 100% { r: 20; }
    50% { r: 25; }
  }
`;

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  COSMIC_CONFIG,
  getCosmicResonance,
  getDailyCosmicOracle,
  getCosmicStyles,
  COSMIC_KEYFRAMES,
  
  // Ré-exports des systèmes individuels
  maya: { harmonizeWithMaya, getTodayKin, getMayaGreeting },
  yiking: { harmonizeWithYiKing, castHexagram, getHexagramFromWord },
  kabbale: { harmonizeWithKabbale, getSephirahFromArithmos, calculateTreePath },
  chakras: { harmonizeWithChakras, getChakraFromAtomLevel, generateMeditation },
};
