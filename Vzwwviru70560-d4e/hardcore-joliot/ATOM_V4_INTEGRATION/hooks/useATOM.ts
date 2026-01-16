/**
 * AT·OM V4 — Hook React Principal
 */
import { useState, useCallback, useMemo, useEffect } from 'react';
import { calculateArithmos, getResonance, goldenDelays, PHI, HEARTBEAT, FREQUENCIES, CIVILIZATIONS, ORACLES, CHAKRAS, SACRED_SITES, FOUNDATION_STONES } from '../index';

let audioContext: AudioContext | null = null;

function playTone(frequency: number, duration: number = 1000): void {
  try {
    if (!audioContext) audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.1);
    gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + duration / 1000);
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration / 1000);
  } catch (e) { console.warn('Audio non disponible'); }
}

export function useATOM(initialWord: string = '') {
  const [word, setWord] = useState(initialWord);
  const [resonance, setResonance] = useState<ReturnType<typeof getResonance> | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(true);
  const [entropyLevel, setEntropyLevel] = useState(0);
  const [lastActivity, setLastActivity] = useState(Date.now());

  const activeChakra = useMemo(() => {
    const hour = new Date().getHours();
    const map: Record<number, number> = { 0:7,1:7,2:7,3:1,4:1,5:1,6:2,7:2,8:3,9:3,10:4,11:4,12:4,13:5,14:5,15:5,16:6,17:6,18:4,19:4,20:7,21:7,22:7,23:7 };
    return CHAKRAS[(map[hour] || 4) - 1];
  }, []);

  const delays = useMemo(() => goldenDelays(100, 8), []);

  useEffect(() => {
    const interval = setInterval(() => {
      const idle = Date.now() - lastActivity;
      const TIMEOUT = 10 * 60 * 1000;
      setEntropyLevel(idle > TIMEOUT ? Math.min(1, (idle - TIMEOUT) * 0.00001) : 0);
    }, 1000);
    return () => clearInterval(interval);
  }, [lastActivity]);

  const illuminate = useCallback(async (wordToIlluminate: string) => {
    setIsAnimating(true);
    setLastActivity(Date.now());
    const res = getResonance(wordToIlluminate);
    setResonance(res);
    setWord(wordToIlluminate);
    if (audioEnabled) playTone(res.frequency, res.delay);
    await new Promise(resolve => setTimeout(resolve, res.delay));
    setIsAnimating(false);
    return res;
  }, [audioEnabled]);

  const playFrequency = useCallback((hz: number, duration = 1000) => {
    if (audioEnabled) playTone(hz, duration);
  }, [audioEnabled]);

  const resetEntropy = useCallback(() => { setLastActivity(Date.now()); setEntropyLevel(0); }, []);
  const toggleAudio = useCallback(() => setAudioEnabled(prev => !prev), []);
  const getOracle = useCallback((id: number) => ORACLES.find(o => o.id === id), []);
  const getCivilization = useCallback((id: string) => CIVILIZATIONS[id as keyof typeof CIVILIZATIONS], []);

  return {
    word, resonance, activeChakra, isAnimating, entropyLevel, audioEnabled,
    setWord, illuminate, playFrequency, resetEntropy, toggleAudio, getOracle, getCivilization,
    phi: PHI, heartbeat: HEARTBEAT, frequencies: FREQUENCIES, civilizations: CIVILIZATIONS,
    oracles: ORACLES, chakras: CHAKRAS, sacredSites: SACRED_SITES, foundationStones: FOUNDATION_STONES,
    goldenDelays: delays
  };
}

export function useEntropy(timeout = 600000) {
  const [entropy, setEntropy] = useState(0);
  const [lastActivity, setLastActivity] = useState(Date.now());
  const resetEntropy = useCallback(() => setLastActivity(Date.now()), []);

  useEffect(() => {
    const interval = setInterval(() => {
      const idle = Date.now() - lastActivity;
      setEntropy(idle > timeout ? Math.min(1, (idle - timeout) * 0.00001) : 0);
    }, 1000);
    return () => clearInterval(interval);
  }, [lastActivity, timeout]);

  const entropyStyle = useMemo(() => ({
    opacity: 1 - entropy * 0.9,
    filter: `grayscale(${entropy * 100}%) blur(${entropy * 2}px)`,
    transition: 'all 2s ease'
  }), [entropy]);

  const entropyMessage = useMemo(() => {
    if (entropy < 0.1) return "✨ L'Arche est vibrante";
    if (entropy < 0.3) return "🌅 L'énergie s'estompe...";
    if (entropy < 0.5) return "🌙 Le savoir attend...";
    if (entropy < 0.7) return "🌑 L'Arche s'assoupit...";
    if (entropy < 0.9) return "💤 Murmures silencieux...";
    return "🕯️ Réveille l'Arche...";
  }, [entropy]);

  return { entropy, resetEntropy, entropyStyle, entropyMessage };
}

export function useSacredGeometry() {
  const fibonacci = useMemo(() => {
    const seq = [0, 1];
    for (let i = 2; i < 20; i++) seq.push(seq[i-1] + seq[i-2]);
    return seq;
  }, []);
  const getGoldenDelay = useCallback((base: number, power = 1) => Math.round(base * Math.pow(PHI, power)), []);
  return { phi: PHI, fibonacci, getGoldenDelay };
}

export function useGlobalSync() {
  const [nearestSite, setNearestSite] = useState(SACRED_SITES[0]);
  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          let min = Infinity, nearest = SACRED_SITES[0];
          for (const site of SACRED_SITES) {
            const d = Math.sqrt(Math.pow(site.lat - pos.coords.latitude, 2) + Math.pow(site.lon - pos.coords.longitude, 2));
            if (d < min) { min = d; nearest = site; }
          }
          setNearestSite(nearest);
        },
        () => {}
      );
    }
  }, []);
  return { nearestSite, syncFrequency: nearestSite.frequency, sacredSites: SACRED_SITES };
}

export function useChakra(chakraNumber?: number) {
  const hour = new Date().getHours();
  const map: Record<number, number> = { 0:7,1:7,2:7,3:1,4:1,5:1,6:2,7:2,8:3,9:3,10:4,11:4,12:4,13:5,14:5,15:5,16:6,17:6,18:4,19:4,20:7,21:7,22:7,23:7 };
  const activeChakra = CHAKRAS[(map[hour] || 4) - 1];
  const selectedChakra = chakraNumber ? CHAKRAS[chakraNumber - 1] : activeChakra;
  const playChakra = useCallback(() => playTone(selectedChakra.frequency, 2000), [selectedChakra]);
  return { chakra: selectedChakra, activeChakra, playChakra, allChakras: CHAKRAS };
}

export function useFoundationStone(stoneName: keyof typeof FOUNDATION_STONES) {
  const stone = FOUNDATION_STONES[stoneName];
  const [isActive, setIsActive] = useState(false);
  const activate = useCallback(() => {
    setIsActive(true);
    playTone(stone.hz, 1000);
    setTimeout(() => setIsActive(false), 1000);
  }, [stone]);
  return { stone, isActive, activate };
}

export default useATOM;
