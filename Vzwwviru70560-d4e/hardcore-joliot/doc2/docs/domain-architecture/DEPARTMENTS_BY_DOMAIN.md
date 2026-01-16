# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — DEPARTMENTS BY DOMAIN
# Complete Department Definitions
# ═══════════════════════════════════════════════════════════════════════════════

**Version**: 1.0.0
**Status**: CANONICAL

---

## 👤 PERSONAL DOMAIN DEPARTMENTS

### Department: Identity
```yaml
code: personal.identity
name: Identity Management
name_fr: Gestion de l'Identité
workflows:
  - Profile management
  - Credential storage
  - Identity verification
apis:
  - Identity_API
  - Credential_Store
  - Verification_API
kpis:
  - Profile completeness
  - Security score
agents:
  - Identity_Guardian
```

### Department: Health
```yaml
code: personal.health
name: Health & Wellness
name_fr: Santé et Bien-être
workflows:
  - Health tracking
  - Wellness monitoring
  - Medical records
apis:
  - Health_API
  - Fitness_API
  - Medical_Records
kpis:
  - Health score
  - Activity level
  - Sleep quality
agents:
  - Health_Monitor
  - Wellness_Coach
```

### Department: Memory
```yaml
code: personal.memory
name: Personal Memory
name_fr: Mémoire Personnelle
workflows:
  - Memory capture
  - Memory organization
  - Memory recall
apis:
  - Memory_API
  - Recall_API
kpis:
  - Memory organization score
  - Recall accuracy
agents:
  - Memory_Curator
```

### Department: Finance Personal
```yaml
code: personal.finance
name: Personal Finance
name_fr: Finances Personnelles
workflows:
  - Budget tracking
  - Expense management
  - Savings goals
apis:
  - Budget_API
  - Banking_Personal
kpis:
  - Budget adherence
  - Savings rate
agents:
  - Budget_Agent
```

### Department: Journal
```yaml
code: personal.journal
name: Personal Journal
name_fr: Journal Personnel
workflows:
  - Daily entries
  - Reflection
  - Goal tracking
apis:
  - Journal_API
  - Goals_API
kpis:
  - Entry frequency
  - Reflection depth
agents:
  - Journal_Agent
```

---

## 💼 BUSINESS DOMAIN DEPARTMENTS

### Department: Sales
```yaml
code: business.sales
name: Sales
name_fr: Ventes
workflows:
  - Lead capture
  - Pipeline management
  - Closing deals
  - Follow-up
apis:
  - CRM_API
  - Calendar_API
  - Communication_API
kpis:
  - Conversion rate
  - Revenue
  - Sales cycle time
  - Win rate
agents:
  - Sales_Agent
  - CRM_Agent
  - Lead_Scorer
```

### Department: Accounting
```yaml
code: business.accounting
name: Accounting
name_fr: Comptabilité
workflows:
  - Invoicing
  - Reconciliation
  - Financial reporting
  - Tax preparation
apis:
  - Invoicing_API
  - Banking_API
  - Tax_API
  - Reporting_API
kpis:
  - AR days
  - Cash flow
  - Accuracy rate
agents:
  - Accounting_Agent
  - Invoice_Agent
  - Reconciliation_Agent
```

### Department: Operations
```yaml
code: business.operations
name: Operations
name_fr: Opérations
workflows:
  - Project scheduling
  - Resource allocation
  - Quality control
  - Delivery management
apis:
  - Project_API
  - Resource_API
  - QC_API
  - Inventory_API
kpis:
  - Efficiency
  - Utilization rate
  - On-time delivery
agents:
  - Project_Agent
  - Resource_Agent
  - QC_Agent
```

### Department: HR
```yaml
code: business.hr
name: Human Resources
name_fr: Ressources Humaines
workflows:
  - Recruitment
  - Onboarding
  - Performance management
  - Payroll
apis:
  - Recruitment_API
  - Onboarding_API
  - Payroll_API
  - Performance_API
kpis:
  - Time to hire
  - Retention rate
  - Employee satisfaction
agents:
  - HR_Agent
  - Onboarding_Agent
  - Performance_Agent
```

