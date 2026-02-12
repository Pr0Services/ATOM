# PROMPT SKYVERN — AT·OM Infrastructure Complete

**Copie ce prompt directement dans Skyvern:**

---

## MISSION

Configure l'infrastructure complete du projet AT·OM. Connecte le domaine at-om.ai, verifie les services cloud, et execute les migrations de base de donnees.

## INFORMATIONS CLES

```
DOMAINE: at-om.ai (GoDaddy)
FRONTEND: Vercel - projet "atom-sovereign"
BACKEND: DigitalOcean - app "sea-turtle-app-n4vsa"
DATABASE: Supabase - projet "vzbrhovthpihrhdbbjud"
BLOCKCHAIN: Hedera Testnet - token 0.0.7730446
```

---

## PHASE 1: CONFIGURATION DOMAINE (GoDaddy + Vercel)

### Etape 1.1: Ajouter domaine dans Vercel
```
1. Aller sur https://vercel.com/dashboard
2. Cliquer sur le projet "atom-sovereign"
3. Aller dans Settings > Domains
4. Cliquer "Add"
5. Entrer: at-om.ai
6. Cliquer "Add"
7. Egalement ajouter: www.at-om.ai
8. Noter les instructions DNS affichees
```

### Etape 1.2: Configurer DNS sur GoDaddy
```
1. Aller sur https://dcc.godaddy.com/manage/at-om.ai/dns
2. Ou: GoDaddy > My Products > at-om.ai > DNS

3. SUPPRIMER les records existants de type A et CNAME pour @ et www (s'ils existent)

4. AJOUTER ces records:

   Type: A
   Name: @
   Value: 76.76.21.21
   TTL: 600

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 600

5. Sauvegarder les changements
```

### Etape 1.3: Verifier dans Vercel
```
1. Retourner dans Vercel > Settings > Domains
2. Attendre que le statut passe a "Valid Configuration"
3. Le SSL sera automatiquement configure
4. Si "Pending", attendre 5-10 minutes et rafraichir
```

---

## PHASE 2: VERIFICATION VERCEL

### Etape 2.1: Variables d'environnement
```
1. Vercel > atom-sovereign > Settings > Environment Variables
2. Verifier que ces variables existent:

   REACT_APP_SUPABASE_URL = https://vzbrhovthpihrhdbbjud.supabase.co
   REACT_APP_SUPABASE_ANON_KEY = [doit exister, commence par "sb_"]
   REACT_APP_HEDERA_TOKEN_ID = 0.0.7730446
   REACT_APP_HEDERA_NETWORK = testnet
   REACT_APP_ATOM_M = 44.4
   REACT_APP_ATOM_P = 161.8
   REACT_APP_ATOM_I = 369
   REACT_APP_ATOM_PO = 1728

3. Si REACT_APP_SUPABASE_ANON_KEY manque:
   - Aller sur Supabase > Settings > API
   - Copier "anon public" key
   - L'ajouter dans Vercel
```

---

## PHASE 3: SUPABASE - MIGRATIONS SQL

### Etape 3.1: Connexion
```
1. Aller sur https://supabase.com/dashboard
2. Selectionner le projet (vzbrhovthpihrhdbbjud)
3. Aller dans SQL Editor (menu gauche)
```

### Etape 3.2: Executer Script 1 - Fix Policies
```
1. Cliquer "New query"
2. Copier-coller ce SQL:

-- 01-fix-existing-policies.sql
-- Fix RLS policies for existing thread tables

-- Drop existing policies on private_threads
DO $$
DECLARE
  pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'private_threads'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON private_threads', pol.policyname);
  END LOOP;
END $$;

-- Drop existing policies on thread_messages
DO $$
DECLARE
  pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'thread_messages'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON thread_messages', pol.policyname);
  END LOOP;
END $$;

-- Recreate policies for private_threads using participant_ids (TEXT[])
CREATE POLICY "Users can view their threads"
ON private_threads FOR SELECT
USING (
  auth.uid()::text = ANY(participant_ids)
  OR created_by = auth.uid()::text
);

CREATE POLICY "Users can create threads"
ON private_threads FOR INSERT
WITH CHECK (created_by = auth.uid()::text);

CREATE POLICY "Creators can update threads"
ON private_threads FOR UPDATE
USING (created_by = auth.uid()::text);

-- Recreate policies for thread_messages
CREATE POLICY "Thread participants can view messages"
ON thread_messages FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE private_threads.id = thread_messages.thread_id
    AND (
      auth.uid()::text = ANY(private_threads.participant_ids)
      OR private_threads.created_by = auth.uid()::text
    )
  )
);

CREATE POLICY "Thread participants can send messages"
ON thread_messages FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE private_threads.id = thread_messages.thread_id
    AND (
      auth.uid()::text = ANY(private_threads.participant_ids)
      OR private_threads.created_by = auth.uid()::text
    )
  )
);

3. Cliquer "Run"
4. Verifier: "Success. No rows returned" = OK
```

### Etape 3.3: Executer Script 2 - Founder Features
```
1. Nouvelle query
2. Aller sur le repo GitHub: /services/database/founder-features.sql
3. Copier tout le contenu
4. Coller dans SQL Editor
5. Cliquer "Run"
6. Verifier: pas d'erreur
```

### Etape 3.4: Executer Script 3 - Agents Tables
```
1. Nouvelle query
2. Copier /services/database/agents-tables.sql depuis le repo
3. Coller et Run
4. Verification: SELECT * FROM agents;
   Resultat attendu: 3 lignes (facilitator, synthesis, memory)
```

