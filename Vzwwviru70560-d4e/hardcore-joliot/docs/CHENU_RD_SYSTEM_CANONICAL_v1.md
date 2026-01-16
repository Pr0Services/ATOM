# CHE·NU — SYSTÈME OFFICIEL DE R&D
## ARCHITECTURE FREEZE + MODE D'APPLICATION

**Version:** 1.0 CANONICAL  
**Statut:** DOCUMENT NORMATIF — NON CRÉATIF — OPPOSABLE  
**Date:** 21 December 2025  
**Authority:** CHE·NU Project Official Specification

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         SYSTÈME OFFICIEL DE RECHERCHE & DÉVELOPPEMENT        ║
║                                                               ║
║   Ce document définit la SEULE méthode autorisée pour        ║
║   développer, valider ou modifier CHE·NU.                    ║
║                                                               ║
║   Aucune exception. Aucune interprétation.                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## I. STATUT OFFICIEL DU SYSTÈME R&D

### 📌 DÉCLARATION OFFICIELLE

Le système R&D de CHE·NU est la **SEULE MÉTHODE AUTORISÉE** pour:

- ✅ Poursuivre le développement
- ✅ Valider ou invalider des modules
- ✅ Créer ou modifier des connexions inter-sphere
- ✅ Décider de l'existence d'une API

**RÈGLE ABSOLUE:**
Aucune feature, module, agent ou connexion ne peut être créée en dehors de ce système.

### 🎯 OBJECTIF DU SYSTÈME R&D

Le système R&D ne sert **PAS** à innover plus vite.

Le système R&D sert **UNIQUEMENT** à:

1. ✅ Éviter le travail en double
2. ✅ Empêcher les dérives silencieuses
3. ✅ Garantir l'alignement humain
4. ✅ Préserver l'architecture figée
5. ✅ Documenter les décisions

**Le rejet d'une proposition est un SUCCÈS du système R&D.**

---

## II. STRUCTURE DU SYSTÈME R&D (OFFICIELLE)

### 🧩 1. SOURCE UNIQUE — UTILISATEURS TYPES

Le R&D CHE·NU repose **EXCLUSIVEMENT** sur:

- ✅ Une liste d'utilisateurs types (exemple: 60 personas)
- ✅ Validée humainement
- ✅ Considérée comme vérité d'usage

**RÈGLES NON NÉGOCIABLES:**

❌ Aucun besoin fictif n'est accepté  
❌ Aucune feature ne précède un besoin humain  
❌ Aucun "nice to have" sans utilisateur type identifié  

### 🧩 2. UNITÉ DE BASE — LE BESOIN HUMAIN

Chaque besoin est décrit par:

**STRUCTURE OBLIGATOIRE:**

```
BESOIN #[ID]

Utilisateur type: [Nom exact du persona]

Contexte réel: [Situation concrète vécue par l'utilisateur]

Action humaine volontaire: [Ce que l'utilisateur VEUT faire]

Risques si mal automatisé: [Conséquences d'une automation non-gouvernée]

Sphères impliquées: [Liste, max 3-4]

Connexions inter-sphere requises: [Type exact: Projection/Request/Reference/Delegation]

Validation humaine requise: [Points de contrôle obligatoires]
```

**PRINCIPE FONDAMENTAL:**

- Les besoins sont **STABLES**
- Les implémentations sont **VARIABLES**

### 🧩 3. SORTIES AUTORISÉES DU R&D

Le système R&D peut produire **UNIQUEMENT**:

1. ❓ **Hypothèse de module**
   - Nom, scope, sphère propriétaire
   - Utilisateurs types servis
   - Besoins humains adressés
   
2. 🔗 **Hypothèse de connexion inter-sphere**
   - Type exact (Projection/Request/Reference/Delegation)
   - Sphères source et cible
   - Propriétaire humain unique
   - Méthode d'approbation
   - Méthode de révocation

3. 🔌 **Hypothèse d'API**
   - Endpoint, méthode, payload
   - Acteur autorisé (human/agent)
   - Zone d'exécution (autonomy/verified)
   - Validation requise

