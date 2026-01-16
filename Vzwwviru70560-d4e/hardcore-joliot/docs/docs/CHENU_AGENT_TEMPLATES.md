============================================================
SECTION 3 — PRE-CONFIGURED AGENT TEMPLATES
============================================================

--- FILE: /che-nu-sdk/core/agent_templates.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Agent Templates
 * =============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Pre-configured agent profile templates.
 * These are DECLARATIVE ONLY - no behavior.
 * 
 * @module AgentTemplates
 * @version 1.0.0
 */

import { 
  AgentProfileEngine, 
  AgentProfile, 
  DomainSphere,
  AgentRole,
  CapabilityLevel 
} from './agent_profile';

// ============================================================
// TEMPLATE FACTORY
// ============================================================

const profileEngine = new AgentProfileEngine();

function createTemplate(config: {
  name: string;
  role: AgentRole;
  description: string;
  domainSpheres: DomainSphere[];
  tags: string[];
  engines: Array<{
    name: string;
    level: CapabilityLevel;
    focus: string[];
    subEngines?: string[];
    isPrimary?: boolean;
  }>;
  limitations: string[];
  useCases: string[];
  collaboratesWith: string[];
}): AgentProfile {
  let profile = profileEngine.createProfile({
    name: config.name,
    role: config.role,
    description: config.description,
    domainSpheres: config.domainSpheres,
    tags: config.tags,
  });

  profile = profileEngine.attachEngines(profile, config.engines);
  profile = profileEngine.setLimitations(profile, config.limitations);
  profile = profileEngine.setUseCases(profile, config.useCases);
  profile = profileEngine.setCollaborations(profile, config.collaboratesWith);

  return profile;
}

// ============================================================
// CORE AGENT TEMPLATES
// ============================================================

/**
 * RESEARCH AGENT
 * Specializes in information gathering, synthesis, and knowledge management
 */
export const ResearchAgent = createTemplate({
  name: 'Research Agent',
  role: 'researcher',
  description: 'Expert in information discovery, source analysis, and knowledge synthesis. Helps users find, validate, and organize information efficiently.',
  domainSpheres: ['Scholar', 'Business', 'Personal'],
  tags: ['research', 'knowledge', 'information', 'synthesis', 'analysis'],
  engines: [
    { name: 'KnowledgeEngine', level: 'expert', focus: ['synthesis', 'search', 'organization', 'mapping'], isPrimary: true },
    { name: 'ResearchEngine', level: 'expert', focus: ['discovery', 'sources', 'validation', 'citation'], subEngines: ['SourceEngine', 'SynthesisEngine', 'CitationEngine'], isPrimary: true },
    { name: 'MethodologyEngine', level: 'high', focus: ['research-methods', 'analysis-frameworks'], isPrimary: true },
    { name: 'AnalysisEngine', level: 'high', focus: ['data-analysis', 'pattern-recognition'], isPrimary: false },
    { name: 'DocumentFormatEngine', level: 'medium', focus: ['export', 'formatting'], isPrimary: false },
  ],
  limitations: [
    'Does not execute autonomous research tasks',
    'Cannot access external databases directly',
    'Provides frameworks, not real-time data',
    'User must validate all findings',
  ],
  useCases: [
    'Academic research planning',
    'Market research frameworks',
    'Literature review structuring',
    'Source validation workflows',
    'Knowledge base organization',
  ],
  collaboratesWith: ['Knowledge Map Agent', 'Content Creator Agent', 'Strategy Agent'],
});

/**
 * XR SCENE ARCHITECT
 * Specializes in immersive experiences, 3D spaces, and XR design
 */
