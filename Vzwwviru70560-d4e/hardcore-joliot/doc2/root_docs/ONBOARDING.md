# 🎯 CHE·NU™ - ONBOARDING & ADOPTION

**Version:** V43  
**Status:** POST-MVP ENHANCEMENTS – RECOMMENDED BY GROK  
**Goal:** >80% completion, <10min time-to-value  

---

## 🎯 OBJECTIF

Maximiser adoption + rétention via onboarding fluide et Nova-guided.

---

## 🚀 WIZARD INTERACTIF (5 ÉTAPES)

### Étape 1: Welcome + Value Proposition
```jsx
// Welcome screen
<OnboardingStep step={1}>
  <h1>Bienvenue sur CHE·NU 👋</h1>
  <p>Votre système d'exploitation d'intelligence gouvernée</p>
  
  <Features>
    <Feature icon="🏠">9 Spheres pour gérer votre vie</Feature>
    <Feature icon="🤖">168 Agents IA spécialisés</Feature>
    <Feature icon="💬">Threads persistants avec gouvernance</Feature>
    <Feature icon="📱">Mobile + Desktop + PWA</Feature>
  </Features>
  
  <Button onClick={nextStep}>Commencer</Button>
</OnboardingStep>
```

### Étape 2: Choix Sphère Initiale
```jsx
<OnboardingStep step={2}>
  <h2>Choisissez votre première sphère</h2>
  <p>Par où voulez-vous commencer?</p>
  
  <SphereSelector>
    <SphereOption id="personal" popular>
      🏠 Personal - Gérer ma vie perso
    </SphereOption>
    <SphereOption id="business" recommended>
      💼 Business - CRM & productivité pro
    </SphereOption>
    <SphereOption id="scholar">
      📚 Scholar - Recherche & citations
    </SphereOption>
  </SphereSelector>
</OnboardingStep>
```

### Étape 3: Premier Thread Guidé
```jsx
<OnboardingStep step={3}>
  <h2>Créez votre premier thread</h2>
  <NovaGuide>
    Nova 🌟: "Un thread est une ligne de pensée persistante. 
    Je vais vous aider à créer votre premier!"
  </NovaGuide>
  
  <ThreadCreator>
    <Input placeholder="Ex: Planifier mes vacances d'été" />
    <BudgetSlider min={100} max={1000} default={500} />
    <Button>Créer avec Nova</Button>
  </ThreadCreator>
</OnboardingStep>
```

### Étape 4: Exécution Premier Agent
```jsx
<OnboardingStep step={4}>
  <h2>Faites travailler un agent pour vous</h2>
  <NovaGuide>
    Nova 🌟: "Les agents exécutent des tâches. 
    Essayons ensemble!"
  </NovaGuide>
  
  <AgentDemo>
    <AgentCard agent="business.crm_assistant">
      📇 Assistant CRM - Gérer vos contacts
    </AgentCard>
    <PreviewExecution>
      "Lister mes 10 derniers contacts"
    </PreviewExecution>
    <Button>Exécuter (Safe Mode)</Button>
  </AgentDemo>
</OnboardingStep>
```

### Étape 5: Quick Capture + Mobile
```jsx
<OnboardingStep step={5}>
  <h2>Capturez vos idées rapidement</h2>
  <NovaGuide>
    Nova 🌟: "Utilisez ⚡ Quick Capture partout: 
    Desktop (Ctrl+Shift+C), Mobile (bouton flottant)"
  </NovaGuide>
  
  <QuickCaptureDemo />
  
  <MobilePrompt>
    📱 Installez CHE·NU sur mobile?
    <Button>Installer PWA</Button>
    <Button variant="ghost">Plus tard</Button>
  </MobilePrompt>
  
  <Button onClick={finishOnboarding}>
    Commencer avec CHE·NU 🚀
  </Button>
</OnboardingStep>
```

---

## 📚 TUTORIELS NOVA-GUIDED

### 1 Tutoriel par Sphère

#### Personal 🏠
```
Nova: "Bienvenue dans Personal! Voici comment:
1. Créer un journal quotidien (Notes)
2. Tracker vos habitudes (Dashboard)
3. Gérer vos finances perso (Budget)
4. Planifier vos objectifs (Tasks + Projects)"

Interactive: ✅ Checkbox quiz après chaque étape
Duration: ~5 min
```

#### Business 💼
```
Nova: "Business est votre CRM + productivité pro:
1. Ajouter vos contacts (CRM)
2. Créer une facture (Invoice)
3. Planifier un meeting (Meetings)
4. Suivre un deal (Pipeline)"

Interactive: ✅ Actions réelles dans le système
Duration: ~7 min
```

#### Scholar 📚
```
Nova: "Scholar pour la recherche académique:
1. Ajouter une référence (Book/Article)
2. Générer une citation APA
3. Créer des flashcards
4. Réviser avec spaced repetition"

Interactive: ✅ Créer vraies flashcards
Duration: ~6 min
```

