# 📈 CHE·NU™ — SYSTÈME DE PROGRESSION UTILISATEUR

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           📈 USER PROGRESSION SYSTEM — TRACKING COMPLET                     ║
║                                                                              ║
║     "Chaque utilisateur a son chemin — Nova le comprend"                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Version**: 1.0
**Date**: 23 Décembre 2025

---

# 1. MODÈLE DE PROGRESSION

## 1.1 États de Progression Globale

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ÉTATS DE PROGRESSION UTILISATEUR                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐    │
│  │  NEWCOMER   │──▶│  EXPLORER   │──▶│   ACTIVE    │──▶│   EXPERT    │    │
│  │   (0-7j)    │   │   (7-30j)   │   │  (30-90j)   │   │   (90j+)    │    │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘    │
│                                                                             │
│  NEWCOMER:                                                                  │
│  • Découverte initiale                                                      │
│  • Tutoriels système                                                        │
│  • Nova très présente                                                       │
│  • Questions minimales                                                      │
│                                                                             │
│  EXPLORER:                                                                  │
│  • Exploration des sphères                                                  │
│  • Tutoriels contextuels                                                    │
│  • Nova guide modérément                                                    │
│  • Questions contextuelles                                                  │
│                                                                             │
│  ACTIVE:                                                                    │
│  • Usage régulier                                                           │
│  • Tutoriels avancés                                                        │
│  • Nova en support                                                          │
│  • Questions d'optimisation                                                 │
│                                                                             │
│  EXPERT:                                                                    │
│  • Maîtrise du système                                                      │
│  • Features avancées                                                        │
│  • Nova discrète                                                            │
│  • Questions rares                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 Critères de Transition

```typescript
interface ProgressionCriteria {
  newcomerToExplorer: {
    minDays: 7;
    OR: {
      tutorialsCompleted: 3;
      spheresVisited: 2;
      actionsPerformed: 20;
    };
  };
  
  explorerToActive: {
    minDays: 30;
    AND: {
      tutorialsCompleted: 10;
      spheresActive: 2;      // Usage régulier dans 2+ sphères
      piecesCollected: 20;
      sessionsPerWeek: 3;
    };
  };
  
  activeToExpert: {
    minDays: 90;
    AND: {
      tutorialsCompleted: 30;
      featuresUnlocked: 15;
      piecesCollected: 50;
      advancedFeaturesUsed: 5;
      sessionsPerWeek: 5;
    };
  };
}
```

---

# 2. SCORE DE COMPLÉTION

## 2.1 Calcul du Score Global

```typescript
interface UserProgressionScore {
  // Score global (0-100)
  globalScore: number;
  
  // Sous-scores
  scores: {
    puzzleCompletion: number;      // % pièces collectées
    tutorialProgress: number;      // % tutoriels complétés
    featureAdoption: number;       // % features utilisées
    sphereBalance: number;         // Équilibre usage sphères
    engagementLevel: number;       // Régularité sessions
  };
  
  // Niveau
  level: 'newcomer' | 'explorer' | 'active' | 'expert';
  
  // Progression vers niveau suivant
  nextLevelProgress: number;       // 0-100%
  
  // Métriques détaillées
  metrics: {
    totalPieces: number;
    collectedPieces: number;
    totalTutorials: number;
    completedTutorials: number;
    totalFeatures: number;
    usedFeatures: number;
    daysActive: number;
    lastSessionDate: Date;
  };
}
```

## 2.2 Formule de Calcul