### Department: Marketing
```yaml
code: business.marketing
name: Marketing
name_fr: Marketing
workflows:
  - Campaign management
  - Content creation
  - Analytics
  - Brand management
apis:
  - Campaign_API
  - Analytics_API
  - Content_API
kpis:
  - ROI
  - Engagement rate
  - Brand awareness
agents:
  - Marketing_Agent
  - Analytics_Agent
```

### Department: Estimating (Construction)
```yaml
code: business.estimating
name: Estimating
name_fr: Estimation
workflows:
  - Quantity takeoffs
  - Cost estimation
  - Bid preparation
apis:
  - Estimating_API
  - Material_Database
  - Supplier_API
kpis:
  - Bid accuracy
  - Win rate
  - Estimation time
agents:
  - Estimating_Agent
  - Quantity_Agent
```

---

## 📚 SCHOLAR DOMAIN DEPARTMENTS

### Department: Learning
```yaml
code: scholar.learning
name: Learning Paths
name_fr: Parcours d'Apprentissage
workflows:
  - Course enrollment
  - Progress tracking
  - Assessment
  - Certification
apis:
  - Learning_API
  - Assessment_API
  - Certification_API
kpis:
  - Completion rate
  - Assessment scores
  - Time to mastery
agents:
  - Tutor_Agent
  - Progress_Agent
```

### Department: Research
```yaml
code: scholar.research
name: Research
name_fr: Recherche
workflows:
  - Literature review
  - Data collection
  - Analysis
  - Publication
apis:
  - Citation_API
  - Database_API
  - Analysis_API
kpis:
  - Sources reviewed
  - Research depth
  - Output quality
agents:
  - Research_Agent
  - Citation_Agent
```

### Department: Knowledge
```yaml
code: scholar.knowledge
name: Knowledge Management
name_fr: Gestion des Connaissances
workflows:
  - Knowledge capture
  - Organization
  - Retrieval
  - Sharing
apis:
  - Knowledge_Graph_API
  - Search_API
  - Tagging_API
kpis:
  - Knowledge coverage
  - Retrieval accuracy
  - Update frequency
agents:
  - Knowledge_Curator
  - Tagging_Agent
```

---

## 🎨 CREATIVE DOMAIN DEPARTMENTS

### Department: Visual
```yaml
code: creative.visual
name: Visual Arts
name_fr: Arts Visuels
workflows:
  - Concept development
  - Image generation
  - Editing
  - Export
apis:
  - Image_Gen_API
  - Editing_API
  - Asset_API
kpis:
  - Output quality
  - Generation speed
  - Revision count
agents:
  - Render_Agent
  - Visual_Agent
```

### Department: Audio
```yaml
code: creative.audio
name: Audio Production
name_fr: Production Audio
workflows:
  - Composition
  - Recording
  - Mixing
  - Mastering
apis:
  - Audio_Gen_API
  - Mixing_API
  - Audio_Asset_API
kpis:
  - Quality score
  - Production time
agents:
  - Audio_Agent
  - Mixing_Agent
```

### Department: Video
```yaml
code: creative.video
name: Video Production
name_fr: Production Vidéo
workflows:
  - Storyboarding
  - Shooting/Generation
  - Editing
  - Post-production
apis:
  - Video_Gen_API
  - Editing_API
  - Effects_API
kpis:
  - Production quality
  - Delivery time
agents:
  - Video_Agent
  - Editor_Agent
```

### Department: Writing
```yaml
code: creative.writing
name: Creative Writing
name_fr: Écriture Créative
workflows:
  - Ideation
  - Drafting
  - Editing
  - Publishing
apis:
  - Text_Gen_API
  - Grammar_API
  - Publishing_API
kpis:
  - Word count
  - Quality score
  - Engagement
agents:
  - Writing_Agent
  - Editor_Agent
```

---

## 📱 SOCIAL DOMAIN DEPARTMENTS

### Department: Platforms
```yaml
code: social.platforms
name: Social Platforms
name_fr: Plateformes Sociales
workflows:
  - Account management
  - Posting
  - Engagement
  - Analytics
apis:
  - Platform_APIs (Twitter, LinkedIn, Instagram, etc.)
  - Analytics_API
kpis:
  - Followers
  - Engagement rate
  - Reach
agents:
  - Social_Poster
  - Platform_Agent
```

