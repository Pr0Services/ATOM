# 🎯 CHENU V22+ - PLAN DE TÂCHES MAÎTRE

## 📊 SOMMAIRE EXÉCUTIF

| Métrique | Valeur |
|----------|--------|
| **Tâches Totales** | 215 |
| **Sprints Planifiés** | 12 |
| **Durée Estimée** | 24 semaines |
| **Score Cible** | 9.9/10 |

---

# PHASE 1: FONDATIONS (Semaines 1-4)

## Sprint 1.1 - Navigation & Structure (Sem 1-2)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| F1-01 | Réorganiser sidebar en 5 catégories (Core, Business, Outils, Système, Épinglés) | Navigation | 4h | ⬜ TODO |
| F1-02 | Implémenter section "Épinglés" personnalisable | Navigation | 3h | ⬜ TODO |
| F1-03 | Ajouter Breadcrumbs dynamiques sur toutes les pages | Navigation | 4h | ⬜ TODO |
| F1-04 | Améliorer Spotlight Search (⌘K) - recherche dans contenu | Navigation | 6h | ⬜ TODO |
| F1-05 | Créer page "Récents" avec historique navigation | Navigation | 3h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| F1-06 | Ajouter animations transitions entre pages | UX | 4h | ⬜ TODO |
| F1-07 | Implémenter skeleton loaders sur toutes les pages | UX | 3h | ⬜ TODO |
| F1-08 | Créer composant ErrorBoundary global | Core | 2h | ⬜ TODO |
| F1-09 | Ajouter mode "Compact" pour sidebar | Navigation | 2h | ⬜ TODO |
| F1-10 | Implémenter persistance état sidebar (localStorage) | Navigation | 1h | ⬜ TODO |

---

## Sprint 1.2 - Dashboard Amélioré (Sem 3-4)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| F2-01 | Widgets drag & drop avec React-Grid-Layout | Dashboard | 8h | ⬜ TODO |
| F2-02 | Widgets redimensionnables (1x1, 2x1, 2x2, 1x2) | Dashboard | 4h | ⬜ TODO |
| F2-03 | Sauvegarde layout personnalisé par utilisateur | Dashboard | 3h | ⬜ TODO |
| F2-04 | Widget "Alertes Critiques" avec clignotement | Dashboard | 3h | ⬜ TODO |
| F2-05 | Widget "Météo Chantiers" multi-sites | Dashboard | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| F2-06 | Graphiques interactifs avec drill-down | Dashboard | 6h | ⬜ TODO |
| F2-07 | Export dashboard en PNG/PDF | Dashboard | 3h | ⬜ TODO |
| F2-08 | Mode "Focus" - 1 widget plein écran | Dashboard | 2h | ⬜ TODO |
| F2-09 | Widgets par rôle (presets Chef/Gestionnaire/Admin) | Dashboard | 4h | ⬜ TODO |
| F2-10 | Refresh automatique configurable (30s/1m/5m) | Dashboard | 2h | ⬜ TODO |

---

# PHASE 2: MODULES CORE (Semaines 5-10)

## Sprint 2.1 - Projects Avancé (Sem 5-6)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| P1-01 | Templates projets (Résidentiel, Commercial, Réno, Infrastructure) | Projects | 6h | ⬜ TODO |
| P1-02 | Système de sous-projets / Phases | Projects | 8h | ⬜ TODO |
| P1-03 | Budget tracking intégré par projet | Projects | 6h | ⬜ TODO |
| P1-04 | Comparaison Estimé vs Réel avec graphiques | Projects | 4h | ⬜ TODO |
| P1-05 | Import projets depuis Excel/CSV | Projects | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| P1-06 | Duplication projet en 1 clic | Projects | 2h | ⬜ TODO |
| P1-07 | Archivage projets avec recherche archives | Projects | 3h | ⬜ TODO |
| P1-08 | Tags/Labels personnalisables | Projects | 3h | ⬜ TODO |
| P1-09 | Vue "Portfolio" - tous projets sur carte | Projects | 6h | ⬜ TODO |
| P1-10 | Notifications jalons/échéances | Projects | 3h | ⬜ TODO |

---

## Sprint 2.2 - Calendar Pro (Sem 7-8)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| C1-01 | Intégration Google Calendar API (sync bidirectionnelle) | Calendar | 8h | ⬜ TODO |
| C1-02 | Intégration Microsoft Outlook API | Calendar | 8h | ⬜ TODO |
| C1-03 | Vue "Équipe" - calendriers superposés | Calendar | 6h | ⬜ TODO |
| C1-04 | Réservation ressources (équipements, véhicules) | Calendar | 6h | ⬜ TODO |
| C1-05 | Événements récurrents avec exceptions | Calendar | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| C1-06 | Météo intégrée sur chaque jour | Calendar | 3h | ⬜ TODO |
| C1-07 | Temps de trajet automatique (Google Maps) | Calendar | 4h | ⬜ TODO |
| C1-08 | Invitations avec réponses (Accept/Decline/Maybe) | Calendar | 4h | ⬜ TODO |
| C1-09 | Vue Agenda (liste chronologique) | Calendar | 3h | ⬜ TODO |
| C1-10 | Intégration Calendly pour RDV clients | Calendar | 4h | ⬜ TODO |