### Etape 3.5: Executer Script 4 - Adaptive Agents
```
1. Nouvelle query
2. Copier /services/database/founder-adaptive-agents.sql depuis le repo
3. Coller et Run
4. Verification: SELECT COUNT(*) FROM agents;
   Resultat attendu: 7 (3 base + 4 adaptive)
```

### Etape 3.6: Executer Script 5 - Grid Tables
```
1. Nouvelle query
2. Copier /services/database/grid-tables.sql depuis le repo
3. Coller et Run
4. Verification: SELECT * FROM grid_sectors;
   Resultat attendu: 12 lignes (zodiac sectors)
```

---

## PHASE 4: SUPABASE - STORAGE BUCKET

### Etape 4.1: Creer le bucket
```
1. Supabase > Storage (menu gauche)
2. Cliquer "New bucket"
3. Configurer:
   - Name: underground-vault
   - Public bucket: NON (decocher)
   - File size limit: 52428800
4. Cliquer "Create bucket"
```

### Etape 4.2: Ajouter les policies
```
1. Retourner dans SQL Editor
2. Executer:

-- Storage policies for underground-vault
CREATE POLICY "Authenticated users can upload to vault"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'underground-vault');

CREATE POLICY "Authenticated users can view vault"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'underground-vault');

CREATE POLICY "Users can delete own uploads"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'underground-vault' AND auth.uid()::text = owner_id::text);
```

---

## PHASE 5: SUPABASE - ACTIVER REALTIME

```
1. Supabase > Database > Replication
2. Sous "Realtime", activer pour ces tables:
   - profiles
   - community_messages
   - private_threads
   - thread_messages
   - activity_feed
   - grid_nodes
   - founder_layout_proposals
3. Sauvegarder
```

---

## PHASE 6: VERIFICATION DIGITALOCEAN

```
1. Aller sur https://cloud.digitalocean.com/apps
2. Cliquer sur "sea-turtle-app-n4vsa"
3. Settings > App-Level Environment Variables
4. Verifier que ces variables existent:
   - SUPABASE_URL
   - SUPABASE_SERVICE_ROLE_KEY
   - DATABASE_URL
   - HEDERA_OPERATOR_ID
   - HEDERA_OPERATOR_KEY
   - JWT_SECRET_KEY
   - ENV = production
   - HOST = 0.0.0.0
5. Si une variable manque, la noter dans le rapport
```

---

## PHASE 7: TESTS DE VALIDATION

### Test 1: Frontend (Vercel)
```
URL: https://at-om.ai
Attendu: Page charge, affiche "AT·OM" ou contenu de l'app
Alternative: https://www.at-om.ai
```

### Test 2: Backend Health
```
URL: https://sea-turtle-app-n4vsa.ondigitalocean.app/api/v2/health
Attendu: {"status": "healthy"} ou reponse 200
```

### Test 3: API Proxy
```
URL: https://at-om.ai/api/health
Attendu: Reponse du backend via le proxy Vercel
```

### Test 4: Supabase Connection
```
Dans Supabase SQL Editor:
SELECT COUNT(*) FROM profiles;
Attendu: Nombre (peut etre 0 si nouveau)
```

---

## RAPPORT FINAL

Genere ce rapport a la fin:

```
========================================
RAPPORT SKYVERN - AT·OM INFRASTRUCTURE
Date: [DATE]
========================================

DOMAINE: at-om.ai
-----------------
[x] Ajoute dans Vercel: OK/ERREUR
[x] DNS GoDaddy configure: OK/ERREUR
[x] SSL actif: OK/EN ATTENTE
[x] https://at-om.ai accessible: OK/ERREUR
[x] https://www.at-om.ai accessible: OK/ERREUR

VERCEL (atom-sovereign)
-----------------------
[x] Variables env presentes: OK/MANQUANTES: [liste]
[x] Build status: OK/ERREUR

SUPABASE (vzbrhovthpihrhdbbjud)
------------------------------
[x] Script 01-fix-policies: OK/ERREUR
[x] Script founder-features: OK/ERREUR
[x] Script agents-tables: OK/ERREUR
[x] Script adaptive-agents: OK/ERREUR
[x] Script grid-tables: OK/ERREUR
[x] Bucket underground-vault: CREE/ERREUR
[x] Realtime active: OK/ERREUR

Verification tables:
- agents: [NOMBRE] lignes (attendu: 7)
- grid_sectors: [NOMBRE] lignes (attendu: 12)

DIGITALOCEAN (sea-turtle-app-n4vsa)
-----------------------------------
[x] App running: OK/ERREUR
[x] Variables env: OK/MANQUANTES: [liste]
[x] Health endpoint: OK/ERREUR

TESTS FINAUX
------------
[x] Frontend https://at-om.ai: OK/ERREUR
[x] Backend API health: OK/ERREUR
[x] API proxy: OK/ERREUR

ACTIONS MANUELLES REQUISES
--------------------------
[Liste si applicable]

NOTES
-----
[Observations]

========================================
```

---

## URLS DE REFERENCE

| Service | URL |
|---------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| Supabase Dashboard | https://supabase.com/dashboard/project/vzbrhovthpihrhdbbjud |
| DigitalOcean Apps | https://cloud.digitalocean.com/apps |
| GoDaddy DNS | https://dcc.godaddy.com/manage/at-om.ai/dns |
| GitHub Repo | https://github.com/[USER]/ATOM |

## FICHIERS SQL (dans le repo)

```
/services/database/01-fix-existing-policies.sql
/services/database/founder-features.sql
/services/database/agents-tables.sql
/services/database/founder-adaptive-agents.sql
/services/database/grid-tables.sql
```

---

**FIN DU PROMPT SKYVERN**
