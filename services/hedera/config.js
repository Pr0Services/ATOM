/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — HEDERA CONFIGURATION
 * ═══════════════════════════════════════════════════════════════════════════
 * Configuration centralisée pour toutes les connexions Hedera
 * Utilise les variables d'environnement pour les secrets
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });

const config = {
    // Network Configuration
    network: process.env.HEDERA_NETWORK || 'testnet',
    mirrorNode: process.env.HEDERA_MIRROR_NODE_URL || 'https://testnet.mirrornode.hedera.com',

    // Operator Credentials
    operator: {
        accountId: process.env.HEDERA_OPERATOR_ID || process.env.MY_ACCOUNT_ID,
        privateKey: process.env.HEDERA_OPERATOR_KEY || process.env.MY_PRIVATE_KEY
    },

    // UR Token Settings
    token: {
        id: process.env.HEDERA_UR_TOKEN_ID || null,
        name: process.env.UR_TOKEN_NAME || 'Unité de Résonance',
        symbol: process.env.UR_TOKEN_SYMBOL || 'UR',
        decimals: parseInt(process.env.UR_TOKEN_DECIMALS) || 8,
        initialSupply: parseInt(process.env.UR_TOKEN_INITIAL_SUPPLY) || 0
    },

    // HCS Settings
    hcs: {
        topicId: process.env.HEDERA_HCS_TOPIC_ID || null,
        topicMemo: process.env.HCS_TOPIC_MEMO || 'AT·OM Sovereign Economy Audit Log'
    },

    // Treasury
    treasury: {
        accountId: process.env.HEDERA_TREASURY_ACCOUNT || process.env.HEDERA_OPERATOR_ID
    },

    // Economic Parameters
    economics: {
        baseRateCAD: parseFloat(process.env.UR_BASE_RATE_CAD) || 1.35,
        baseRateUSD: parseFloat(process.env.UR_BASE_RATE_USD) || 1.00,
        minReserveRatio: parseInt(process.env.MIN_RESERVE_RATIO) || 80,
        maxMintAmount: parseInt(process.env.MAX_MINT_AMOUNT) || 1000000000
    },

    // Security
    security: {
        simulationMode: process.env.HEDERA_SIMULATION_MODE === 'true',
        txTimeout: parseInt(process.env.HEDERA_TX_TIMEOUT) || 30,
        maxRetries: parseInt(process.env.HEDERA_MAX_RETRIES) || 3
    }
};

/**
 * Validate configuration
 */
function validateConfig() {
    const errors = [];

    if (!config.operator.accountId) {
        errors.push('HEDERA_OPERATOR_ID ou MY_ACCOUNT_ID manquant');
    }

    if (!config.operator.privateKey || config.operator.privateKey === 'private_key') {
        errors.push('HEDERA_OPERATOR_KEY ou MY_PRIVATE_KEY manquant ou placeholder');
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

module.exports = { config, validateConfig };
