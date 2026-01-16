############################################################
#                                                          #
#       CHE·NU TOOL LAYER                                  #
#       TOOLSETS + TOOLCHAINS + PIPELINES + SCHEMA         #
#       + FRONTEND                                         #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION C7 — TOOLSETS LIBRARY
============================================================

--- FILE: /che-nu-sdk/core/tool/toolsets.ts

/**
 * CHE·NU ToolSet Library
 * =======================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

import { ToolSet, ToolModel } from '../tool';

// ============================================================
// PREDEFINED TOOLSETS
// ============================================================

export const TOOLSETS: ToolSet[] = [
  {
    id: 'toolset_analysis_basic',
    name: 'Analysis Basic Set',
    description: 'Basic analysis tools for data structures',
    tools: [
      {
        id: 'tool_analysis_pattern', name: 'Pattern Analyzer', type: 'analysis',
        description: 'Analyzes patterns', inputs: [], outputs: [], required_engines: ['KnowledgeEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_analysis_node', name: 'Node Analyzer', type: 'analysis',
        description: 'Analyzes nodes', inputs: [], outputs: [], required_engines: ['KnowledgeEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'analysis',
    metadata: {},
  },
  {
    id: 'toolset_mapping_core',
    name: 'Mapping Core Set',
    description: 'Core mapping tools for CHE·NU structures',
    tools: [
      {
        id: 'tool_mapping_engine', name: 'Engine Mapper', type: 'mapping',
        description: 'Maps to engines', inputs: [], outputs: [], required_engines: [],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_mapping_sphere', name: 'Sphere Mapper', type: 'mapping',
        description: 'Maps to spheres', inputs: [], outputs: [], required_engines: [],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_mapping_graph_linker', name: 'Graph Linker', type: 'mapping',
        description: 'Links graph nodes', inputs: [], outputs: [], required_engines: ['KnowledgeEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'mapping',
    metadata: {},
  },
  {
    id: 'toolset_process_construction',
    name: 'Process Construction Set',
    description: 'Tools for building process structures',
    tools: [
      {
        id: 'tool_construction_process', name: 'Process Builder', type: 'construction',
        description: 'Builds processes', inputs: [], outputs: [], required_engines: ['ProcessEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_construction_workflow', name: 'Workflow Builder', type: 'construction',
        description: 'Builds workflows', inputs: [], outputs: [], required_engines: ['ProcessEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'construction',
    metadata: {},
  },
  {
    id: 'toolset_xr_builder',
    name: 'XR Builder Set',
    description: 'Tools for XR scene creation',
    tools: [
      {
        id: 'tool_xr_scene_placeholder', name: 'XR Scene Placeholder', type: 'xr-helper',
        description: 'Creates scene placeholders', inputs: [], outputs: [], required_engines: ['XREngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_xr_object_mapping', name: 'XR Object Mapper', type: 'xr-helper',
        description: 'Maps XR objects', inputs: [], outputs: [], required_engines: ['XREngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_xr_environment_builder', name: 'XR Environment Builder', type: 'xr-helper',
        description: 'Builds XR environments', inputs: [], outputs: [], required_engines: ['XREngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'xr',
    metadata: {},
  },
  {
    id: 'toolset_persona_influence',
    name: 'Persona Influence Set',
    description: 'Tools for persona-based workflows',
    tools: [
      {
        id: 'tool_persona_trait_mapper', name: 'Trait Mapper', type: 'mapping',
        description: 'Maps persona traits', inputs: [], outputs: [], required_engines: ['PersonaEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_persona_style_matcher', name: 'Style Matcher', type: 'mapping',
        description: 'Matches persona styles', inputs: [], outputs: [], required_engines: ['PersonaEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'persona',
    metadata: {},
  },
  {
    id: 'toolset_simulation_helper',
    name: 'Simulation Helper Set',
    description: 'Tools for simulation workflows',
    tools: [
      {
        id: 'tool_simulation_frame_builder', name: 'Frame Builder', type: 'construction',
        description: 'Builds simulation frames', inputs: [], outputs: [], required_engines: ['SimulationEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
      {
        id: 'tool_simulation_branch_analyzer', name: 'Branch Analyzer', type: 'analysis',
        description: 'Analyzes simulation branches', inputs: [], outputs: [], required_engines: ['SimulationEngine'],
        metadata: { created_at: '', version: '1.0.0' },
        safe: { isRepresentational: true, noExecution: true, noAPI: true },
      },
    ],
    category: 'simulation',
    metadata: {},
  },
];

export const ToolSetLibrary = {
  name: 'ToolSetLibrary',
  version: '1.0.0',
  
  listToolSets(): ToolSet[] {
    return TOOLSETS;
  },
  
  getToolSet(id: string): ToolSet | null {
    return TOOLSETS.find(ts => ts.id === id) || null;
  },
  
  getToolSetsByCategory(category: string): ToolSet[] {
    return TOOLSETS.filter(ts => ts.category === category);
  },
  
  listCategories(): string[] {
    return [...new Set(TOOLSETS.map(ts => ts.category))];
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      toolset_count: TOOLSETS.length,
      categories: this.listCategories(),
    };
  },
};

export default ToolSetLibrary;

============================================================
SECTION C8 — TOOLCHAINS LIBRARY
============================================================

--- FILE: /che-nu-sdk/core/tool/toolchains.ts

/**
 * CHE·NU ToolChain Library
 * =========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

import { ToolChain } from '../tool';

// ============================================================
// PREDEFINED TOOLCHAINS
// ============================================================

export const TOOLCHAINS: ToolChain[] = [
  {
    id: 'toolchain_project_startup',
    name: 'Project Startup ToolChain',
    description: 'Tools for initializing projects',
    steps: [
      { order: 1, tool_id: 'tool_analysis_pattern', tool_name: 'Pattern Analyzer', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_mapping_engine', tool_name: 'Engine Mapper', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_construction_process', tool_name: 'Process Builder', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'project' },
  },
  {
    id: 'toolchain_mission_structuring',
    name: 'Mission Structuring ToolChain',
    description: 'Tools for structuring missions',
    steps: [
      { order: 1, tool_id: 'tool_analysis_dependency', tool_name: 'Dependency Analyzer', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_mapping_sphere', tool_name: 'Sphere Mapper', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_construction_workflow', tool_name: 'Workflow Builder', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'mission' },
  },
  {
    id: 'toolchain_process_mapping',
    name: 'Process Mapping Chain',
    description: 'Tools for mapping processes',
    steps: [
      { order: 1, tool_id: 'tool_analysis_node', tool_name: 'Node Analyzer', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_mapping_graph_linker', tool_name: 'Graph Linker', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_transform_structure', tool_name: 'Structure Transformer', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'process' },
  },
  {
    id: 'toolchain_knowledge_expansion',
    name: 'Knowledge Graph Expansion Chain',
    description: 'Tools for expanding knowledge graphs',
    steps: [
      { order: 1, tool_id: 'tool_abstraction_concept_extractor', tool_name: 'Concept Extractor', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_mapping_graph_linker', tool_name: 'Graph Linker', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_analysis_pattern', tool_name: 'Pattern Analyzer', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'knowledge' },
  },
  {
    id: 'toolchain_xr_scene_assembly',
    name: 'XR Scene Assembly Chain',
    description: 'Tools for assembling XR scenes',
    steps: [
      { order: 1, tool_id: 'tool_xr_environment_builder', tool_name: 'XR Environment Builder', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_xr_scene_placeholder', tool_name: 'XR Scene Placeholder', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_xr_object_mapping', tool_name: 'XR Object Mapper', input_mapping: {}, output_mapping: {} },
      { order: 4, tool_id: 'tool_xr_interaction_definer', tool_name: 'XR Interaction Definer', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'xr' },
  },
  {
    id: 'toolchain_simulation_prep',
    name: 'Simulation Prep Chain',
    description: 'Tools for preparing simulations',
    steps: [
      { order: 1, tool_id: 'tool_analysis_complexity', tool_name: 'Complexity Analyzer', input_mapping: {}, output_mapping: {} },
      { order: 2, tool_id: 'tool_simulation_frame_builder', tool_name: 'Frame Builder', input_mapping: {}, output_mapping: {} },
      { order: 3, tool_id: 'tool_mapping_context', tool_name: 'Context Mapper', input_mapping: {}, output_mapping: {} },
    ],
    metadata: { category: 'simulation' },
  },
];

export const ToolChainLibrary = {
  name: 'ToolChainLibrary',
  version: '1.0.0',
  
  listToolChains(): ToolChain[] {
    return TOOLCHAINS;
  },
  
  getToolChain(id: string): ToolChain | null {
    return TOOLCHAINS.find(tc => tc.id === id) || null;
  },
  
  getToolChainsByCategory(category: string): ToolChain[] {
    return TOOLCHAINS.filter(tc => tc.metadata?.category === category);
  },
  
  listCategories(): string[] {
    return [...new Set(TOOLCHAINS.map(tc => tc.metadata?.category).filter(Boolean))];
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      toolchain_count: TOOLCHAINS.length,
      categories: this.listCategories(),
    };
  },
};

export default ToolChainLibrary;

============================================================
SECTION C9 — TOOLPIPELINES LIBRARY
============================================================

--- FILE: /che-nu-sdk/core/tool/toolpipelines.ts

/**
 * CHE·NU ToolPipeline Library
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

import { ToolPipeline } from '../tool';

// ============================================================
// PREDEFINED PIPELINES
// ============================================================

export const TOOLPIPELINES: ToolPipeline[] = [
  {
    id: 'pipeline_project_mapping',
    name: 'Project Mapping Pipeline',
    description: 'Maps project structures to engines',
    toolchain_id: 'toolchain_project_startup',
    mapped_process_id: null,
    mapped_engine_ids: ['ProjectEngine', 'ProcessEngine'],
    metadata: { category: 'project' },
  },
  {
    id: 'pipeline_mission_execution',
    name: 'Mission Execution Pipeline',
    description: 'Pipeline for mission structuring',
    toolchain_id: 'toolchain_mission_structuring',
    mapped_process_id: null,
    mapped_engine_ids: ['MissionEngine', 'ProcessEngine'],
    metadata: { category: 'mission' },
  },
  {
    id: 'pipeline_knowledge_graph',
    name: 'Knowledge Graph Pipeline',
    description: 'Pipeline for knowledge graph operations',
    toolchain_id: 'toolchain_knowledge_expansion',
    mapped_process_id: null,
    mapped_engine_ids: ['KnowledgeEngine'],
    metadata: { category: 'knowledge' },
  },
  {
    id: 'pipeline_xr_production',
    name: 'XR Production Pipeline',
    description: 'Pipeline for XR scene production',
    toolchain_id: 'toolchain_xr_scene_assembly',
    mapped_process_id: null,
    mapped_engine_ids: ['XREngine', 'ContextEngine'],
    metadata: { category: 'xr' },
  },
  {
    id: 'pipeline_simulation_run',
    name: 'Simulation Run Pipeline',
    description: 'Pipeline for simulation workflows',
    toolchain_id: 'toolchain_simulation_prep',
    mapped_process_id: null,
    mapped_engine_ids: ['SimulationEngine'],
    metadata: { category: 'simulation' },
  },
  {
    id: 'pipeline_process_optimization',
    name: 'Process Optimization Pipeline',
    description: 'Pipeline for process optimization',
    toolchain_id: 'toolchain_process_mapping',
    mapped_process_id: null,
    mapped_engine_ids: ['ProcessEngine', 'SimulationEngine'],
    metadata: { category: 'process' },
  },
];

export const ToolPipelineLibrary = {
  name: 'ToolPipelineLibrary',
  version: '1.0.0',
  
  listToolPipelines(): ToolPipeline[] {
    return TOOLPIPELINES;
  },
  
  getToolPipeline(id: string): ToolPipeline | null {
    return TOOLPIPELINES.find(tp => tp.id === id) || null;
  },
  
  getToolPipelinesByEngine(engineId: string): ToolPipeline[] {
    return TOOLPIPELINES.filter(tp => tp.mapped_engine_ids.includes(engineId));
  },
  
  getToolPipelinesByCategory(category: string): ToolPipeline[] {
    return TOOLPIPELINES.filter(tp => tp.metadata?.category === category);
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      pipeline_count: TOOLPIPELINES.length,
    };
  },
};

export default ToolPipelineLibrary;

============================================================
SECTION C10 — TOOL SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/tool.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/tool.schema.json",
  "title": "CHE·NU Tool Schema",
  "description": "JSON Schema for CHE·NU representational tools",
  "definitions": {
    "tool": {
      "type": "object",
      "required": ["id", "name", "type", "safe"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^tool_[a-z0-9_]+$"
        },
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["analysis", "transformation", "mapping", "construction", "abstraction", "contextual", "xr-helper", "knowledge", "fabric-tool", "timeline-tool", "projection-tool"]
        },
        "description": { "type": "string" },
        "inputs": {
          "type": "array",
          "items": { "$ref": "#/definitions/tool_parameter" }
        },
        "outputs": {
          "type": "array",
          "items": { "$ref": "#/definitions/tool_parameter" }
        },
        "required_engines": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": { "type": "object" },
        "safe": { "$ref": "#/definitions/safe_compliance" }
      }
    },
    "tool_parameter": {
      "type": "object",
      "required": ["name", "type", "required"],
      "properties": {
        "name": { "type": "string" },
        "type": { "enum": ["string", "number", "boolean", "object", "array", "reference"] },
        "description": { "type": "string" },
        "required": { "type": "boolean" }
      }
    },
    "toolset": {
      "type": "object",
      "required": ["id", "name", "tools", "category"],
      "properties": {
        "id": { "type": "string", "pattern": "^toolset_[a-z0-9_]+$" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "tools": { "type": "array", "items": { "$ref": "#/definitions/tool" } },
        "category": { "type": "string" },
        "metadata": { "type": "object" }
      }
    },
    "toolchain": {
      "type": "object",
      "required": ["id", "name", "steps"],
      "properties": {
        "id": { "type": "string", "pattern": "^toolchain_[a-z0-9_]+$" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "steps": { "type": "array", "items": { "$ref": "#/definitions/toolchain_step" } },
        "metadata": { "type": "object" }
      }
    },
    "toolchain_step": {
      "type": "object",
      "required": ["order", "tool_id", "tool_name"],
      "properties": {
        "order": { "type": "integer", "minimum": 1 },
        "tool_id": { "type": "string" },
        "tool_name": { "type": "string" },
        "input_mapping": { "type": "object" },
        "output_mapping": { "type": "object" }
      }
    },
    "toolpipeline": {
      "type": "object",
      "required": ["id", "name", "toolchain_id", "mapped_engine_ids"],
      "properties": {
        "id": { "type": "string", "pattern": "^pipeline_[a-z0-9_]+$" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "toolchain_id": { "type": "string" },
        "mapped_process_id": { "type": ["string", "null"] },
        "mapped_engine_ids": { "type": "array", "items": { "type": "string" } },
        "metadata": { "type": "object" }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noExecution", "noAPI"],
      "properties": {
        "isRepresentational": { "type": "boolean", "const": true },
        "noExecution": { "type": "boolean", "const": true },
        "noAPI": { "type": "boolean", "const": true }
      }
    }
  },
  "oneOf": [
    { "$ref": "#/definitions/tool" },
    { "$ref": "#/definitions/toolset" },
    { "$ref": "#/definitions/toolchain" },
    { "$ref": "#/definitions/toolpipeline" }
  ]
}

============================================================
SECTION C11 — FRONTEND: TOOLS PAGE
============================================================

--- FILE: /che-nu-frontend/pages/tools.tsx

/**
 * CHE·NU Frontend — Tool Layer Page
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

import React, { useState } from 'react';
import { ToolViewer } from '../components/ToolViewer';

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

const TYPE_ICONS: Record<string, string> = {
  analysis: '🔍',
  transformation: '🔄',
  mapping: '🗺️',
  construction: '🏗️',
  abstraction: '💭',
  'xr-helper': '🥽',
  knowledge: '📚',
};

const TYPE_COLORS: Record<string, string> = {
  analysis: COLORS.cenoteTurquoise,
  transformation: COLORS.sacredGold,
  mapping: COLORS.jungleEmerald,
  construction: COLORS.earthEmber,
  abstraction: '#9B59B6',
  'xr-helper': '#3498DB',
  knowledge: COLORS.ancientStone,
};

// Sample data
const SAMPLE_TOOLS = [
  { id: 'tool_analysis_pattern', name: 'Pattern Analyzer', type: 'analysis', description: 'Analyzes patterns in data structures', inputs: 2, outputs: 2, engines: ['KnowledgeEngine'] },
  { id: 'tool_mapping_engine', name: 'Engine Mapper', type: 'mapping', description: 'Maps elements to appropriate engines', inputs: 1, outputs: 2, engines: [] },
  { id: 'tool_construction_process', name: 'Process Builder', type: 'construction', description: 'Builds process structures', inputs: 2, outputs: 1, engines: ['ProcessEngine'] },
  { id: 'tool_xr_scene_placeholder', name: 'XR Scene Placeholder', type: 'xr-helper', description: 'Creates XR scene placeholders', inputs: 2, outputs: 1, engines: ['XREngine'] },
];

const SAMPLE_TOOLSETS = [
  { id: 'toolset_analysis_basic', name: 'Analysis Basic Set', category: 'analysis', tool_count: 4 },
  { id: 'toolset_mapping_core', name: 'Mapping Core Set', category: 'mapping', tool_count: 4 },
  { id: 'toolset_xr_builder', name: 'XR Builder Set', category: 'xr', tool_count: 4 },
];

const SAMPLE_TOOLCHAINS = [
  { id: 'toolchain_project_startup', name: 'Project Startup Chain', step_count: 3, category: 'project' },
  { id: 'toolchain_xr_scene_assembly', name: 'XR Scene Assembly Chain', step_count: 4, category: 'xr' },
  { id: 'toolchain_simulation_prep', name: 'Simulation Prep Chain', step_count: 3, category: 'simulation' },
];

const SAMPLE_PIPELINES = [
  { id: 'pipeline_project_mapping', name: 'Project Mapping Pipeline', toolchain: 'Project Startup', engines: ['ProjectEngine', 'ProcessEngine'] },
  { id: 'pipeline_xr_production', name: 'XR Production Pipeline', toolchain: 'XR Scene Assembly', engines: ['XREngine', 'ContextEngine'] },
];

type ViewTab = 'tools' | 'toolsets' | 'toolchains' | 'pipelines';

export function ToolsPage() {
  const [activeTab, setActiveTab] = useState<ViewTab>('tools');
  const [selectedTool, setSelectedTool] = useState<any>(SAMPLE_TOOLS[0]);
  
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      backgroundColor: COLORS.uiSlate,
      color: COLORS.softSand,
    }}>
      {/* Header */}
      <div style={{
        padding: '20px 24px',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ 
              margin: 0, 
              fontSize: '24px', 
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
            }}>
              <span>🛠️</span>
              Tool Layer
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Representational tools, toolsets, toolchains, and pipelines
            </p>
          </div>
        </div>
        
        {/* Tabs */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '4px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '10px',
          padding: '4px',
          width: 'fit-content',
        }}>
          {(['tools', 'toolsets', 'toolchains', 'pipelines'] as ViewTab[]).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '10px 20px',
                backgroundColor: activeTab === tab ? COLORS.sacredGold : 'transparent',
                color: activeTab === tab ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: activeTab === tab ? 600 : 400,
                textTransform: 'capitalize',
              }}
            >
              {tab === 'tools' && '🔧'} 
              {tab === 'toolsets' && '📦'} 
              {tab === 'toolchains' && '⛓️'} 
              {tab === 'pipelines' && '🔀'} 
              {' '}{tab}
            </button>
          ))}
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Sidebar */}
        <div style={{
          width: '320px',
          borderRight: `1px solid ${COLORS.shadowMoss}`,
          overflowY: 'auto',
          padding: '16px',
        }}>
          {activeTab === 'tools' && (
            <>
              <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
                Tools ({SAMPLE_TOOLS.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {SAMPLE_TOOLS.map(tool => (
                  <div
                    key={tool.id}
                    onClick={() => setSelectedTool(tool)}
                    style={{
                      padding: '12px',
                      backgroundColor: selectedTool?.id === tool.id 
                        ? `${TYPE_COLORS[tool.type]}20` 
                        : COLORS.shadowMoss,
                      borderRadius: '8px',
                      cursor: 'pointer',
                      borderLeft: selectedTool?.id === tool.id 
                        ? `3px solid ${TYPE_COLORS[tool.type]}` 
                        : '3px solid transparent',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span style={{ fontSize: '20px' }}>{TYPE_ICONS[tool.type]}</span>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '14px' }}>{tool.name}</div>
                        <div style={{ 
                          fontSize: '11px', 
                          color: TYPE_COLORS[tool.type],
                          textTransform: 'capitalize',
                        }}>
                          {tool.type}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeTab === 'toolsets' && (
            <>
              <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
                ToolSets ({SAMPLE_TOOLSETS.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {SAMPLE_TOOLSETS.map(ts => (
                  <div
                    key={ts.id}
                    style={{
                      padding: '12px',
                      backgroundColor: COLORS.shadowMoss,
                      borderRadius: '8px',
                    }}
                  >
                    <div style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>
                      📦 {ts.name}
                    </div>
                    <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>
                      {ts.tool_count} tools • {ts.category}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeTab === 'toolchains' && (
            <>
              <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
                ToolChains ({SAMPLE_TOOLCHAINS.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {SAMPLE_TOOLCHAINS.map(tc => (
                  <div
                    key={tc.id}
                    style={{
                      padding: '12px',
                      backgroundColor: COLORS.shadowMoss,
                      borderRadius: '8px',
                    }}
                  >
                    <div style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>
                      ⛓️ {tc.name}
                    </div>
                    <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>
                      {tc.step_count} steps • {tc.category}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeTab === 'pipelines' && (
            <>
              <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
                Pipelines ({SAMPLE_PIPELINES.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {SAMPLE_PIPELINES.map(pl => (
                  <div
                    key={pl.id}
                    style={{
                      padding: '12px',
                      backgroundColor: COLORS.shadowMoss,
                      borderRadius: '8px',
                    }}
                  >
                    <div style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>
                      🔀 {pl.name}
                    </div>
                    <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '6px' }}>
                      Chain: {pl.toolchain}
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {pl.engines.map(e => (
                        <span key={e} style={{
                          padding: '2px 6px',
                          backgroundColor: `${COLORS.sacredGold}20`,
                          color: COLORS.sacredGold,
                          borderRadius: '4px',
                          fontSize: '10px',
                        }}>
                          {e}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
        
        {/* Detail View */}
        <div style={{ flex: 1, overflow: 'auto' }}>
          {activeTab === 'tools' && selectedTool && (
            <ToolViewer tool={selectedTool} />
          )}
          {activeTab !== 'tools' && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>
                  {activeTab === 'toolsets' && '📦'}
                  {activeTab === 'toolchains' && '⛓️'}
                  {activeTab === 'pipelines' && '🔀'}
                </span>
                <p>Select a {activeTab.slice(0, -1)} to view details</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* SAFE Notice */}
      <div style={{
        padding: '12px 24px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderTop: `1px solid ${COLORS.jungleEmerald}30`,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span>🔒</span>
        <span style={{ fontSize: '12px', color: COLORS.jungleEmerald }}>
          SAFE · NO EXECUTION · NO API CALLS · Tools are representational structures only
        </span>
      </div>
    </div>
  );
}

export default ToolsPage;

============================================================
SECTION C12 — FRONTEND: TOOL VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/ToolViewer.tsx

/**
 * CHE·NU Frontend — Tool Viewer Component
 * ========================================
 * @version 1.0.0
 */

import React from 'react';

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

const TYPE_ICONS: Record<string, string> = {
  analysis: '🔍',
  transformation: '🔄',
  mapping: '🗺️',
  construction: '🏗️',
  abstraction: '💭',
  'xr-helper': '🥽',
  knowledge: '📚',
};

const TYPE_COLORS: Record<string, string> = {
  analysis: COLORS.cenoteTurquoise,
  transformation: COLORS.sacredGold,
  mapping: COLORS.jungleEmerald,
  construction: COLORS.earthEmber,
  abstraction: '#9B59B6',
  'xr-helper': '#3498DB',
  knowledge: COLORS.ancientStone,
};

interface ToolViewerProps {
  tool: any;
}

export function ToolViewer({ tool }: ToolViewerProps) {
  const typeColor = TYPE_COLORS[tool.type] || COLORS.ancientStone;
  
  return (
    <div style={{ padding: '24px', overflowY: 'auto', height: '100%', backgroundColor: '#16171a' }}>
      {/* Header */}
      <div style={{
        padding: '32px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '16px',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{
            width: '80px',
            height: '80px',
            backgroundColor: `${typeColor}20`,
            borderRadius: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '40px',
          }}>
            {TYPE_ICONS[tool.type] || '🔧'}
          </div>
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: 700 }}>
              {tool.name}
            </h1>
            <p style={{ margin: '0 0 12px', color: COLORS.ancientStone }}>
              {tool.description}
            </p>
            <span style={{
              display: 'inline-block',
              padding: '4px 12px',
              backgroundColor: `${typeColor}20`,
              color: typeColor,
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              textTransform: 'capitalize',
            }}>
              {tool.type} Tool
            </span>
          </div>
        </div>
      </div>
      
      {/* Stats */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(4, 1fr)', 
        gap: '16px',
        marginBottom: '24px',
      }}>
        <div style={{
          padding: '20px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color: COLORS.cenoteTurquoise }}>
            {tool.inputs || 0}
          </div>
          <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>Inputs</div>
        </div>
        <div style={{
          padding: '20px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color: COLORS.sacredGold }}>
            {tool.outputs || 0}
          </div>
          <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>Outputs</div>
        </div>
        <div style={{
          padding: '20px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color: COLORS.jungleEmerald }}>
            {tool.engines?.length || 0}
          </div>
          <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>Engines</div>
        </div>
        <div style={{
          padding: '20px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color: COLORS.earthEmber }}>
            ✓
          </div>
          <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>SAFE</div>
        </div>
      </div>
      
      {/* Required Engines */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        marginBottom: '24px',
      }}>
        <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>⚙️</span> Required Engines
        </h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {tool.engines?.length > 0 ? (
            tool.engines.map((engine: string) => (
              <span key={engine} style={{
                padding: '8px 16px',
                backgroundColor: `${COLORS.sacredGold}20`,
                color: COLORS.sacredGold,
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: 500,
              }}>
                {engine}
              </span>
            ))
          ) : (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
              No specific engine required
            </span>
          )}
        </div>
      </div>
      
      {/* SAFE Compliance */}
      <div style={{
        padding: '24px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderRadius: '12px',
        border: `1px solid ${COLORS.jungleEmerald}30`,
      }}>
        <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px', color: COLORS.jungleEmerald }}>
          <span>🔒</span> SAFE Compliance
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
          <div style={{
            padding: '12px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '20px', marginBottom: '4px' }}>✅</div>
            <div style={{ fontSize: '12px' }}>Representational</div>
          </div>
          <div style={{
            padding: '12px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '20px', marginBottom: '4px' }}>✅</div>
            <div style={{ fontSize: '12px' }}>No Execution</div>
          </div>
          <div style={{
            padding: '12px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '20px', marginBottom: '4px' }}>✅</div>
            <div style={{ fontSize: '12px' }}>No API Calls</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ToolViewer;

============================================================
END OF TOOL LAYER COMPLETE
============================================================
