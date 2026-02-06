/**
 * AT·OM — Unified API Gateway
 * Author: AT·OM Collective
 */

import { supabase, isSupabaseConfigured, getSession } from './supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * API_URL is empty in production (Vercel proxy rewrites /api/* to DigitalOcean).
 * In development, set REACT_APP_API_URL=http://localhost:8000
 */
const API_URL = process.env.REACT_APP_API_URL || '';

const HEDERA_NETWORK = process.env.REACT_APP_HEDERA_NETWORK || 'testnet';
const HEDERA_TOKEN_ID = process.env.REACT_APP_HEDERA_TOKEN_ID || '0.0.7780104';
const NFT_COLLECTION_ID = process.env.REACT_APP_NFT_COLLECTION_ID || '0.0.7780274';

const HEDERA_MIRROR_URL = HEDERA_NETWORK === 'mainnet'
  ? 'https://mainnet-public.mirrornode.hedera.com'
  : 'https://testnet.mirrornode.hedera.com';

// ═══════════════════════════════════════════════════════════════════════════════
// CORE FETCH (FastAPI backend)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Authenticated fetch to FastAPI backend.
 * Automatically adds Supabase JWT token as Bearer auth.
 */
async function backendFetch(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;

  // Get Supabase JWT for backend auth
  let authHeaders = {};
  try {
    const session = await getSession();
    if (session?.access_token) {
      authHeaders['Authorization'] = `Bearer ${session.access_token}`;
    }
  } catch (e) {
    // No auth — proceed without token
  }

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...options.headers,
      },
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || `API error: ${response.status}`);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      console.warn(`[API] Backend unreachable: ${url}`);
      return null;
    }
    throw error;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 1: AUTHENTICATION (Supabase)
// ═══════════════════════════════════════════════════════════════════════════════

