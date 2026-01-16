############################################################
#                                                          #
#              PHASE F: SYSTEM UPDATES                     #
#                                                          #
############################################################

============================================================
F.1 — SYSTEM INDEX JSON (COMPLETE UPDATE)
============================================================

--- FILE: /che-nu-sdk/system_index.json
--- ACTION: REPLACE ENTIRE FILE
--- PRIORITY: F.1

{
  "version": "3.0.0",
  "generated": "2025-12-12",
  "classification_note": "Health, Finance, Knowledge, Emotion, Productivity are OPERATIONAL MODULES, NOT Spheres.",

  "spheres": [
    { "name": "Personal", "path": "/che-nu-sdk/core/spheres/personal.ts", "status": "complete" },
    { "name": "Business", "path": "/che-nu-sdk/core/spheres/business.ts", "status": "complete" },
    { "name": "Creative", "path": "/che-nu-sdk/core/spheres/creative.ts", "status": "complete" },
    { "name": "Scholar", "path": "/che-nu-sdk/core/spheres/scholar.ts", "status": "complete" },
    { "name": "Social", "path": "/che-nu-sdk/core/spheres/social.ts", "status": "complete" },
    { "name": "Community", "path": "/che-nu-sdk/core/spheres/community.ts", "status": "complete" },
    { "name": "XR", "path": "/che-nu-sdk/core/spheres/xr.ts", "status": "complete" },
    { "name": "MyTeam", "path": "/che-nu-sdk/core/spheres/myteam.ts", "status": "complete" }
  ],

  "super_modules": [
    {
      "name": "MethodologyEngine",
      "path": "/che-nu-sdk/core/methodology.ts",
      "status": "complete",
      "classification": "super_module",
      "submodules": [
        { "name": "DecompositionOperator", "path": "/che-nu-sdk/core/methodology/operator.decomposition.ts" },
        { "name": "WorkflowOperator", "path": "/che-nu-sdk/core/methodology/operator.workflow.ts" },
        { "name": "TransformationOperator", "path": "/che-nu-sdk/core/methodology/operator.transformation.ts" },
        { "name": "AnalysisOperator", "path": "/che-nu-sdk/core/methodology/operator.analysis.ts" }
      ]
    },
    {
      "name": "SkillEngine",
      "path": "/che-nu-sdk/core/skill.ts",
      "status": "complete",
      "classification": "super_module",
      "submodules": [
        { "name": "CognitiveSkillsDomain", "path": "/che-nu-sdk/core/skill/domain.cognitive.ts" },
        { "name": "TechnicalSkillsDomain", "path": "/che-nu-sdk/core/skill/domain.technical.ts" },
        { "name": "SocialSkillsDomain", "path": "/che-nu-sdk/core/skill/domain.social.ts" },
        { "name": "CreativeSkillsDomain", "path": "/che-nu-sdk/core/skill/domain.creative.ts" },
        { "name": "PhysicalSkillsDomain", "path": "/che-nu-sdk/core/skill/domain.physical.ts" }
      ]
    }
  ],

  "operational_modules": [
    {
      "name": "HealthEngine",
      "path": "/che-nu-sdk/core/health.ts",
      "status": "complete",
      "classification": "operational_module",
      "attachedTo": ["Personal Sphere", "Agents"],
      "submodules": [
        { "name": "PhysicalEngine", "path": "/che-nu-sdk/core/health/physical.engine.ts" },
        { "name": "MentalEngine", "path": "/che-nu-sdk/core/health/mental.engine.ts" },
        { "name": "SleepEngine", "path": "/che-nu-sdk/core/health/sleep.engine.ts" },
        { "name": "StressEngine", "path": "/che-nu-sdk/core/health/stress.engine.ts" },
        { "name": "EnergyEngine", "path": "/che-nu-sdk/core/health/energy.engine.ts" },
        { "name": "NutritionEngine", "path": "/che-nu-sdk/core/health/nutrition.engine.ts" },
        { "name": "HabitsEngine", "path": "/che-nu-sdk/core/health/habits.engine.ts" },
        { "name": "RecoveryEngine", "path": "/che-nu-sdk/core/health/recovery.engine.ts" }
      ]
    },
    {
      "name": "FinanceEngine",
      "path": "/che-nu-sdk/core/finance.ts",
      "status": "complete",
      "classification": "operational_module",
      "submodules": [
        { "name": "BudgetEngine", "path": "/che-nu-sdk/core/finance/budget.engine.ts" },
        { "name": "CashflowEngine", "path": "/che-nu-sdk/core/finance/cashflow.engine.ts" },
        { "name": "GoalsEngine", "path": "/che-nu-sdk/core/finance/goals.engine.ts" },
        { "name": "RiskProfileEngine", "path": "/che-nu-sdk/core/finance/riskprofile.engine.ts" },
        { "name": "PlanningEngine", "path": "/che-nu-sdk/core/finance/planning.engine.ts" }
      ]
    },
    {
      "name": "KnowledgeEngine",
      "path": "/che-nu-sdk/core/knowledge.ts",
      "status": "complete",
      "classification": "operational_module",
      "submodules": [
        { "name": "GraphEngine", "path": "/che-nu-sdk/core/knowledge/graph.engine.ts" },
        { "name": "ClassifyEngine", "path": "/che-nu-sdk/core/knowledge/classify.engine.ts" },
        { "name": "IndexingEngine", "path": "/che-nu-sdk/core/knowledge/indexing.engine.ts" },
        { "name": "RetrievalEngine", "path": "/che-nu-sdk/core/knowledge/retrieval.engine.ts" },
        { "name": "MappingEngine", "path": "/che-nu-sdk/core/knowledge/mapping.engine.ts" }
      ]
    },
    {
      "name": "EmotionEngine",
      "path": "/che-nu-sdk/core/emotion.ts",
      "status": "complete",
      "classification": "operational_module",
      "submodules": [
        { "name": "ToneEngine", "path": "/che-nu-sdk/core/emotion/tone.engine.ts" },
        { "name": "SelfRegulationEngine", "path": "/che-nu-sdk/core/emotion/selfregulation.engine.ts" },
        { "name": "EmpathyEngine", "path": "/che-nu-sdk/core/emotion/empathy.engine.ts" },
        { "name": "RelationshipEngine", "path": "/che-nu-sdk/core/emotion/relationship.engine.ts" },
        { "name": "SocialMapEngine", "path": "/che-nu-sdk/core/emotion/socialmap.engine.ts" }
      ]
    },
    {
      "name": "ProductivityEngine",
      "path": "/che-nu-sdk/core/productivity.ts",
      "status": "complete",
      "classification": "operational_module",
      "submodules": [
        { "name": "TimeEngine", "path": "/che-nu-sdk/core/productivity/time.engine.ts" },
        { "name": "FocusEngine", "path": "/che-nu-sdk/core/productivity/focus.engine.ts" },
        { "name": "PlanningEngine", "path": "/che-nu-sdk/core/productivity/planning.engine.ts" },
        { "name": "ExecutionEngine", "path": "/che-nu-sdk/core/productivity/execution.engine.ts" },
        { "name": "ContextSwitchEngine", "path": "/che-nu-sdk/core/productivity/contextswitch.engine.ts" }
      ]
    }
  ],

  "transversal_engines": [
    { "name": "MemoryManager", "path": "/che-nu-sdk/core/memory_manager.ts", "status": "complete" },
    { "name": "ReplayEngine", "path": "/che-nu-sdk/core/replay_engine.ts", "status": "complete" },
    { "name": "HyperFabric", "path": "/che-nu-sdk/core/hyper_fabric.ts", "status": "complete" },
    { "name": "DepthLensSystem", "path": "/che-nu-sdk/core/depth_lens.ts", "status": "complete" },
    { "name": "CartographyEngine", "path": "/che-nu-sdk/core/cartography.ts", "status": "complete" },
    { "name": "ProjectionEngine", "path": "/che-nu-sdk/core/projection.ts", "status": "complete" }
  ],

  "schemas": [
    { "name": "methodology.schema.json", "path": "/che-nu-sdk/schemas/methodology.schema.json", "status": "complete" },
    { "name": "skill.schema.json", "path": "/che-nu-sdk/schemas/skill.schema.json", "status": "complete" },
    { "name": "health.schema.json", "path": "/che-nu-sdk/schemas/health.schema.json", "status": "complete" },
    { "name": "finance.schema.json", "path": "/che-nu-sdk/schemas/finance.schema.json", "status": "complete" },
    { "name": "knowledge.schema.json", "path": "/che-nu-sdk/schemas/knowledge.schema.json", "status": "complete" },
    { "name": "emotion.schema.json", "path": "/che-nu-sdk/schemas/emotion.schema.json", "status": "complete" },
    { "name": "productivity.schema.json", "path": "/che-nu-sdk/schemas/productivity.schema.json", "status": "complete" },
    { "name": "community.schema.json", "path": "/che-nu-sdk/schemas/community.schema.json", "status": "complete" },
    { "name": "xr.schema.json", "path": "/che-nu-sdk/schemas/xr.schema.json", "status": "complete" }
  ],

  "statistics": {
    "totalSpheres": 8,
    "totalSuperModules": 2,
    "totalOperationalModules": 5,
    "totalSubEngines": 28,
    "totalSchemas": 9,
    "totalTransversalEngines": 6
  }
}

