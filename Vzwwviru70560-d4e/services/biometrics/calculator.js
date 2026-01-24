/**
 * AT·OM Biometric Engine v1.0
 * Calcule les dimensions sacrées basées sur le Nombre d'Or (Phi)
 *
 * Ce moteur transforme les mesures corporelles en dimensions harmoniques
 * pour l'armure bio-résonante ZAMA.
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

// Le Nombre d'Or - ratio universel de la création
const PHI = 1.61803398875;

// Puissances de Phi pré-calculées pour performance
const PHI_SQUARED = Math.pow(PHI, 2);  // ≈ 2.618
const PHI_CUBED = Math.pow(PHI, 3);    // ≈ 4.236

/**
 * Catégories de symboles selon le Cahier des Charges ZAMA
 */
const SYMBOL_CATEGORIES = {
  SMALL: 'small',       // Sceaux, symboles de protection
  MEDIUM: 'medium',     // Triskel, Œil d'Horus
  LARGE: 'large'        // Fleur de Vie, Cube de Métatron
};

/**
 * Phases d'activation de l'armure
 */
const PHASES = {
  NOYAU: 1,     // Cube de Métatron, Fleur de Vie
  ANCRAGE: 2,   // Triskels, Sceaux de Protection
  SENSEURS: 3   // Œil d'Horus
};

/**
 * Calcule toutes les dimensions de l'armure basées sur les mesures biométriques
 *
 * @param {Object} userMeasures - Mesures de l'utilisateur en centimètres
 * @param {number} userMeasures.M - Largeur du pouce à la jointure (Module de base)
 * @param {number} userMeasures.P - Largeur de la paume sans le pouce
 * @param {number} userMeasures.I - Longueur de l'index
 * @param {number} userMeasures.Po - Largeur du poing fermé
 * @returns {Object} Dimensions calculées pour tous les symboles
 */
function calculateArmorDimensions(userMeasures) {
  const { M, P, I, Po } = userMeasures;

  // Validation des entrées
  if (!M || !P || !I || !Po) {
    throw new Error('Toutes les mesures biométriques sont requises (M, P, I, Po)');
  }

  if (M <= 0 || P <= 0 || I <= 0 || Po <= 0) {
    throw new Error('Les mesures doivent être des valeurs positives');
  }

  return {
    // Dimensions selon les catégories de symboles
    dimensions: {
      small: parseFloat((M * PHI).toFixed(2)),           // Sceaux Infini, Protection
      medium: parseFloat((M * PHI_SQUARED).toFixed(2)),  // Triskel, Œil d'Horus
      large: parseFloat((M * PHI_CUBED).toFixed(2))      // Fleur de Vie, Métatron
    },

    // Calibrations anatomiques spécifiques
    anatomical: {
      fleurDeVie: parseFloat(Po.toFixed(2)),    // Calibrée sur le poing fermé
      cubeMetatron: parseFloat((M * PHI_CUBED).toFixed(2)),
      eyeOfHorus: parseFloat(I.toFixed(2)),     // Calibrée sur l'index
      triskel: parseFloat((M * 3).toFixed(2)),  // 3x la largeur du pouce
      sceauProtection: parseFloat((M * PHI).toFixed(2))
    },

    // Métadonnées pour Hedera
    metadata: {
      baseModule: M,
      palmWidth: P,
      indexLength: I,
      fistWidth: Po,
      phiRatio: PHI,
      calculatedAt: new Date().toISOString()
    },

    // Ratios de validation
    ratios: {
      palmToModule: parseFloat((P / M).toFixed(3)),
      fistToModule: parseFloat((Po / M).toFixed(3)),
      indexToModule: parseFloat((I / M).toFixed(3))
    }
  };
}

/**
 * Calcule les dimensions pour un symbole spécifique
 *
 * @param {string} symbolName - Nom du symbole
 * @param {Object} userMeasures - Mesures biométriques
 * @returns {Object} Dimension et métadonnées du symbole
 */
