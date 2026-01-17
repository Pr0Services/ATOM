# AT·OM - NOVA-999 Database Migration

**PROPRIÉTÉ EXCLUSIVE DE JONATHAN EMMANUEL RODRIGUE**
**TOUS DROITS RÉSERVÉS - BREVET EN COURS - 2025**

---

## 📊 Infrastructure DigitalOcean

| Paramètre | Valeur |
|-----------|--------|
| **Host** | `db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com` |
| **Port** | `25060` |
| **Database** | `defaultdb` |
| **User** | `doadmin` |
| **SSL** | `require` (obligatoire) |
| **Région** | NYC9 |

---

## 📁 Structure des Fichiers

```
database/
├── schema.sql          # Schéma PostgreSQL complet
├── inject_agents.py    # Script d'injection Python
└── README.md           # Ce fichier
```

---

## 🚀 Guide de Migration

### Étape 1: Installer les dépendances

```bash
pip install psycopg2-binary
```

### Étape 2: Créer le schéma

Connectez-vous à PostgreSQL et exécutez le schéma:

```bash
# Via psql
psql "postgresql://doadmin:AVNS_11mUpQDq99BeOE4o068@db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com:25060/defaultdb?sslmode=require" -f schema.sql
```

Ou via un client GUI (DBeaver, pgAdmin) avec SSL activé.

### Étape 3: Lancer l'injection

```bash
# Windows
python inject_agents.py "C:\Users\Jonathan\Documents\AT-OM-Dataset"

# Mac/Linux
python inject_agents.py "/home/jonathan/data/agents"
```

---

## 📋 Schéma de Base de Données

### Tables Principales

| Table | Description | Capacité |
|-------|-------------|----------|
| `spheres` | 16 sphères de l'Essaim | 16 rows |
| `agents` | Agents individuels | 6500+ rows |
| `modules` | Modules V68 | 7 rows |
| `agent_modules` | Association N:N | Variable |
| `protocol_999_logs` | Logs Brise-Circuit | Audit |
| `activity_log` | Journal d'activité | Illimité |

### Les 16 Sphères

| Code | Nom | Couleur | Agents |
|------|-----|---------|--------|
| TECH | Technologie | #00D4FF | 450 |
| FIN | Finance | #FFD700 | 380 |
| LEGAL | Juridique | #C0C0C0 | 320 |
| HEALTH | Santé | #00FF88 | 400 |
| EDU | Éducation | #FF6B35 | 350 |
| CREATE | Créatif | #FF00FF | 420 |
| DATA | Data Science | #0047AB | 480 |
| COMM | Communication | #FF4444 | 360 |
| OPS | Opérations | #888888 | 340 |
| RESEARCH | Recherche | #9933FF | 390 |
| SECURITY | Sécurité | #FF0000 | 280 |
| ENV | Environnement | #00AA00 | 310 |
| SOCIAL | Social | #FFB347 | 370 |
| STRATEGY | Stratégie | #4169E1 | 330 |
| QUANTUM | Quantique | #E6E6FA | 220 |
| SOVEREIGN | Souverain | #D4AF37 | 100 |

---

## ⚡ Optimisations

Le script utilise plusieurs optimisations pour un vieux laptop:

1. **Batch Inserts** - 100 agents par transaction
2. **execute_values** - Insertion optimisée psycopg2
3. **Streaming Hash** - SHA-256 par chunks de 8KB
4. **UPSERT** - Mise à jour si l'agent existe déjà
5. **Index GIN** - Pour recherche JSONB rapide

---

## 🔒 Sécurité SSL

Le paramètre `sslmode='require'` est **obligatoire** pour DigitalOcean.

Sans SSL, vous obtiendrez l'erreur:
```
FATAL: no pg_hba.conf entry for host "x.x.x.x"
```

---

## 📈 Monitoring

### Vérifier le nombre d'agents

```sql
SELECT
    s.name AS sphere,
    COUNT(a.id) AS agents
FROM spheres s
LEFT JOIN agents a ON s.id = a.sphere_id
GROUP BY s.id
ORDER BY agents DESC;
```

### Dashboard complet

```sql
SELECT * FROM v_essaim_dashboard;
```

---

## 🆘 Troubleshooting

### Erreur SSL
```bash
# Vérifier que le certificat CA est accessible
openssl s_client -connect db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com:25060
```

### Timeout sur vieux laptop
Réduire `BATCH_SIZE` dans `inject_agents.py`:
```python
BATCH_SIZE = 50  # Au lieu de 100
```

### Mémoire insuffisante
Le script lit les fichiers texte jusqu'à 100KB max. Pour ignorer le contenu:
```python
raw_content = None  # Commenter la ligne read_text_content()
```

---

© 2025 Jonathan Emmanuel Rodrigue - Tous droits réservés
