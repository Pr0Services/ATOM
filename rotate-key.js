/**
 * AT·OM — Hedera Key Rotation Script
 * ═══════════════════════════════════════════════════════════════════════════
 * ⚠️ SECURITY: Never hardcode private keys in source code
 * ⚠️ 2026-02-05: Old key purged — account 0.0.7702951 was COMPROMISED
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * Usage:
 *   1. Set your HEDERA_ACCOUNT_ID and HEDERA_PRIVATE_KEY in .env
 *   2. Run: node rotate-key.js
 *   3. SAVE the new private key somewhere VERY safe
 */

require('dotenv').config({ path: '../.env' });
const { Client, PrivateKey, AccountUpdateTransaction } = require('@hashgraph/sdk');

async function rotateKey() {
    const accountId = process.env.HEDERA_ACCOUNT_ID;
    const currentKeyHex = process.env.HEDERA_PRIVATE_KEY;

    if (!accountId || !currentKeyHex || currentKeyHex === 'YOUR_PRIVATE_KEY_HERE') {
        console.log('⚠️  Configure HEDERA_ACCOUNT_ID and HEDERA_PRIVATE_KEY in .env first');
        process.exit(1);
    }

    const client = Client.forTestnet();
    const currentPrivateKey = PrivateKey.fromStringED25519(currentKeyHex);
    client.setOperator(accountId, currentPrivateKey);

    const newPrivateKey = await PrivateKey.generateED25519Async();
    const newPublicKey = newPrivateKey.publicKey;

    console.log('🔑 Rotating key for account:', accountId);
    console.log('🔑 New Public Key:', newPublicKey.toString());

    const tx = await new AccountUpdateTransaction()
        .setAccountId(accountId)
        .setKey(newPublicKey)
        .freezeWith(client)
        .sign(currentPrivateKey);

    const res = await tx.execute(client);
    await res.getReceipt(client);

    console.log('');
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('  🟢 KEY ROTATED SUCCESSFULLY');
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('  ⚠️ SAVE THIS NEW PRIVATE KEY IMMEDIATELY:');
    console.log(`  ${newPrivateKey.toString()}`);
    console.log('  ⚠️ Update your .env with this new key');
    console.log('═══════════════════════════════════════════════════════════════');

    client.close();
}

rotateKey().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
});