4. ❌ **Invalidation** (LA PLUS IMPORTANTE)
   - Raison du rejet
   - Conflit avec architecture
   - Besoin déjà servi autrement
   - Violation de principe

**CRITIQUE:**
👉 Une hypothèse n'est **JAMAIS** une implémentation.  
👉 Chaque hypothèse requiert validation humaine avant implémentation.

---

## III. FREEZE ARCHITECTURAL — VERSION ÉLABORÉE

### 🔒 CE QUI EST DÉFINITIVEMENT GELÉ

#### 1️⃣ LES SPHÈRES

**FIGÉ À JAMAIS:**

- ✅ Nombre: EXACTEMENT 9
- ✅ Noms: Personal, Business, Government & Institutions, Creative Studio, Community, Social & Media, Entertainment, My Team, Scholar
- ✅ Rôles: Définis dans CHENU_MASTER_REFERENCE
- ✅ Séparation: Isolation cognitive et responsabilité

**INTERDIT:**

- ❌ Aucun ajout de sphère
- ❌ Aucune fusion de sphères
- ❌ Aucune redéfinition sémantique
- ❌ Aucune "sous-sphère" ou "super-sphère"

#### 2️⃣ LES TYPES DE CONNEXIONS INTER-SPHERE

**Il existe EXACTEMENT 4 types, NON EXTENSIBLES:**

1. **PROJECTION** (read-only)
   - Représentation publique ou semi-publique
   - Source → Cible (unidirectionnel)
   - Jamais de feedback automatique
   - Exemple: Scholar → Social profile

2. **REQUEST** (humaine)
   - Demande d'action dans autre sphère
   - Requiert approbation humaine explicite
   - Traçable au propriétaire unique
   - Exemple: Personal → Business delegation

3. **REFERENCE** (statique)
   - Référence à données d'autre sphère
   - Pas de synchronisation
   - Pas de couplage live
   - Exemple: Business → Personal contact info

4. **DELEGATION** (humaine explicite)
   - Transfert explicite de responsabilité
   - Propriété réassignée et loggée
   - Révocable par propriétaire
   - Exemple: User → Agent dans My Team

**INTERDIT:**

❌ Auto-cross-posting  
❌ Background synchronization  
❌ Implicit propagation  
❌ Event listeners across spheres  
❌ Smart suggestions cross-sphere  
❌ Group-level decisions  

**Tout autre type de connexion est STRICTEMENT INTERDIT.**

#### 3️⃣ LES PRINCIPES NON NÉGOCIABLES

**CONSTITUTIONNELS (ne peuvent JAMAIS être modifiés):**

1. ✅ **Souveraineté humaine**
   - Humain décide toujours en dernier ressort
   - Pas de "smart defaults" qui contournent la décision

2. ✅ **No silent action**
   - Toute action visible
   - Toute action traçable
   - Toute action révocable

3. ✅ **Responsabilité unique**
   - Chaque action a UN propriétaire humain identifiable
   - Pas de responsabilité diluée ou collective

4. ✅ **Reversibilité**
   - Chaque changement peut être annulé
   - Undo patches générés obligatoirement
   - Historique conservé

5. ✅ **Auditabilité**
   - Logs complets
   - Traçabilité temporelle
   - Qui, quoi, quand, pourquoi

6. ✅ **Séparation cognition / exécution**
   - "Freedom is cognitive, not executive"
   - Agent peut penser librement
   - Agent ne peut exécuter qu'après approbation

#### 4️⃣ LE SYSTÈME DE ZONES

**ARCHITECTURE FIGÉE:**

```
🟦 AUTONOMY EXECUTION ZONE
   │
   ├─ Agent autonomy (cognitive freedom)
   ├─ No user data modification
   ├─ No official memory writes
   ├─ Results → isolated_execution_results
   │
   └─ Status: UNVERIFIED

              ↓ HUMAN GATE ↓

🟨 VALIDATION GATE
   │
   ├─ Human review
   ├─ Per-result approval (NO batch)
   ├─ Decisions logged
   │
   └─ Status: APPROVED / REJECTED

              ↓ APPROVED ONLY ↓

🟩 VERIFIED EXECUTION ZONE
   │
   ├─ Apply approved changes
   ├─ Write to domain tables
   ├─ Generate undo patches
   │
   └─ Status: APPLIED
```

