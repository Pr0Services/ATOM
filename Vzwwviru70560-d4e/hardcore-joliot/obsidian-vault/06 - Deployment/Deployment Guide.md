# Deployment Guide

> Guide complet de deploiement AT·OM (DigitalOcean + Vercel)

---

## Architecture de Deploiement

```
┌─────────────────────────────────────────────┐
│              Vercel (Frontend)              │
│         atom-interface.vercel.app           │
│     React + Vite + TailwindCSS (CDN)       │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         DigitalOcean Droplet (Backend)      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │  Nginx  │──│   API   │──│   WS    │     │
│  │ :80/443 │  │  :8000  │  │  :8001  │     │
│  └─────────┘  └────┬────┘  └────┬────┘     │
│                    │            │           │
│              ┌─────┴────────────┴─────┐    │
│              │        Redis           │    │
│              │        :6379           │    │
│              └────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Pre-requis

### Comptes necessaires
- [ ] DigitalOcean account
- [ ] Vercel account
- [ ] Domaine configure

### Outils locaux
```bash
# Docker
curl -fsSL https://get.docker.com | sh

# Vercel CLI
npm i -g vercel
```

---

## 1. DigitalOcean Setup

### Creer le Droplet

| Parametre | Valeur |
|-----------|--------|
| Region | FRA1 ou AMS3 |
| Image | Ubuntu 22.04 LTS |
| Size | 4GB / 2 vCPUs |
| Monitoring | Enable |

### Configuration initiale

```bash
# SSH au serveur
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose-plugin -y

# Create deployment directory
mkdir -p /opt/atom
cd /opt/atom

# Clone repository
git clone https://github.com/your-repo/atom.git .
```

---

## 2. SSL Certificates

### Let's Encrypt (Production)

```bash
apt install certbot -y

certbot certonly --standalone -d api.your-domain.com

mkdir -p /opt/atom/deployment/ssl
cp /etc/letsencrypt/live/api.your-domain.com/fullchain.pem /opt/atom/deployment/ssl/
cp /etc/letsencrypt/live/api.your-domain.com/privkey.pem /opt/atom/deployment/ssl/

# Auto-renewal
echo "0 0 * * * certbot renew --quiet && docker compose restart nginx" | crontab -
```

---

## 3. Environment Configuration

### Fichier .env

```bash
cd /opt/atom/deployment
cp .env.production .env
nano .env
```

### Variables requises

```env
# API
ATOM_API_HOST=0.0.0.0
ATOM_API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@db.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://atom-redis:6379/0

# Security
SECRET_KEY=your-secure-secret-key
CORS_ORIGINS=https://atom-interface.vercel.app

# AT·OM Canon
FREQUENCY=999
ESSAIM_SIZE=350
ZERO_LOG=true
```

---

## 4. Docker Compose

### Lancer les services

```bash
cd /opt/atom/deployment

# Build et start
docker compose up -d --build

# Verifier
docker compose ps

# Logs
docker compose logs -f
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| atom-api | 8000 | API REST |
| atom-websocket | 8001 | WebSocket L'Essaim |
| atom-redis | 6379 | Cache/Pub-Sub |
| atom-nginx | 80/443 | Reverse Proxy |

---

## 5. Vercel Frontend

### Configuration

```bash
cd atom/interface
vercel login
vercel link
```

### Variables d'environnement (Vercel Dashboard)

| Variable | Valeur |
|----------|--------|
| VITE_ATOM_API_URL | https://api.your-domain.com |
| VITE_WS_URL | wss://api.your-domain.com/ws |
| VITE_FREQUENCY | 999 |
| VITE_SOVEREIGN_MODE | true |
| VITE_ESSAIM_SIZE | 350 |
| VITE_ZERO_LOG | true |

### Deployer

```bash
vercel --prod
```

---

## 6. Verification

### Health Checks

```bash
# API Health
curl https://api.your-domain.com/health

# WebSocket Test
npm i -g wscat
wscat -c wss://api.your-domain.com/ws/swarm
```

### Reponse attendue

```json
{
  "status": "healthy",
  "frequency": 999,
  "essaim_size": 350,
  "connections": 0
}
```

---

## 7. Firewall

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

---

## 8. Monitoring

### Docker Stats

```bash
docker stats
```

### Logs en temps reel

```bash
docker compose logs -f atom-websocket
```

---

## Troubleshooting

### WebSocket ne connecte pas
1. Verifier nginx logs: `docker compose logs nginx`
2. Verifier SSL: `openssl s_client -connect api.domain.com:443`
3. Test direct: `wscat -c wss://api.domain.com/ws/swarm`

### 502 Bad Gateway
1. Backend running? `docker compose ps`
2. API logs: `docker compose logs atom-api`
3. Verifier upstream nginx

### High Memory
1. Stats: `docker stats`
2. Reduce buffer sizes
3. Scale horizontally

---

## Liens

- [[System Architecture]]
- [[WebSocket Server]]
- [[Security Protocol]]

#deployment #digitalocean #vercel #docker