export const XRSceneArchitect = createTemplate({
  name: 'XR Scene Architect',
  role: 'architect',
  description: 'Expert in designing immersive XR experiences, 3D environments, and spatial interfaces. Creates blueprints for virtual spaces and interactions.',
  domainSpheres: ['XR', 'Creative', 'Business'],
  tags: ['xr', '3d', 'immersive', 'spatial', 'vr', 'ar', 'metaverse'],
  engines: [
    { name: 'XRSceneEngine', level: 'expert', focus: ['scene-composition', 'spatial-design', 'interaction-patterns'], subEngines: ['EnvironmentEngine', 'AvatarEngine', 'InteractionEngine', 'LightingEngine', 'PhysicsEngine'], isPrimary: true },
    { name: 'CreativityEngine', level: 'high', focus: ['ideation', 'visual-design', 'iteration'], isPrimary: true },
    { name: 'MethodologyEngine', level: 'medium', focus: ['design-thinking', 'prototyping'], isPrimary: false },
    { name: 'ProductivityEngine', level: 'medium', focus: ['workflow', 'project-planning'], isPrimary: false },
    { name: 'CollaborationEngine', level: 'medium', focus: ['team-coordination', 'review-cycles'], isPrimary: false },
  ],
  limitations: [
    'Does not generate real 3D assets',
    'Cannot render actual XR experiences',
    'Provides design blueprints only',
    'Requires external tools for implementation',
  ],
  useCases: [
    'Virtual showroom design',
    'Immersive training environments',
    'XR meeting spaces',
    'Interactive product visualizations',
    'Spatial UI/UX design',
  ],
  collaboratesWith: ['Creative Director Agent', 'Project Manager Agent', 'Technical Lead Agent'],
});

/**
 * PRODUCTIVITY COACH
 * Specializes in personal efficiency, time management, and workflow optimization
 */
export const ProductivityCoach = createTemplate({
  name: 'Productivity Coach',
  role: 'coach',
  description: 'Expert in personal productivity, time management, and workflow optimization. Helps users achieve more with less stress through structured approaches.',
  domainSpheres: ['Personal', 'Business', 'MyTeam'],
  tags: ['productivity', 'time-management', 'efficiency', 'habits', 'workflow'],
  engines: [
    { name: 'ProductivityEngine', level: 'expert', focus: ['workflow', 'time-management', 'focus', 'habits'], subEngines: ['TimeBlockEngine', 'FocusEngine', 'HabitEngine', 'EnergyEngine'], isPrimary: true },
    { name: 'GoalEngine', level: 'high', focus: ['goal-setting', 'tracking', 'milestones'], isPrimary: true },
    { name: 'TaskEngine', level: 'high', focus: ['prioritization', 'scheduling', 'delegation'], subEngines: ['PriorityEngine', 'DeadlineEngine', 'DelegationEngine'], isPrimary: true },
    { name: 'SchedulingEngine', level: 'high', focus: ['calendar', 'time-blocking', 'availability'], isPrimary: true },
    { name: 'MethodologyEngine', level: 'medium', focus: ['GTD', 'pomodoro', 'time-boxing'], isPrimary: false },
    { name: 'ReflectionEngine', level: 'medium', focus: ['weekly-reviews', 'retrospectives'], isPrimary: false },
  ],
  limitations: [
    'Does not manage actual calendar',
    'Cannot automate tasks',
    'Provides frameworks and structures only',
    'User must implement recommendations',
  ],
  useCases: [
    'Daily planning routines',
    'Weekly review structures',
    'Goal tracking frameworks',
    'Focus session design',
    'Habit formation plans',
  ],
  collaboratesWith: ['Health Overview Agent', 'Goal Setting Agent', 'Project Manager Agent'],
});

/**
 * FINANCE OVERVIEW AGENT
 * Specializes in financial planning, analysis, and investment frameworks
 */
export const FinanceOverviewAgent = createTemplate({
  name: 'Finance Overview Agent',
  role: 'analyst',
  description: 'Expert in financial planning, budgeting, and investment analysis. Provides frameworks for financial decision-making and wealth management.',
  domainSpheres: ['Personal', 'Business'],
  tags: ['finance', 'budget', 'investment', 'planning', 'analysis'],
  engines: [
    { name: 'FinanceEngine', level: 'expert', focus: ['budgeting', 'investment', 'planning', 'analysis'], subEngines: ['BudgetEngine', 'InvestmentEngine', 'TaxEngine', 'RetirementEngine', 'DebtEngine'], isPrimary: true },
    { name: 'AnalysisEngine', level: 'high', focus: ['financial-analysis', 'risk-assessment', 'forecasting'], isPrimary: true },
    { name: 'StrategyEngine', level: 'high', focus: ['financial-strategy', 'portfolio-planning'], isPrimary: true },
    { name: 'GoalEngine', level: 'medium', focus: ['financial-goals', 'milestones'], isPrimary: false },
    { name: 'KnowledgeEngine', level: 'medium', focus: ['financial-education', 'market-understanding'], isPrimary: false },
    { name: 'DecisionEngine', level: 'medium', focus: ['investment-decisions', 'risk-analysis'], isPrimary: false },
  ],
  limitations: [
    'Does not provide financial advice',
    'Cannot execute transactions',
    'Frameworks only - not real recommendations',
    'User should consult licensed professionals',
  ],
  useCases: [
    'Budget planning frameworks',
    'Investment analysis structures',
    'Retirement planning templates',
    'Financial goal tracking',
    'Risk assessment frameworks',
  ],
  collaboratesWith: ['Strategy Agent', 'Goal Setting Agent', 'Analysis Agent'],
});

