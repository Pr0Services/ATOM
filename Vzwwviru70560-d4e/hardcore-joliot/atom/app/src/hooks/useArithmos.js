/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ██╗   ██╗███████╗███████╗ █████╗ ██████╗ ██╗████████╗██╗  ██╗███╗   ███╗ ██████╗ ███████╗
 *      ██║   ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██║  ██║████╗ ████║██╔═══██╗██╔════╝
 *      ██║   ██║███████╗█████╗  ███████║██████╔╝██║   ██║   ███████║██╔████╔██║██║   ██║███████╗
 *      ██║   ██║╚════██║██╔══╝  ██╔══██║██╔══██╗██║   ██║   ██╔══██║██║╚██╔╝██║██║   ██║╚════██║
 *      ╚██████╔╝███████║███████╗██║  ██║██║  ██║██║   ██║   ██║  ██║██║ ╚═╝ ██║╚██████╔╝███████║
 *       ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝
 *                                                                                          
 *                                    🔢 HOOK ARITHMOS COMPLET 🔢
 *                                      CALCUL NUMÉRIQUE SACRÉ
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *   Fonctionnalités:
 *   - Calcul Arithmos (1-9) pour tout mot ou phrase
 *   - Gestion des noms composés (ignore espaces, additionne tout)
 *   - Détection du Sceau de l'Architecte (Jonathan Rodrigue = Mode Divin)
 *   - Mapping vers les fréquences, oracles, civilisations
 *   - Historique des calculs
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import { useState, useCallback } from 'react';

// Données de résonance enrichies (chakras étendus, séquences sacrées, matrice 1728)
import RESONANCE_DATA from '../data/resonance_data.json';

// Exporter les données de résonance pour usage externe
export { RESONANCE_DATA };

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = 1.6180339887498949;

// Alphabet Pythagoricien (Gématrie)
const ALPHABET = {
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
  'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
  'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
};

