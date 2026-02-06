import React, { useState, useEffect } from 'react';

const ZamaIgnitionStoryboard = () => {
  const [activePhase, setActivePhase] = useState(0);
  const [bpm, setBpm] = useState(72);
  const [pulseScale, setPulseScale] = useState(1);

  // Simulate heartbeat pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setPulseScale(prev => prev === 1 ? 1.1 : 1);
    }, 60000 / bpm);
    return () => clearInterval(interval);
  }, [bpm]);

  const phases = [
    { name: 'CALIBRATION', icon: '◎', color: '#A8C5D8' },
    { name: 'ACTIVATION', icon: '⚡', color: '#D4AF37' },
    { name: 'DASHBOARD', icon: '🛡️', color: '#8A2BE2' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-black text-white p-4">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-2xl font-bold text-amber-400">CHE·NU™ / ZAMA IGNITION</h1>
        <p className="text-gray-400 text-sm">Module RA - Storyboard Interface</p>
      </div>

      {/* Phase Selector */}
      <div className="flex justify-center gap-4 mb-8">
        {phases.map((phase, idx) => (
          <button
            key={idx}
            onClick={() => setActivePhase(idx)}
            className={`px-4 py-2 rounded-lg transition-all ${
              activePhase === idx 
                ? 'bg-amber-500 text-black font-bold scale-105' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            <span className="mr-2">{phase.icon}</span>
            {phase.name}
          </button>
        ))}
      </div>

      {/* Phone Frame */}
      <div className="flex justify-center">
        <div className="relative w-80 h-[640px] bg-black rounded-[40px] p-3 shadow-2xl border-4 border-gray-700">
          {/* Notch */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-black rounded-b-2xl z-20" />
          
          {/* Screen */}
          <div className="w-full h-full bg-gradient-to-b from-gray-900 to-gray-950 rounded-[32px] overflow-hidden relative">
            
            {/* PHASE 1: CALIBRATION */}
            {activePhase === 0 && (
              <div className="h-full flex flex-col">
                {/* Status Bar */}
                <div className="flex justify-between px-6 py-2 text-xs text-gray-400">
                  <span>9:41</span>
                  <span>◉ ZAMA</span>
                  <span>🔋 85%</span>
                </div>
                
                {/* Title */}
                <div className="px-4 py-2">
                  <h2 className="text-lg font-bold text-cyan-400">CALIBRATION</h2>
                  <p className="text-xs text-gray-500">Scanning anchor points...</p>
                </div>

                {/* Body Silhouette */}
                <div className="flex-1 relative flex justify-center items-center">
                  <svg viewBox="0 0 200 400" className="w-48 h-80 opacity-30">
                    <ellipse cx="100" cy="45" rx="35" ry="40" fill="#4A5568" />
                    <rect x="70" y="85" width="60" height="120" rx="10" fill="#4A5568" />
                    <rect x="30" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="130" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="75" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                    <rect x="103" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                  </svg>
                  
                  {/* Anchor Points */}
                  <div className="absolute top-16 left-1/2 transform -translate-x-1/2">
                    <div className="w-4 h-4 rounded-full bg-cyan-400 animate-ping" />
                    <span className="absolute -right-16 top-0 text-xs text-cyan-400">C7 Nuque</span>
                  </div>
                  <div className="absolute top-36 left-1/2 transform -translate-x-1/2">
                    <div className="w-4 h-4 rounded-full bg-amber-400 animate-ping" style={{animationDelay: '0.5s'}} />
                    <span className="absolute -right-16 top-0 text-xs text-amber-400">Plexus</span>
                  </div>
                  <div className="absolute top-44 left-24">
                    <div className="w-3 h-3 rounded-full bg-blue-400 animate-ping" style={{animationDelay: '1s'}} />
                    <span className="absolute -left-16 top-0 text-xs text-blue-400">Poignet L</span>
                  </div>
                  <div className="absolute top-44 right-24">
                    <div className="w-3 h-3 rounded-full bg-blue-400 animate-ping" style={{animationDelay: '1s'}} />
                    <span className="absolute -right-16 top-0 text-xs text-blue-400">Poignet R</span>
                  </div>
                </div>

                {/* Progress */}
                <div className="px-6 py-4">
                  <div className="flex justify-between text-xs text-gray-400 mb-1">
                    <span>STATUS: Scanning...</span>
                    <span>62%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-cyan-500 to-amber-500 w-3/5 animate-pulse" />
                  </div>
                </div>

                {/* Button */}
                <div className="px-6 pb-8">
                  <button className="w-full py-3 bg-gray-700 text-gray-300 rounded-xl">
                    ANNULER
                  </button>
                </div>
              </div>
            )}

            {/* PHASE 2: ACTIVATION */}
            {activePhase === 1 && (
              <div className="h-full flex flex-col">
                {/* Status Bar */}
                <div className="flex justify-between px-6 py-2 text-xs text-gray-400">
                  <span>9:42</span>
                  <span className="text-amber-400">⚡ ACTIVATION</span>
                  <span>🔋 84%</span>
                </div>
                
                {/* Title */}
                <div className="px-4 py-2">
                  <h2 className="text-lg font-bold text-amber-400">ACTIVATION EN COURS</h2>
                  <p className="text-xs text-gray-500">Séquençage du circuit énergétique...</p>
                </div>

                {/* Body with Glowing Symbols */}
                <div className="flex-1 relative flex justify-center items-center">
                  <svg viewBox="0 0 200 400" className="w-48 h-80 opacity-20">
                    <ellipse cx="100" cy="45" rx="35" ry="40" fill="#4A5568" />
                    <rect x="70" y="85" width="60" height="120" rx="10" fill="#4A5568" />
                    <rect x="30" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="130" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="75" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                    <rect x="103" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                  </svg>
                  
                  {/* Metatron Cube - Active */}
                  <div className="absolute top-12 left-1/2 transform -translate-x-1/2">
                    <div className="relative">
                      <div className="w-12 h-12 rounded-full bg-purple-500/30 animate-pulse absolute -inset-2" />
                      <div className="w-8 h-8 border-2 border-purple-400 rotate-45 flex items-center justify-center">
                        <div className="w-4 h-4 border border-purple-300 rotate-45" />
                      </div>
                    </div>
                  </div>
                  
                  {/* Nadi Lines - Flowing */}
                  <svg className="absolute inset-0 w-full h-full" viewBox="0 0 200 400">
                    <defs>
                      <linearGradient id="nadiGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#8A2BE2" stopOpacity="0.8" />
                        <stop offset="100%" stopColor="#D4AF37" stopOpacity="0.8" />
                      </linearGradient>
                    </defs>
                    <path 
                      d="M100 60 L100 140" 
                      stroke="url(#nadiGradient)" 
                      strokeWidth="2" 
                      strokeDasharray="4,4"
                      className="animate-pulse"
                    />
                  </svg>
                  
                  {/* Flower of Life - Pulsing with BPM */}
                  <div 
                    className="absolute top-32 left-1/2 transform -translate-x-1/2 transition-transform"
                    style={{ transform: `translate(-50%, 0) scale(${pulseScale})` }}
                  >
                    <div className="relative">
                      <div className="w-16 h-16 rounded-full bg-amber-500/20 animate-pulse absolute -inset-3" />
                      <div className="w-10 h-10 rounded-full border-2 border-amber-400 flex items-center justify-center">
                        <div className="w-4 h-4 rounded-full border border-amber-300" />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Activation Progress */}
                <div className="px-4 py-2 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-purple-400">⬡ CUBE MÉTATRON</span>
                    <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-purple-500 w-full" />
                    </div>
                    <span className="text-green-400">✓</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-cyan-400">◎ NADI CONNEXION</span>
                    <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-cyan-500 w-3/4 animate-pulse" />
                    </div>
                    <span className="text-gray-500">...</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-amber-400">❀ FLEUR DE VIE</span>
                    <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-amber-500 w-1/2" />
                    </div>
                    <span className="text-gray-500">...</span>
                  </div>
                </div>

                {/* BPM Indicator */}
                <div className="px-6 py-2 flex items-center justify-center gap-4 text-sm">
                  <span className="text-red-400 animate-pulse">♡</span>
                  <span className="text-gray-300">BPM: {bpm}</span>
                  <span className="text-green-400">SYNC: Active</span>
                </div>

                {/* Buttons */}
                <div className="px-6 pb-8 flex gap-4">
                  <button className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-xl">
                    PAUSE
                  </button>
                  <button className="flex-1 py-3 bg-amber-600 text-black font-bold rounded-xl">
                    SKIP →
                  </button>
                </div>
              </div>
            )}

            {/* PHASE 3: DASHBOARD */}
            {activePhase === 2 && (
              <div className="h-full flex flex-col">
                {/* Status Bar */}
                <div className="flex justify-between px-6 py-2 text-xs text-gray-400">
                  <span>9:45</span>
                  <span className="text-green-400">🛡️ ACTIVE</span>
                  <span>🔋 83%</span>
                </div>
                
                {/* Title */}
                <div className="px-4 py-2">
                  <h2 className="text-lg font-bold text-green-400">ARMURE ZAMA</h2>
                  <p className="text-xs text-gray-500">Circuit énergétique actif</p>
                </div>

                {/* Full Armor Visualization */}
                <div className="flex-1 relative flex justify-center items-center">
                  {/* Aura Effect */}
                  <div className="absolute inset-0 flex justify-center items-center">
                    <div className="w-56 h-72 rounded-full bg-gradient-to-b from-purple-500/10 via-amber-500/10 to-cyan-500/10 blur-xl animate-pulse" />
                  </div>
                  
                  <svg viewBox="0 0 200 400" className="w-48 h-80 opacity-30">
                    <ellipse cx="100" cy="45" rx="35" ry="40" fill="#4A5568" />
                    <rect x="70" y="85" width="60" height="120" rx="10" fill="#4A5568" />
                    <rect x="30" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="130" y="90" width="40" height="100" rx="8" fill="#4A5568" />
                    <rect x="75" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                    <rect x="103" y="205" width="22" height="120" rx="8" fill="#4A5568" />
                  </svg>
                  
                  {/* All Symbols Active */}
                  <div className="absolute top-12 left-1/2 transform -translate-x-1/2">
                    <div className="w-10 h-10 border-2 border-purple-400 rotate-45 opacity-80" />
                  </div>
                  <div 
                    className="absolute top-32 left-1/2 transform -translate-x-1/2"
                    style={{ transform: `translate(-50%, 0) scale(${pulseScale})` }}
                  >
                    <div className="w-12 h-12 rounded-full border-2 border-amber-400 opacity-80" />
                  </div>
                  <div className="absolute top-44 left-20">
                    <div className="w-4 h-2 text-cyan-400 text-lg">∞</div>
                  </div>
                  <div className="absolute top-44 right-20">
                    <div className="w-4 h-2 text-cyan-400 text-lg">∞</div>
                  </div>
                  <div className="absolute bottom-32 left-28">
                    <div className="w-4 h-4 text-green-400 text-xs">☯</div>
                  </div>
                  <div className="absolute bottom-32 right-28">
                    <div className="w-4 h-4 text-green-400 text-xs">☯</div>
                  </div>
                </div>

                {/* Mode Toggle */}
                <div className="px-6 py-2">
                  <div className="flex items-center justify-center gap-6 bg-gray-800 rounded-xl p-3">
                    <span className="text-gray-500">MODE:</span>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="mode" className="hidden" />
                      <span className="px-3 py-1 bg-gray-700 rounded-lg text-gray-400 text-sm">
                        ⚔️ Combat
                      </span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="mode" defaultChecked className="hidden" />
                      <span className="px-3 py-1 bg-purple-600 rounded-lg text-white text-sm">
                        🌙 Repos
                      </span>
                    </label>
                  </div>
                </div>

                {/* Energy Charge */}
                <div className="px-6 py-2">
                  <div className="flex justify-between text-xs text-gray-400 mb-1">
                    <span>CHARGE ÉNERGÉTIQUE</span>
                    <span className="text-green-400">78%</span>
                  </div>
                  <div className="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-green-500 via-amber-500 to-green-500 w-4/5" />
                  </div>
                </div>

                {/* Detected Stones */}
                <div className="px-6 py-2">
                  <p className="text-xs text-gray-500 mb-2">PIERRES DÉTECTÉES:</p>
                  <div className="space-y-1 text-xs">
                    <div className="flex items-center gap-2">
                      <span className="text-green-400">✓</span>
                      <span className="text-amber-300">Œil de Tigre</span>
                      <span className="text-gray-500">(Plexus)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-400">✓</span>
                      <span className="text-gray-300">Tourmaline Noire</span>
                      <span className="text-gray-500">(Poignets)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600">○</span>
                      <span className="text-gray-500">Hématite</span>
                      <span className="text-gray-600">(Non détectée)</span>
                    </div>
                  </div>
                </div>

                {/* Buttons */}
                <div className="px-6 pb-8 flex gap-4">
                  <button className="flex-1 py-3 bg-red-900/50 text-red-300 rounded-xl border border-red-700">
                    DÉSACTIVER
                  </button>
                  <button className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-xl">
                    ⚙️ PARAMS
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Phase Description */}
      <div className="mt-8 max-w-md mx-auto text-center">
        <div className="bg-gray-800 rounded-xl p-4">
          {activePhase === 0 && (
            <>
              <h3 className="text-cyan-400 font-bold mb-2">Phase 1: Calibration</h3>
              <p className="text-gray-400 text-sm">
                L'app scanne le corps via la caméra pour identifier les "Anchor Points" 
                (tatouages Fine Line). Des micro-points de lumière apparaissent sur les zones clés.
              </p>
            </>
          )}
          {activePhase === 1 && (
            <>
              <h3 className="text-amber-400 font-bold mb-2">Phase 2: Activation Séquencée</h3>
              <p className="text-gray-400 text-sm">
                Le circuit s'active dans l'ordre: Core (Métatron) → Connexions (Nadi) → 
                Cœur (Fleur de Vie). La Fleur pulse au rythme du BPM détecté.
              </p>
            </>
          )}
          {activePhase === 2 && (
            <>
              <h3 className="text-green-400 font-bold mb-2">Phase 3: Dashboard Actif</h3>
              <p className="text-gray-400 text-sm">
                L'armure est visible en overlay 3D. L'utilisateur peut switcher entre 
                mode Combat (protection max) et Repos (récupération). Les pierres portées 
                sont détectées et affichées.
              </p>
            </>
          )}
        </div>
      </div>

      {/* Tech Footer */}
      <div className="mt-8 text-center text-xs text-gray-600">
        <p>CHE·NU™ / Sphère AT·OM / Module ZAMA IGNITION v0.1</p>
        <p className="text-amber-700">GOUVERNANCE {'>'} EXÉCUTION</p>
      </div>
    </div>
  );
};

export default ZamaIgnitionStoryboard;