### Format Tutoriel
```jsx
<TutorialFlow sphere="business">
  <Step number={1} checkpoint>
    <NovaExplanation>
      "Les contacts sont la base de votre CRM..."
    </NovaExplanation>
    <InteractiveTask>
      Ajouter un contact: [Formulaire]
    </InteractiveTask>
    <Validation>
      ✅ Contact créé! +10 XP
    </Validation>
  </Step>
  
  <Step number={2}>
    ...
  </Step>
  
  <Completion>
    🎉 Tutoriel Business complété!
    Badge: "Business Pro" unlocked
  </Completion>
</TutorialFlow>
```

---

## 📋 TEMPLATES PRÉ-CONFIGURÉS

### Personal Templates
- **Journal Quotidien** (Notes pré-structurées)
- **Budget Mensuel** (Excel-like tracker)
- **Objectifs SMART** (Framework structuré)
- **Routine Matinale** (Checklist recurring)

### Business Templates
- **Pipeline de Ventes** (5 stages standard)
- **Facture Freelance** (Format professionnel)
- **Meeting Agenda** (Structure type)
- **Onboarding Client** (Workflow complet)

### Scholar Templates
- **Bibliographie** (Collection références)
- **Notes de Lecture** (Cornell method)
- **Flashcards Deck** (Spaced repetition)
- **Synthèse Chapitre** (Structure analytique)

```python
# backend/templates/template_engine.py
class TemplateEngine:
    async def apply_template(
        self,
        template_id: str,
        sphere_id: str,
        user_id: str
    ):
        """Apply pre-configured template"""
        template = await self.load_template(template_id)
        
        # Create resources
        for resource in template.resources:
            if resource.type == "thread":
                await threads.create(resource.config, user_id)
            elif resource.type == "note":
                await notes.create(resource.content, sphere_id)
            elif resource.type == "task":
                await tasks.create(resource.data, user_id)
        
        # Track template usage
        await analytics.track("template_applied", {
            "template_id": template_id,
            "user_id": user_id
        })
```

---

## 📊 FEEDBACK LOOP BETA USERS

### NPS Survey (Net Promoter Score)
```jsx
<NPSSurvey trigger="day-7">
  <Question>
    Sur une échelle de 0 à 10, recommanderiez-vous CHE·NU?
    <Scale min={0} max={10} />
  </Question>
  
  {score <= 6 && (
    <FollowUp>
      Que pouvons-nous améliorer?
      <TextArea rows={3} />
    </FollowUp>
  )}
  
  {score >= 9 && (
    <Incentive>
      Merci! Partagez CHE·NU et gagnez 1000 tokens 🎁
      <ShareButtons />
    </Incentive>
  )}
</NPSSurvey>
```

### In-App Surveys
```python
# backend/feedback/surveys.py
surveys = [
    {
        "id": "onboarding_completion",
        "trigger": "onboarding_finished",
        "questions": [
            "L'onboarding était-il clair? (1-5)",
            "Temps pour comprendre CHE·NU? (<5min, 5-10min, >10min)",
            "Quelle fonctionnalité vous a le plus impressionné?"
        ]
    },
    {
        "id": "feature_usage",
        "trigger": "day-14",
        "questions": [
            "Quelle sphère utilisez-vous le plus?",
            "Utilisez-vous Quick Capture? (Oui/Non)",
            "Manque-t-il une fonctionnalité? (Texte libre)"
        ]
    }
]
```

---

## 📈 ANALYTICS ADOPTION

### Metrics Trackées
```python
# Acquisition
signup_source: str  # Organic, Referral, Paid
signup_date: datetime

# Activation
onboarding_started: bool
onboarding_completed: bool
time_to_first_thread: int  # seconds
first_sphere_chosen: str

# Engagement
daily_active_users (DAU)
weekly_active_users (WAU)
monthly_active_users (MAU)
threads_per_week: int
agents_executed_per_week: int

# Retention
d1_retention: bool  # Retour jour 1
d7_retention: bool  # Retour jour 7
d30_retention: bool  # Retour jour 30

# Referral
referrals_sent: int
referrals_converted: int
```

### Dashboards (Mixpanel/Amplitude)
```javascript
// Funnel analysis
Signup → Onboarding Start → Complete → First Thread → D7 Active

// Cohort analysis
Retention by signup week
Retention by first sphere chosen
Retention by template used

// Feature adoption
Quick Capture usage over time
Agent execution frequency
Mobile vs Desktop split
```

---

## 🌍 MULTILINGUE (6 LANGUES)

### Langues Supportées
- 🇫🇷 Français (primary)
- 🇬🇧 English
- 🇪🇸 Español
- 🇩🇪 Deutsch
- 🇮🇹 Italiano
- 🇵🇹 Português