```typescript
function calculateProgressionScore(userId: string): UserProgressionScore {
  const metrics = getUserMetrics(userId);
  
  // Calcul des sous-scores
  const puzzleCompletion = (metrics.collectedPieces / metrics.totalPieces) * 100;
  const tutorialProgress = (metrics.completedTutorials / metrics.totalTutorials) * 100;
  const featureAdoption = (metrics.usedFeatures / metrics.totalFeatures) * 100;
  const sphereBalance = calculateSphereBalance(userId);
  const engagementLevel = calculateEngagement(userId);
  
  // Pondération pour score global
  const globalScore = (
    puzzleCompletion * 0.25 +
    tutorialProgress * 0.20 +
    featureAdoption * 0.25 +
    sphereBalance * 0.15 +
    engagementLevel * 0.15
  );
  
  return {
    globalScore,
    scores: {
      puzzleCompletion,
      tutorialProgress,
      featureAdoption,
      sphereBalance,
      engagementLevel,
    },
    level: determineLevel(metrics),
    nextLevelProgress: calculateNextLevelProgress(metrics),
    metrics,
  };
}
```

---

# 3. TRACKING PAR SPHÈRE

## 3.1 Progression par Sphère

```typescript
interface SphereProgression {
  sphereId: string;
  sphereName: string;
  
  // État
  status: 'locked' | 'discovered' | 'exploring' | 'active' | 'mastered';
  
  // Métriques
  metrics: {
    firstVisit: Date | null;
    lastVisit: Date | null;
    totalVisits: number;
    timeSpentMinutes: number;
    actionsPerformed: number;
  };
  
  // Pièces
  puzzle: {
    totalPieces: number;
    collectedPieces: number;
    essentialPieces: number;
    essentialCollected: number;
  };
  
  // Tutoriels
  tutorials: {
    totalAvailable: number;
    unlocked: number;
    completed: number;
    inProgress: number;
  };
  
  // Features
  features: {
    totalAvailable: number;
    unlocked: number;
    used: number;
  };
  
  // Score sphère (0-100)
  sphereScore: number;
}
```

## 3.2 Tableau de Bord Progression

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TABLEAU DE BORD PROGRESSION                               ║
║                         (Exemple Utilisateur)                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  NIVEAU GLOBAL: EXPLORER                    SCORE: 45/100                   ║
║  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 45%          ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ SPHÈRE          │ STATUT     │ PIÈCES  │ TUTORIELS │ FEATURES │ SCORE │ ║
║  ├────────────────────────────────────────────────────────────────────────┤ ║
║  │ 🏠 Personal     │ Active     │ 6/12    │ 4/8       │ 8/15     │  62   │ ║
║  │ 💼 Business     │ Exploring  │ 8/18    │ 3/12      │ 5/20     │  41   │ ║
║  │ 🏛️ Government   │ Discovered │ 1/8     │ 0/5       │ 0/10     │  12   │ ║
║  │ 🎨 Creative     │ Locked     │ 0/10    │ 0/6       │ 0/12     │   0   │ ║
║  │ 👥 Community    │ Locked     │ 0/8     │ 0/5       │ 0/10     │   0   │ ║
║  │ 📱 Social       │ Locked     │ 0/6     │ 0/4       │ 0/8      │   0   │ ║
║  │ 🎬 Entertainment│ Discovered │ 2/6     │ 1/4       │ 2/8      │  25   │ ║
║  │ 🤝 My Team      │ Locked     │ 0/10    │ 0/8       │ 0/15     │   0   │ ║
║  │ 📚 Scholar      │ Locked     │ 0/8     │ 0/5       │ 0/10     │   0   │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  PROGRESSION VERS NIVEAU SUIVANT (Active):                                   ║
║  ██████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 68%           ║
║                                                                              ║
║  • Tutoriels complétés: 8/10 ✓                                              ║
║  • Sphères actives: 1/2 (besoin: 1 de plus)                                 ║
║  • Pièces collectées: 17/20 (besoin: 3 de plus)                             ║
║  • Sessions/semaine: 4/3 ✓                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 4. MILESTONES & ACHIEVEMENTS

## 4.1 Système de Milestones

