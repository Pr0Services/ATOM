# SUPABASE - LISTE DE VÉRIFICATION
## AT-OM CHE·NU™ V76

---

## CONFIGURATION EXISTANTE ✅

```env
SUPABASE_URL=https://<VOTRE_PROJET>.supabase.co
SUPABASE_ANON_KEY=<VOTRE_ANON_KEY>
SUPABASE_SERVICE_ROLE_KEY=<VOTRE_SERVICE_ROLE_KEY>
```

---

## 1. VÉRIFICATION DASHBOARD SUPABASE

- [ ] **1.1** Accéder à https://supabase.com/dashboard
- [ ] **1.2** Sélectionner le projet `<VOTRE_PROJECT_ID>`
- [ ] **1.3** Vérifier que le projet est actif (pas en pause)

---

## 2. VÉRIFICATION DES TABLES

Ouvrir **Table Editor** et vérifier la présence des tables:

### Tables Core (OBLIGATOIRES)
| Table | Status | Description |
|-------|--------|-------------|
| `profiles` | ❓ À vérifier | Extension auth.users |
| `perceptions` | ❓ À vérifier | Journal de perception |
| `local_needs` | ❓ À vérifier | Besoins locaux |
| `need_votes` | ❓ À vérifier | Suivi des votes |
| `annales` | ❓ À vérifier | Calculs Arithmos |

### Tables Avancées
| Table | Status | Description |
|-------|--------|-------------|
| `succes_humanite` | ❓ À vérifier | Knowledge Base |
| `atom_mapping` | ❓ À vérifier | Flux de données |
| `gratitude_letter` | ❓ À vérifier | Lettres de remerciement |
| `territory_projects` | ❓ À vérifier | Projets Québec |
| `accreditations` | ❓ À vérifier | Accréditations |
| `subcontractor_services` | ❓ À vérifier | Services sous-traitants |
| `institutional_partners` | ❓ À vérifier | Partenaires |

### Action si tables manquantes:
1. Aller dans **SQL Editor**
2. Exécuter le script `supabase-schema.sql` depuis:
   `C:\Users\admin\Github\ATOM\ATOM\Vzwwviru70560-d4e\hardcore-joliot\atom\app\supabase-schema.sql`

---

## 3. VÉRIFICATION AUTH

Dans **Authentication** > **Settings**:

- [ ] **3.1** Site URL configuré: `https://at-om-999-deploy-zama-alleluya.vercel.app`
- [ ] **3.2** Redirect URLs inclut:
  - `https://at-om-999-deploy-zama-alleluya.vercel.app/**`
  - `http://localhost:3000/**`
  - `http://localhost:5173/**`

- [ ] **3.3** Email Auth activé
- [ ] **3.4** Confirm Email désactivé (pour dev) ou activé (pour prod)

---

## 4. VÉRIFICATION RLS (Row Level Security)

Dans **Authentication** > **Policies**:

- [ ] **4.1** RLS activé sur toutes les tables
- [ ] **4.2** Policies créées pour chaque table

### Policies attendues par table:

**profiles:**
- `Profiles are viewable by everyone` (SELECT)
- `Users can update own profile` (UPDATE)
- `Users can insert own profile` (INSERT)

**perceptions:**
- `Users can view own perceptions` (SELECT)
- `Users can create own perceptions` (INSERT)
- `Users can delete own perceptions` (DELETE)

**local_needs:**
- `Anyone can view needs` (SELECT)
- `Authenticated users can create needs` (INSERT)
- `Users can update own needs` (UPDATE)

---

## 5. VÉRIFICATION FONCTIONS SQL

Dans **Database** > **Functions**:

- [ ] **5.1** `increment_votes` - Fonction de vote
- [ ] **5.2** `handle_new_user` - Trigger création profil
- [ ] **5.3** `search_knowledge_base` - Recherche full-text
- [ ] **5.4** `process_perception_to_analysis` - Mapping L0-L3
- [ ] **5.5** `calculate_accreditation_score` - Score accréditation
- [ ] **5.6** `approve_accreditation` - Approbation partenaire

---

## 6. VÉRIFICATION TRIGGERS

Dans **Database** > **Triggers**:

- [ ] **6.1** `on_auth_user_created` sur `auth.users` → `handle_new_user()`

---

## 7. VÉRIFICATION API KEYS

Dans **Settings** > **API**:

- [ ] **7.1** Copier `anon` key → `SUPABASE_ANON_KEY`
- [ ] **7.2** Copier `service_role` key → `SUPABASE_SERVICE_ROLE_KEY`
- [ ] **7.3** Noter l'URL du projet → `SUPABASE_URL`

---

## 8. INTÉGRATION FRONTEND

### Fichiers à vérifier/créer dans le déploiement:

| Fichier | Status | Action |
|---------|--------|--------|
| `/js/supabase-client.js` | ❌ À créer | Client Supabase vanilla JS |
| `config.js` | ⚠️ À modifier | Ajouter clés Supabase |

---

## 9. TEST DE CONNEXION

Script de test à exécuter dans la console browser:

```javascript
// Test Supabase Connection
const SUPABASE_URL = '<VOTRE_SUPABASE_URL>';
const SUPABASE_ANON_KEY = '<VOTRE_ANON_KEY>';

fetch(`${SUPABASE_URL}/rest/v1/profiles?select=count`, {
    headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
    }
})
.then(r => r.json())
.then(data => console.log('✅ Supabase connecté:', data))
.catch(err => console.error('❌ Erreur Supabase:', err));
```

---

## 10. VARIABLES VERCEL

Dans le dashboard Vercel du projet, ajouter:

| Variable | Valeur |
|----------|--------|
| `NEXT_PUBLIC_SUPABASE_URL` | `<VOTRE_SUPABASE_URL>` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `<VOTRE_ANON_KEY>` |

---

## RÉSUMÉ STATUS

| Composant | Status |
|-----------|--------|
| Projet Supabase | ✅ Existe |
| URL & Clés | ✅ Configurés dans .env |
| Tables DB | ❓ À vérifier manuellement |
| RLS Policies | ❓ À vérifier manuellement |
| Functions SQL | ❓ À vérifier manuellement |
| Client Frontend | ❌ À créer (voir tâche 3-4) |
| Variables Vercel | ❓ À configurer |

---

*Généré le 2026-01-30 - AT-OM CHE·NU™ V76*