function calculateSymbolDimension(symbolName, userMeasures) {
  const { M, I, Po } = userMeasures;

  const symbolMap = {
    'cube_metatron': {
      dimension: M * PHI_CUBED,
      phase: PHASES.NOYAU,
      category: SYMBOL_CATEGORIES.LARGE,
      location: 'Centre du torse (plexus solaire/cœur)'
    },
    'fleur_de_vie': {
      dimension: Po,
      phase: PHASES.NOYAU,
      category: SYMBOL_CATEGORIES.LARGE,
      location: 'Sternum (cœur)'
    },
    'triskel': {
      dimension: M * 3,
      phase: PHASES.ANCRAGE,
      category: SYMBOL_CATEGORIES.MEDIUM,
      location: 'Épaules, hanches, genoux'
    },
    'sceau_protection': {
      dimension: M * PHI,
      phase: PHASES.ANCRAGE,
      category: SYMBOL_CATEGORIES.SMALL,
      location: 'Sacrum, nuque, articulations'
    },
    'oeil_horus': {
      dimension: I,
      phase: PHASES.SENSEURS,
      category: SYMBOL_CATEGORIES.MEDIUM,
      location: 'Entre les sourcils / tempes',
      security: 'iris_required'
    }
  };

  const symbol = symbolMap[symbolName.toLowerCase()];

  if (!symbol) {
    throw new Error(`Symbole inconnu: ${symbolName}`);
  }

  return {
    name: symbolName,
    dimension: parseFloat(symbol.dimension.toFixed(2)),
    unit: 'cm',
    phase: symbol.phase,
    category: symbol.category,
    location: symbol.location,
    security: symbol.security || 'public'
  };
}

/**
 * Génère le blueprint complet de l'armure
 *
 * @param {Object} userMeasures - Mesures biométriques
 * @param {Object} options - Options de génération
 * @returns {Object} Blueprint technique complet
 */
function generateArmorBlueprint(userMeasures, options = {}) {
  const dimensions = calculateArmorDimensions(userMeasures);

  const symbols = [
    'cube_metatron',
    'fleur_de_vie',
    'triskel',
    'sceau_protection',
    'oeil_horus'
  ].map(name => calculateSymbolDimension(name, userMeasures));

  return {
    version: '4.0',
    type: 'ZAMA_ARMOR_BLUEPRINT',
    createdAt: new Date().toISOString(),
    validated: false, // Requiert Human-in-the-Loop

    biometrics: {
      input: userMeasures,
      ...dimensions
    },

    symbols: symbols,

    phases: {
      1: {
        name: 'NOYAU',
        symbols: symbols.filter(s => s.phase === 1),
        unlocked: true
      },
      2: {
        name: 'ANCRAGE',
        symbols: symbols.filter(s => s.phase === 2),
        unlocked: options.phase2Unlocked || false
      },
      3: {
        name: 'SENSEURS',
        symbols: symbols.filter(s => s.phase === 3),
        unlocked: options.phase3Unlocked || false,
        security: 'iris_required'
      }
    },

    security: {
      layer1_geometry: true,
      layer2_ocular: options.irisValidated || false,
      layer3_fingerprint: options.fingerprintValidated || false,
      layer4_bioresonance: options.bpmConnected || false
    }
  };
}

/**
 * Valide les proportions biométriques selon les ratios naturels
 *
 * @param {Object} userMeasures - Mesures à valider
 * @returns {Object} Résultat de validation avec avertissements
 */
function validateBiometricProportions(userMeasures) {
  const { M, P, I, Po } = userMeasures;
  const warnings = [];
  const errors = [];

  // Ratio paume/module devrait être proche de PHI²
  const palmRatio = P / M;
  if (Math.abs(palmRatio - PHI_SQUARED) > 1.5) {
    warnings.push(`Ratio Paume/Module (${palmRatio.toFixed(2)}) s'écarte du ratio naturel (${PHI_SQUARED.toFixed(2)})`);
  }

  // Ratio poing/paume devrait être proche de PHI
  const fistPalmRatio = Po / P;
  if (Math.abs(fistPalmRatio - PHI) > 0.5) {
    warnings.push(`Ratio Poing/Paume (${fistPalmRatio.toFixed(2)}) s'écarte du ratio doré`);
  }

  // Vérifications de cohérence
  if (Po < P) {
    errors.push('Le poing fermé devrait être plus large que la paume seule');
  }

  if (I < M * 2) {
    warnings.push('L\'index semble court par rapport au module du pouce');
  }

  return {
    valid: errors.length === 0,
    errors: errors,
    warnings: warnings,
    harmonicScore: calculateHarmonicScore(userMeasures)
  };
}

