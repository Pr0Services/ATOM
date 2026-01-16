# 💰 CHE·NU™ - MONETIZATION & BUSINESS

**Version:** V44  
**Status:** POST-MVP ENHANCEMENTS – RECOMMENDED BY GROK  
**Goal:** €50K MRR (1000 users × €50 ARPU)  

---

## 🎯 OBJECTIF

Revenue streams validation + business model scalable.

---

## 💳 FREEMIUM MODEL

### Tiers de Prix

| Tier | Prix | Token Budget | Agents | Storage | Support |
|------|------|--------------|--------|---------|---------|
| **FREE** | €0 | 500/mois | 50 basiques | 1GB | Community |
| **STARTER** | €9/mois | 5,000/mois | 100 (L0-L1) | 10GB | Email |
| **PRO** | €29/mois | 25,000/mois | All 168 | 50GB | Priority |
| **BUSINESS** | €99/mois | 100,000/mois | All + Custom | 500GB | Dedicated |
| **ENTERPRISE** | Custom | Unlimited | All + SSO | Unlimited | Phone + SLA |

### Feature Matrix
```
Feature               | FREE | STARTER | PRO | BUSINESS | ENTERPRISE
─────────────────────────────────────────────────────────────────────
Spheres (9)           |  ✅  |   ✅    | ✅  |    ✅     |     ✅
Threads               |  5   |   50    | 500 |  Unlimited| Unlimited
Agents basiques (L0)  |  ✅  |   ✅    | ✅  |    ✅     |     ✅
Agents avancés (L1-L3)|  ❌  |   L1    | All |    All    |     All
Mobile/PWA            |  ✅  |   ✅    | ✅  |    ✅     |     ✅
Quick Capture         |  ✅  |   ✅    | ✅  |    ✅     |     ✅
API Access            |  ❌  |   ❌    | ✅  |    ✅     |     ✅
Marketplace           |  ❌  |   ✅    | ✅  |    ✅     |     ✅
Custom Agents         |  ❌  |   ❌    | ❌  |    ✅     |     ✅
SSO (SAML/OIDC)       |  ❌  |   ❌    | ❌  |    ❌     |     ✅
White-label           |  ❌  |   ❌    | ❌  |    ❌     |     ✅
SLA 99.9%             |  ❌  |   ❌    | ❌  |    ❌     |     ✅
```

---

## 💵 PRICING STRATEGY

### Positionnement
- **FREE**: Acquisition + Conversion funnel
- **STARTER**: Freelancers, étudiants
- **PRO**: Power users, small teams
- **BUSINESS**: SMBs, agencies
- **ENTERPRISE**: Corporates, government

### Conversion Targets
```
FREE → STARTER:   15% (high intent users)
STARTER → PRO:    25% (power users unlock)
PRO → BUSINESS:   10% (team growth)
BUSINESS → ENTERPRISE: 5% (custom needs)
```

### Pricing Psychology
- Anchoring: BUSINESS (€99) fait paraître PRO (€29) bon marché
- Decoy effect: STARTER (€9) pousse vers PRO (€29)
- Tiered value: Chaque tier débloque vraie valeur perçue

---

## 🔌 STRIPE SUBSCRIPTIONS

### Implementation
```python
# backend/billing/subscriptions.py
import stripe

class SubscriptionManager:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Price IDs (from Stripe Dashboard)
        self.prices = {
            "starter_monthly": "price_starter_monthly",
            "starter_yearly": "price_starter_yearly",
            "pro_monthly": "price_pro_monthly",
            "pro_yearly": "price_pro_yearly",
            "business_monthly": "price_business_monthly",
            "business_yearly": "price_business_yearly"
        }
    
    async def create_subscription(
        self,
        user_id: str,
        price_id: str,
        payment_method_id: str
    ):
        """Create Stripe subscription"""
        # Get or create Stripe customer
        customer = await self.get_or_create_customer(user_id)
        
        # Attach payment method
        await stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer.id
        )
        
        # Set as default
        await stripe.Customer.modify(
            customer.id,
            invoice_settings={"default_payment_method": payment_method_id}
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_id}],
            trial_period_days=14,
            expand=["latest_invoice.payment_intent"]
        )
        
        # Update user tier in DB
        await self.update_user_tier(user_id, subscription)
        
        return subscription
    
    async def handle_webhook(self, event: dict):
        """Handle Stripe webhook events"""
        event_type = event["type"]
        
        handlers = {
            "customer.subscription.created": self.on_subscription_created,
            "customer.subscription.updated": self.on_subscription_updated,
            "customer.subscription.deleted": self.on_subscription_canceled,
            "invoice.payment_succeeded": self.on_payment_succeeded,
            "invoice.payment_failed": self.on_payment_failed
        }
        
        handler = handlers.get(event_type)
        if handler:
            await handler(event["data"]["object"])
```

