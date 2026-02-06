/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
 *      ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
 *      █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
 *      ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
 *      ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
 *      ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
 *                                                                                          
 *                                    🔥 LA FORGE - LE FEU 🔥
 *                                      CONFIGURATION ET PARAMÈTRES
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState } from 'react';
import { useATOMContext, PHI } from '../contexts/ATOMContext';

const ForgePage = () => {
  const { 
    config, 
    setConfig, 
    frequency,
    setFrequency,
    torusSpeed,
    setTorusSpeed,
    annales,
    setAnnales
  } = useATOMContext();

  const [showAdvanced, setShowAdvanced] = useState(false);

  // Mettre à jour une config
  const updateConfig = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  // Réinitialiser tout
  const resetAll = () => {
    if (window.confirm('Réinitialiser toutes les configurations et effacer les données ?')) {
      setConfig({
        animationSpeed: 1,
        frequencyOffset: 0,
        soundEnabled: true,
        particleCount: 50,
        colorScheme: 'gold'
      });
      setAnnales([]);
      setFrequency(444);
      setTorusSpeed(1);
      localStorage.clear();
    }
  };

  // Exporter les données
  const exportData = () => {
    const data = {
      annales,
      config,
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `atom-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Importer les données
  const importData = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.annales) setAnnales(data.annales);
        if (data.config) setConfig(data.config);
        alert('Données importées avec succès !');
      } catch (err) {
        alert('Erreur lors de l\'importation : ' + err.message);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="min-h-[70vh] px-4 py-6">
      
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500 tracking-widest mb-2">
          🔥 LA FORGE
        </h1>
        <p className="text-gray-500 text-sm">Le Feu (Nord) — Configuration et Paramètres</p>
      </div>

      <div className="max-w-2xl mx-auto space-y-6">

        {/* ANIMATION */}
        <div className="bg-black/50 rounded-lg border border-yellow-900/30 p-6">
          <h2 className="text-lg font-bold text-yellow-400 mb-4">🌀 Animation Toroïdale</h2>
          
          <div className="space-y-4">
            {/* Vitesse */}
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-gray-400">Vitesse du Flux</label>
                <span className="text-yellow-400">{torusSpeed.toFixed(2)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="3"
                step="0.1"
                value={torusSpeed}
                onChange={(e) => setTorusSpeed(parseFloat(e.target.value))}
                className="w-full accent-yellow-500"
              />
              <div className="flex justify-between text-xs text-gray-600 mt-1">
                <span>Lent</span>
                <span>φ ({PHI.toFixed(2)})</span>
                <span>Rapide</span>
              </div>
            </div>

            {/* Particules */}
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-gray-400">Nombre de Particules</label>
                <span className="text-yellow-400">{config.particleCount}</span>
              </div>
              <input
                type="range"
                min="20"
                max="100"
                step="10"
                value={config.particleCount}
                onChange={(e) => updateConfig('particleCount', parseInt(e.target.value))}
                className="w-full accent-yellow-500"
              />
            </div>

            {/* Boutons rapides */}
            <div className="flex gap-2">
              <button
                onClick={() => setTorusSpeed(1)}
                className="flex-1 py-2 bg-yellow-900/20 rounded text-yellow-400 hover:bg-yellow-900/40 transition-all"
              >
                Normal (1x)
              </button>
              <button
                onClick={() => setTorusSpeed(PHI)}
                className="flex-1 py-2 bg-yellow-600/20 rounded text-yellow-400 hover:bg-yellow-600/40 transition-all"
              >
                Doré (φ)
              </button>
              <button
                onClick={() => setTorusSpeed(PHI * 2)}
                className="flex-1 py-2 bg-white/10 rounded text-white hover:bg-white/20 transition-all"
              >
                Divin (2φ)
              </button>
            </div>
          </div>
        </div>

        {/* FRÉQUENCE */}
        <div className="bg-black/50 rounded-lg border border-yellow-900/30 p-6">
          <h2 className="text-lg font-bold text-yellow-400 mb-4">〰️ Fréquence de Base</h2>
          
          <div className="space-y-4">
            {/* Fréquence actuelle */}
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-gray-400">Fréquence Actuelle</label>
                <span className="text-yellow-400 font-mono text-xl">{frequency} Hz</span>
              </div>
              <input
                type="range"
                min="111"
                max="999"
                step="111"
                value={frequency}
                onChange={(e) => setFrequency(parseInt(e.target.value))}
                className="w-full accent-yellow-500"
              />
            </div>

            {/* Offset */}
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-gray-400">Offset de Fréquence</label>
                <span className="text-yellow-400">{config.frequencyOffset > 0 ? '+' : ''}{config.frequencyOffset} Hz</span>
              </div>
              <input
                type="range"
                min="-50"
                max="50"
                step="1"
                value={config.frequencyOffset}
                onChange={(e) => updateConfig('frequencyOffset', parseInt(e.target.value))}
                className="w-full accent-yellow-500"
              />
            </div>

            {/* Boutons de fréquence */}
            <div className="grid grid-cols-3 gap-2">
              {[111, 222, 333, 444, 555, 666, 777, 888, 999].map(hz => (
                <button
                  key={hz}
                  onClick={() => setFrequency(hz)}
                  className={`py-2 rounded transition-all ${
                    frequency === hz
                      ? 'bg-yellow-500 text-black'
                      : 'bg-yellow-900/20 text-yellow-400 hover:bg-yellow-900/40'
                  }`}
                >
                  {hz} Hz
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* THÈME */}
        <div className="bg-black/50 rounded-lg border border-yellow-900/30 p-6">
          <h2 className="text-lg font-bold text-yellow-400 mb-4">🎨 Apparence</h2>
          
          <div className="space-y-4">
            {/* Schéma de couleurs */}
            <div>
              <label className="text-gray-400 block mb-2">Schéma de Couleurs</label>
              <div className="flex gap-2">
                {[
                  { id: 'gold', label: 'Or', color: '#D4AF37' },
                  { id: 'silver', label: 'Argent', color: '#C0C0C0' },
                  { id: 'emerald', label: 'Émeraude', color: '#50C878' },
                  { id: 'sapphire', label: 'Saphir', color: '#0F52BA' }
                ].map(scheme => (
                  <button
                    key={scheme.id}
                    onClick={() => updateConfig('colorScheme', scheme.id)}
                    className={`flex-1 py-2 rounded flex items-center justify-center gap-2 transition-all ${
                      config.colorScheme === scheme.id
                        ? 'ring-2 ring-white'
                        : 'hover:opacity-80'
                    }`}
                    style={{ backgroundColor: scheme.color + '30', color: scheme.color }}
                  >
                    <span className="w-3 h-3 rounded-full" style={{ backgroundColor: scheme.color }} />
                    {scheme.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Son */}
            <div className="flex justify-between items-center">
              <label className="text-gray-400">Son Activé</label>
              <button
                onClick={() => updateConfig('soundEnabled', !config.soundEnabled)}
                className={`w-12 h-6 rounded-full transition-all ${
                  config.soundEnabled ? 'bg-yellow-500' : 'bg-gray-700'
                }`}
              >
                <div className={`w-5 h-5 rounded-full bg-white transition-all ${
                  config.soundEnabled ? 'translate-x-6' : 'translate-x-0.5'
                }`} />
              </button>
            </div>
          </div>
        </div>

        {/* DONNÉES */}
        <div className="bg-black/50 rounded-lg border border-yellow-900/30 p-6">
          <h2 className="text-lg font-bold text-yellow-400 mb-4">💾 Données</h2>
          
          <div className="space-y-4">
            {/* Stats */}
            <div className="grid grid-cols-2 gap-4 text-center">
              <div className="p-4 bg-yellow-900/10 rounded">
                <p className="text-2xl font-bold text-yellow-400">{annales.length}</p>
                <p className="text-xs text-gray-500">Entrées dans les Annales</p>
              </div>
              <div className="p-4 bg-yellow-900/10 rounded">
                <p className="text-2xl font-bold text-yellow-400">
                  {(JSON.stringify(annales).length / 1024).toFixed(1)} KB
                </p>
                <p className="text-xs text-gray-500">Taille des données</p>
              </div>
            </div>

            {/* Boutons */}
            <div className="flex gap-2">
              <button
                onClick={exportData}
                className="flex-1 py-2 bg-green-900/20 border border-green-600/50 rounded text-green-400 hover:bg-green-600 hover:text-white transition-all"
              >
                📥 Exporter
              </button>
              <label className="flex-1 py-2 bg-blue-900/20 border border-blue-600/50 rounded text-blue-400 hover:bg-blue-600 hover:text-white transition-all text-center cursor-pointer">
                📤 Importer
                <input type="file" accept=".json" onChange={importData} className="hidden" />
              </label>
            </div>
          </div>
        </div>

        {/* AVANCÉ */}
        <div className="bg-black/50 rounded-lg border border-red-900/30 p-6">
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="w-full flex justify-between items-center text-red-400"
          >
            <span className="font-bold">⚠️ Options Avancées</span>
            <span>{showAdvanced ? '▼' : '▶'}</span>
          </button>
          
          {showAdvanced && (
            <div className="mt-4 space-y-4">
              <button
                onClick={resetAll}
                className="w-full py-3 bg-red-900/20 border border-red-600 rounded text-red-400 hover:bg-red-600 hover:text-white transition-all"
              >
                🗑️ Réinitialiser Tout
              </button>
              <p className="text-xs text-gray-500 text-center">
                Cette action effacera toutes les données et réinitialisera les paramètres.
              </p>
            </div>
          )}
        </div>

        {/* INFO */}
        <div className="text-center text-sm text-gray-600 space-y-1">
          <p>AT·OM v4.0 — L'Arche des Résonances Universelles</p>
          <p>Architecte: Jonathan Rodrigue | Oracle 17</p>
          <p>φ = {PHI.toFixed(10)}</p>
        </div>

      </div>
    </div>
  );
};

export default ForgePage;
