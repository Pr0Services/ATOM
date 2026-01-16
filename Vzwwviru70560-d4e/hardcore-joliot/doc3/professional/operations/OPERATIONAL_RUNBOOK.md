# 🚨 CHE·NU™ OPERATIONAL RUNBOOK
## Complete Incident Response & Operations Guide

**Version:** 1.0.0  
**Last Updated:** December 20, 2025  
**For:** CHE·NU v41.6+  
**On-Call:** 24/7 Support

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                   CHE·NU™ OPERATIONAL RUNBOOK                                 ║
║                                                                               ║
║   Incident Response • Troubleshooting • Recovery Procedures                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Emergency Contacts](#emergency-contacts)
2. [Incident Response Framework](#incident-response-framework)
3. [Common Incidents](#common-incidents)
4. [Runbooks by Severity](#runbooks-by-severity)
5. [Monitoring & Alerts](#monitoring--alerts)
6. [Performance Troubleshooting](#performance-troubleshooting)
7. [Database Operations](#database-operations)
8. [Security Incidents](#security-incidents)

---

## Emergency Contacts

### On-Call Rotation

```
┌─────────────────────────────────────────┐
│ ROLE          │ NAME      │ CONTACT     │
├─────────────────────────────────────────┤
│ Primary       │ John Doe  │ +1-555-0001 │
│ Secondary     │ Jane Smith│ +1-555-0002 │
│ Manager       │ Bob Wilson│ +1-555-0003 │
│ CTO           │ Alice Chen│ +1-555-0004 │
└─────────────────────────────────────────┘
```

### Escalation Path

```
Level 1: On-Call Engineer (0-15 min)
   ↓
Level 2: Senior Engineer (15-30 min)
   ↓
Level 3: Engineering Manager (30-60 min)
   ↓
Level 4: CTO (60+ min or P0 incident)
```

### External Vendors

- **AWS Support:** 1-800-AWS-HELP (P1: 15min SLA)
- **Datadog:** support@datadoghq.com
- **Sentry:** support@sentry.io
- **PagerDuty:** +1-844-PAGERDUTY

---

## Incident Response Framework

### Severity Levels

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| **P0** | Complete outage | <15 min | Site down, data breach |
| **P1** | Major degradation | <30 min | API slow, DB overload |
| **P2** | Minor issues | <2 hours | Feature broken, UI bug |
| **P3** | Low impact | <24 hours | Cosmetic issues |

### Incident Workflow

```
┌──────────────────────────────────────────────┐
│ 1. DETECT                                    │
│    • Alert triggered                         │
│    • User report                             │
│    • Monitoring                              │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ 2. ASSESS                                    │
│    • Determine severity (P0-P3)              │
│    • Identify affected users                 │
│    • Estimate impact                         │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ 3. RESPOND                                   │
│    • Page on-call                            │
│    • Create incident ticket                  │
│    • Follow runbook                          │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ 4. MITIGATE                                  │
│    • Apply temporary fix                     │
│    • Communicate status                      │
│    • Monitor metrics                         │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ 5. RESOLVE                                   │
│    • Implement permanent fix                 │
│    • Deploy solution                         │
│    • Verify resolution                       │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ 6. POSTMORTEM                                │
│    • Document incident                       │
│    • Identify root cause                     │
│    • Define preventive actions               │
└──────────────────────────────────────────────┘
```

---

## Common Incidents

### 🔴 RUNBOOK #1: Site Down (P0)

**Symptoms:**
- Users cannot access site
- HTTP 503 errors
- All health checks failing

**Immediate Actions (< 5 min):**

```bash
# 1. Check service status
aws ecs describe-services \
  --cluster chenu-prod \
  --services api | jq '.services[0].runningCount'

# Expected: 3 or more
# If 0: Service is down!

# 2. Check load balancer
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-east-1:123456789:targetgroup/chenu-api/abc123

# Expected: "healthy"
# If "unhealthy": Targets are failing health checks

# 3. Check recent deployments
aws ecs describe-services \
  --cluster chenu-prod \
  --services api | jq '.services[0].deployments'

# If multiple deployments: Deployment in progress or failed

# 4. Check CloudWatch Logs (last 5 min)
aws logs tail /ecs/chenu-api --since 5m --follow
```

**Diagnosis:**

```bash
# Scenario A: ECS tasks crashing
if [ "$(aws ecs describe-services --cluster chenu-prod --services api | jq '.services[0].runningCount')" -eq 0 ]; then
  echo "🚨 SCENARIO A: No running tasks"
  
  # Check task failures
  aws ecs describe-services \
    --cluster chenu-prod \
    --services api | jq '.services[0].events[0:5]'
  
  # Common causes:
  # - OOMKilled: Increase memory
  # - Health check failing: Check /health endpoint
  # - Image pull error: Verify ECR image exists
fi

# Scenario B: Database down
if ! pg_isready -h db.internal -U chenu; then
  echo "🚨 SCENARIO B: Database unreachable"
  
  # Check RDS status
  aws rds describe-db-instances \
    --db-instance-identifier chenu-prod \
    | jq '.DBInstances[0].DBInstanceStatus'
fi

# Scenario C: Redis down
if ! redis-cli -h redis.internal ping; then
  echo "🚨 SCENARIO C: Redis unreachable"
  
  # Check ElastiCache
  aws elasticache describe-cache-clusters \
    --cache-cluster-id chenu-prod \
    | jq '.CacheClusters[0].CacheClusterStatus'
fi
```

**Mitigation Steps:**

```bash
# MITIGATION A: Rollback to last known good version
./scripts/rollback.sh v41.5

# MITIGATION B: Scale up tasks (if running but overwhelmed)
aws ecs update-service \
  --cluster chenu-prod \
  --service api \
  --desired-count 10

# MITIGATION C: Restart service (force new deployment)
aws ecs update-service \
  --cluster chenu-prod \
  --service api \
  --force-new-deployment

# MITIGATION D: Enable maintenance mode
aws s3 cp maintenance.html s3://chenu-static/index.html
# Update CloudFront to serve maintenance page
```

**Communication Template:**

```
[STATUS PAGE UPDATE]
🔴 Major Outage

We are currently experiencing a complete service outage. 
Our team is actively investigating and working on a resolution.

Status: Investigating
Started: [TIME]
Impact: All users unable to access CHE·NU
ETA: [TIME]

Updates: https://status.chenu.com
```

**Resolution:**

1. Service restored and stable for 10+ minutes
2. Health checks passing
3. Error rate < 0.1%
4. User reports confirm resolution

**Postmortem (within 48h):**

```markdown
# Incident Postmortem: Site Down

**Date:** Dec 20, 2025
**Duration:** 15 minutes
**Severity:** P0
**Impact:** 100% of users unable to access service

## Timeline
- 14:00 UTC: Deployment started (v41.6)
- 14:05 UTC: Health checks begin failing
- 14:06 UTC: Alert triggered
- 14:07 UTC: On-call paged
- 14:10 UTC: Investigation started
- 14:12 UTC: Root cause identified (OOM)
- 14:13 UTC: Rollback initiated
- 14:15 UTC: Service restored

## Root Cause
Memory leak in new feature caused containers to consume 
4GB+ memory, exceeding 2GB limit and causing OOMKill.

## Prevention
- [ ] Add memory profiling to CI/CD
- [ ] Increase container memory to 4GB
- [ ] Add memory usage alerts at 75%
- [ ] Implement gradual rollout (10% → 50% → 100%)

## Action Items
- [x] Fix memory leak (JIRA-123)
- [ ] Update monitoring (JIRA-124)
- [ ] Deploy fix (JIRA-125)
```

---

### 🟡 RUNBOOK #2: Slow API Response (P1)

**Symptoms:**
- p95 response time > 500ms
- Users report slowness
- Timeout errors increasing

**Quick Check:**

```bash
# 1. Check current response times
curl -w "@curl-format.txt" -o /dev/null -s https://api.chenu.com/health

# 2. Check database performance
psql -h db.internal -U chenu -c "
SELECT pid, now() - query_start as duration, query 
FROM pg_stat_activity 
WHERE state = 'active' 
AND now() - query_start > interval '1 second'
ORDER BY duration DESC;"

# 3. Check cache hit rate
redis-cli -h redis.internal info stats | grep keyspace_hits
```

**Diagnosis Tree:**

```
Slow API?
├─ Database slow?
│  ├─ Yes → Check slow queries
│  │  ├─ N+1 queries? → Add includes
│  │  ├─ Missing index? → Create index
│  │  └─ Table bloat? → VACUUM
│  └─ No → Check Redis
│     ├─ Cache miss? → Warm cache
│     └─ Redis slow? → Check memory
├─ High CPU?
│  ├─ Traffic spike? → Scale up
│  └─ Inefficient code? → Profile & fix
└─ Network issue?
   ├─ AWS outage? → Check status
   └─ DDoS? → Enable WAF
```

**Mitigation:**

```bash
# QUICK WIN 1: Scale up
aws ecs update-service \
  --cluster chenu-prod \
  --service api \
  --desired-count 6  # Double capacity

# QUICK WIN 2: Warm cache
curl -X POST https://api.chenu.com/admin/cache/warm

# QUICK WIN 3: Kill slow queries
psql -h db.internal -U chenu -c "
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE pid <> pg_backend_pid() 
AND state = 'active' 
AND now() - query_start > interval '30 seconds';"
```

---

### 🟢 RUNBOOK #3: Database High CPU (P1)

**Symptoms:**
- RDS CPU > 80%
- Queries queueing
- Connection pool exhausted

**Investigation:**

```sql
-- Find expensive queries
SELECT 
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Find slow running queries
SELECT 
  pid,
  now() - query_start AS duration,
  state,
  query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Check locks
SELECT 
  pid,
  usename,
  pg_blocking_pids(pid) as blocked_by,
  query
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;
```

**Solutions:**

```sql
-- Solution 1: Kill long-running queries
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
AND now() - query_start > interval '1 minute'
AND query NOT LIKE '%pg_stat_activity%';

-- Solution 2: Add missing indexes
CREATE INDEX CONCURRENTLY idx_missing
ON table_name(column_name);

-- Solution 3: Update statistics
ANALYZE;

-- Solution 4: Clear bloat
VACUUM ANALYZE;
```

**Prevention:**

```bash
# Enable query logging for slow queries
aws rds modify-db-parameter-group \
  --db-parameter-group-name chenu-prod \
  --parameters \
    "ParameterName=log_min_duration_statement,ParameterValue=1000,ApplyMethod=immediate"

# Set up CloudWatch alarm
aws cloudwatch put-metric-alarm \
  --alarm-name chenu-db-cpu-high \
  --alarm-description "Database CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

---

### 🔴 RUNBOOK #4: Data Breach (P0)

**CRITICAL: Stop all access immediately!**

```bash
# 1. ISOLATE (< 1 minute)
# Revoke all API keys
psql -h db.internal -U chenu -c "
UPDATE api_keys SET revoked_at = NOW() WHERE revoked_at IS NULL;"

# Invalidate all sessions
redis-cli -h redis.internal FLUSHDB

# Block all traffic except admin
aws waf update-ip-set \
  --id abc123 \
  --updates Action=INSERT,IPSetDescriptor={Type=IPV4,Value=YOUR_ADMIN_IP/32}

# 2. ASSESS (< 5 minutes)
# Check audit logs for breach
psql -h db.internal -U chenu -c "
SELECT * FROM audit_log 
WHERE created_at > NOW() - interval '1 hour'
AND (event_type = 'unauthorized_access' 
     OR event_type = 'data_export')
ORDER BY created_at DESC;"

# 3. NOTIFY (< 15 minutes)
# Legal team
# Security team
# Affected users (if confirmed)
```

**Evidence Collection:**

```bash
# Preserve logs
aws logs create-export-task \
  --log-group-name /ecs/chenu-api \
  --from $(date -d '24 hours ago' +%s)000 \
  --to $(date +%s)000 \
  --destination s3://chenu-incident-logs/breach-$(date +%Y%m%d)

# Database snapshot
aws rds create-db-snapshot \
  --db-instance-identifier chenu-prod \
  --db-snapshot-identifier breach-forensics-$(date +%Y%m%d)

# Preserve security group rules
aws ec2 describe-security-groups > security-groups-$(date +%Y%m%d).json
```

**Legal Requirements:**

- **GDPR:** Notify DPA within 72 hours
- **CCPA:** Notify users "without unreasonable delay"
- **SOC 2:** Document in audit trail
- **Insurance:** Notify cyber insurance provider

---

## Monitoring & Alerts

### Critical Alerts (Page Immediately)

```yaml
# alerts/critical.yaml
alerts:
  - name: SiteDown
    condition: http_status != 200
    for: 1m
    severity: P0
    notification: pagerduty
    
  - name: HighErrorRate
    condition: error_rate > 5%
    for: 5m
    severity: P0
    notification: pagerduty
    
  - name: DatabaseDown
    condition: db_connections = 0
    for: 1m
    severity: P0
    notification: pagerduty
    
  - name: DiskFull
    condition: disk_usage > 90%
    for: 5m
    severity: P0
    notification: pagerduty
```

### Warning Alerts (Slack)

```yaml
# alerts/warnings.yaml
alerts:
  - name: HighCPU
    condition: cpu > 70%
    for: 10m
    severity: P1
    notification: slack
    
  - name: SlowQueries
    condition: p95_query_time > 100ms
    for: 15m
    severity: P1
    notification: slack
    
  - name: CacheMissRate
    condition: cache_hit_rate < 70%
    for: 30m
    severity: P2
    notification: slack
```

### Dashboards

**Main Dashboard:**
- Request rate (req/s)
- Error rate (%)
- Response time (p50, p95, p99)
- Active users
- Database connections
- Cache hit rate

**Infrastructure Dashboard:**
- CPU usage (%)
- Memory usage (%)
- Disk usage (%)
- Network I/O
- Container count

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    ON-CALL QUICK REFERENCE                                    ║
║                                                                               ║
║   Site Down?          → Runbook #1 (Page 3)                                  ║
║   Slow Performance?   → Runbook #2 (Page 6)                                  ║
║   Database Issues?    → Runbook #3 (Page 8)                                  ║
║   Security Breach?    → Runbook #4 (Page 10)                                 ║
║                                                                               ║
║   Emergency Contacts: See Page 1                                             ║
║   Escalation Path:    See Page 1                                             ║
║                                                                               ║
║   Remember:                                                                  ║
║   1. Stay calm                                                               ║
║   2. Follow runbook                                                          ║
║   3. Communicate status                                                      ║
║   4. Document everything                                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Your operations team is READY!** 🚨✨