/**
 * Calcule un score d'harmonie basé sur la proximité avec les ratios dorés
 *
 * @param {Object} userMeasures - Mesures biométriques
 * @returns {number} Score de 0 à 100
 */
function calculateHarmonicScore(userMeasures) {
  const { M, P, I, Po } = userMeasures;

  const ratios = [
    { actual: P / M, expected: PHI_SQUARED, weight: 0.3 },
    { actual: Po / P, expected: PHI, weight: 0.3 },
    { actual: I / M, expected: PHI_CUBED, weight: 0.2 },
    { actual: Po / M, expected: PHI_CUBED, weight: 0.2 }
  ];

  let totalScore = 0;

  for (const ratio of ratios) {
    const deviation = Math.abs(ratio.actual - ratio.expected) / ratio.expected;
    const score = Math.max(0, 1 - deviation) * 100;
    totalScore += score * ratio.weight;
  }

  return Math.round(totalScore);
}

// ==================== EXPORTS ====================

module.exports = {
  PHI,
  PHI_SQUARED,
  PHI_CUBED,
  SYMBOL_CATEGORIES,
  PHASES,
  calculateArmorDimensions,
  calculateSymbolDimension,
  generateArmorBlueprint,
  validateBiometricProportions,
  calculateHarmonicScore
};

// ==================== EXEMPLE D'UTILISATION ====================

if (require.main === module) {
  // Exemple avec mesures test
  const myMeasures = { M: 2.1, P: 8.5, I: 7.2, Po: 9.5 };

  console.log('\n═══════════════════════════════════════════════════════════════');
  console.log('           AT·OM BIOMETRIC ENGINE - RÉSULTATS                   ');
  console.log('═══════════════════════════════════════════════════════════════\n');

  const results = calculateArmorDimensions(myMeasures);

  console.log('MESURES ENTRÉES:');
  console.log(`  Module (M):    ${myMeasures.M} cm`);
  console.log(`  Paume (P):     ${myMeasures.P} cm`);
  console.log(`  Index (I):     ${myMeasures.I} cm`);
  console.log(`  Poing (Po):    ${myMeasures.Po} cm`);

  console.log('\nDIMENSIONS CALCULÉES:');
  console.log(`  Petits Symboles:  ${results.dimensions.small} cm`);
  console.log(`  Symboles Moyens:  ${results.dimensions.medium} cm`);
  console.log(`  Grands Symboles:  ${results.dimensions.large} cm`);

  console.log('\nCALIBRATIONS ANATOMIQUES:');
  console.log(`  Fleur de Vie:     ${results.anatomical.fleurDeVie} cm (Poing)`);
  console.log(`  Cube de Métatron: ${results.anatomical.cubeMetatron} cm`);
  console.log(`  Œil d'Horus:      ${results.anatomical.eyeOfHorus} cm (Index)`);
  console.log(`  Triskel:          ${results.anatomical.triskel} cm`);

  const validation = validateBiometricProportions(myMeasures);
  console.log('\nVALIDATION:');
  console.log(`  Score Harmonique: ${validation.harmonicScore}/100`);
  console.log(`  Valide: ${validation.valid ? 'OUI' : 'NON'}`);

  if (validation.warnings.length > 0) {
    console.log('\n  Avertissements:');
    validation.warnings.forEach(w => console.log(`    - ${w}`));
  }

  console.log('\n═══════════════════════════════════════════════════════════════\n');
}
