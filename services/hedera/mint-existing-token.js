/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — MINT NFT ON EXISTING TOKEN
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });
const { Client, TokenMintTransaction, PrivateKey } = require('@hashgraph/sdk');
const crypto = require('crypto');

const TOKEN_ID = '0.0.7780104'; // AT-OM$ Token (remplace ZAMA 0.0.7730446 compromis)

async function mintOnExistingToken() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('        AT·OM — MINT SUR TOKEN EXISTANT');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const operatorId = process.env.HEDERA_OPERATOR_ID;
    const operatorKey = process.env.HEDERA_OPERATOR_KEY;

    // Générer le hash biométrique
    const biometricString = '44.4:161.8:369:1728';
    const biometricHash = crypto.createHash('sha256').update(biometricString).digest('hex');

    console.log(`📋 Token ID: ${TOKEN_ID}`);
    console.log(`📋 Hash biométrique: ${biometricHash.substring(0, 16)}...`);
    console.log('');

    // Connexion
    const client = Client.forTestnet();
    client.setOperator(operatorId, PrivateKey.fromString(operatorKey));

    console.log('🔨 Mint en cours...');

    try {
        const mintTx = new TokenMintTransaction()
            .setTokenId(TOKEN_ID)
            .addMetadata(Buffer.from(biometricHash.substring(0, 64)));

        const response = await mintTx.execute(client);
        const receipt = await response.getReceipt(client);
        const serialNumber = receipt.serials[0].toString();

        console.log('');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              🟢 NFT AT-OM$ CRÉÉ AVEC SUCCÈS !');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Token ID: ${TOKEN_ID}`);
        console.log(`   Serial: #${serialNumber}`);
        console.log(`   Hash: ${biometricHash}`);
        console.log('');
        console.log(`   🔗 Voir sur Hashscan:`);
        console.log(`   https://hashscan.io/testnet/token/${TOKEN_ID}`);
        console.log('═══════════════════════════════════════════════════════════════\n');

        client.close();
        return { success: true, tokenId: TOKEN_ID, serial: serialNumber };

    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        client.close();
        return { success: false, error: error.message };
    }
}

mintOnExistingToken();