/**
 * HEALTH OVERVIEW AGENT
 * Specializes in wellness, fitness, and health management frameworks
 */
export const HealthOverviewAgent = createTemplate({
  name: 'Health Overview Agent',
  role: 'coach',
  description: 'Expert in holistic health management, fitness planning, and wellness optimization. Provides frameworks for physical and mental well-being.',
  domainSpheres: ['Personal'],
  tags: ['health', 'fitness', 'wellness', 'nutrition', 'mental-health'],
  engines: [
    { name: 'HealthEngine', level: 'expert', focus: ['fitness', 'nutrition', 'sleep', 'wellness'], subEngines: ['FitnessEngine', 'NutritionEngine', 'SleepEngine', 'WellnessEngine', 'VitalEngine'], isPrimary: true },
    { name: 'EmotionEngine', level: 'high', focus: ['emotional-wellness', 'stress-management', 'mindfulness'], isPrimary: true },
    { name: 'GoalEngine', level: 'medium', focus: ['health-goals', 'milestones'], isPrimary: false },
    { name: 'HabitEngine', level: 'medium', focus: ['healthy-habits', 'behavior-change'], isPrimary: false },
    { name: 'SchedulingEngine', level: 'low', focus: ['workout-scheduling', 'meal-planning'], isPrimary: false },
    { name: 'ReflectionEngine', level: 'low', focus: ['health-journaling', 'progress-reflection'], isPrimary: false },
  ],
  limitations: [
    'Does not provide medical advice',
    'Cannot diagnose conditions',
    'Frameworks only - consult healthcare providers',
    'Does not replace professional care',
  ],
  useCases: [
    'Fitness planning frameworks',
    'Nutrition tracking structures',
    'Sleep optimization plans',
    'Stress management strategies',
    'Wellness routine design',
  ],
  collaboratesWith: ['Productivity Coach', 'Goal Setting Agent', 'Reflection Agent'],
});

/**
 * KNOWLEDGE MAP AGENT
 * Specializes in knowledge organization, learning paths, and skill development
 */
export const KnowledgeMapAgent = createTemplate({
  name: 'Knowledge Map Agent',
  role: 'curator',
  description: 'Expert in organizing knowledge, creating learning paths, and mapping skills. Helps users structure their learning journey and connect concepts.',
  domainSpheres: ['Scholar', 'Personal', 'Business'],
  tags: ['knowledge', 'learning', 'skills', 'education', 'mapping'],
  engines: [
    { name: 'KnowledgeEngine', level: 'expert', focus: ['mapping', 'organization', 'connections', 'taxonomy'], subEngines: ['TaxonomyEngine', 'ConnectionEngine', 'VisualizationEngine'], isPrimary: true },
    { name: 'SkillEngine', level: 'expert', focus: ['skill-mapping', 'gap-analysis', 'learning-paths'], subEngines: ['TaxonomyEngine', 'GapAnalysisEngine', 'RoadmapEngine', 'AssessmentEngine'], isPrimary: true },
    { name: 'LearningEngine', level: 'high', focus: ['learning-design', 'curriculum', 'assessment'], isPrimary: true },
    { name: 'MethodologyEngine', level: 'medium', focus: ['learning-methodologies', 'spaced-repetition'], isPrimary: false },
    { name: 'GoalEngine', level: 'medium', focus: ['learning-goals', 'skill-targets'], isPrimary: false },
  ],
  limitations: [
    'Does not teach content directly',
    'Cannot assess real skill levels',
    'Provides frameworks and maps only',
    'User must pursue actual learning',
  ],
  useCases: [
    'Skill gap analysis',
    'Learning path design',
    'Knowledge base organization',
    'Competency mapping',
    'Career development planning',
  ],
  collaboratesWith: ['Research Agent', 'Productivity Coach', 'Strategy Agent'],
});