============================================================
F.3 — ORCHESTRATOR UPDATE
============================================================

--- FILE: /che-nu-sdk/core/orchestrator.ts
--- ACTION: ADD TO determineModule() function
--- PRIORITY: F.3

/**
 * Determine which module handles the request
 * Updated with all operational modules
 */
function determineModule(domain: string, intent: string): string {
  const lowerDomain = domain.toLowerCase();
  const lowerIntent = intent.toLowerCase();

  // ============================================================
  // SPHERES — Domains of life
  // ============================================================
  
  if (lowerDomain === 'personal') return 'PersonalSphere';
  if (lowerDomain === 'business') return 'BusinessSphere';
  if (lowerDomain === 'creative') return 'CreativeSphere';
  if (lowerDomain === 'scholar') return 'ScholarSphere';
  if (lowerDomain === 'social') return 'SocialSphere';
  if (lowerDomain === 'community') return 'CommunitySphere';
  if (lowerDomain === 'xr') return 'XRSphere';
  if (lowerDomain === 'myteam') return 'MyTeamSphere';

  // ============================================================
  // SUPER-MODULES — NOT Spheres
  // ============================================================
  
  if (lowerDomain === 'methodology' || 
      lowerIntent.includes('workflow') ||
      lowerIntent.includes('decompose') ||
      lowerIntent.includes('transformation')) {
    return 'MethodologyEngine';
  }

  if (lowerDomain === 'skill' ||
      lowerIntent.includes('skill') ||
      lowerIntent.includes('learning path')) {
    return 'SkillEngine';
  }

  // ============================================================
  // OPERATIONAL MODULES — NOT Spheres
  // ============================================================
  
  // Health
  if (lowerDomain === 'health' ||
      lowerIntent.includes('health') ||
      lowerIntent.includes('sleep') ||
      lowerIntent.includes('energy') ||
      lowerIntent.includes('stress') ||
      lowerIntent.includes('nutrition') ||
      lowerIntent.includes('habits') ||
      lowerIntent.includes('recovery')) {
    return 'HealthEngine';
  }

  // Finance
  if (lowerDomain === 'finance' ||
      lowerIntent.includes('finance') ||
      lowerIntent.includes('budget') ||
      lowerIntent.includes('cashflow') ||
      lowerIntent.includes('financial goal')) {
    return 'FinanceEngine';
  }

  // Knowledge
  if (lowerDomain === 'knowledge' ||
      lowerIntent.includes('knowledge') ||
      lowerIntent.includes('topics') ||
      lowerIntent.includes('learning content') ||
      lowerIntent.includes('information structure')) {
    return 'KnowledgeEngine';
  }

  // Emotion / Social Intelligence
  if (lowerDomain === 'emotion' ||
      lowerDomain === 'social intelligence' ||
      lowerIntent.includes('emotion') ||
      lowerIntent.includes('tone') ||
      lowerIntent.includes('social dynamic') ||
      lowerIntent.includes('relationship')) {
    return 'EmotionEngine';
  }

  // Productivity
  if (lowerDomain === 'productivity' ||
      lowerIntent.includes('productivity') ||
      lowerIntent.includes('time management') ||
      lowerIntent.includes('focus') ||
      lowerIntent.includes('task')) {
    return 'ProductivityEngine';
  }

  // ============================================================
  // TRANSVERSAL ENGINES
  // ============================================================
  
  if (lowerIntent.includes('memory')) return 'MemoryManager';
  if (lowerIntent.includes('replay')) return 'ReplayEngine';
  if (lowerIntent.includes('fabric')) return 'HyperFabric';
  if (lowerIntent.includes('depth') || lowerIntent.includes('lens')) return 'DepthLensSystem';
  if (lowerIntent.includes('map') || lowerIntent.includes('cartograph')) return 'CartographyEngine';
  if (lowerIntent.includes('project') || lowerIntent.includes('view')) return 'ProjectionEngine';

  return 'GeneralHandler';
}

