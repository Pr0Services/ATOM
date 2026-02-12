# SKYVERN EXECUTION PROMPT — AT·OM Infrastructure Setup

## MISSION

Tu es un agent d'automatisation charge de configurer l'infrastructure complete du projet AT·OM (codename: CHE-NU). Tu dois connecter et valider tous les services cloud pour deployer une application Web3 de production.

---

## CONTEXTE PROJET

```
Projet: AT·OM (L'Arche des Resonances Universelles)
Type: Application Web3 avec blockchain Hedera
Stack: React (Vercel) + FastAPI (DigitalOcean) + Supabase + Hedera
Status: Infrastructure existante, migrations DB en attente
```

---

## SERVICES A CONFIGURER

### 1. VERCEL (Frontend)
- **URL Dashboard**: https://vercel.com/dashboard
- **Projet**: `atom-sovereign`
- **Action**: Verifier les variables d'environnement et ajouter le domaine

### 2. SUPABASE (Database + Auth)
- **URL Dashboard**: https://supabase.com/dashboard
- **Projet**: `vzbrhovthpihrhdbbjud`
- **Action**: Executer les scripts SQL et creer le bucket storage

### 3. DIGITALOCEAN (Backend)
- **URL Dashboard**: https://cloud.digitalocean.com
- **App**: `sea-turtle-app-n4vsa`
- **Action**: Verifier les variables d'environnement

