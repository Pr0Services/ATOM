**SPÉCIFICATION DES AGENTS**

168 Agents IA --- Architecture Hiérarchique

CHE·NU v27 --- Governed Intelligence OS

1\. VUE D\'ENSEMBLE

CHE·NU utilise 168 agents IA organisés hiérarchiquement en 4 niveaux:

  ------------ ------------------- -------------- ---------------------------
  **Niveau**   **Type**            **Quantité**   **Fonction**

  **L0**       **NOVA**            1              Gouvernance, interface
                                                  utilisateur

  **L1**       **Orchestrators**   8              Coordination départementale

  **L2**       **Managers**        32             Gestion équipes
                                                  spécialisées

  **L3**       **Specialists**     127            Exécution tâches
                                                  spécifiques
  ------------ ------------------- -------------- ---------------------------

2\. L0 --- NOVA (Gouvernance)

*Nova est l\'agent principal de gouvernance. Il est l\'interface entre
l\'utilisateur et tous les autres agents. Aucune action n\'est exécutée
sans son approbation.*

Responsabilités

-   Recevoir et interpréter les demandes utilisateur

-   Expliquer les actions proposées avant exécution

-   Valider le consentement explicite

-   Déléguer aux Orchestrators appropriés

-   Rapporter les résultats à l\'utilisateur

Configuration Technique

  ---------------------- ------------------------------------------------
  **Paramètre**          **Valeur**

  LLM Principal          **Claude 3.5 Sonnet**

  Temperature            0.3 (conservateur)

  Max Tokens             4096

  Context Window         200k tokens
  ---------------------- ------------------------------------------------

3\. L1 --- ORCHESTRATORS (8 agents)

Les Orchestrators coordonnent les activités au sein de leur département
respectif:

  -------- ---------------------- ---------------------------------------------
  **\#**   **Orchestrator**       **Domaine**

  1        **ConstructionOrch**   Estimation, planification, suivi chantiers,
                                  conformité

  2        **FinanceOrch**        Comptabilité, facturation, budgets, rapports
                                  financiers

  3        **HROrch**             Recrutement, paie, conformité CCQ, formation

  4        **MarketingOrch**      Communication, réseaux sociaux, branding, SEO

  5        **SalesOrch**          CRM, soumissions, suivi clients, négociation

  6        **OpsOrch**            Logistique, inventaire, fournisseurs, achats

  7        **LegalOrch**          Contrats, conformité RBQ/CNESST, litiges

  8        **CreativeOrch**       Design, 3D, vidéo, photo (38 agents
                                  spécialisés)
  -------- ---------------------- ---------------------------------------------

4\. CREATIVE STUDIO (38 agents)

Le Creative Studio est le département le plus fourni avec 38 agents
spécialisés répartis en 7 studios:

  ------------------ ------------ -----------------------------------------
  **Studio**         **Agents**   **Spécialités**

  **Design Studio**  8            UI/UX, graphisme, identité visuelle,
                                  mockups

  **3D Studio**      6            Modélisation, rendus, visualisation
                                  architecture

  **Video Studio**   7            Montage, animation, motion design,
                                  sous-titres

  **Photo Studio**   4            Retouche, HDR, catalogues produits

  **Audio Studio**   4            Musique, sound design, voix-off, podcast

  **Writing Studio** 5            Copywriting, SEO, documentation,
                                  traduction

  **Web Studio**     4            Landing pages, emails, social media
                                  assets
  ------------------ ------------ -----------------------------------------

5\. EXEMPLES AGENTS L3 (Specialists)

Construction Department

-   **EstimationAgent:** Calcul des coûts matériaux et main-d\'œuvre

-   **PlanningAgent:** Création de calendriers de projet

-   **RBQComplianceAgent:** Vérification conformité RBQ

-   **CNESSTAgent:** Conformité santé-sécurité

-   **QualityControlAgent:** Inspections et rapports qualité

Finance Department

-   **InvoicingAgent:** Génération de factures

-   **BudgetAgent:** Suivi budgétaire par projet

-   **PayrollAgent:** Calcul paie et déductions

-   **TaxAgent:** Calcul TPS/TVQ, rapports fiscaux

Sales Department

-   **LeadScoringAgent:** Qualification des prospects

-   **QuoteGeneratorAgent:** Génération de soumissions

-   **FollowUpAgent:** Relances automatisées

-   **ContractDraftAgent:** Rédaction de contrats

--- Fin du Document ---

Total: 168 Agents \| 4 Niveaux \| 8 Départements
