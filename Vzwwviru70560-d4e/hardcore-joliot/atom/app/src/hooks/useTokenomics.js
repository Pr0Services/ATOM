/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *   AT·OM — useTokenomics Hook (Unified Gateway)
 *
 *   React hook for the complete 4-instrument economic system.
 *   Now powered by the unified API gateway (api.js) instead of raw fetch.
 *
 *   INSTRUMENTS:
 *   - UR (Unite de Resonance) — stable internal currency
 *   - JT (Jetons de Transition) — pre-launch investment tokens
 *   - ATOM (Bonding Curve) — progressive crypto
 *   - NFT (5 Tiers) — symbolic recognition
 *   - Flow Keeper — community stimulus
 *
 *   USAGE:
 *     import { useTokenomics } from '../hooks/useTokenomics';
 *
 *     const {
 *       economy, momentum, nftAvailability, atomState,
 *       contribute, buyAtom, sellAtom, contributeFlow,
 *       loading, error, isSimulation
 *     } = useTokenomics();
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useEffect, useCallback } from 'react';
import { tokenomics as api } from '../lib/api';

/**
 * Simulation data for when backend is offline
 */
const SIMULATION_ECONOMY = {
  ur_total_supply: '0',
  ur_circulating: '0',
  jt_total_minted: '0',
  jt_outstanding: '0',
  atom_supply: '0',
  atom_price: '0.01',
  atom_reserve: '0',
  atom_market_cap: '0',
  nft_minted: { graine: 0, pousse: 0, branche: 0, racine: 0, arbre: 0 },
  total_raised_usd: '0',
  total_contributors: 0,
  flow_total: '0',
  flow_token_count: 0,
  momentum_progress: {
    goal_usd: '100000',
    raised_usd: '0',
    percentage: '0',
    contributors: 0,
  },
  nft_availability: {
    graine: { name: 'Graine de l\'Arche', symbol: '\u{1F330}', minted: 0, max_supply: null, available: 'unlimited', sold_out: false, min_contribution: '10' },
    pousse: { name: 'Pousse de l\'Arbre', symbol: '\u{1F331}', minted: 0, max_supply: 1000, available: 1000, sold_out: false, min_contribution: '100' },
    branche: { name: 'Branche de l\'Arbre de Vie', symbol: '\u{1F33F}', minted: 0, max_supply: 144, available: 144, sold_out: false, min_contribution: '500' },
    racine: { name: 'Racine de l\'Arche', symbol: '\u{1F333}', minted: 0, max_supply: 36, available: 36, sold_out: false, min_contribution: '2000' },
    arbre: { name: 'Arbre de Vie Complet', symbol: '\u{1F332}', minted: 0, max_supply: 9, available: 9, sold_out: false, min_contribution: '10000' },
  },
  bonding_curve: {
    supply: '0',
    max_supply: '9990000',
    price: '0.01',
    reserve: '0',
    market_cap: '0',
  },
};

/**
 * Apply simulation fallback to all state setters
 */
function applySimulation(setters) {
  setters.setEconomy(SIMULATION_ECONOMY);
  setters.setMomentum(SIMULATION_ECONOMY.momentum_progress);
  setters.setNftAvailability(SIMULATION_ECONOMY.nft_availability);
  setters.setAtomState(SIMULATION_ECONOMY.bonding_curve);
  setters.setIsSimulation(true);
}

/**
 * useTokenomics — Main hook for the AT·OM economic system
 */
