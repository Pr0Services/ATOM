/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ████████╗ ██████╗ ██████╗ ██╗   ██╗███████╗    ██████╗  █████╗  ██████╗██╗  ██╗ ██████╗ ██████╗  ██████╗ 
 *      ╚══██╔══╝██╔═══██╗██╔══██╗██║   ██║██╔════╝    ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔══██╗██╔═══██╗
 *         ██║   ██║   ██║██████╔╝██║   ██║███████╗    ██████╔╝███████║██║     █████╔╝ ██║  ███╗██████╔╝██║   ██║
 *         ██║   ██║   ██║██╔══██╗██║   ██║╚════██║    ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔══██╗██║   ██║
 *         ██║   ╚██████╔╝██║  ██║╚██████╔╝███████║    ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║  ██║╚██████╔╝
 *         ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
 *                                                                                          
 *                                    🌀 FOND TOROÏDAL ANIMÉ 🌀
 *                                      L'ÉTHER EN MOUVEMENT
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *   Les particules sortent du centre et reviennent par les pôles
 *   suivant le ratio d'or φ ≈ 1.618
 * 
 *   Spirale Masculine (Or - ↻) : Émission
 *   Spirale Féminine (Argent - ↺) : Réception
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useRef, useEffect, useCallback, useMemo } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = 1.6180339887498949;
const PHI_INVERSE = 0.6180339887498949;