============================================================
F.4 — CONTEXT INTERPRETER UPDATE
============================================================

--- FILE: /che-nu-sdk/core/context_interpreter.ts
--- ACTION: ADD TO classifyDomain() function
--- PRIORITY: F.4

/**
 * Classify domain from input
 * Updated with all operational modules
 */
function classifyDomain(input: string): { domain: string; isModule: boolean } {
  const lowerInput = input.toLowerCase();

  // ============================================================
  // SPHERES
  // ============================================================
  
  if (lowerInput.includes('personal') || lowerInput.includes('home') || lowerInput.includes('family')) {
    return { domain: 'Personal', isModule: false };
  }
  if (lowerInput.includes('business') || lowerInput.includes('enterprise') || lowerInput.includes('company')) {
    return { domain: 'Business', isModule: false };
  }
  if (lowerInput.includes('creative') || lowerInput.includes('art') || lowerInput.includes('design')) {
    return { domain: 'Creative', isModule: false };
  }
  if (lowerInput.includes('scholar') || lowerInput.includes('research') || lowerInput.includes('academic')) {
    return { domain: 'Scholar', isModule: false };
  }
  if (lowerInput.includes('social') && !lowerInput.includes('intelligence')) {
    return { domain: 'Social', isModule: false };
  }
  if (lowerInput.includes('community') || lowerInput.includes('group') || lowerInput.includes('collective')) {
    return { domain: 'Community', isModule: false };
  }
  if (lowerInput.includes('xr') || lowerInput.includes('virtual') || lowerInput.includes('immersive')) {
    return { domain: 'XR', isModule: false };
  }
  if (lowerInput.includes('team') || lowerInput.includes('agent') || lowerInput.includes('myteam')) {
    return { domain: 'MyTeam', isModule: false };
  }

  // ============================================================
  // SUPER-MODULES (NOT Spheres)
  // ============================================================
  
  if (lowerInput.includes('methodology') || lowerInput.includes('workflow') || lowerInput.includes('decompose')) {
    return { domain: 'Methodology', isModule: true };
  }

  if (lowerInput.includes('skill') || lowerInput.includes('competency') || lowerInput.includes('learning path')) {
    return { domain: 'Skill', isModule: true };
  }

  // ============================================================
  // OPERATIONAL MODULES (NOT Spheres)
  // ============================================================
  
  // Health
  if (lowerInput.includes('health') || lowerInput.includes('sleep') || lowerInput.includes('energy') ||
      lowerInput.includes('stress') || lowerInput.includes('nutrition') || lowerInput.includes('habits') ||
      lowerInput.includes('recovery') || lowerInput.includes('physical') || lowerInput.includes('mental')) {
    return { domain: 'Health', isModule: true };
  }

  // Finance
  if (lowerInput.includes('finance') || lowerInput.includes('budget') || lowerInput.includes('cashflow') ||
      lowerInput.includes('financial') || lowerInput.includes('money') || lowerInput.includes('savings')) {
    return { domain: 'Finance', isModule: true };
  }

  // Knowledge
  if (lowerInput.includes('knowledge') || lowerInput.includes('topics') || lowerInput.includes('learning content') ||
      lowerInput.includes('information structure') || lowerInput.includes('graph')) {
    return { domain: 'Knowledge', isModule: true };
  }

  // Emotion / Social Intelligence
  if (lowerInput.includes('emotion') || lowerInput.includes('tone') || lowerInput.includes('social intelligence') ||
      lowerInput.includes('relationship') || lowerInput.includes('empathy')) {
    return { domain: 'Emotion', isModule: true };
  }

  // Productivity
  if (lowerInput.includes('productivity') || lowerInput.includes('time management') || lowerInput.includes('focus') ||
      lowerInput.includes('task') || lowerInput.includes('planning')) {
    return { domain: 'Productivity', isModule: true };
  }

  return { domain: 'General', isModule: false };
}

