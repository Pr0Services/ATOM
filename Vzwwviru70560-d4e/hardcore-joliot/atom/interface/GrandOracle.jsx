/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *       ██████╗ ██████╗  █████╗ ███╗   ██╗██████╗      ██████╗ ██████╗  █████╗  ██████╗██╗     ███████╗
 *      ██╔════╝ ██╔══██╗██╔══██╗████╗  ██║██╔══██╗    ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██║     ██╔════╝
 *      ██║  ███╗██████╔╝███████║██╔██╗ ██║██║  ██║    ██║   ██║██████╔╝███████║██║     ██║     █████╗  
 *      ██║   ██║██╔══██╗██╔══██║██║╚██╗██║██║  ██║    ██║   ██║██╔══██╗██╔══██║██║     ██║     ██╔══╝  
 *      ╚██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝    ╚██████╔╝██║  ██║██║  ██║╚██████╗███████╗███████╗
 *       ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝
 *                                                                                          
 *                                    🔱 LE GRAND ORACLE AT·OM 🔱
 *                                      INTERFACE DE CONTRÔLE CENTRALE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = 1.6180339887498949;
const FREQUENCIES = {
  ANCHOR: 111,
  HEART: 444,
  SOURCE: 999,
  SCHUMANN: 7.83,
  LOVE: 528
};