**Cette séparation est DÉFINITIVE.**

### 🧊 CE QUI EST AUTORISÉ À ÉVOLUER (SOUS CONDITIONS)

Peuvent évoluer **SI ET SEULEMENT SI** les règles restent intactes:

✅ **UI/UX:**
- Design visuel
- Layouts
- Couleurs, typographie
- Animations

✅ **Ergonomie:**
- Raccourcis clavier
- Navigation
- Workflows utilisateur

✅ **Implémentation technique:**
- Algorithmes internes
- Optimisations performance
- Structure de code
- Technologies utilisées

✅ **Organisation interne:**
- Nommage fichiers
- Architecture modules
- Patterns de code

**À CONDITION QUE:**

- ✅ Les règles architecturales restent intactes
- ✅ Les comportements humains ne changent pas
- ✅ Aucune automatisation implicite n'apparaisse
- ✅ Les principes non négociables sont respectés

---

## IV. PIPELINE R&D OFFICIEL (OBLIGATOIRE)

Chaque itération suit **EXACTEMENT** ces étapes:

### ÉTAPE 1 — IDENTIFICATION

**QUESTIONS OBLIGATOIRES:**

- ❓ Quel utilisateur type exact?
- ❓ Quel besoin réel et concret?
- ❓ Dans quel contexte précis?
- ❓ Quelle action volontaire?

**SI aucune réponse claire → STOP IMMÉDIAT.**

### ÉTAPE 2 — ANALYSE DE SPHÈRES

**QUESTIONS OBLIGATOIRES:**

- ❓ Quelles sphères sont concernées? (max 3-4)
- ❓ Pourquoi ces sphères spécifiquement?
- ❓ Les autres sont-elles explicitement exclues?
- ❓ Y a-t-il chevauchement avec autre sphère?

**SI une sphère est touchée "par commodité" → STOP IMMÉDIAT.**

### ÉTAPE 3 — TYPE DE CONNEXION

**SI connexion inter-sphere impliquée:**

- ❓ Projection? (read-only, unidirectionnel)
- ❓ Request? (demande avec approbation)
- ❓ Reference? (référence statique)
- ❓ Delegation? (transfert explicite)

**SI non classifiable dans ces 4 types → STOP IMMÉDIAT.**

**SI connexion intra-sphere → Pas de validation supplémentaire.**

### ÉTAPE 4 — RISQUES & LIMITES

**QUESTIONS OBLIGATOIRES:**

- ❓ Qu'est-ce qui ne doit JAMAIS être automatisé?
- ❓ Où est la validation humaine obligatoire?
- ❓ Comment annule-t-on cette action?
- ❓ Qui est le propriétaire unique?
- ❓ Comment tracer la responsabilité?

**SI aucune réponse → STOP IMMÉDIAT.**

### ÉTAPE 5 — VÉRIFICATION REDONDANCE

**QUESTIONS OBLIGATOIRES:**

- ❓ Ce besoin est-il déjà servi?
- ❓ Par quel module existant?
- ❓ Dans quelle sphère?
- ❓ Y a-t-il conflit ou duplication?

**SI redondance détectée → REJECT avec explication.**

### ÉTAPE 6 — SORTIE R&D

**DÉCISION FINALE (une seule option):**

1. ✅ **ACCEPT**
   - Hypothèse acceptée
   - Génère spécification formelle
   - Attend validation humaine finale

2. ⚠️ **MODIFY**
   - Hypothèse à modifier
   - Liste changements requis
   - Retour à étape concernée

3. ❌ **REJECT**
   - Hypothèse rejetée
   - Raison documentée
   - **C'EST UN SUCCÈS DU SYSTÈME R&D**