---

## 🛒 MARKETPLACE AGENTS

### Concept
Utilisateurs peuvent **créer et vendre leurs propres agents**.

### Revenue Split
- **70% Créateur** (agent creator)
- **30% CHE·NU** (platform fee)

### Pricing Agents
- Prix suggéré: €1-€50 one-time ou €5-€20/mois subscription
- Créateurs fixent prix
- CHE·NU prend commission automatiquement

### Implementation
```python
# backend/marketplace/agent_sales.py
class MarketplaceAgent:
    async def publish_agent(
        self,
        creator_id: str,
        agent_config: dict,
        pricing: dict
    ):
        """Publish agent to marketplace"""
        agent = await db.marketplace_agents.insert({
            "creator_id": creator_id,
            "name": agent_config["name"],
            "description": agent_config["description"],
            "capabilities": agent_config["capabilities"],
            "price_type": pricing["type"],  # "one_time" or "subscription"
            "price_amount": pricing["amount"],  # cents
            "revenue_split": 0.70,  # 70% to creator
            "status": "pending_review"
        })
        
        return agent
    
    async def purchase_agent(
        self,
        buyer_id: str,
        agent_id: str
    ):
        """Purchase marketplace agent"""
        agent = await db.marketplace_agents.get(agent_id)
        
        # Create Stripe charge
        charge = stripe.Charge.create(
            amount=agent.price_amount,
            currency="eur",
            customer=buyer_stripe_id,
            description=f"Agent: {agent.name}"
        )
        
        # Split revenue (Stripe Connect)
        await stripe.Transfer.create(
            amount=int(agent.price_amount * 0.70),  # 70% to creator
            currency="eur",
            destination=creator_stripe_account,
            transfer_group=f"agent_{agent_id}"
        )
        
        # Grant access to buyer
        await db.user_agents.insert({
            "user_id": buyer_id,
            "agent_id": agent_id,
            "purchased_at": datetime.utcnow()
        })
```

---

## 🔌 API PAYANTE

### Tiers API
| Tier | Calls/mois | Prix | Rate Limit |
|------|------------|------|------------|
| **FREE** | 1,000 | €0 | 10/min |
| **BASIC** | 100,000 | €49/mois | 100/min |
| **PRO** | 1,000,000 | €299/mois | 1000/min |
| **ENTERPRISE** | Unlimited | Custom | Custom |

### Implementation
```python
# backend/api/rate_limiting.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/threads")
@limiter.limit(get_user_rate_limit)  # Dynamic based on tier
async def list_threads(user_id: str):
    tier = await get_user_api_tier(user_id)
    
    if tier == "free":
        rate_limit = "10/minute"
    elif tier == "basic":
        rate_limit = "100/minute"
    elif tier == "pro":
        rate_limit = "1000/minute"
    else:  # enterprise
        rate_limit = None  # unlimited
    
    # ... endpoint logic
```

---

## 💎 TOKEN PACKS

### Achats In-App
```
100 tokens    = €1   (top-up)
1,000 tokens  = €9   (10% bonus)
10,000 tokens = €80  (20% bonus)
100,000 tokens = €700 (30% bonus)
```

### Use Cases
- User dépasse budget mensuel → achète pack
- Projets ponctuels importants
- Flexibilité vs subscription