############################################################
#                                                          #
#              PHASE G: FRONTEND PAGES                     #
#                                                          #
############################################################

============================================================
G.1 — HEALTH PAGE
============================================================

--- FILE: /che-nu-frontend/pages/health.tsx
--- ACTION: CREATE NEW FILE
--- PRIORITY: G.1

import React, { useState } from 'react';
import Layout from '../components/Layout';
import HealthViewer from '../components/HealthViewer';
import { runCheNu } from '../services/chenu.service';

type ViewMode = 'overview' | 'sleep' | 'energy' | 'mental' | 'habits' | 'stress';

export default function HealthPage() {
  const [viewMode, setViewMode] = useState<ViewMode>('overview');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (mode: ViewMode) => {
    setLoading(true);
    setViewMode(mode);
    try {
      const queries: Record<ViewMode, string> = {
        overview: 'evaluate overall health',
        sleep: 'analyze sleep patterns',
        energy: 'analyze energy levels',
        mental: 'analyze mental state',
        habits: 'analyze habits',
        stress: 'analyze stress levels',
      };
      const res = await runCheNu(queries[mode]);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="health-page">
        <header>
          <h1>Personal Health Dashboard</h1>
          <span className="badge">Operational Module</span>
          <p>Representational health structures. NO medical advice.</p>
        </header>

        <nav className="mode-nav">
          <button className={viewMode === 'overview' ? 'active' : ''} onClick={() => handleAnalyze('overview')}>Overview</button>
          <button className={viewMode === 'sleep' ? 'active' : ''} onClick={() => handleAnalyze('sleep')}>Sleep</button>
          <button className={viewMode === 'energy' ? 'active' : ''} onClick={() => handleAnalyze('energy')}>Energy</button>
          <button className={viewMode === 'mental' ? 'active' : ''} onClick={() => handleAnalyze('mental')}>Mental</button>
          <button className={viewMode === 'habits' ? 'active' : ''} onClick={() => handleAnalyze('habits')}>Habits</button>
          <button className={viewMode === 'stress' ? 'active' : ''} onClick={() => handleAnalyze('stress')}>Stress</button>
        </nav>

        <main>
          {loading ? <p>Loading...</p> : <HealthViewer viewMode={viewMode} result={result} />}
        </main>

        <footer>
          <p>HealthEngine v1.0.0 — Operational Module — SAFE Compliant — NO Medical Advice</p>
        </footer>
      </div>
    </Layout>
  );
}

============================================================
G.2 — HEALTH VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/HealthViewer.tsx
--- ACTION: CREATE NEW FILE
--- PRIORITY: G.2

import React from 'react';

interface Props {
  viewMode: string;
  result: any;
}

export default function HealthViewer({ viewMode, result }: Props) {
  const renderScoreCard = (title: string, score: number, status: string) => (
    <div className="score-card">
      <h4>{title}</h4>
      <div className="score">{score}</div>
      <div className="status">{status}</div>
    </div>
  );

  if (!result) {
    return <p className="placeholder">Select an analysis type to view health insights.</p>;
  }

  return (
    <div className="health-viewer">
      {viewMode === 'overview' && (
        <div className="overview-grid">
          {renderScoreCard('Overall', result.overallScore || 50, 'Representational')}
          {renderScoreCard('Physical', result.physical?.score || 50, result.physical?.strength || 'moderate')}
          {renderScoreCard('Mental', result.mental?.score || 50, result.mental?.clarity || 'moderate')}
          {renderScoreCard('Sleep', result.sleep?.score || 50, result.sleep?.quality || 'fair')}
          {renderScoreCard('Energy', result.energy?.score || 50, result.energy?.current || 'moderate')}
          {renderScoreCard('Stress', result.stress?.score || 50, result.stress?.level || 'moderate')}
        </div>
      )}

      {viewMode === 'sleep' && (
        <div className="detail-view">
          <h3>Sleep Analysis</h3>
          <p>Duration: {result.sleep?.duration || 'adequate'}</p>
          <p>Quality: {result.sleep?.quality || 'fair'}</p>
          <p>Cycles: {result.sleep?.cycles || 4}</p>
        </div>
      )}

      {viewMode === 'energy' && (
        <div className="detail-view">
          <h3>Energy Analysis</h3>
          <p>Current: {result.energy?.current || 'moderate'}</p>
          <p>Trend: {result.energy?.trend || 'stable'}</p>
        </div>
      )}

      {viewMode === 'mental' && (
        <div className="detail-view">
          <h3>Mental Analysis</h3>
          <p>Cognitive Load: {result.mental?.cognitiveLoad || 'moderate'}</p>
          <p>Clarity: {result.mental?.clarity || 'moderate'}</p>
          <p>Focus Index: {result.mental?.focusIndex || 50}</p>
        </div>
      )}

      {viewMode === 'habits' && (
        <div className="detail-view">
          <h3>Habits Analysis</h3>
          <p>Positive Habits: {result.habits?.positive?.length || 0}</p>
          <p>Areas for Review: {result.habits?.negative?.length || 0}</p>
        </div>
      )}

      {viewMode === 'stress' && (
        <div className="detail-view">
          <h3>Stress Analysis</h3>
          <p>Level: {result.stress?.level || 'moderate'}</p>
          <p>Stressors: {result.stress?.stressors?.join(', ') || 'general'}</p>
        </div>
      )}

      <style jsx>{`
        .health-viewer { color: #E9E4D6; }
        .overview-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
        .score-card { background: #2F4C39; border-radius: 8px; padding: 1.5rem; text-align: center; }
        .score-card h4 { color: #D8B26A; margin-bottom: 0.5rem; }
        .score { font-size: 2.5rem; font-weight: bold; color: #3EB4A2; }
        .status { color: #8D8371; text-transform: capitalize; }
        .detail-view { background: #2F4C39; border-radius: 8px; padding: 2rem; }
        .detail-view h3 { color: #D8B26A; margin-bottom: 1rem; }
        .placeholder { color: #8D8371; font-style: italic; }
      `}</style>
    </div>
  );
}

============================================================
G.3-G.10 — OTHER FRONTEND PAGES (COMPACT)
============================================================

--- FILE: /che-nu-frontend/pages/finance.tsx

import React, { useState } from 'react';
import Layout from '../components/Layout';
import FinanceViewer from '../components/FinanceViewer';
import { runCheNu } from '../services/chenu.service';

export default function FinancePage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (type: string) => {
    setLoading(true);
    const res = await runCheNu(`analyze ${type}`);
    setResult(res);
    setLoading(false);
  };

  return (
    <Layout>
      <div className="finance-page">
        <header>
          <h1>Finance Dashboard</h1>
          <span className="badge">Operational Module - NO Financial Advice</span>
        </header>
        <nav>
          <button onClick={() => handleAnalyze('budget structure')}>Budget</button>
          <button onClick={() => handleAnalyze('cashflow')}>Cashflow</button>
          <button onClick={() => handleAnalyze('financial goals')}>Goals</button>
          <button onClick={() => handleAnalyze('risk profile')}>Risk Profile</button>
        </nav>
        <main>{loading ? <p>Loading...</p> : <FinanceViewer result={result} />}</main>
      </div>
    </Layout>
  );
}

