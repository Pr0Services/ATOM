/**
 * AT·OM Vision Engine - Body Scanner v1.0
 * Extraction des mesures biométriques à partir d'une photo avec échelle de référence
 *
 * Ce service utilise la détection d'objets de référence (carte de crédit standard)
 * pour établir un ratio pixel/cm précis et extraire les mesures corporelles.
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

// Dimensions standard des objets de référence (en cm)
const REFERENCE_OBJECTS = {
  CREDIT_CARD: {
    width: 8.56,
    height: 5.398,
    name: 'Carte de crédit/bancaire'
  },
  ID_CARD: {
    width: 8.56,
    height: 5.398,
    name: 'Carte d\'identité'
  },
  BUSINESS_CARD: {
    width: 8.5,
    height: 5.5,
    name: 'Carte de visite standard'
  },
  A4_PAPER: {
    width: 21.0,
    height: 29.7,
    name: 'Feuille A4'
  }
};

// Points anatomiques pour la détection
const BODY_LANDMARKS = {
  THUMB_JOINT: 'thumb_mcp',        // Jointure du pouce (pour M)
  PALM_WIDTH: 'palm_width',         // Largeur de la paume (pour P)
  INDEX_TIP: 'index_tip',           // Bout de l'index
  INDEX_BASE: 'index_mcp',          // Base de l'index
  FIST_WIDTH: 'fist_width'          // Largeur du poing fermé
};

/**
 * Classe principale du scanner corporel
 */
class BodyScanner {
  constructor(options = {}) {
    this.referenceObject = options.referenceObject || REFERENCE_OBJECTS.CREDIT_CARD;
    this.pixelsPerCm = null;
    this.calibrated = false;
    this.lastAnalysis = null;
  }

  /**
   * Calibre le scanner avec l'objet de référence détecté
   *
   * @param {Object} referenceDetection - Résultat de la détection de l'objet de référence
   * @param {number} referenceDetection.widthPixels - Largeur en pixels de l'objet détecté
   * @returns {Object} Informations de calibration
   */
  calibrate(referenceDetection) {
    if (!referenceDetection || !referenceDetection.widthPixels) {
      throw new Error('Détection de l\'objet de référence invalide');
    }

    const { widthPixels } = referenceDetection;
    const { width: widthCm } = this.referenceObject;

    this.pixelsPerCm = widthPixels / widthCm;
    this.calibrated = true;

    return {
      calibrated: true,
      pixelsPerCm: this.pixelsPerCm,
      referenceObject: this.referenceObject.name,
      accuracy: this._estimateAccuracy(widthPixels)
    };
  }

  /**
   * Estime la précision de la calibration
   *
   * @param {number} pixelWidth - Largeur en pixels
   * @returns {string} Niveau de précision
   */
  _estimateAccuracy(pixelWidth) {
    if (pixelWidth >= 500) return 'Excellente (±0.5mm)';
    if (pixelWidth >= 300) return 'Bonne (±1mm)';
    if (pixelWidth >= 150) return 'Acceptable (±2mm)';
    return 'Faible - rapprochez l\'objet de référence';
  }

  /**
   * Convertit une distance en pixels vers des centimètres
   *
   * @param {number} pixels - Distance en pixels
   * @returns {number} Distance en centimètres
   */
  pixelsToCm(pixels) {
    if (!this.calibrated) {
      throw new Error('Scanner non calibré. Appelez calibrate() d\'abord.');
    }
    return pixels / this.pixelsPerCm;
  }

  /**
   * Extrait les mesures biométriques à partir des points détectés
   *
   * @param {Object} analysisResult - Résultat de l'analyse d'image
   * @param {number} analysisResult.thumbPixels - Largeur du pouce en pixels
   * @param {number} analysisResult.palmPixels - Largeur de la paume en pixels
   * @param {number} analysisResult.indexPixels - Longueur de l'index en pixels
   * @param {number} analysisResult.fistPixels - Largeur du poing en pixels
   * @returns {Object} Mesures biométriques en centimètres
   */
  extractMeasures(analysisResult) {
    if (!this.calibrated) {
      throw new Error('Scanner non calibré. Appelez calibrate() d\'abord.');
    }

    const {
      thumbPixels,
      palmPixels,
      indexPixels,
      fistPixels,
      referenceObjectPixels
    } = analysisResult;

    // Re-calibrer si un nouvel objet de référence est fourni
    if (referenceObjectPixels) {
      this.calibrate({ widthPixels: referenceObjectPixels });
    }

    const measures = {
      M: this._safeConvert(thumbPixels, 'Module (M)'),
      P: this._safeConvert(palmPixels, 'Paume (P)'),
      I: this._safeConvert(indexPixels, 'Index (I)'),
      Po: this._safeConvert(fistPixels, 'Poing (Po)')
    };

    this.lastAnalysis = {
      measures,
      extractedAt: new Date().toISOString(),
      calibration: {
        pixelsPerCm: this.pixelsPerCm,
        referenceObject: this.referenceObject.name
      },
      validated: false // Requiert Human-in-the-Loop
    };

    return this.lastAnalysis;
  }

