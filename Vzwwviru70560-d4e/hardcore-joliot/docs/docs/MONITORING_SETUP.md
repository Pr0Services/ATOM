# 📊 STEP 3: Monitoring & Observability - CODE COMPLET

**Status:** ✅ Ready to deploy  
**Durée installation:** 15-20 minutes  
**Impact:** Complete visibility, proactive alerting, 10x faster debugging

---

## 📦 CONTENU DU PACKAGE

```
STEP3_MONITORING_CODE/
├── app/
│   ├── core/
│   │   ├── logging.py (550+ lignes)     # Structured logging
│   │   ├── metrics.py (500+ lignes)     # Prometheus metrics
│   │   └── tracing.py (450+ lignes)     # OpenTelemetry tracing
│   └── middleware/
│       └── monitoring.py (400+ lignes)   # Request monitoring
│
├── docker/
│   ├── docker-compose.monitoring.yml     # Prometheus+Grafana+Jaeger
│   ├── prometheus/
│   │   ├── prometheus.yml                # Prometheus config
│   │   └── alerts.yml                    # Alert rules
│   └── grafana/
│       ├── provisioning/                 # Datasources + dashboards
│       └── dashboards/                   # Pre-built dashboards
│
├── scripts/
│   └── install_step3.sh                  # Auto installation
│
└── README.md                              # Ce fichier
```

**Total: ~2,000 lignes de monitoring production-ready!**

---

## ⚡ INSTALLATION RAPIDE

```bash
# 1. Copier dans ton projet
cp -r STEP3_MONITORING_CODE/* /path/to/chenu_v3/

# 2. Lancer installation
cd /path/to/chenu_v3
chmod +x STEP3_MONITORING_CODE/scripts/install_step3.sh
./STEP3_MONITORING_CODE/scripts/install_step3.sh

# 3. DONE! Monitoring running! 🎉
```

---

## 💻 CE QUE TU OBTIENS

### **1. Structured Logging (structlog)**

**Logs JSON structurés pour meilleure observabilité:**

```python
from app.core.logging import get_logger, log_request

logger = get_logger(__name__)

# Log structuré
logger.info(
    "user_action",
    user_id="123",
    action="create_thread",
    thread_id="abc",
    tokens_used=150
)

# Output JSON:
# {
#   "event": "user_action",
#   "timestamp": "2024-12-18T01:30:00Z",
#   "level": "info",
#   "user_id": "123",
#   "action": "create_thread",
#   "thread_id": "abc",
#   "tokens_used": 150,
#   "request_id": "req-xyz"
# }
```

**Convenience functions:**
- `log_request()` - HTTP requests
- `log_database_query()` - DB queries  
- `log_cache_operation()` - Cache ops
- `log_agent_execution()` - Agent runs
- `log_thread_event()` - Thread events

---

### **2. Prometheus Metrics**

**40+ metrics pré-configurées:**

```python
from app.core.metrics import (
    record_http_request,
    record_agent_execution,
    agent_cost_usd_total
)

# Record HTTP request
record_http_request(
    method="GET",
    endpoint="/agents",
    status_code=200,
    duration_seconds=0.045
)

# Track agent execution
record_agent_execution(
    agent_id="agent-001",
    agent_name="NOVA",
    duration_seconds=1.2,
    tokens_used=150,
    cost_usd=0.0045,
    success=True
)
```

**Metrics disponibles:**
- HTTP: requests, latency, errors
- Database: queries, connections, duration
- Cache: hits, misses, hit rate
- Agents: executions, tokens, cost
- Threads: total, messages, budget
- WebSocket: connections, messages

---

### **3. Distributed Tracing (Jaeger)**

**Trace requests across services:**

```python
from app.core.tracing import traced, add_span_attributes

@traced("process_thread")
async def process_thread(thread_id: str):
    add_span_attributes(thread_id=thread_id)
    
    # Automatic sub-spans for:
    # - DB queries
    # - Cache operations
    # - Agent calls
    # - External APIs
    
    return result
```

**Auto-instrumentation pour:**
- FastAPI routes
- SQLAlchemy queries
- Redis operations

---

### **4. Monitoring Middleware**

**Automatic per-request monitoring:**

```python
# Automatically tracks:
# - Request ID (generated or from header)
# - Duration (P50, P95, P99)
# - Status codes
# - User context
# - Metrics collection
# - Distributed tracing
# - Error tracking
```

