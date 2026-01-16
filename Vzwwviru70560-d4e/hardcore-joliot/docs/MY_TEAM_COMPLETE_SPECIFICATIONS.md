# 🤝 MY TEAM — SPÉCIFICATIONS COMPLÈTES V2.0

**Date:** 21 Décembre 2025  
**Architecture:** HUB INTÉGRÉ (RH + Agents + Skills + Prompts + IA Labs)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                   MY TEAM 🤝 = HUB COMPLET                                   ║
║                                                                               ║
║   👥 Employés | 🤖 Agents | 🛠️ Skills | 💬 Prompts | 🔬 IA Labs            ║
║                                                                               ║
║   My Team NE SE SÉPARE PAS - Tout est intégré dans une sphère unique        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 LISTE COMPLÈTE DES BESOINS (58)

### EMPLOYÉS HUMAINS (8)
1. Liste employés
2. Org chart complet
3. Org chart par sphère
4. Org chart par entité
5. Onboarding
6. Profils employés
7. Performance reviews
8. Training

### AGENTS IA (12)
9. Liste tous agents
10. Hiérarchie complète L0→L3
11. Hiérarchie par sphère
12. Hiérarchie par entité
13. **Agent card → Bouton "⚙️ Modifier dans IA Labs"**
14. Embaucher agent
15. Assigner agent → sphère
16. Assigner agent → entité
17. Désactiver agent
18. Supprimer agent
19. Performance agent
20. Coûts tokens

### SKILLS & TOOLS (8)
21. BD compétences
22. BD méthodes (GTD, Agile)
23. BD templates
24. Créer skill
25. Modifier skill
26. **Assigner skill → agent**
27. Catégories skills
28. Recherche skills

### PROMPTS (10)
29. BD prompts
30. BD templates prompts
31. Créer prompt
32. Créer prompt from template
33. Modifier prompt
34. **Tester prompt (Playground)**
35. Variables prompts
36. Versioning prompts
37. **Assigner prompt → agent**
38. Catégories prompts

### IA LABS (10)
39. Développer nouvel agent
40. **Modifier agent (from card)**
41. **Accès mémoire contrôlée agent**
42. Modifier paramètres
43. **Assigner modèle LLM**
44. Assigner prompt
45. Sandbox testing
46. Déployer agent
47. Version control
48. Clone agent

### WORKFLOWS (5)
49. **Améliorer Workflow Builder existant**
50. Workflows avec agents
51. Templates workflows
52. Workflows cross-sphere
53. Workflows RH

### ANALYTICS (5)
54. Dashboard My Team
55. Analytics agents
56. Analytics employés
57. Reports automatisés
58. Alerts

## 🎯 ARCHITECTURE NAVIGATION

```
MY TEAM 🤝
│
├── 📊 DASHBOARD
│
├── 👥 EMPLOYÉS (RH)
│   ├── Liste employés
│   ├── Org Charts (complet/sphère/entité)
│   └── Onboarding
│
├── 🤖 AGENTS IA
│   ├── Tous les agents
│   │   └── [Agent Card] → ⚙️ IA Labs
│   ├── Hiérarchie (L0→L3)
│   │   ├── Par niveau
│   │   ├── Par sphère
│   │   └── Par entité
│   ├── ➕ Embaucher
│   └── 📊 Analytics
│
├── 🛠️ SKILLS & TOOLS
│   ├── BD Skills
│   ├── Méthodes (GTD, Agile...)
│   ├── Templates
│   └── Assignment skills→agents
│
├── 🔬 IA LABS
│   ├── 🤖 AGENTS
│   │   ├── ➕ Nouveau
│   │   ├── ✏️ Modifier (from card)
│   │   │   ├── General
│   │   │   ├── 💬 Prompts
│   │   │   ├── 🧠 MÉMOIRE CONTRÔLÉE
│   │   │   │   ├── Conversations
│   │   │   │   ├── Décisions
│   │   │   │   ├── Contexte permanent
│   │   │   │   └── Préférences
│   │   │   ├── ⚙️ Paramètres LLM
│   │   │   └── 🛠️ Skills
│   │   ├── 🧪 Sandbox
│   │   └── 🚀 Deploy
│   │
│   └── 💬 PROMPTS
│       ├── BD Prompts
│       ├── Templates Prompts
│       ├── ➕ Nouveau Prompt
│       ├── ✏️ Prompt Editor
│       │   ├── Texte prompt
│       │   ├── Variables
│       │   ├── Exemples
│       │   └── 🧪 Playground
│       └── Assignment prompts→agents
│
├── 🔄 WORKFLOWS
│   └── Builder amélioré + Agent nodes
│
└── 📊 ANALYTICS
```

## 🏗️ PLAN DE BUILD (8 SPRINTS)

### SPRINT 1: Fondations (3-4j)
- DB tables + migrations
- API routes basiques
- Tests

### SPRINT 2: Agents (4-5j)
- Liste + hiérarchie
- Agent card avec bouton IA Labs
- Hiring + assignment
- Analytics

### SPRINT 3: IA Labs Agents (5-6j)
- Layout IA Labs
- Agent editor tabs
- **Mémoire contrôlée UI**
- Params + Skills
- Version control

### SPRINT 4: Prompts (4-5j)
- BD prompts
- Prompt editor
- **Playground testing**
- Templates
- Assignment→agents

### SPRINT 5: Skills (3-4j)
- BD skills
- Méthodes + templates
- UI complète
- Assignment→agents

### SPRINT 6: Workflows (3-4j)
- Améliorer builder existant
- Agent nodes
- Templates

### SPRINT 7: RH (2-3j)
- Employés
- Org charts
- Onboarding

### SPRINT 8: Polish (2-3j)
- UI/UX
- Tests E2E
- Documentation

## ✅ CRITÈRES DE SUCCÈS

**Must Have:**
- ✅ Agent card → Bouton IA Labs fonctionne
- ✅ Mémoire contrôlée accessible et éditable
- ✅ Prompts assignables aux agents
- ✅ Skills assignables aux agents
- ✅ Modèles LLM configurables
- ✅ Workflow Builder avec agents
- ✅ Hiérarchie complète visible
- ✅ Analytics agents fonctionnels

**Architecture:**
- ✅ MY TEAM reste UNE sphère intégrée
- ✅ Skills & Tools DANS My Team
- ✅ IA Labs DANS My Team
- ✅ Connexion fluide entre toutes parties

## 🔥 NEXT STEPS

1. Valider cette spec ✅
2. Commencer Sprint 1 (DB)
3. Coder progressivement
4. Générer ZIP complet final

**PRÊT À COMMENCER! 💪**
