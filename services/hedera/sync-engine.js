/**
 * AT·OM Sync Engine
 * =================
 * Bridge between Hedera Hashgraph and Supabase
 *
 * Purpose:
 * - Verify NFT ownership on Hedera
 * - Update is_sovereign status in Supabase profiles
 * - Sync $ATOM token balances
 *
 * @author AT·OM Team
 * @version 1.0.0
 */

// Load .env from multiple possible locations
const path = require('path');
const fs = require('fs');

// Try different paths for .env
const possiblePaths = [
  path.resolve(__dirname, '../../.env'),      // From services/hedera/
  path.resolve(process.cwd(), '.env'),         // From current working directory
  path.resolve(__dirname, '.env')              // Local .env
];

let envLoaded = false;
for (const envPath of possiblePaths) {
  if (fs.existsSync(envPath)) {
    require('dotenv').config({ path: envPath });
    console.log(`✅ Loaded .env from: ${envPath}`);
    envLoaded = true;
    break;
  }
}

if (!envLoaded) {
  console.warn('⚠️ No .env file found, using environment variables');
  require('dotenv').config(); // Try default
}

const { Client, AccountId, PrivateKey, TokenNftInfoQuery, TokenId, NftId } = require('@hashgraph/sdk');
const { createClient } = require('@supabase/supabase-js');

// ===========================================
// CONFIGURATION
// ===========================================

const config = {
  hedera: {
    accountId: process.env.HEDERA_ACCOUNT_ID,
    privateKey: process.env.HEDERA_PRIVATE_KEY,
    network: process.env.HEDERA_NETWORK || 'testnet',
    tokenId: process.env.HEDERA_TOKEN_ID,
    nftCollectionId: process.env.NFT_COLLECTION_ID
  },
  supabase: {
    url: process.env.SUPABASE_URL,
    serviceRoleKey: process.env.SUPABASE_SERVICE_ROLE_KEY
  }
};

// Validate required environment variables
function validateConfig() {
  const required = [
    'HEDERA_ACCOUNT_ID',
    'HEDERA_PRIVATE_KEY',
    'NFT_COLLECTION_ID',
    'SUPABASE_URL',
    'SUPABASE_SERVICE_ROLE_KEY'
  ];

  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:', missing.join(', '));
    process.exit(1);
  }

  console.log('✅ Configuration validated');
}

// ===========================================
// HEDERA CLIENT
// ===========================================

function initHederaClient() {
  try {
    const client = config.hedera.network === 'mainnet'
      ? Client.forMainnet()
      : Client.forTestnet();

    client.setOperator(
      AccountId.fromString(config.hedera.accountId),
      PrivateKey.fromStringED25519(config.hedera.privateKey)
    );

    console.log(`✅ Hedera client initialized (${config.hedera.network})`);
    console.log(`   Account: ${config.hedera.accountId}`);

    return client;
  } catch (error) {
    console.error('❌ Failed to initialize Hedera client:', error.message);
    throw error;
  }
}

// ===========================================
// SUPABASE CLIENT
// ===========================================

function initSupabaseClient() {
  try {
    const supabase = createClient(
      config.supabase.url,
      config.supabase.serviceRoleKey,
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false
        }
      }
    );

    console.log('✅ Supabase client initialized');
    return supabase;
  } catch (error) {
    console.error('❌ Failed to initialize Supabase client:', error.message);
    throw error;
  }
}

// ===========================================
// NFT OWNERSHIP VERIFICATION
// ===========================================

/**
 * Get the owner of a specific NFT serial number
 * @param {Client} client - Hedera client
 * @param {string} tokenId - NFT Collection Token ID
 * @param {number} serialNumber - NFT Serial Number
 * @returns {Promise<string|null>} - Owner account ID or null
 */
async function getNftOwner(client, tokenId, serialNumber) {
  try {
    const nftId = new NftId(TokenId.fromString(tokenId), serialNumber);

    const nftInfo = await new TokenNftInfoQuery()
      .setNftId(nftId)
      .execute(client);

    if (nftInfo && nftInfo.length > 0) {
      const ownerAccountId = nftInfo[0].accountId.toString();
      console.log(`   NFT #${serialNumber} owner: ${ownerAccountId}`);
      return ownerAccountId;
    }

    return null;
  } catch (error) {
    console.error(`❌ Error getting NFT #${serialNumber} owner:`, error.message);
    return null;
  }
}

