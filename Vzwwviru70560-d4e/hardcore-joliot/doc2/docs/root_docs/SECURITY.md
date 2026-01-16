# 🔐 CHE·NU™ - SECURITY & COMPLIANCE

**Version:** V41  
**Status:** POST-MVP ENHANCEMENTS – RECOMMENDED BY GROK  
**Priority:** CRITICAL  

---

## 🎯 OBJECTIF

Assurer production-grade security + conformité réglementaire complète (GDPR, EU AI Act 2025).

---

## 📋 PLAN SÉCURITÉ

### 1. Tests de Pénétration
**Status:** TODO

#### Scope
- Infrastructure (AWS/GCP)
- Backend API (FastAPI)
- Frontend (React/PWA)
- Database (PostgreSQL)
- Cache (Redis)

#### Pentest Checklist
- [ ] OWASP Top 10 compliance
- [ ] SQL injection tests
- [ ] XSS (Cross-Site Scripting) tests
- [ ] CSRF (Cross-Site Request Forgery) tests
- [ ] Authentication bypass attempts
- [ ] Authorization escalation tests
- [ ] Session hijacking tests
- [ ] API rate limiting bypass
- [ ] File upload vulnerabilities
- [ ] Dependency vulnerabilities scan

#### Vendor
- [ ] Engager pentest externe (budget: €10K)
- [ ] Quarterly pentests (post-launch)
- [ ] Bug bounty program (HackerOne)

#### KPI
- 0 vulnerabilités critiques
- <3 vulnerabilités moyennes
- Report complet sous 30 jours

---

### 2. Audit Sécurité Complet
**Status:** TODO

#### Code Audit
- [ ] SAST (Static Application Security Testing)
- [ ] DAST (Dynamic Application Security Testing)
- [ ] Dependency scanning (Snyk, Dependabot)
- [ ] Secret scanning (GitGuardian)
- [ ] License compliance

#### Infrastructure Audit
- [ ] Cloud security posture (AWS Security Hub)
- [ ] Network segmentation
- [ ] Firewall rules review
- [ ] IAM policies review
- [ ] Logging & monitoring

#### Tools
- SonarQube (code quality + security)
- Snyk (dependencies)
- AWS GuardDuty (threat detection)
- CloudFlare (DDoS protection)

---

### 3. Conformité GDPR
**Status:** TODO

#### GDPR Requirements
- [ ] **Right to access** - User data export
- [ ] **Right to erasure** - Account deletion + data purge
- [ ] **Right to portability** - Data export (JSON/CSV)
- [ ] **Right to rectification** - Profile editing
- [ ] **Consent management** - Explicit opt-ins
- [ ] **Data minimization** - Collect only necessary data
- [ ] **Privacy by design** - Default privacy settings
- [ ] **DPO** (Data Protection Officer) - Designate contact

#### Implementation
```python
# backend/gdpr/data_export.py
async def export_user_data(user_id: str) -> dict:
    """Export all user data (GDPR Article 20)"""
    return {
        "profile": {...},
        "threads": [...],
        "agents": [...],
        "history": [...]
    }

# backend/gdpr/data_deletion.py
async def delete_user_data(user_id: str):
    """Permanent data deletion (GDPR Article 17)"""
    # Cascade delete all related data
    # Anonymize audit logs
    # Remove from backups (30 days)
```

#### Documentation
- Privacy Policy (FR + EN)
- Terms of Service
- Cookie Policy
- Data Processing Agreement (DPA)

#### KPI
- GDPR compliance: 100%
- Data requests response: <30 days
- Consent rate: >95%

---

### 4. Conformité EU AI Act 2025
**Status:** TODO

#### Prohibited Practices Check
CHE·NU vérifie qu'aucun agent ne:
- [ ] Manipule comportement (subliminal techniques)
- [ ] Exploite vulnérabilités (enfants, handicap)
- [ ] Social scoring gouvernemental
- [ ] Biometric categorization (sauf exceptions)

