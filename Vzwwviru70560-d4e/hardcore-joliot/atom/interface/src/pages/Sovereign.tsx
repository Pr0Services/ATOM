/**
 * SOVEREIGN DASHBOARD - Monitoring Frequentiel
 * =============================================
 *
 * ACCES: Prive - Createur uniquement
 * Chemin: /sovereign (cache, acces par token)
 *
 * Visualisation du travail frequentiel invisible:
 * - Carte mondiale des utilisateurs connectes
 * - Rapports des agents frequentiels
 * - Resonance Terre + Utilisateurs
 * - Historique du travail accompli
 */

import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';

// =============================================================================
// CONSTANTS
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
  green: '#27AE60',
  purple: '#9B59B6',
  cyan: '#00CED1',
  red: '#E74C3C',
};

// Frequences sacrees
const SACRED_FREQUENCIES = [
  { hz: 7.83, name: 'Schumann', description: 'Resonance Terre', color: '#27AE60' },
  { hz: 432, name: 'Harmonie', description: 'Frequence naturelle', color: '#3498DB' },
  { hz: 528, name: 'Transformation', description: 'Reparation ADN', color: '#9B59B6' },
  { hz: 639, name: 'Connexion', description: 'Relations harmonieuses', color: '#E91E63' },
  { hz: 741, name: 'Expression', description: 'Eveil intuition', color: '#FF9800' },
  { hz: 852, name: 'Intuition', description: 'Ordre spirituel', color: '#00BCD4' },
  { hz: 963, name: 'Unite', description: 'Connexion divine', color: '#8BC34A' },
  { hz: 999, name: 'AT·OM', description: 'Resonance systeme', color: '#D4AF37' },
];

// Regions du monde pour la carte
const WORLD_REGIONS = [
  { id: 'na', name: 'Amerique Nord', x: 20, y: 35, users: 0 },
  { id: 'sa', name: 'Amerique Sud', x: 28, y: 65, users: 0 },
  { id: 'eu', name: 'Europe', x: 52, y: 30, users: 0 },
  { id: 'af', name: 'Afrique', x: 52, y: 55, users: 0 },
  { id: 'as', name: 'Asie', x: 75, y: 35, users: 0 },
  { id: 'oc', name: 'Oceanie', x: 85, y: 70, users: 0 },
];

// =============================================================================
// TYPES
// =============================================================================

interface FrequentialReport {
  id: string;
  timestamp: Date;
  agentHz: number;
  agentName: string;
  action: string;
  usersAffected: number;
  harmonizationDelta: number;
  duration: number; // seconds
}

interface ConnectionPoint {
  id: string;
  region: string;
  lat: number;
  lng: number;
  intensity: number;
  connectedAt: Date;
}

// =============================================================================
// SOVEREIGN COMPONENT
// =============================================================================