  /**
   * Conversion sécurisée avec gestion des valeurs manquantes
   *
   * @param {number} pixels - Valeur en pixels
   * @param {string} measureName - Nom de la mesure pour les logs
   * @returns {number|null} Valeur en cm ou null
   */
  _safeConvert(pixels, measureName) {
    if (pixels === undefined || pixels === null || pixels <= 0) {
      console.warn(`Mesure manquante ou invalide: ${measureName}`);
      return null;
    }
    return parseFloat(this.pixelsToCm(pixels).toFixed(2));
  }

  /**
   * Valide les mesures extraites pour cohérence
   *
   * @param {Object} measures - Mesures extraites
   * @returns {Object} Résultat de validation
   */
  validateMeasures(measures) {
    const { M, P, I, Po } = measures;
    const issues = [];
    const suggestions = [];

    // Vérifier les valeurs nulles
    if (!M) issues.push('Module du pouce (M) non détecté');
    if (!P) issues.push('Largeur de paume (P) non détectée');
    if (!I) issues.push('Longueur d\'index (I) non détectée');
    if (!Po) issues.push('Largeur du poing (Po) non détectée');

    // Vérifier les proportions anatomiques
    if (M && P && M > P) {
      issues.push('Le pouce semble plus large que la paume - vérifiez l\'alignement');
    }

    if (P && Po && Po < P * 0.9) {
      suggestions.push('Le poing semble étroit - assurez-vous qu\'il est bien fermé');
    }

    if (M && I && I < M * 2.5) {
      suggestions.push('L\'index semble court - vérifiez que le doigt est bien étendu');
    }

    // Plages de valeurs typiques (adulte)
    if (M && (M < 1.5 || M > 3.5)) {
      suggestions.push(`Module ${M}cm hors plage typique (1.5-3.5cm)`);
    }

    if (P && (P < 6 || P > 12)) {
      suggestions.push(`Paume ${P}cm hors plage typique (6-12cm)`);
    }

    return {
      valid: issues.length === 0,
      issues,
      suggestions,
      confidence: this._calculateConfidence(measures, issues)
    };
  }