---

## Sprint 2.3 - Team & RH (Sem 9-10)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| T1-01 | Organigramme visuel interactif | Team | 8h | ⬜ TODO |
| T1-02 | Indicateurs charge de travail par agent | Team | 4h | ⬜ TODO |
| T1-03 | Profil compétences/certifications par employé | Team | 6h | ⬜ TODO |
| T1-04 | Intégration CCQ API - validation cartes compétences | Team | 8h | ⬜ TODO |
| T1-05 | Chat direct avec agents depuis leur profil | Team | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| T1-06 | Planification automatique selon skills | Team | 6h | ⬜ TODO |
| T1-07 | Historique performance par employé | Team | 4h | ⬜ TODO |
| T1-08 | Intégration BambooHR API | Team | 6h | ⬜ TODO |
| T1-09 | Intégration Deputy API - scheduling | Team | 6h | ⬜ TODO |
| T1-10 | Export feuilles de temps pour paie | Team | 3h | ⬜ TODO |

---

# PHASE 3: COMMUNICATION (Semaines 11-14)

## Sprint 3.1 - Email Pro (Sem 11-12)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| E1-01 | Intégration Gmail API complète | Email | 8h | ⬜ TODO |
| E1-02 | Intégration Outlook/Microsoft Graph API | Email | 8h | ⬜ TODO |
| E1-03 | Composer email avec éditeur riche | Email | 6h | ⬜ TODO |
| E1-04 | Templates emails (Soumission, Suivi, Rappel, Facture) | Email | 4h | ⬜ TODO |
| E1-05 | Signatures multiples par contexte | Email | 3h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| E1-06 | Programmation envoi différé | Email | 3h | ⬜ TODO |
| E1-07 | Suivi ouvertures (tracking pixels) | Email | 4h | ⬜ TODO |
| E1-08 | Lier emails aux contacts CRM | Email | 4h | ⬜ TODO |
| E1-09 | Recherche avancée dans emails | Email | 3h | ⬜ TODO |
| E1-10 | Règles automatiques (filtres) | Email | 4h | ⬜ TODO |

---

## Sprint 3.2 - Communication Unifiée (Sem 13-14)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| COM-01 | Intégration Slack API | Communication | 6h | ⬜ TODO |
| COM-02 | Intégration Microsoft Teams API | Communication | 6h | ⬜ TODO |
| COM-03 | Intégration WhatsApp Business API | Communication | 8h | ⬜ TODO |
| COM-04 | Centre de notifications unifié | Communication | 6h | ⬜ TODO |
| COM-05 | Préférences notification par canal | Communication | 3h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| COM-06 | Intégration Zoom API - vidéoconférence | Communication | 4h | ⬜ TODO |
| COM-07 | Intégration Google Meet | Communication | 4h | ⬜ TODO |
| COM-08 | Chatbot basique pour infos projet | Communication | 8h | ⬜ TODO |
| COM-09 | Broadcast messages multi-canaux | Communication | 4h | ⬜ TODO |
| COM-10 | Historique communications par contact | Communication | 4h | ⬜ TODO |

---

# PHASE 4: FINANCE & BUSINESS (Semaines 15-18)

## Sprint 4.1 - Finance Avancée (Sem 15-16)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| FIN-01 | Intégration QuickBooks Online API | Finance | 10h | ⬜ TODO |
| FIN-02 | Intégration Sage API | Finance | 10h | ⬜ TODO |
| FIN-03 | Cash flow forecast (prévisions trésorerie) | Finance | 8h | ⬜ TODO |
| FIN-04 | Rapprochement bancaire automatique | Finance | 6h | ⬜ TODO |
| FIN-05 | Alertes seuils (solde bas, gros débit) | Finance | 3h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| FIN-06 | Intégration Stripe - paiements en ligne | Finance | 6h | ⬜ TODO |
| FIN-07 | Intégration Square - paiements terrain | Finance | 4h | ⬜ TODO |
| FIN-08 | Facturation automatique depuis projets | Finance | 6h | ⬜ TODO |
| FIN-09 | Suivi paiements clients avec relances | Finance | 4h | ⬜ TODO |
| FIN-10 | Export comptable multi-format | Finance | 3h | ⬜ TODO |

---

## Sprint 4.2 - Fournisseurs Multi-Sources (Sem 17-18)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| SUP-01 | Intégration RONA Pro API | Suppliers | 8h | ⬜ TODO |
| SUP-02 | Intégration Home Depot Pro API | Suppliers | 8h | ⬜ TODO |
| SUP-03 | Comparateur prix multi-fournisseurs | Suppliers | 6h | ⬜ TODO |
| SUP-04 | Listes de matériaux par type projet | Suppliers | 4h | ⬜ TODO |
| SUP-05 | Scan code-barre pour ajout panier | Suppliers | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| SUP-06 | Suivi livraisons temps réel | Suppliers | 6h | ⬜ TODO |
| SUP-07 | Historique commandes avec réachat rapide | Suppliers | 3h | ⬜ TODO |
| SUP-08 | Alertes stock bas projet | Suppliers | 3h | ⬜ TODO |
| SUP-09 | Intégration Patrick Morin API | Suppliers | 6h | ⬜ TODO |
| SUP-10 | Budget matériaux vs commandes | Suppliers | 4h | ⬜ TODO |