### Department: Community
```yaml
code: social.community
name: Community Management
name_fr: Gestion de Communauté
workflows:
  - Community building
  - Moderation
  - Event organization
  - Member support
apis:
  - Community_API
  - Moderation_API
  - Event_API
kpis:
  - Community growth
  - Engagement
  - Retention
agents:
  - Community_Agent
  - Moderation_Agent
```

### Department: Content
```yaml
code: social.content
name: Content Strategy
name_fr: Stratégie de Contenu
workflows:
  - Content planning
  - Creation
  - Scheduling
  - Performance analysis
apis:
  - Content_API
  - Scheduling_API
  - Analytics_API
kpis:
  - Content output
  - Engagement
  - Virality
agents:
  - Content_Agent
  - Trend_Analyzer
```

---

## 🏛️ INSTITUTIONAL DOMAIN DEPARTMENTS

### Department: Compliance
```yaml
code: institutional.compliance
name: Compliance
name_fr: Conformité
workflows:
  - Regulation monitoring
  - Compliance checking
  - Gap analysis
  - Remediation
apis:
  - Compliance_Check_API
  - Regulation_Database
  - Audit_API
kpis:
  - Compliance score
  - Gap count
  - Remediation time
agents:
  - Compliance_Agent
  - Regulation_Agent
constraints:
  - RBQ compliance (Quebec)
  - CNESST compliance
  - CCQ compliance
```

### Department: Audit
```yaml
code: institutional.audit
name: Audit
name_fr: Audit
workflows:
  - Audit planning
  - Evidence collection
  - Assessment
  - Reporting
apis:
  - Audit_API
  - Evidence_API
  - Reporting_API
kpis:
  - Audit coverage
  - Finding severity
  - Resolution rate
agents:
  - Audit_Agent
  - Evidence_Agent
```

### Department: Governance
```yaml
code: institutional.governance
name: Governance
name_fr: Gouvernance
workflows:
  - Policy management
  - Decision tracking
  - Board management
apis:
  - Policy_API
  - Board_API
  - Decision_API
kpis:
  - Policy adherence
  - Decision quality
agents:
  - Governance_Agent
  - Policy_Agent
```

---

## ⚙️ METHODOLOGY DOMAIN DEPARTMENTS

### Department: Frameworks
```yaml
code: methodology.frameworks
name: Framework Library
name_fr: Bibliothèque de Cadres
workflows:
  - Framework selection
  - Application
  - Evaluation
apis:
  - Framework_API
  - Template_API
kpis:
  - Framework usage
  - Success rate
agents:
  - Methodology_Agent
```

### Department: Process
```yaml
code: methodology.process
name: Process Optimization
name_fr: Optimisation des Processus
workflows:
  - Process mapping
  - Analysis
  - Optimization
  - Implementation
apis:
  - Process_API
  - Analysis_API
kpis:
  - Process efficiency
  - Improvement rate
agents:
  - Process_Agent
  - Optimization_Agent
```

### Department: Strategy
```yaml
code: methodology.strategy
name: Strategy
name_fr: Stratégie
workflows:
  - Strategic planning
  - Scenario analysis
  - Decision support
apis:
  - Strategy_API
  - Scenario_API
kpis:
  - Strategic alignment
  - Decision quality
agents:
  - Strategy_Agent
  - Decision_Agent
```

---

## 🥽 XR DOMAIN DEPARTMENTS

### Department: Meetings
```yaml
code: xr.meetings
name: XR Meetings
name_fr: Réunions XR
workflows:
  - Session setup
  - Immersive collaboration
  - Recording
  - Sync to MR-2D
apis:
  - XR_Meeting_API
  - Sync_API
  - Recording_API
kpis:
  - Session quality
  - Sync success rate
  - Presence score
agents:
  - XR_Meeting_Agent
  - Presence_Agent
```

### Department: Visualization
```yaml
code: xr.visualization
name: Spatial Visualization
name_fr: Visualisation Spatiale
workflows:
  - 3D model loading
  - Spatial navigation
  - Annotation
  - Export
apis:
  - Rendering_API
  - Model_API
  - Annotation_API
kpis:
  - Render quality
  - Performance
  - Annotation accuracy
agents:
  - Spatial_Agent
  - Render_Agent
```

