**ARCHITECTURE TECHNIQUE**

CHE·NU v27 --- Governed Intelligence OS

Documentation Technique Complète

Version: 27.0.0

Date: 14 décembre 2025

1\. VUE D\'ENSEMBLE

1.1 Stack Technologique

  ------------------ ---------------------- ------------------------------
  **Couche**         **Technologie**        **Détails**

  Frontend           **React 18 +           Vite, TailwindCSS, Framer
                     TypeScript**           Motion

  State              **Zustand + React      Global state + Server state
                     Query**                

  Backend            **Python FastAPI**     Async, OpenAPI, Pydantic

  Database           **PostgreSQL +         Supabase hosted
                     Prisma**               

  Cache              **Redis (Upstash)**    Sessions, rate limiting

  AI/LLM             **Multi-LLM Router**   Claude, GPT-4, Gemini, Ollama

  Vector DB          **Pinecone**           RAG, embeddings, search
  ------------------ ---------------------- ------------------------------

1.2 Architecture 3 Zones

L\'interface utilisateur est organisée en 3 zones distinctes, chacune
avec une responsabilité claire:

  ------------------ --------------------- ----------------------------------
  **Zone**           **Composant**         **Responsabilité**

  **INTERACTION**    ZoneInteraction.tsx   Nova dialogue, gouvernance,
                                           validation actions

  **NAVIGATION**     ZoneNavigation.tsx    11 sphères, sélection contexte,
                                           agents

  **CONCEPTION**     ZoneConception.tsx    Documents, workspace, édition,
                                           versions
  ------------------ --------------------- ----------------------------------

2\. HIÉRARCHIE DES AGENTS IA

CHE·NU utilise une architecture hiérarchique de 168 agents organisés en
4 niveaux:

  ------------ ------------------- ------------------ -------------------------
  **Niveau**   **Nom**             **Quantité**       **Rôle**

  **L0**       **NOVA**            1                  Gouvernance, dialogue
                                                      utilisateur

  **L1**       **Orchestrators**   8                  Coordination par
                                                      département

  **L2**       **Managers**        32                 Gestion équipes
                                                      spécialisées

  **L3**       **Specialists**     127                Exécution tâches
                                                      spécifiques

  **TOTAL**                        **168**            
  ------------ ------------------- ------------------ -------------------------

2.2 Départements (8)

1.  **Construction:** Estimation, planification, suivi chantiers

2.  **Finance:** Comptabilité, facturation, budgets

3.  **RH:** Recrutement, paie, conformité CCQ

4.  **Marketing:** Communication, réseaux sociaux, branding

5.  **Ventes:** CRM, soumissions, suivi clients

6.  **Opérations:** Logistique, inventaire, fournisseurs

7.  **Juridique:** Contrats, conformité RBQ/CNESST

8.  **Creative Studio:** Design, 3D, vidéo, photo (38 agents)

3\. LES 11 SPHÈRES

Les sphères représentent les différents contextes de vie de
l\'utilisateur:

  -------- ------------------- ------------------------------------------------
  **\#**   **Sphère**          **Description**

  1        **Personnel**       Vie personnelle, bien-être, santé, développement

  2        **Social**          Loisirs, divertissement, vie sociale, événements

  3        **Scholar**         Éducation, formation continue, certifications

  4        **Maison**          Gestion du foyer, entretien, famille

  5        **Entreprise**      Pro-Service Construction - activité principale

  6        **Projets**         Gestion transversale de tous les projets

  7        **Creative Studio** Design, création multimédia, branding

  8        **Gouvernement**    Interactions services publics, permis, impôts

  9        **Immobilier**      Investissements, gestion propriétés

  10       **Associations**    OBNL, bénévolat, implication communautaire

  11       **Environnement**   Développement durable, éco-responsabilité
  -------- ------------------- ------------------------------------------------

4\. MODÈLE DE GOUVERNANCE

4.1 Le Canon de Gouvernance

*\"CHE·NU does not act for you. CHE·NU acts with you. CHE·NU acts only
when you decide.\"*

4.2 Tree Laws (Lois de l\'Arbre)

-   **Loi 1 - Consentement:** Aucune action sans approbation explicite

-   **Loi 2 - Transparence:** Nova explique chaque proposition

-   **Loi 3 - Réversibilité:** Toute action peut être annulée

-   **Loi 4 - Traçabilité:** Historique complet des actions

-   **Loi 5 - Hiérarchie:** Utilisateur \> Nova \> Orchestrator \> Agent

4.3 Flux de Validation

Chaque action suit un flux de validation en 5 étapes:

9.  **Proposition:** L\'agent propose une action

10. **Explication:** Nova explique le contexte et les impacts

11. **Confirmation:** L\'utilisateur approuve ou refuse

12. **Exécution:** Action exécutée avec logging

13. **Rapport:** Confirmation du résultat à l\'utilisateur

5\. STRUCTURE DES FICHIERS

5.1 Frontend (React)

frontend/src/ ├── App.tsx \# Point d\'entrée principal ├── components/ │
├── layout/ │ │ └── AppHeader.tsx \# Navigation 3 zones │ ├── zones/ │ │
├── ZoneInteraction.tsx │ │ ├── ZoneNavigation.tsx │ │ └──
ZoneConception.tsx │ └── Logo.tsx ├── hooks/ │ ├── useAuth.ts │ ├──
useNova.ts │ ├── useExpertMode.ts │ └── \... ├── features/ │ ├──
nova-avatar/ │ ├── orchestrator/ │ ├── voice/ │ └── meetings/ ├── pages/
│ ├── preaccount/ │ ├── auth/ │ └── \... └── stores/ └── appStore.ts

5.2 Backend (Python)

backend/ ├── main.py \# FastAPI entry point ├── api/ │ ├── routes/ │ │
├── auth.py │ │ ├── projects.py │ │ └── agents.py │ └── deps.py ├──
core/ │ ├── config.py │ ├── security.py │ └── database.py ├── models/ │
├── user.py │ ├── project.py │ └── agent.py ├── services/ │ ├── llm/ │ │
├── router.py │ │ ├── claude.py │ │ └── openai.py │ └── nova/ │ └──
governance.py └── utils/

--- Fin du Document ---

CHE·NU v27 --- Governed Intelligence OS

Pro-Service Construction • Brossard, Québec