/**
 * Get all NFT owners for a collection
 * @param {Client} client - Hedera client
 * @param {string} tokenId - NFT Collection Token ID
 * @param {number} maxSerial - Maximum serial number to check
 * @returns {Promise<Map<string, number[]>>} - Map of accountId to serial numbers
 */
async function getAllNftOwners(client, tokenId, maxSerial = 144) {
  const ownerMap = new Map();

  console.log(`\n📊 Scanning NFT collection ${tokenId} (serials 1-${maxSerial})...`);

  for (let serial = 1; serial <= maxSerial; serial++) {
    const owner = await getNftOwner(client, tokenId, serial);

    if (owner) {
      if (!ownerMap.has(owner)) {
        ownerMap.set(owner, []);
      }
      ownerMap.get(owner).push(serial);
    }

    // Rate limiting - Hedera allows ~100 requests per second
    if (serial % 10 === 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  console.log(`✅ Found ${ownerMap.size} unique NFT owners`);
  return ownerMap;
}

// ===========================================
// SUPABASE PROFILE SYNC
// ===========================================

/**
 * Update is_sovereign status for a user based on NFT ownership
 * @param {SupabaseClient} supabase - Supabase client
 * @param {string} hederaAccountId - Hedera account ID
 * @param {boolean} isSovereign - Sovereignty status
 * @param {number[]} nftSerials - Owned NFT serial numbers
 */
async function updateSovereignStatus(supabase, hederaAccountId, isSovereign, nftSerials = []) {
  try {
    // Find user by hedera_account_id in profiles
    const { data: profile, error: findError } = await supabase
      .from('profiles')
      .select('id, full_name, is_sovereign')
      .eq('hedera_account_id', hederaAccountId)
      .single();

    if (findError && findError.code !== 'PGRST116') {
      console.error(`   ❌ Error finding profile for ${hederaAccountId}:`, findError.message);
      return false;
    }

    if (!profile) {
      console.log(`   ⚠️ No profile found for Hedera account ${hederaAccountId}`);
      return false;
    }

    // Update sovereignty status
    const { error: updateError } = await supabase
      .from('profiles')
      .update({
        is_sovereign: isSovereign,
        sovereign_nft_serials: nftSerials,
        sovereign_verified_at: isSovereign ? new Date().toISOString() : null,
        updated_at: new Date().toISOString()
      })
      .eq('id', profile.id);

    if (updateError) {
      console.error(`   ❌ Error updating profile:`, updateError.message);
      return false;
    }

    const status = isSovereign ? '👑 SOVEREIGN' : '○ Standard';
    console.log(`   ${status}: ${profile.full_name || hederaAccountId} (NFTs: ${nftSerials.join(', ') || 'none'})`);
    return true;
  } catch (error) {
    console.error(`   ❌ Unexpected error:`, error.message);
    return false;
  }
}

/**
 * Sync all NFT owners with Supabase profiles
 * @param {SupabaseClient} supabase - Supabase client
 * @param {Map<string, number[]>} ownerMap - Map of accountId to serial numbers
 */
async function syncAllProfiles(supabase, ownerMap) {
  console.log('\n🔄 Syncing profiles with NFT ownership...');

  let updated = 0;
  let notFound = 0;

  // First, reset all is_sovereign to false
  const { error: resetError } = await supabase
    .from('profiles')
    .update({
      is_sovereign: false,
      sovereign_nft_serials: [],
      sovereign_verified_at: null
    })
    .neq('id', '00000000-0000-0000-0000-000000000000'); // Update all

  if (resetError) {
    console.error('❌ Error resetting sovereignty status:', resetError.message);
  }

  // Update owners
  for (const [accountId, serials] of ownerMap) {
    const success = await updateSovereignStatus(supabase, accountId, true, serials);
    if (success) updated++;
    else notFound++;
  }

  console.log(`\n📊 Sync complete:`);
  console.log(`   ✅ Updated: ${updated} profiles`);
  console.log(`   ⚠️ Not found: ${notFound} accounts`);
}

// ===========================================
// SPECIFIC SOVEREIGN CHECK (Serial #1)
// ===========================================

/**
 * Check who owns the Sovereign NFT (Serial #1) and update their status
 * This is the primary sovereignty verification
 */
async function verifySovereignNft(client, supabase) {
  console.log('\n👑 Verifying Sovereign NFT (Serial #1)...');

  const sovereignOwner = await getNftOwner(
    client,
    config.hedera.nftCollectionId,
    1  // Serial #1 = The Sovereign
  );

  if (!sovereignOwner) {
    console.log('⚠️ Sovereign NFT #1 has no owner or not found');
    return null;
  }

  console.log(`\n🎯 Sovereign NFT #1 owned by: ${sovereignOwner}`);

  // Update this user as THE Sovereign
  const success = await updateSovereignStatus(supabase, sovereignOwner, true, [1]);

  if (success) {
    console.log('✅ Sovereign status updated in Supabase');
  }

  return sovereignOwner;
}

// ===========================================
// EXPRESS API (Optional Health Endpoint)
// ===========================================

function startHealthServer(port = 3000) {
  const express = require('express');
  const app = express();

  let lastSync = null;
  let syncStatus = 'idle';

  app.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      service: 'AT·OM Sync Engine',
      version: '1.0.0',
      lastSync: lastSync,
      syncStatus: syncStatus,
      config: {
        network: config.hedera.network,
        nftCollection: config.hedera.nftCollectionId
      }
    });
  });

  app.get('/sync', async (req, res) => {
    if (syncStatus === 'running') {
      return res.status(429).json({ error: 'Sync already in progress' });
    }

    syncStatus = 'running';
    res.json({ message: 'Sync started', timestamp: new Date().toISOString() });

    try {
      await runSync();
      lastSync = new Date().toISOString();
      syncStatus = 'completed';
    } catch (error) {
      syncStatus = 'error';
    }
  });

  app.listen(port, () => {
    console.log(`\n🌐 Health server running on port ${port}`);
    console.log(`   GET /health - Check status`);
    console.log(`   GET /sync - Trigger manual sync`);
  });

  return { setLastSync: (date) => { lastSync = date; }, setSyncStatus: (status) => { syncStatus = status; } };
}