### 4. DOMAINE (DNS)
- **Domaine**: [A SPECIFIER PAR L'UTILISATEUR]
- **Action**: Configurer les records DNS pour pointer vers Vercel

---

## WORKFLOW D'EXECUTION

### PHASE 1: Verification Vercel
```
1. Aller sur https://vercel.com/dashboard
2. Ouvrir le projet "atom-sovereign"
3. Aller dans Settings > Environment Variables
4. Verifier que ces variables existent:
   - REACT_APP_SUPABASE_URL = https://vzbrhovthpihrhdbbjud.supabase.co
   - REACT_APP_SUPABASE_ANON_KEY = [doit exister]
   - REACT_APP_HEDERA_TOKEN_ID = 0.0.7730446
   - REACT_APP_HEDERA_NETWORK = testnet
   - REACT_APP_ATOM_M = 44.4
   - REACT_APP_ATOM_P = 161.8
   - REACT_APP_ATOM_I = 369
   - REACT_APP_ATOM_PO = 1728
5. Si une variable manque, la signaler
6. Capturer une screenshot de confirmation
```

### PHASE 2: Configuration Domaine (si demande)
```
1. Dans Vercel > Project > Settings > Domains
2. Cliquer "Add Domain"
3. Entrer le domaine fourni par l'utilisateur
4. Noter les records DNS requis:
   - Type A: @ -> 76.76.21.21
   - Type CNAME: www -> cname.vercel-dns.com
5. Indiquer a l'utilisateur de configurer ces records chez son registrar
6. Attendre la verification (peut prendre jusqu'a 48h)
```

### PHASE 3: Verification Supabase
```
1. Aller sur https://supabase.com/dashboard
2. Ouvrir le projet (vzbrhovthpihrhdbbjud)
3. Aller dans Table Editor
4. Verifier que ces tables existent:
   - profiles
   - community_messages
   - private_threads
   - thread_messages
5. Noter les tables manquantes
```

### PHASE 4: Execution Scripts SQL
```
Pour chaque script, dans l'ordre:

SCRIPT 1: 01-fix-existing-policies.sql
1. Aller dans SQL Editor
2. Copier le contenu du fichier /services/database/01-fix-existing-policies.sql
3. Cliquer "Run"
4. Verifier: pas d'erreur

SCRIPT 2: founder-features.sql
1. Copier /services/database/founder-features.sql
2. Cliquer "Run"
3. Verifier: tables underground_videos et activity_feed creees

SCRIPT 3: agents-tables.sql
1. Copier /services/database/agents-tables.sql
2. Cliquer "Run"
3. Verifier: SELECT * FROM agents (doit retourner 3+ lignes)

SCRIPT 4: founder-adaptive-agents.sql
1. Copier /services/database/founder-adaptive-agents.sql
2. Cliquer "Run"
3. Verifier: SELECT * FROM agents (doit retourner 7+ lignes)

SCRIPT 5: grid-tables.sql
1. Copier /services/database/grid-tables.sql
2. Cliquer "Run"
3. Verifier: SELECT * FROM grid_sectors (doit retourner 12 lignes)
```

### PHASE 5: Creation Bucket Storage
```
1. Dans Supabase > Storage
2. Verifier si "zama-assets" existe (bucket public)
3. Creer "underground-vault":
   - Cliquer "New bucket"
   - Name: underground-vault
   - Public: NON (decocher)
   - File size limit: 52428800 (50MB)
4. Ajouter les policies RLS via SQL Editor:

CREATE POLICY "Founders can upload videos"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'underground-vault');

CREATE POLICY "Founders can view videos"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'underground-vault');
```

### PHASE 6: Verification DigitalOcean
```
1. Aller sur https://cloud.digitalocean.com
2. Apps > sea-turtle-app-n4vsa
3. Settings > App-Level Environment Variables
4. Verifier que ces variables existent:
   - SUPABASE_URL
   - SUPABASE_SERVICE_ROLE_KEY
   - DATABASE_URL
   - HEDERA_OPERATOR_ID
   - HEDERA_OPERATOR_KEY
   - JWT_SECRET_KEY
   - ENV = production
5. Si une variable manque, la signaler
```

### PHASE 7: Validation Finale
```
1. Tester le frontend: https://atom-arche.vercel.app
   - La page doit charger sans erreur

2. Tester le backend: https://sea-turtle-app-n4vsa.ondigitalocean.app/api/v2/health
   - Doit retourner {"status": "healthy"}

3. Tester avec le domaine (si configure):
   - https://[DOMAINE]/ doit charger le frontend
```

---

## VARIABLES D'ENVIRONNEMENT REFERENCE

### Vercel (Frontend) - Variables REACT_APP_*
```
REACT_APP_SUPABASE_URL=https://vzbrhovthpihrhdbbjud.supabase.co
REACT_APP_SUPABASE_ANON_KEY=[depuis Supabase > Settings > API]
REACT_APP_HEDERA_TOKEN_ID=0.0.7730446
REACT_APP_HEDERA_NETWORK=testnet
REACT_APP_ATOM_M=44.4
REACT_APP_ATOM_P=161.8
REACT_APP_ATOM_I=369
REACT_APP_ATOM_PO=1728
```

### DigitalOcean (Backend)
```
SUPABASE_URL=https://vzbrhovthpihrhdbbjud.supabase.co
SUPABASE_SERVICE_ROLE_KEY=[depuis Supabase > Settings > API > service_role]
DATABASE_URL=[depuis DigitalOcean > Databases > Connection string]
HEDERA_OPERATOR_ID=0.0.7702951
HEDERA_OPERATOR_KEY=[cle privee Hedera]
JWT_SECRET_KEY=[UUID genere]
ENV=production
DEBUG=false
HOST=0.0.0.0
```

---

## DNS RECORDS (pour domaine personnalise)

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 76.76.21.21 | 300 |
| CNAME | www | cname.vercel-dns.com | 300 |

---

## GESTION DES ERREURS

### Si erreur SQL "policy already exists"
- Ignorer, la policy existe deja

### Si erreur SQL "table already exists"
- Ignorer, le script utilise CREATE TABLE IF NOT EXISTS

### Si erreur SQL "column already exists"
- Ignorer, le script gere ce cas

### Si erreur "permission denied"
- Verifier que tu es connecte au bon projet Supabase
- Utiliser le service_role_key pour les operations admin

### Si domaine ne se propage pas
- Attendre 30 minutes
- Verifier les records DNS chez le registrar
- Contacter l'utilisateur si >2h

---

## RAPPORT DE FIN DE MISSION

A la fin, generer un rapport avec:

```
## RAPPORT SKYVERN - AT·OM Infrastructure

### Services Verifies
- [ ] Vercel: [OK/ERREUR]
- [ ] Supabase: [OK/ERREUR]
- [ ] DigitalOcean: [OK/ERREUR]
- [ ] Domaine: [OK/NON CONFIGURE/EN ATTENTE]

### Scripts SQL Executes
- [ ] 01-fix-existing-policies.sql: [OK/ERREUR]
- [ ] founder-features.sql: [OK/ERREUR]
- [ ] agents-tables.sql: [OK/ERREUR]
- [ ] founder-adaptive-agents.sql: [OK/ERREUR]
- [ ] grid-tables.sql: [OK/ERREUR]

### Storage
- [ ] Bucket underground-vault: [CREE/EXISTANT/ERREUR]

### Tests
- [ ] Frontend accessible: [OK/ERREUR]
- [ ] Backend health: [OK/ERREUR]
- [ ] Domaine (si applicable): [OK/ERREUR]

### Actions Requises par l'Utilisateur
[Liste des actions manuelles necessaires]

### Notes
[Observations importantes]
```

---

## INFORMATIONS IMPORTANTES

- **NE PAS** modifier les cles API existantes sauf si demande
- **NE PAS** supprimer de tables ou donnees existantes
- **TOUJOURS** faire des screenshots avant/apres les modifications
- **SIGNALER** immediatement toute erreur critique
- Les scripts SQL sont idempotents (peuvent etre re-executes sans danger)

---

## FICHIERS DE REFERENCE

Les scripts SQL sont dans le repository:
- `/services/database/01-fix-existing-policies.sql`
- `/services/database/founder-features.sql`
- `/services/database/agents-tables.sql`
- `/services/database/founder-adaptive-agents.sql`
- `/services/database/grid-tables.sql`

Documentation complete:
- `/automation/SKYVERN_MASTER_PLAN.md`
- `/automation/COHERENCE_TABLE.md`
- `/automation/SKYVERN_OPERATIONS.json`

---

*Mission: Configurer l'infrastructure AT·OM pour la Phase I (144 Fondateurs)*
