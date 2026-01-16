/**
 * CHE·NU™ CANONICAL SKILLS CATALOG
 * 
 * SKILLS = WHAT an agent can do (abstract, declarative, reusable)
 * TOOLS = HOW a skill is executed (concrete, technical, versioned)
 * 
 * A SKILL may use multiple TOOLS.
 * A TOOL may support multiple SKILLS.
 * 
 * These skills are GLOBAL.
 * Their availability is FILTERED by sphere and permissions.
 * Spheres NEVER redefine skills - they only allow, restrict, or preset them.
 */

// ═══════════════════════════════════════════════════════════════
// DOCUMENT & CONTENT SKILLS
// ═══════════════════════════════════════════════════════════════

const DOCUMENT_SKILLS = {
  CreateDocument: {
    id: 'skill-doc-create',
    name: 'CreateDocument',
    category: 'document',
    description: 'Create a new document from scratch or template',
    input_types: ['text', 'template', 'outline'],
    output_types: ['document'],
    required_tools: ['TextEditorEngine'],
    optional_tools: ['TemplateEngine'],
    permissions_required: ['create_content'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  EditDocument: {
    id: 'skill-doc-edit',
    name: 'EditDocument',
    category: 'document',
    description: 'Modify existing document content',
    input_types: ['document', 'edits'],
    output_types: ['document'],
    required_tools: ['TextEditorEngine'],
    permissions_required: ['edit_content'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  StructureDocument: {
    id: 'skill-doc-structure',
    name: 'StructureDocument',
    category: 'document',
    description: 'Organize document with headings, sections, formatting',
    input_types: ['document', 'structure_rules'],
    output_types: ['document'],
    required_tools: ['TextEditorEngine'],
    permissions_required: ['edit_content'],
    budget_estimate: 'low',
    agent_levels: ['L1', 'L2']
  },
  
  SummarizeContent: {
    id: 'skill-doc-summarize',
    name: 'SummarizeContent',
    category: 'document',
    description: 'Generate concise summary of content',
    input_types: ['document', 'text'],
    output_types: ['summary'],
    required_tools: ['TextEditorEngine'],
    permissions_required: ['read_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  RewriteTone: {
    id: 'skill-doc-rewrite',
    name: 'RewriteTone',
    category: 'document',
    description: 'Rewrite content with different tone/style',
    input_types: ['document', 'tone_parameters'],
    output_types: ['document'],
    required_tools: ['TextEditorEngine'],
    permissions_required: ['edit_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  GeneratePDF: {
    id: 'skill-doc-pdf',
    name: 'GeneratePDF',
    category: 'document',
    description: 'Convert content to PDF format',
    input_types: ['document', 'html'],
    output_types: ['pdf'],
    required_tools: ['PDFGenerator'],
    permissions_required: ['create_content', 'export'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  GenerateDOCX: {
    id: 'skill-doc-docx',
    name: 'GenerateDOCX',
    category: 'document',
    description: 'Convert content to DOCX format',
    input_types: ['document', 'html'],
    output_types: ['docx'],
    required_tools: ['DOCXGenerator'],
    permissions_required: ['create_content', 'export'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  GenerateMarkdown: {
    id: 'skill-doc-markdown',
    name: 'GenerateMarkdown',
    category: 'document',
    description: 'Convert content to Markdown format',
    input_types: ['document', 'html'],
    output_types: ['markdown'],
    required_tools: ['MarkdownGenerator'],
    permissions_required: ['create_content', 'export'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// TABLE & DATA SKILLS
// ═══════════════════════════════════════════════════════════════

const TABLE_SKILLS = {
  CreateTable: {
    id: 'skill-table-create',
    name: 'CreateTable',
    category: 'table',
    description: 'Create structured data table',
    input_types: ['data', 'schema'],
    output_types: ['table'],
    required_tools: ['TableEngine'],
    permissions_required: ['create_data'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  EditTable: {
    id: 'skill-table-edit',
    name: 'EditTable',
    category: 'table',
    description: 'Modify table data or structure',
    input_types: ['table', 'edits'],
    output_types: ['table'],
    required_tools: ['TableEngine'],
    permissions_required: ['edit_data'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  AnalyzeTable: {
    id: 'skill-table-analyze',
    name: 'AnalyzeTable',
    category: 'table',
    description: 'Extract insights from table data',
    input_types: ['table'],
    output_types: ['analysis', 'insights'],
    required_tools: ['TableEngine', 'AnalysisEngine'],
    permissions_required: ['read_data', 'analyze'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  GenerateSpreadsheet: {
    id: 'skill-table-spreadsheet',
    name: 'GenerateSpreadsheet',
    category: 'table',
    description: 'Create formatted spreadsheet file',
    input_types: ['table', 'data'],
    output_types: ['xlsx', 'csv'],
    required_tools: ['SpreadsheetEngine'],
    permissions_required: ['create_data', 'export'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  ConvertCSV: {
    id: 'skill-table-csv',
    name: 'ConvertCSV',
    category: 'table',
    description: 'Convert data to/from CSV format',
    input_types: ['table', 'csv'],
    output_types: ['table', 'csv'],
    required_tools: ['FileConverter'],
    permissions_required: ['read_data', 'create_data'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  CleanData: {
    id: 'skill-table-clean',
    name: 'CleanData',
    category: 'table',
    description: 'Remove duplicates, fix formatting, validate data',
    input_types: ['table', 'data'],
    output_types: ['table', 'data'],
    required_tools: ['TableEngine', 'DataValidator'],
    permissions_required: ['edit_data'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  VisualizeData: {
    id: 'skill-table-visualize',
    name: 'VisualizeData',
    category: 'table',
    description: 'Create charts and graphs from data',
    input_types: ['table', 'data'],
    output_types: ['chart', 'graph', 'image'],
    required_tools: ['ChartEngine', 'VisualizationEngine'],
    permissions_required: ['read_data', 'create_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// THREAD & KNOWLEDGE SKILLS
// ═══════════════════════════════════════════════════════════════

const THREAD_SKILLS = {
  CreateThread: {
    id: 'skill-thread-create',
    name: 'CreateThread',
    category: 'thread',
    description: 'Create new .chenu thread artifact',
    input_types: ['intent', 'context'],
    output_types: ['thread'],
    required_tools: ['ThreadEngine'],
    permissions_required: ['create_thread'],
    budget_estimate: 'low',
    agent_levels: ['L0', 'L1', 'L2']
  },
  
  LinkThreads: {
    id: 'skill-thread-link',
    name: 'LinkThreads',
    category: 'thread',
    description: 'Create relationships between threads',
    input_types: ['thread_ids', 'link_type'],
    output_types: ['thread_links'],
    required_tools: ['ThreadEngine'],
    permissions_required: ['edit_thread'],
    budget_estimate: 'low',
    agent_levels: ['L1', 'L2']
  },
  
  SummarizeThread: {
    id: 'skill-thread-summarize',
    name: 'SummarizeThread',
    category: 'thread',
    description: 'Generate thread summary and key points',
    input_types: ['thread'],
    output_types: ['summary'],
    required_tools: ['ThreadEngine', 'TextEditorEngine'],
    permissions_required: ['read_thread'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  ExtractDecisions: {
    id: 'skill-thread-decisions',
    name: 'ExtractDecisions',
    category: 'thread',
    description: 'Identify decisions made in thread',
    input_types: ['thread'],
    output_types: ['decisions'],
    required_tools: ['ThreadEngine', 'AnalysisEngine'],
    permissions_required: ['read_thread'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  DetectInconsistencies: {
    id: 'skill-thread-inconsistencies',
    name: 'DetectInconsistencies',
    category: 'thread',
    description: 'Find conflicting information in thread',
    input_types: ['thread'],
    output_types: ['inconsistencies'],
    required_tools: ['ThreadEngine', 'AnalysisEngine'],
    permissions_required: ['read_thread'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  ClassifyContent: {
    id: 'skill-thread-classify',
    name: 'ClassifyContent',
    category: 'thread',
    description: 'Categorize thread content by type/topic',
    input_types: ['thread', 'content'],
    output_types: ['classification'],
    required_tools: ['ThreadEngine', 'ClassificationEngine'],
    permissions_required: ['read_thread'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// ANALYSIS & STRATEGY SKILLS
// ═══════════════════════════════════════════════════════════════

const ANALYSIS_SKILLS = {
  SituationAnalysis: {
    id: 'skill-analysis-situation',
    name: 'SituationAnalysis',
    category: 'analysis',
    description: 'Analyze current situation and context',
    input_types: ['context', 'data'],
    output_types: ['analysis'],
    required_tools: ['AnalysisEngine'],
    permissions_required: ['read_data', 'analyze'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  OptionComparison: {
    id: 'skill-analysis-options',
    name: 'OptionComparison',
    category: 'analysis',
    description: 'Compare multiple options with pros/cons',
    input_types: ['options', 'criteria'],
    output_types: ['comparison'],
    required_tools: ['AnalysisEngine', 'TableEngine'],
    permissions_required: ['analyze'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  RiskAnalysis: {
    id: 'skill-analysis-risk',
    name: 'RiskAnalysis',
    category: 'analysis',
    description: 'Identify and evaluate risks',
    input_types: ['context', 'options'],
    output_types: ['risk_assessment'],
    required_tools: ['AnalysisEngine'],
    permissions_required: ['analyze'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  DecisionSupport: {
    id: 'skill-analysis-decision',
    name: 'DecisionSupport',
    category: 'analysis',
    description: 'Provide decision-making framework and recommendations',
    input_types: ['context', 'options', 'criteria'],
    output_types: ['recommendations'],
    required_tools: ['AnalysisEngine'],
    permissions_required: ['analyze'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  ScenarioSimulation: {
    id: 'skill-analysis-scenario',
    name: 'ScenarioSimulation',
    category: 'analysis',
    description: 'Model potential outcomes of different scenarios',
    input_types: ['scenarios', 'parameters'],
    output_types: ['simulation_results'],
    required_tools: ['AnalysisEngine', 'SimulationEngine'],
    permissions_required: ['analyze'],
    budget_estimate: 'very_high',
    agent_levels: ['L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// MEETING SKILLS
// ═══════════════════════════════════════════════════════════════

const MEETING_SKILLS = {
  PrepareMeeting: {
    id: 'skill-meeting-prepare',
    name: 'PrepareMeeting',
    category: 'meeting',
    description: 'Generate agenda and preparation materials',
    input_types: ['meeting_info', 'context'],
    output_types: ['agenda', 'materials'],
    required_tools: ['TextEditorEngine', 'MeetingEngine'],
    permissions_required: ['read_meeting', 'create_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  TakeMeetingNotes: {
    id: 'skill-meeting-notes',
    name: 'TakeMeetingNotes',
    category: 'meeting',
    description: 'Capture meeting discussion in real-time',
    input_types: ['meeting_transcript', 'audio'],
    output_types: ['notes'],
    required_tools: ['TextEditorEngine', 'MeetingEngine'],
    permissions_required: ['create_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  GenerateMinutes: {
    id: 'skill-meeting-minutes',
    name: 'GenerateMinutes',
    category: 'meeting',
    description: 'Create formal meeting minutes document',
    input_types: ['meeting_notes', 'meeting_info'],
    output_types: ['minutes'],
    required_tools: ['TextEditorEngine', 'MeetingEngine'],
    permissions_required: ['create_content'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  ExtractActionItems: {
    id: 'skill-meeting-actions',
    name: 'ExtractActionItems',
    category: 'meeting',
    description: 'Identify and list action items from meeting',
    input_types: ['meeting_notes', 'minutes'],
    output_types: ['action_items'],
    required_tools: ['MeetingEngine', 'AnalysisEngine'],
    permissions_required: ['read_meeting'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// WEB & RESEARCH SKILLS
// ═══════════════════════════════════════════════════════════════

const WEB_SKILLS = {
  BrowseWeb: {
    id: 'skill-web-browse',
    name: 'BrowseWeb',
    category: 'web',
    description: 'Search and retrieve information from web',
    input_types: ['query', 'url'],
    output_types: ['content'],
    required_tools: ['BrowserEngine'],
    permissions_required: ['web_access'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  ExtractSources: {
    id: 'skill-web-sources',
    name: 'ExtractSources',
    category: 'web',
    description: 'Collect and organize web sources',
    input_types: ['urls', 'content'],
    output_types: ['sources'],
    required_tools: ['BrowserEngine', 'TextEditorEngine'],
    permissions_required: ['web_access'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  },
  
  VerifyInformation: {
    id: 'skill-web-verify',
    name: 'VerifyInformation',
    category: 'web',
    description: 'Cross-check information across sources',
    input_types: ['claims', 'sources'],
    output_types: ['verification'],
    required_tools: ['BrowserEngine', 'AnalysisEngine'],
    permissions_required: ['web_access', 'analyze'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  CiteReferences: {
    id: 'skill-web-cite',
    name: 'CiteReferences',
    category: 'web',
    description: 'Generate proper citations and bibliography',
    input_types: ['sources'],
    output_types: ['citations', 'bibliography'],
    required_tools: ['TextEditorEngine', 'CitationEngine'],
    permissions_required: ['create_content'],
    budget_estimate: 'low',
    agent_levels: ['L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// CREATIVE SKILLS
// ═══════════════════════════════════════════════════════════════

const CREATIVE_SKILLS = {
  GenerateImage: {
    id: 'skill-creative-image',
    name: 'GenerateImage',
    category: 'creative',
    description: 'Create images from descriptions',
    input_types: ['prompt', 'parameters'],
    output_types: ['image'],
    required_tools: ['MediaGenerator'],
    permissions_required: ['create_media'],
    budget_estimate: 'high',
    agent_levels: ['L1', 'L2']
  },
  
  GenerateVideoDraft: {
    id: 'skill-creative-video',
    name: 'GenerateVideoDraft',
    category: 'creative',
    description: 'Create video concept or storyboard',
    input_types: ['concept', 'parameters'],
    output_types: ['storyboard', 'video_draft'],
    required_tools: ['MediaGenerator', 'VideoEngine'],
    permissions_required: ['create_media'],
    budget_estimate: 'very_high',
    agent_levels: ['L2']
  },
  
  GenerateMusicDraft: {
    id: 'skill-creative-music',
    name: 'GenerateMusicDraft',
    category: 'creative',
    description: 'Create music concepts or samples',
    input_types: ['style', 'parameters'],
    output_types: ['music_draft'],
    required_tools: ['MediaGenerator', 'AudioEngine'],
    permissions_required: ['create_media'],
    budget_estimate: 'high',
    agent_levels: ['L2']
  },
  
  CreativeBrainstorm: {
    id: 'skill-creative-brainstorm',
    name: 'CreativeBrainstorm',
    category: 'creative',
    description: 'Generate creative ideas and concepts',
    input_types: ['topic', 'constraints'],
    output_types: ['ideas'],
    required_tools: ['TextEditorEngine'],
    permissions_required: ['analyze'],
    budget_estimate: 'medium',
    agent_levels: ['L1', 'L2']
  }
};

// ═══════════════════════════════════════════════════════════════
// MASTER CATALOG
// ═══════════════════════════════════════════════════════════════

const SKILLS_CATALOG = {
  ...DOCUMENT_SKILLS,
  ...TABLE_SKILLS,
  ...THREAD_SKILLS,
  ...ANALYSIS_SKILLS,
  ...MEETING_SKILLS,
  ...WEB_SKILLS,
  ...CREATIVE_SKILLS
};

// ═══════════════════════════════════════════════════════════════
// SPHERE COMPATIBILITY MATRIX
// ═══════════════════════════════════════════════════════════════

const SPHERE_SKILL_RULES = {
  personal: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'SummarizeContent',
      'CreateTable', 'GenerateSpreadsheet',
      'CreateThread', 'SummarizeThread',
      'BrowseWeb'
    ],
    optional: [
      'GeneratePDF', 'GenerateDOCX', 'GenerateMarkdown',
      'AnalyzeTable', 'VisualizeData',
      'PrepareMeeting', 'GenerateMinutes',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    restricted: [
      'GenerateVideoDraft', 'GenerateMusicDraft'
    ]
  },
  
  business: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'StructureDocument', 'SummarizeContent',
      'CreateTable', 'EditTable', 'AnalyzeTable', 'GenerateSpreadsheet',
      'CreateThread', 'LinkThreads', 'SummarizeThread', 'ExtractDecisions',
      'PrepareMeeting', 'TakeMeetingNotes', 'GenerateMinutes', 'ExtractActionItems',
      'BrowseWeb', 'ExtractSources'
    ],
    optional: [
      'GeneratePDF', 'GenerateDOCX',
      'ConvertCSV', 'CleanData', 'VisualizeData',
      'SituationAnalysis', 'OptionComparison', 'RiskAnalysis', 'DecisionSupport',
      'VerifyInformation', 'CiteReferences',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    restricted: []
  },
  
  government: {
    enabled_by_default: [
      'CreateDocument', 'StructureDocument',
      'GeneratePDF', 'GenerateDOCX',
      'CreateThread', 'SummarizeThread',
      'BrowseWeb'
    ],
    optional: [
      'EditDocument', 'SummarizeContent',
      'CreateTable', 'AnalyzeTable',
      'ExtractSources', 'CiteReferences'
    ],
    restricted: [
      'GenerateSpreadsheet', // May require compliance review
      'VisualizeData',
      'GenerateImage', 'GenerateVideoDraft', 'GenerateMusicDraft'
    ]
  },
  
  creative: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'RewriteTone',
      'CreateThread',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    optional: [
      'GeneratePDF', 'GenerateDOCX', 'GenerateMarkdown',
      'SummarizeContent', 'StructureDocument',
      'GenerateVideoDraft', 'GenerateMusicDraft',
      'BrowseWeb', 'ExtractSources'
    ],
    restricted: []
  },
  
  community: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'SummarizeContent',
      'CreateThread', 'SummarizeThread',
      'BrowseWeb'
    ],
    optional: [
      'GeneratePDF', 'GenerateDOCX',
      'PrepareMeeting', 'GenerateMinutes',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    restricted: []
  },
  
  social: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'RewriteTone',
      'SummarizeContent',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    optional: [
      'GenerateVideoDraft',
      'BrowseWeb', 'ExtractSources'
    ],
    restricted: []
  },
  
  entertainment: {
    enabled_by_default: [
      'CreateDocument', 'SummarizeContent',
      'GenerateImage', 'CreativeBrainstorm'
    ],
    optional: [
      'GenerateVideoDraft', 'GenerateMusicDraft',
      'BrowseWeb'
    ],
    restricted: []
  },
  
  my_team: {
    enabled_by_default: [
      'CreateDocument', 'EditDocument', 'StructureDocument',
      'CreateThread', 'LinkThreads', 'SummarizeThread',
      'PrepareMeeting', 'TakeMeetingNotes', 'GenerateMinutes', 'ExtractActionItems',
      'OptionComparison', 'DecisionSupport'
    ],
    optional: [
      'GeneratePDF', 'GenerateDOCX',
      'CreateTable', 'GenerateSpreadsheet',
      'SituationAnalysis', 'RiskAnalysis',
      'BrowseWeb'
    ],
    restricted: []
  }
};

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  SKILLS_CATALOG,
  DOCUMENT_SKILLS,
  TABLE_SKILLS,
  THREAD_SKILLS,
  ANALYSIS_SKILLS,
  MEETING_SKILLS,
  WEB_SKILLS,
  CREATIVE_SKILLS,
  SPHERE_SKILL_RULES,
  
  // Helper functions
  getSkillById: (skillId) => {
    return Object.values(SKILLS_CATALOG).find(skill => skill.id === skillId);
  },
  
  getSkillsByCategory: (category) => {
    return Object.values(SKILLS_CATALOG).filter(skill => skill.category === category);
  },
  
  getSkillsForSphere: (sphereId, includeOptional = true) => {
    const rules = SPHERE_SKILL_RULES[sphereId];
    if (!rules) return [];
    
    let skills = rules.enabled_by_default;
    if (includeOptional) {
      skills = [...skills, ...rules.optional];
    }
    
    return skills.map(skillName => {
      return Object.values(SKILLS_CATALOG).find(s => s.name === skillName);
    }).filter(Boolean);
  },
  
  isSkillAllowedInSphere: (skillName, sphereId) => {
    const rules = SPHERE_SKILL_RULES[sphereId];
    if (!rules) return false;
    
    return !rules.restricted.includes(skillName);
  }
};