```typescript
interface Milestone {
  id: string;
  category: 'onboarding' | 'puzzle' | 'tutorial' | 'feature' | 'engagement';
  
  // Définition
  name: { fr: string; en: string };
  description: { fr: string; en: string };
  icon: string;
  
  // Condition
  condition: MilestoneCondition;
  
  // Récompense
  reward?: {
    unlocks?: string[];        // IDs features/tutoriels
    novaMessage?: { fr: string; en: string };
    celebration?: 'confetti' | 'badge' | 'notification';
  };
  
  // État
  status: 'locked' | 'in_progress' | 'achieved';
  achievedAt?: Date;
}

type MilestoneCondition = 
  | { type: 'piece_count'; count: number }
  | { type: 'tutorial_count'; count: number }
  | { type: 'feature_used'; featureId: string }
  | { type: 'days_active'; days: number }
  | { type: 'sphere_mastered'; sphereId: string }
  | { type: 'custom'; check: (user: User) => boolean };
```

## 4.2 Liste des Milestones

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         MILESTONES CHE·NU                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ONBOARDING                                                                  ║
║  ─────────                                                                   ║
║  🎯 Premier Pas         │ Compléter tutoriel bienvenue                      ║
║  🔍 Explorateur         │ Visiter 3 sphères différentes                     ║
║  📝 Première Note       │ Créer première note                               ║
║  ✅ Première Tâche      │ Créer première tâche                              ║
║  💬 Premier Thread      │ Créer premier thread                              ║
║                                                                              ║
║  PUZZLE                                                                      ║
║  ──────                                                                      ║
║  🧩 Collectionneur      │ 10 pièces collectées                              ║
║  🧩 Puzzle Master       │ 25 pièces collectées                              ║
║  🧩 Puzzle Legend       │ 50 pièces collectées                              ║
║  🎯 Profil Complet      │ Toutes pièces essentielles d'une sphère          ║
║                                                                              ║
║  TUTORIELS                                                                   ║
║  ─────────                                                                   ║
║  📚 Étudiant            │ 5 tutoriels complétés                             ║
║  📚 Diplômé             │ 15 tutoriels complétés                            ║
║  📚 Expert              │ 30 tutoriels complétés                            ║
║  🎓 Maître              │ Tous tutoriels d'une sphère                       ║
║                                                                              ║
║  FEATURES                                                                    ║
║  ────────                                                                    ║
║  ⚡ Power User          │ 10 features utilisées                              ║
║  ⚡ Super User          │ 25 features utilisées                              ║
║  🔓 Débloqueur          │ Première feature débloquée par pièce             ║
║  🌟 Feature Master      │ Toutes features d'un module                       ║
║                                                                              ║
║  ENGAGEMENT                                                                  ║
║  ──────────                                                                  ║
║  📅 7 Jours             │ 7 jours consécutifs d'utilisation                 ║
║  📅 30 Jours            │ 30 jours consécutifs d'utilisation                ║
║  📅 Fidèle              │ 3 mois d'utilisation active                       ║
║  🏠 Maître de Sphère    │ Score 90+ dans une sphère                         ║
║                                                                              ║
║  DOMAINES                                                                    ║
║  ────────                                                                    ║
║  🏗️ Pro Construction    │ Module Construction maîtrisé                      ║
║  🏢 Pro Immobilier      │ Module Immobilier maîtrisé                        ║
║  🎨 Pro Créatif         │ Sphère Creative maîtrisée                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 5. ANALYTICS & REPORTING

## 5.1 Métriques Utilisateur

```typescript
interface UserAnalytics {
  userId: string;
  
  // Activité
  activity: {
    totalSessions: number;
    totalTimeMinutes: number;
    averageSessionMinutes: number;
    lastActiveAt: Date;
    streakDays: number;
    longestStreak: number;
  };
  
  // Engagement
  engagement: {
    actionsPerSession: number;
    featuresUsedPerSession: number;
    tutorialsStartedVsCompleted: number; // Ratio
    questionsAnsweredVsSkipped: number;  // Ratio
  };
  
  // Progression
  progression: {
    currentLevel: string;
    daysToNextLevel: number | null;
    progressionVelocity: number; // Pièces/semaine
  };
  
  // Préférences détectées
  preferences: {
    preferredSpheres: string[];
    preferredTimeOfDay: 'morning' | 'afternoon' | 'evening' | 'night';
    preferredDevice: 'desktop' | 'mobile' | 'tablet';
    communicationStyle: 'minimal' | 'balanced' | 'detailed';
  };
  
  // Risques
  risks: {
    churnRisk: 'low' | 'medium' | 'high';
    lastRiskAssessment: Date;
    inactiveDays: number;
    engagementTrend: 'increasing' | 'stable' | 'decreasing';
  };
}
```

