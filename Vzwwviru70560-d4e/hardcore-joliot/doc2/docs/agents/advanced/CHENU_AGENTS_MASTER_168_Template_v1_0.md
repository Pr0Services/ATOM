# CHEÂ·NU â€” AGENTS MASTER LIST (168+ AGENTS)
**VERSION:** AGENTS.v1.0  
**MODE:** FOUNDATION / CONFIGURABLE / ONBOARDING-READY

---

## AGENT CONFIGURATION TEMPLATE âš¡

### Structure Universelle Pour Chaque Agent

```json
{
  "agent": {
    "id": "AGENT_XXX",
    "name": "Agent Name",
    "department": "sphere|system|utility",
    "level": "L0|L1|L2|L3",
    
    "system_prompt": {
      "base": "Prompt systÃ¨me fixe...",
      "dynamic_prefix": "{{user_context}}",
      "rules": ["non-manipulative", "factual", "neutral"]
    },
    
    "llm_config": {
      "recommended": "claude-sonnet-4-20250514|gpt-4o|llama-3.1-70b|gemini-pro",
      "fallback": "claude-haiku|gpt-4o-mini|llama-3.1-8b",
      "local_option": "ollama/mistral|ollama/llama3"
    },
    
    "parameters": {
      "temperature": { "default": 0.7, "range": [0.0, 1.0], "user_editable": true },
      "max_tokens": { "default": 2048, "range": [256, 8192], "user_editable": true },
      "top_p": { "default": 0.9, "range": [0.0, 1.0], "user_editable": true },
      "frequency_penalty": { "default": 0.0, "range": [0.0, 2.0], "user_editable": true }
    },
    
    "apis": {
      "required": ["api_1", "api_2"],
      "optional": ["api_3"],
      "internal": ["che_nu_memory", "che_nu_threads"]
    },
    
    "onboarding": {
      "required_fields": ["field_1", "field_2"],
      "optional_fields": ["field_3"],
      "context_injection": true
    },
    
    "user_customizable": {
      "name": true,
      "avatar": true,
      "tone": true,
      "language": true,
      "specialty_focus": true
    }
  }
}
```

---

## ONBOARDING FIELDS â€” USER INPUT âš¡

### Champs Universels (Tous Agents) âš¡

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_name` | string | âœ… | Nom de l'utilisateur |
| `company_name` | string | âœ… | Nom de l'entreprise |
| `company_industry` | string | âœ… | Secteur d'activitÃ© |
| `company_size` | enum | âœ… | startup/pme/grande/enterprise |
| `user_role` | string | âœ… | RÃ´le/titre de l'utilisateur |
| `user_responsibilities` | array | âœ… | Liste des responsabilitÃ©s |
| `current_projects` | array | âšª | Projets en cours |
| `team_members` | array | âšª | Membres de l'Ã©quipe |
| `company_vision` | text | âšª | Vision de l'entreprise |
| `company_values` | array | âšª | Valeurs de l'entreprise |
| `preferred_language` | enum | âœ… | fr/en/es/... |
| `timezone` | string | âœ… | Fuseau horaire |

### Champs Par SphÃ¨re âš¡

#### Business Sphere âš¡
| Field | Type | Description |
|-------|------|-------------|
| `revenue_target` | number | Objectif de revenus |
| `fiscal_year_end` | date | Fin d'annÃ©e fiscale |
| `key_competitors` | array | Concurrents principaux |
| `market_position` | string | Position sur le marchÃ© |
| `business_model` | string | ModÃ¨le d'affaires |

#### Scholar Sphere âš¡
| Field | Type | Description |
|-------|------|-------------|
| `research_domains` | array | Domaines de recherche |
| `certifications` | array | Certifications visÃ©es |
| `learning_goals` | array | Objectifs d'apprentissage |
| `expertise_level` | enum | beginner/intermediate/expert |

#### Creative Sphere âš¡
| Field | Type | Description |
|-------|------|-------------|
| `brand_guidelines` | object | Guide de marque |
| `design_preferences` | array | PrÃ©fÃ©rences design |
| `content_types` | array | Types de contenu produits |
| `target_audience` | string | Audience cible |

#### Institution Sphere (Construction QC) âš¡
| Field | Type | Description |
|-------|------|-------------|
| `rbq_license` | string | NumÃ©ro RBQ |
| `cnesst_registration` | string | Inscription CNESST |
| `ccq_region` | string | RÃ©gion CCQ |
| `specialty_codes` | array | Codes de spÃ©cialitÃ© |

---

## DYNAMIC PRE-PROMPT INJECTION âš¡

### Template Pre-Prompt âš¡

```
=== CONTEXTE UTILISATEUR ===
Utilisateur: {{user_name}}
RÃ´le: {{user_role}}
Entreprise: {{company_name}} ({{company_industry}}, {{company_size}})
ResponsabilitÃ©s: {{user_responsibilities | join(", ")}}
Projets actifs: {{current_projects | join(", ")}}
Vision: {{company_vision}}
Langue: {{preferred_language}}
Timezone: {{timezone}}

=== CONTEXTE SPHÃˆRE ===
{{sphere_specific_context}}

=== INSTRUCTIONS AGENT ===
{{agent_system_prompt}}

=== RÃˆGLES NON-NÃ‰GOCIABLES ===
- Tu ne manipules JAMAIS l'utilisateur
- Tu ne prends JAMAIS de dÃ©cisions pour lui
- Tu fournis des FAITS, pas des opinions
- Tu respectes la CONFIDENTIALITÃ‰
```

---

## LLM RECOMMENDATIONS PAR TYPE D'AGENT âš¡

| Agent Type | Recommended LLM | Fallback | Local Option |
|------------|-----------------|----------|--------------|
| **Strategic/Complex** | Claude Sonnet 4 | GPT-4o | Llama-3.1-70B |
| **Creative/Writing** | Claude Sonnet 4 | GPT-4o | Mistral-Large |
| **Code/Technical** | Claude Sonnet 4 | GPT-4o | CodeLlama-34B |
| **Data/Analysis** | GPT-4o | Claude Sonnet | Llama-3.1-70B |
| **Quick/Simple** | Claude Haiku | GPT-4o-mini | Llama-3.1-8B |
| **Multilingual** | Claude Sonnet 4 | GPT-4o | Mixtral-8x7B |
| **Safety/Compliance** | Claude Sonnet 4 | GPT-4o | Local only |

---

## PARAMETER PRESETS âš¡

### Preset: PRECISE âš¡
```json
{
  "temperature": 0.2,
  "top_p": 0.8,
  "frequency_penalty": 0.0,
  "use_case": "compliance, legal, data extraction"
}
```

### Preset: BALANCED âš¡
```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "frequency_penalty": 0.3,
  "use_case": "general assistance, analysis"
}
```

### Preset: CREATIVE âš¡
```json
{
  "temperature": 0.9,
  "top_p": 0.95,
  "frequency_penalty": 0.5,
  "use_case": "brainstorming, content creation"
}
```

### Preset: CONVERSATIONAL âš¡
```json
{
  "temperature": 0.8,
  "top_p": 0.9,
  "frequency_penalty": 0.2,
  "use_case": "coaching, support, dialogue"
}
```

---

**VOIR FICHIERS SUIVANTS POUR LISTE COMPLÃˆTE DES 168 AGENTS**
