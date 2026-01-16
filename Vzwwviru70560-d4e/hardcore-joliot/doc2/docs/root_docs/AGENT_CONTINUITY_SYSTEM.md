# 🔄 CHE·NU™ — SYSTÈME DE CONTINUITÉ INTER-AGENTS

## 📋 PROTOCOLE DE COMMUNICATION ENTRE AGENTS

Ce document établit le protocole de passation entre agents Claude travaillant sur CHE·NU™.
**CHAQUE AGENT DOIT LIRE CE DOCUMENT EN PREMIER.**

---

## 🧠 MÉMOIRE PARTAGÉE — STRUCTURE

### Format Standard de Compte Rendu

Chaque agent DOIT terminer sa session en créant/mettant à jour:

```
CHENU_AGENT_HANDOFF.md
├── AGENT_ID: [Numéro séquentiel]
├── DATE_SESSION: [YYYY-MM-DD HH:MM]
├── DURÉE: [Temps de session]
├── SPRINT_ACTUEL: [1-10]
├── TÂCHES_COMPLÉTÉES: [Liste]
├── TÂCHES_EN_COURS: [Liste avec % progression]
├── BLOCAGES: [Problèmes rencontrés]
├── DÉCISIONS_PRISES: [Choix architecturaux]
├── FICHIERS_MODIFIÉS: [Liste des fichiers]
├── PROCHAINES_ACTIONS: [Pour l'agent suivant]
└── NOTES_IMPORTANTES: [Contexte critique]
```

---

## 📊 ÉTAT ACTUEL DU PROJET

### Version: v40.0.0
### Score Qualité: 67/100
### Score Cible: 90/100

### Architecture GELÉE (NE PAS MODIFIER)

```
9 SPHÈRES:
1. Personal 🏠
2. Business 💼
3. Government 🏛️
4. Creative 🎨
5. Community 👥
6. Social 📱
7. Entertainment 🎬
8. My Team 🤝
9. Scholar 📚 ← NOUVELLE (9ème sphère académique)

6 SECTIONS BUREAU:
1. Quick Capture 📝
2. Resume Workspace ▶️
3. Threads 💬
4. Data Files 📁
5. Active Agents 🤖
6. Meetings 📅
```

### Statistiques Actuelles

| Métrique | Valeur |
|----------|--------|
| Fichiers totaux | 5,840 |
| Web (React) | 2,879 |
| Mobile (Expo) | 59 |
| Desktop (Electron) | 4 |
| Backend (Python/TS) | 904 |
| SDK | 288 |
| Tests | 49 (~15% coverage) |
| Documentation | 848 MD files |

---

## ⚠️ RÈGLES NON-NÉGOCIABLES

1. **9 SPHÈRES** — Ne jamais ajouter/supprimer/fusionner
2. **6 SECTIONS** — Structure fixe pour tous les bureaux
3. **Nova = L0** — Jamais "hired", toujours système
4. **Tokens = Crédits internes** — PAS de crypto
5. **Governance BEFORE execution** — Toujours
6. **Scholar = 9ème sphère** — Nouvelle, à maintenir

---

## 🎯 OBJECTIFS GLOBAUX

### Vision
Transformer CHE·NU™ d'un prototype (67/100) en produit production-ready (90/100) en 10 sprints.

### Métriques Cibles

| Métrique | Actuel | Cible |
|----------|--------|-------|
| Test Coverage | 15% | 85% |
| Lighthouse Score | ? | 95 |
| Mobile Completion | 35% | 95% |
| Desktop Completion | 25% | 95% |
| Intégrations | 2 | 30 |
| Components UI | 50 | 150 |

---

## 📁 FICHIERS CRITIQUES À CONNAÎTRE

```
/frontend/src/constants/canonical.ts    ← SOURCE DE VÉRITÉ (9 sphères, 6 sections)
/frontend/src/stores/sphereStore.ts     ← State management sphères
/frontend/src/stores/governanceStore.ts ← Gouvernance tokens
/frontend/src/components/bureau/        ← Composants bureau
/mobile/src/constants/canonical.ts      ← Config mobile
/desktop/src/main.js                    ← Entry Electron
/backend/services/                      ← Services API
```

---

## 🔄 PROTOCOLE DE PASSATION

### À la FIN de chaque session:

1. **Sauvegarder le travail** dans un ZIP daté
2. **Mettre à jour** CHENU_AGENT_HANDOFF.md
3. **Lister** les fichiers modifiés
4. **Documenter** les décisions prises
5. **Identifier** les blocages
6. **Préparer** les instructions pour l'agent suivant

### Au DÉBUT de chaque session:

1. **Lire** ce document (AGENT_CONTINUITY_SYSTEM.md)
2. **Lire** CHENU_AGENT_HANDOFF.md
3. **Vérifier** le sprint actuel
4. **Identifier** les tâches assignées
5. **Continuer** là où l'agent précédent s'est arrêté

---

## 📞 COMMUNICATION INTER-AGENTS

### Via Mémoire Claude (userMemories)

Chaque agent doit demander à Jo de mettre à jour la mémoire avec:

```
Format mémoire:
"CHE·NU SPRINT [X]: [Résumé 200 chars max]. Tâches [X-Y] complétées. Prochain: [action]."
```

### Exemple:
```
"CHE·NU SPRINT 2: Tests stores complétés (sphereStore, authStore). 
Tâches 11-15 done. Prochain: tests hooks useAuth, useNavigation."
```

---

## 📋 CHECKLIST AGENT

### Début de Session
- [ ] Lu AGENT_CONTINUITY_SYSTEM.md
- [ ] Lu CHENU_AGENT_HANDOFF.md
- [ ] Identifié sprint actuel
- [ ] Compris les tâches assignées
- [ ] Vérifié les fichiers critiques

### Fin de Session
- [ ] Travail sauvegardé (ZIP)
- [ ] CHENU_AGENT_HANDOFF.md mis à jour
- [ ] Fichiers modifiés listés
- [ ] Décisions documentées
- [ ] Instructions prochain agent préparées
- [ ] Demandé mise à jour mémoire Jo

---

*Dernière mise à jour: 20 décembre 2025 — Agent Initial*
