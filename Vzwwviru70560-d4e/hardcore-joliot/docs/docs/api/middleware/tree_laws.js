/**
 * CHE·NU™ TREE LAWS (OFFICIAL)
 * The 5 fundamental governance laws that apply to ALL actions in CHE·NU
 * Based on CHENU_MASTER_REFERENCE v5.0 - EXACT IMPLEMENTATION
 */

/**
 * LAW 1: SAFE
 * Rule: "Le système est toujours sécurisé"
 * Enforcement: Toute action compromettant la sécurité est bloquée
 */
function enforceSafe(action, context) {
  const UNSAFE_ACTIONS = [
    'execute_arbitrary_code',
    'system_config_change',
    'modify_security_settings',
    'disable_validation',
    'bypass_authentication'
  ];
  
  // Check if action is inherently unsafe
  if (UNSAFE_ACTIONS.includes(action.type)) {
    return {
      allowed: false,
      violation: '1_SAFE',
      law_name: 'Safe',
      message: `Action "${action.type}" compromises system security`,
      enforcement: 'Action blocked to maintain system safety'
    };
  }
  
  // Check if action has unsafe parameters
  if (action.parameters && action.parameters.unsafe === true) {
    return {
      allowed: false,
      violation: '1_SAFE',
      law_name: 'Safe',
      message: 'Action contains unsafe parameters',
      enforcement: 'Action blocked to maintain system safety'
    };
  }
  
  return { allowed: true };
}

/**
 * LAW 2: NON_AUTONOMOUS
 * Rule: "Aucune action sans approbation humaine"
 * Enforcement: Toute action requiert validation explicite
 */
function enforceNonAutonomous(action, context) {
  // Check if action has explicit human approval
  if (!action.approved_by_human) {
    return {
      allowed: false,
      violation: '2_NON_AUTONOMOUS',
      law_name: 'Non-Autonomous',
      message: 'No action can execute without explicit human approval',
      enforcement: 'Requires explicit user validation',
      requires: 'human_approval'
    };
  }
  
  // Verify approval timestamp is recent (< 5 minutes)
  if (action.approval_timestamp) {
    const approvalAge = Date.now() - new Date(action.approval_timestamp).getTime();
    if (approvalAge > 5 * 60 * 1000) {
      return {
        allowed: false,
        violation: '2_NON_AUTONOMOUS',
        law_name: 'Non-Autonomous',
        message: 'Approval expired - action requires fresh approval',
        enforcement: 'Approval must be recent (< 5 minutes)',
        requires: 'fresh_human_approval'
      };
    }
  }
  
  return { allowed: true };
}

/**
 * LAW 3: REPRESENTATIONAL
 * Rule: "Structure uniquement, pas d'exécution réelle non-approuvée"
 * Enforcement: L'IA propose, l'humain dispose
 */
function enforceRepresentational(action, context) {
  const REAL_EXECUTION_ACTIONS = [
    'send_email',
    'make_payment',
    'delete_data',
    'publish_content',
    'create_external_resource',
    'modify_production_data'
  ];
  
  // Check if this is a real execution (not just a proposal/preview)
  if (REAL_EXECUTION_ACTIONS.includes(action.type) && action.mode !== 'preview') {
    if (!action.execution_approved) {
      return {
        allowed: false,
        violation: '3_REPRESENTATIONAL',
        law_name: 'Representational',
        message: 'AI can only propose structure, not execute real actions without approval',
        enforcement: 'Action converted to preview/proposal mode',
        suggestion: 'Change action.mode to "preview" or get execution_approved=true'
      };
    }
  }
  
  return { allowed: true };
}

/**
 * LAW 4: PRIVACY
 * Rule: "Protection absolue des données"
 * Enforcement: Chiffrement, isolation, consentement explicite
 */
function enforcePrivacy(action, context) {
  // Check for personal data access
  if (action.accesses_personal_data) {
    // Verify user gave consent for this specific data access
    if (!action.data_access_consent) {
      return {
        allowed: false,
        violation: '4_PRIVACY',
        law_name: 'Privacy',
        message: 'Accessing personal data requires explicit consent',
        enforcement: 'Data access blocked - consent required',
        requires: 'explicit_data_consent'
      };
    }
  }
  
  // Check for cross-sphere data access
  if (context.sphere_id && action.target_sphere_id) {
    if (context.sphere_id !== action.target_sphere_id) {
      if (!action.cross_sphere_approved) {
        return {
          allowed: false,
          violation: '4_PRIVACY',
          law_name: 'Privacy',
          message: 'Cross-sphere data access requires explicit approval',
          enforcement: 'Data isolation enforced between spheres',
          requires: 'cross_sphere_consent'
        };
      }
    }
  }
  
  // Check for data export
  if (action.type === 'export_data' && !action.encryption_enabled) {
    return {
      allowed: false,
      violation: '4_PRIVACY',
      law_name: 'Privacy',
      message: 'Data export requires encryption',
      enforcement: 'Encryption mandatory for data export'
    };
  }
  
  return { allowed: true };
}

