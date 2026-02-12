/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — MINT DIVINE ARMOR NFT
 * ═══════════════════════════════════════════════════════════════════════════
 * Script de création du NFT d'Armure Divine sur Hedera
 * Utilise les métadonnées de metadata.json
 * ═══════════════════════════════════════════════════════════════════════════
 */

const {
    Client,
    TokenCreateTransaction,
    TokenType,
    TokenSupplyType,
    TokenMintTransaction,
    PrivateKey
} = require('@hashgraph/sdk');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { config, validateConfig } = require('./config');

// Charger les métadonnées
const metadataPath = path.join(__dirname, 'metadata.json');

async function mintArmor() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('        AT·OM — CRÉATION ARMURE DIVINE NFT');
    console.log('═══════════════════════════════════════════════════════════════\n');

    // =========================================================================
    // ÉTAPE 1: Validation de la configuration
    // =========================================================================
    console.log('📋 Étape 1: Validation de la configuration...');

    const validation = validateConfig();
    if (!validation.valid) {
        console.log('❌ Configuration invalide:');
        validation.errors.forEach(e => console.log(`   - ${e}`));
        console.log('\n⚠️  Vérifie ton fichier .env à la racine du projet');
        return { success: false, step: 'config', errors: validation.errors };
    }
    console.log('✅ Configuration validée\n');

    // =========================================================================
    // ÉTAPE 2: Lecture des métadonnées
    // =========================================================================
    console.log('📋 Étape 2: Lecture des métadonnées...');

    if (!fs.existsSync(metadataPath)) {
        console.log('❌ Fichier metadata.json introuvable');
        return { success: false, step: 'metadata', error: 'metadata.json missing' };
    }

    const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));

    // Vérifier que les mesures sont remplies
    const mesures = metadata.attributes.filter(a => a.trait_type.startsWith('Mesure_'));
    const mesuresVides = mesures.filter(m => !m.value || m.value === '');

    if (mesuresVides.length > 0) {
        console.log('❌ Métadonnées incomplètes:');
        mesuresVides.forEach(m => console.log(`   - ${m.trait_type} est vide`));
        console.log('\n⚠️  Remplis tes mesures M, P, I, Po dans metadata.json');
        return { success: false, step: 'metadata', error: 'mesures vides' };
    }

    // Vérifier l'image
    if (!metadata.image || metadata.image === 'LIEN_VERS_TON_IMAGE_V4_ICI') {
        console.log('❌ Lien vers l\'image non configuré');
        console.log('\n⚠️  Ajoute le lien vers ton image V4 dans metadata.json');
        return { success: false, step: 'metadata', error: 'image manquante' };
    }

    console.log('✅ Métadonnées validées');
    console.log(`   Nom: ${metadata.name}`);
    mesures.forEach(m => console.log(`   ${m.trait_type}: ${m.value}`));
    console.log('');

    // =========================================================================
    // ÉTAPE 3: Génération du hash biométrique
    // =========================================================================
    console.log('📋 Étape 3: Génération de la signature biométrique...');

    const biometricString = mesures.map(m => m.value).join(':');
    const biometricHash = crypto.createHash('sha256').update(biometricString).digest('hex');

    console.log(`✅ Hash biométrique: ${biometricHash.substring(0, 16)}...`);
    console.log('');

    // =========================================================================
    // ÉTAPE 4: Vérification du mode simulation
    // =========================================================================
    if (config.security.simulationMode) {
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              ⚠️  MODE SIMULATION ACTIVÉ');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('Aucune transaction réelle ne sera effectuée.');
        console.log('');
        console.log('Pour créer le vrai NFT:');
        console.log('1. Modifie HEDERA_SIMULATION_MODE=false dans .env');
        console.log('2. Assure-toi d\'avoir assez de HBAR sur ton compte');
        console.log('3. Relance ce script');
        console.log('═══════════════════════════════════════════════════════════════\n');

        return {
            success: true,
            simulated: true,
            metadata: metadata,
            biometricHash: biometricHash
        };
    }

    // =========================================================================
    // ÉTAPE 5: Connexion au réseau Hedera
    // =========================================================================
    console.log('📋 Étape 5: Connexion au réseau Hedera...');

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

    console.log(`✅ Connecté au ${config.network}`);
    console.log(`   Opérateur: ${config.operator.accountId}`);
    console.log('');

    // =========================================================================
    // ÉTAPE 6: Création du Token NFT
    // =========================================================================
    console.log('📋 Étape 6: Création du Token NFT...');

    try {
        // Créer le token NFT (Collection)
        const createTokenTx = new TokenCreateTransaction()
            .setTokenName(metadata.name)
            .setTokenSymbol('ATOM')
            .setTokenType(TokenType.NonFungibleUnique)
            .setSupplyType(TokenSupplyType.Finite)
            .setMaxSupply(1) // NFT unique
            .setInitialSupply(0)
            .setTreasuryAccountId(config.operator.accountId)
            .setAdminKey(operatorKey)
            .setSupplyKey(operatorKey)
            .setFreezeKey(operatorKey)
            .setPauseKey(operatorKey)
            .setTokenMemo(`AT·OM Divine Armor | Hash: ${biometricHash.substring(0, 16)}`);

        const createResponse = await createTokenTx.execute(client);
        const createReceipt = await createResponse.getReceipt(client);
        const tokenId = createReceipt.tokenId;

        console.log(`✅ Token créé: ${tokenId.toString()}`);
        console.log('');

        // =====================================================================
        // ÉTAPE 7: Mint du NFT
        // =====================================================================
        console.log('📋 Étape 7: Mint du NFT...');

        // Hedera limite les métadonnées à 100 bytes
        // On stocke le hash biométrique (les détails complets sont sur Supabase/IPFS)
        const metadataBytes = Buffer.from(biometricHash.substring(0, 64));

        const mintTx = new TokenMintTransaction()
            .setTokenId(tokenId)
            .addMetadata(metadataBytes);

        const mintResponse = await mintTx.execute(client);
        const mintReceipt = await mintResponse.getReceipt(client);
        const serialNumber = mintReceipt.serials[0].toString();

        console.log(`✅ NFT minté avec succès!`);
        console.log(`   Serial: ${serialNumber}`);
        console.log('');

        // =====================================================================
        // RÉSULTAT FINAL
        // =====================================================================
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              🟢 ARMURE DIVINE CRÉÉE');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Token ID: ${tokenId.toString()}`);
        console.log(`   Serial: #${serialNumber}`);
        console.log(`   Hash: ${biometricHash}`);
        console.log(`   Network: ${config.network}`);
        console.log('');
        console.log(`   Explorer: https://hashscan.io/${config.network}/token/${tokenId.toString()}`);
        console.log('═══════════════════════════════════════════════════════════════\n');

        client.close();

        return {
            success: true,
            tokenId: tokenId.toString(),
            serial: serialNumber,
            biometricHash: biometricHash,
            network: config.network,
            explorer: `https://hashscan.io/${config.network}/token/${tokenId.toString()}`
        };

    } catch (error) {
        console.log(`❌ Erreur lors du mint: ${error.message}`);
        client.close();
        return { success: false, step: 'mint', error: error.message };
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// EXÉCUTION
// ═══════════════════════════════════════════════════════════════════════════
if (require.main === module) {
    mintArmor()
        .then(result => {
            if (!result.success && !result.simulated) {
                process.exit(1);
            }
        })
        .catch(error => {
            console.error('❌ Erreur inattendue:', error);
            process.exit(1);
        });
}

module.exports = { mintArmor };
