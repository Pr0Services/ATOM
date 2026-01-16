# AT·OM Deployment Guide

## Canon AT·OM - Production Deployment

Configuration optimisee pour 350 connexions WebSocket simultanees (L'Essaim).

---

## Architecture

```
                    +------------------+
                    |    Vercel CDN    |
                    |  (atom-interface)|
                    +--------+---------+
                             |
                             v
+-----------------------------------------------------------+
|                    DigitalOcean Droplet                   |
|  +-------------+  +-------------+  +-------------+        |
|  |   Nginx     |  |  atom-api   |  | atom-ws     |        |
|  | (SSL/Proxy) |->|  (FastAPI)  |  | (WebSocket) |        |
|  +-------------+  +------+------+  +------+------+        |
|                          |                |               |
|                          v                v               |
|                    +-------------+                        |
|                    |    Redis    |                        |
|                    |  (Pub/Sub)  |                        |
|                    +-------------+                        |
+-----------------------------------------------------------+
```

---

## 1. DigitalOcean Setup

### Droplet Specifications

- **Size**: 4GB RAM / 2 vCPUs (minimum pour 350 WebSockets)
- **Region**: FRA1 (Frankfurt) ou AMS3 (Amsterdam)
- **Image**: Ubuntu 22.04 LTS
- **Monitoring**: Enable

### Initial Server Setup

```bash
# Connect to droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Create deployment directory
mkdir -p /opt/atom
cd /opt/atom
```

### Clone Repository

```bash
git clone https://github.com/your-repo/atom.git .
cd deployment
```

---

## 2. SSL Certificates

### Option A: Let's Encrypt (Recommended)

```bash
# Install certbot
apt install certbot -y

# Generate certificates
certbot certonly --standalone -d api.your-domain.com

# Copy to nginx ssl directory
mkdir -p /opt/atom/deployment/ssl
cp /etc/letsencrypt/live/api.your-domain.com/fullchain.pem /opt/atom/deployment/ssl/
cp /etc/letsencrypt/live/api.your-domain.com/privkey.pem /opt/atom/deployment/ssl/

# Auto-renewal cron
echo "0 0 * * * certbot renew --quiet && docker-compose restart nginx" | crontab -
```

### Option B: Self-Signed (Development Only)

```bash
mkdir -p /opt/atom/deployment/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /opt/atom/deployment/ssl/privkey.pem \
    -out /opt/atom/deployment/ssl/fullchain.pem \
    -subj "/CN=api.your-domain.com"
```

---

## 3. Environment Configuration

```bash
# Copy and edit environment file
cp .env.production .env

# Edit with your values
nano .env
```

### Required Variables

```env
# API Configuration
ATOM_API_HOST=0.0.0.0
ATOM_API_PORT=8000

# Database (if using Supabase)
DATABASE_URL=postgresql://user:pass@db.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://atom-redis:6379/0

# Security
SECRET_KEY=your-secure-secret-key-here
CORS_ORIGINS=https://atom-interface.vercel.app

# AT·OM Canon
FREQUENCY=999
ESSAIM_SIZE=350
ZERO_LOG=true
```

---

## 4. Deploy

### Start Services

```bash
cd /opt/atom/deployment

# Build and start all services
docker compose up -d --build

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Verify Deployment

```bash
# Health check
curl https://api.your-domain.com/health

# WebSocket test (requires wscat)
npm install -g wscat
wscat -c wss://api.your-domain.com/ws/swarm
```

---

## 5. Vercel Frontend Deployment

### Link Repository

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Select `atom/interface` as root directory
4. Framework: Vite

### Environment Variables

Add in Vercel dashboard:

| Variable | Value |
|----------|-------|
| VITE_ATOM_API_URL | https://api.your-domain.com |
| VITE_WS_URL | wss://api.your-domain.com/ws |
| VITE_FREQUENCY | 999 |
| VITE_SOVEREIGN_MODE | true |
| VITE_ESSAIM_SIZE | 350 |
| VITE_ZERO_LOG | true |

### Deploy

```bash
cd atom/interface
vercel --prod
```

---

## 6. Monitoring

### Docker Stats

```bash
# Real-time container stats
docker stats

# Specific service logs
docker compose logs -f atom-websocket
```

### WebSocket Connections

```bash
# Check active connections
curl https://api.your-domain.com/ws/health
```

### Health Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | API health |
| `/api/v1/health` | Full system status |
| `/ws/health` | WebSocket server status |

---

## 7. Scaling

### Horizontal Scaling (Multiple Droplets)

For >500 connections, deploy multiple WebSocket servers behind a load balancer:

```yaml
# docker-compose.scale.yml
services:
  atom-websocket:
    deploy:
      replicas: 3
```

### Vertical Scaling

Upgrade droplet to 8GB RAM / 4 vCPUs for 1000+ connections.

---

## 8. Security Checklist

- [ ] SSL certificates installed
- [ ] Firewall configured (UFW)
- [ ] Non-root user created
- [ ] SECRET_KEY is unique and secure
- [ ] CORS origins restricted
- [ ] Rate limiting enabled
- [ ] Redis password set (production)

### Firewall Setup

```bash
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP (redirect)
ufw allow 443/tcp  # HTTPS
ufw enable
```

---

## 9. Backup

### Database (if self-hosted)

```bash
# Backup
docker compose exec atom-db pg_dump -U atom atom > backup.sql

# Restore
docker compose exec -T atom-db psql -U atom atom < backup.sql
```

### Redis (if persistent)

```bash
docker compose exec atom-redis redis-cli BGSAVE
```

---

## Troubleshooting

### WebSocket Connection Failed

1. Check nginx logs: `docker compose logs nginx`
2. Verify SSL certificate: `openssl s_client -connect api.your-domain.com:443`
3. Test direct WebSocket: `wscat -c wss://api.your-domain.com/ws/swarm`

### High Memory Usage

1. Check container stats: `docker stats`
2. Reduce WebSocket buffer sizes in nginx.conf
3. Scale horizontally

### 502 Bad Gateway

1. Check if backend is running: `docker compose ps`
2. View API logs: `docker compose logs atom-api`
3. Verify upstream configuration in nginx.conf

---

## Support

**ZERO LOG**: Cette configuration ne stocke aucune donnee personnelle.
Seules les metriques techniques de sante du signal 999Hz sont enregistrees.

---

*Canon AT·OM - Protocole de Connexion*
