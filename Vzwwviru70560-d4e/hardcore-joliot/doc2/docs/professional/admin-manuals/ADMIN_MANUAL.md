# CHE·NU™ ADMINISTRATOR MANUAL
## Complete Guide for System Administrators

**Version:** 1.0.0  
**Last Updated:** December 20, 2025  
**For:** CHE·NU v41.6+ Enterprise

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                  CHE·NU™ ADMINISTRATOR MANUAL                                 ║
║                                                                               ║
║        System Administration, User Management & Operations                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Admin Dashboard Overview](#admin-dashboard-overview)
2. [User Management](#user-management)
3. [System Configuration](#system-configuration)
4. [Monitoring & Analytics](#monitoring--analytics)
5. [Security Administration](#security-administration)
6. [Backup & Recovery](#backup--recovery)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Admin Dashboard Overview

### Accessing Admin Panel

**URL:** `https://your-instance.chenu.com/admin`

**Permissions required:**
- Role: `admin` or `owner`
- MFA: **Required** (cannot be disabled for admins)
- IP whitelist: Optional (recommended for production)

### Dashboard Sections

```
┌────────────────────────────────────────────┐
│ CHE·NU Admin Dashboard                     │
├────────────────────────────────────────────┤
│                                            │
│ Quick Stats:                               │
│ ├─ Active Users:        127 ↑ +12         │
│ ├─ Total Threads:       3,451 ↑ +89       │
│ ├─ Token Usage:         1.2M / 5M (24%)   │
│ └─ System Health:       ✅ All systems OK  │
│                                            │
│ Recent Activity:                           │
│ ├─ Login spike detected   [View]          │
│ ├─ 3 new users joined     [Manage]        │
│ └─ Backup completed       [Verify]        │
│                                            │
│ Alerts:                                    │
│ ⚠️  Token budget at 80%   [Increase]       │
│ ⚠️  SSL cert expires in 7d [Renew]         │
│                                            │
└────────────────────────────────────────────┘
```

### Key Metrics (Real-time)

**System Health:**
- API Response Time: `<100ms` ✅
- Database Connections: `45/100` ✅
- Cache Hit Rate: `85%` ✅
- Error Rate: `0.02%` ✅

**User Activity:**
- Active Sessions: `127`
- Requests/Minute: `1,234`
- Failed Logins: `2` (last hour)
- MFA Adoption: `98%` ✅

**Resource Usage:**
- CPU: `34%`
- Memory: `6.2GB / 16GB`
- Disk: `145GB / 500GB`
- Bandwidth: `12Mbps`

---

## User Management

### User Roles

CHE·NU has four predefined roles:

| Role | Permissions | Use Case |
|------|-------------|----------|
| **User** | Access own data, create threads | Regular users |
| **Manager** | View team data, run reports | Team leads |
| **Admin** | Full system access except billing | IT admins |
| **Owner** | Full access including billing | Company owner |

**Role hierarchy:**
```
Owner
  └─ Admin
      └─ Manager
          └─ User
```

### Creating Users

**Method 1: Admin Panel**
1. Go to Admin → Users
2. Click "Add User"
3. Fill in:
   - Email (required)
   - Name (required)
   - Role (default: User)
   - Send invite: Yes/No
4. Click "Create"

**Method 2: Bulk Import**
1. Go to Admin → Users → Import
2. Download CSV template
3. Fill in user data
4. Upload CSV
5. Review and confirm

**CSV Format:**
```csv
email,name,role,department
john@example.com,John Doe,user,Engineering
jane@example.com,Jane Smith,manager,Marketing
admin@example.com,Admin User,admin,IT
```

**Method 3: API**
```bash
curl -X POST https://api.chenu.com/v1/admin/users \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "New User",
    "role": "user",
    "send_invite": true
  }'
```

### Managing Users

**Edit User:**
1. Find user in list
2. Click edit icon
3. Modify fields:
   - Name
   - Email
   - Role
   - Status (active/suspended)
4. Save changes

**Suspend User:**
- **Purpose:** Temporarily disable access
- **Effect:** User cannot login, tokens frozen
- **Duration:** Until manually reactivated
- **Use case:** Security investigation, policy violation

**Delete User:**
- **Warning:** Permanent action!
- **Effect:** User deleted, data retained (audit)
- **Process:**
  1. Confirm deletion reason
  2. Transfer ownership of threads
  3. Final confirmation
  4. User deleted

**Reset Password:**
1. Find user
2. Click "Reset Password"
3. Options:
   - Send reset email (user chooses new password)
   - Generate temp password (admin sets)

**Force MFA Setup:**
1. Select user
2. Click "Require MFA"
3. User must set up MFA on next login
4. Cannot access system until MFA enabled

### User Activity Monitoring

**View user activity:**
1. Admin → Users → [Select User]
2. Activity tab shows:
   - Login history
   - Thread activity
   - Token usage
   - Failed attempts
   - Device history

**Audit Log:**
```
Dec 20, 2025 10:15:23 - Login (Chrome, MacOS)
Dec 20, 2025 10:16:45 - Created thread "Q1 Planning"
Dec 20, 2025 10:45:12 - Uploaded file (report.pdf)
Dec 20, 2025 11:30:00 - Logout
```

**Red Flags:**
- Multiple failed login attempts
- Login from unusual location
- Unusual API usage spikes
- Access to restricted data

**Automated Alerts:**
- Settings → Alerts → User Monitoring
- Configure thresholds:
  - Failed logins: >5 in 10 min
  - Geographic anomaly: Different country
  - API spike: >1000 req/min
  - Privilege escalation attempt

---

## System Configuration

### General Settings

**Company Information:**
```
Admin → Settings → General

Company Name:    Acme Corp
Primary Domain:  acme.com
Support Email:   support@acme.com
Timezone:        America/New_York
Language:        English (US)
```

**Instance Settings:**
```
Admin → Settings → Instance

Instance Name:     Acme CHE·NU
Custom Domain:     chenu.acme.com
SSL Certificate:   Auto-renew (Let's Encrypt)
Maintenance Mode:  Off
```

### Authentication Settings

**Password Policy:**
```
Admin → Settings → Security → Password Policy

Minimum Length:         12 characters  ✅
Require Uppercase:      Yes            ✅
Require Lowercase:      Yes            ✅
Require Numbers:        Yes            ✅
Require Symbols:        Yes            ✅
Password History:       Last 5         ✅
Expiration:             90 days        (optional)
Max Login Attempts:     5
Lockout Duration:       15 minutes
```

**MFA Policy:**
```
Admin → Settings → Security → MFA

Enforce MFA:            Yes (all users)  ✅
Grace Period:           7 days
Backup Codes:           10 per user
MFA Methods:            TOTP only
```

**Session Management:**
```
Admin → Settings → Security → Sessions

Session Timeout:        24 hours
Idle Timeout:           30 minutes
Concurrent Sessions:    3 per user
Remember Me:            Disabled (recommended)
```

### Email Configuration

**SMTP Settings:**
```
Admin → Settings → Email

SMTP Host:        smtp.sendgrid.net
SMTP Port:        587 (TLS)
Username:         apikey
Password:         ••••••••••••••••
From Address:     noreply@acme.com
From Name:        Acme CHE·NU
```

**Test Email:**
1. Enter settings
2. Click "Send Test Email"
3. Check inbox
4. Verify formatting

**Email Templates:**
- Welcome email
- Password reset
- MFA setup
- Security alerts
- Weekly digest

**Customize templates:**
1. Admin → Settings → Email → Templates
2. Select template
3. Edit HTML/text
4. Use variables: `{{user.name}}`, `{{company.name}}`
5. Preview and save

### Integration Settings

**SSO (Single Sign-On):**
```
Admin → Settings → Integrations → SSO

Provider:         Google Workspace
Client ID:        ••••••••••••••••
Client Secret:    ••••••••••••••••
Allowed Domains:  acme.com
Auto-provision:   Yes
Default Role:     user
```

**Supported providers:**
- Google Workspace
- Microsoft Azure AD
- Okta
- Auth0
- SAML 2.0 (custom)

**Webhooks:**
```
Admin → Settings → Integrations → Webhooks

Add webhook:
URL:              https://your-app.com/webhook
Events:           user.created, thread.created
Secret:           ••••••••••••••••
Status:           Active ✅
```

**API Rate Limits:**
```
Admin → Settings → API

Default Limit:    100 req/min   (per user)
Admin Limit:      1000 req/min  (for admins)
Burst:            200 requests  (short spike)
Throttle After:   Rate limit reached
Response:         429 Too Many Requests
```

---

## Monitoring & Analytics

### System Monitoring

**Health Dashboard:**
```
Admin → Monitoring → Health

┌────────────────────────────────────┐
│ API                     ✅ Healthy  │
│ ├─ Response Time:       87ms       │
│ ├─ Success Rate:        99.98%     │
│ └─ Error Rate:          0.02%      │
│                                    │
│ Database                ✅ Healthy  │
│ ├─ Connections:         45/100     │
│ ├─ Query Time:          8ms        │
│ └─ Cache Hit:           85%        │
│                                    │
│ Redis Cache             ✅ Healthy  │
│ ├─ Memory:              2.1GB/4GB  │
│ ├─ Hit Rate:            85%        │
│ └─ Evictions:           0          │
│                                    │
│ Background Jobs         ✅ Healthy  │
│ ├─ Queue Size:          12         │
│ ├─ Processing:          3          │
│ └─ Failed:              0          │
└────────────────────────────────────┘
```

**Performance Metrics:**
```
Admin → Monitoring → Performance

Response Times (p95):
├─ API Endpoints:        98ms  ✅
├─ GraphQL Queries:      145ms ✅
├─ Database Queries:     12ms  ✅
└─ Cache Lookups:        2ms   ✅

Throughput:
├─ Requests/sec:         45
├─ DB Queries/sec:       234
└─ Cache Ops/sec:        890
```

**Error Tracking:**
```
Admin → Monitoring → Errors

Last 24 hours:
├─ Total Errors:         23
├─ 4xx Errors:          18  (user errors)
├─ 5xx Errors:          5   (server errors)
└─ Critical:            0   ✅

Top Errors:
1. 404 Not Found         12x
2. 401 Unauthorized      6x
3. 500 Internal Error    3x
```

### Usage Analytics

**User Activity:**
```
Admin → Analytics → Users

Active Users (7 days):   89  ↑ +12
New Signups:            15  ↑ +3
Daily Active (DAU):     67  ↑ +8
Weekly Active (WAU):    89  →
Monthly Active (MAU):   127 ↑ +12

Engagement:
├─ Avg Sessions/User:   3.2
├─ Avg Session Time:    24min
├─ Threads/User:        4.5
└─ Messages/User:       18.3
```

**Token Usage:**
```
Admin → Analytics → Tokens

Total Allocation:       5,000,000
Used (Month):          1,234,567  (24.7%)
Remaining:             3,765,433  (75.3%)

Top Users:
1. john@acme.com       45,000
2. jane@acme.com       38,500
3. admin@acme.com      12,300

Top Spheres:
1. Business            567,000
2. Personal            234,000
3. Scholar             156,000
```

**Feature Usage:**
```
Admin → Analytics → Features

Most Used:
├─ Threads:            3,451 created
├─ Agents:            1,234 executions
├─ Files:             892 uploads
└─ Meetings:          234 scheduled

Adoption Rates:
├─ MFA:               98%  ✅
├─ Mobile App:        45%
├─ API:               23%
└─ Integrations:      67%
```

### Custom Reports

**Create Report:**
1. Admin → Analytics → Reports → New
2. Select metrics:
   - User growth
   - Token usage
   - Feature adoption
   - Error rates
3. Set date range
4. Add filters
5. Schedule (daily/weekly/monthly)
6. Save and run

**Export Data:**
- CSV download
- PDF report
- API access
- Data warehouse integration

---

## Security Administration

### Access Control

**Role-Based Access Control (RBAC):**
```
Admin → Security → Roles

Custom Roles:
├─ Data Analyst
│   ├─ View all threads
│   ├─ Run reports
│   └─ Export data
├─ Support Agent
│   ├─ View user profiles
│   ├─ Reset passwords
│   └─ View audit logs
└─ Developer
    ├─ API access
    ├─ Webhook management
    └─ Integration config
```

**Permission Matrix:**

| Permission | User | Manager | Admin | Owner |
|------------|------|---------|-------|-------|
| Create threads | ✅ | ✅ | ✅ | ✅ |
| View own data | ✅ | ✅ | ✅ | ✅ |
| View team data | ❌ | ✅ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ✅ | ✅ |
| System config | ❌ | ❌ | ✅ | ✅ |
| Billing | ❌ | ❌ | ❌ | ✅ |

### Audit Logs

**View Audit Logs:**
```
Admin → Security → Audit

Filters:
├─ User:           [All Users ▾]
├─ Event Type:     [All Events ▾]
├─ Date Range:     [Last 7 days ▾]
├─ Severity:       [All ▾]
└─ [Search...]     [Export]

Recent Events:
┌───────────────────────────────────────────────┐
│ Dec 20 10:15  LOGIN_SUCCESS                   │
│ User: john@acme.com                           │
│ IP: 192.168.1.1                               │
│ Device: Chrome, MacOS                         │
├───────────────────────────────────────────────┤
│ Dec 20 10:16  THREAD_CREATE                   │
│ User: john@acme.com                           │
│ Thread: "Q1 Planning"                         │
│ Sphere: Business                              │
├───────────────────────────────────────────────┤
│ Dec 20 10:45  USER_ROLE_CHANGE                │
│ Admin: admin@acme.com                         │
│ Target: jane@acme.com                         │
│ Change: user → manager                        │
└───────────────────────────────────────────────┘
```

**Audit Event Types:**
- Authentication (login, logout, MFA)
- User management (create, update, delete)
- Data access (view, export, delete)
- System changes (config, integrations)
- Security events (failed login, permission denied)

**Compliance Reports:**
- SOC 2 audit trail
- GDPR data access log
- User activity report
- Security incident report

### Security Scanning

**Vulnerability Scans:**
```
Admin → Security → Scans → Run Scan

Last Scan: Dec 19, 2025 (daily)
Status:    ✅ No vulnerabilities found

Scan Results:
├─ Dependencies:   ✅ Up to date
├─ SSL/TLS:        ✅ A+ rating
├─ Headers:        ✅ All present
├─ Permissions:    ✅ Properly configured
└─ Secrets:        ✅ No exposed secrets
```

**Penetration Testing:**
- Schedule: Quarterly
- Provider: External security firm
- Scope: Full application + infrastructure
- Report: Available in Admin → Security → Pentest

### Incident Response

**Security Incidents:**
1. Detect (automated alerts)
2. Contain (suspend account, block IP)
3. Investigate (audit logs, forensics)
4. Remediate (patch, update)
5. Report (document, notify)

**Incident Runbook:**
```
Admin → Security → Incidents → Runbooks

Available Runbooks:
├─ Compromised Account
├─ Data Breach
├─ DDoS Attack
├─ Unauthorized Access
└─ Malware Detection
```

---

## Backup & Recovery

### Backup Strategy

**Automated Backups:**
```
Admin → Backup → Settings

Schedule:
├─ Full Backup:    Daily at 2:00 AM
├─ Incremental:    Every 6 hours
└─ Snapshot:       Before deployments

Retention:
├─ Daily:          30 days
├─ Weekly:         12 weeks
├─ Monthly:        12 months
└─ Yearly:         7 years

Storage:
├─ Primary:        AWS S3 (us-east-1)
├─ Secondary:      AWS S3 (us-west-2)
└─ Archive:        AWS Glacier
```

**What's Backed Up:**
- ✅ Database (all tables)
- ✅ File uploads
- ✅ Configuration
- ✅ Audit logs
- ✅ User data
- ❌ Cached data (regenerated)
- ❌ Temporary files

### Manual Backup

**Create Backup:**
1. Admin → Backup → Create
2. Select what to backup:
   - Full system
   - Database only
   - Files only
3. Add description
4. Click "Start Backup"
5. Monitor progress

**Verify Backup:**
1. Admin → Backup → [Select Backup]
2. Click "Verify"
3. System checks:
   - File integrity
   - Data consistency
   - Restoration readiness
4. Status: ✅ Verified

### Disaster Recovery

**Recovery Point Objective (RPO):** 1 hour  
**Recovery Time Objective (RTO):** 4 hours

**Restore from Backup:**
1. Admin → Backup → Restore
2. Select backup point
3. Choose restore type:
   - Full system restore
   - Partial restore (specific tables)
   - Point-in-time recovery
4. Review impact
5. Confirm restoration
6. Monitor progress

**Emergency Contact:**
- Support: support@chenu.com
- Emergency: +1-555-CHENU-911
- Status: status.chenu.com

---

## Troubleshooting

### Common Admin Issues

**Issue: Users can't login**

**Symptoms:**
- Multiple users reporting login failures
- "Invalid credentials" error
- MFA codes not working

**Diagnosis:**
1. Check system status dashboard
2. Verify auth service health
3. Check rate limiting
4. Review error logs

**Solution:**
```
Admin → Monitoring → Services

Auth Service:  ❌ Down
Action: Click "Restart Service"
Status: ✅ Service restored

Alternative:
1. SSH to server
2. sudo systemctl restart chenu-auth
3. Verify: curl https://api.chenu.com/v1/health
```

**Issue: Slow performance**

**Diagnosis:**
```
Admin → Monitoring → Performance

Database:
├─ Query Time: 450ms  ⚠️ (normal: <50ms)
├─ Connections: 95/100 ⚠️ (near limit)
└─ Slow Queries: 234

Action needed:
1. Identify slow queries
2. Add missing indexes
3. Optimize queries
4. Consider read replicas
```

**Solution:**
1. Admin → Monitoring → Slow Queries
2. Export slow query log
3. Analyze with `pt-query-digest`
4. Add indexes:
   ```sql
   CREATE INDEX idx_threads_user_updated 
   ON threads(user_id, updated_at DESC);
   ```
5. Monitor improvement

**Issue: Backup failed**

**Diagnosis:**
```
Admin → Backup → History

Last Backup: Dec 20, 2025 02:00
Status:      ❌ Failed
Error:       Insufficient storage space
```

**Solution:**
1. Check disk space:
   ```bash
   df -h
   # /dev/sda1  98%  ⚠️ Low space
   ```
2. Clean old backups:
   ```bash
   Admin → Backup → Cleanup
   Remove backups older than 90 days
   ```
3. Retry backup
4. Consider larger disk

---

## Best Practices

### Daily Tasks

**Morning Checklist:**
- [ ] Check system health dashboard
- [ ] Review overnight alerts
- [ ] Verify backup completion
- [ ] Check error rates
- [ ] Review new user signups

### Weekly Tasks

**Monday:**
- [ ] User activity review
- [ ] Token usage analysis
- [ ] Security scan
- [ ] Performance review

**Friday:**
- [ ] Weekly backup verification
- [ ] Access review (suspended users)
- [ ] Audit log review
- [ ] Capacity planning

### Monthly Tasks

**First Monday:**
- [ ] Full security audit
- [ ] User permission review
- [ ] Integration health check
- [ ] Cost analysis
- [ ] Compliance review

**Third Monday:**
- [ ] Disaster recovery test
- [ ] Documentation update
- [ ] Training materials review
- [ ] Roadmap planning

### Security Best Practices

**Password Management:**
- ✅ Use password manager
- ✅ Unique passwords per service
- ✅ Rotate admin passwords quarterly
- ✅ Never share passwords
- ✅ MFA on all admin accounts

**Access Control:**
- ✅ Principle of least privilege
- ✅ Regular access reviews
- ✅ Disable inactive accounts
- ✅ Audit admin actions
- ✅ Require MFA for admins

**Monitoring:**
- ✅ Set up alerts for critical events
- ✅ Review logs daily
- ✅ Monitor performance metrics
- ✅ Track user behavior anomalies
- ✅ Regular security scans

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    ADMIN RESPONSIBILITIES                                     ║
║                                                                               ║
║   🔐 Security: Protect user data and system integrity                        ║
║   📊 Monitoring: Keep the system running smoothly                            ║
║   👥 Users: Support and manage user accounts                                 ║
║   💾 Backups: Ensure data can be recovered                                   ║
║   📈 Performance: Optimize for best user experience                          ║
║                                                                               ║
║   Questions? admin-support@chenu.com                                         ║
║   Emergency? +1-555-CHENU-911                                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**You have the power. Use it wisely.** 🛡️
