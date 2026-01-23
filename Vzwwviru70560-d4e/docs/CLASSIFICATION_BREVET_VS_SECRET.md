# CLASSIFICATION: BREVET vs SECRET D'ENTREPRISE

**Document Interne - NE PAS INCLURE DANS LE DEPOT DE BREVET**
**Date:** 23-01-2026
**Auteur:** Jonathan Emmanuel Rodrigue

---

## PRINCIPE DE BASE

| Protection | Duree | Divulgation | Quand l'utiliser |
|------------|-------|-------------|------------------|
| **Brevet** | 20 ans | Publique (obligatoire) | Innovation qu'un concurrent pourrait reverse-engineer |
| **Secret** | Illimitee | Jamais | Avantage competitif impossible a deduire du produit |

---

## CLASSIFICATION DES ELEMENTS AT-OM

### A BREVETER (Divulgation securitaire)

Ces elements sont visibles dans le produit final ou peuvent etre deduits par un concurrent:

| Element | Raison de breveter |
|---------|-------------------|
| Architecture tri-hub (Alpha/Core/Omega) | Visible dans l'interface |
| Navigation cardinale (N/S/E/W) | UX observable |
| Concept de frequences 111-999 Hz | Marketing public |
| Principe du Relais API centralise | Architecture deductible |
| Isolation database par membre | Pattern connu mais combinaison unique |
| Distribution automatique Stripe Connect | Fonctionnalite visible |
| Score de resonance (concept) | Affiche dans l'interface |

### A GARDER SECRET (Ne jamais divulguer)

Ces elements sont des avantages competitifs internes:

| Element | Raison de garder secret |
|---------|------------------------|
| **Algorithmes de calcul de resonance** | Formule exacte = avantage competitif |
| **Poids des facteurs de scoring** | Tuning interne impossible a deduire |
| **Seuils de qualification energetique** | Criteres business confidentiels |
| **Cles API et credentials** | Securite evidente |
| **Regles de routage detaillees** | Logique business proprietary |
| **Mapping exact modele/tache** | Optimisation interne |
| **Pourcentages de distribution exacts** | Negociations commerciales |
| **Noms des partenaires Stripe Connect** | Relations d'affaires |
| **Structure de couts API** | Avantage pricing |
| **Metriques de performance internes** | Benchmarks proprietaires |

---

## ANALYSE PAR EXHIBIT

### EXHIBIT A - White Paper (A REVISER)

**A GARDER:**
- Architecture generale tri-hub
- Concept d'Arithmos (encodage frequentiel)
- Principe des 12 noeuds de resonance
- Protocole Heartbeat 444 Hz
- Concept de coherence spectrale

**A RETIRER:**
- Code Python detaille des algorithmes
- Formules mathematiques exactes de coherence
- Parametres de configuration (Q_factor, thresholds)
- Implementation complete du DiamondTransmuter
- Details de l'ErrorCorrectionProtocol

### EXHIBIT B - Sovereign Grid SQL (A REVISER)

**A GARDER:**
- Structure des tables (noms, colonnes principales)
- Concept de RLS par membre
- Principe des fonctions RPC

**A RETIRER:**
- Formule exacte de calcul de resonance
- Poids des facteurs (25 points chaque)
- Seuils de completion (25%, 50%, 75%, 100%)
- Pourcentages de distribution par defaut
- Implementation detaillee des fonctions

### EXHIBIT C - API Usage (A REVISER)

**A GARDER:**
- Concept de quotas par utilisateur
- Structure de suivi d'usage
- Principe des plans d'abonnement

**A RETIRER:**
- Quotas exacts (50K, 500K tokens)
- Prix exacts (99$/mois)
- Formules de calcul de credits

### EXHIBIT D - API Router (A RETIRER COMPLETEMENT)

**DANGER:** Ce fichier contient toute la logique de routage proprietary.

- Mapping modele/tache = SECRET
- Logique de selection Cost vs Power = SECRET
- Seuils de complexite (L0-L9) = SECRET
- Integration providers = SECRET

**Action:** Remplacer par une description de haut niveau sans code.

### EXHIBIT E - Setup Wizard (A REVISER)

**A GARDER:**
- Concept d'interface de configuration
- Principe d'indicateur de frequence
- Structure en etapes

**A RETIRER:**
- Code source complet
- Mapping frequence/completion exact
- Logique de validation des APIs

### EXHIBITS F, G, H (PHILOSOPHIQUES - OK)

Ces documents sont principalement conceptuels et peuvent etre inclus car ils ne revelent pas d'implementation technique sensible.

---

## ACTIONS RECOMMANDEES

### 1. Creer des versions "sanitisees" des exhibits

Pour chaque exhibit technique, creer une version qui:
- Decrit le QUOI (fonctionnalite) sans le COMMENT (implementation)
- Utilise des diagrammes de flux au lieu de code
- Remplace les valeurs exactes par "[VALEUR CONFIDENTIELLE]"

### 2. Retirer EXHIBIT D completement

L'API Router est trop sensible. Le remplacer par un diagramme de flux decrivant:
- Input: Requete utilisateur
- Process: Selection de modele (sans details)
- Output: Reponse

### 3. Creer un document de secrets d'entreprise

Un document interne listant tous les secrets avec leur justification, stocke de maniere securisee (pas sur GitHub public).

### 4. Reviser les Claims du brevet

S'assurer que les claims protegent le concept sans reveler l'implementation:
- ❌ "Utilisant un Q_factor de 10.0 et un seuil de 0.618"
- ✅ "Utilisant un filtre de resonance configurable"

---

## DOCUMENTS A CREER

1. `PATENT_EXHIBITS_SANITIZED/` - Versions nettoyees pour depot
2. `TRADE_SECRETS_CONFIDENTIAL.md` - Document interne (pas sur Git)
3. `PATENT_CLAIMS_REVISED.md` - Claims revises sans details sensibles

---

## RAPPEL LEGAL

- Un brevet divulgue TOUT ce qui est claim
- Un secret d'entreprise perd sa protection si divulgue
- Ne JAMAIS mettre de secrets dans un depot de brevet
- Les claims doivent etre assez specifiques pour etre defendables mais assez generaux pour ne pas reveler les secrets

---

**DECISION FINALE:**

| Document | Action |
|----------|--------|
| Brevet principal | Garder, reviser les details techniques |
| Exhibit A | Creer version sanitisee (sans code) |
| Exhibit B | Creer version sanitisee (structure seulement) |
| Exhibit C | Creer version sanitisee (concept seulement) |
| Exhibit D | RETIRER - trop sensible |
| Exhibit E | Creer version sanitisee (sans code) |
| Exhibit F | Garder tel quel |
| Exhibit G | Garder tel quel |
| Exhibit H | Garder tel quel |