/**
 * PROJECT MANAGER AGENT
 * Specializes in project planning, team coordination, and delivery management
 */
export const ProjectManagerAgent = createTemplate({
  name: 'Project Manager Agent',
  role: 'coordinator',
  description: 'Expert in project planning, resource management, and team coordination. Provides frameworks for successful project delivery.',
  domainSpheres: ['Business', 'Projets', 'MyTeam'],
  tags: ['project', 'management', 'planning', 'coordination', 'delivery'],
  engines: [
    { name: 'ProjectEngine', level: 'expert', focus: ['planning', 'tracking', 'resources', 'milestones'], subEngines: ['PlanningEngine', 'TrackingEngine', 'ResourceEngine', 'RiskEngine'], isPrimary: true },
    { name: 'TaskEngine', level: 'expert', focus: ['task-breakdown', 'assignment', 'dependencies'], isPrimary: true },
    { name: 'CollaborationEngine', level: 'high', focus: ['team-coordination', 'communication', 'meetings'], subEngines: ['TeamEngine', 'MeetingEngine', 'StatusEngine'], isPrimary: true },
    { name: 'SchedulingEngine', level: 'high', focus: ['timeline', 'deadlines', 'resource-allocation'], isPrimary: true },
    { name: 'StrategyEngine', level: 'medium', focus: ['project-strategy', 'risk-management'], isPrimary: false },
    { name: 'CommunicationEngine', level: 'medium', focus: ['stakeholder-updates', 'reporting'], isPrimary: false },
  ],
  limitations: [
    'Does not manage real projects',
    'Cannot assign real tasks',
    'Provides frameworks and templates only',
    'Requires project management tools',
  ],
  useCases: [
    'Project kickoff planning',
    'Sprint planning structures',
    'Risk assessment frameworks',
    'Status reporting templates',
    'Team coordination workflows',
  ],
  collaboratesWith: ['Productivity Coach', 'Strategy Agent', 'Technical Lead Agent'],
});

/**
 * CREATIVE DIRECTOR AGENT
 * Specializes in creative processes, content strategy, and design thinking
 */
export const CreativeDirectorAgent = createTemplate({
  name: 'Creative Director Agent',
  role: 'creator',
  description: 'Expert in creative processes, ideation, and content strategy. Guides users through creative projects from concept to execution.',
  domainSpheres: ['Creative', 'Business', 'Personal'],
  tags: ['creative', 'design', 'content', 'ideation', 'branding'],
  engines: [
    { name: 'CreativityEngine', level: 'expert', focus: ['ideation', 'brainstorming', 'iteration', 'evaluation'], subEngines: ['IdeationEngine', 'BrainstormEngine', 'IterationEngine', 'EvaluationEngine'], isPrimary: true },
    { name: 'ContentEngine', level: 'expert', focus: ['content-strategy', 'storytelling', 'brand-voice'], subEngines: ['StoryEngine', 'BrandEngine', 'MediaEngine', 'EditorialEngine'], isPrimary: true },
    { name: 'MethodologyEngine', level: 'high', focus: ['design-thinking', 'creative-frameworks'], isPrimary: true },
    { name: 'ProjectEngine', level: 'medium', focus: ['creative-project-planning'], isPrimary: false },
    { name: 'CollaborationEngine', level: 'medium', focus: ['creative-team-coordination', 'reviews'], isPrimary: false },
    { name: 'DocumentFormatEngine', level: 'medium', focus: ['presentation', 'portfolio'], isPrimary: false },
  ],
  limitations: [
    'Does not create actual content',
    'Cannot design graphics',
    'Provides creative frameworks only',
    'User must execute creative work',
  ],
  useCases: [
    'Brand identity development',
    'Content calendar planning',
    'Creative brief structuring',
    'Design review frameworks',
    'Storytelling strategies',
  ],
  collaboratesWith: ['XR Scene Architect', 'Strategy Agent', 'Content Creator Agent'],
});

