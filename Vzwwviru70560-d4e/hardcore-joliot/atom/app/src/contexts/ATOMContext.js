/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *                    CONTEXTE GLOBAL AT·OM — POINT 0 DU SYSTÈME
 *
 *   Extrait de App.js pour éliminer la dépendance circulaire.
 *   Ce fichier est la SOURCE UNIQUE pour :
 *   - Constantes globales (PHI, HEARTBEAT, SOURCE, etc.)
 *   - ATOMContext + ATOMProvider + useATOMContext
 *
 *   Importez TOUJOURS depuis ce fichier, JAMAIS depuis App.js.
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, createContext, useContext } from 'react';
import { useTokenomics } from '../hooks/useTokenomics';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES GLOBALES
// ═══════════════════════════════════════════════════════════════════════════════

export const PHI = 1.6180339887498949;
export const HEARTBEAT = 444;
export const SOURCE = 999;
export const ARCHITECT_NAME = "JONATHAN RODRIGUE";
export const ARCHITECT_ORACLE = 17;

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE GLOBAL AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

export const ATOMContext = createContext(null);

export const ATOMProvider = ({ children }) => {
  // États globaux
  const [frequency, setFrequency] = useState(HEARTBEAT);
  const [isArchitectMode, setIsArchitectMode] = useState(false);
  const [isGratitudeMode, setIsGratitudeMode] = useState(false);
  const [annales, setAnnales] = useState([]);
  const [torusSpeed, setTorusSpeed] = useState(1);

  // Tokenomics — Économie globale accessible partout
  const tokenomics = useTokenomics();

  // Configuration
  const [config, setConfig] = useState({
    animationSpeed: 1,
    frequencyOffset: 0,
    soundEnabled: true,
    particleCount: 50,
    colorScheme: 'gold'
  });

  // Ajouter une entrée aux Annales
  const addToAnnales = (entry) => {
    const newEntry = {
      ...entry,
      id: Date.now(),
      timestamp: new Date().toISOString()
    };
    setAnnales(prev => [newEntry, ...prev].slice(0, 1000)); // Max 1000 entrées

    // Sauvegarder en localStorage
    try {
      const stored = JSON.parse(localStorage.getItem('atom_annales') || '[]');
      localStorage.setItem('atom_annales', JSON.stringify([newEntry, ...stored].slice(0, 1000)));
    } catch (e) {
      console.warn('Erreur localStorage:', e);
    }
  };

  // Charger les Annales au démarrage
  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem('atom_annales') || '[]');
      setAnnales(stored);
    } catch (e) {
      console.warn('Erreur chargement Annales:', e);
    }
  }, []);

  // Activer le Mode Architecte
  const activateArchitectMode = () => {
    setIsArchitectMode(true);
    setFrequency(SOURCE);
    setTorusSpeed(PHI * 2);
  };

  // Désactiver le Mode Architecte
  const deactivateArchitectMode = () => {
    setIsArchitectMode(false);
    setFrequency(HEARTBEAT);
    setTorusSpeed(1);
  };

  const value = {
    // États
    frequency,
    setFrequency,
    isArchitectMode,
    setIsArchitectMode,
    isGratitudeMode,
    setIsGratitudeMode,
    annales,
    setAnnales,
    torusSpeed,
    setTorusSpeed,
    config,
    setConfig,

    // Actions
    addToAnnales,
    activateArchitectMode,
    deactivateArchitectMode,

    // Tokenomics (économie globale)
    tokenomics,

    // Constantes
    PHI,
    HEARTBEAT,
    SOURCE,
    ARCHITECT_NAME,
    ARCHITECT_ORACLE
  };

  return (
    <ATOMContext.Provider value={value}>
      {children}
    </ATOMContext.Provider>
  );
};

// Hook pour utiliser le contexte
export const useATOMContext = () => {
  const context = useContext(ATOMContext);
  if (!context) {
    throw new Error('useATOMContext must be used within ATOMProvider');
  }
  return context;
};