#### High-Risk AI Systems
CHE·NU agents = **High-risk** (AI decision-making)

Requirements:
- [ ] Risk management system
- [ ] Data governance
- [ ] Technical documentation
- [ ] Record-keeping (logs)
- [ ] Transparency to users
- [ ] Human oversight
- [ ] Accuracy, robustness, cybersecurity

#### Implementation
```python
# backend/compliance/eu_ai_act.py
class AgentRiskAssessment:
    """EU AI Act Article 9 - Risk Management"""
    
    def assess_agent(self, agent_id: str) -> RiskLevel:
        # Risk-based classification
        if agent.involves_minors:
            return RiskLevel.PROHIBITED
        if agent.makes_decisions:
            return RiskLevel.HIGH
        return RiskLevel.LIMITED
    
    def require_human_oversight(self, execution_id: str):
        """Article 14 - Human oversight"""
        if execution.risk == RiskLevel.HIGH:
            await approval_queue.add(execution)
```

#### Documentation
- AI Act Compliance Statement
- Agent Risk Register
- Human Oversight Procedures
- Transparency Notices

#### KPI
- Prohibited practices: 0
- High-risk agents with oversight: 100%
- Compliance audits: quarterly

---

### 5. Chiffrement Données
**Status:** PARTIAL (in-transit only)

#### At-Rest Encryption
- [ ] Database encryption (PostgreSQL TDE)
- [ ] File storage encryption (S3 SSE)
- [ ] Backup encryption (AES-256)
- [ ] Key rotation (quarterly)

#### In-Transit Encryption
- [x] HTTPS/TLS 1.3 (Cloudflare)
- [x] WebSocket SSL
- [ ] mTLS for microservices
- [ ] VPN for internal services

#### Key Management
- [ ] AWS KMS (Key Management Service)
- [ ] Separate keys per environment
- [ ] Automatic key rotation
- [ ] Audit key usage

```python
# backend/security/encryption_at_rest.py
from cryptography.fernet import Fernet
import boto3

class EncryptionService:
    def __init__(self):
        self.kms = boto3.client('kms')
        self.key_id = os.getenv('KMS_KEY_ID')
    
    async def encrypt_sensitive_field(self, data: str) -> str:
        """Encrypt PII before DB storage"""
        response = self.kms.encrypt(
            KeyId=self.key_id,
            Plaintext=data.encode()
        )
        return base64.b64encode(response['CiphertextBlob']).decode()
    
    async def decrypt_sensitive_field(self, encrypted: str) -> str:
        """Decrypt PII from DB"""
        blob = base64.b64decode(encrypted)
        response = self.kms.decrypt(CiphertextBlob=blob)
        return response['Plaintext'].decode()
```

---

### 6. Gestion Secrets
**Status:** TODO

#### Current Issues
- ❌ Secrets in .env files
- ❌ API keys in code
- ❌ No rotation policy

#### Target Solution
- [ ] AWS Secrets Manager / HashiCorp Vault
- [ ] Automatic secret injection (K8s)
- [ ] Secret rotation (30 days)
- [ ] Audit secret access

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: chenu-secrets
type: Opaque
data:
  database-url: <base64>
  stripe-key: <base64>
  jwt-secret: <base64>
```

```python
# backend/config/secrets.py
import boto3

class SecretsManager:
    def __init__(self):
        self.client = boto3.client('secretsmanager')
    
    def get_secret(self, secret_name: str) -> str:
        response = self.client.get_secret_value(SecretId=secret_name)
        return response['SecretString']

