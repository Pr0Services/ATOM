# 📚 04_SPECS_REFERENCE
## Documentation de Référence Complète

Ce dossier contient TOUS les documents officiels du projet CHE·NU™.

---

## 📄 Documents Clés

### 🔑 SOURCE DE VÉRITÉ
| Document | Taille | Description |
|----------|--------|-------------|
| **CHENU_MASTER_REFERENCE_v5_FINAL__1_.md** | 92 KB | Architecture complète, 10 sphères, 3 hubs |
| **CHENU_SYSTEM_MANUAL.md** | 61 KB | Guide technique détaillé |

### 📡 Spécifications Techniques
| Document | Taille | Description |
|----------|--------|-------------|
| **CHENU_API_SPECS_v29.md** | 19 KB | 15 sections API complètes |
| **CHENU_AGENT_PROMPTS_v29.md** | 17 KB | 226 agents définis |
| **CHENU_MERMAID_DIAGRAMS_v29.md** | 14 KB | Diagrammes architecture |

### 💼 Business
| Document | Taille | Description |
|----------|--------|-------------|
| **CHENU_INVESTOR_BOOK.md** | 48 KB | Vision et pitch investisseurs |
| **FEATURE_AUDIT_ROADMAP.md** | 8 KB | Audit features et roadmap |
| **CHENU_COMPTE_RENDU_CONTINUITY.md** | 5 KB | Compte-rendu continuité |

### 📕 PDFs (Versions Formatées)
| Document | Taille |
|----------|--------|
| CHENU_SYSTEM_MANUAL_v27.pdf | 10 MB |
| CHENU_INVESTOR_BOOK.pdf | 3.9 MB |
| CHENU_Documentation_Complete.pdf | 995 KB |

---

## 🎯 Ordre de Lecture Recommandé

### Pour comprendre le projet:
1. **CHENU_MASTER_REFERENCE_v5** — Vision et architecture
2. **CHENU_SYSTEM_MANUAL** — Détails techniques
3. **CHENU_INVESTOR_BOOK** — Business case

### Pour implémenter:
1. **CHENU_API_SPECS_v29** — Endpoints à implémenter
2. **CHENU_AGENT_PROMPTS_v29** — Agents à configurer
3. **CHENU_MERMAID_DIAGRAMS** — Flux à respecter

---

## 🏛️ Architecture Rappel

### 10 Sphères (selon MASTER_REFERENCE)
1. 🏠 Personnel
2. 💼 Entreprises
3. 🏛️ Gouvernement & Institutions
4. 🎨 Creative Studio
5. 🛠️ Skills & Tools (PILIER)
6. 🎮 Entertainment
7. 🤝 Community
8. 📱 Social Network & Media
9. 🤖 IA Labs
10. 👥 My Team

### 3 Hubs
1. **Communication Hub** — Intent Clarification (Nova, Agents, Messagerie, Email)
2. **Navigation Hub** — Contextual Selection (Sphères, DataSpaces, Données, Plateformes)
3. **Execution Workspace Hub** — Controlled Operations (Documents, Éditeurs, Browser, Projets)

### Governed Execution Pipeline (10 étapes)
1. Intent Capture
2. Semantic Encoding
3. Encoding Validation
4. Token & Cost Estimation
5. Scope Locking
6. Budget Verification
7. Agent Compatibility Check (ACM)
8. Controlled Execution
9. Result Capture
10. Thread Update (audit trail)

---

## ⚠️ Note sur les 8 vs 10 Sphères

Le MEMORY PROMPT mentionne 8 sphères, mais le MASTER_REFERENCE v5 définit 10 sphères.

**Réconciliation:**
- Le MASTER_REFERENCE v5 est la SOURCE DE VÉRITÉ
- Certaines sphères peuvent être regroupées dans l'UI
- Skills & Tools et IA Labs peuvent être dans "My Team" visuellement
- Social & Media peut être dans "Community" visuellement

**Règle:** Toujours respecter le MASTER_REFERENCE pour les structures de données, mais l'UI peut regrouper visuellement.

---

## 🔗 Liens entre Documents

```
MASTER_REFERENCE
      │
      ├── API_SPECS_v29 (endpoints)
      │       │
      │       └── SQL_SCHEMA_v29 (tables)
      │
      ├── AGENT_PROMPTS_v29 (226 agents)
      │
      ├── SYSTEM_MANUAL (détails)
      │       │
      │       └── CHAPTERS (dans 03_A_REFAIRE)
      │
      └── MERMAID_DIAGRAMS (flux)
```