/**
 * STRATEGY AGENT
 * Specializes in strategic planning, analysis, and decision-making
 */
export const StrategyAgent = createTemplate({
  name: 'Strategy Agent',
  role: 'analyst',
  description: 'Expert in strategic thinking, business analysis, and long-term planning. Helps users develop comprehensive strategies and make informed decisions.',
  domainSpheres: ['Business', 'Personal', 'Projets'],
  tags: ['strategy', 'planning', 'analysis', 'decision-making', 'vision'],
  engines: [
    { name: 'StrategyEngine', level: 'expert', focus: ['vision', 'analysis', 'positioning', 'roadmap', 'execution'], subEngines: ['VisionEngine', 'AnalysisEngine', 'PositioningEngine', 'RoadmapEngine', 'ExecutionEngine'], isPrimary: true },
    { name: 'AnalysisEngine', level: 'expert', focus: ['SWOT', 'competitive-analysis', 'market-analysis'], isPrimary: true },
    { name: 'DecisionEngine', level: 'high', focus: ['decision-frameworks', 'risk-assessment', 'trade-offs'], isPrimary: true },
    { name: 'GoalEngine', level: 'high', focus: ['strategic-goals', 'OKRs', 'KPIs'], isPrimary: true },
    { name: 'KnowledgeEngine', level: 'medium', focus: ['market-intelligence', 'competitive-insights'], isPrimary: false },
  ],
  limitations: [
    'Does not execute strategies',
    'Cannot predict market outcomes',
    'Provides frameworks only',
    'Decisions remain with user',
  ],
  useCases: [
    'Business strategy development',
    'Market entry planning',
    'Competitive positioning',
    'Strategic roadmapping',
    'Decision analysis frameworks',
  ],
  collaboratesWith: ['Finance Overview Agent', 'Project Manager Agent', 'Research Agent'],
});

/**
 * COMMUNICATION SPECIALIST AGENT
 * Specializes in communication, messaging, and stakeholder engagement
 */
export const CommunicationSpecialistAgent = createTemplate({
  name: 'Communication Specialist Agent',
  role: 'specialist',
  description: 'Expert in communication strategy, messaging, and stakeholder engagement. Helps craft effective communications across channels and audiences.',
  domainSpheres: ['Business', 'Personal', 'Community'],
  tags: ['communication', 'messaging', 'stakeholder', 'presentation', 'negotiation'],
  engines: [
    { name: 'CommunicationEngine', level: 'expert', focus: ['messaging', 'channels', 'audience-analysis', 'presentation'], subEngines: ['MessagingEngine', 'ChannelEngine', 'PresentationEngine', 'NegotiationEngine'], isPrimary: true },
    { name: 'RelationshipEngine', level: 'high', focus: ['stakeholder-mapping', 'relationship-building'], isPrimary: true },
    { name: 'ContentEngine', level: 'high', focus: ['content-creation', 'copywriting', 'tone'], isPrimary: true },
    { name: 'DocumentFormatEngine', level: 'medium', focus: ['document-formatting', 'presentations'], isPrimary: false },
    { name: 'AnalysisEngine', level: 'medium', focus: ['audience-analysis', 'feedback-analysis'], isPrimary: false },
  ],
  limitations: [
    'Does not send actual communications',
    'Cannot manage real relationships',
    'Provides frameworks and templates only',
    'User executes communications',
  ],
  useCases: [
    'Stakeholder communication plans',
    'Presentation structuring',
    'Email campaign frameworks',
    'Crisis communication templates',
    'Meeting facilitation guides',
  ],
  collaboratesWith: ['Project Manager Agent', 'Strategy Agent', 'Creative Director Agent'],
});

/**
 * DATA ANALYST AGENT
 * Specializes in data analysis, visualization, and insights
 */
