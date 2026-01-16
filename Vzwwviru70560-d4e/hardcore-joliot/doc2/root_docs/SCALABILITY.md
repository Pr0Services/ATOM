# ⚡ CHE·NU™ - SCALABILITY & MLOPS

**Version:** V42  
**Status:** POST-MVP ENHANCEMENTS – RECOMMENDED BY GROK  
**Goal:** Scale 0→70K users  

---

## 🎯 OBJECTIF

Infrastructure auto-scalable + MLOps practices pour 70,000 users.

---

## 📊 BENCHMARKS CHARGE

### Target Performance
| Users | RPS | Latency p95 | DB Connections | Memory | CPU |
|-------|-----|-------------|----------------|--------|-----|
| **100** | 10 | <100ms | 10 | 2GB | 20% |
| **1K** | 100 | <150ms | 50 | 8GB | 40% |
| **10K** | 1K | <200ms | 200 | 32GB | 60% |
| **50K** | 5K | <300ms | 500 | 128GB | 80% |
| **70K** | 7K | <500ms | 700 | 256GB | 80% |

### Load Testing Tools
- Locust (Python)
- K6 (Go)
- Artillery (Node.js)
- JMeter (Java)

```python
# tests/load/locust_test.py
from locust import HttpUser, task, between

class ChenuUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def list_threads(self):
        self.client.get("/api/v1/threads")
    
    @task(2)
    def execute_agent(self):
        self.client.post("/api/v1/agents/execute", json={
            "agent_id": "business.crm_assistant",
            "capability": "list_contacts"
        })
    
    @task(1)
    def create_thread(self):
        self.client.post("/api/v1/threads", json={
            "title": "Load test thread",
            "sphere_id": "business"
        })
```

---

## ☸️ KUBERNETES AUTO-SCALING

### Architecture
```
┌─────────────────────────────────────────────────┐
│  Cloudflare CDN (Global)                        │
└───────────────┬─────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────┐
│  Kubernetes Cluster (GKE/EKS)                   │
│  ┌──────────────────────────────────────────┐   │
│  │  Nginx Ingress (Load Balancer)           │   │
│  └─────┬────────────────────────────────────┘   │
│        │                                         │
│  ┌─────▼──────────┐  ┌──────────────────────┐   │
│  │ Frontend Pods  │  │ Backend Pods         │   │
│  │ (replicas: 2-10)│  │ (replicas: 3-20)    │   │
│  │ HPA enabled    │  │ HPA + VPA enabled   │   │
│  └────────────────┘  └──────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ PostgreSQL (CloudSQL/RDS)                │   │
│  │ - Master + 2 Read replicas               │   │
│  │ - Auto-scaling storage                   │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ Redis Cluster (6 nodes)                  │   │
│  │ - Sharded + replicated                   │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

### HPA (Horizontal Pod Autoscaler)
```yaml
# k8s/backend-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: chenu-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chenu-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
```

### VPA (Vertical Pod Autoscaler)
```yaml
# k8s/backend-vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: chenu-backend-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chenu-backend
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: backend
      minAllowed:
        cpu: 100m
        memory: 256Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
```

---

## 🌍 LOAD BALANCING MULTI-RÉGION

### Global Architecture
```
US-EAST-1 (Primary)
US-WEST-2 (Secondary)
EU-WEST-1 (Europe)
AP-SOUTHEAST-1 (Asia)
SA-EAST-1 (South America)
```

### Cloudflare Load Balancing
```javascript
// cloudflare-config.js
{
  "pools": [
    {
      "id": "us-primary",
      "origins": [
        {"name": "us-east-1", "address": "api-us.chenu.com"},
        {"name": "us-west-2", "address": "api-usw.chenu.com"}
      ],
      "check_regions": ["WNAM", "ENAM"]
    },
    {
      "id": "eu-primary",
      "origins": [
        {"name": "eu-west-1", "address": "api-eu.chenu.com"}
      ]
    }
  ],
  "rules": [
    {
      "condition": "http.request.origin.country in {\"FR\" \"DE\" \"IT\" \"ES\" \"GB\"}",
      "pool": "eu-primary",
      "fallback": "us-primary"
    },
    {
      "condition": "http.request.origin.country in {\"SG\" \"JP\" \"AU\"}",
      "pool": "ap-primary",
      "fallback": "us-primary"
    }
  ],
  "steering_policy": "geo"
}
```

---

## 🗄️ DATABASE SHARDING

### Sharding Strategy
```
Users 0-10K:     Shard 1 (Primary)
Users 10K-30K:   Shard 2
Users 30K-50K:   Shard 3
Users 50K-70K:   Shard 4
```

### Implementation
```python
# backend/database/sharding.py
class DatabaseSharding:
    def get_shard(self, user_id: str) -> str:
        """Route user to correct shard based on ID hash"""
        shard_count = 4
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        shard_id = hash_value % shard_count
        
        return f"postgresql://shard-{shard_id}.chenu.com/chenu"
    
    async def query_all_shards(self, query: str) -> list:
        """Fan-out query across all shards (use sparingly)"""
        results = []
        for shard_id in range(4):
            shard_db = self.get_shard_connection(shard_id)
            result = await shard_db.execute(query)
            results.extend(result)
        return results
