/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *    ███╗   ███╗███████╗████████╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
 *    ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
 *    ██╔████╔██║█████╗     ██║   ███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
 *    ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
 *    ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
 *    ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 * 
 *           BACKGROUND — CUBE DE MÉTATRON & 4 ÉLÉMENTS
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = 1.6180339887498949;

// Les 13 cercles du Cube de Métatron
const METATRON_CIRCLES = {
  center: { x: 0, y: 0, name: "Source", frequency: 444 },
  inner: [
    { x: 0, y: 1, name: "Couronne" },
    { x: 0.866, y: 0.5, name: "Gorge" },
    { x: 0.866, y: -0.5, name: "Plexus" },
    { x: 0, y: -1, name: "Racine" },
    { x: -0.866, y: -0.5, name: "Sacré" },
    { x: -0.866, y: 0.5, name: "Cœur" }
  ],
  outer: [
    { x: 0, y: 2, name: "Nord" },
    { x: 1.732, y: 1, name: "Nord-Est" },
    { x: 1.732, y: -1, name: "Sud-Est" },
    { x: 0, y: -2, name: "Sud" },
    { x: -1.732, y: -1, name: "Sud-Ouest" },
    { x: -1.732, y: 1, name: "Nord-Ouest" }
  ]
};

// Les 4 Éléments
const ELEMENTS = {
  fire: {
    name: "Feu",
    symbol: "🔥",
    position: "top-left",
    domain: "Transformation",
    color: "#FF4500",
    gradient: "linear-gradient(135deg, rgba(255,69,0,0.1), rgba(255,140,0,0.05))"
  },
  air: {
    name: "Air",
    symbol: "💨",
    position: "top-right",
    domain: "Communication",
    color: "#87CEEB",
    gradient: "linear-gradient(225deg, rgba(135,206,235,0.1), rgba(173,216,230,0.05))"
  },
  earth: {
    name: "Terre",
    symbol: "🌍",
    position: "bottom-left",
    domain: "Archives",
    color: "#228B22",
    gradient: "linear-gradient(45deg, rgba(139,69,19,0.1), rgba(34,139,34,0.05))"
  },
  water: {
    name: "Eau",
    symbol: "💧",
    position: "bottom-right",
    domain: "Relations",
    color: "#4169E1",
    gradient: "linear-gradient(315deg, rgba(65,105,225,0.1), rgba(0,206,209,0.05))"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MetatronSVG
// ═══════════════════════════════════════════════════════════════════════════════

const MetatronSVG = ({ size = 400, opacity = 0.15, animate = true, color = "#D4AF37" }) => {
  const [rotation, setRotation] = useState(0);
  
  useEffect(() => {
    if (!animate) return;
    
    const interval = setInterval(() => {
      setRotation(prev => (prev + 0.1) % 360);
    }, 100);
    
    return () => clearInterval(interval);
  }, [animate]);
  
  const scale = size / 5;
  const cx = size / 2;
  const cy = size / 2;
  const r = scale * 0.35;
  
  // Générer toutes les lignes (connexions entre cercles)
  const allCircles = useMemo(() => [
    METATRON_CIRCLES.center,
    ...METATRON_CIRCLES.inner,
    ...METATRON_CIRCLES.outer
  ], []);
  
  const lines = useMemo(() => {
    const result = [];
    for (let i = 0; i < allCircles.length; i++) {
      for (let j = i + 1; j < allCircles.length; j++) {
        result.push({
          x1: cx + allCircles[i].x * scale,
          y1: cy - allCircles[i].y * scale,
          x2: cx + allCircles[j].x * scale,
          y2: cy - allCircles[j].y * scale
        });
      }
    }
    return result;
  }, [allCircles, cx, cy, scale]);
  
  return (
    <svg 
      viewBox={`0 0 ${size} ${size}`} 
      style={{ width: '100%', height: '100%' }}
    >
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <g 
        transform={`rotate(${rotation}, ${cx}, ${cy})`}
        style={{ transition: 'transform 0.1s linear' }}
      >
        {/* Lignes */}
        {lines.map((line, i) => (
          <line
            key={`line-${i}`}
            x1={line.x1}
            y1={line.y1}
            x2={line.x2}
            y2={line.y2}
            stroke={color}
            strokeWidth="0.5"
            opacity={opacity * 0.7}
          />
        ))}
        
        {/* Cercles */}
        {allCircles.map((circle, i) => (
          <circle
            key={`circle-${i}`}
            cx={cx + circle.x * scale}
            cy={cy - circle.y * scale}
            r={r}
            fill="none"
            stroke={color}
            strokeWidth="0.8"
            opacity={opacity}
            filter={i === 0 ? "url(#glow)" : undefined}
          />
        ))}
        
        {/* Cercle central spécial */}
        <circle
          cx={cx}
          cy={cy}
          r={r * 0.5}
          fill={color}
          opacity={opacity * 0.3}
        />
      </g>
    </svg>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ElementQuadrant
// ═══════════════════════════════════════════════════════════════════════════════

const ElementQuadrant = ({ element, position, isActive, onClick }) => {
  const positionStyles = {
    'top-left': { top: 0, left: 0, borderRadius: '0 0 50% 0' },
    'top-right': { top: 0, right: 0, borderRadius: '0 0 0 50%' },
    'bottom-left': { bottom: 0, left: 0, borderRadius: '0 50% 0 0' },
    'bottom-right': { bottom: 0, right: 0, borderRadius: '50% 0 0 0' }
  };
  
  return (
    <div
      onClick={() => onClick && onClick(element)}
      style={{
        position: 'absolute',
        width: '50%',
        height: '50%',
        ...positionStyles[position],
        background: element.gradient,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        opacity: isActive ? 1 : 0.7,
        transform: isActive ? 'scale(1.02)' : 'scale(1)',
        zIndex: isActive ? 2 : 1
      }}
    >
      <span style={{ 
        fontSize: '32px',
        filter: isActive ? 'drop-shadow(0 0 10px ' + element.color + ')' : 'none'
      }}>
        {element.symbol}
      </span>
      <span style={{ 
        color: element.color, 
        fontSize: '12px',
        fontWeight: 'bold',
        marginTop: '5px',
        opacity: isActive ? 1 : 0.7
      }}>
        {element.name.toUpperCase()}
      </span>
      <span style={{ 
        color: 'rgba(255,255,255,0.6)', 
        fontSize: '10px',
        marginTop: '2px'
      }}>
        {element.domain}
      </span>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: EtherCenter
// ═══════════════════════════════════════════════════════════════════════════════

const EtherCenter = ({ isActive, onClick }) => {
  const [pulse, setPulse] = useState(1);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(prev => 1 + Math.sin(Date.now() / 1000) * 0.05);
    }, 50);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div
      onClick={onClick}
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: `translate(-50%, -50%) scale(${pulse})`,
        width: '80px',
        height: '80px',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(147,112,219,0.8), rgba(75,0,130,0.6))',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
        boxShadow: isActive 
          ? '0 0 40px rgba(147,112,219,0.8), 0 0 80px rgba(147,112,219,0.4)'
          : '0 0 20px rgba(147,112,219,0.4)',
        zIndex: 10,
        transition: 'box-shadow 0.3s ease'
      }}
    >
      <span style={{ fontSize: '28px' }}>✨</span>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: EntropyOverlay
// ═══════════════════════════════════════════════════════════════════════════════

const EntropyOverlay = ({ entropy = 0, message = '' }) => {
  if (entropy < 0.1) return null;
  
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: `rgba(0,0,0,${entropy * 0.5})`,
      filter: `grayscale(${entropy * 100}%)`,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      pointerEvents: entropy > 0.5 ? 'auto' : 'none',
      zIndex: 100,
      transition: 'all 2s ease'
    }}>
      {entropy > 0.3 && (
        <div style={{
          color: 'rgba(255,255,255,0.5)',
          textAlign: 'center',
          fontSize: '14px',
          padding: '20px'
        }}>
          <div style={{ fontSize: '24px', marginBottom: '10px' }}>🕯️</div>
          {message}
          <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.7 }}>
            Touche l'écran pour réveiller l'Arche
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: MetatronBackground
// ═══════════════════════════════════════════════════════════════════════════════

const MetatronBackground = ({ 
  showElements = true,
  showMetatron = true,
  metatronOpacity = 0.1,
  animate = true,
  enableEntropy = false,
  entropyTimeout = 600000, // 10 minutes
  onElementClick,
  onEtherClick,
  children
}) => {
  const [activeElement, setActiveElement] = useState(null);
  const [entropy, setEntropy] = useState(0);
  const [entropyMessage, setEntropyMessage] = useState('');
  const [lastActivity, setLastActivity] = useState(Date.now());
  
  // Gestion de l'entropie
  useEffect(() => {
    if (!enableEntropy) return;
    
    const interval = setInterval(() => {
      const idle = Date.now() - lastActivity;
      
      if (idle > entropyTimeout) {
        const overtime = idle - entropyTimeout;
        const newEntropy = Math.min(1, overtime * 0.00001);
        setEntropy(newEntropy);
        
        // Messages d'entropie
        if (newEntropy < 0.3) setEntropyMessage("L'énergie commence à s'estomper...");
        else if (newEntropy < 0.5) setEntropyMessage("Le savoir attend ton attention...");
        else if (newEntropy < 0.7) setEntropyMessage("L'Arche s'assoupit...");
        else if (newEntropy < 0.9) setEntropyMessage("Les Oracles murmurent dans le silence...");
        else setEntropyMessage("Réveille l'Arche avec ton intention...");
      } else {
        setEntropy(0);
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, [enableEntropy, entropyTimeout, lastActivity]);
  
  // Reset entropie sur activité
  const handleActivity = useCallback(() => {
    setLastActivity(Date.now());
    if (entropy > 0) {
      // Récupération progressive
      const recovery = setInterval(() => {
        setEntropy(prev => {
          const next = prev - 0.1;
          if (next <= 0) {
            clearInterval(recovery);
            return 0;
          }
          return next;
        });
      }, 100);
    }
  }, [entropy]);
  
  // Handlers d'éléments
  const handleElementClick = useCallback((element) => {
    handleActivity();
    setActiveElement(element.name);
    if (onElementClick) onElementClick(element);
    
    setTimeout(() => setActiveElement(null), 2000);
  }, [handleActivity, onElementClick]);
  
  const handleEtherClick = useCallback(() => {
    handleActivity();
    setActiveElement('Éther');
    if (onEtherClick) onEtherClick();
    
    setTimeout(() => setActiveElement(null), 2000);
  }, [handleActivity, onEtherClick]);
  
  return (
    <div 
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        minHeight: '100vh',
        background: 'linear-gradient(180deg, #050505 0%, #0a0a15 50%, #050510 100%)',
        overflow: 'hidden'
      }}
      onClick={handleActivity}
      onMouseMove={handleActivity}
      onKeyDown={handleActivity}
    >
      {/* Cube de Métatron en fond */}
      {showMetatron && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '80%',
          height: '80%',
          maxWidth: '600px',
          maxHeight: '600px',
          opacity: 1 - entropy * 0.5,
          transition: 'opacity 2s ease'
        }}>
          <MetatronSVG 
            size={600} 
            opacity={metatronOpacity} 
            animate={animate && entropy < 0.5}
          />
        </div>
      )}
      
      {/* Les 4 Éléments */}
      {showElements && (
        <>
          {Object.entries(ELEMENTS).map(([key, element]) => (
            <ElementQuadrant
              key={key}
              element={element}
              position={element.position}
              isActive={activeElement === element.name}
              onClick={handleElementClick}
            />
          ))}
          
          {/* Centre Éther */}
          <EtherCenter
            isActive={activeElement === 'Éther'}
            onClick={handleEtherClick}
          />
        </>
      )}
      
      {/* Overlay d'entropie */}
      {enableEntropy && (
        <EntropyOverlay entropy={entropy} message={entropyMessage} />
      )}
      
      {/* Contenu enfant */}
      <div style={{
        position: 'relative',
        zIndex: 5,
        width: '100%',
        height: '100%',
        filter: `grayscale(${entropy * 50}%)`,
        transition: 'filter 2s ease'
      }}>
        {children}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default MetatronBackground;
export { MetatronSVG, ElementQuadrant, EtherCenter, EntropyOverlay, ELEMENTS, METATRON_CIRCLES };