export function useTokenomics() {
  const [economy, setEconomy] = useState(null);
  const [momentum, setMomentum] = useState(null);
  const [nftAvailability, setNftAvailability] = useState(null);
  const [atomState, setAtomState] = useState(null);
  const [flowWall, setFlowWall] = useState([]);
  const [contributions, setContributions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isSimulation, setIsSimulation] = useState(false);

  const setters = { setEconomy, setMomentum, setNftAvailability, setAtomState, setIsSimulation };

  // ─── FETCH ECONOMY STATE ─────────────────────────────────────────────────

  const fetchEconomy = useCallback(async () => {
    try {
      const result = await api.getEconomy();
      if (result?.success) {
        setEconomy(result.data);
        setMomentum(result.data.momentum_progress);
        setNftAvailability(result.data.nft_availability);
        setAtomState(result.data.bonding_curve);
        setIsSimulation(false);
      } else {
        applySimulation(setters);
      }
    } catch (err) {
      console.warn('[useTokenomics] Using simulation mode:', err.message);
      applySimulation(setters);
    } finally {
      setLoading(false);
    }
  }, []);

  // ─── INITIAL LOAD ─────────────────────────────────────────────────────────

  useEffect(() => {
    fetchEconomy();
  }, [fetchEconomy]);

  // ─── CONTRIBUTE (JT + NFT + FLOW) ────────────────────────────────────────

  const contribute = useCallback(async (amountUsd, flowType = null, message = null) => {
    setError(null);
    try {
      const result = await api.contribute(amountUsd, flowType, message);

      if (result?.success) {
        await fetchEconomy();
        return result.data;
      } else {
        throw new Error(result?.detail || 'Contribution failed');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [fetchEconomy]);

  // ─── BUY ATOM ─────────────────────────────────────────────────────────────

  const buyAtom = useCallback(async (amountTokens) => {
    setError(null);
    try {
      const result = await api.buyAtom(amountTokens);

      if (result?.success) {
        await fetchEconomy();
        return result.data;
      } else {
        throw new Error(result?.detail || 'Buy failed');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [fetchEconomy]);

  // ─── SELL ATOM ────────────────────────────────────────────────────────────

  const sellAtom = useCallback(async (amountTokens) => {
    setError(null);
    try {
      const result = await api.sellAtom(amountTokens);

      if (result?.success) {
        await fetchEconomy();
        return result.data;
      } else {
        throw new Error(result?.detail || 'Sell failed');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [fetchEconomy]);

  // ─── GET ATOM QUOTE ───────────────────────────────────────────────────────

  const getAtomQuote = useCallback(async (action, amountTokens) => {
    try {
      const result = await api.getAtomQuote(action, amountTokens);
      return result?.success ? result.data : null;
    } catch (err) {
      console.warn('[useTokenomics] Quote error:', err.message);
      return null;
    }
  }, []);

  // ─── GET BONDING CURVE CHART DATA ─────────────────────────────────────────

  const getChartData = useCallback(async (points = 50) => {
    try {
      const result = await api.getChartData(points);
      return result?.success ? result.data : [];
    } catch (err) {
      console.warn('[useTokenomics] Chart error:', err.message);
      return [];
    }
  }, []);

  // ─── FLOW KEEPER ──────────────────────────────────────────────────────────

  const contributeFlow = useCallback(async (amountUsd, flowType, message = null) => {
    setError(null);
    try {
      const result = await api.contributeFlow(amountUsd, flowType, message);

      if (result?.success) {
        await fetchEconomy();
        return result.data;
      } else {
        throw new Error(result?.detail || 'Flow contribution failed');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [fetchEconomy]);

  const fetchFlowWall = useCallback(async (limit = 50) => {
    try {
      const result = await api.getFlowWall(limit);
      if (result?.success) {
        setFlowWall(result.data);
        return result.data;
      }
      return [];
    } catch (err) {
      console.warn('[useTokenomics] Flow wall error:', err.message);
      return [];
    }
  }, []);

  // ─── FETCH CONTRIBUTIONS ──────────────────────────────────────────────────

  const fetchContributions = useCallback(async (limit = 20) => {
    try {
      const result = await api.getContributions(limit);
      if (result?.success) {
        setContributions(result.data);
        return result.data;
      }
      return [];
    } catch (err) {
      console.warn('[useTokenomics] Contributions error:', err.message);
      return [];
    }
  }, []);

  // ─── RETURN ───────────────────────────────────────────────────────────────

  return {
    // State
    economy,
    momentum,
    nftAvailability,
    atomState,
    flowWall,
    contributions,
    loading,
    error,
    isSimulation,

    // Actions
    contribute,
    buyAtom,
    sellAtom,
    getAtomQuote,
    getChartData,
    contributeFlow,

    // Data fetching
    fetchEconomy,
    fetchFlowWall,
    fetchContributions,
    refresh: fetchEconomy,
  };
}

export default useTokenomics;