## 5.2 Tableau de Bord Admin

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ANALYTICS PROGRESSION — VUE ADMIN                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DISTRIBUTION DES NIVEAUX                         PÉRIODE: 30 derniers jours║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                                                                        │ ║
║  │  Newcomer   ████████████████████████████████████░░░░░░░░░  35%        │ ║
║  │  Explorer   ██████████████████████████░░░░░░░░░░░░░░░░░░░  28%        │ ║
║  │  Active     ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  22%        │ ║
║  │  Expert     ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  15%        │ ║
║  │                                                                        │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  MÉTRIQUES CLÉS                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                                                                        │ ║
║  │  Pièces collectées/user      │ 23.4     │ ▲ +12% vs mois dernier      │ ║
║  │  Tutoriels complétés/user    │ 8.2      │ ▲ +8%  vs mois dernier      │ ║
║  │  Questions répondues         │ 67%      │ ▼ -3%  vs mois dernier      │ ║
║  │  Temps progression Newcomer→Explorer  │ 12 jours │ ▲ -2j amélioration │ ║
║  │                                                                        │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  TUTORIELS LES PLUS COMPLÉTÉS                                               ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  1. TUT-000 Bienvenue           │ 98% │ ████████████████████████████  │ ║
║  │  2. TUT-001 Sphères             │ 89% │ █████████████████████████     │ ║
║  │  3. TUT-B01 Facturation         │ 72% │ █████████████████████         │ ║
║  │  4. TUT-003 Threads             │ 68% │ ███████████████████           │ ║
║  │  5. TUT-P01 Budget              │ 54% │ ███████████████               │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  TUTORIELS LES PLUS SKIPPÉS                                                 ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  1. TUT-CON-RBQ-ADV             │ 45% skip │ ⚠️ Revoir contenu?        │ ║
║  │  2. TUT-B-TEAM-L                │ 38% skip │                           │ ║
║  │  3. TUT-IMM-PORT                │ 32% skip │                           │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  QUESTIONS LES PLUS SKIPPÉES                                                ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  1. Q-PROJ-002 Méthodologie     │ 52% skip │ Timing? Reformuler?       │ ║
║  │  2. Q-DASH-002 Densité          │ 41% skip │                           │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# 6. SCHÉMA BASE DE DONNÉES PROGRESSION

