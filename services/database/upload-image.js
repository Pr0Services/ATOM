/**
 * ═══════════════════════════════════════════════════════════════════════════
 * AT·OM — UPLOAD IMAGE TO SUPABASE STORAGE
 * ═══════════════════════════════════════════════════════════════════════════
 * Script pour uploader l'image ZAMA sur Supabase Storage
 * Usage: node upload-image.js <chemin_image>
 * ═══════════════════════════════════════════════════════════════════════════
 */

require('dotenv').config({ path: '../../.env' });
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Configuration
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const BUCKET_NAME = 'zama-assets';

async function uploadImage(imagePath) {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('        AT·OM — UPLOAD IMAGE SUPABASE');
    console.log('═══════════════════════════════════════════════════════════════\n');

    // Validation
    if (!supabaseUrl || supabaseUrl === 'YOUR_SUPABASE_URL') {
        console.log('❌ SUPABASE_URL non configuré dans .env');
        return { success: false, error: 'SUPABASE_URL missing' };
    }

    if (!supabaseServiceKey || supabaseServiceKey === 'YOUR_SERVICE_ROLE_KEY') {
        console.log('❌ SUPABASE_SERVICE_ROLE_KEY non configuré dans .env');
        return { success: false, error: 'SUPABASE_SERVICE_ROLE_KEY missing' };
    }

    if (!imagePath) {
        console.log('❌ Chemin de l\'image requis');
        console.log('   Usage: node upload-image.js <chemin_image>');
        return { success: false, error: 'image path missing' };
    }

    if (!fs.existsSync(imagePath)) {
        console.log(`❌ Fichier non trouvé: ${imagePath}`);
        return { success: false, error: 'file not found' };
    }

    console.log(`📁 Image: ${imagePath}`);
    console.log(`📡 Supabase: ${supabaseUrl}`);
    console.log('');

    // Initialize Supabase client
    const supabase = createClient(supabaseUrl, supabaseServiceKey, {
        auth: {
            autoRefreshToken: false,
            persistSession: false
        }
    });

    try {
        // Read file
        const fileBuffer = fs.readFileSync(imagePath);
        const fileName = `zama-armor-${Date.now()}${path.extname(imagePath)}`;
        const contentType = imagePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

        console.log('📤 Upload en cours...');

        // Check if bucket exists, create if not
        const { data: buckets } = await supabase.storage.listBuckets();
        const bucketExists = buckets?.some(b => b.name === BUCKET_NAME);

        if (!bucketExists) {
            console.log(`📦 Création du bucket "${BUCKET_NAME}"...`);
            const { error: createError } = await supabase.storage.createBucket(BUCKET_NAME, {
                public: true,
                fileSizeLimit: 10485760 // 10MB
            });

            if (createError) {
                console.log(`⚠️  Bucket existe peut-être déjà: ${createError.message}`);
            }
        }

        // Upload file
        const { data, error } = await supabase.storage
            .from(BUCKET_NAME)
            .upload(fileName, fileBuffer, {
                contentType: contentType,
                upsert: true
            });

        if (error) {
            throw error;
        }

        // Get public URL
        const { data: urlData } = supabase.storage
            .from(BUCKET_NAME)
            .getPublicUrl(fileName);

        const publicUrl = urlData.publicUrl;

        console.log('');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('              🟢 IMAGE UPLOADÉE AVEC SUCCÈS');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`   URL: ${publicUrl}`);
        console.log('');
        console.log('📋 Copie cette URL dans metadata.json (champ "image")');
        console.log('═══════════════════════════════════════════════════════════════\n');

        return {
            success: true,
            url: publicUrl,
            fileName: fileName
        };

    } catch (error) {
        console.log(`❌ Erreur upload: ${error.message}`);
        return { success: false, error: error.message };
    }
}

// Run if executed directly
if (require.main === module) {
    const imagePath = process.argv[2];
    uploadImage(imagePath);
}

module.exports = { uploadImage };