```

---

## 💾 REDIS CLUSTER

### Cluster Config
```
Master 1 (Shard 1) + Replica 1
Master 2 (Shard 2) + Replica 2
Master 3 (Shard 3) + Replica 3
```

```python
# backend/cache/redis_cluster.py
from redis.cluster import RedisCluster

redis_cluster = RedisCluster(
    startup_nodes=[
        {"host": "redis-1.chenu.com", "port": 7000},
        {"host": "redis-2.chenu.com", "port": 7001},
        {"host": "redis-3.chenu.com", "port": 7002},
    ],
    decode_responses=True,
    skip_full_coverage_check=True
)

# Usage
await redis_cluster.set(f"user:{user_id}", data)
cached = await redis_cluster.get(f"user:{user_id}")
```

---

## 🤖 MLOPS PIPELINE

### Model Lifecycle
```
1. Training (weekly)
2. Evaluation (offline metrics)
3. Staging deployment
4. A/B testing (10% traffic)
5. Production rollout
6. Monitoring (drift detection)
7. Retraining trigger (drift >5%)
```

### Architecture
```python
# backend/mlops/pipeline.py
class MLOpsPipeline:
    async def train_model(self, model_name: str):
        """Train or retrain model"""
        # Load training data
        data = await self.load_training_data()
        
        # Train model
        model = self.trainer.train(data)
        
        # Evaluate
        metrics = self.evaluator.evaluate(model, test_data)
        
        if metrics['accuracy'] > 0.90:
            # Push to model registry
            await self.model_registry.push(model_name, model, metrics)
            
            # Deploy to staging
            await self.deploy_to_staging(model_name)
    
    async def deploy_to_production(self, model_name: str):
        """Gradual rollout with A/B testing"""
        # Start with 10% traffic
        await self.traffic_split(model_name, percentage=10)
        
        # Monitor for 24h
        await asyncio.sleep(86400)
        
        # Check metrics
        if self.metrics_ok(model_name):
            # Rollout to 100%
            await self.traffic_split(model_name, percentage=100)
```

---

## 📈 AGENT DRIFT MONITORING

### Drift Detection
```python
# backend/monitoring/agent_drift.py
class AgentDriftMonitor:
    async def detect_drift(self, agent_id: str):
        """Detect agent behavior drift"""
        # Get baseline metrics (from training)
        baseline = await self.get_baseline_metrics(agent_id)
        
        # Get current metrics (last 7 days)
        current = await self.get_current_metrics(agent_id)
        
        # Statistical tests
        drift_score = self.calculate_drift(baseline, current)
        
        if drift_score > 0.05:  # 5% threshold
            # Alert
            await self.alert_drift_detected(agent_id, drift_score)
            
            # Trigger retraining
            await mlops_pipeline.train_model(agent_id)
    
    def calculate_drift(self, baseline, current):
        """PSI (Population Stability Index)"""
        psi = 0
        for feature in baseline.keys():
            expected = baseline[feature]
            actual = current[feature]
            psi += (actual - expected) * np.log(actual / expected)
        return psi
