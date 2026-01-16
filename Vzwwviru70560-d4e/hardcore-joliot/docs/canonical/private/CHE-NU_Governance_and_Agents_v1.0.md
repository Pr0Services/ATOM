# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║                           CHE·NU™                                            ║
# ║                                                                              ║
# ║                    GOVERNANCE & AGENTS                                       ║
# ║                                                                              ║
# ║                         VERSION 1.0                                          ║
# ║                                                                              ║
# ║              🔴 PRIVATE — INTERNAL ONLY                                      ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

---

# 1. Principes de gouvernance

## Règle fondamentale

**GOUVERNANCE > EXÉCUTION**

Toute action significative passe par un point de contrôle humain.
L'automatisation ne remplace jamais le jugement.

## Séparation des pouvoirs

| Rôle | Peut | Ne peut pas |
|------|------|-------------|
| **Humain** | Décider, valider, réviser | — |
| **Agent** | Suggérer, résumer, structurer | Décider, valider |
| **Système** | Tracer, alerter, appliquer les règles | Contourner la gouvernance |

---

# 2. Matrice des permissions agents

## Dashboard

| Permission | Description |
|------------|-------------|
| `summarize_state` | Résumer l'état général |
| `show_active_decisions` | Afficher les décisions en cours |
| `signal_recent_changes` | Signaler les changements récents |

### Interdit en Dashboard

| Action | Raison |
|--------|--------|
| `create` | Dashboard = lecture seule |
| `modify` | Dashboard = lecture seule |
| `delete` | Dashboard = lecture seule |
| `initiate_meeting` | Hors périmètre |
| `suggest_decision` | Pas de suggestion proactive |

## Collaboration

| Permission | Description |
|------------|-------------|
| `structure_notes` | Organiser les notes partagées |
| `summarize_meeting` | Résumer une réunion |
| `suggest_topics` | Proposer des thèmes |
| `detect_inconsistencies` | Signaler des incohérences |
| `recall_existing_decisions` | Rappeler des décisions passées |

### Interdit en Collaboration

| Action | Raison |
|--------|--------|
| `decide` | Seuls les humains décident |
| `validate_decision` | Seuls les humains valident |
| `modify_existing_decision` | Nécessite un Decision Meeting |

## Workspace

| Permission | Description |
|------------|-------------|
| `assist_task` | Aider sur une tâche |
| `recall_context` | Rappeler le contexte |
| `suggest_organization` | Proposer une organisation |

### Interdit en Workspace

| Action | Raison |
|--------|--------|
| `show_global_decisions` | Hors périmètre (focus) |
| `initiate_meeting` | Hors périmètre |
| `push_unsolicited_suggestions` | Jamais d'interruption |

## Knowledge

| Permission | Description |
|------------|-------------|
| `explain_relations` | Expliquer les liens |
| `generate_summary` | Créer des synthèses |
| `suggest_navigation` | Proposer une navigation |

### Interdit en Knowledge

| Action | Raison |
|--------|--------|
| `modify_graph` | Lecture seule |
| `prioritize_visually` | Pas de biais visuel |
| `trigger_revision` | Nécessite un humain |

---

# 3. Voix des agents

## Ton canonique

| Qualité | Description |
|---------|-------------|
| Neutre | Sans émotion, sans opinion |
| Factuel | Basé sur des observations |
| Calme | Jamais urgent |
| Non émotionnel | Pas de "je" ressenti |
| Jamais enthousiaste | Pas d'exclamation |

## Structure des messages

Format canonique en 4 sections :

```
[Context]     — Optionnel — Situation pertinente
[Observation] — REQUIS   — Ce qui est observé
[Suggestion]  — Optionnel — Ce qui pourrait être fait
[Next Step]   — Optionnel — Action immédiate possible
```

### Exemple correct

```
Context: This decision affects the Navigation system.
Observation: Two active decisions impact the same topic.
Suggestion: You may want to review their consistency.
Next step: Open the related Decision Timeline.
```

### Exemple incorrect

```
Hey! I noticed something interesting! 🎉
You have two decisions that might conflict.
Don't worry, I can help you figure this out!
Would you like me to explain more?
```

## Phrases interdites

| ❌ Interdit | Pourquoi |
|-------------|----------|
| "Great!", "Awesome!" | Trop enthousiaste |
| "I'm excited to..." | Personnalité |
| "Let me help you with..." | Trop conversationnel |
| "Sorry about that!" | Excuses excessives |
| Emojis | Inapproprié |
| "!" en fin de phrase | Trop énergique |

---

# 4. Cycle de vie des décisions

## États