// Couleurs
const COLORS = {
  gold: { r: 212, g: 175, b: 55 },
  silver: { r: 192, g: 192, b: 192 },
  white: { r: 255, g: 255, b: 255 },
  emerald: { r: 80, g: 200, b: 120 },
  background: 'rgba(5, 5, 5, 0.03)'
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE PARTICULE
// ═══════════════════════════════════════════════════════════════════════════════

class Particle {
  constructor(canvas, index, totalParticles, isArchitectMode) {
    this.canvas = canvas;
    this.index = index;
    this.totalParticles = totalParticles;
    this.isArchitectMode = isArchitectMode;
    
    // Position initiale répartie sur le tore
    this.angle = (index / totalParticles) * Math.PI * 2;
    this.baseRadius = 50 + Math.random() * 150;
    this.radius = this.baseRadius;
    
    // Direction (alternance masculine/féminine)
    this.direction = index % 2 === 0 ? 1 : -1;
    this.isMasculine = this.direction > 0;
    
    // Position verticale
    this.y = Math.random() * canvas.height;
    
    // Vitesse basée sur φ
    this.speed = (Math.random() * 0.3 + 0.2) * this.direction;
    this.angularSpeed = (Math.random() * 0.02 + 0.01) * this.direction;
    
    // Taille
    this.size = Math.random() * 2 + 1;
    
    // Trail
    this.trail = [];
    this.maxTrailLength = 15;
  }

  update(speed = 1) {
    // Mise à jour de l'angle
    this.angle += this.angularSpeed * speed * (this.isArchitectMode ? PHI : 1);
    
    // Mouvement vertical
    this.y += this.direction * PHI * speed * 0.5;
    
    // Rebouclage toroïdal
    if (this.y > this.canvas.height) this.y = 0;
    if (this.y < 0) this.y = this.canvas.height;
    
    // Calcul du rayon toroïdal (forme de donut)
    const centerY = this.canvas.height / 2;
    const torusY = this.y - centerY;
    const normalizedY = torusY / (this.canvas.height / 2);
    
    // Le rayon varie selon la position Y pour créer l'effet toroïdal
    const torusRadius = Math.sqrt(Math.max(0, 1 - Math.pow(normalizedY, 2))) * this.baseRadius;
    this.radius = torusRadius;
    
    // Position X basée sur l'angle et le rayon
    const centerX = this.canvas.width / 2;
    this.x = centerX + Math.cos(this.angle) * this.radius;
    
    // Calcul de l'opacité (plus opaque au centre du tore)
    this.alpha = Math.max(0.1, 1 - Math.abs(normalizedY));
    
    // Mise à jour du trail
    this.trail.push({ x: this.x, y: this.y, alpha: this.alpha });
    if (this.trail.length > this.maxTrailLength) {
      this.trail.shift();
    }
  }

  draw(ctx) {
    // Dessiner le trail
    if (this.trail.length > 1) {
      ctx.beginPath();
      ctx.moveTo(this.trail[0].x, this.trail[0].y);
      
      for (let i = 1; i < this.trail.length; i++) {
        ctx.lineTo(this.trail[i].x, this.trail[i].y);
      }
      
      const color = this.isMasculine ? COLORS.gold : COLORS.silver;
      const trailAlpha = this.alpha * 0.3;
      ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${trailAlpha})`;
      ctx.lineWidth = this.size * 0.5;
      ctx.stroke();
    }
    
    // Dessiner la particule
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    
    // Couleur selon le mode et la direction
    let color;
    if (this.isArchitectMode) {
      color = COLORS.white;
    } else {
      color = this.isMasculine ? COLORS.gold : COLORS.silver;
    }
    
    ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${this.alpha})`;
    ctx.fill();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const TorusBackground = ({ 
  speed = 1, 
  isArchitectMode = false,
  particleCount = 60,
  showZeroPoint = true 
}) => {
  const canvasRef = useRef(null);
  const particlesRef = useRef([]);
  const animationRef = useRef(null);
  const lastTimeRef = useRef(0);

  // Initialisation des particules
  const initParticles = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    particlesRef.current = Array.from(
      { length: particleCount },
      (_, i) => new Particle(canvas, i, particleCount, isArchitectMode)
    );
  }, [particleCount, isArchitectMode]);

  // Dessiner le Point Zéro
  const drawZeroPoint = useCallback((ctx, centerX, centerY, time) => {
    const pulseSize = 10 + Math.sin(time * 0.003) * 3;
    
    // Halo externe
    const gradient = ctx.createRadialGradient(
      centerX, centerY, 0,
      centerX, centerY, pulseSize * 3
    );
    
    const color = isArchitectMode ? COLORS.white : COLORS.emerald;
    gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, 0.8)`);
    gradient.addColorStop(0.5, `rgba(${color.r}, ${color.g}, ${color.b}, 0.2)`);
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, pulseSize * 3, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Point central
    ctx.beginPath();
    ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 1)`;
    ctx.shadowColor = `rgb(${color.r}, ${color.g}, ${color.b})`;
    ctx.shadowBlur = 20;
    ctx.fill();
    ctx.shadowBlur = 0;
  }, [isArchitectMode]);

  // Dessiner les cercles concentriques (basés sur φ)
  const drawConcentricCircles = useCallback((ctx, centerX, centerY) => {
    const baseRadius = 30;
    const color = isArchitectMode ? COLORS.white : COLORS.gold;
    
    for (let i = 1; i <= 7; i++) {
      const radius = baseRadius * Math.pow(PHI, i - 1);
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${0.1 / i})`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }, [isArchitectMode]);

  // Dessiner les pôles
  const drawPoles = useCallback((ctx, centerX, height, time) => {
    const poleSize = 5 + Math.sin(time * 0.002) * 2;
    
    // Pôle Nord (999 Hz)
    ctx.beginPath();
    ctx.arc(centerX, 50, poleSize, 0, Math.PI * 2);
    ctx.fillStyle = isArchitectMode ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 253, 208, 0.6)';
    ctx.fill();
    
    ctx.font = '10px monospace';
    ctx.fillStyle = isArchitectMode ? 'rgba(255, 255, 255, 0.5)' : 'rgba(255, 253, 208, 0.5)';
    ctx.textAlign = 'center';
    ctx.fillText('999 Hz', centerX, 70);
    
    // Pôle Sud (111 Hz)
    ctx.beginPath();
    ctx.arc(centerX, height - 50, poleSize, 0, Math.PI * 2);
    ctx.fillStyle = isArchitectMode ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 0, 0, 0.4)';
    ctx.fill();
    
    ctx.fillStyle = isArchitectMode ? 'rgba(255, 255, 255, 0.5)' : 'rgba(255, 100, 100, 0.5)';
    ctx.fillText('111 Hz', centerX, height - 60);
  }, [isArchitectMode]);

  // Boucle d'animation
  const animate = useCallback((time) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Delta time pour animation fluide
    const deltaTime = time - lastTimeRef.current;
    lastTimeRef.current = time;
    
    // Effacer avec un léger fade (effet trail)
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, width, height);
    
    // Dessiner les cercles concentriques
    drawConcentricCircles(ctx, centerX, centerY);
    
    // Dessiner les pôles
    drawPoles(ctx, centerX, height, time);
    
    // Mettre à jour et dessiner les particules
    particlesRef.current.forEach(particle => {
      particle.isArchitectMode = isArchitectMode;
      particle.update(speed);
      particle.draw(ctx);
    });
    
    // Dessiner le Point Zéro
    if (showZeroPoint) {
      drawZeroPoint(ctx, centerX, centerY, time);
    }
    
    // Continuer l'animation
    animationRef.current = requestAnimationFrame(animate);
  }, [speed, isArchitectMode, showZeroPoint, drawZeroPoint, drawConcentricCircles, drawPoles]);

  // Gestion du redimensionnement
  const handleResize = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Réinitialiser les particules
    initParticles();
  }, [initParticles]);

  // Effet d'initialisation
  useEffect(() => {
    handleResize();
    window.addEventListener('resize', handleResize);
    
    // Démarrer l'animation
    animationRef.current = requestAnimationFrame(animate);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [handleResize, animate]);

  // Réinitialiser quand le mode change
  useEffect(() => {
    initParticles();
  }, [isArchitectMode, initParticles]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
      style={{
        background: isArchitectMode 
          ? 'radial-gradient(ellipse at center, rgba(50,50,50,1) 0%, rgba(0,0,0,1) 100%)'
          : 'radial-gradient(ellipse at center, rgba(10,10,10,1) 0%, rgba(0,0,0,1) 100%)'
      }}
    />
  );
};

export default TorusBackground;