---

# PHASE 5: CONFORMITÉ QC (Semaines 19-20)

## Sprint 5.1 - Intégrations Gouvernementales

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| GOV-01 | Intégration CCQ API - cartes compétences | Conformité | 10h | ⬜ TODO |
| GOV-02 | Intégration CNESST API - santé-sécurité | Conformité | 10h | ⬜ TODO |
| GOV-03 | Intégration RBQ API - licences entrepreneurs | Conformité | 8h | ⬜ TODO |
| GOV-04 | Vérification automatique conformité employés | Conformité | 6h | ⬜ TODO |
| GOV-05 | Alertes expiration (cartes, licences, assurances) | Conformité | 4h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| GOV-06 | Intégration Revenu Québec - DAS | Conformité | 6h | ⬜ TODO |
| GOV-07 | Rapport conformité mensuel automatique | Conformité | 4h | ⬜ TODO |
| GOV-08 | Checklist inspection CNESST | Conformité | 4h | ⬜ TODO |
| GOV-09 | Gestion documents légaux (permis, assurances) | Conformité | 4h | ⬜ TODO |
| GOV-10 | Historique conformité par projet | Conformité | 3h | ⬜ TODO |

---

# PHASE 6: IA & AUTOMATISATION (Semaines 21-24)

## Sprint 6.1 - AI Lab Pro (Sem 21-22)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| AI-01 | Mode comparaison multi-modèles | AI Lab | 6h | ⬜ TODO |
| AI-02 | Bibliothèque prompts construction | AI Lab | 4h | ⬜ TODO |
| AI-03 | Génération documents automatique | AI Lab | 8h | ⬜ TODO |
| AI-04 | Intégration OpenAI Whisper - transcription | AI Lab | 6h | ⬜ TODO |
| AI-05 | Analyse de plans avec Vision API | AI Lab | 8h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| AI-06 | Résumé automatique réunions | AI Lab | 6h | ⬜ TODO |
| AI-07 | Suggestions proactives Nova 2.0 | AI Lab | 8h | ⬜ TODO |
| AI-08 | Détection anomalies budgets | AI Lab | 6h | ⬜ TODO |
| AI-09 | Prédiction délais projets | AI Lab | 8h | ⬜ TODO |
| AI-10 | Commandes vocales Nova | AI Lab | 6h | ⬜ TODO |

---

## Sprint 6.2 - Photos IA (Sem 23-24)

### 🔴 HAUTE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| PHO-01 | Intégration Google Cloud Vision | Photos | 6h | ⬜ TODO |
| PHO-02 | Détection IA défauts (fissures, moisissures) | Photos | 8h | ⬜ TODO |
| PHO-03 | Comparaison slider avant/après | Photos | 4h | ⬜ TODO |
| PHO-04 | Capture mobile avec GPS auto | Photos | 6h | ⬜ TODO |
| PHO-05 | Génération rapport photo automatique | Photos | 6h | ⬜ TODO |

### 🟡 MOYENNE PRIORITÉ
| ID | Tâche | Module | Effort | Status |
|----|-------|--------|--------|--------|
| PHO-06 | Organisation par phase projet | Photos | 3h | ⬜ TODO |
| PHO-07 | Tags automatiques IA | Photos | 4h | ⬜ TODO |
| PHO-08 | Mesures sur photo (AR) | Photos | 8h | ⬜ TODO |
| PHO-09 | Intégration CompanyCam API | Photos | 6h | ⬜ TODO |
| PHO-10 | Timelapse automatique chantier | Photos | 6h | ⬜ TODO |

---

# 📊 STATISTIQUES PLAN

## Par Phase
| Phase | Tâches | Heures | Semaines |
|-------|--------|--------|----------|
| Phase 1: Fondations | 20 | 68h | 4 |
| Phase 2: Modules Core | 30 | 142h | 6 |
| Phase 3: Communication | 20 | 102h | 4 |
| Phase 4: Finance | 20 | 108h | 4 |
| Phase 5: Conformité QC | 10 | 69h | 2 |
| Phase 6: IA | 20 | 124h | 4 |
| **TOTAL** | **120** | **613h** | **24** |

## Par Priorité
| Priorité | Tâches | % |
|----------|--------|---|
| 🔴 Haute | 60 | 50% |
| 🟡 Moyenne | 60 | 50% |

## Par Catégorie API
| Catégorie | APIs à Intégrer |
|-----------|-----------------|
| Construction | Procore, Autodesk, PlanGrid |
| Finance | QuickBooks, Sage, Stripe, Square |
| Communication | Gmail, Outlook, Slack, Teams, WhatsApp |
| Conformité | CCQ, CNESST, RBQ |
| Fournisseurs | BMR, RONA, Home Depot |
| IA | OpenAI, Google Vision, Whisper |

---

*Plan généré pour CHENU V22+ - Décembre 2024*