```

---

## 🧪 A/B TESTING INFRASTRUCTURE

```python
# backend/experiments/ab_testing.py
class ABTestingFramework:
    async def assign_variant(self, user_id: str, experiment_id: str) -> str:
        """Assign user to A/B test variant"""
        # Deterministic hash-based assignment
        hash_value = int(hashlib.md5(f"{user_id}:{experiment_id}".encode()).hexdigest(), 16)
        variant = "B" if hash_value % 100 < 50 else "A"  # 50/50 split
        
        # Track assignment
        await self.track_assignment(user_id, experiment_id, variant)
        
        return variant
    
    async def track_metric(self, user_id: str, experiment_id: str, metric: str, value: float):
        """Track experiment metric"""
        variant = await self.get_user_variant(user_id, experiment_id)
        
        await db.experiment_metrics.insert({
            "experiment_id": experiment_id,
            "variant": variant,
            "metric": metric,
            "value": value,
            "timestamp": datetime.utcnow()
        })
    
    async def analyze_experiment(self, experiment_id: str):
        """Statistical analysis (t-test)"""
        metrics_a = await self.get_metrics(experiment_id, "A")
        metrics_b = await self.get_metrics(experiment_id, "B")
        
        t_stat, p_value = stats.ttest_ind(metrics_a, metrics_b)
        
        return {
            "winner": "B" if p_value < 0.05 and mean(metrics_b) > mean(metrics_a) else "A",
            "p_value": p_value,
            "confidence": 1 - p_value
        }
```

---

## 🚩 FEATURE FLAGS

```python
# backend/features/feature_flags.py
class FeatureFlags:
    async def is_enabled(self, flag: str, user_id: str) -> bool:
        """Check if feature is enabled for user"""
        # Global override
        if flag in GLOBALLY_ENABLED:
            return True
        
        # Percentage rollout
        rollout = await self.get_rollout_percentage(flag)
        if rollout > 0:
            hash_value = int(hashlib.md5(f"{user_id}:{flag}".encode()).hexdigest(), 16)
            if hash_value % 100 < rollout:
                return True
        
        # User-specific override
        if user_id in await self.get_allowlist(flag):
            return True
        
        return False

# Usage
if await feature_flags.is_enabled("new_ui", user_id):
    return render_new_ui()
else:
    return render_old_ui()
```

---

## 🔥 CHAOS ENGINEERING

```python
# tests/chaos/chaos_experiments.py
import chaoslib

class ChaosExperiments:
    async def kill_random_pod(self):
        """Simulate pod failure"""
        pods = await k8s.list_pods(namespace="chenu")
        victim = random.choice(pods)
        await k8s.delete_pod(victim.name)
        
        # Monitor recovery
        await asyncio.sleep(60)
        assert await self.check_health() == "OK"
    
    async def introduce_latency(self, duration_sec: int):
        """Inject network latency"""
        await network.add_latency(delay_ms=500, duration=duration_sec)
        
        # Check degraded performance acceptable
        response_time = await self.measure_response_time()
        assert response_time < 1000  # <1s acceptable
    
    async def simulate_db_failure(self):
        """Simulate database unavailability"""
        await db.disconnect()
        
        # Check graceful degradation
        response = await api_client.get("/health")
        assert response.status == 503  # Service Unavailable
        assert "database" in response.json()["errors"]
```

---

## 📊 MÉTRIQUES SCALABILITÉ

### Dashboards
- **Latency**: p50, p95, p99
- **Throughput**: RPS, RPM
- **Error rate**: 5xx errors
- **Saturation**: CPU, Memory, Disk, Network
- **Pod count**: Current, Min, Max
- **DB connections**: Active, Idle, Max

### Alerts
- Latency p95 > 500ms (3 min)
- Error rate > 1% (1 min)
- CPU > 80% (5 min)
- Memory > 90% (3 min)
- Pod crash loop
- DB connection pool exhausted

---

## 📅 TIMELINE V42

| Semaine | Tâche |
|---------|-------|
| **W1-2** | Load testing (1K, 10K users) |
| **W3-4** | Kubernetes setup + HPA/VPA |
| **W5-6** | Multi-region deployment |
| **W7-8** | Database sharding |
| **W9-10** | Redis cluster |
| **W11-12** | MLOps pipeline |
| **W13-14** | Agent drift monitoring |
| **W15-16** | A/B testing framework |
| **W17-18** | Feature flags system |
| **W19-20** | Chaos engineering tests |

---

## ✅ VALIDATION CHECKLIST

- [ ] Load test: 70K users simulated
- [ ] Latency p95: <500ms at 70K users
- [ ] Auto-scale: 0→10K users in <5min
- [ ] Multi-region: 5 regions deployed
- [ ] DB sharding: 4 shards operational
- [ ] Redis cluster: 6 nodes operational
- [ ] MLOps: Automated weekly retraining
- [ ] Drift detection: <1% agent drift
- [ ] A/B testing: 10+ active experiments
- [ ] Chaos tests: All passing

---

*CHE·NU™ Scalability & MLOps — V42*  
***SCALE. OPTIMIZE. GOVERN.*** ⚡
