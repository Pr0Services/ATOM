# CHE·NU™ — GOUVERNANCE DES CONFIRMATIONS

## Règle Fondatrice | Version 1.0 | Statut: FIGÉE

---

## PRINCIPE CENTRAL (NON NÉGOCIABLE)

> **L'information explicite n'est JAMAIS redemandée.**
> **La confirmation porte UNIQUEMENT sur l'interprétation, pas le contenu.**

---

## DISTINCTION FONDAMENTALE

CHE·NU distingue strictement deux catégories d'actions:

### 1️⃣ OPÉRATIONS → Fluides (Pas de confirmation)

| Type | Exemples |
|------|----------|
| Navigation | view, read, navigate, browse, explore |
| Analyse | analyze, calculate, compute, evaluate |
| Préparation | draft, prepare, structure, preview |
| Suggestions | suggest, recommend, propose_draft |
| Temporaire | temp_save, pre_classify, bookmark_temp |

**Règles des opérations:**
- ✅ S'exécutent SANS confirmation
- ✅ Ne créent PAS de mémoire longue
- ✅ N'engagent PAS le futur
- ✅ Toujours traçables mais non bloquantes

---

### 2️⃣ ENGAGEMENTS → Confirmés (Confirmation obligatoire)

| Type | Exemples |
|------|----------|
| Suppression | delete, remove_permanent, purge |
| Archivage | archive_final, close_permanent |
| Publication | publish, share_public, broadcast |
| Mémoire | memorize, remember_long, store_permanent |
| Décision | decide, conclude, finalize, commit |
| Cadre | change_frame, update_rules, modify_governance |
| Externe | send_to_client, legal_commit, invoice_send |

**Règles des engagements:**
- ✅ Confirmation explicite AVANT exécution
- ✅ Confirmation sur l'ACTION INTERPRÉTÉE
- ✅ UNE SEULE confirmation par action
- ✅ Jamais de redemande d'information explicite

---

## LOGIQUE D'INTERPRÉTATION CONTEXTUELLE

```
┌─────────────────────────────────────────────────────────────┐
│  1. Utilisateur fournit information explicite               │
│                         │                                   │
│                         ▼                                   │
│  2. Système interprète l'action possible                    │
│                         │                                   │
│                         ▼                                   │
│  3. Système formule clairement:                             │
│     "Voici l'action que je comprends devoir effectuer"      │
│                         │                                   │
│                         ▼                                   │
│  4. UNE UNIQUE confirmation sur cette action                │
│                         │                                   │
│                         ▼                                   │
│  5. Action exécutée ou ajustée                              │
└─────────────────────────────────────────────────────────────┘
```

---

## EXCEPTIONS (Pas de confirmation même si engagement)

| Exception | Description |
|-----------|-------------|
| `CADRE_DEJA_VALIDE` | Action dans un cadre prévalidé |
| `MANDAT_AGENT` | Couvert par mandat explicite d'agent |
| `FLUX_TECHNIQUE` | Purement technique/interne |
| `TOTALEMENT_REVERSIBLE` | 100% réversible et non engageant |
| `PREFERENCE_VALIDEE` | Conforme à préférence validée |

---

## CAS TOUJOURS CONFIRMÉS

**Même si le contexte est clair, confirmation obligatoire pour:**

- 🗑️ Suppression définitive
- 📦 Archivage final
- 🌐 Publication publique
- ✅ Décision finale
- 🧠 Mémoire longue
- ⚙️ Changement de cadre
- ⚡ Action à impact élevé
- 🤝 Engagement externe

---

## DIMINUTION DES CONFIRMATIONS DANS LE TEMPS

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   Plus les CADRES sont explicites                           │
│   Plus les MANDATS sont définis                             │
│   Plus les PRÉFÉRENCES sont validées                        │
│                         │                                   │
│                         ▼                                   │
│              MOINS le système interrompt                    │
│                                                              │
│   MAIS:                                                      │
│   → Les confirmations ne deviennent JAMAIS invisibles       │
│   → Elles restent lisibles, réversibles et auditables       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ANTI-PATTERNS (INTERDITS)

| ❌ Anti-Pattern | Explication |
|-----------------|-------------|
| Redemander une information explicite | L'utilisateur l'a déjà fournie |
| Multiplier les micro-confirmations | Fatigue inutile |
| Interrompre le flow pour des opérations | Les opérations sont fluides |
| Décider sans exposer l'interprétation | L'utilisateur doit voir ce qui sera fait |
| Mémoriser sans validation | La mémoire longue est un engagement |

---

## IMPLÉMENTATION TECHNIQUE

### Module Python

```python
from backend.core.governance.confirmation import requires_confirmation

result = requires_confirmation(
    action_type="create_note",
    user_id="user_123",
    sphere_id="personal",
    creates_memory=True,
    is_reversible=True,
    affects_external=False,
)

if result.requires_confirmation:
    # ENGAGEMENT → Demander confirmation
    show_confirmation_dialog(result.interpreted_action, result.preview)
else:
    # OPÉRATION → Exécuter directement
    execute_action()
```

### API Response

```json
{
  "action_id": "uuid",
  "interpreted_action": "Créer une note dans votre espace personnel",
  "requires_confirmation": true,
  "preview": "📝 Note: Titre de la page\n\nContenu capturé...",
  "confirmation_reason": "Création de mémoire — confirmation requise"
}
```

---

## PRINCIPE DE FLUIDITÉ

| Contexte | Priorité |
|----------|----------|
| Pendant l'exécution | **Fluidité** |
| Pour conclusions et mémoires importantes | **Responsabilité** |

**Le système privilégie:**
- Fiabilité > Vitesse
- Clarté > Fluidité artificielle

---

## OBJECTIF FINAL

Un système qui:
- ✅ Respecte l'intelligence humaine
- ✅ Ne fatigue pas inutilement
- ✅ Protège la responsabilité
- ✅ Rend l'engagement conscient
- ✅ Reste habitable à long terme

---

## APPLICABILITÉ

**Cette règle s'applique à:**
- Tous les agents CHE·NU
- Tous les hubs
- Toutes les interfaces (web, mobile, desktop)
- Toutes les extensions (Chrome Browser Habitat)
- Tous les modules
- Toutes les API

---

## STATUT

| Attribut | Valeur |
|----------|--------|
| Version | 1.0 |
| Statut | **FIGÉE** |
| Stabilité | **STABLE** |
| Type | **FONDATRICE** |
| Date | Décembre 2024 |

---

*CHE·NU™ — Governed Intelligence Operating System*