**Added to every request:**
- Structured logging context
- Prometheus metrics
- Trace spans
- Response headers (Request-ID, Process-Time)

---

## 📊 DASHBOARDS & VISUALIZATION

### **Prometheus** (http://localhost:9090)
- Query metrics directly
- View time series
- Test alert rules

### **Grafana** (http://localhost:3001)
- Pre-built dashboards
- Real-time visualization
- Custom queries
- Alert management

**Default credentials:** admin/admin

### **Jaeger** (http://localhost:16686)
- Distributed traces
- Service dependencies
- Latency analysis
- Error tracking

---

## 🚨 ALERTING

**Pre-configured alerts:**

```yaml
# High API Latency
P95 > 1s for 5 minutes → WARNING

# High Error Rate  
5xx errors > 5% for 5 minutes → CRITICAL

# Low Cache Hit Rate
Hit rate < 50% for 10 minutes → WARNING

# Slow Database Queries
P95 > 500ms for 5 minutes → WARNING

# High Agent Failure Rate
Failures > 10% for 10 minutes → CRITICAL

# High Agent Costs
> $10/hour → WARNING
```

**Customize in:** `docker/prometheus/alerts.yml`

---

## 📈 PERFORMANCE METRICS

**Track everything:**

```
Metric                  | Description
------------------------|----------------------------------
http_requests_total     | Total HTTP requests by endpoint
http_request_duration   | Request latency histogram
db_queries_total        | Database queries by type
db_query_duration       | Query latency histogram  
cache_hits_total        | Cache hits
cache_misses_total      | Cache misses
agent_executions_total  | Agent runs by status
agent_tokens_used       | Tokens consumed
agent_cost_usd_total    | $ spent on agents
threads_total           | Active threads
errors_total            | Errors by type
```

---

## 🔧 CONFIGURATION

**`.env` settings:**
```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Tracing
JAEGER_HOST=localhost
JAEGER_PORT=6831
ENABLE_TRACING=true

# Metrics
ENABLE_METRICS=true
```

---

## 🧪 USAGE EXAMPLES

### **Example 1: Log with context**

```python
from app.core.logging import get_logger, bind_context

logger = get_logger(__name__)

# Bind user context (applies to all subsequent logs)
bind_context(user_id="123", org_id="abc")

logger.info("processing_started")  # Has user_id + org_id
logger.info("processing_complete")  # Has user_id + org_id
```

### **Example 2: Track custom metrics**

```python
from app.core.metrics import Counter

my_counter = Counter(
    'custom_events_total',
    'My custom events',
    ['event_type']
)

my_counter.labels(event_type="signup").inc()
```

### **Example 3: Manual tracing**

```python
from app.core.tracing import create_span

with create_span("expensive_operation", {"user_id": "123"}):
    # Traced automatically
    result = expensive_calculation()
```

---

## 🚀 INTEGRATION

**Add to `main.py`:**

```python
from app.core.logging import setup_logging
from app.core.metrics import init_metrics, get_metrics
from app.core.tracing import setup_tracing, instrument_fastapi
from app.middleware.monitoring import MonitoringMiddleware

# Startup
@app.on_event("startup")
async def startup():
    setup_logging(level="INFO", format="json")
    init_metrics("chenu-backend", "1.0.0", "dev")
    setup_tracing()
    instrument_fastapi(app)

# Middleware
app.add_middleware(MonitoringMiddleware)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    from fastapi import Response
    from app.core.metrics import get_metrics, get_content_type
    return Response(get_metrics(), media_type=get_content_type())
```

---

## ✅ VALIDATION

**Checklist:**

- [ ] Prometheus running (http://localhost:9090)
- [ ] Grafana running (http://localhost:3001)
- [ ] Jaeger running (http://localhost:16686)
- [ ] Backend exposes /metrics endpoint
- [ ] Logs are JSON structured
- [ ] Traces appear in Jaeger
- [ ] Dashboards show data

---

## 🎯 NEXT STEPS

**After Step 3:**

1. **Customize dashboards** in Grafana
2. **Configure alerts** for your thresholds
3. **Integrate with PagerDuty/Slack** for notifications
4. **Add custom metrics** for business KPIs
5. **Move to Step 4: Semantic Agent Cache**

---

## 📚 RESOURCES

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [Jaeger Docs](https://www.jaegertracing.io/docs/)
- [structlog Docs](https://www.structlog.org/)
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)

---

**STEP 3 READY! 📊**

*Complete observability - Debug 10x faster!*
