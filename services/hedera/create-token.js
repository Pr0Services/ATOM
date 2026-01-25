/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — CREATE UR TOKEN
 * ═══════════════════════════════════════════════════════════════════════════
 * Script de création du token UR sur Hedera
 * ═══════════════════════════════════════════════════════════════════════════
 */

const {
    Client,
    TokenCreateTransaction,
    TokenType,
    TokenSupplyType,
    PrivateKey
} = require('@hashgraph/sdk');
const { config, validateConfig } = require('./config');

async function createURToken() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('          AT·OM — CRÉATION TOKEN UR');
    console.log('═══════════════════════════════════════════════════════════════\n');

    // Validate configuration
    const validation = validateConfig();
    if (!validation.valid) {
        console.log('❌ Configuration invalide:');
        validation.errors.forEach(e => console.log(`   - ${e}`));
        return { success: false, errors: validation.errors };
    }

    // Check simulation mode
    if (config.security.simulationMode) {
        console.log('⚠️  Mode simulation activé - aucune transaction réelle');
        console.log('   Pour créer un vrai token, mettre HEDERA_SIMULATION_MODE=false\n');
        return {
            success: true,
            simulated: true,
            token: {
                name: config.token.name,
                symbol: config.token.symbol,
                decimals: config.token.decimals
            }
        };
    }

    // Initialize client
    let client;
    if (config.network === 'testnet') {
        client = Client.forTestnet();
    } else if (config.network === 'mainnet') {
        client = Client.forMainnet();
    } else {
        client = Client.forPreviewnet();
    }

    const operatorKey = PrivateKey.fromString(config.operator.privateKey);
    client.setOperator(config.operator.accountId, operatorKey);

    console.log('📋 Paramètres du token:');
    console.log(`   Nom: ${config.token.name}`);
    console.log(`   Symbole: ${config.token.symbol}`);
    console.log(`   Décimales: ${config.token.decimals}`);
    console.log(`   Supply initiale: ${config.token.initialSupply}`);
    console.log('');

    try {
        console.log('🔨 Création du token...');

        const transaction = new TokenCreateTransaction()
            .setTokenName(config.token.name)
            .setTokenSymbol(config.token.symbol)
            .setDecimals(config.token.decimals)
            .setInitialSupply(config.token.initialSupply)
            .setTreasuryAccountId(config.operator.accountId)
            .setAdminKey(operatorKey)
            .setSupplyKey(operatorKey)
            .setFreezeKey(operatorKey)
            .setPauseKey(operatorKey)
            .setTokenType(TokenType.FungibleCommon)
            .setSupplyType(TokenSupplyType.Infinite)
            .setTokenMemo('AT·OM Sovereign Economy - Unité de Résonance');

        const response = await transaction.execute(client);
        const receipt = await response.getReceipt(client);
        const tokenId = receipt.tokenId;

        console.log('');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              🟢 TOKEN CRÉÉ AVEC SUCCÈS');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Token ID: ${tokenId.toString()}`);
        console.log('');
        console.log('⚠️  IMPORTANT: Ajouter cette ligne à votre .env:');
        console.log(`   HEDERA_UR_TOKEN_ID=${tokenId.toString()}`);
        console.log('═══════════════════════════════════════════════════════════════\n');

        client.close();

        return {
            success: true,
            tokenId: tokenId.toString(),
            name: config.token.name,
            symbol: config.token.symbol
        };

    } catch (error) {
        console.log(`❌ Erreur création token: ${error.message}`);
        client.close();
        return { success: false, error: error.message };
    }
}

// Run if executed directly
if (require.main === module) {
    createURToken()
        .then(result => {
            if (!result.success) {
                process.exit(1);
            }
        })
        .catch(error => {
            console.error('❌ Erreur inattendue:', error);
            process.exit(1);
        });
}

module.exports = { createURToken };