/**
 * LAW 5: TRANSPARENCY
 * Rule: "Traçabilité complète de toutes les actions"
 * Enforcement: Audit trail immutable sur toutes les opérations
 */
async function enforceTransparency(pool, action, context) {
  // Every action MUST be logged to audit trail
  try {
    await pool.query(
      `INSERT INTO governance_audit_log 
       (user_id, action_type, resource_type, resource_id, details, created_at)
       VALUES ($1, $2, $3, $4, $5, NOW())`,
      [
        context.user_id,
        action.type,
        action.resource_type || 'unknown',
        action.resource_id || null,
        JSON.stringify({
          action: action,
          context: context,
          tree_law: '5_TRANSPARENCY'
        })
      ]
    );
    
    return { 
      allowed: true,
      logged: true,
      audit_entry_created: true
    };
  } catch (error) {
    // If audit logging fails, action CANNOT proceed
    return {
      allowed: false,
      violation: '5_TRANSPARENCY',
      law_name: 'Transparency',
      message: 'Failed to create audit trail - action blocked',
      enforcement: 'All actions must be logged - no exceptions',
      error: error.message
    };
  }
}

/**
 * APPLICATION EXAMPLES OF TREE LAWS
 * Based on Master Reference Table
 */
const TREE_LAW_EXAMPLES = {
  '1_SAFE': {
    situation: 'Exécution de code',
    action: 'Sandbox + validation'
  },
  '2_NON_AUTONOMOUS': {
    situation: 'Agent veut envoyer email',
    action: 'Demande approbation utilisateur'
  },
  '3_REPRESENTATIONAL': {
    situation: 'Modification document',
    action: 'Preview avant commit'
  },
  '4_PRIVACY': {
    situation: 'Accès données sensibles',
    action: 'Vérification permissions + log'
  },
  '5_TRANSPARENCY': {
    situation: 'Toute action',
    action: 'Ajout à l\'audit trail'
  }
};

/**
 * MASTER ENFORCEMENT FUNCTION
 * Applies THE 5 OFFICIAL TREE LAWS to a given context
 * Based on CHENU_MASTER_REFERENCE v5.0
 */
async function enforceTreeLaws(pool, context, action) {
  const violations = [];
  
  // LAW 1: SAFE
  const law1 = enforceSafe(action, context);
  if (!law1.allowed) violations.push(law1);
  
  // LAW 2: NON_AUTONOMOUS
  const law2 = enforceNonAutonomous(action, context);
  if (!law2.allowed) violations.push(law2);
  
  // LAW 3: REPRESENTATIONAL
  const law3 = enforceRepresentational(action, context);
  if (!law3.allowed) violations.push(law3);
  
  // LAW 4: PRIVACY
  const law4 = enforcePrivacy(action, context);
  if (!law4.allowed) violations.push(law4);
  
  // LAW 5: TRANSPARENCY (async - must log to database)
  const law5 = await enforceTransparency(pool, action, context);
  if (!law5.allowed) violations.push(law5);
  
  // Return result
  if (violations.length > 0) {
    return {
      allowed: false,
      violations,
      summary: `${violations.length} Tree Law violation(s) detected`,
      violated_laws: violations.map(v => v.law_name)
    };
  }
  
  return {
    allowed: true,
    laws_enforced: 5,
    laws: ['SAFE', 'NON_AUTONOMOUS', 'REPRESENTATIONAL', 'PRIVACY', 'TRANSPARENCY'],
    summary: 'All 5 Tree Laws satisfied'
  };
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  // The 5 Official Tree Laws
  enforceSafe,                    // LAW 1: SAFE
  enforceNonAutonomous,           // LAW 2: NON_AUTONOMOUS
  enforceRepresentational,        // LAW 3: REPRESENTATIONAL
  enforcePrivacy,                 // LAW 4: PRIVACY
  enforceTransparency,            // LAW 5: TRANSPARENCY
  
  // Master enforcement function
  enforceTreeLaws,
  
  // Examples
  TREE_LAW_EXAMPLES
};