```python
# backend/billing/token_packs.py
async def purchase_token_pack(user_id: str, pack_id: str):
    packs = {
        "pack_100": {"tokens": 100, "price": 100},  # cents
        "pack_1k": {"tokens": 1100, "price": 900},  # 10% bonus
        "pack_10k": {"tokens": 12000, "price": 8000},  # 20% bonus
        "pack_100k": {"tokens": 130000, "price": 70000}  # 30% bonus
    }
    
    pack = packs[pack_id]
    
    # Stripe charge
    charge = stripe.Charge.create(
        amount=pack["price"],
        currency="eur",
        customer=user_stripe_id
    )
    
    # Credit tokens
    await tokens.add(user_id, pack["tokens"], reason="pack_purchase")
```

---

## 📊 ROI DASHBOARDS

### Metrics Tracked
```python
# For users
saved_hours = sum(agent_executions) * avg_time_saved_per_execution
productivity_gain = saved_hours * hourly_rate
roi_percentage = (productivity_gain - subscription_cost) / subscription_cost

# Example:
# User: 50 agent executions/mois × 15min saved = 12.5h saved
# At €50/h hourly rate = €625 value
# Subscription: €29/mois
# ROI = (€625 - €29) / €29 = 2055% ROI
```

### Dashboard UI
```jsx
<ROIDashboard>
  <Metric>
    <Label>Temps économisé</Label>
    <Value>12.5 heures ce mois</Value>
  </Metric>
  
  <Metric>
    <Label>Valeur créée</Label>
    <Value>€625</Value>
  </Metric>
  
  <Metric>
    <Label>ROI</Label>
    <Value highlight>2,055%</Value>
  </Metric>
  
  <Chart type="line" data={productivityOverTime} />
</ROIDashboard>
```

---

## 📈 REVENUE ANALYTICS

### MRR Tracking
```python
# backend/analytics/revenue.py
class RevenueAnalytics:
    async def calculate_mrr(self) -> float:
        """Monthly Recurring Revenue"""
        subscriptions = await db.subscriptions.find(status="active")
        
        mrr = 0
        for sub in subscriptions:
            if sub.interval == "month":
                mrr += sub.amount
            elif sub.interval == "year":
                mrr += sub.amount / 12
        
        return mrr
    
    async def calculate_metrics(self) -> dict:
        """Core business metrics"""
        return {
            "mrr": await self.calculate_mrr(),
            "arr": await self.calculate_arr(),
            "arpu": await self.calculate_arpu(),
            "ltv": await self.calculate_ltv(),
            "cac": await self.calculate_cac(),
            "ltv_cac_ratio": ltv / cac,
            "churn_rate": await self.calculate_churn(),
            "expansion_mrr": await self.calculate_expansion()
        }
```

### Targets V44
```
MRR:            €50,000
Users payants:  1,000
ARPU:           €50/mois
Churn:          <5% mensuel
LTV:            €1,500 (30 months × €50)
CAC:            €300 (ads + onboarding)
LTV/CAC:        5:1 (excellent)
```

---

## 💳 FACTURATION AUTOMATIQUE

```python
# backend/billing/invoicing.py
async def generate_invoice(subscription_id: str):
    """Auto-generate invoice on subscription renewal"""
    subscription = await db.subscriptions.get(subscription_id)
    user = await db.users.get(subscription.user_id)
    
    # Stripe invoice
    invoice = stripe.Invoice.create(
        customer=user.stripe_id,
        auto_advance=True,  # Auto-finalize
        collection_method="charge_automatically"
    )
    
    # Add line items
    stripe.InvoiceItem.create(
        customer=user.stripe_id,
        amount=subscription.amount,
        currency="eur",
        description=f"CHE·NU {subscription.tier} - {month}/{year}",
        invoice=invoice.id
    )
    
    # Store in DB
    await db.invoices.insert({
        "user_id": user.id,
        "stripe_invoice_id": invoice.id,
        "amount": subscription.amount,
        "status": "paid",
        "pdf_url": invoice.invoice_pdf
    })
    
    # Email invoice
    await emails.send_invoice(user.email, invoice.invoice_pdf)
```

---

## 🎁 TRIALS GRATUITS

