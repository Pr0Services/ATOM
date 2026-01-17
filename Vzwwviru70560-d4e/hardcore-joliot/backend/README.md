# 🚀 CHE·NU™ / AT·OM — BACKEND READY PACKAGE
## [AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12

---

## 📦 CONTENU DU PACKAGE

```
BACKEND_READY_PACKAGE/
├── .env                    ← Configuration (SEUL FICHIER À MODIFIER)
├── docker-compose.yml      ← Orchestration Docker
├── start.sh               ← Script démarrage avec Docker
├── start-direct.sh        ← Script démarrage sans Docker
├── nginx/
│   └── nginx.conf         ← Reverse proxy configuration
└── README.md              ← Ce fichier
```

---

## ⚡ DÉMARRAGE RAPIDE (2 ÉTAPES)

### Étape 1 : Modifier le mot de passe

Ouvrir le fichier `.env` et remplacer **UNE SEULE CHOSE** :

```env
# AVANT (ligne 23)
DATABASE_URL=postgresql+asyncpg://doadmin:VOTRE_MOT_DE_PASSE_ICI@db-postgresql...

# APRÈS
DATABASE_URL=postgresql+asyncpg://doadmin:ton_vrai_mot_de_passe@db-postgresql...
```

### Étape 2 : Lancer

**Option A — Avec Docker (recommandé) :**
```bash
chmod +x start.sh
./start.sh
```

**Option B — Sans Docker :**
```bash
chmod +x start-direct.sh
./start-direct.sh
```

---

## ✅ VÉRIFICATION

Après démarrage, tester :

```bash
# Health check
curl http://localhost:8000/health

# Réponse attendue :
{"status":"healthy","version":"82.0.0","signal":"4.44s","frequency":"444Hz"}
```

Ou ouvrir dans le navigateur :
- **API Docs** : http://localhost:8000/docs
- **Health** : http://localhost:8000/health

---

## 📋 CONFIGURATION COMPLÈTE (.env)

Le fichier `.env` est **100% configuré** sauf le mot de passe. Voici ce qu'il contient :

| Section | Status |
|---------|--------|
| 🖥️ Server (port 8000) | ✅ Prêt |
| 🗄️ Database URL | ⚠️ MOT DE PASSE À ENTRER |
| 🔐 JWT Auth | ✅ Clé générée |
| 🤖 AI Providers | ⏸️ Optionnel |
| 🌐 CORS | ✅ Vercel autorisé |
| 🎵 Résonance 444Hz | ✅ Configuré |
| 🏛️ Gouvernance | ✅ Human sovereignty |
| 📡 WebSocket 4.44s | ✅ Prêt |

---

## 🔧 COMMANDES UTILES

### Docker

```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Voir les logs
docker logs -f chenu-api

# Redémarrer
docker compose restart

# Rebuild
docker compose build --no-cache
```

### Sans Docker

```bash
# Activer l'environnement
source venv/bin/activate

# Démarrer
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Avec plusieurs workers (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🌐 ENDPOINTS PRINCIPAUX

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/api/v2/auth/login` | POST | Authentification |
| `/api/v2/spheres` | GET | 10 Sphères |
| `/api/v2/agents` | GET | 168+ Agents |
| `/api/v2/nova/chat` | POST | IA NOVA |
| `/ws` | WebSocket | Signal 4.44s |

---

## 🔒 SSL / HTTPS (Production)

Pour activer HTTPS :

1. Obtenir certificats SSL (Let's Encrypt) :
```bash
certbot certonly --standalone -d ton-domaine.com
```

2. Copier les certificats :
```bash
cp /etc/letsencrypt/live/ton-domaine.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/ton-domaine.com/privkey.pem nginx/ssl/
```

3. Démarrer avec nginx :
```bash
docker compose up -d
```

---

## 🎵 CONSTANTES AT·OM

| Constante | Valeur |
|-----------|--------|
| Fréquence d'ancrage | 444 Hz |
| Intervalle signal | 4.44 s |
| Séquence sacrée | 3-6-9-12 |
| Balance ratio | 30 |
| Cube Métatron | 1728 (12³) |

---

## ⚠️ TROUBLESHOOTING

### Erreur de connexion DB
```
asyncpg.exceptions.InvalidPasswordError
```
→ Vérifier le mot de passe dans `DATABASE_URL`

### Port déjà utilisé
```
Address already in use
```
→ `docker compose down` ou `kill $(lsof -t -i:8000)`

### Permission denied
```
./start.sh: Permission denied
```
→ `chmod +x start.sh`

---

## 📞 SUPPORT

- **Database** : DigitalOcean NYC9
- **6500 agents** : Déjà injectés
- **Frontend** : Vercel (atom.vercel.app)

---

*MU·A·RA·TA — Le chemin du retour*