```sql
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLES PROGRESSION UTILISATEUR
-- ═══════════════════════════════════════════════════════════════════════════

-- État de progression global
CREATE TABLE user_progression (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) UNIQUE,
    
    -- Niveau
    level VARCHAR(20) DEFAULT 'newcomer',
    level_achieved_at TIMESTAMP,
    
    -- Score global
    global_score INTEGER DEFAULT 0,
    
    -- Sous-scores
    puzzle_score INTEGER DEFAULT 0,
    tutorial_score INTEGER DEFAULT 0,
    feature_score INTEGER DEFAULT 0,
    sphere_score INTEGER DEFAULT 0,
    engagement_score INTEGER DEFAULT 0,
    
    -- Métriques
    total_pieces_collected INTEGER DEFAULT 0,
    total_tutorials_completed INTEGER DEFAULT 0,
    total_features_used INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    total_time_minutes INTEGER DEFAULT 0,
    
    -- Streak
    current_streak_days INTEGER DEFAULT 0,
    longest_streak_days INTEGER DEFAULT 0,
    last_active_date DATE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Progression par sphère
CREATE TABLE user_sphere_progression (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    sphere_id VARCHAR(50) NOT NULL,
    
    -- État
    status VARCHAR(20) DEFAULT 'locked',
    
    -- Métriques
    first_visit_at TIMESTAMP,
    last_visit_at TIMESTAMP,
    total_visits INTEGER DEFAULT 0,
    time_spent_minutes INTEGER DEFAULT 0,
    actions_performed INTEGER DEFAULT 0,
    
    -- Puzzle
    pieces_total INTEGER DEFAULT 0,
    pieces_collected INTEGER DEFAULT 0,
    essential_pieces_total INTEGER DEFAULT 0,
    essential_pieces_collected INTEGER DEFAULT 0,
    
    -- Tutoriels
    tutorials_available INTEGER DEFAULT 0,
    tutorials_unlocked INTEGER DEFAULT 0,
    tutorials_completed INTEGER DEFAULT 0,
    
    -- Features
    features_available INTEGER DEFAULT 0,
    features_unlocked INTEGER DEFAULT 0,
    features_used INTEGER DEFAULT 0,
    
    -- Score
    sphere_score INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, sphere_id)
);

-- Milestones utilisateur
CREATE TABLE user_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    milestone_id VARCHAR(100) NOT NULL,
    
    -- État
    status VARCHAR(20) DEFAULT 'locked',
    progress INTEGER DEFAULT 0,      -- Progression 0-100
    
    -- Achievement
    achieved_at TIMESTAMP,
    
    -- Récompenses accordées
    rewards_granted BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, milestone_id)
);

-- Historique de progression (pour analytics)
CREATE TABLE progression_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Snapshot
    snapshot_date DATE NOT NULL,
    level VARCHAR(20),
    global_score INTEGER,
    
    -- Détail scores
    scores JSONB,
    
    -- Métriques du jour
    daily_metrics JSONB,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, snapshot_date)
);

-- Index
CREATE INDEX idx_progression_level ON user_progression(level);
CREATE INDEX idx_progression_score ON user_progression(global_score DESC);
CREATE INDEX idx_sphere_progression_status ON user_sphere_progression(status);
CREATE INDEX idx_milestones_achieved ON user_milestones(achieved_at) WHERE achieved_at IS NOT NULL;

-- ═══════════════════════════════════════════════════════════════════════════
-- FONCTIONS
-- ═══════════════════════════════════════════════════════════════════════════

-- Recalcul du score global
CREATE OR REPLACE FUNCTION recalculate_progression_score(p_user_id UUID)
RETURNS void AS $$
DECLARE
    v_puzzle_score INTEGER;
    v_tutorial_score INTEGER;
    v_feature_score INTEGER;
    v_sphere_score INTEGER;
    v_engagement_score INTEGER;
    v_global_score INTEGER;
BEGIN
    -- Calculer puzzle score
    SELECT COALESCE(
        (SUM(pieces_collected)::FLOAT / NULLIF(SUM(pieces_total), 0) * 100)::INTEGER,
        0
    ) INTO v_puzzle_score
    FROM user_sphere_progression
    WHERE user_id = p_user_id;
    
    -- Calculer tutorial score
    SELECT COALESCE(
        (SUM(tutorials_completed)::FLOAT / NULLIF(SUM(tutorials_available), 0) * 100)::INTEGER,
        0
    ) INTO v_tutorial_score
    FROM user_sphere_progression
    WHERE user_id = p_user_id;
    
    -- Calculer feature score
    SELECT COALESCE(
        (SUM(features_used)::FLOAT / NULLIF(SUM(features_available), 0) * 100)::INTEGER,
        0
    ) INTO v_feature_score
    FROM user_sphere_progression
    WHERE user_id = p_user_id;
    
    -- Calculer sphere balance score
    SELECT COALESCE(
        (COUNT(CASE WHEN status IN ('active', 'mastered') THEN 1 END)::FLOAT / 
         NULLIF(COUNT(*), 0) * 100)::INTEGER,
        0
    ) INTO v_sphere_score
    FROM user_sphere_progression
    WHERE user_id = p_user_id;
    
    -- Calculer engagement (basé sur streak et régularité)
    SELECT COALESCE(
        LEAST(current_streak_days * 5, 100),
        0
    ) INTO v_engagement_score
    FROM user_progression
    WHERE user_id = p_user_id;
    
    -- Calcul score global pondéré
    v_global_score := (
        v_puzzle_score * 0.25 +
        v_tutorial_score * 0.20 +
        v_feature_score * 0.25 +
        v_sphere_score * 0.15 +
        v_engagement_score * 0.15
    )::INTEGER;
    
    -- Mettre à jour
    UPDATE user_progression SET
        puzzle_score = v_puzzle_score,
        tutorial_score = v_tutorial_score,
        feature_score = v_feature_score,
        sphere_score = v_sphere_score,
        engagement_score = v_engagement_score,
        global_score = v_global_score,
        updated_at = NOW()
    WHERE user_id = p_user_id;
    
END;
$$ LANGUAGE plpgsql;

-- Vérification niveau
CREATE OR REPLACE FUNCTION check_level_progression(p_user_id UUID)
RETURNS void AS $$
DECLARE
    v_current_level VARCHAR(20);
    v_new_level VARCHAR(20);
    v_metrics RECORD;
BEGIN
    -- Récupérer métriques
    SELECT * INTO v_metrics FROM user_progression WHERE user_id = p_user_id;
    v_current_level := v_metrics.level;
    
    -- Déterminer nouveau niveau
    IF v_metrics.total_sessions >= 50 
       AND v_metrics.total_tutorials_completed >= 30 
       AND v_metrics.total_features_used >= 15 THEN
        v_new_level := 'expert';
    ELSIF v_metrics.total_sessions >= 20 
          AND v_metrics.total_tutorials_completed >= 10 
          AND v_metrics.total_pieces_collected >= 20 THEN
        v_new_level := 'active';
    ELSIF v_metrics.total_sessions >= 5 
          OR v_metrics.total_tutorials_completed >= 3 THEN
        v_new_level := 'explorer';
    ELSE
        v_new_level := 'newcomer';
    END IF;
    
    -- Mettre à jour si changement
    IF v_new_level != v_current_level THEN
        UPDATE user_progression SET
            level = v_new_level,
            level_achieved_at = NOW(),
            updated_at = NOW()
        WHERE user_id = p_user_id;
        
        -- Notifier
        PERFORM pg_notify('level_change', json_build_object(
            'user_id', p_user_id,
            'old_level', v_current_level,
            'new_level', v_new_level
        )::text);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Snapshot quotidien
CREATE OR REPLACE FUNCTION create_daily_snapshot()
RETURNS void AS $$
BEGIN
    INSERT INTO progression_history (user_id, snapshot_date, level, global_score, scores, daily_metrics)
    SELECT 
        user_id,
        CURRENT_DATE,
        level,
        global_score,
        jsonb_build_object(
            'puzzle', puzzle_score,
            'tutorial', tutorial_score,
            'feature', feature_score,
            'sphere', sphere_score,
            'engagement', engagement_score
        ),
        jsonb_build_object(
            'pieces', total_pieces_collected,
            'tutorials', total_tutorials_completed,
            'features', total_features_used,
            'sessions', total_sessions,
            'time', total_time_minutes
        )
    FROM user_progression
    ON CONFLICT (user_id, snapshot_date) DO UPDATE SET
        level = EXCLUDED.level,
        global_score = EXCLUDED.global_score,
        scores = EXCLUDED.scores,
        daily_metrics = EXCLUDED.daily_metrics;
END;
$$ LANGUAGE plpgsql;
```