### i18n Implementation
```typescript
// frontend/src/i18n/index.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: require('./locales/en.json') },
      fr: { translation: require('./locales/fr.json') },
      es: { translation: require('./locales/es.json') },
    },
    lng: 'fr',
    fallbackLng: 'en',
    interpolation: { escapeValue: false }
  });

// Usage
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

---

## 📱 PWA OFFLINE-FIRST ONBOARDING

### Offline Capabilities
```javascript
// Service Worker - onboarding cache
const ONBOARDING_CACHE = 'chenu-onboarding-v1';
const ONBOARDING_ASSETS = [
  '/onboarding/step-1.html',
  '/onboarding/step-2.html',
  '/onboarding/nova-guide.mp4',
  '/onboarding/assets/icons.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(ONBOARDING_CACHE)
      .then((cache) => cache.addAll(ONBOARDING_ASSETS))
  );
});

// Offline detection
if (!navigator.onLine) {
  showOfflineOnboarding(); // Lightweight version
}
```

---

## 🎮 GAMIFICATION

### Achievements
```javascript
const achievements = [
  { id: "first_thread", title: "First Thread", icon: "💬", xp: 10 },
  { id: "5_agents_executed", title: "Agent Master", icon: "🤖", xp: 50 },
  { id: "complete_onboarding", title: "Quick Learner", icon: "🎓", xp: 100 },
  { id: "7_day_streak", title: "Consistency", icon: "🔥", xp: 200 },
  { id: "invite_friend", title: "Ambassador", icon: "🌟", xp: 500 }
];

// Award achievement
async function awardAchievement(user_id, achievement_id) {
  await db.user_achievements.insert({ user_id, achievement_id });
  await notifications.send(user_id, {
    title: `🎉 Achievement Unlocked!`,
    body: `You earned "${achievement.title}" (+${achievement.xp} XP)`
  });
}
```

---

## 🎁 REFERRAL PROGRAM

```python
# backend/referral/program.py
class ReferralProgram:
    async def generate_referral_link(self, user_id: str) -> str:
        """Generate unique referral link"""
        code = secrets.token_urlsafe(8)
        await db.referral_codes.insert({
            "code": code,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        })
        return f"https://chenu.com/signup?ref={code}"
    
    async def track_referral(self, referral_code: str, new_user_id: str):
        """Track successful referral"""
        referrer = await db.referral_codes.get(code=referral_code)
        
        await db.referrals.insert({
            "referrer_id": referrer.user_id,
            "referee_id": new_user_id,
            "status": "pending"  # → "confirmed" after 7 days
        })
    
    async def reward_referrer(self, referral_id: str):
        """Reward referrer (called after 7 days retention)"""
        referral = await db.referrals.get(referral_id)
        
        # Award tokens
        await tokens.add(referral.referrer_id, amount=1000, reason="referral")
        
        # Update status
        await db.referrals.update(referral_id, status="confirmed")
```

---

## 💬 IN-APP CHAT SUPPORT

```jsx
// Intercom/Crisp integration
<SupportChat>
  <Trigger>
    <Button variant="fab" position="bottom-right">
      💬 Aide
    </Button>
  </Trigger>
  
  <ChatWindow>
    <AutoMessage delay={30000}>
      Nova 🌟: "Besoin d'aide? Je suis là!"
    </AutoMessage>
    
    <QuickReplies>
      <Reply>Comment créer un thread?</Reply>
      <Reply>Exécuter un agent</Reply>
      <Reply>Parler à un humain</Reply>
    </QuickReplies>
  </ChatWindow>
</SupportChat>
```

---

## 📅 TIMELINE V43

| Semaine | Tâche |
|---------|-------|
| **W1-2** | Wizard interactif (5 étapes) |
| **W3-4** | 9 tutoriels Nova-guided |
| **W5-6** | Templates pré-configurés |
| **W7-8** | Analytics adoption (Mixpanel) |
| **W9-10** | Multilingue (6 langues) |
| **W11-12** | PWA offline onboarding |
| **W13-14** | Gamification + achievements |
| **W15-16** | Referral program |
| **W17-18** | In-app chat support |
| **W19-20** | A/B testing onboarding variants |

---

## ✅ VALIDATION CHECKLIST

- [ ] Onboarding completion: >80%
- [ ] Time to first thread: <5min
- [ ] Time to first value: <10min
- [ ] D7 retention: >40%
- [ ] D30 retention: >25%
- [ ] NPS score: >50
- [ ] Support tickets: <5% users
- [ ] Template usage: >60% users
- [ ] Referral conversion: >10%
- [ ] 6 langues live

---

*CHE·NU™ Onboarding & Adoption — V43*  
***ENGAGE. ACTIVATE. RETAIN.*** 🎯