export const auth = {
  signUp: async (email, password, displayName) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          display_name: displayName,
          role: 'citoyen',
          frequency: 444,
          joined_at: new Date().toISOString(),
        },
      },
    });
    if (error) throw error;
    return { success: true, user: data.user };
  },

  signIn: async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return { success: true, user: data.user, session: data.session };
  },

  signOut: async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    return { success: true };
  },

  getUser: async () => {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  },

  getSession,

  onAuthStateChange: (callback) => {
    return supabase.auth.onAuthStateChange(callback);
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 2: PROFILES & SOVEREIGNTY (Supabase)
// ═══════════════════════════════════════════════════════════════════════════════

export const profiles = {
  get: async (userId) => {
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single();
    if (error) throw error;
    return data;
  },

  checkSovereignty: async (userId) => {
    const { data, error } = await supabase
      .from('profiles')
      .select('id, full_name, is_sovereign, hedera_account_id, sovereign_nft_serials, role, frequency')
      .eq('id', userId)
      .single();
    if (error) return { isSovereign: false, profile: null };
    return {
      isSovereign: data?.is_sovereign === true,
      profile: data,
    };
  },

  linkHedera: async (userId, hederaAccountId) => {
    const { data, error } = await supabase
      .from('profiles')
      .update({ hedera_account_id: hederaAccountId, updated_at: new Date().toISOString() })
      .eq('id', userId)
      .select();
    if (error) throw error;
    return data;
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 3: TOKENOMICS ENGINE (FastAPI → /api/v2/tokenomics/*)
// ═══════════════════════════════════════════════════════════════════════════════

export const tokenomics = {
  /** Economy state */
  getEconomy: () => backendFetch('/api/v2/tokenomics/economy'),

  /** Momentum progress toward Phase I goal */
  getMomentum: () => backendFetch('/api/v2/tokenomics/momentum'),

  /** NFT availability per tier */
  getNFTAvailability: () => backendFetch('/api/v2/tokenomics/nft-availability'),

  /** Process a contribution */
  contribute: (amountUsd, flowType = null, message = null, contributorId = null) =>
    backendFetch('/api/v2/tokenomics/contribute', {
      method: 'POST',
      body: JSON.stringify({
        amount_usd: amountUsd,
        flow_type: flowType,
        message: message,
        contributor_id: contributorId,
      }),
    }),

  /** Convert JT to UR */
  convertJT: (contributorId, jtAmount, contributionDate = null) =>
    backendFetch('/api/v2/tokenomics/convert-jt', {
      method: 'POST',
      body: JSON.stringify({
        contributor_id: contributorId,
        jt_amount: jtAmount,
        contribution_date: contributionDate,
      }),
    }),

  /** Recent contribution history */
  getContributions: (limit = 20) =>
    backendFetch(`/api/v2/tokenomics/contributions?limit=${limit}`),

  // ─── ATOM Bonding Curve ──────────────────────────────────────────────────

  /** Buy ATOM tokens */
  buyAtom: (amountTokens) =>
    backendFetch('/api/v2/tokenomics/atom/buy', {
      method: 'POST',
      body: JSON.stringify({ amount_tokens: amountTokens }),
    }),

  /** Sell ATOM tokens */
  sellAtom: (amountTokens) =>
    backendFetch('/api/v2/tokenomics/atom/sell', {
      method: 'POST',
      body: JSON.stringify({ amount_tokens: amountTokens }),
    }),

  /** Get price quote without executing */
  getAtomQuote: (action, amount) =>
    backendFetch(`/api/v2/tokenomics/atom/quote?action=${action}&amount=${amount}`),

  /** Chart data for visualization */
  getChartData: (points = 50) =>
    backendFetch(`/api/v2/tokenomics/atom/chart?points=${points}`),

  /** Current ATOM state */
  getAtomState: () => backendFetch('/api/v2/tokenomics/atom/state'),

  // ─── Flow Keeper ─────────────────────────────────────────────────────────

  /** Flow Keeper contribution */
  contributeFlow: (amountUsd, flowType, message = null, contributorId = null) =>
    backendFetch('/api/v2/tokenomics/flow', {
      method: 'POST',
      body: JSON.stringify({
        amount_usd: amountUsd,
        flow_type: flowType,
        message: message,
        contributor_id: contributorId,
      }),
    }),

  /** Flow Wall (live feed) */
  getFlowWall: (limit = 50) =>
    backendFetch(`/api/v2/tokenomics/flow/wall?limit=${limit}`),

  /** Flow stats by type */
  getFlowStats: () => backendFetch('/api/v2/tokenomics/flow/stats'),

  // ─── UR Admin ────────────────────────────────────────────────────────────

  /** Admin: mint UR */
  mintUR: (amount, reason) =>
    backendFetch('/api/v2/tokenomics/ur/mint', {
      method: 'POST',
      body: JSON.stringify({ amount, reason }),
    }),

  /** Admin: burn UR */
  burnUR: (amount, reason) =>
    backendFetch('/api/v2/tokenomics/ur/burn', {
      method: 'POST',
      body: JSON.stringify({ amount, reason }),
    }),
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 4: RESONANCE ENGINE (FastAPI)
// ═══════════════════════════════════════════════════════════════════════════════

export const resonance = {
  /** Get current resonance state */
  getState: () => backendFetch('/resonance'),

  /** Get R&D rules */
  getRules: () => backendFetch('/rd-rules'),

  /** Health check */
  health: () => backendFetch('/health'),

  /** Readiness check (includes DB + Resonance engine status) */
  ready: () => backendFetch('/health/ready'),

  /** Connect to real-time resonance WebSocket */
  connectWebSocket: (onMessage, onError = null) => {
    const wsUrl = process.env.REACT_APP_WS_URL ||
      (API_URL ? API_URL.replace('http', 'ws') + '/ws/resonance' : null);

    if (!wsUrl) {
      console.warn('[Resonance] WebSocket URL not configured');
      return null;
    }

    const ws = new WebSocket(wsUrl);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.warn('[Resonance] Parse error:', e);
      }
    };
    ws.onerror = (event) => {
      if (onError) onError(event);
      else console.warn('[Resonance] WebSocket error');
    };
    return ws;
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 5: AT·OM MAPPING (FastAPI → /api/v2/atom/*)
// ═══════════════════════════════════════════════════════════════════════════════

export const atomMapping = {
  /** Analyze text via Pythagorean gematria */
  analyzeGematria: (text) =>
    backendFetch('/api/v2/atom/gematria/analyze', {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),

  /** Quick gematria lookup */
  quickGematria: (text) =>
    backendFetch(`/api/v2/atom/gematria/quick?text=${encodeURIComponent(text)}`),

  /** Full vibration profile for visualization */
  getVibrationProfile: (text) =>
    backendFetch('/api/v2/atom/vibration/profile', {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),

  /** Compare vibration profiles */
  compareVibrations: (texts) =>
    backendFetch('/api/v2/atom/vibration/compare', {
      method: 'POST',
      body: JSON.stringify(texts),
    }),

  /** Get active guardrails */
  getGuardrails: () => backendFetch('/api/v2/atom/guardrails'),
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 6: COMMUNITY DATA (Supabase direct)
// ═══════════════════════════════════════════════════════════════════════════════

export const community = {
  /** Submit a local need */
  submitNeed: async (need) => {
    const user = await auth.getUser();
    const { data, error } = await supabase
      .from('local_needs')
      .insert({
        user_id: user?.id,
        title: need.title,
        description: need.description,
        category: need.category,
        location: need.location || 'Quebec',
        priority: need.priority || 'medium',
        votes: 0,
        status: 'pending',
      })
      .select();
    if (error) throw error;
    return data;
  },

  /** Get local needs */
  getNeeds: async (filters = {}, limit = 50) => {
    let query = supabase
      .from('local_needs')
      .select('*')
      .order('votes', { ascending: false });
    if (filters.category) query = query.eq('category', filters.category);
    if (filters.location) query = query.eq('location', filters.location);
    const { data, error } = await query.limit(limit);
    if (error) throw error;
    return data;
  },

  /** Vote for a need */
  voteForNeed: async (needId) => {
    const { data, error } = await supabase.rpc('increment_votes', { need_id: needId });
    if (error) throw error;
    return data;
  },

  /** Save a perception */
  savePerception: async (perception) => {
    const user = await auth.getUser();
    const { data, error } = await supabase
      .from('perceptions')
      .insert({
        user_id: user?.id || null,
        text: perception.text,
        frequency: perception.frequency || 999,
        heartbeat: perception.heartbeat || 444,
      })
      .select();
    if (error) throw error;
    return data;
  },

  /** Get perceptions */
  getPerceptions: async (userId, limit = 100) => {
    const { data, error } = await supabase
      .from('perceptions')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit);
    if (error) throw error;
    return data;
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 7: HEDERA MIRROR NODE (Read-only, no auth needed)
// ═══════════════════════════════════════════════════════════════════════════════

export const hedera = {
  /** Get ATOM token info from mirror node */
  getTokenInfo: async () => {
    try {
      const response = await fetch(`${HEDERA_MIRROR_URL}/api/v1/tokens/${HEDERA_TOKEN_ID}`);
      if (!response.ok) return null;
      return await response.json();
    } catch (e) {
      console.warn('[Hedera] Mirror node error:', e.message);
      return null;
    }
  },

  /** Get NFT collection info */
  getNFTCollectionInfo: async () => {
    try {
      const response = await fetch(`${HEDERA_MIRROR_URL}/api/v1/tokens/${NFT_COLLECTION_ID}`);
      if (!response.ok) return null;
      return await response.json();
    } catch (e) {
      console.warn('[Hedera] Mirror node error:', e.message);
      return null;
    }
  },

  /** Get token balance for a Hedera account */
  getTokenBalance: async (accountId) => {
    try {
      const response = await fetch(
        `${HEDERA_MIRROR_URL}/api/v1/accounts/${accountId}/tokens?token.id=${HEDERA_TOKEN_ID}`
      );
      if (!response.ok) return null;
      const data = await response.json();
      return data.tokens?.[0] || null;
    } catch (e) {
      console.warn('[Hedera] Balance check error:', e.message);
      return null;
    }
  },

  /** Get NFTs owned by an account */
  getNFTs: async (accountId) => {
    try {
      const response = await fetch(
        `${HEDERA_MIRROR_URL}/api/v1/accounts/${accountId}/nfts?token.id=${NFT_COLLECTION_ID}`
      );
      if (!response.ok) return null;
      const data = await response.json();
      return data.nfts || [];
    } catch (e) {
      console.warn('[Hedera] NFT check error:', e.message);
      return [];
    }
  },

  /** Get Hashscan URL for a token */
  getHashscanUrl: (tokenId) =>
    `https://hashscan.io/${HEDERA_NETWORK}/token/${tokenId || HEDERA_TOKEN_ID}`,

  /** Config info */
  config: {
    tokenId: HEDERA_TOKEN_ID,
    nftCollectionId: NFT_COLLECTION_ID,
    network: HEDERA_NETWORK,
    mirrorUrl: HEDERA_MIRROR_URL,
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 8: NOVA PIPELINE (FastAPI → /api/v2/*)
// ═══════════════════════════════════════════════════════════════════════════════

export const nova = {
  /** Get agents (paginated) */
  getAgents: (page = 1, pageSize = 50) =>
    backendFetch(`/api/v2/agents?page=${page}&page_size=${pageSize}`),

  /** Threads */
  getThreads: () => backendFetch('/api/v2/threads'),
  createThread: (data) =>
    backendFetch('/api/v2/threads', { method: 'POST', body: JSON.stringify(data) }),

  /** Spheres */
  getSpheres: () => backendFetch('/api/v2/spheres'),

  /** Memory */
  getMemory: () => backendFetch('/api/v2/memory'),
};

// ═══════════════════════════════════════════════════════════════════════════════
// UNIFIED EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

const api = {
  auth,
  profiles,
  tokenomics,
  resonance,
  atomMapping,
  community,
  hedera,
  nova,
  // Utility
  backendFetch,
  isSupabaseConfigured,
  config: {
    apiUrl: API_URL,
    hederaNetwork: HEDERA_NETWORK,
    hederaTokenId: HEDERA_TOKEN_ID,
    nftCollectionId: NFT_COLLECTION_ID,
  },
};

export default api;