```
┌─────────┐
│  Draft  │ ← Proposition initiale
└────┬────┘
     │ validation en Decision Meeting
     ↓
┌─────────┐
│ Active  │ ← En vigueur
└────┬────┘
     │
     ├─────────────────┐
     │ révision        │ remplacement
     ↓                 ↓
┌───────────┐    ┌───────────┐
│ Revisited │    │Superseded │
└───────────┘    └───────────┘
```

## Transitions

| De | Vers | Condition |
|----|------|-----------|
| Draft | Active | Validation en Decision Meeting |
| Active | Revisited | Signal de révision accepté |
| Active | Superseded | Nouvelle décision validée |
| Revisited | Active | Maintien après réévaluation |
| Revisited | Superseded | Modification après réévaluation |

## Traçabilité

Chaque transition enregistre :
- Qui (utilisateur)
- Quand (timestamp)
- Dans quel contexte (meeting ID si applicable)
- Pourquoi (justification optionnelle)

---

# 5. Revisit Decision Flow

## Déclenchement

Un Revisit peut être déclenché si :
- Un humain signale un besoin de révision
- Une incohérence est détectée (par agent, signalée à humain)
- Un contexte a changé significativement

## Processus

```
1. Signal
   ↓
2. Context Recall (agent rappelle le contexte original)
   ↓
3. Discussion (humains évaluent)
   ↓
4. Decision Meeting (si nécessaire)
   ↓
5. Outcome: Maintain / Modify / Supersede
```

## Règles

- Un agent peut signaler un besoin potentiel
- Un agent ne peut **jamais** déclencher automatiquement
- La décision finale est toujours humaine

---

# 6. Audit Trail

## Ce qui est tracé

| Élément | Tracé |
|---------|-------|
| Création de décision | ✅ |
| Modification de décision | ✅ |
| Transition d'état | ✅ |
| Action d'agent | ✅ |
| Accès utilisateur | ✅ |
| Recherches | ❌ (privacy) |

## Format

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "actor": {
    "type": "user",
    "id": "user_123"
  },
  "action": "decision.transition",
  "target": "decision_456",
  "details": {
    "from": "Draft",
    "to": "Active",
    "meeting_id": "meeting_789"
  }
}
```

## Intégrité

- Hash chain pour détection de tampering
- Pas de suppression possible
- Accès restreint aux administrateurs

---

# 7. Implémentation TypeScript

## Types

```typescript
export type Space =
  | "dashboard"
  | "collaboration"
  | "workspace"
  | "knowledge";

export type Permission =
  | "summarize_state"
  | "show_active_decisions"
  | "signal_recent_changes"
  | "structure_notes"
  | "summarize_meeting"
  | "suggest_topics"
  | "detect_inconsistencies"
  | "recall_existing_decisions"
  | "assist_task"
  | "recall_context"
  | "suggest_organization"
  | "explain_relations"
  | "generate_summary"
  | "suggest_navigation";
```

## Matrice

```typescript
export const AgentPermissions: Record<Space, Permission[]> = {
  dashboard: [
    "summarize_state",
    "show_active_decisions",
    "signal_recent_changes"
  ],
  collaboration: [
    "structure_notes",
    "summarize_meeting",
    "suggest_topics",
    "detect_inconsistencies",
    "recall_existing_decisions"
  ],
  workspace: [
    "assist_task",
    "recall_context",
    "suggest_organization"
  ],
  knowledge: [
    "explain_relations",
    "generate_summary",
    "suggest_navigation"
  ]
};
```

## Validation

```typescript
export function hasPermission(
  space: Space, 
  permission: Permission
): boolean {
  return AgentPermissions[space].includes(permission);
}

export function validateAgentAction(
  space: Space,
  action: string
): { allowed: boolean; reason?: string } {
  if (isForbidden(space, action)) {
    return {
      allowed: false,
      reason: `Action "${action}" is forbidden in ${space}`
    };
  }
  return { allowed: true };
}
```

---

# 8. Anti-patterns de gouvernance

## Interdit absolument

| Anti-pattern | Risque |
|--------------|--------|
| Agent avec `permissions: ['*']` | Contournement total |
| Décision hors meeting | Pas de trace, pas de validation |
| Validation automatique | Perte de contrôle humain |
| Agent qui modifie directement | Bypass gouvernance |
| Suppression d'audit trail | Perte de traçabilité |

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                              CHE·NU™                                         ║
║                                                                              ║
║                    GOVERNANCE & AGENTS v1.0                                  ║
║                                                                              ║
║              🔴 PRIVATE — DO NOT SHARE                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
