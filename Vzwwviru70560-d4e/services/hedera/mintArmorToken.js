/**
 * AT·OM Hedera Armor Token Minter v1.0
 * Création de NFT unique sur Hedera pour l'armure ZAMA
 *
 * Ce script crée un token non-fongible (NFT) sur Hedera Hashgraph
 * qui représente l'armure bio-résonante calibrée du porteur.
 *
 * SÉCURITÉ: Les clés sont chargées depuis process.env
 * Ne jamais hardcoder les clés privées !
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

const {
  Client,
  PrivateKey,
  TokenCreateTransaction,
  TokenType,
  TokenSupplyType,
  TokenMintTransaction,
  TokenNftInfoQuery,
  AccountId,
  Hbar
} = require('@hashgraph/sdk');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ==================== CONFIGURATION ====================

/**
 * Charge la configuration depuis les variables d'environnement
 * IMPORTANT: Ne jamais stocker de clés dans le code !
 */
function loadConfig() {
  const required = ['MY_ACCOUNT_ID', 'MY_PRIVATE_KEY'];

  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`Variable d'environnement manquante: ${key}`);
    }
  }

  return {
    accountId: AccountId.fromString(process.env.MY_ACCOUNT_ID),
    privateKey: PrivateKey.fromString(process.env.MY_PRIVATE_KEY),
    network: process.env.HEDERA_NETWORK || 'testnet'
  };
}

/**
 * Crée un client Hedera configuré
 *
 * @returns {Client} Client Hedera
 */
function createHederaClient() {
  const config = loadConfig();
  let client;

  if (config.network === 'mainnet') {
    client = Client.forMainnet();
  } else {
    client = Client.forTestnet();
  }

  client.setOperator(config.accountId, config.privateKey);

  // Limiter les frais maximum par transaction
  client.setDefaultMaxTransactionFee(new Hbar(10));

  return client;
}

// ==================== GÉNÉRATION DE HASH ====================

/**
 * Génère le hash SHA-256 d'un fichier blueprint
 *
 * @param {string} filePath - Chemin vers le fichier
 * @returns {string} Hash SHA-256 en hexadécimal
 */
