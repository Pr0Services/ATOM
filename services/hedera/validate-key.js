/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — VALIDATE HEDERA KEY FORMAT
 * ═══════════════════════════════════════════════════════════════════════════
 * Script pour valider que la clé Hedera est au format ED25519
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });
const { PrivateKey } = require('@hashgraph/sdk');

// Préfixes DER pour identifier le type de clé
const ED25519_PREFIX = '302e020100300506032b6570';
const ECDSA_PREFIX = '3030020100300706052b8104000a';

function validateKey() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('        AT·OM — VALIDATION CLÉ HEDERA');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const privateKeyStr = process.env.HEDERA_OPERATOR_KEY || process.env.MY_PRIVATE_KEY;

    if (!privateKeyStr || privateKeyStr === 'YOUR_PRIVATE_KEY_HERE') {
        console.log('❌ Clé privée non configurée dans .env');
        console.log('');
        console.log('📋 Pour obtenir ta clé ED25519:');
        console.log('   1. Va sur https://portal.hedera.com/');
        console.log('   2. Connecte-toi à ton compte');
        console.log('   3. Va dans "Keys" ou "Account Details"');
        console.log('   4. Copie ta "Private Key" (format DER hex)');
        console.log('   5. Colle-la dans .env (HEDERA_OPERATOR_KEY et MY_PRIVATE_KEY)');
        console.log('');
        return { valid: false, type: null, error: 'key not configured' };
    }

    // Détecter le type de clé
    let keyType = 'UNKNOWN';
    let isED25519 = false;

    if (privateKeyStr.toLowerCase().startsWith(ED25519_PREFIX.toLowerCase())) {
        keyType = 'ED25519';
        isED25519 = true;
    } else if (privateKeyStr.toLowerCase().startsWith(ECDSA_PREFIX.toLowerCase())) {
        keyType = 'ECDSA';
        isED25519 = false;
    } else if (privateKeyStr.length === 64 || privateKeyStr.length === 66) {
        // Clé raw hex (32 bytes = 64 chars)
        keyType = 'RAW_HEX (probablement ED25519)';
        isED25519 = true;
    }

    console.log(`📋 Analyse de la clé...`);
    console.log(`   Longueur: ${privateKeyStr.length} caractères`);
    console.log(`   Préfixe: ${privateKeyStr.substring(0, 24)}...`);
    console.log(`   Type détecté: ${keyType}`);
    console.log('');

    // Tenter de parser la clé
    try {
        let privateKey;

        if (keyType === 'ED25519' || privateKeyStr.toLowerCase().startsWith('302e')) {
            privateKey = PrivateKey.fromStringED25519(privateKeyStr);
            keyType = 'ED25519';
            isED25519 = true;
        } else if (keyType === 'ECDSA' || privateKeyStr.toLowerCase().startsWith('3030')) {
            privateKey = PrivateKey.fromStringECDSA(privateKeyStr);
            keyType = 'ECDSA';
            isED25519 = false;
        } else {
            // Essayer ED25519 par défaut
            try {
                privateKey = PrivateKey.fromStringED25519(privateKeyStr);
                keyType = 'ED25519';
                isED25519 = true;
            } catch {
                privateKey = PrivateKey.fromStringECDSA(privateKeyStr);
                keyType = 'ECDSA';
                isED25519 = false;
            }
        }

        const publicKey = privateKey.publicKey;

        console.log('═══════════════════════════════════════════════════════════════');
        if (isED25519) {
            console.log('              🟢 CLÉ ED25519 VALIDÉE');
        } else {
            console.log('              ⚠️  CLÉ ECDSA DÉTECTÉE');
        }
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Type: ${keyType}`);
        console.log(`   Public Key: ${publicKey.toString().substring(0, 40)}...`);
        console.log('');

        if (!isED25519) {
            console.log('⚠️  RECOMMANDATION:');
            console.log('   Pour une sécurité maximale, utilise une clé ED25519.');
            console.log('   ED25519 offre:');
            console.log('   - Signatures plus rapides');
            console.log('   - Meilleure résistance aux attaques');
            console.log('   - Compatibilité optimale avec Hedera');
            console.log('');
            console.log('   Pour générer une nouvelle clé ED25519:');
            console.log('   1. Va sur https://portal.hedera.com/');
            console.log('   2. Crée un nouveau compte ou régénère ta clé');
            console.log('   3. Sélectionne "ED25519" comme type de clé');
            console.log('');
        }

        return {
            valid: true,
            type: keyType,
            isED25519: isED25519,
            publicKey: publicKey.toString()
        };

    } catch (error) {
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              ❌ CLÉ INVALIDE');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Erreur: ${error.message}`);
        console.log('');
        console.log('   Vérifie que ta clé est correctement copiée dans .env');
        console.log('   Format attendu: chaîne hexadécimale sans espaces');
        console.log('');

        return { valid: false, type: null, error: error.message };
    }
}

// Run if executed directly
if (require.main === module) {
    validateKey();
}

module.exports = { validateKey };
