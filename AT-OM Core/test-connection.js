require('dotenv').config();
const { Client, AccountBalanceQuery } = require("@hashgraph/sdk");

async function main() {
    // 1. Récupération des infos du fichier .env
    const myAccountId = process.env.MY_ACCOUNT_ID;
    const myPrivateKey = process.env.MY_PRIVATE_KEY;

    // Vérification de sécurité
    if (myAccountId == null || myPrivateKey == null) {
        throw new Error("ERREUR : Les clés sont absentes du fichier .env !");
    }

    // 2. Création de la connexion au réseau Hedera
    const client = Client.forMainnet(); // Utilise .forTestnet() si tu n'as pas encore de vrais HBAR
    client.setOperator(myAccountId, myPrivateKey);

    try {
        // 3. Demande au réseau le solde du compte
        const balance = await new AccountBalanceQuery()
            .setAccountId(myAccountId)
            .execute(client);

        console.log("-----------------------------------------");
        console.log("✅ CONNEXION RÉUSSIE !");
        console.log(`Le compte ${myAccountId} est actif.`);
        console.log(`Solde : ${balance.hbars.toString()}`);
        console.log("-----------------------------------------");
    } catch (error) {
        console.error("❌ ÉCHEC DE LA CONNEXION :", error.message);
    }
}

main();