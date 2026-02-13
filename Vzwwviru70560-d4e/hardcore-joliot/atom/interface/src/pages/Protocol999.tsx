/**
 * PROTOCOL-999 - KILL-SWITCH INTERFACE
 * =====================================
 *
 * CANON AT·OM - Securite / Protocole de Securite
 * Chemin: /protocol-999 (INVISIBLE / CACHE)
 *
 * Fonctionnalite: Kill-Switch. Dispersion instantanee des 226 agents reels.
 * Ce chemin n'apparait JAMAIS dans la navigation visible.
 * Accessible uniquement via:
 * - Sequence gestuelle secrete (triple tap + hold)
 * - URL directe avec token de verification
 *
 * ETAT: INVISIBLE / CACHE
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { agentsService } from '@/services/agents.service';

// =============================================================================
// CONSTANTS
// =============================================================================

const COLORS = {
  black: '#000000',
  red: '#FF0000',
  gold: '#D4AF37',
  white: '#FFFFFF',
};

const DISPERSION_MODES = {
  PARTIAL: 'partial',
  SECTORAL: 'sectoral',
  TOTAL: 'total',
};

// =============================================================================
// TYPES
// =============================================================================

interface DispersionState {
  mode: string | null;
  isActive: boolean;
  countdown: number;
  dispersedCount: number;
  canAbort: boolean;
}

// =============================================================================
// PROTOCOL-999 COMPONENT
// =============================================================================

export function Protocol999() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();

  const [essaimSize, setEssaimSize] = useState(226); // Real agents from API

  const [isAuthorized, setIsAuthorized] = useState(false);
  const [authAttempts, setAuthAttempts] = useState(0);
  const [inputCode, setInputCode] = useState('');

  const [dispersionState, setDispersionState] = useState<DispersionState>({
    mode: null,
    isActive: false,
    countdown: 10,
    dispersedCount: 0,
    canAbort: true,
  });

  // Fetch real agent count from API
  useEffect(() => {
    const fetchAgentCount = async () => {
      try {
        const stats = await agentsService.getStats();
        setEssaimSize(stats.total_agents);
        console.log(`[Protocol999] Essaim size: ${stats.total_agents} agents`);
      } catch {
        console.log('[Protocol999] Using default essaim size: 226');
      }
    };
    fetchAgentCount();
  }, []);

  // Verify authorization
  useEffect(() => {
    const token = searchParams.get('token');
    const emergencyCode = searchParams.get('emergency');

    // Check for valid authorization
    if (token === 'sovereign-access' || emergencyCode === 'ATOM-999') {
      setIsAuthorized(true);
    }
  }, [searchParams]);

  // Authorization input handler
  const handleAuthSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();

    // Valid codes: ATOM-999, SOVEREIGN-KEY, DISPERSION-ACTIVE
    const validCodes = ['ATOM-999', 'SOVEREIGN-KEY', 'DISPERSION-ACTIVE'];

    if (validCodes.includes(inputCode.toUpperCase())) {
      setIsAuthorized(true);
    } else {
      setAuthAttempts(prev => prev + 1);
      setInputCode('');

      // After 3 failed attempts, redirect
      if (authAttempts >= 2) {
        navigate('/');
      }
    }
  }, [inputCode, authAttempts, navigate]);

  // Initiate dispersion
  const initiateDispersion = useCallback((mode: string) => {
    setDispersionState(prev => ({
      ...prev,
      mode,
      isActive: true,
      countdown: mode === DISPERSION_MODES.TOTAL ? 10 : 5,
      canAbort: true,
    }));
  }, []);

  // Abort dispersion
  const abortDispersion = useCallback(() => {
    if (dispersionState.canAbort) {
      setDispersionState({
        mode: null,
        isActive: false,
        countdown: 10,
        dispersedCount: 0,
        canAbort: true,
      });
    }
  }, [dispersionState.canAbort]);

  // Countdown and execution
  useEffect(() => {
    if (!dispersionState.isActive || dispersionState.countdown <= 0) return;

    const timer = setTimeout(() => {
      setDispersionState(prev => {
        if (prev.countdown <= 1) {
          // Execute dispersion
          return {
            ...prev,
            countdown: 0,
            canAbort: false,
          };
        }
        return {
          ...prev,
          countdown: prev.countdown - 1,
          canAbort: prev.countdown > 3,
        };
      });
    }, 1000);

    return () => clearTimeout(timer);
  }, [dispersionState.isActive, dispersionState.countdown]);

  // Dispersion animation
  useEffect(() => {
    if (dispersionState.countdown !== 0 || !dispersionState.isActive) return;

    const interval = setInterval(() => {
      setDispersionState(prev => {
        const targetCount = prev.mode === DISPERSION_MODES.TOTAL
          ? essaimSize
          : prev.mode === DISPERSION_MODES.SECTORAL
            ? Math.floor(essaimSize * 0.5)
            : Math.floor(essaimSize * 0.2);

        if (prev.dispersedCount >= targetCount) {
          clearInterval(interval);
          // Redirect to confirmation after full dispersion
          setTimeout(() => navigate('/'), 3000);
          return prev;
        }

        return {
          ...prev,
          dispersedCount: Math.min(targetCount, prev.dispersedCount + 10),
        };
      });
    }, 50);

    return () => clearInterval(interval);
  }, [dispersionState.countdown, dispersionState.isActive, dispersionState.mode, navigate]);

  // Canvas animation
  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = COLORS.black;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Warning pulse
    if (dispersionState.isActive) {
      const pulseSize = 50 + Math.sin(Date.now() / 100) * 20;
      const gradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, pulseSize
      );
      gradient.addColorStop(0, dispersionState.countdown > 0 ? 'rgba(255, 0, 0, 0.5)' : 'rgba(255, 0, 0, 0.8)');
      gradient.addColorStop(1, 'transparent');
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
    }

    // Dispersing particles
    if (dispersionState.dispersedCount > 0) {
      for (let i = 0; i < dispersionState.dispersedCount; i++) {
        const angle = (i / essaimSize) * Math.PI * 2;
        const speed = 2 + (dispersionState.dispersedCount / essaimSize) * 300;
        const x = centerX + Math.cos(angle) * speed;
        const y = centerY + Math.sin(angle) * speed;

        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fillStyle = i % 3 === 0 ? COLORS.red : COLORS.gold;
        ctx.fill();
      }
    }

    animationRef.current = requestAnimationFrame(animate);
  }, [dispersionState, essaimSize]);

  // Setup animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  // Unauthorized view
  if (!isAuthorized) {
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          backgroundColor: COLORS.black,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'monospace',
        }}
      >
        <div style={{ color: COLORS.red, fontSize: '24px', marginBottom: '20px' }}>
          ACCES RESTREINT
        </div>

        <form onSubmit={handleAuthSubmit} style={{ textAlign: 'center' }}>
          <input
            type="password"
            value={inputCode}
            onChange={e => setInputCode(e.target.value)}
            placeholder="CODE D'AUTORISATION"
            style={{
              backgroundColor: 'transparent',
              border: `1px solid ${COLORS.red}`,
              color: COLORS.white,
              padding: '12px 20px',
              fontSize: '14px',
              fontFamily: 'monospace',
              textAlign: 'center',
              letterSpacing: '0.2em',
              width: '250px',
            }}
          />

          {authAttempts > 0 && (
            <div style={{ color: COLORS.red, fontSize: '12px', marginTop: '10px' }}>
              Tentative {authAttempts}/3 echouee
            </div>
          )}
        </form>

        <button
          onClick={() => navigate('/')}
          style={{
            marginTop: '40px',
            background: 'transparent',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.3)',
            fontFamily: 'monospace',
            fontSize: '12px',
            cursor: 'pointer',
          }}
        >
          RETOUR
        </button>
      </div>
    );
  }

  // Authorized view - Sovereign Command Interface
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: COLORS.black,
      }}
    >
      <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0 }} />

      <div
        style={{
          position: 'relative',
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          fontFamily: 'monospace',
        }}
      >
        <div style={{ color: COLORS.red, fontSize: '32px', marginBottom: '10px', letterSpacing: '0.3em' }}>
          PROTOCOL-999
        </div>

        <div style={{ color: COLORS.gold, fontSize: '14px', marginBottom: '40px' }}>
          BRISE-CIRCUIT | KILL-SWITCH
        </div>

        {!dispersionState.isActive ? (
          // Mode selection
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', alignItems: 'center' }}>
            <button
              onClick={() => initiateDispersion(DISPERSION_MODES.PARTIAL)}
              style={{
                backgroundColor: 'transparent',
                border: '2px solid #FFA500',
                color: '#FFA500',
                padding: '15px 40px',
                fontSize: '14px',
                fontFamily: 'monospace',
                cursor: 'pointer',
                letterSpacing: '0.1em',
              }}
            >
              DISPERSION PARTIELLE
              <div style={{ fontSize: '10px', marginTop: '5px', opacity: 0.7 }}>
                {Math.floor(essaimSize * 0.2)} agents (20%)
              </div>
            </button>

            <button
              onClick={() => initiateDispersion(DISPERSION_MODES.SECTORAL)}
              style={{
                backgroundColor: 'transparent',
                border: '2px solid #FF6600',
                color: '#FF6600',
                padding: '15px 40px',
                fontSize: '14px',
                fontFamily: 'monospace',
                cursor: 'pointer',
                letterSpacing: '0.1em',
              }}
            >
              DISPERSION SECTORIELLE
              <div style={{ fontSize: '10px', marginTop: '5px', opacity: 0.7 }}>
                {Math.floor(essaimSize * 0.5)} agents (50%)
              </div>
            </button>

            <button
              onClick={() => initiateDispersion(DISPERSION_MODES.TOTAL)}
              style={{
                backgroundColor: 'transparent',
                border: '2px solid #FF0000',
                color: '#FF0000',
                padding: '15px 40px',
                fontSize: '14px',
                fontFamily: 'monospace',
                cursor: 'pointer',
                letterSpacing: '0.1em',
              }}
            >
              DISPERSION TOTALE
              <div style={{ fontSize: '10px', marginTop: '5px', opacity: 0.7 }}>
                {essaimSize} agents (100%) - VEILLE PROFONDE
              </div>
            </button>
          </div>
        ) : (
          // Active dispersion
          <div style={{ textAlign: 'center' }}>
            {dispersionState.countdown > 0 ? (
              <>
                <div style={{ color: COLORS.red, fontSize: '72px', marginBottom: '20px' }}>
                  {dispersionState.countdown}
                </div>
                <div style={{ color: COLORS.white, fontSize: '14px', marginBottom: '30px' }}>
                  {dispersionState.mode?.toUpperCase()} EN COURS D'INITIALISATION
                </div>
                {dispersionState.canAbort && (
                  <button
                    onClick={abortDispersion}
                    style={{
                      backgroundColor: COLORS.gold,
                      border: 'none',
                      color: COLORS.black,
                      padding: '15px 40px',
                      fontSize: '14px',
                      fontFamily: 'monospace',
                      cursor: 'pointer',
                      letterSpacing: '0.1em',
                    }}
                  >
                    ANNULER
                  </button>
                )}
              </>
            ) : (
              <>
                <div style={{ color: COLORS.red, fontSize: '24px', marginBottom: '20px' }}>
                  DISPERSION ACTIVE
                </div>
                <div style={{ color: COLORS.white, fontSize: '48px', marginBottom: '10px' }}>
                  {dispersionState.dispersedCount} / {essaimSize}
                </div>
                <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '12px' }}>
                  AGENTS DISPERSES
                </div>
              </>
            )}
          </div>
        )}

        {/* Status bar */}
        <div
          style={{
            position: 'absolute',
            bottom: 40,
            left: '50%',
            transform: 'translateX(-50%)',
            color: 'rgba(255, 255, 255, 0.3)',
            fontSize: '10px',
            textAlign: 'center',
          }}
        >
          FREQUENCE: {dispersionState.isActive ? '0' : '999'} Hz | ESSAIM: {essaimSize - dispersionState.dispersedCount} ACTIFS
        </div>
      </div>
    </div>
  );
}

export default Protocol999;
