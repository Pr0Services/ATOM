/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — SUPABASE CLIENT
 * ═══════════════════════════════════════════════════════════════════════════
 * Client Supabase centralisé pour toutes les opérations database
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });
const { createClient } = require('@supabase/supabase-js');

// Configuration
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

// Validation
function validateConfig() {
    const errors = [];

    if (!supabaseUrl || supabaseUrl === 'YOUR_SUPABASE_URL') {
        errors.push('SUPABASE_URL manquant');
    }
    if (!supabaseAnonKey || supabaseAnonKey === 'YOUR_ANON_KEY') {
        errors.push('SUPABASE_ANON_KEY manquant');
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

// Client public (pour le frontend)
const supabase = supabaseUrl && supabaseAnonKey
    ? createClient(supabaseUrl, supabaseAnonKey)
    : null;

// Client admin (pour les opérations serveur - utiliser avec précaution)
const supabaseAdmin = supabaseUrl && supabaseServiceKey
    ? createClient(supabaseUrl, supabaseServiceKey, {
        auth: {
            autoRefreshToken: false,
            persistSession: false
        }
    })
    : null;

/**
 * Test de connexion Supabase
 */
async function testConnection() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('          AT·OM — TEST CONNEXION SUPABASE');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const validation = validateConfig();
    if (!validation.valid) {
        console.log('❌ Configuration invalide:');
        validation.errors.forEach(e => console.log(`   - ${e}`));
        return { success: false, errors: validation.errors };
    }

    console.log('📡 Configuration:');
    console.log(`   URL: ${supabaseUrl}`);
    console.log(`   Anon Key: ${supabaseAnonKey?.substring(0, 20)}...`);
    console.log('');

    try {
        // Test simple query
        console.log('🔌 Test de connexion...');
        const { data, error } = await supabase
            .from('user_biometrics')
            .select('count')
            .limit(1);

        if (error && error.code !== 'PGRST116') { // PGRST116 = table doesn't exist yet
            if (error.code === '42P01') {
                console.log('⚠️  Table user_biometrics non créée (normal pour première config)');
            } else {
                throw error;
            }
        }

        console.log('✅ Connexion Supabase réussie\n');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('                    🟢 SUPABASE OPÉRATIONNEL');
        console.log('═══════════════════════════════════════════════════════════════\n');

        return { success: true, status: 'OPERATIONAL' };

    } catch (error) {
        console.log(`❌ Erreur connexion: ${error.message}`);
        return { success: false, error: error.message };
    }
}

module.exports = {
    supabase,
    supabaseAdmin,
    validateConfig,
    testConnection
};

// Run if executed directly
if (require.main === module) {
    testConnection();
}
