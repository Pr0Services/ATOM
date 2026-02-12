/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — SAVE ZAMA NFT TO SUPABASE (Table: armors)
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });
const { createClient } = require('@supabase/supabase-js');

const ZAMA_NFT = {
    token_id: '0.0.7780104',  // AT-OM$ (remplace ZAMA 0.0.7730446 compromis)
    m_frequency: 44.4,
    p_ratio: 161.8,
    i_sequence: 369.0,
    po_stability: 1728.0,
    image_url: 'https://vzbrhovthpihrhdbbjud.supabase.co/storage/v1/object/public/zama-assets/placeholder-zama-armor.png',
    status: 'ACTIVE'
};

async function saveToSupabase() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('        AT·OM — ENREGISTREMENT ZAMA NFT DANS SUPABASE');
    console.log('═══════════════════════════════════════════════════════════════\n');

    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (!supabaseUrl || !supabaseKey) {
        console.log('❌ Configuration Supabase manquante');
        return { success: false };
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    console.log(`📡 Supabase: ${supabaseUrl}`);
    console.log(`📋 Token ID: ${ZAMA_NFT.token_id}`);
    console.log('');

    try {
        console.log('🔨 Insertion dans la table armors...');

        const { data, error } = await supabase
            .from('armors')
            .upsert({
                token_id: ZAMA_NFT.token_id,
                m_frequency: ZAMA_NFT.m_frequency,
                p_ratio: ZAMA_NFT.p_ratio,
                i_sequence: ZAMA_NFT.i_sequence,
                po_stability: ZAMA_NFT.po_stability,
                image_url: ZAMA_NFT.image_url,
                status: ZAMA_NFT.status
            }, { onConflict: 'token_id' })
            .select();

        if (error) throw error;

        console.log('');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              🟢 NFT ZAMA ENREGISTRÉ DANS SUPABASE');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   Token ID: ${ZAMA_NFT.token_id}`);
        console.log(`   M: ${ZAMA_NFT.m_frequency} | P: ${ZAMA_NFT.p_ratio}`);
        console.log(`   I: ${ZAMA_NFT.i_sequence} | Po: ${ZAMA_NFT.po_stability}`);
        console.log(`   Table: armors`);
        console.log('═══════════════════════════════════════════════════════════════\n');

        return { success: true, data };

    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return { success: false, error: error.message };
    }
}

saveToSupabase();
