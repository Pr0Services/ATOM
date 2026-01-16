# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU™ — SEARCH & REPLACE GUIDE v39
# Guide de mise à jour pour passer de 10 → 9 sphères avec Scholar
# ═══════════════════════════════════════════════════════════════════════════════

## 🔍 RECHERCHER ET REMPLACER

### Pattern 1: Nombre de sphères
```
RECHERCHER: "10 spheres" | "10 sphères" | "10 Spheres" | "ten spheres"
REMPLACER:  "9 spheres" | "9 sphères" | "9 Spheres" | "nine spheres"
```

### Pattern 2: Liste numérotée avec My Team en 10
```
RECHERCHER: "| 10 | `my_team`" ou "10. my_team"
REMPLACER:  "| 9 | `team`" ou "9. team"
```

### Pattern 3: IDs des sphères (French → English)
```
personnel       → personal
entreprises     → business
gouvernement    → government
creative_studio → creative
skills_tools    → SUPPRIMER (intégré dans team)
entertainment   → entertainment
community       → community
social_media    → social
ia_labs         → SUPPRIMER (intégré dans team)
my_team         → team
```

### Pattern 4: Ajouter Scholar (position 8)
Insérer entre Entertainment (7) et Team (9):
```
| 8 | `scholar` | Scholar | 🎓 | #2980B9 | Recherche, apprentissage, synthèse |
```

---

## 📁 FICHIERS À MODIFIER

### CHENU_MASTER_REFERENCE_v5_FINAL.md
**Sections à modifier:**
- Ligne ~340: Table des sphères
- Ligne ~978: export type SphereId
- Ligne ~1005: export const SPHERES
- Ligne ~1119: export const SPHERE_LIST

### CHENU_SQL_SCHEMA_v29.sql
**Sections à modifier:**
- CREATE TYPE sphere_id AS ENUM
- INSERT INTO spheres
- Toute référence à skills_tools ou ia_labs

### CHENU_API_SPECS_v29.md
**Sections à modifier:**
- Liste des sphere_id valides
- Endpoints par sphère
- Ajouter section Scholar API

### CHENU_AGENT_PROMPTS_v29.md
**Sections à modifier:**
- Agents par sphère
- Ajouter section Scholar Agents

### CHENU_MERMAID_DIAGRAMS_v29.md
**Sections à modifier:**
- Tous les diagrammes avec sphères
- Mettre à jour le graph TB

### CHENU_INVESTOR_BOOK.md
**Rechercher:**
- "10 spheres" → "9 spheres"
- Mettre à jour la liste des sphères
- Ajouter Scholar dans les descriptions

### LAYOUT_ENGINE_CHAPTER.md
**Sections à modifier:**
- SphereNavigator component
- SPHERES array
- Couleurs et routes

### Autres chapters:
- WORKSPACE_ENGINE_CHAPTER.md
- DATASPACE_ENGINE_CHAPTER.md
- MEMORY_GOVERNANCE_CHAPTER.md
- BACKSTAGE_INTELLIGENCE_CHAPTER.md
- ONECLICK_ENGINE_CHAPTER.md
- OCW_CHAPTER.md
- MEETING_SYSTEM_CHAPTER.md
- IMMOBILIER_DOMAIN_CHAPTER.md

---

## ✅ COMMANDES SED POUR MISE À JOUR AUTOMATIQUE

```bash
#!/bin/bash
# Script de mise à jour des documents CHE·NU pour 9 sphères

# Pattern: 10 spheres → 9 spheres
sed -i 's/10 spheres/9 spheres/g' *.md
sed -i 's/10 sphères/9 sphères/g' *.md
sed -i 's/10 Spheres/9 Spheres/g' *.md

# Pattern: French IDs → English IDs
sed -i 's/personnel/personal/g' *.md *.sql
sed -i 's/entreprises/business/g' *.md *.sql
sed -i 's/gouvernement/government/g' *.md *.sql
sed -i 's/creative_studio/creative/g' *.md *.sql
sed -i 's/social_media/social/g' *.md *.sql
sed -i 's/my_team/team/g' *.md *.sql

# ATTENTION: skills_tools et ia_labs doivent être remplacés manuellement
# car ils sont intégrés dans team avec contexte

echo "✅ Mise à jour terminée - vérifier manuellement:"
echo "  - skills_tools → team (avec contexte)"
echo "  - ia_labs → team (avec contexte)"
echo "  - Ajouter Scholar (position 8)"
```

---

## 📋 CHECKLIST DE VÉRIFICATION

Après mise à jour, vérifier:

```bash
# Compter les occurrences de l'ancien format
grep -r "10 sphere\|skills_tools\|ia_labs\|my_team\|personnel\|entreprises" /path/to/docs/

# Vérifier que Scholar existe
grep -r "scholar\|Scholar\|🎓" /path/to/docs/

# Vérifier le compte des sphères
grep -r "9 sphere\|nine sphere" /path/to/docs/
```

---

## 🎯 STRUCTURE FINALE ATTENDUE

Après toutes les modifications, chaque document devrait avoir:

```typescript
// TypeScript
export type SphereId = 
  | 'personal'
  | 'business'
  | 'government'
  | 'creative'
  | 'community'
  | 'social'
  | 'entertainment'
  | 'scholar'      // ← NOUVEAU
  | 'team';        // ← Inclut IA Labs + Skills
```

```sql
-- SQL
CREATE TYPE sphere_id AS ENUM (
    'personal',
    'business',
    'government',
    'creative',
    'community',
    'social',
    'entertainment',
    'scholar',      -- NOUVEAU
    'team'          -- Inclut IA Labs + Skills
);
```

```markdown
| # | ID | Nom | Emoji | Description |
|---|-----|-----|-------|-------------|
| 1 | personal | Personal | 🏠 | Vie privée |
| 2 | business | Business | 💼 | Affaires |
| 3 | government | Government | 🏛️ | Institutions |
| 4 | creative | Creative | 🎨 | Création |
| 5 | community | Community | 👥 | Communauté |
| 6 | social | Social | 📱 | Médias |
| 7 | entertainment | Entertainment | 🎬 | Divertissement |
| 8 | scholar | Scholar | 🎓 | Connaissance |  ← NOUVEAU
| 9 | team | Team | 🤝 | Équipe + IA |
```

---

## ⚠️ POINTS D'ATTENTION

1. **Ne pas supprimer skills_tools et ia_labs brutalement**
   - Leurs fonctionnalités sont INTÉGRÉES dans team
   - Documenter cette intégration

2. **Scholar n'est pas optionnelle**
   - C'est le CŒUR de l'intelligence gouvernée
   - Doit être présente dans tous les diagrammes

3. **Ordre des sphères**
   - L'ordre 1-9 est FIXE
   - Scholar = 8, Team = 9 (pas l'inverse)

4. **Couleurs**
   - Scholar: #2980B9 (Deep Blue)
   - Team: #2F4C39 (Shadow Moss)

---

*Document créé: 2024-12-20*
*Version: v39*