---

# 7. API PROGRESSION

```typescript
// Routes API Progression

// ═══════════════════════════════════════════════════════════════════════════
// GET /api/progression/:userId
// Retourne l'état de progression complet
// ═══════════════════════════════════════════════════════════════════════════
interface ProgressionResponse {
  user: {
    id: string;
    level: 'newcomer' | 'explorer' | 'active' | 'expert';
    globalScore: number;
    scores: {
      puzzle: number;
      tutorial: number;
      feature: number;
      sphere: number;
      engagement: number;
    };
    streak: {
      current: number;
      longest: number;
    };
  };
  spheres: SphereProgression[];
  milestones: {
    achieved: Milestone[];
    inProgress: Milestone[];
    locked: Milestone[];
  };
  nextLevel: {
    name: string;
    progress: number;
    requirements: {
      name: string;
      current: number;
      target: number;
      met: boolean;
    }[];
  } | null;
}

// ═══════════════════════════════════════════════════════════════════════════
// GET /api/progression/:userId/history
// Retourne l'historique de progression
// ═══════════════════════════════════════════════════════════════════════════
interface ProgressionHistoryResponse {
  history: {
    date: string;
    level: string;
    globalScore: number;
    scores: Record<string, number>;
  }[];
  trends: {
    scoreChange30d: number;
    velocityPiecesPerWeek: number;
    velocityTutorialsPerWeek: number;
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// GET /api/progression/:userId/recommendations
// Retourne les recommandations personnalisées
// ═══════════════════════════════════════════════════════════════════════════
interface RecommendationsResponse {
  nextTutorials: {
    id: string;
    title: string;
    reason: string;
    priority: 'high' | 'medium' | 'low';
  }[];
  nextPieces: {
    id: string;
    name: string;
    howToCollect: string;
    impact: string;
  }[];
  suggestedSpheres: {
    id: string;
    name: string;
    reason: string;
  }[];
  milestoneOpportunities: {
    id: string;
    name: string;
    progress: number;
    remaining: string;
  }[];
}
```

