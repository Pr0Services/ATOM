/**
 * CHE·NU™ TOOLS REGISTRY
 * 
 * TOOLS = HOW a skill is executed (concrete, technical, versioned)
 * SKILLS = WHAT an agent can do (abstract, declarative, reusable)
 * 
 * All tools must be:
 * - versioned
 * - permission-scoped
 * - budget-aware
 * - auditable
 */

// ═══════════════════════════════════════════════════════════════
// CORE TOOLS
// ═══════════════════════════════════════════════════════════════

const TOOLS_REGISTRY = {
  TextEditorEngine: {
    id: 'tool-text-editor',
    name: 'TextEditorEngine',
    version: '1.0.0',
    category: 'content',
    description: 'Text creation, editing, and formatting engine',
    supports_skills: [
      'CreateDocument',
      'EditDocument',
      'StructureDocument',
      'SummarizeContent',
      'RewriteTone',
      'GenerateMarkdown',
      'PrepareMeeting',
      'TakeMeetingNotes',
      'GenerateMinutes',
      'ExtractSources',
      'CiteReferences',
      'CreativeBrainstorm'
    ],
    permissions_required: ['text_processing'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 30,
    audit_level: 'standard'
  },
  
  TableEngine: {
    id: 'tool-table-engine',
    name: 'TableEngine',
    version: '1.0.0',
    category: 'data',
    description: 'Structured data table manipulation',
    supports_skills: [
      'CreateTable',
      'EditTable',
      'AnalyzeTable',
      'ConvertCSV',
      'CleanData',
      'OptionComparison'
    ],
    permissions_required: ['data_processing'],
    budget_cost: 'low',
    concurrency_limit: 5,
    timeout_seconds: 60,
    audit_level: 'standard'
  },
  
  SpreadsheetEngine: {
    id: 'tool-spreadsheet',
    name: 'SpreadsheetEngine',
    version: '1.0.0',
    category: 'data',
    description: 'Excel/CSV file generation and manipulation',
    supports_skills: ['GenerateSpreadsheet'],
    permissions_required: ['file_export', 'data_processing'],
    budget_cost: 'low',
    concurrency_limit: 5,
    timeout_seconds: 45,
    audit_level: 'standard'
  },
  
  FileConverter: {
    id: 'tool-file-converter',
    name: 'FileConverter',
    version: '1.0.0',
    category: 'conversion',
    description: 'File format conversion utilities',
    supports_skills: ['ConvertCSV'],
    permissions_required: ['file_read', 'file_write'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 30,
    audit_level: 'standard'
  },
  
  PDFGenerator: {
    id: 'tool-pdf-gen',
    name: 'PDFGenerator',
    version: '1.0.0',
    category: 'export',
    description: 'PDF document generation from content',
    supports_skills: ['GeneratePDF'],
    permissions_required: ['file_export'],
    budget_cost: 'low',
    concurrency_limit: 5,
    timeout_seconds: 45,
    audit_level: 'standard'
  },
  
  DOCXGenerator: {
    id: 'tool-docx-gen',
    name: 'DOCXGenerator',
    version: '1.0.0',
    category: 'export',
    description: 'DOCX document generation from content',
    supports_skills: ['GenerateDOCX'],
    permissions_required: ['file_export'],
    budget_cost: 'low',
    concurrency_limit: 5,
    timeout_seconds: 45,
    audit_level: 'standard'
  },
  
  MarkdownGenerator: {
    id: 'tool-markdown-gen',
    name: 'MarkdownGenerator',
    version: '1.0.0',
    category: 'export',
    description: 'Markdown format generation',
    supports_skills: ['GenerateMarkdown'],
    permissions_required: ['file_export'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 15,
    audit_level: 'minimal'
  },
  
  BrowserEngine: {
    id: 'tool-browser',
    name: 'BrowserEngine',
    version: '1.0.0',
    category: 'web',
    description: 'Web browsing and content extraction',
    supports_skills: [
      'BrowseWeb',
      'ExtractSources',
      'VerifyInformation'
    ],
    permissions_required: ['web_access'],
    budget_cost: 'medium',
    concurrency_limit: 3,
    timeout_seconds: 90,
    audit_level: 'high'
  },
  
  MediaGenerator: {
    id: 'tool-media-gen',
    name: 'MediaGenerator',
    version: '1.0.0',
    category: 'creative',
    description: 'AI-powered media generation (images, video, audio)',
    supports_skills: [
      'GenerateImage',
      'GenerateVideoDraft',
      'GenerateMusicDraft'
    ],
    permissions_required: ['media_generation'],
    budget_cost: 'high',
    concurrency_limit: 2,
    timeout_seconds: 180,
    audit_level: 'high'
  },
  
  ThreadEngine: {
    id: 'tool-thread',
    name: 'ThreadEngine',
    version: '1.0.0',
    category: 'knowledge',
    description: 'Thread artifact (.chenu) management',
    supports_skills: [
      'CreateThread',
      'LinkThreads',
      'SummarizeThread',
      'ExtractDecisions',
      'DetectInconsistencies',
      'ClassifyContent'
    ],
    permissions_required: ['thread_access'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 30,
    audit_level: 'high'
  },
  
  AnalysisEngine: {
    id: 'tool-analysis',
    name: 'AnalysisEngine',
    version: '1.0.0',
    category: 'intelligence',
    description: 'Advanced reasoning and analysis capabilities',
    supports_skills: [
      'AnalyzeTable',
      'ExtractDecisions',
      'DetectInconsistencies',
      'SituationAnalysis',
      'OptionComparison',
      'RiskAnalysis',
      'DecisionSupport',
      'ExtractActionItems',
      'VerifyInformation'
    ],
    permissions_required: ['advanced_reasoning'],
    budget_cost: 'high',
    concurrency_limit: 3,
    timeout_seconds: 120,
    audit_level: 'high'
  },
  
  SimulationEngine: {
    id: 'tool-simulation',
    name: 'SimulationEngine',
    version: '1.0.0',
    category: 'intelligence',
    description: 'Scenario modeling and prediction',
    supports_skills: ['ScenarioSimulation'],
    permissions_required: ['advanced_reasoning', 'simulation'],
    budget_cost: 'very_high',
    concurrency_limit: 1,
    timeout_seconds: 300,
    audit_level: 'high'
  },
  
  MeetingEngine: {
    id: 'tool-meeting',
    name: 'MeetingEngine',
    version: '1.0.0',
    category: 'collaboration',
    description: 'Meeting preparation, note-taking, and minutes generation',
    supports_skills: [
      'PrepareMeeting',
      'TakeMeetingNotes',
      'GenerateMinutes',
      'ExtractActionItems'
    ],
    permissions_required: ['meeting_access'],
    budget_cost: 'medium',
    concurrency_limit: 5,
    timeout_seconds: 60,
    audit_level: 'high'
  },
  
  ChartEngine: {
    id: 'tool-chart',
    name: 'ChartEngine',
    version: '1.0.0',
    category: 'visualization',
    description: 'Chart and graph generation',
    supports_skills: ['VisualizeData'],
    permissions_required: ['visualization'],
    budget_cost: 'medium',
    concurrency_limit: 5,
    timeout_seconds: 45,
    audit_level: 'standard'
  },
  
  VisualizationEngine: {
    id: 'tool-viz',
    name: 'VisualizationEngine',
    version: '1.0.0',
    category: 'visualization',
    description: 'Advanced data visualization',
    supports_skills: ['VisualizeData'],
    permissions_required: ['visualization', 'data_processing'],
    budget_cost: 'medium',
    concurrency_limit: 3,
    timeout_seconds: 90,
    audit_level: 'standard'
  },
  
  DataValidator: {
    id: 'tool-data-validator',
    name: 'DataValidator',
    version: '1.0.0',
    category: 'data',
    description: 'Data quality validation and cleaning',
    supports_skills: ['CleanData'],
    permissions_required: ['data_processing'],
    budget_cost: 'medium',
    concurrency_limit: 5,
    timeout_seconds: 60,
    audit_level: 'standard'
  },
  
  ClassificationEngine: {
    id: 'tool-classify',
    name: 'ClassificationEngine',
    version: '1.0.0',
    category: 'intelligence',
    description: 'Content categorization and tagging',
    supports_skills: ['ClassifyContent'],
    permissions_required: ['classification'],
    budget_cost: 'medium',
    concurrency_limit: 10,
    timeout_seconds: 30,
    audit_level: 'standard'
  },
  
  CitationEngine: {
    id: 'tool-citation',
    name: 'CitationEngine',
    version: '1.0.0',
    category: 'research',
    description: 'Academic citation and bibliography formatting',
    supports_skills: ['CiteReferences'],
    permissions_required: ['text_processing'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 15,
    audit_level: 'minimal'
  },
  
  VideoEngine: {
    id: 'tool-video',
    name: 'VideoEngine',
    version: '1.0.0',
    category: 'creative',
    description: 'Video concept and storyboard creation',
    supports_skills: ['GenerateVideoDraft'],
    permissions_required: ['media_generation', 'video_processing'],
    budget_cost: 'very_high',
    concurrency_limit: 1,
    timeout_seconds: 300,
    audit_level: 'high'
  },
  
  AudioEngine: {
    id: 'tool-audio',
    name: 'AudioEngine',
    version: '1.0.0',
    category: 'creative',
    description: 'Audio and music generation',
    supports_skills: ['GenerateMusicDraft'],
    permissions_required: ['media_generation', 'audio_processing'],
    budget_cost: 'high',
    concurrency_limit: 2,
    timeout_seconds: 180,
    audit_level: 'high'
  },
  
  TemplateEngine: {
    id: 'tool-template',
    name: 'TemplateEngine',
    version: '1.0.0',
    category: 'content',
    description: 'Template management and application',
    supports_skills: ['CreateDocument'],
    permissions_required: ['template_access'],
    budget_cost: 'low',
    concurrency_limit: 10,
    timeout_seconds: 15,
    audit_level: 'minimal'
  },
  
  XRSceneGenerator: {
    id: 'tool-xr-scene',
    name: 'XRSceneGenerator',
    version: '1.0.0',
    category: 'extended',
    description: 'XR/VR scene generation (extension)',
    supports_skills: [], // Extended skills not in core catalog
    permissions_required: ['xr_access', 'media_generation'],
    budget_cost: 'very_high',
    concurrency_limit: 1,
    timeout_seconds: 300,
    audit_level: 'high'
  }
};

// ═══════════════════════════════════════════════════════════════
// TOOL STATUS TRACKING
// ═══════════════════════════════════════════════════════════════

const TOOL_STATUS = {
  // Production-ready tools
  AVAILABLE: 'available',
  
  // Temporarily unavailable
  MAINTENANCE: 'maintenance',
  
  // Experimental/testing
  BETA: 'beta',
  
  // Deprecated
  DEPRECATED: 'deprecated'
};

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  TOOLS_REGISTRY,
  TOOL_STATUS,
  
  // Helper functions
  getToolById: (toolId) => {
    return TOOLS_REGISTRY[Object.keys(TOOLS_REGISTRY).find(key => 
      TOOLS_REGISTRY[key].id === toolId
    )];
  },
  
  getToolsByCategory: (category) => {
    return Object.values(TOOLS_REGISTRY).filter(tool => tool.category === category);
  },
  
  getToolsForSkill: (skillName) => {
    return Object.values(TOOLS_REGISTRY).filter(tool => 
      tool.supports_skills.includes(skillName)
    );
  },
  
  canToolExecute: (toolName, permissions) => {
    const tool = TOOLS_REGISTRY[toolName];
    if (!tool) return false;
    
    // Check if user has all required permissions
    return tool.permissions_required.every(perm => permissions.includes(perm));
  },
  
  estimateToolCost: (toolName) => {
    const tool = TOOLS_REGISTRY[toolName];
    if (!tool) return 0;
    
    const costs = {
      'low': 10,
      'medium': 50,
      'high': 200,
      'very_high': 500
    };
    
    return costs[tool.budget_cost] || 0;
  }
};