# Usage
DATABASE_URL = secrets_manager.get_secret('chenu/database-url')
```

---

### 7. Risk-Based Governance Agents
**Status:** TODO

#### Agent Risk Classification

| Level | Risk | Examples | Governance |
|-------|------|----------|------------|
| **L0** | Minimal | Read-only agents | Auto-execute |
| **L1** | Low | Simple writes | Auto-execute |
| **L2** | Medium | CRM updates | Require approval |
| **L3** | High | Financial transactions | Require approval + audit |

#### Implementation
```python
# backend/agents/governance.py
class AgentGovernance:
    async def execute_with_governance(
        self,
        agent_id: str,
        capability: str,
        params: dict
    ):
        agent = self.get_agent(agent_id)
        
        # Risk assessment
        risk_level = self.assess_risk(agent, capability)
        
        if risk_level >= RiskLevel.MEDIUM:
            # Require human approval
            approval = await self.request_approval(agent_id, params)
            if not approval.approved:
                raise GovernanceException("Execution denied")
        
        # Execute with audit trail
        result = await agent.execute(capability, params)
        await self.log_execution(agent_id, result, risk_level)
        
        return result
```

---

### 8. Audit Trail Complet
**Status:** PARTIAL

#### Current State
- Logs basiques (access logs)
- Metrics Prometheus

#### Target State
- [ ] All agent executions logged
- [ ] All user actions logged
- [ ] All data modifications logged
- [ ] Immutable audit logs
- [ ] Retention: 7 years (compliance)

```python
# backend/audit/audit_trail.py
class AuditTrail:
    async def log_action(
        self,
        user_id: str,
        action: str,
        resource: str,
        details: dict
    ):
        entry = {
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details,
            "ip_address": request.client.host,
            "user_agent": request.headers.get("User-Agent")
        }
        
        # Store in immutable log (S3 + Glacier)
        await self.store_audit_log(entry)
        
        # Index in Elasticsearch for search
        await self.index_log(entry)
```

---

## 🛡️ SECURITY HEADERS

```nginx
# nginx.conf
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

---

## 🔑 2FA OBLIGATOIRE

```python
# backend/auth/two_factor.py
import pyotp

class TwoFactorAuth:
    async def enable_2fa(self, user_id: str) -> str:
        """Generate TOTP secret"""
        secret = pyotp.random_base32()
        await db.users.update(user_id, totp_secret=secret)
        
        # Return QR code for authenticator app
        uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="CHE·NU"
        )
        return qrcode.make(uri)
    
    async def verify_2fa(self, user_id: str, code: str) -> bool:
        user = await db.users.get(user_id)
        totp = pyotp.TOTP(user.totp_secret)
        return totp.verify(code, valid_window=1)
```

---

## 📊 MÉTRIQUES SÉCURITÉ

### Dashboards
- Vulnerabilities (SonarQube)
- Failed login attempts
- 2FA adoption rate
- GDPR requests (export/delete)
- Audit trail anomalies

### Alerts
- Critical vulnerability detected
- Unusual login pattern
- Failed 2FA attempts (>3)
- Unauthorized API access
- Data export spike

---

## 📅 TIMELINE V41

| Semaine | Tâche |
|---------|-------|
| **W1-2** | Pentest externe + report |
| **W3-4** | Fix vulnerabilités critiques |
| **W5-6** | GDPR implementation |
| **W7-8** | EU AI Act compliance |
| **W9-10** | Encryption at-rest |
| **W11-12** | Secrets management |
| **W13-14** | Agent risk governance |
| **W15-16** | Audit trail complet |
| **W17-18** | 2FA rollout |
| **W19-20** | Security review finale |

---

## ✅ VALIDATION CHECKLIST

### Pre-Launch
- [ ] Pentest: 0 critiques
- [ ] GDPR: 100% compliant
- [ ] EU AI Act: 100% compliant
- [ ] Encryption: at-rest + in-transit
- [ ] Secrets: Vault/Secrets Manager
- [ ] 2FA: Enabled for all users
- [ ] Audit trail: 100% actions logged
- [ ] Security headers: All configured
- [ ] Dependency scanning: Automated
- [ ] Incident response plan: Documented

---

*CHE·NU™ Security & Compliance — V41*  
***GOVERNED. SECURE. COMPLIANT.*** 🔐