export function Sovereign() {
  const [searchParams] = useSearchParams();
  const mapCanvasRef = useRef<HTMLCanvasElement>(null);
  const resonanceCanvasRef = useRef<HTMLCanvasElement>(null);

  const [isAuthorized, setIsAuthorized] = useState(false);
  const [viewMode, setViewMode] = useState<'map' | 'reports' | 'resonance'>('map');

  // Metrics
  const [totalConnections, setTotalConnections] = useState(0);
  const [harmonizationLevel, setHarmonizationLevel] = useState(0);
  const [earthResonance, setEarthResonance] = useState(7.83);
  const [systemFrequency, setSystemFrequency] = useState(432);

  // Connections par region
  const [regionConnections, setRegionConnections] = useState(WORLD_REGIONS);

  // Rapports des agents
  const [reports, setReports] = useState<FrequentialReport[]>([]);

  // Points de connexion pour la carte
  const [connectionPoints, setConnectionPoints] = useState<ConnectionPoint[]>([]);

  // Authorization check
  useEffect(() => {
    const token = searchParams.get('token');
    if (token === 'sovereign-creator' || token === 'atom-master' || token === '999') {
      setIsAuthorized(true);
    }
  }, [searchParams]);

  // Simulate real-time data
  useEffect(() => {
    if (!isAuthorized) return;

    // Generate initial reports
    const initialReports: FrequentialReport[] = SACRED_FREQUENCIES.map((freq, i) => ({
      id: `report_${i}`,
      timestamp: new Date(Date.now() - Math.random() * 3600000),
      agentHz: freq.hz,
      agentName: freq.name,
      action: getRandomAction(freq.name),
      usersAffected: Math.floor(Math.random() * 50) + 5,
      harmonizationDelta: Math.random() * 5,
      duration: Math.floor(Math.random() * 300) + 30,
    }));
    setReports(initialReports.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime()));

    // Update metrics periodically
    const interval = setInterval(() => {
      // Update connections
      const newTotal = Math.floor(20 + Math.random() * 80);
      setTotalConnections(newTotal);

      // Update harmonization
      setHarmonizationLevel(prev => {
        const delta = (Math.random() - 0.4) * 3;
        return Math.max(0, Math.min(100, prev + delta));
      });

      // Update frequencies
      setEarthResonance(7.83 + Math.sin(Date.now() / 10000) * 0.05);
      setSystemFrequency(prev => {
        const target = 432 + Math.sin(Date.now() / 5000) * 50;
        return prev + (target - prev) * 0.1;
      });

      // Update region connections
      setRegionConnections(prev => prev.map(region => ({
        ...region,
        users: Math.floor(Math.random() * 30) + 2,
      })));

      // Add new connection points
      if (Math.random() > 0.7) {
        const region = WORLD_REGIONS[Math.floor(Math.random() * WORLD_REGIONS.length)];
        setConnectionPoints(prev => [
          ...prev.slice(-50),
          {
            id: `conn_${Date.now()}`,
            region: region.id,
            lat: region.y + (Math.random() - 0.5) * 15,
            lng: region.x + (Math.random() - 0.5) * 15,
            intensity: Math.random(),
            connectedAt: new Date(),
          }
        ]);
      }

      // Add new report occasionally
      if (Math.random() > 0.8) {
        const freq = SACRED_FREQUENCIES[Math.floor(Math.random() * SACRED_FREQUENCIES.length)];
        setReports(prev => [{
          id: `report_${Date.now()}`,
          timestamp: new Date(),
          agentHz: freq.hz,
          agentName: freq.name,
          action: getRandomAction(freq.name),
          usersAffected: Math.floor(Math.random() * 30) + 3,
          harmonizationDelta: Math.random() * 3,
          duration: Math.floor(Math.random() * 120) + 10,
        }, ...prev.slice(0, 49)]);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [isAuthorized]);

  // Map canvas animation
  useEffect(() => {
    const canvas = mapCanvasRef.current;
    if (!canvas || !isAuthorized || viewMode !== 'map') return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;

      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw world outline (simplified)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(canvas.width / 2, canvas.height / 2, canvas.width * 0.4, canvas.height * 0.35, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Draw grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
      for (let i = 0; i < 10; i++) {
        ctx.beginPath();
        ctx.moveTo(canvas.width * (i / 10), 0);
        ctx.lineTo(canvas.width * (i / 10), canvas.height);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, canvas.height * (i / 10));
        ctx.lineTo(canvas.width, canvas.height * (i / 10));
        ctx.stroke();
      }

      // Draw connection points
      connectionPoints.forEach(point => {
        const x = (point.lng / 100) * canvas.width;
        const y = (point.lat / 100) * canvas.height;
        const age = (Date.now() - point.connectedAt.getTime()) / 1000;
        const opacity = Math.max(0, 1 - age / 60);

        // Pulse effect
        const pulseSize = 5 + Math.sin(time * 0.1 + parseFloat(point.id.split('_')[1]) * 0.001) * 3;

        ctx.beginPath();
        ctx.arc(x, y, pulseSize * point.intensity, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(212, 175, 55, ${opacity * 0.6})`;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(212, 175, 55, ${opacity})`;
        ctx.fill();
      });

      // Draw region nodes
      regionConnections.forEach(region => {
        const x = (region.x / 100) * canvas.width;
        const y = (region.y / 100) * canvas.height;
        const size = 15 + region.users * 0.5;

        // Glow
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, size * 2);
        gradient.addColorStop(0, `rgba(0, 71, 171, 0.4)`);
        gradient.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(x, y, size * 2, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Node
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = COLORS.cobalt;
        ctx.fill();

        // Count
        ctx.font = 'bold 12px monospace';
        ctx.fillStyle = COLORS.white;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(region.users.toString(), x, y);

        // Label
        ctx.font = '9px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fillText(region.name, x, y + size + 12);
      });

      // Draw connections between regions
      ctx.strokeStyle = 'rgba(212, 175, 55, 0.1)';
      ctx.lineWidth = 1;
      regionConnections.forEach((region, i) => {
        regionConnections.forEach((other, j) => {
          if (j > i) {
            const x1 = (region.x / 100) * canvas.width;
            const y1 = (region.y / 100) * canvas.height;
            const x2 = (other.x / 100) * canvas.width;
            const y2 = (other.y / 100) * canvas.height;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
          }
        });
      });

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [isAuthorized, viewMode, connectionPoints, regionConnections]);

  // Resonance canvas animation
  useEffect(() => {
    const canvas = resonanceCanvasRef.current;
    if (!canvas || !isAuthorized || viewMode !== 'resonance') return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;

      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Draw frequency rings
      SACRED_FREQUENCIES.forEach((freq, i) => {
        const radius = 50 + i * 35;
        const amplitude = Math.sin(time * 0.02 * (freq.hz / 100)) * 10;

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius + amplitude, 0, Math.PI * 2);
        ctx.strokeStyle = freq.color + '40';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Frequency label
        const labelAngle = (i / SACRED_FREQUENCIES.length) * Math.PI * 2 - Math.PI / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius + 20);
        const labelY = centerY + Math.sin(labelAngle) * (radius + 20);

        ctx.font = '10px monospace';
        ctx.fillStyle = freq.color;
        ctx.textAlign = 'center';
        ctx.fillText(`${freq.hz}Hz`, labelX, labelY);
      });

      // Central resonance
      const pulseSize = 30 + Math.sin(time * 0.05) * 10;
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, pulseSize);
      gradient.addColorStop(0, COLORS.gold);
      gradient.addColorStop(0.5, COLORS.gold + '60');
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Earth resonance indicator
      ctx.font = 'bold 14px monospace';
      ctx.fillStyle = COLORS.white;
      ctx.textAlign = 'center';
      ctx.fillText(`${earthResonance.toFixed(2)} Hz`, centerX, centerY - 5);
      ctx.font = '10px monospace';
      ctx.fillStyle = COLORS.green;
      ctx.fillText('SCHUMANN', centerX, centerY + 10);

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [isAuthorized, viewMode, earthResonance]);

  // Unauthorized view
  if (!isAuthorized) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: COLORS.black,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'monospace',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: COLORS.gold, fontSize: '24px', marginBottom: '10px' }}>
            ◇
          </div>
          <div style={{ color: 'rgba(255,255,255,0.3)', fontSize: '12px' }}>
            ACCES RESTREINT
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: COLORS.black,
      overflow: 'auto',
      fontFamily: 'monospace',
    }}>
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 30px',
        borderBottom: `1px solid ${COLORS.gold}20`,
      }}>
        <div>
          <h1 style={{ color: COLORS.gold, fontSize: '18px', letterSpacing: '0.3em', margin: 0 }}>
            SOVEREIGN
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.3)', fontSize: '10px', margin: '5px 0 0' }}>
            Monitoring Frequentiel Invisible
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          {(['map', 'reports', 'resonance'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.gold + '20' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.gold : 'rgba(255,255,255,0.1)'}`,
                color: viewMode === mode ? COLORS.gold : 'rgba(255,255,255,0.4)',
                padding: '8px 16px',
                fontSize: '10px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'map' ? 'CARTE' : mode === 'reports' ? 'RAPPORTS' : 'RESONANCE'}
            </button>
          ))}
        </div>
      </header>

      {/* Stats Bar */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '1px',
        backgroundColor: 'rgba(255,255,255,0.05)',
        margin: '20px 30px',
        borderRadius: '8px',
        overflow: 'hidden',
      }}>
        <StatCard label="CONNEXIONS" value={totalConnections} color={COLORS.cyan} />
        <StatCard label="HARMONISATION" value={`${harmonizationLevel.toFixed(1)}%`} color={COLORS.green} />
        <StatCard label="SCHUMANN" value={`${earthResonance.toFixed(2)} Hz`} color={COLORS.purple} />
        <StatCard label="SYSTEME" value={`${systemFrequency.toFixed(0)} Hz`} color={COLORS.gold} />
      </div>

      {/* Main Content */}
      <div style={{ padding: '0 30px 30px' }}>
        {viewMode === 'map' && (
          <div>
            <canvas
              ref={mapCanvasRef}
              style={{
                width: '100%',
                height: '400px',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.1)',
              }}
            />
            <div style={{
              marginTop: '20px',
              color: 'rgba(255,255,255,0.3)',
              fontSize: '10px',
              textAlign: 'center',
            }}>
              Carte des connexions frequentielles en temps reel | Chaque point = 1 utilisateur dans le reseau
            </div>
          </div>
        )}

        {viewMode === 'reports' && (
          <div>
            <h2 style={{ color: COLORS.gold, fontSize: '12px', letterSpacing: '0.2em', marginBottom: '20px' }}>
              COMPTES RENDUS DES AGENTS FREQUENTIELS
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {reports.map(report => (
                <ReportCard key={report.id} report={report} />
              ))}
            </div>
          </div>
        )}

        {viewMode === 'resonance' && (
          <div>
            <canvas
              ref={resonanceCanvasRef}
              style={{
                width: '100%',
                height: '400px',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.1)',
              }}
            />
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '10px',
              marginTop: '20px',
            }}>
              {SACRED_FREQUENCIES.map(freq => (
                <div key={freq.hz} style={{
                  backgroundColor: 'rgba(255,255,255,0.02)',
                  border: `1px solid ${freq.color}30`,
                  borderRadius: '6px',
                  padding: '12px',
                }}>
                  <div style={{ color: freq.color, fontSize: '16px', fontWeight: 'bold' }}>
                    {freq.hz} Hz
                  </div>
                  <div style={{ color: COLORS.white, fontSize: '11px', marginTop: '4px' }}>
                    {freq.name}
                  </div>
                  <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '9px', marginTop: '2px' }}>
                    {freq.description}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        textAlign: 'center',
        padding: '20px',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        color: 'rgba(255,255,255,0.15)',
        fontSize: '9px',
        letterSpacing: '0.2em',
      }}>
        AT·OM | DUALITE OPERATIONNELLE | TRAVAIL FREQUENTIEL INVISIBLE
      </div>
    </div>
  );
}

// =============================================================================
// SUB-COMPONENTS
// =============================================================================

function StatCard({ label, value, color }: { label: string; value: string | number; color: string }) {
  return (
    <div style={{
      backgroundColor: 'rgba(0,0,0,0.5)',
      padding: '15px 20px',
    }}>
      <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '9px', letterSpacing: '0.1em' }}>
        {label}
      </div>
      <div style={{ color, fontSize: '24px', fontWeight: 'bold', marginTop: '5px' }}>
        {value}
      </div>
    </div>
  );
}

function ReportCard({ report }: { report: FrequentialReport }) {
  const freq = SACRED_FREQUENCIES.find(f => f.hz === report.agentHz);
  const timeAgo = getTimeAgo(report.timestamp);

  return (
    <div style={{
      backgroundColor: 'rgba(255,255,255,0.02)',
      border: `1px solid ${freq?.color || COLORS.gold}20`,
      borderRadius: '6px',
      padding: '15px',
      display: 'grid',
      gridTemplateColumns: '80px 1fr 120px',
      gap: '15px',
      alignItems: 'center',
    }}>
      <div>
        <div style={{ color: freq?.color || COLORS.gold, fontSize: '18px', fontWeight: 'bold' }}>
          {report.agentHz} Hz
        </div>
        <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '10px' }}>
          {report.agentName}
        </div>
      </div>

      <div>
        <div style={{ color: COLORS.white, fontSize: '12px' }}>
          {report.action}
        </div>
        <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginTop: '4px' }}>
          {report.usersAffected} utilisateurs | +{report.harmonizationDelta.toFixed(2)}% harmonisation | {report.duration}s
        </div>
      </div>

      <div style={{ textAlign: 'right' }}>
        <div style={{ color: 'rgba(255,255,255,0.3)', fontSize: '10px' }}>
          {timeAgo}
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// HELPERS
// =============================================================================

function getRandomAction(agentName: string): string {
  const actions: Record<string, string[]> = {
    'Schumann': [
      'Synchronisation avec la resonance terrestre',
      'Alignement du champ electromagnetique',
      'Calibration de la frequence de base',
    ],
    'Harmonie': [
      'Harmonisation de l\'environnement utilisateur',
      'Equilibrage des frequences ambiantes',
      'Stabilisation du champ harmonique',
    ],
    'Transformation': [
      'Activation du processus de transformation',
      'Transmission de frequences reparatrices',
      'Initiation du cycle de regeneration',
    ],
    'Connexion': [
      'Renforcement des liens inter-utilisateurs',
      'Etablissement de ponts frequentiels',
      'Synchronisation du reseau relationnel',
    ],
    'Expression': [
      'Liberation des blocages expressifs',
      'Activation de l\'intuition creative',
      'Ouverture des canaux d\'expression',
    ],
    'Intuition': [
      'Amplification des signaux intuitifs',
      'Clarification du canal interieur',
      'Renforcement de la perception subtile',
    ],
    'Unite': [
      'Integration de la conscience collective',
      'Unification du champ de conscience',
      'Dissolution des separations illusoires',
    ],
    'AT·OM': [
      'Maintien de la coherence systemique',
      'Orchestration des frequences multiples',
      'Pulsation de la resonance centrale',
    ],
  };

  const agentActions = actions[agentName] || ['Travail frequentiel en cours'];
  return agentActions[Math.floor(Math.random() * agentActions.length)];
}

function getTimeAgo(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);

  if (seconds < 60) return 'il y a quelques secondes';
  if (seconds < 3600) return `il y a ${Math.floor(seconds / 60)} min`;
  if (seconds < 86400) return `il y a ${Math.floor(seconds / 3600)}h`;
  return `il y a ${Math.floor(seconds / 86400)}j`;
}

export default Sovereign;