--- FILE: /che-nu-frontend/components/FinanceViewer.tsx

import React from 'react';

export default function FinanceViewer({ result }: { result: any }) {
  if (!result) return <p>Select analysis type to view finance structure.</p>;
  return (
    <div className="finance-viewer">
      <h3>Finance Structure</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

--- FILE: /che-nu-frontend/pages/knowledge.tsx

import React, { useState } from 'react';
import Layout from '../components/Layout';
import KnowledgeViewer from '../components/KnowledgeViewer';
import { runCheNu } from '../services/chenu.service';

export default function KnowledgePage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (type: string) => {
    setLoading(true);
    const res = await runCheNu(`${type}`);
    setResult(res);
    setLoading(false);
  };

  return (
    <Layout>
      <div className="knowledge-page">
        <header>
          <h1>Knowledge Map</h1>
          <span className="badge">Operational Module</span>
        </header>
        <nav>
          <button onClick={() => handleAnalyze('build knowledge graph')}>Build Graph</button>
          <button onClick={() => handleAnalyze('classify topics')}>Classify</button>
          <button onClick={() => handleAnalyze('suggest index structure')}>Index</button>
          <button onClick={() => handleAnalyze('create retrieval plan')}>Retrieval</button>
        </nav>
        <main>{loading ? <p>Loading...</p> : <KnowledgeViewer result={result} />}</main>
      </div>
    </Layout>
  );
}

--- FILE: /che-nu-frontend/components/KnowledgeViewer.tsx

import React from 'react';

export default function KnowledgeViewer({ result }: { result: any }) {
  if (!result) return <p>Select analysis type to view knowledge structure.</p>;
  return (
    <div className="knowledge-viewer">
      <h3>Knowledge Structure</h3>
      {result.nodes && <p>Nodes: {result.nodes.length}</p>}
      {result.edges && <p>Edges: {result.edges.length}</p>}
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

--- FILE: /che-nu-frontend/pages/emotion.tsx

import React, { useState } from 'react';
import Layout from '../components/Layout';
import EmotionViewer from '../components/EmotionViewer';
import { runCheNu } from '../services/chenu.service';

export default function EmotionPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (type: string) => {
    setLoading(true);
    const res = await runCheNu(`analyze ${type}`);
    setResult(res);
    setLoading(false);
  };

  return (
    <Layout>
      <div className="emotion-page">
        <header>
          <h1>Emotion & Social Intelligence</h1>
          <span className="badge">Operational Module - NO Diagnosis</span>
        </header>
        <nav>
          <button onClick={() => handleAnalyze('emotional tone')}>Tone</button>
          <button onClick={() => handleAnalyze('relationships')}>Relationships</button>
          <button onClick={() => handleAnalyze('social context')}>Social Map</button>
        </nav>
        <main>{loading ? <p>Loading...</p> : <EmotionViewer result={result} />}</main>
      </div>
    </Layout>
  );
}

--- FILE: /che-nu-frontend/components/EmotionViewer.tsx

import React from 'react';

export default function EmotionViewer({ result }: { result: any }) {
  if (!result) return <p>Select analysis type to view emotion/social structure.</p>;
  return (
    <div className="emotion-viewer">
      <h3>Emotion / Social Structure</h3>
      {result.category && <p>Tone: {result.category}</p>}
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

--- FILE: /che-nu-frontend/pages/productivity.tsx

import React, { useState } from 'react';
import Layout from '../components/Layout';
import ProductivityViewer from '../components/ProductivityViewer';
import { runCheNu } from '../services/chenu.service';

export default function ProductivityPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (type: string) => {
    setLoading(true);
    const res = await runCheNu(`${type}`);
    setResult(res);
    setLoading(false);
  };

  return (
    <Layout>
      <div className="productivity-page">
        <header>
          <h1>Productivity Dashboard</h1>
          <span className="badge">Operational Module</span>
        </header>
        <nav>
          <button onClick={() => handleAnalyze('build task map')}>Task Map</button>
          <button onClick={() => handleAnalyze('plan time blocks')}>Time Blocks</button>
          <button onClick={() => handleAnalyze('outline priorities')}>Priorities</button>
          <button onClick={() => handleAnalyze('focus session')}>Focus</button>
        </nav>
        <main>{loading ? <p>Loading...</p> : <ProductivityViewer result={result} />}</main>
      </div>
    </Layout>
  );
}

--- FILE: /che-nu-frontend/components/ProductivityViewer.tsx

import React from 'react';

export default function ProductivityViewer({ result }: { result: any }) {
  if (!result) return <p>Select analysis type to view productivity structure.</p>;
  return (
    <div className="productivity-viewer">
      <h3>Productivity Structure</h3>
      {result.tasks && <p>Tasks: {result.tasks.length}</p>}
      {result.blocks && <p>Time Blocks: {result.blocks.length}</p>}
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

============================================================
G.11 — WORKFLOW GRID UPDATE
============================================================

--- FILE: /che-nu-frontend/components/WorkflowGrid.tsx
--- ACTION: ADD BUTTONS

// ADD these buttons to the existing WorkflowGrid:

<button className="workflow-btn" onClick={() => navigateTo('/health')}>
  <span className="icon">❤️</span>
  <span className="label">Health Tools</span>
  <span className="badge operational">Operational</span>
</button>

<button className="workflow-btn" onClick={() => navigateTo('/finance')}>
  <span className="icon">💰</span>
  <span className="label">Finance Tools</span>
  <span className="badge operational">Operational</span>
</button>

<button className="workflow-btn" onClick={() => navigateTo('/knowledge')}>
  <span className="icon">📚</span>
  <span className="label">Knowledge Tools</span>
  <span className="badge operational">Operational</span>
</button>

<button className="workflow-btn" onClick={() => navigateTo('/emotion')}>
  <span className="icon">🧠</span>
  <span className="label">Emotion / Social IQ</span>
  <span className="badge operational">Operational</span>
</button>

<button className="workflow-btn" onClick={() => navigateTo('/productivity')}>
  <span className="icon">⚡</span>
  <span className="label">Productivity Tools</span>
  <span className="badge operational">Operational</span>
</button>

############################################################
#                                                          #
#              PHASE H: DOCUMENTATION                      #
#                                                          #
############################################################

============================================================
H.1 — UI FLOW UPDATE
============================================================

--- FILE: /che-nu-app/docs/UI_FLOW.md
--- ACTION: ADD SECTION

## Operational Module Workflows

These are OPERATIONAL MODULES - NOT Spheres.

### Health Tools
- Evaluate Overall Health
- Analyze Sleep
- Analyze Energy
- Analyze Mental Load
- Analyze Habits
- Analyze Stress

### Finance Tools
- Finance Overview
- Budget Skeleton
- Cashflow Map
- Goal Mapping
- Risk Profile

### Knowledge Tools
- Build Knowledge Graph
- Classify Topics
- Design Index
- Retrieval Plan

### Emotion / Social IQ
- Analyze Emotional Tone
- Map Relationships
- Social Context Overview

### Productivity Tools
- Task Map
- Time Block Plan
- Focus Layout
- Execution Overview

### Mermaid Diagram

```mermaid
flowchart TD
    subgraph OperationalModules[Operational Modules - NOT Spheres]
        Health[HealthEngine]
        Finance[FinanceEngine]
        Knowledge[KnowledgeEngine]
        Emotion[EmotionEngine]
        Productivity[ProductivityEngine]
    end

    Orchestrator --> OperationalModules
    Health --> HealthView
    Finance --> FinanceView
    Knowledge --> KnowledgeView
    Emotion --> EmotionView
    Productivity --> ProductivityView
```

============================================================
H.2 — COMPLETE DIAGRAMS UPDATE
============================================================

--- FILE: /che-nu-sdk/docs/DIAGRAMS.md
--- ACTION: ADD SECTION

## Complete CHE·NU Architecture Diagram

```mermaid
flowchart TB
    CHE_NU[CHE·NU System v3.0]
    
    CHE_NU --> Spheres
    CHE_NU --> SuperModules
    CHE_NU --> OperationalModules
    CHE_NU --> TransversalEngines

    subgraph Spheres[Spheres - 8 Domains of Life]
        S1[Personal]
        S2[Business]
        S3[Creative]
        S4[Scholar]
        S5[Social]
        S6[Community]
        S7[XR]
        S8[MyTeam]
    end

    subgraph SuperModules[Super-Modules]
        SM1[MethodologyEngine]
        SM2[SkillEngine]
    end

    subgraph OperationalModules[Operational Modules]
        OM1[HealthEngine]
        OM2[FinanceEngine]
        OM3[KnowledgeEngine]
        OM4[EmotionEngine]
        OM5[ProductivityEngine]
    end

    subgraph TransversalEngines[Transversal Engines]
        TE1[MemoryManager]
        TE2[ReplayEngine]
        TE3[HyperFabric]
        TE4[DepthLensSystem]
        TE5[CartographyEngine]
        TE6[ProjectionEngine]
    end

    style Spheres fill:#2F4C39,stroke:#3F7249
    style SuperModules fill:#7A593A,stroke:#D8B26A
    style OperationalModules fill:#3EB4A2,stroke:#D8B26A
    style TransversalEngines fill:#1E1F22,stroke:#8D8371
```

## Operational Modules Sub-Engines

```mermaid
flowchart LR
    subgraph HealthSuite[Health Engine Suite]
        H[HealthEngine]
        H --> H1[Physical]
        H --> H2[Mental]
        H --> H3[Sleep]
        H --> H4[Stress]
        H --> H5[Energy]
        H --> H6[Nutrition]
        H --> H7[Habits]
        H --> H8[Recovery]
    end

    subgraph FinanceSuite[Finance Engine Suite]
        F[FinanceEngine]
        F --> F1[Budget]
        F --> F2[Cashflow]
        F --> F3[Goals]
        F --> F4[RiskProfile]
        F --> F5[Planning]
    end

    subgraph KnowledgeSuite[Knowledge Engine Suite]
        K[KnowledgeEngine]
        K --> K1[Graph]
        K --> K2[Classify]
        K --> K3[Indexing]
        K --> K4[Retrieval]
        K --> K5[Mapping]
    end

    subgraph EmotionSuite[Emotion Engine Suite]
        E[EmotionEngine]
        E --> E1[Tone]
        E --> E2[SelfRegulation]
        E --> E3[Empathy]
        E --> E4[Relationship]
        E --> E5[SocialMap]
    end

    subgraph ProductivitySuite[Productivity Engine Suite]
        P[ProductivityEngine]
        P --> P1[Time]
        P --> P2[Focus]
        P --> P3[Planning]
        P --> P4[Execution]
        P --> P5[ContextSwitch]
    end
```

############################################################
#                                                          #
#              END OF MEGA PACK                            #
#                                                          #
############################################################

============================================================
CONSOLIDATION SUMMARY
============================================================

TOTAL FILES CREATED/UPDATED:

PHASE A: Health Engine Suite
- 1 main engine + 8 sub-engines + 1 index + 1 schema = 11 files

PHASE B: Finance Engine Suite
- 1 main engine + 5 sub-engines + 1 index + 1 schema = 8 files

PHASE C: Knowledge Engine Suite
- 1 main engine + 5 sub-engines + 1 index + 1 schema = 8 files

PHASE D: Emotion Engine Suite
- 1 main engine + 5 sub-engines + 1 index + 1 schema = 8 files

PHASE E: Productivity Engine Suite
- 1 main engine + 5 sub-engines + 1 index + 1 schema = 8 files

PHASE F: System Updates
- system_index.json + orchestrator.ts + context_interpreter.ts = 3 files

PHASE G: Frontend
- 5 pages + 5 viewers + WorkflowGrid update = 11 files

PHASE H: Documentation
- UI_FLOW.md + DIAGRAMS.md = 2 files

TOTAL: ~59 new/updated files

============================================================
STATISTICS
============================================================

| Category | Count |
|----------|-------|
| Spheres | 8 |
| Super-Modules | 2 |
| Operational Modules | 5 |
| Sub-Engines | 28 |
| Schemas | 9 |
| Frontend Pages | 5 |
| Frontend Components | 5 |
| Transversal Engines | 6 |

============================================================
END OF MEGA ENGINE PACK
============================================================
