# EXHIBIT C: API USAGE TRACKING SYSTEM

**Patent Application:** CHENU-2026-001-PROV
**Document Type:** Resource Allocation Description
**Classification:** PUBLIC - Safe for Patent Disclosure

---

## 1. OVERVIEW

The system implements a credit-based API access model where the platform acts as a Sovereign Proxy with centralized credentials, eliminating the need for users to manage their own API keys.

---

## 2. ARCHITECTURE CONCEPT

```
+-------------------------------------------------------------------+
|                    SOVEREIGN PROXY MODEL                          |
+-------------------------------------------------------------------+
|                                                                   |
|    [User Request]                                                 |
|          |                                                        |
|          v                                                        |
|    +-------------+                                                |
|    | Credit      | <-- Verify available tokens                    |
|    | Validation  |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Sovereign   | <-- Single master API credential               |
|    | Proxy       |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | External    | <-- OpenRouter, Anthropic, etc.                |
|    | Providers   |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Usage       | <-- Record consumption                         |
|    | Recording   |                                                |
|    +-------------+                                                |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 3. DATA MODEL

### 3.1 Usage Tracking

```
TABLE: api_usage
+-- id (unique identifier)
+-- user_id (reference to user)
+-- month (billing period)
+-- tokens_used (consumption counter)
+-- requests_count (request counter)
+-- cost_tracking (internal cost)
+-- tokens_limit (quota for period)
+-- timestamps
```

**Purpose:** Track monthly token consumption per user against their allocated quota.

### 3.2 Request Logging

```
TABLE: api_requests
+-- id (unique identifier)
+-- user_id (reference to user)
+-- provider (API provider name)
+-- model (model identifier)
+-- token_counts (input/output/total)
+-- cost_tracking (internal cost)
+-- context (usage context)
+-- latency (performance metric)
+-- timestamp
```

**Purpose:** Detailed logging of individual API requests for analytics and billing.

### 3.3 Subscription Tiers

```
TABLE: subscription_plans
+-- id (plan identifier)
+-- name (display name)
+-- tokens_monthly (allocation)
+-- price (subscription cost)
+-- features (capability list)
+-- is_active (availability)
```

**Purpose:** Define subscription tiers with their associated token allocations and features.

---

## 4. ACCESS TIERS

```
+-------------------------------------------------------------------+
|                    SUBSCRIPTION MODEL                             |
+-------------------------------------------------------------------+
|                                                                   |
|  TIER           | TOKENS      | FEATURES                         |
|  ----------------+-------------+--------------------------------  |
|  Entry Level    | Basic quota | Standard access                  |
|  Member         | Enhanced    | Extended features + Grid access  |
|  Sovereign      | Unlimited   | Full system control              |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 5. CREDIT VERIFICATION FLOW

```
+-------------------------------------------------------------------+
|                    CREDIT CHECK PROCESS                           |
+-------------------------------------------------------------------+
|                                                                   |
|    1. Retrieve user's subscription tier                           |
|    2. Check if tier grants unlimited access                       |
|       - If yes: Allow request                                     |
|    3. Retrieve current month's usage                              |
|    4. Calculate remaining tokens                                  |
|    5. Compare required tokens against remaining                   |
|       - If sufficient: Allow request                              |
|       - If insufficient: Reject with quota message                |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 6. USAGE RECORDING

When an API request completes:

1. Calculate actual tokens consumed
2. Update monthly usage counters
3. Log detailed request information
4. Update cost tracking for internal analytics

---

## 7. SECURITY MODEL

### 7.1 Row-Level Security

- Users can only view their own usage data
- Users can only view their own request history
- Sovereign role can access aggregate statistics
- System functions operate with elevated privileges for recording

### 7.2 Data Protection

- API credentials never exposed to end users
- Usage data isolated per user
- Cost data for internal use only

---

## 8. KEY FEATURES

1. **Zero-Account Model**: Users don't need their own API keys
2. **Transparent Quotas**: Clear visibility into available resources
3. **Tiered Access**: Different capabilities per subscription level
4. **Detailed Analytics**: Per-request logging for optimization
5. **Cost Tracking**: Internal cost monitoring for sustainability

---

## 9. STATISTICS FUNCTIONS

The system provides aggregate statistics (Sovereign only):

- Total active users
- Total tokens consumed
- Total requests processed
- Most used models
- Daily usage patterns

---

**END OF EXHIBIT C**

*This document describes the resource tracking concepts without revealing specific quotas, pricing, or calculation algorithms.*