### 14 Jours Gratuits
```python
# backend/billing/trials.py
async def start_trial(user_id: str, tier: str):
    """Start 14-day free trial"""
    subscription = stripe.Subscription.create(
        customer=user_stripe_id,
        items=[{"price": tier_price_id}],
        trial_period_days=14,
        trial_settings={
            "end_behavior": {
                "missing_payment_method": "cancel"  # Auto-cancel si pas de carte
            }
        }
    )
    
    # Track trial
    await analytics.track("trial_started", {
        "user_id": user_id,
        "tier": tier,
        "trial_end": subscription.trial_end
    })
    
    # Trial expiry reminder (email day 12)
    await schedule_email(
        user_id,
        template="trial_ending_soon",
        send_at=subscription.trial_end - timedelta(days=2)
    )
```

---

## 🎫 COUPONS & PROMOTIONS

```python
# backend/billing/coupons.py
async def create_coupon(code: str, discount: int, duration: str):
    """Create promotional coupon"""
    coupon = stripe.Coupon.create(
        id=code,
        percent_off=discount,  # % de réduction
        duration=duration,  # "once", "repeating", "forever"
        duration_in_months=3 if duration == "repeating" else None
    )
    
    return coupon

# Usage examples
await create_coupon("LAUNCH50", 50, "once")  # 50% off first month
await create_coupon("CHENU20", 20, "forever")  # 20% off forever
await create_coupon("Q1DEAL", 30, "repeating")  # 30% off for 3 months
```

---

## 🤝 AFFILIATE PROGRAM

### Commission Structure
- **10% recurring** de toutes les subscriptions générées
- Paiement mensuel via Stripe Connect
- Cookie 90 jours

```python
# backend/affiliates/program.py
class AffiliateProgram:
    async def register_affiliate(self, user_id: str) -> str:
        """Register user as affiliate"""
        affiliate_code = f"CHENU{secrets.token_hex(4).upper()}"
        
        await db.affiliates.insert({
            "user_id": user_id,
            "code": affiliate_code,
            "commission_rate": 0.10,
            "status": "active"
        })
        
        return f"https://chenu.com/?ref={affiliate_code}"
    
    async def track_conversion(self, affiliate_code: str, new_user_id: str):
        """Track affiliate conversion"""
        affiliate = await db.affiliates.get(code=affiliate_code)
        
        await db.affiliate_conversions.insert({
            "affiliate_id": affiliate.id,
            "user_id": new_user_id,
            "conversion_date": datetime.utcnow()
        })
    
    async def pay_commissions(self, month: int, year: int):
        """Monthly affiliate payout"""
        affiliates = await db.affiliates.find(status="active")
        
        for affiliate in affiliates:
            # Calculate commission
            subscriptions = await self.get_affiliate_subscriptions(affiliate.id, month, year)
            total_commission = sum(s.amount * 0.10 for s in subscriptions)
            
            if total_commission >= 50:  # Minimum €50 payout
                # Stripe transfer
                await stripe.Transfer.create(
                    amount=int(total_commission * 100),
                    currency="eur",
                    destination=affiliate.stripe_account
                )
```

---

## 📅 TIMELINE V44

| Semaine | Tâche |
|---------|-------|
| **W1-2** | Stripe subscriptions + webhooks |
| **W3-4** | Pricing tiers implémentation |
| **W5-6** | Marketplace agents (création + achat) |
| **W7-8** | API payante + rate limiting |
| **W9-10** | Token packs in-app |
| **W11-12** | ROI dashboards |
| **W13-14** | Facturation automatique |
| **W15-16** | Trials + coupons |
| **W17-18** | Affiliate program |
| **W19-20** | Revenue analytics dashboard |

---

## ✅ VALIDATION CHECKLIST

- [ ] MRR: €50K
- [ ] Users payants: 1,000
- [ ] Free→Paid conversion: >10%
- [ ] Churn rate: <5% mensuel
- [ ] LTV/CAC ratio: >3:1
- [ ] Marketplace GMV: €5K/mois
- [ ] API revenue: €10K/mois
- [ ] Affiliate conversions: 100+/mois
- [ ] ROI dashboard: 100% users
- [ ] Invoicing: 100% automated

---

*CHE·NU™ Monetization & Business — V44*  
***SCALE. REVENUE. PROFIT.*** 💰