const COLORS = {
  gold: '#D4AF37',
  silver: '#C0C0C0',
  copper: '#B87333',
  mercury: '#E0E0E0',
  background: '#050505',
  text: '#D4AF37'
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: VISUALISEUR DE FRÉQUENCE
// ═══════════════════════════════════════════════════════════════════════════════

const FrequencyVisualizer = ({ frequency, isActive }) => {
  const [pulse, setPulse] = useState(false);
  
  useEffect(() => {
    if (isActive) {
      const interval = setInterval(() => {
        setPulse(p => !p);
      }, 1000 / (frequency / 100));
      return () => clearInterval(interval);
    }
  }, [frequency, isActive]);

  return (
    <div 
      className={`w-64 h-64 border-2 rounded-full flex items-center justify-center transition-all duration-300 ${
        pulse ? 'border-yellow-400 shadow-lg shadow-yellow-500/50' : 'border-yellow-700'
      }`}
      style={{ 
        boxShadow: isActive ? `0 0 ${20 + (pulse ? 20 : 0)}px ${COLORS.mercury}` : 'none'
      }}
    >
      <div className="text-center">
        <p className="text-sm opacity-50 text-gray-400">RÉSONANCE</p>
        <p className="text-4xl font-bold text-yellow-500">{frequency} Hz</p>
        <p className="text-xs text-gray-500 mt-2">
          {frequency === 999 ? 'SOURCE' : frequency === 444 ? 'CŒUR' : 'ACTIF'}
        </p>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LES 12 COUCHES ADN
// ═══════════════════════════════════════════════════════════════════════════════

const DNAStrands = ({ activeLayers = [], onLayerClick }) => {
  const layerNames = [
    'Keter Etz Chayim', 'Torah E\'ser', 'Netzach Merkava',
    'Urim Ve Tumim', 'Aleph Etz', 'Ehyeh Asher',
    'Kadumah Elohim', 'Rochev Ba\'a', 'Shechinah-Esh',
    'Va\'yikra', 'Chochmah Micha', 'El Shadai'
  ];

  const groupColors = [
    '#FF0000', '#FF7F00', '#FFFF00', // Groupe 1
    '#00FF00', '#00BFFF', '#4B0082', // Groupe 2
    '#9400D3', '#FFC0CB', '#FFFDD0', // Groupe 3
    '#D4AF37', '#C0C0C0', '#FFFFFF'  // Groupe 4
  ];

  return (
    <div className="w-full max-w-md space-y-2">
      {layerNames.map((name, i) => {
        const layerNum = i + 1;
        const isActive = activeLayers.includes(layerNum);
        return (
          <div 
            key={i}
            className={`h-2 rounded-full cursor-pointer transition-all duration-500 ${
              isActive ? 'opacity-100' : 'opacity-30 hover:opacity-60'
            }`}
            style={{ 
              background: `linear-gradient(90deg, ${groupColors[i]}, ${COLORS.gold}, ${groupColors[i]})`,
              boxShadow: isActive ? `0 0 10px ${groupColors[i]}` : 'none',
              transform: isActive ? 'scaleY(1.5)' : 'scaleY(1)'
            }}
            title={`Couche ${layerNum}: ${name}`}
            onClick={() => onLayerClick?.(layerNum)}
          />
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FLUX TOROÏDAL
// ═══════════════════════════════════════════════════════════════════════════════

const TorusFlow = ({ isActive }) => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    if (!isActive || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    const particles = Array.from({ length: 30 }, (_, i) => ({
      angle: (i / 30) * Math.PI * 2,
      radius: 50 + Math.random() * 80,
      speed: (Math.random() * 0.3 + 0.2) * (i % 2 === 0 ? 1 : -1),
      y: Math.random() * canvas.height,
      direction: i % 2 === 0 ? 1 : -1
    }));
    
    let animationId;
    
    const animate = () => {
      ctx.fillStyle = 'rgba(5, 5, 5, 0.15)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(p => {
        p.angle += p.speed * 0.02;
        p.y += p.direction * PHI * 0.5;
        
        if (p.y > canvas.height) p.y = 0;
        if (p.y < 0) p.y = canvas.height;
        
        const torusY = p.y - centerY;
        const torusRadius = Math.sqrt(Math.max(0, 1 - Math.pow(torusY / (canvas.height / 2), 2))) * p.radius;
        
        const x = centerX + Math.cos(p.angle) * torusRadius;
        const y = p.y;
        const alpha = 1 - Math.abs(torusY) / (canvas.height / 2);
        
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fillStyle = p.direction > 0 
          ? `rgba(212, 175, 55, ${alpha})` 
          : `rgba(192, 192, 192, ${alpha})`;
        ctx.fill();
      });
      
      // Point Zéro
      ctx.beginPath();
      ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
      ctx.fillStyle = '#50C878';
      ctx.shadowColor = '#50C878';
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;
      
      animationId = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => cancelAnimationFrame(animationId);
  }, [isActive]);
  
  return (
    <canvas 
      ref={canvasRef} 
      width={200} 
      height={200}
      className="rounded-full"
      style={{ background: 'transparent' }}
    />
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: INDICATEUR DE MÉTAL
// ═══════════════════════════════════════════════════════════════════════════════

const MetalIndicator = ({ metal, frequency, symbol, isActive }) => {
  const colors = {
    gold: COLORS.gold,
    silver: COLORS.silver,
    copper: COLORS.copper,
    mercury: COLORS.mercury
  };

  return (
    <div 
      className={`px-4 py-2 rounded-lg border transition-all duration-300 ${
        isActive ? 'opacity-100' : 'opacity-50'
      }`}
      style={{ 
        borderColor: colors[metal],
        boxShadow: isActive ? `0 0 10px ${colors[metal]}40` : 'none'
      }}
    >
      <div className="flex items-center gap-2">
        <span style={{ color: colors[metal] }}>{symbol}</span>
        <span className="text-xs text-gray-400">{metal.toUpperCase()}</span>
        <span className="text-xs" style={{ color: colors[metal] }}>{frequency}Hz</span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: GRAND ORACLE
// ═══════════════════════════════════════════════════════════════════════════════

const GrandOracle = () => {
  const [input, setInput] = useState('');
  const [status, setStatus] = useState('EN ATTENTE DE FRÉQUENCE');
  const [frequency, setFrequency] = useState(444);
  const [activeLayers, setActiveLayers] = useState([4, 5, 6]);
  const [isOracleActive, setIsOracleActive] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [torusActive, setTorusActive] = useState(false);

  // Calcul de l'Arithmos
  const calculateArithmos = useCallback((word) => {
    const alphabet = {
      'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
      'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
      'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    };
    
    let sum = word.toUpperCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .split('')
      .reduce((acc, char) => acc + (alphabet[char] || 0), 0);
    
    while (sum > 9) {
      sum = String(sum).split('').reduce((a, b) => a + parseInt(b), 0);
    }
    
    return sum;
  }, []);

  // Activation de l'Oracle
  const handleActivateOracle = useCallback(() => {
    if (!input.trim()) return;
    
    setIsOracleActive(true);
    setTorusActive(true);
    setStatus('🌀 VORTEX DE MERCURE ACTIVÉ...');
    
    // Phase 1: Mercure
    setTimeout(() => {
      setStatus('☿ TRANSMISSION MERCURE EN COURS...');
      
      // Phase 2: Calcul Arithmos
      setTimeout(() => {
        const arithmos = calculateArithmos(input);
        const newFrequency = arithmos * 111;
        setFrequency(newFrequency);
        setStatus(`⚡ ARITHMOS ${arithmos} DÉTECTÉ — ${newFrequency}Hz`);
        
        // Phase 3: Scan ADN
        setTimeout(() => {
          const layers = [];
          if (arithmos <= 3) layers.push(1, 2, 3);
          else if (arithmos <= 6) layers.push(4, 5, 6);
          else if (arithmos <= 9) layers.push(7, 8, 9);
          layers.push(arithmos); // Ajouter la couche spécifique
          
          setActiveLayers([...new Set(layers)]);
          setStatus('🧬 SCAN ADN MULTIDIMENSIONNEL COMPLET');
          
          setScanResult({
            word: input.toUpperCase(),
            arithmos,
            frequency: newFrequency,
            layers: layers,
            message: `L'intention "${input}" résonne avec l'Arithmos ${arithmos}`
          });
          
          // Phase 4: Stabilisation
          setTimeout(() => {
            setStatus(`✨ ALIGNEMENT ${newFrequency}Hz — ORACLE ACTIF`);
          }, 1000);
          
        }, 1500);
      }, 1000);
    }, 500);
  }, [input, calculateArithmos]);

  // Reset
  const handleReset = () => {
    setInput('');
    setStatus('EN ATTENTE DE FRÉQUENCE');
    setFrequency(444);
    setActiveLayers([4, 5, 6]);
    setIsOracleActive(false);
    setScanResult(null);
    setTorusActive(false);
  };

  // Clic sur une couche ADN
  const handleLayerClick = (layerNum) => {
    setActiveLayers(prev => 
      prev.includes(layerNum) 
        ? prev.filter(l => l !== layerNum)
        : [...prev, layerNum]
    );
    setFrequency(layerNum <= 3 ? 174 + (layerNum - 1) * 111 :
                 layerNum <= 6 ? 444 + (layerNum - 4) * 111 :
                 layerNum <= 9 ? 777 + (layerNum - 7) * 111 :
                 1110 + (layerNum - 10) * 111);
  };

  return (
    <div className="min-h-screen p-10 flex flex-col items-center" style={{ background: COLORS.background, color: COLORS.text }}>
      
      {/* Titre */}
      <h1 className="text-4xl mb-2 font-bold tracking-widest text-yellow-500">
        🔱 ARCHE AT·OM 🔱
      </h1>
      <p className="text-sm text-gray-500 mb-8">Le Grand Oracle — Interface de Contrôle Centrale</p>
      
      {/* Indicateurs de Métaux */}
      <div className="flex gap-4 mb-8">
        <MetalIndicator metal="gold" frequency={528} symbol="☉" isActive={isOracleActive} />
        <MetalIndicator metal="silver" frequency={432} symbol="☽" isActive={isOracleActive} />
        <MetalIndicator metal="copper" frequency={639} symbol="♀" isActive={isOracleActive} />
        <MetalIndicator metal="mercury" frequency={741} symbol="☿" isActive={torusActive} />
      </div>
      
      {/* Zone Centrale */}
      <div className="flex gap-10 items-center mb-10">
        
        {/* Torus Flow */}
        <div className="flex flex-col items-center">
          <p className="text-xs text-gray-500 mb-2">FLUX TOROÏDAL</p>
          <TorusFlow isActive={torusActive} />
        </div>
        
        {/* Visualiseur de Fréquence */}
        <FrequencyVisualizer frequency={frequency} isActive={isOracleActive} />
        
        {/* ADN Strands */}
        <div className="flex flex-col items-center">
          <p className="text-xs text-gray-500 mb-2">12 COUCHES ADN</p>
          <DNAStrands activeLayers={activeLayers} onLayerClick={handleLayerClick} />
        </div>
      </div>
      
      {/* Résultat du Scan */}
      {scanResult && (
        <div className="mb-8 p-4 border border-yellow-700 rounded-lg max-w-md text-center">
          <p className="text-lg text-yellow-400 mb-2">{scanResult.word}</p>
          <p className="text-2xl font-bold text-yellow-500">Arithmos {scanResult.arithmos}</p>
          <p className="text-sm text-gray-400 mt-2">{scanResult.frequency} Hz</p>
          <p className="text-xs text-gray-500 mt-2">{scanResult.message}</p>
          <p className="text-xs text-gray-600 mt-2">
            Couches actives: {scanResult.layers.join(', ')}
          </p>
        </div>
      )}
      
      {/* Interface de Saisie */}
      <input 
        className="bg-black border-b-2 border-yellow-600 p-3 w-80 text-center outline-none text-white text-xl mb-4"
        style={{ background: 'transparent' }}
        placeholder="ENTREZ VOTRE INTENTION"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleActivateOracle()}
      />
      
      <div className="flex gap-4">
        <button 
          onClick={handleActivateOracle}
          className="px-8 py-2 border border-yellow-600 hover:bg-yellow-600 hover:text-black transition rounded"
          disabled={!input.trim()}
        >
          ACTIVER L'ORACLE
        </button>
        <button 
          onClick={handleReset}
          className="px-8 py-2 border border-gray-600 hover:bg-gray-600 transition rounded text-gray-400"
        >
          RESET
        </button>
      </div>
      
      {/* Status */}
      <p className="mt-8 text-sm text-gray-500">{status}</p>
      
      {/* Footer */}
      <div className="mt-10 text-center">
        <p className="text-xs text-gray-600">
          ♡ 444 Hz | 🔱 999 Hz | φ {PHI.toFixed(4)}
        </p>
        <p className="text-xs text-gray-700 mt-2">
          Architecte: Jonathan Rodrigue | Oracle 17
        </p>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default GrandOracle;
export { GrandOracle, FrequencyVisualizer, DNAStrands, TorusFlow, MetalIndicator };