// Sceau de l'Architecte
const ARCHITECT_SIGNATURES = [
  'JONATHAN RODRIGUE',
  'JONATHANRODRIGUE',
  'JONATHAN',
  'ARCHITECTE',
  'ORACLE 17',
  'ORACLE17'
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES DES ARITHMOS
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_DATA = {
  1: {
    name: 'Monade',
    essence: 'Unité',
    principle: 'Commencement',
    frequency: 111,
    color: '#FF0000',
    element: 'Feu Primordial',
    planet: 'Soleil',
    oracle: 'Oracle de l\'Origine',
    civilization: 'Rapa Nui',
    chakra: 1,
    keywords: ['début', 'initiative', 'leadership', 'pionnier'],
    description: 'Le point de départ, la source unique d\'où tout émane.'
  },
  2: {
    name: 'Dyade',
    essence: 'Dualité',
    principle: 'Division',
    frequency: 222,
    color: '#FF7F00',
    element: 'Eau',
    planet: 'Lune',
    oracle: 'Oracle de l\'Équilibre',
    civilization: 'Grèce',
    chakra: 2,
    keywords: ['partenariat', 'équilibre', 'diplomatie', 'réceptivité'],
    description: 'La polarité, le miroir, la relation entre deux forces.'
  },
  3: {
    name: 'Triade',
    essence: 'Harmonie',
    principle: 'Création',
    frequency: 333,
    color: '#FFFF00',
    element: 'Feu',
    planet: 'Jupiter',
    oracle: 'Oracle de la Création',
    civilization: 'Aztèque',
    chakra: 3,
    keywords: ['créativité', 'expression', 'joie', 'expansion'],
    description: 'La synthèse des opposés, la naissance du nouveau.'
  },
  4: {
    name: 'Tétrade',
    essence: 'Stabilité',
    principle: 'Manifestation',
    frequency: 444,
    color: '#00FF00',
    element: 'Terre',
    planet: 'Saturne',
    oracle: 'Oracle de la Structure',
    civilization: 'Égypte',
    chakra: 4,
    keywords: ['fondation', 'ordre', 'discipline', 'construction'],
    description: 'Les 4 directions, les 4 éléments, la base solide.'
  },
  5: {
    name: 'Pentade',
    essence: 'Vie',
    principle: 'Régénération',
    frequency: 555,
    color: '#00BFFF',
    element: 'Éther',
    planet: 'Mercure',
    oracle: 'Oracle du Changement',
    civilization: 'Sumer',
    chakra: 5,
    keywords: ['changement', 'liberté', 'aventure', 'transformation'],
    description: 'Le pentagramme, l\'homme de Vitruve, la vie en mouvement.'
  },
  6: {
    name: 'Hexade',
    essence: 'Équilibre',
    principle: 'Harmonie',
    frequency: 666,
    color: '#4B0082',
    element: 'Air',
    planet: 'Vénus',
    oracle: 'Oracle de l\'Harmonie',
    civilization: 'Maya',
    chakra: 6,
    keywords: ['responsabilité', 'amour', 'famille', 'beauté'],
    description: 'L\'étoile de David, l\'union du haut et du bas.'
  },
  7: {
    name: 'Heptade',
    essence: 'Perfection',
    principle: 'Achèvement',
    frequency: 777,
    color: '#9400D3',
    element: 'Lumière',
    planet: 'Neptune',
    oracle: 'Oracle de la Sagesse',
    civilization: 'Kabbale',
    chakra: 7,
    keywords: ['spiritualité', 'introspection', 'mystère', 'sagesse'],
    description: 'Les 7 jours, les 7 chakras, le nombre de la complétude.'
  },
  8: {
    name: 'Ogdoade',
    essence: 'Infini',
    principle: 'Renouveau',
    frequency: 888,
    color: '#FFC0CB',
    element: 'Énergie',
    planet: 'Mars',
    oracle: 'Oracle de l\'Abondance',
    civilization: 'Yi-King',
    chakra: 8,
    keywords: ['abondance', 'pouvoir', 'succès', 'karma'],
    description: 'L\'infini vertical, le cycle éternel, la puissance.'
  },
  9: {
    name: 'Ennéade',
    essence: 'Accomplissement',
    principle: 'Retour à l\'Unité',
    frequency: 999,
    color: '#FFFDD0',
    element: 'Source',
    planet: 'Pluton',
    oracle: 'Oracle de la Source',
    civilization: 'Atlantide',
    chakra: 9,
    keywords: ['achèvement', 'sagesse universelle', 'humanitaire', 'transcendance'],
    description: 'Le retour à la Source, la fin qui est un commencement.'
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export const useArithmos = () => {
  const [history, setHistory] = useState([]);
  const [lastResult, setLastResult] = useState(null);

  /**
   * Nettoie et normalise un texte pour le calcul
   * - Supprime accents
   * - Met en majuscules
   * - Garde uniquement les lettres (ignore espaces et chiffres)
   */
  const normalizeText = useCallback((text) => {
    return text
      .toUpperCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Supprime les accents
      .replace(/[^A-Z]/g, ''); // Garde uniquement les lettres
  }, []);

  /**
   * Calcule la somme brute des lettres
   */
  const calculateRawSum = useCallback((text) => {
    const normalized = normalizeText(text);
    let sum = 0;
    
    for (const char of normalized) {
      sum += ALPHABET[char] || 0;
    }
    
    return {
      normalized,
      rawSum: sum,
      letterCount: normalized.length
    };
  }, [normalizeText]);

  /**
   * Réduit un nombre à un chiffre (1-9)
   * Théoriquement, on additionne les chiffres jusqu'à obtenir un seul chiffre
   */
  const reduceToSingleDigit = useCallback((num) => {
    const steps = [num];
    
    while (num > 9) {
      num = String(num)
        .split('')
        .reduce((acc, digit) => acc + parseInt(digit, 10), 0);
      steps.push(num);
    }
    
    return {
      finalDigit: num || 9, // Si 0, retourne 9
      steps
    };
  }, []);

  /**
   * Vérifie si le texte est le Sceau de l'Architecte
   */
  const checkArchitectSeal = useCallback((text) => {
    const normalized = normalizeText(text);
    const withSpaces = text.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
    
    return ARCHITECT_SIGNATURES.some(sig => 
      normalized === normalizeText(sig) || withSpaces === sig
    );
  }, [normalizeText]);

  /**
   * Calcul principal de l'Arithmos
   */
  const calculate = useCallback((input) => {
    if (!input || typeof input !== 'string' || input.trim().length === 0) {
      return null;
    }

    const originalInput = input.trim();
    const { normalized, rawSum, letterCount } = calculateRawSum(originalInput);
    const { finalDigit, steps } = reduceToSingleDigit(rawSum);
    const isArchitect = checkArchitectSeal(originalInput);
    
    // Données de l'Arithmos
    const arithmosData = ARITHMOS_DATA[finalDigit];
    
    // Calcul de la fréquence
    const baseFrequency = finalDigit * 111;
    const goldenFrequency = Math.round(baseFrequency * PHI);
    
    // Résultat complet
    const result = {
      // Input
      originalInput,
      normalizedInput: normalized,
      letterCount,
      
      // Calcul
      rawSum,
      reductionSteps: steps,
      arithmos: finalDigit,
      
      // Données
      ...arithmosData,
      baseFrequency,
      goldenFrequency,
      
      // Statuts spéciaux
      isArchitect,
      isSource: finalDigit === 9,
      isHeart: finalDigit === 4,
      
      // Mode visuel
      visualMode: isArchitect ? 'DIVINE' : 
                  finalDigit === 9 ? 'SOURCE' :
                  finalDigit === 4 ? 'HEART' : 'STANDARD',
      
      // Timestamp
      timestamp: new Date().toISOString(),
      id: Date.now()
    };

    // Sauvegarder dans l'historique
    setHistory(prev => [result, ...prev].slice(0, 100));
    setLastResult(result);

    return result;
  }, [calculateRawSum, reduceToSingleDigit, checkArchitectSeal]);

  /**
   * Obtient les données d'un Arithmos spécifique
   */
  const getArithmosData = useCallback((num) => {
    if (num < 1 || num > 9) return null;
    return ARITHMOS_DATA[num];
  }, []);

  /**
   * Obtient tous les Arithmos
   */
  const getAllArithmos = useCallback(() => {
    return ARITHMOS_DATA;
  }, []);

  /**
   * Efface l'historique
   */
  const clearHistory = useCallback(() => {
    setHistory([]);
    setLastResult(null);
  }, []);

  /**
   * Calcule la compatibilité entre deux mots
   */
  const calculateCompatibility = useCallback((word1, word2) => {
    const result1 = calculate(word1);
    const result2 = calculate(word2);
    
    if (!result1 || !result2) return null;
    
    const sum = result1.arithmos + result2.arithmos;
    const { finalDigit: combinedArithmos } = reduceToSingleDigit(sum);
    
    // Calcul de compatibilité
    const diff = Math.abs(result1.arithmos - result2.arithmos);
    const compatibility = 1 - (diff / 9);
    
    // Harmonie basée sur les éléments
    const elementHarmony = result1.element === result2.element ? 1 : 0.5;
    
    return {
      word1: result1,
      word2: result2,
      combinedArithmos,
      compatibility: Math.round(compatibility * 100),
      elementHarmony: Math.round(elementHarmony * 100),
      resonance: result1.arithmos === result2.arithmos ? 'PARFAITE' :
                 diff <= 2 ? 'FORTE' :
                 diff <= 4 ? 'MODÉRÉE' : 'FAIBLE',
      combinedFrequency: result1.baseFrequency + result2.baseFrequency
    };
  }, [calculate, reduceToSingleDigit]);

  // Retour du hook
  return {
    // Fonction principale
    calculate,
    
    // Utilitaires
    normalizeText,
    reduceToSingleDigit,
    checkArchitectSeal,
    getArithmosData,
    getAllArithmos,
    calculateCompatibility,
    
    // États
    history,
    lastResult,
    clearHistory,
    
    // Constantes
    ALPHABET,
    ARITHMOS_DATA,
    PHI
  };
};

export default useArithmos;