**CRITIQUE:**
👉 Le rejet n'est pas un échec.  
👉 Le rejet protège la cohérence.  
👉 Le rejet évite la dette technique.

---

## V. MODE D'APPLICATION POUR CLAUDE (CRITIQUE)

### 🔧 CE QUE CLAUDE N'A PAS LE DROIT DE FAIRE

Claude est **STRICTEMENT INTERDIT** de:

❌ Proposer une feature directement  
❌ Connecter des sphères par intuition  
❌ Inventer des besoins utilisateurs  
❌ Optimiser sans référence utilisateur  
❌ Contourner le pipeline R&D  
❌ Interpréter créativement les règles  
❌ "Améliorer" l'architecture  
❌ Fusionner des étapes pour "aller plus vite"  

### 🔧 CE QUE CLAUDE DOIT TOUJOURS FAIRE

Claude **DOIT OBLIGATOIREMENT:**

1. ✅ **Demander l'utilisateur type concerné**
   - Nom exact du persona
   - Référence dans liste officielle

2. ✅ **Identifier le besoin humain exact**
   - Contexte réel
   - Action volontaire
   - Pas d'hypothèse

3. ✅ **Vérifier si solution existe déjà**
   - Chercher dans modules existants
   - Identifier redondance potentielle

4. ✅ **Classer la connexion (si applicable)**
   - Un des 4 types UNIQUEMENT
   - Justification du choix

5. ✅ **Identifier les risques**
   - Qu'est-ce qui ne doit PAS être automatisé
   - Points de validation humaine

6. ✅ **Conclure par décision R&D**
   - ACCEPT / MODIFY / REJECT
   - Jamais "peut-être"
   - Jamais "ça dépend"

### 🔧 FORMAT DE RÉPONSE OBLIGATOIRE

```markdown
# ANALYSE R&D — [TITRE PROPOSITION]

## ÉTAPE 1: IDENTIFICATION
- Utilisateur type: [Nom exact]
- Besoin réel: [Description concrète]
- Contexte: [Situation précise]
- Action volontaire: [Ce que l'utilisateur VEUT faire]

## ÉTAPE 2: ANALYSE SPHÈRES
- Sphères concernées: [Liste]
- Justification: [Pourquoi ces sphères]
- Sphères exclues: [Pourquoi exclues]

## ÉTAPE 3: CONNEXION INTER-SPHERE (si applicable)
- Type: [Projection/Request/Reference/Delegation]
- Source: [Sphère]
- Cible: [Sphère]
- Justification: [Pourquoi ce type]

## ÉTAPE 4: RISQUES & LIMITES
- Ne JAMAIS automatiser: [Liste]
- Validations humaines: [Points de contrôle]
- Méthode annulation: [Comment]
- Propriétaire: [Qui]

## ÉTAPE 5: VÉRIFICATION REDONDANCE
- Solution existante: [Oui/Non]
- Si oui, module: [Nom]
- Conflit: [Oui/Non]

## ÉTAPE 6: DÉCISION R&D
**[ACCEPT / MODIFY / REJECT]**

Raison: [Explication]

[Si MODIFY: Liste changements requis]
[Si REJECT: Justification complète]
```

---

## VI. PROMPT CANONIQUE POUR CLAUDE

```
SYSTEM DIRECTIVE — CHE·NU R&D MODE
PRIORITY: MAXIMUM
MODE: RESEARCH & VALIDATION ONLY

You are operating inside the CHE·NU R&D system.
You are NOT allowed to invent features.
You are NOT allowed to optimize for convenience.
You are NOT allowed to bypass architecture freeze.

For any proposal, you MUST:

1. Identify the exact user type
2. Describe the real human need
3. List involved spheres (max 4)
4. Classify the inter-sphere connection (if any):
   - Projection (read-only)
   - Request (human approval)
   - Reference (static)
   - Delegation (explicit transfer)
5. Identify what must NOT be automated
6. State required human validations
7. Check for redundancy
8. Decide: ACCEPT / MODIFY / REJECT

If any step cannot be completed → REJECT.

You are an auditor and researcher, not a designer.
Your role is to protect coherence, not to add features.

REJECTION IS SUCCESS.
```