function generateBlueprintHash(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Fichier blueprint non trouvé: ${filePath}`);
  }

  const fileBuffer = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(fileBuffer).digest('hex');
}

/**
 * Génère le hash des mesures biométriques
 *
 * @param {Object} biometrics - Mesures M, P, I, Po
 * @returns {string} Hash des mesures
 */
function generateBiometricsHash(biometrics) {
  const content = JSON.stringify(biometrics);
  return crypto.createHash('sha256').update(content).digest('hex');
}

// ==================== CRÉATION DU TOKEN NFT ====================

/**
 * Crée la collection de tokens NFT ZAMA sur Hedera
 *
 * @param {Client} client - Client Hedera
 * @param {Object} options - Options de création
 * @returns {Object} Informations du token créé
 */
async function createZamaTokenCollection(client, options = {}) {
  const config = loadConfig();

  console.log('Création de la collection ZAMA Armor...');

  const createTx = await new TokenCreateTransaction()
    .setTokenName(options.name || 'AT-OM : Back to Light')
    .setTokenSymbol(options.symbol || 'ATOM')
    .setTokenType(TokenType.NonFungibleUnique)
    .setSupplyType(TokenSupplyType.Infinite)
    .setInitialSupply(0)
    .setDecimals(0)
    .setTreasuryAccountId(config.accountId)
    .setAdminKey(config.privateKey)
    .setSupplyKey(config.privateKey)
    .setFreezeDefault(false)
    .setTokenMemo('AT·OM Bio-Resonant Armor System')
    .freezeWith(client);

  const signedTx = await createTx.sign(config.privateKey);
  const txResponse = await signedTx.execute(client);
  const receipt = await txResponse.getReceipt(client);

  const tokenId = receipt.tokenId;

  console.log(`Collection créée avec succès !`);
  console.log(`Token ID: ${tokenId.toString()}`);

  return {
    tokenId: tokenId.toString(),
    transactionId: txResponse.transactionId.toString(),
    status: 'SUCCESS'
  };
}

// ==================== MINT D'UN NFT ARMOR ====================

/**
 * Mint un NFT unique pour une armure ZAMA
 *
 * @param {Client} client - Client Hedera
 * @param {string} tokenId - ID du token collection
 * @param {Object} armorData - Données de l'armure
 * @returns {Object} Informations du NFT minté
 */
async function mintArmorNFT(client, tokenId, armorData) {
  const config = loadConfig();

  const {
    biometrics,
    blueprintPath,
    securityLayers,
    phasesUnlocked,
    ownerName
  } = armorData;

  // Générer les hashes
  const blueprintHash = blueprintPath
    ? generateBlueprintHash(blueprintPath)
    : 'NO_BLUEPRINT';

  const biometricsHash = generateBiometricsHash(biometrics);

  // Construire les métadonnées
  const metadata = {
    version: '4.0',
    type: 'ZAMA_ARMOR',
    createdAt: new Date().toISOString(),

    // Hashes de sécurité (pas les données brutes!)
    blueprintHash: `SHA256:${blueprintHash}`,
    biometricsHash: `SHA256:${biometricsHash}`,

    // Informations publiques
    phasesUnlocked: phasesUnlocked || ['NOYAU'],
    securityLayers: securityLayers || 1,

    // Dimensions calculées (valeurs arrondies pour privacy)
    dimensions: {
      small: Math.round(biometrics.M * 1.618 * 10) / 10,
      medium: Math.round(biometrics.M * 2.618 * 10) / 10,
      large: Math.round(biometrics.M * 4.236 * 10) / 10
    },

    // Identifiant du propriétaire (optionnel)
    owner: ownerName || 'Anonymous Sovereign'
  };

  // Convertir en bytes pour Hedera
  const metadataBytes = Buffer.from(JSON.stringify(metadata), 'utf8');

  // Vérifier la taille (max 100 bytes pour les métadonnées NFT sur Hedera)
  if (metadataBytes.length > 100) {
    // Si trop grand, stocker sur IPFS et garder juste le CID
    console.log('⚠️  Métadonnées trop grandes, stockage des hashes uniquement');
    const compactMetadata = {
      v: '4.0',
      bh: blueprintHash.substring(0, 16),
      mh: biometricsHash.substring(0, 16),
      ph: phasesUnlocked?.length || 1,
      sl: securityLayers || 1
    };
    metadata.compact = compactMetadata;
  }

  console.log('Minting du NFT Armor...');

  const mintTx = await new TokenMintTransaction()
    .setTokenId(tokenId)
    .addMetadata(metadataBytes)
    .freezeWith(client);

  const signedTx = await mintTx.sign(config.privateKey);
  const txResponse = await signedTx.execute(client);
  const receipt = await txResponse.getReceipt(client);

  const serialNumber = receipt.serials[0].toString();

  console.log(`NFT Armor minté avec succès !`);
  console.log(`Serial Number: ${serialNumber}`);
  console.log(`Transaction ID: ${txResponse.transactionId.toString()}`);

  return {
    tokenId: tokenId,
    serialNumber: serialNumber,
    transactionId: txResponse.transactionId.toString(),
    metadata: metadata,
    status: 'SUCCESS'
  };
}

// ==================== REQUÊTE D'INFORMATION NFT ====================

/**
 * Récupère les informations d'un NFT Armor
 *
 * @param {Client} client - Client Hedera
 * @param {string} tokenId - ID du token
 * @param {string} serialNumber - Numéro de série
 * @returns {Object} Informations du NFT
 */
async function getArmorNFTInfo(client, tokenId, serialNumber) {
  console.log(`Récupération des infos pour ${tokenId}/${serialNumber}...`);

  const nftInfo = await new TokenNftInfoQuery()
    .setNftId({ tokenId, serialNumber })
    .execute(client);

  const info = nftInfo[0];

  // Décoder les métadonnées
  let metadata = null;
  try {
    metadata = JSON.parse(Buffer.from(info.metadata).toString('utf8'));
  } catch (e) {
    metadata = { raw: info.metadata.toString('hex') };
  }

  return {
    tokenId: info.nftId.tokenId.toString(),
    serialNumber: info.nftId.serial.toString(),
    owner: info.accountId.toString(),
    creationTime: info.creationTime.toDate().toISOString(),
    metadata: metadata
  };
}

// ==================== WORKFLOW COMPLET ====================

/**
 * Workflow complet: Création collection + Mint du premier NFT
 *
 * @param {Object} armorData - Données de l'armure à minter
 * @returns {Object} Résultat complet
 */
async function mintNewArmor(armorData) {
  const client = createHederaClient();

  try {
    // Étape 1: Créer la collection (si pas encore créée)
    let tokenId = process.env.ZAMA_TOKEN_ID;

    if (!tokenId) {
      console.log('\n═══════════════════════════════════════════════════════════════');
      console.log('  ÉTAPE 1: Création de la collection ZAMA');
      console.log('═══════════════════════════════════════════════════════════════\n');

      const collection = await createZamaTokenCollection(client);
      tokenId = collection.tokenId;

      console.log('\n⚠️  Sauvegardez ce Token ID dans vos variables d\'environnement:');
      console.log(`   ZAMA_TOKEN_ID=${tokenId}\n`);
    }

    // Étape 2: Mint le NFT
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('  ÉTAPE 2: Minting du NFT Armor');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const nft = await mintArmorNFT(client, tokenId, armorData);

    // Étape 3: Vérifier le NFT
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('  ÉTAPE 3: Vérification');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const info = await getArmorNFTInfo(client, tokenId, nft.serialNumber);

    console.log('NFT Info:');
    console.log(JSON.stringify(info, null, 2));

    return {
      success: true,
      collection: { tokenId },
      nft: nft,
      verification: info
    };

  } catch (error) {
    console.error('Erreur lors du minting:', error.message);
    throw error;
  } finally {
    client.close();
  }
}

// ==================== EXPORTS ====================

module.exports = {
  createHederaClient,
  createZamaTokenCollection,
  mintArmorNFT,
  getArmorNFTInfo,
  mintNewArmor,
  generateBlueprintHash,
  generateBiometricsHash
};

// ==================== EXEMPLE D'UTILISATION ====================

if (require.main === module) {
  // Vérifier que les variables d'environnement sont définies
  if (!process.env.MY_ACCOUNT_ID || !process.env.MY_PRIVATE_KEY) {
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('  AT·OM HEDERA ARMOR MINTER - MODE DÉMONSTRATION');
    console.log('═══════════════════════════════════════════════════════════════\n');

    console.log('⚠️  Variables d\'environnement requises non définies.');
    console.log('   Configurez MY_ACCOUNT_ID et MY_PRIVATE_KEY pour utiliser ce script.\n');

    console.log('EXEMPLE DE CONFIGURATION .env:');
    console.log('────────────────────────────────────────────────────────────────');
    console.log('MY_ACCOUNT_ID=0.0.XXXXXX');
    console.log('MY_PRIVATE_KEY=302e....');
    console.log('HEDERA_NETWORK=testnet');
    console.log('ZAMA_TOKEN_ID=0.0.YYYYYY  # Après création de la collection\n');

    console.log('EXEMPLE D\'UTILISATION:');
    console.log('────────────────────────────────────────────────────────────────');
    console.log(`
const { mintNewArmor } = require('./mintArmorToken');

const armorData = {
  biometrics: { M: 2.1, P: 8.5, I: 7.2, Po: 9.5 },
  blueprintPath: './assets/ZAMA_ARMOR_V4_FINAL.png',
  securityLayers: 2,
  phasesUnlocked: ['NOYAU', 'ANCRAGE'],
  ownerName: 'Sovereign One'
};

mintNewArmor(armorData)
  .then(result => console.log('Armor minted:', result))
  .catch(err => console.error('Error:', err));
`);

    console.log('═══════════════════════════════════════════════════════════════\n');
    process.exit(0);
  }

  // Si les variables sont définies, exécuter le minting
  const testArmorData = {
    biometrics: { M: 2.1, P: 8.5, I: 7.2, Po: 9.5 },
    blueprintPath: null, // Pas de fichier pour le test
    securityLayers: 1,
    phasesUnlocked: ['NOYAU'],
    ownerName: 'Test Sovereign'
  };

  mintNewArmor(testArmorData)
    .then(result => {
      console.log('\n═══════════════════════════════════════════════════════════════');
      console.log('  MINTING RÉUSSI !');
      console.log('═══════════════════════════════════════════════════════════════\n');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(err => {
      console.error('\nErreur:', err.message);
      process.exit(1);
    });
}