  /**
   * Calcule un score de confiance pour les mesures
   *
   * @param {Object} measures - Mesures extraites
   * @param {Array} issues - Problèmes détectés
   * @returns {number} Score de confiance (0-100)
   */
  _calculateConfidence(measures, issues) {
    let score = 100;

    // Pénalité pour chaque mesure manquante
    const measureCount = Object.values(measures).filter(v => v !== null).length;
    score -= (4 - measureCount) * 20;

    // Pénalité pour chaque problème
    score -= issues.length * 10;

    // Bonus pour calibration haute résolution
    if (this.pixelsPerCm > 50) score += 5;

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Génère un guide visuel pour l'utilisateur
   *
   * @param {string} step - Étape actuelle
   * @returns {Object} Instructions pour l'affichage
   */
  getVisualGuide(step) {
    const guides = {
      reference: {
        title: 'Étape 1: Calibration',
        instruction: 'Placez une carte de crédit à plat, visible dans le cadre',
        highlight: 'reference_zone',
        tips: [
          'La carte doit être à plat et non inclinée',
          'Assurez-vous que la largeur complète est visible',
          'Évitez les ombres sur la carte'
        ]
      },
      hand_open: {
        title: 'Étape 2: Main ouverte',
        instruction: 'Placez votre main à plat, doigts écartés',
        highlight: 'hand_zone',
        tips: [
          'La main doit être à la même distance que la carte de référence',
          'Gardez les doigts bien écartés',
          'Le pouce doit être visible de profil'
        ]
      },
      fist: {
        title: 'Étape 3: Poing fermé',
        instruction: 'Fermez le poing, pouce visible sur le côté',
        highlight: 'fist_zone',
        tips: [
          'Serrez bien le poing',
          'La largeur du poing doit être visible',
          'Gardez la même distance que les photos précédentes'
        ]
      },
      validation: {
        title: 'Étape 4: Validation',
        instruction: 'Vérifiez les mesures affichées et confirmez',
        highlight: 'measures_overlay',
        tips: [
          'Les lignes de mesure doivent correspondre à vos doigts/paume',
          'Vous pouvez reprendre une photo si nécessaire',
          'Cette étape scelle vos mesures pour l\'armure'
        ]
      }
    };

    return guides[step] || guides.reference;
  }

  /**
   * Prépare les données pour l'affichage RA avec overlay de mesures
   *
   * @param {Object} measures - Mesures validées
   * @returns {Object} Données pour l'overlay RA
   */
  prepareRAOverlay(measures) {
    const { M, P, I, Po } = measures;

    return {
      overlays: [
        {
          type: 'measurement_line',
          label: `M: ${M}cm`,
          position: 'thumb',
          color: '#FFD700' // Or
        },
        {
          type: 'measurement_line',
          label: `P: ${P}cm`,
          position: 'palm',
          color: '#C0C0C0' // Argent
        },
        {
          type: 'measurement_line',
          label: `I: ${I}cm`,
          position: 'index',
          color: '#87CEEB' // Bleu ciel
        },
        {
          type: 'measurement_line',
          label: `Po: ${Po}cm`,
          position: 'fist',
          color: '#9370DB' // Violet
        }
      ],
      validation_button: {
        label: 'Valider la Bio-Résonance',
        action: 'seal_measures',
        enabled: Object.values(measures).every(v => v !== null)
      }
    };
  }
}

/**
 * Simule l'analyse d'image (à remplacer par MediaPipe ou autre)
 * Cette fonction sert de placeholder pour l'intégration future
 *
 * @param {Object} imageData - Données de l'image
 * @returns {Object} Résultat simulé de l'analyse
 */
function simulateImageAnalysis(imageData) {
  // En production, cette fonction utiliserait MediaPipe ou TensorFlow.js
  // Pour l'instant, retourne des valeurs simulées pour les tests

  console.log('⚠️  Mode simulation - Intégrer MediaPipe pour la production');

  return {
    referenceObjectPixels: 428, // Carte de crédit à ~50px/cm
    thumbPixels: 105,           // ~2.1cm
    palmPixels: 425,            // ~8.5cm
    indexPixels: 360,           // ~7.2cm
    fistPixels: 475,            // ~9.5cm
    landmarks: {
      detected: true,
      confidence: 0.92
    }
  };
}

// ==================== EXPORTS ====================

module.exports = {
  BodyScanner,
  REFERENCE_OBJECTS,
  BODY_LANDMARKS,
  simulateImageAnalysis
};

// ==================== EXEMPLE D'UTILISATION ====================

if (require.main === module) {
  console.log('\n═══════════════════════════════════════════════════════════════');
  console.log('           AT·OM VISION ENGINE - BODY SCANNER                   ');
  console.log('═══════════════════════════════════════════════════════════════\n');

  // Créer le scanner
  const scanner = new BodyScanner({
    referenceObject: REFERENCE_OBJECTS.CREDIT_CARD
  });

  // Simuler une analyse d'image
  const analysisResult = simulateImageAnalysis({});

  // Calibrer avec l'objet de référence
  const calibration = scanner.calibrate({
    widthPixels: analysisResult.referenceObjectPixels
  });

  console.log('CALIBRATION:');
  console.log(`  Objet de référence: ${calibration.referenceObject}`);
  console.log(`  Pixels/cm: ${calibration.pixelsPerCm.toFixed(2)}`);
  console.log(`  Précision: ${calibration.accuracy}`);

  // Extraire les mesures
  const extraction = scanner.extractMeasures(analysisResult);

  console.log('\nMESURES EXTRAITES:');
  console.log(`  Module (M):  ${extraction.measures.M} cm`);
  console.log(`  Paume (P):   ${extraction.measures.P} cm`);
  console.log(`  Index (I):   ${extraction.measures.I} cm`);
  console.log(`  Poing (Po):  ${extraction.measures.Po} cm`);

  // Valider les mesures
  const validation = scanner.validateMeasures(extraction.measures);

  console.log('\nVALIDATION:');
  console.log(`  Valide: ${validation.valid ? 'OUI' : 'NON'}`);
  console.log(`  Confiance: ${validation.confidence}%`);

  if (validation.suggestions.length > 0) {
    console.log('\n  Suggestions:');
    validation.suggestions.forEach(s => console.log(`    - ${s}`));
  }

  console.log('\n═══════════════════════════════════════════════════════════════\n');
}