export const DataAnalystAgent = createTemplate({
  name: 'Data Analyst Agent',
  role: 'analyst',
  description: 'Expert in data analysis, visualization, and deriving insights. Helps users understand data and make data-driven decisions.',
  domainSpheres: ['Business', 'Scholar', 'Personal'],
  tags: ['data', 'analysis', 'visualization', 'insights', 'metrics'],
  engines: [
    { name: 'AnalysisEngine', level: 'expert', focus: ['data-analysis', 'pattern-recognition', 'synthesis'], subEngines: ['DataEngine', 'PatternEngine', 'SynthesisEngine'], isPrimary: true },
    { name: 'DataEngine', level: 'expert', focus: ['data-processing', 'transformation', 'quality'], subEngines: ['ProcessingEngine', 'TransformEngine', 'QualityEngine', 'VisualizationEngine'], isPrimary: true },
    { name: 'KnowledgeEngine', level: 'high', focus: ['domain-knowledge', 'context'], isPrimary: false },
    { name: 'DocumentFormatEngine', level: 'medium', focus: ['reports', 'dashboards'], isPrimary: false },
    { name: 'MethodologyEngine', level: 'medium', focus: ['statistical-methods', 'analysis-frameworks'], isPrimary: false },
  ],
  limitations: [
    'Does not process real data',
    'Cannot access databases',
    'Provides analysis frameworks only',
    'Requires data tools for execution',
  ],
  useCases: [
    'Data analysis planning',
    'Dashboard design frameworks',
    'KPI definition structures',
    'Report templates',
    'Data quality frameworks',
  ],
  collaboratesWith: ['Strategy Agent', 'Finance Overview Agent', 'Research Agent'],
});

/**
 * WELLBEING MENTOR AGENT
 * Specializes in emotional wellness, relationships, and personal growth
 */
export const WellbeingMentorAgent = createTemplate({
  name: 'Wellbeing Mentor Agent',
  role: 'mentor',
  description: 'Expert in emotional wellness, relationship health, and personal growth. Provides frameworks for holistic well-being and self-improvement.',
  domainSpheres: ['Personal', 'Social'],
  tags: ['wellbeing', 'emotional', 'relationships', 'growth', 'mindfulness'],
  engines: [
    { name: 'EmotionEngine', level: 'expert', focus: ['emotional-awareness', 'regulation', 'resilience'], subEngines: ['AwarenessEngine', 'RegulationEngine', 'ResilienceEngine'], isPrimary: true },
    { name: 'RelationshipEngine', level: 'high', focus: ['relationship-health', 'boundaries', 'communication'], isPrimary: true },
    { name: 'ReflectionEngine', level: 'high', focus: ['journaling', 'gratitude', 'growth-planning'], isPrimary: true },
    { name: 'GoalEngine', level: 'medium', focus: ['personal-goals', 'growth-milestones'], isPrimary: false },
    { name: 'HealthEngine', level: 'medium', focus: ['mental-wellness', 'stress-management'], isPrimary: false },
  ],
  limitations: [
    'Does not provide therapy',
    'Cannot diagnose mental health conditions',
    'Provides frameworks only - not treatment',
    'Professional help recommended for serious concerns',
  ],
  useCases: [
    'Self-reflection frameworks',
    'Relationship assessment structures',
    'Stress management plans',
    'Personal growth roadmaps',
    'Gratitude practice designs',
  ],
  collaboratesWith: ['Health Overview Agent', 'Productivity Coach', 'Reflection Agent'],
});

// ============================================================
// ALL TEMPLATES EXPORT
// ============================================================

export const AgentTemplates = {
  ResearchAgent,
  XRSceneArchitect,
  ProductivityCoach,
  FinanceOverviewAgent,
  HealthOverviewAgent,
  KnowledgeMapAgent,
  ProjectManagerAgent,
  CreativeDirectorAgent,
  StrategyAgent,
  CommunicationSpecialistAgent,
  DataAnalystAgent,
  WellbeingMentorAgent,
};

/**
 * Get all templates as array
 */
export function getAllTemplates(): AgentProfile[] {
  return Object.values(AgentTemplates);
}

/**
 * Get template by name
 */
export function getTemplateByName(name: string): AgentProfile | null {
  return Object.values(AgentTemplates).find(t => t.name === name) || null;
}

/**
 * Get templates for a specific sphere
 */
export function getTemplatesForSphere(sphere: DomainSphere): AgentProfile[] {
  return Object.values(AgentTemplates).filter(t => t.domainSpheres.includes(sphere));
}

/**
 * Get templates that use a specific engine
 */
export function getTemplatesUsingEngine(engineName: string): AgentProfile[] {
  return Object.values(AgentTemplates).filter(t => 
    t.capabilities.some(c => c.engine === engineName)
  );
}

export default AgentTemplates;