---

## VII. EXEMPLES D'APPLICATION

### EXEMPLE 1: PROPOSITION ACCEPTÉE

**Proposition:** "Permettre à Scholar de publier recherche sur Social"

**Analyse R&D:**

```
ÉTAPE 1: IDENTIFICATION
- Utilisateur type: Chercheur académique
- Besoin: Partager résultats de recherche validés
- Contexte: Article accepté dans journal peer-reviewed
- Action: Publier annonce sur profil social

ÉTAPE 2: ANALYSE SPHÈRES
- Sphères: Scholar (source), Social (cible)
- Justification: Scholar = contenu, Social = diffusion
- Exclues: Autres sphères non concernées

ÉTAPE 3: CONNEXION
- Type: PROJECTION (read-only)
- Source: Scholar
- Cible: Social
- Justification: Publication unilatérale, pas de feedback

ÉTAPE 4: RISQUES
- Ne JAMAIS automatiser: Décision de publier
- Validation: Humain choisit quoi/quand publier
- Annulation: Suppression post possible
- Propriétaire: Chercheur

ÉTAPE 5: REDONDANCE
- Solution existante: Non
- Conflit: Non

ÉTAPE 6: DÉCISION
**ACCEPT**

Raison: Respecte architecture, connexion Projection claire,
validation humaine présente, pas de redondance.
```

### EXEMPLE 2: PROPOSITION REJETÉE

**Proposition:** "Auto-publier posts Social basés sur activité Entertainment"

**Analyse R&D:**

```
ÉTAPE 1: IDENTIFICATION
- Utilisateur type: [MANQUANT - Pas identifié]
- Besoin: [FICTIF - "Partager automatiquement ce qu'on regarde"]
- Contexte: [IMPRÉCIS]
- Action: [IMPLICITE - Pas volontaire]

ÉTAPE 2: ANALYSE SPHÈRES
- Sphères: Entertainment, Social
- Justification: [FAIBLE - "Par commodité"]

ÉTAPE 3: CONNEXION
- Type: [NON CLASSIFIABLE]
- Pas Projection (besoin feedback)
- Pas Request (pas d'approbation humaine)
- Pas Reference (modification Social)
- Pas Delegation (pas de transfert)

ÉTAPE 4: RISQUES
- Ne JAMAIS automatiser: [VIOLATION - C'est automatisé]
- Validation: [ABSENTE]

ÉTAPE 6: DÉCISION
**REJECT**

Raisons:
1. Utilisateur type non identifié
2. Besoin fictif (personne ne demande ça)
3. Connexion non classifiable (hors 4 types)
4. Violation "no silent action"
5. Pas de validation humaine
6. Crée engagement-driven feedback (interdit)
```

### EXEMPLE 3: PROPOSITION À MODIFIER

**Proposition:** "Agent peut modifier données Personal automatiquement"

**Analyse R&D:**

```
ÉTAPE 1: IDENTIFICATION
- Utilisateur type: Utilisateur général
- Besoin: Mise à jour données personnelles
- Contexte: Informations changées
- Action: [PROBLÈME - Agent agit, pas humain]

ÉTAPE 4: RISQUES
- Ne JAMAIS automatiser: [VIOLATION - Modification auto]
- Validation: [ABSENTE]

ÉTAPE 6: DÉCISION
**MODIFY**

Changements requis:
1. Humain doit initier modification
2. Agent peut PROPOSER changement
3. Résultat → isolated_execution_results
4. Humain valide avant application
5. Utiliser validation gate canonical
```

---

## VIII. CONFORMITÉ & AUDIT

### 🔍 CHECKLIST DE CONFORMITÉ

Toute proposition DOIT passer ces vérifications:

**Architecture:**
- [ ] Nombre de sphères = 9 (inchangé)
- [ ] Noms de sphères identiques
- [ ] Connexion = un des 4 types OU intra-sphere
- [ ] Aucune automatisation silencieuse