// ===========================================
// MAIN SYNC FUNCTION
// ===========================================

async function runSync() {
  console.log('\n========================================');
  console.log('   AT·OM SYNC ENGINE');
  console.log('   Hedera <-> Supabase Bridge');
  console.log('========================================\n');

  // Validate configuration
  validateConfig();

  // Initialize clients
  const hederaClient = initHederaClient();
  const supabaseClient = initSupabaseClient();

  // Option 1: Just verify Sovereign NFT #1
  console.log('\n--- SOVEREIGN VERIFICATION ---');
  await verifySovereignNft(hederaClient, supabaseClient);

  // Option 2: Full sync of all NFTs (uncomment if needed)
  // console.log('\n--- FULL NFT SYNC ---');
  // const ownerMap = await getAllNftOwners(hederaClient, config.hedera.nftCollectionId, 144);
  // await syncAllProfiles(supabaseClient, ownerMap);

  console.log('\n========================================');
  console.log('   SYNC COMPLETE');
  console.log('========================================\n');
}

// ===========================================
// ENTRY POINT
// ===========================================

// Run as standalone script
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.includes('--server')) {
    // Run with health server
    const server = startHealthServer(process.env.PORT || 3000);

    // Run initial sync
    runSync().then(() => {
      server.setLastSync(new Date().toISOString());
    });

    // Schedule periodic sync (every 4 hours)
    setInterval(async () => {
      console.log('\n⏰ Scheduled sync starting...');
      server.setSyncStatus('running');
      await runSync();
      server.setLastSync(new Date().toISOString());
      server.setSyncStatus('completed');
    }, 4 * 60 * 60 * 1000);

  } else {
    // Run once and exit
    runSync()
      .then(() => process.exit(0))
      .catch((error) => {
        console.error('Fatal error:', error);
        process.exit(1);
      });
  }
}

// Export for use as module
module.exports = {
  runSync,
  verifySovereignNft,
  getNftOwner,
  getAllNftOwners,
  updateSovereignStatus,
  syncAllProfiles
};
