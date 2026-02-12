/**
 * AT·OM — useEconomy
 * Hook d'économie de résonance — transactions UR, FlowKeeper, stabilisation
 *
 * "La richesse circule comme le sang. Donner = Recevoir."
 *
 * Le même flux Rosetta circule ici :
 *   TECH   → Payload JSON (montant, type, from/to, metadata)
 *   PEOPLE → Narration humaine ("Pierre a contribué 100 UR à la Sphère Santé")
 *   SPIRIT → Fréquence modifiée par le type de transaction
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import type { SphereId } from '../types/atom-types';
import { DEFAULT_FLOW_KEEPER } from '../types/atom-types';

/** Types de transaction exposés par le hook */
export type TransactionParams = {
  type: 'CONTRIBUTION' | 'FLOW_KEEPER' | 'EXCHANGE' | 'REBATE' | 'STIMULUS' | 'BURN' | 'MINT_JT' | 'MINT_SOUVENIR';
  amount_ur: number;
  sphere_id: SphereId;
  description?: string;
  to_id?: string;
};

export function useEconomy() {
  const { state, dispatch, parser, flowKeeper } = useATOM();
  const { economy } = state;

  // ─── Créer une transaction ──────────────────────────────
  const createTransaction = useCallback((params: TransactionParams) => {
    if (params.amount_ur <= 0) {
      return { success: false, reason: 'Montant doit être positif' };
    }

    const fromResonance = state.identity.sovereign_identity?.resonance_score ?? 0;

    // Traduire par Rosetta (3 dimensions)
    parser.translate('economy', {
      transaction_type: params.type,
      sphere_id: params.sphere_id,
      amount: params.amount_ur,
      from_resonance: fromResonance,
      to_resonance: 0,
      description: params.description ?? '',
    }, 'TECH', `tx_${Date.now().toString(36)}`);

    // Mettre à jour le state local
    const newBalance = params.type === 'BURN'
      ? economy.balance_ur - params.amount_ur
      : params.type === 'CONTRIBUTION' || params.type === 'FLOW_KEEPER'
        ? economy.balance_ur - params.amount_ur
        : economy.balance_ur;

    dispatch({
      type: 'ECONOMY_UPDATE',
      payload: { balance_ur: Math.max(0, newBalance) },
    });

    return { success: true };
  }, [state, dispatch, parser, economy]);

  // ─── FlowKeeper — Diagnostic ───────────────────────────
  const getFlowKeeperAnalysis = useCallback(() => {
    return flowKeeper.analyze({
      velocity_30d: economy.velocity_30d,
      reserve_ratio: economy.total_supply > 0 ? 1.0 : 0,
      total_supply: economy.total_supply,
      total_burned: 0,
    });
  }, [flowKeeper, economy]);

  // ─── Calculs utilitaires ───────────────────────────────
  const calculateRebate = useCallback((amount: number, resonanceScore: number) => {
    return flowKeeper.calculateRebate(amount, resonanceScore);
  }, [flowKeeper]);

  const calculateBurn = useCallback((amount: number) => {
    return flowKeeper.calculateBurn(amount);
  }, [flowKeeper]);

  // ─── Métriques dérivées ─────────────────────────────────
  const isHealthy = useMemo(() =>
    economy.flow_keeper_status === 'EQUILIBRE',
  [economy.flow_keeper_status]);

  return {
    // État
    balanceUR: economy.balance_ur,
    flowKeeperStatus: economy.flow_keeper_status,
    totalSupply: economy.total_supply,
    velocity30d: economy.velocity_30d,
    isHealthy,

    // Actions
    createTransaction,

    // FlowKeeper
    getFlowKeeperAnalysis,
    calculateRebate,
    calculateBurn,

    // Constantes
    config: DEFAULT_FLOW_KEEPER,
  };
}