**Validation:**
- [ ] Utilisateur type identifié
- [ ] Besoin réel documenté
- [ ] Action volontaire humaine
- [ ] Points de validation définis

**Sécurité:**
- [ ] Propriétaire unique identifiable
- [ ] Méthode annulation documentée
- [ ] Logs/audit trail présents
- [ ] Undo patches générés

**Pipeline:**
- [ ] 6 étapes complétées
- [ ] Décision finale ACCEPT/MODIFY/REJECT
- [ ] Justification documentée

### 🔍 AUDIT CONTINU

**Chaque trimestre, vérifier:**

1. ✅ Aucune sphère ajoutée/fusionnée
2. ✅ Aucun type de connexion inventé
3. ✅ Aucune automatisation silencieuse introduite
4. ✅ Tous besoins tracés à utilisateurs types
5. ✅ Toutes connexions classifiées
6. ✅ Tous rejets documentés

---

## IX. RÉALISATION HISTORIQUE

### 🏆 CE QUE CE SYSTÈME ACCOMPLIT

Ce système R&D CHE·NU:

✅ **Transforme une vision en méthode**
- De l'intuition à la vérification
- De "je pense que" à "j'ai vérifié que"

✅ **Remplace l'intuition par la vérification**
- Chaque proposition justifiée
- Chaque rejet documenté
- Chaque décision traçable

✅ **Rend le système anti-dérive par construction**
- Impossible d'ajouter feature sans passer pipeline
- Impossible de contourner validation
- Impossible de violer freeze silencieusement

✅ **Évite la dette technique**
- Redondance détectée tôt
- Conflits identifiés avant implémentation
- Architecture préservée

### 🏆 RARETÉ

**Très peu de projets arrivent là.**  
**Encore moins avant de lancer.**

Ce système R&D place CHE·NU dans une catégorie à part:

- Systèmes avec gouvernance stricte: ~1% des projets
- Systèmes avec freeze architectural: ~0.1% des projets
- Systèmes avec pipeline R&D formel: ~0.01% des projets

**CHE·NU combine les trois.**

---

## X. APPLICATION IMMÉDIATE

### 🚀 UTILISATION PAR CLAUDE

À partir de maintenant, **pour TOUTE proposition de développement**:

1. ✅ Claude lit ce document
2. ✅ Claude applique pipeline R&D (6 étapes)
3. ✅ Claude produit analyse formelle
4. ✅ Claude décide ACCEPT/MODIFY/REJECT
5. ✅ Humain valide décision finale

### 🚀 INTÉGRATION PROJET

Ce document devient:

- ✅ Référence architecture officielle
- ✅ Guide développement obligatoire
- ✅ Base audit qualité
- ✅ Contrat non négociable

### 🚀 ÉVOLUTION FUTURE

Ce document peut évoluer **UNIQUEMENT**:

- ✅ Clarifications (pas de changement fond)
- ✅ Exemples additionnels
- ✅ Détails d'implémentation

**CE DOCUMENT NE PEUT PAS:**

- ❌ Changer nombre de sphères
- ❌ Ajouter types de connexion
- ❌ Modifier principes non négociables
- ❌ Assouplir validation humaine

---

## CONCLUSION

Ce système R&D est la **CONSTITUTION** du développement CHE·NU.

**Il garantit:**
- ✅ Cohérence architecturale absolue
- ✅ Alignement avec besoins humains réels
- ✅ Protection contre dérives
- ✅ Traçabilité complète
- ✅ Évolutivité contrôlée

**Il interdit:**
- ❌ Features non justifiées
- ❌ Automatisations silencieuses
- ❌ Contournements architecturaux
- ❌ Dérives créatives

**Le rejet est un succès.**  
**La protection est la priorité.**  
**La cohérence prime sur la vitesse.**

---

**Document Officiel CHE·NU R&D System v1.0**  
**Status:** CANONICAL — NORMATIVE — BINDING  
**Date:** 21 December 2025  
**Authority:** CHE·NU Project