### Department: Replay
```yaml
code: xr.replay
name: Session Replay
name_fr: Relecture de Session
workflows:
  - Session recording
  - Replay
  - Analysis
  - Export to 2D
apis:
  - Recording_API
  - Replay_API
  - Export_API
kpis:
  - Recording quality
  - Replay fidelity
agents:
  - Replay_Agent
```

---

## DATABASE INSERT

```sql
-- Insert all departments
INSERT INTO core.departments (domain_code, code, name, name_fr, workflows, available_apis)
VALUES
-- Personal
('PERSONAL', 'personal.identity', 'Identity Management', 'Gestion de l''Identité', 
 ARRAY['Profile management', 'Credential storage', 'Identity verification'],
 ARRAY['Identity_API', 'Credential_Store', 'Verification_API']),
('PERSONAL', 'personal.health', 'Health & Wellness', 'Santé et Bien-être',
 ARRAY['Health tracking', 'Wellness monitoring', 'Medical records'],
 ARRAY['Health_API', 'Fitness_API', 'Medical_Records']),
('PERSONAL', 'personal.memory', 'Personal Memory', 'Mémoire Personnelle',
 ARRAY['Memory capture', 'Memory organization', 'Memory recall'],
 ARRAY['Memory_API', 'Recall_API']),
('PERSONAL', 'personal.finance', 'Personal Finance', 'Finances Personnelles',
 ARRAY['Budget tracking', 'Expense management', 'Savings goals'],
 ARRAY['Budget_API', 'Banking_Personal']),
('PERSONAL', 'personal.journal', 'Personal Journal', 'Journal Personnel',
 ARRAY['Daily entries', 'Reflection', 'Goal tracking'],
 ARRAY['Journal_API', 'Goals_API']),

-- Business
('BUSINESS', 'business.sales', 'Sales', 'Ventes',
 ARRAY['Lead capture', 'Pipeline management', 'Closing deals', 'Follow-up'],
 ARRAY['CRM_API', 'Calendar_API', 'Communication_API']),
('BUSINESS', 'business.accounting', 'Accounting', 'Comptabilité',
 ARRAY['Invoicing', 'Reconciliation', 'Financial reporting', 'Tax preparation'],
 ARRAY['Invoicing_API', 'Banking_API', 'Tax_API', 'Reporting_API']),
('BUSINESS', 'business.operations', 'Operations', 'Opérations',
 ARRAY['Project scheduling', 'Resource allocation', 'Quality control', 'Delivery management'],
 ARRAY['Project_API', 'Resource_API', 'QC_API', 'Inventory_API']),
('BUSINESS', 'business.hr', 'Human Resources', 'Ressources Humaines',
 ARRAY['Recruitment', 'Onboarding', 'Performance management', 'Payroll'],
 ARRAY['Recruitment_API', 'Onboarding_API', 'Payroll_API', 'Performance_API']),
('BUSINESS', 'business.marketing', 'Marketing', 'Marketing',
 ARRAY['Campaign management', 'Content creation', 'Analytics', 'Brand management'],
 ARRAY['Campaign_API', 'Analytics_API', 'Content_API']),
('BUSINESS', 'business.estimating', 'Estimating', 'Estimation',
 ARRAY['Quantity takeoffs', 'Cost estimation', 'Bid preparation'],
 ARRAY['Estimating_API', 'Material_Database', 'Supplier_API']),

-- Scholar
('SCHOLAR', 'scholar.learning', 'Learning Paths', 'Parcours d''Apprentissage',
 ARRAY['Course enrollment', 'Progress tracking', 'Assessment', 'Certification'],
 ARRAY['Learning_API', 'Assessment_API', 'Certification_API']),
('SCHOLAR', 'scholar.research', 'Research', 'Recherche',
 ARRAY['Literature review', 'Data collection', 'Analysis', 'Publication'],
 ARRAY['Citation_API', 'Database_API', 'Analysis_API']),
('SCHOLAR', 'scholar.knowledge', 'Knowledge Management', 'Gestion des Connaissances',
 ARRAY['Knowledge capture', 'Organization', 'Retrieval', 'Sharing'],
 ARRAY['Knowledge_Graph_API', 'Search_API', 'Tagging_API']),

-- Creative
('CREATIVE', 'creative.visual', 'Visual Arts', 'Arts Visuels',
 ARRAY['Concept development', 'Image generation', 'Editing', 'Export'],
 ARRAY['Image_Gen_API', 'Editing_API', 'Asset_API']),
('CREATIVE', 'creative.audio', 'Audio Production', 'Production Audio',
 ARRAY['Composition', 'Recording', 'Mixing', 'Mastering'],
 ARRAY['Audio_Gen_API', 'Mixing_API', 'Audio_Asset_API']),
('CREATIVE', 'creative.video', 'Video Production', 'Production Vidéo',
 ARRAY['Storyboarding', 'Shooting/Generation', 'Editing', 'Post-production'],
 ARRAY['Video_Gen_API', 'Editing_API', 'Effects_API']),
('CREATIVE', 'creative.writing', 'Creative Writing', 'Écriture Créative',
 ARRAY['Ideation', 'Drafting', 'Editing', 'Publishing'],
 ARRAY['Text_Gen_API', 'Grammar_API', 'Publishing_API']),

-- Social
('SOCIAL', 'social.platforms', 'Social Platforms', 'Plateformes Sociales',
 ARRAY['Account management', 'Posting', 'Engagement', 'Analytics'],
 ARRAY['Platform_APIs', 'Analytics_API']),
('SOCIAL', 'social.community', 'Community Management', 'Gestion de Communauté',
 ARRAY['Community building', 'Moderation', 'Event organization', 'Member support'],
 ARRAY['Community_API', 'Moderation_API', 'Event_API']),
('SOCIAL', 'social.content', 'Content Strategy', 'Stratégie de Contenu',
 ARRAY['Content planning', 'Creation', 'Scheduling', 'Performance analysis'],
 ARRAY['Content_API', 'Scheduling_API', 'Analytics_API']),

-- Institutional
('INSTITUTIONAL', 'institutional.compliance', 'Compliance', 'Conformité',
 ARRAY['Regulation monitoring', 'Compliance checking', 'Gap analysis', 'Remediation'],
 ARRAY['Compliance_Check_API', 'Regulation_Database', 'Audit_API']),
('INSTITUTIONAL', 'institutional.audit', 'Audit', 'Audit',
 ARRAY['Audit planning', 'Evidence collection', 'Assessment', 'Reporting'],
 ARRAY['Audit_API', 'Evidence_API', 'Reporting_API']),
('INSTITUTIONAL', 'institutional.governance', 'Governance', 'Gouvernance',
 ARRAY['Policy management', 'Decision tracking', 'Board management'],
 ARRAY['Policy_API', 'Board_API', 'Decision_API']),

-- Methodology
('METHODOLOGY', 'methodology.frameworks', 'Framework Library', 'Bibliothèque de Cadres',
 ARRAY['Framework selection', 'Application', 'Evaluation'],
 ARRAY['Framework_API', 'Template_API']),
('METHODOLOGY', 'methodology.process', 'Process Optimization', 'Optimisation des Processus',
 ARRAY['Process mapping', 'Analysis', 'Optimization', 'Implementation'],
 ARRAY['Process_API', 'Analysis_API']),
('METHODOLOGY', 'methodology.strategy', 'Strategy', 'Stratégie',
 ARRAY['Strategic planning', 'Scenario analysis', 'Decision support'],
 ARRAY['Strategy_API', 'Scenario_API']),

-- XR
('XR', 'xr.meetings', 'XR Meetings', 'Réunions XR',
 ARRAY['Session setup', 'Immersive collaboration', 'Recording', 'Sync to MR-2D'],
 ARRAY['XR_Meeting_API', 'Sync_API', 'Recording_API']),
('XR', 'xr.visualization', 'Spatial Visualization', 'Visualisation Spatiale',
 ARRAY['3D model loading', 'Spatial navigation', 'Annotation', 'Export'],
 ARRAY['Rendering_API', 'Model_API', 'Annotation_API']),
('XR', 'xr.replay', 'Session Replay', 'Relecture de Session',
 ARRAY['Session recording', 'Replay', 'Analysis', 'Export to 2D'],
 ARRAY['Recording_API', 'Replay_API', 'Export_API']);
```

---

**END OF DEPARTMENTS BY DOMAIN**

*CHE·NU Canonical Architecture*
*Pro-Service Construction*