---

# 8. COMPOSANTS UI

## 8.1 Progression Widget

```typescript
// components/progression/ProgressionWidget.tsx

interface ProgressionWidgetProps {
  userId: string;
  variant: 'compact' | 'detailed' | 'full';
}

const ProgressionWidget: React.FC<ProgressionWidgetProps> = ({ userId, variant }) => {
  // Compact: Juste le niveau et score
  // Detailed: + barres de progression
  // Full: + liste sphères + milestones proches
  
  return (
    <div className="progression-widget">
      {/* Niveau actuel */}
      <LevelBadge level={progression.level} />
      
      {/* Score global */}
      <ScoreCircle score={progression.globalScore} />
      
      {variant !== 'compact' && (
        <>
          {/* Barres sous-scores */}
          <ScoreBreakdown scores={progression.scores} />
          
          {/* Progression vers niveau suivant */}
          <NextLevelProgress next={progression.nextLevel} />
        </>
      )}
      
      {variant === 'full' && (
        <>
          {/* Sphères */}
          <SpheresOverview spheres={progression.spheres} />
          
          {/* Milestones proches */}
          <UpcomingMilestones milestones={progression.milestones.inProgress} />
        </>
      )}
    </div>
  );
};
```

## 8.2 Milestone Card

```typescript
// components/progression/MilestoneCard.tsx

interface MilestoneCardProps {
  milestone: Milestone;
  showProgress?: boolean;
}

const MilestoneCard: React.FC<MilestoneCardProps> = ({ milestone, showProgress }) => {
  return (
    <div className={`milestone-card ${milestone.status}`}>
      <span className="milestone-icon">{milestone.icon}</span>
      
      <div className="milestone-content">
        <h4>{milestone.name}</h4>
        <p>{milestone.description}</p>
        
        {showProgress && milestone.status === 'in_progress' && (
          <ProgressBar progress={milestone.progress} />
        )}
        
        {milestone.status === 'achieved' && (
          <span className="achieved-date">
            ✓ {formatDate(milestone.achievedAt)}
          </span>
        )}
      </div>
    </div>
  );
};
```

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    SYSTÈME DE PROGRESSION COMPLET                            ║
║                                                                              ║
║     4 Niveaux | 30+ Milestones | Tracking Temps Réel                        ║
║                                                                              ║
║           "Chaque action compte — Chaque progrès est visible"               ║
║                                                                              ║
║                          ON CONTINUE! 💪🔥                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
