/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — HEDERA CONNECTION TEST
 * ═══════════════════════════════════════════════════════════════════════════
 * Script de validation de connexion au Testnet Hedera
 * ═══════════════════════════════════════════════════════════════════════════
 */

const { Client, AccountBalanceQuery } = require('@hashgraph/sdk');
const { config, validateConfig } = require('./config');

async function testConnection() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('          AT·OM — TEST CONNEXION HEDERA');
    console.log('═══════════════════════════════════════════════════════════════\n');

    // Step 1: Validate configuration
    console.log('📋 Validation de la configuration...');
    const validation = validateConfig();

    if (!validation.valid) {
        console.log('❌ Configuration invalide:');
        validation.errors.forEach(e => console.log(`   - ${e}`));
        return { success: false, step: 'config', errors: validation.errors };
    }
    console.log('✅ Configuration valide\n');

    // Step 2: Display configuration (sans secrets)
    console.log('📡 Configuration:');
    console.log(`   Network: ${config.network}`);
    console.log(`   Operator ID: ${config.operator.accountId}`);
    console.log(`   Simulation Mode: ${config.security.simulationMode}`);
    console.log('');

    // Step 3: Test client connection
    console.log('🔌 Connexion au client Hedera...');

    let client;
    try {
        if (config.network === 'testnet') {
            client = Client.forTestnet();
        } else if (config.network === 'mainnet') {
            client = Client.forMainnet();
        } else {
            client = Client.forPreviewnet();
        }

        client.setOperator(config.operator.accountId, config.operator.privateKey);
        console.log('✅ Client initialisé\n');
    } catch (error) {
        console.log(`❌ Erreur initialisation client: ${error.message}`);
        return { success: false, step: 'client', error: error.message };
    }

    // Step 4: Query account balance
    console.log('💰 Récupération du solde du compte...');

    try {
        const balance = await new AccountBalanceQuery()
            .setAccountId(config.operator.accountId)
            .execute(client);

        console.log(`✅ Solde HBAR: ${balance.hbars.toString()}`);

        if (balance.tokens && balance.tokens.size > 0) {
            console.log('   Tokens associés:');
            balance.tokens.forEach((amount, tokenId) => {
                console.log(`   - ${tokenId.toString()}: ${amount.toString()}`);
            });
        }
        console.log('');
    } catch (error) {
        console.log(`❌ Erreur requête solde: ${error.message}`);
        return { success: false, step: 'balance', error: error.message };
    }

    // Step 5: Final status
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('                    🟢 CONNEXION RÉUSSIE');
    console.log('═══════════════════════════════════════════════════════════════\n');

    client.close();

    return {
        success: true,
        network: config.network,
        accountId: config.operator.accountId,
        status: 'OPERATIONAL'
    };
}

// Run if executed directly
if (require.main === module) {
    testConnection()
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

module.exports = { testConnection };
