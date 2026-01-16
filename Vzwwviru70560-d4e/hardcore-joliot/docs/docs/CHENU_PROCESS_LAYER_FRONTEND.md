############################################################
#                                                          #
#       CHE·NU PROCESS LAYER (PIPELINE SYSTEM)             #
#       PART 2: SCHEMA + FRONTEND                          #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 3 — PROCESS SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/process.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/process.schema.json",
  "title": "CHE·NU Process Schema",
  "description": "JSON Schema for CHE·NU process/pipeline structures",
  "type": "object",
  "required": ["id", "name", "steps", "transitions", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique process identifier",
      "pattern": "^proc_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Process name",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Process description",
      "maxLength": 2000
    },
    "version": {
      "type": "string",
      "description": "Process version",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "category": {
      "type": "string",
      "description": "Process category",
      "enum": ["general", "research", "creative", "xr", "personal", "business", "technical"]
    },
    "steps": {
      "type": "array",
      "description": "Process steps",
      "items": {
        "$ref": "#/definitions/process_step"
      }
    },
    "transitions": {
      "type": "array",
      "description": "Step transitions",
      "items": {
        "$ref": "#/definitions/process_transition"
      }
    },
    "states": {
      "type": "array",
      "description": "Process states",
      "items": {
        "$ref": "#/definitions/process_state"
      }
    },
    "context": {
      "$ref": "#/definitions/process_context"
    },
    "metadata": {
      "$ref": "#/definitions/process_metadata"
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "process_step": {
      "type": "object",
      "required": ["id", "name", "order"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^step_[a-z0-9]+_[a-z0-9]+$"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 100
        },
        "description": {
          "type": "string",
          "maxLength": 500
        },
        "order": {
          "type": "integer",
          "minimum": 1
        },
        "required_engines": {
          "type": "array",
          "items": { "type": "string" }
        },
        "suggested_agents": {
          "type": "array",
          "items": { "type": "string" }
        },
        "inputs": {
          "type": "array",
          "items": { "$ref": "#/definitions/step_io" }
        },
        "outputs": {
          "type": "array",
          "items": { "$ref": "#/definitions/step_io" }
        },
        "estimated_duration": {
          "type": "string"
        },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" }
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "step_io": {
      "type": "object",
      "required": ["name", "type", "required"],
      "properties": {
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["data", "document", "object", "decision", "approval"]
        },
        "description": { "type": "string" },
        "required": { "type": "boolean" },
        "schema": { "type": "string" }
      }
    },
    "process_transition": {
      "type": "object",
      "required": ["id", "from", "to", "type"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^trans_[a-z0-9]+_[a-z0-9]+$"
        },
        "from": { "type": "string" },
        "to": { "type": "string" },
        "condition": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["sequential", "conditional", "parallel", "loop"]
        },
        "weight": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "process_state": {
      "type": "object",
      "required": ["id", "step_id", "status"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^state_[a-z0-9]+_[a-z0-9]+$"
        },
        "step_id": { "type": "string" },
        "description": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["pending", "in_progress", "complete", "blocked", "skipped"]
        },
        "entered_at": {
          "type": "string",
          "format": "date-time"
        },
        "context": {
          "type": "object",
          "additionalProperties": true
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "process_context": {
      "type": "object",
      "properties": {
        "sphere": { "type": "string" },
        "project_id": { "type": "string" },
        "mission_id": { "type": "string" },
        "owner_agent": { "type": "string" },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"]
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "variables": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "process_metadata": {
      "type": "object",
      "properties": {
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "author": { "type": "string" },
        "template_source": { "type": "string" }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noAutonomy", "noExecution", "noPersistence"],
      "properties": {
        "isRepresentational": {
          "type": "boolean",
          "const": true
        },
        "noAutonomy": {
          "type": "boolean",
          "const": true
        },
        "noExecution": {
          "type": "boolean",
          "const": true
        },
        "noPersistence": {
          "type": "boolean",
          "const": true
        }
      }
    }
  },
  "additionalProperties": false
}

============================================================
SECTION 7 — FRONTEND: PROCESS PAGE
============================================================

--- FILE: /che-nu-frontend/pages/process.tsx

/**
 * CHE·NU Frontend — Process & Pipeline Tools Page
 * ================================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Process modeling, pipeline design, and workflow visualization.
 * All structures are representational only — no actual execution.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { ProcessViewer } from '../components/ProcessViewer';

// ============================================================
// CONSTANTS
// ============================================================

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

const STATUS_COLORS: Record<string, string> = {
  pending: COLORS.ancientStone,
  in_progress: COLORS.sacredGold,
  complete: COLORS.jungleEmerald,
  blocked: COLORS.earthEmber,
  skipped: '#6B7280',
};

const TRANSITION_COLORS: Record<string, string> = {
  sequential: COLORS.cenoteTurquoise,
  conditional: COLORS.sacredGold,
  parallel: COLORS.jungleEmerald,
  loop: COLORS.earthEmber,
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface ProcessStep {
  id: string;
  name: string;
  description: string;
  order: number;
  required_engines: string[];
  suggested_agents: string[];
  inputs: { name: string; type: string; required: boolean }[];
  outputs: { name: string; type: string; required: boolean }[];
  dependencies: string[];
  tags: string[];
}

interface ProcessTransition {
  id: string;
  from: string;
  to: string;
  condition: string;
  type: 'sequential' | 'conditional' | 'parallel' | 'loop';
  weight: number;
}

interface ProcessState {
  id: string;
  step_id: string;
  status: string;
  entered_at: string;
}

interface ProcessModel {
  id: string;
  name: string;
  description: string;
  version: string;
  category: string;
  steps: ProcessStep[];
  transitions: ProcessTransition[];
  states: ProcessState[];
  context: {
    sphere?: string;
    project_id?: string;
    priority: string;
  };
  metadata: {
    created_at: string;
    updated_at: string;
    template_source?: string;
  };
}

interface TemplateInfo {
  id: string;
  name: string;
  description: string;
  category: string;
  steps_count: number;
  complexity: string;
}

// ============================================================
// SAMPLE DATA
// ============================================================

const SAMPLE_TEMPLATES: TemplateInfo[] = [
  {
    id: 'research_pipeline',
    name: 'Research Pipeline',
    description: 'Standard research process from question to findings',
    category: 'research',
    steps_count: 5,
    complexity: 'moderate',
  },
  {
    id: 'creative_pipeline',
    name: 'Creative Pipeline',
    description: 'Creative content development process',
    category: 'creative',
    steps_count: 5,
    complexity: 'moderate',
  },
  {
    id: 'xr_production_pipeline',
    name: 'XR Production Pipeline',
    description: 'Extended Reality content production',
    category: 'xr',
    steps_count: 6,
    complexity: 'complex',
  },
  {
    id: 'personal_development_pipeline',
    name: 'Personal Development Pipeline',
    description: 'Self-improvement and growth process',
    category: 'personal',
    steps_count: 5,
    complexity: 'simple',
  },
];

const SAMPLE_PROCESS: ProcessModel = {
  id: 'proc_abc123_def456',
  name: 'Research Pipeline',
  description: 'Standard research process from question to findings',
  version: '1.0.0',
  category: 'research',
  steps: [
    {
      id: 'step_1_abc',
      name: 'Define Research Question',
      description: 'Clearly articulate the research question or hypothesis',
      order: 1,
      required_engines: ['KnowledgeEngine'],
      suggested_agents: ['ResearchLead'],
      inputs: [],
      outputs: [{ name: 'research_question', type: 'document', required: true }],
      dependencies: [],
      tags: ['input', 'planning'],
    },
    {
      id: 'step_2_def',
      name: 'Literature Review',
      description: 'Review existing research and literature',
      order: 2,
      required_engines: ['KnowledgeEngine', 'ContentEngine'],
      suggested_agents: ['Researcher'],
      inputs: [{ name: 'research_question', type: 'document', required: true }],
      outputs: [{ name: 'literature_review', type: 'document', required: true }],
      dependencies: ['step_1_abc'],
      tags: ['research', 'analysis'],
    },
    {
      id: 'step_3_ghi',
      name: 'Data Collection',
      description: 'Collect relevant data for analysis',
      order: 3,
      required_engines: ['DataEngine'],
      suggested_agents: ['DataAnalyst'],
      inputs: [{ name: 'methodology', type: 'document', required: true }],
      outputs: [{ name: 'raw_data', type: 'data', required: true }],
      dependencies: ['step_2_def'],
      tags: ['data', 'collection'],
    },
    {
      id: 'step_4_jkl',
      name: 'Analysis',
      description: 'Analyze collected data',
      order: 4,
      required_engines: ['AnalysisEngine', 'DataEngine'],
      suggested_agents: ['DataAnalyst', 'Researcher'],
      inputs: [{ name: 'raw_data', type: 'data', required: true }],
      outputs: [{ name: 'analysis_results', type: 'document', required: true }],
      dependencies: ['step_3_ghi'],
      tags: ['analysis'],
    },
    {
      id: 'step_5_mno',
      name: 'Synthesize Findings',
      description: 'Compile and synthesize research findings',
      order: 5,
      required_engines: ['ContentEngine', 'KnowledgeEngine'],
      suggested_agents: ['ResearchLead'],
      inputs: [
        { name: 'analysis_results', type: 'document', required: true },
        { name: 'literature_review', type: 'document', required: true },
      ],
      outputs: [{ name: 'research_findings', type: 'document', required: true }],
      dependencies: ['step_4_jkl'],
      tags: ['synthesis', 'output'],
    },
  ],
  transitions: [
    { id: 'trans_1', from: 'START', to: 'step_1_abc', condition: 'always', type: 'sequential', weight: 1 },
    { id: 'trans_2', from: 'step_1_abc', to: 'step_2_def', condition: 'always', type: 'sequential', weight: 1 },
    { id: 'trans_3', from: 'step_2_def', to: 'step_3_ghi', condition: 'always', type: 'sequential', weight: 1 },
    { id: 'trans_4', from: 'step_3_ghi', to: 'step_4_jkl', condition: 'always', type: 'sequential', weight: 1 },
    { id: 'trans_5', from: 'step_4_jkl', to: 'step_5_mno', condition: 'always', type: 'sequential', weight: 1 },
    { id: 'trans_6', from: 'step_5_mno', to: 'END', condition: 'always', type: 'sequential', weight: 1 },
  ],
  states: [
    { id: 'state_1', step_id: 'step_1_abc', status: 'complete', entered_at: '2024-12-10T10:00:00Z' },
    { id: 'state_2', step_id: 'step_2_def', status: 'complete', entered_at: '2024-12-11T14:00:00Z' },
    { id: 'state_3', step_id: 'step_3_ghi', status: 'in_progress', entered_at: '2024-12-12T09:00:00Z' },
    { id: 'state_4', step_id: 'step_4_jkl', status: 'pending', entered_at: '2024-12-12T00:00:00Z' },
    { id: 'state_5', step_id: 'step_5_mno', status: 'pending', entered_at: '2024-12-12T00:00:00Z' },
  ],
  context: {
    sphere: 'Scholar',
    project_id: 'proj_research_abc',
    priority: 'medium',
  },
  metadata: {
    created_at: '2024-12-10T08:00:00Z',
    updated_at: '2024-12-12T09:30:00Z',
    template_source: 'research_pipeline',
  },
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function ProcessPage() {
  const [selectedProcess, setSelectedProcess] = useState<ProcessModel | null>(SAMPLE_PROCESS);
  const [selectedStep, setSelectedStep] = useState<ProcessStep | null>(null);
  const [viewMode, setViewMode] = useState<'flow' | 'list' | 'timeline'>('flow');
  const [showTemplates, setShowTemplates] = useState(false);
  
  // Calculate process progress
  const progress = useMemo(() => {
    if (!selectedProcess) return 0;
    const completed = selectedProcess.states.filter(s => s.status === 'complete').length;
    return Math.round((completed / selectedProcess.states.length) * 100);
  }, [selectedProcess]);
  
  // Get engines used
  const enginesUsed = useMemo(() => {
    if (!selectedProcess) return [];
    const engines = new Set<string>();
    selectedProcess.steps.forEach(step => {
      step.required_engines.forEach(e => engines.add(e));
    });
    return Array.from(engines);
  }, [selectedProcess]);
  
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
              <span>🔄</span>
              Process & Pipeline Tools
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Design and visualize representational process models
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              onClick={() => setShowTemplates(!showTemplates)}
              style={{
                padding: '10px 20px',
                backgroundColor: showTemplates ? COLORS.sacredGold : COLORS.shadowMoss,
                color: showTemplates ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '8px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              📋 Templates
            </button>
            <button style={{
              padding: '10px 20px',
              backgroundColor: COLORS.jungleEmerald,
              color: COLORS.softSand,
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
            }}>
              + Create Process
            </button>
          </div>
        </div>
        
        {/* View Mode Toggle */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '8px',
          alignItems: 'center',
        }}>
          {(['flow', 'list', 'timeline'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                padding: '8px 16px',
                backgroundColor: viewMode === mode ? COLORS.sacredGold : COLORS.shadowMoss,
                color: viewMode === mode ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '6px',
                fontWeight: viewMode === mode ? 600 : 400,
                cursor: 'pointer',
              }}
            >
              {mode === 'flow' ? '🔀 Flow' : mode === 'list' ? '📋 List' : '📅 Timeline'}
            </button>
          ))}
          
          {selectedProcess && (
            <div style={{ 
              marginLeft: 'auto', 
              display: 'flex', 
              alignItems: 'center', 
              gap: '16px',
            }}>
              <div>
                <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>Progress</span>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}>
                  <div style={{
                    width: '120px',
                    height: '8px',
                    backgroundColor: COLORS.shadowMoss,
                    borderRadius: '4px',
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      width: `${progress}%`,
                      height: '100%',
                      backgroundColor: COLORS.jungleEmerald,
                    }} />
                  </div>
                  <span style={{ fontWeight: 600, color: COLORS.jungleEmerald }}>{progress}%</span>
                </div>
              </div>
              
              <div>
                <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>Steps</span>
                <div style={{ fontWeight: 600 }}>{selectedProcess.steps.length}</div>
              </div>
              
              <div>
                <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>Engines</span>
                <div style={{ fontWeight: 600 }}>{enginesUsed.length}</div>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Templates Sidebar */}
      {showTemplates && (
        <div style={{
          padding: '16px 24px',
          backgroundColor: COLORS.shadowMoss,
          borderBottom: `1px solid ${COLORS.uiSlate}`,
        }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.sacredGold }}>
            Available Templates
          </h3>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            {SAMPLE_TEMPLATES.map(template => (
              <div
                key={template.id}
                style={{
                  padding: '12px 16px',
                  backgroundColor: COLORS.uiSlate,
                  borderRadius: '8px',
                  cursor: 'pointer',
                  border: `1px solid ${COLORS.ancientStone}30`,
                  minWidth: '200px',
                }}
              >
                <div style={{ fontWeight: 600, marginBottom: '4px' }}>{template.name}</div>
                <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
                  {template.description}
                </div>
                <div style={{ 
                  display: 'flex', 
                  gap: '12px', 
                  fontSize: '11px', 
                  color: COLORS.cenoteTurquoise,
                }}>
                  <span>{template.steps_count} steps</span>
                  <span>{template.complexity}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Process Viewer */}
        <div style={{
          flex: selectedStep ? '1 1 60%' : 1,
          overflow: 'hidden',
          borderRight: selectedStep ? `1px solid ${COLORS.shadowMoss}` : 'none',
        }}>
          {selectedProcess ? (
            viewMode === 'flow' ? (
              <ProcessFlowView
                process={selectedProcess}
                onStepSelect={setSelectedStep}
                selectedStepId={selectedStep?.id}
              />
            ) : viewMode === 'list' ? (
              <ProcessListView
                process={selectedProcess}
                onStepSelect={setSelectedStep}
                selectedStepId={selectedStep?.id}
              />
            ) : (
              <ProcessTimelineView
                process={selectedProcess}
                onStepSelect={setSelectedStep}
                selectedStepId={selectedStep?.id}
              />
            )
          ) : (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>🔄</span>
                <p>Select a process or create a new one</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Step Detail Panel */}
        {selectedStep && selectedProcess && (
          <div style={{
            flex: '0 0 400px',
            overflowY: 'auto',
            padding: '20px',
            backgroundColor: '#16171a',
          }}>
            <StepDetailPanel
              step={selectedStep}
              state={selectedProcess.states.find(s => s.step_id === selectedStep.id)}
              transitions={selectedProcess.transitions.filter(
                t => t.from === selectedStep.id || t.to === selectedStep.id
              )}
              onClose={() => setSelectedStep(null)}
            />
          </div>
        )}
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
          SAFE · NON-AUTONOMOUS · Process models are representational only — no actual execution
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

interface ProcessViewProps {
  process: ProcessModel;
  onStepSelect: (step: ProcessStep) => void;
  selectedStepId?: string;
}

function ProcessFlowView({ process, onStepSelect, selectedStepId }: ProcessViewProps) {
  return (
    <div style={{ 
      padding: '40px', 
      overflowY: 'auto', 
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}>
      {/* Start Node */}
      <div style={{
        width: '60px',
        height: '60px',
        borderRadius: '50%',
        backgroundColor: COLORS.jungleEmerald,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '20px',
      }}>
        <span style={{ fontSize: '24px' }}>▶️</span>
      </div>
      
      {/* Steps */}
      {process.steps.map((step, index) => {
        const state = process.states.find(s => s.step_id === step.id);
        const statusColor = STATUS_COLORS[state?.status || 'pending'];
        const isSelected = selectedStepId === step.id;
        
        return (
          <React.Fragment key={step.id}>
            {/* Connector */}
            <div style={{
              width: '2px',
              height: '30px',
              backgroundColor: COLORS.ancientStone,
            }} />
            
            {/* Step Card */}
            <div
              onClick={() => onStepSelect(step)}
              style={{
                padding: '20px',
                backgroundColor: isSelected ? `${COLORS.sacredGold}20` : COLORS.shadowMoss,
                border: `2px solid ${isSelected ? COLORS.sacredGold : statusColor}`,
                borderRadius: '12px',
                cursor: 'pointer',
                width: '300px',
                textAlign: 'center',
                position: 'relative',
              }}
            >
              {/* Order badge */}
              <div style={{
                position: 'absolute',
                top: '-12px',
                left: '50%',
                transform: 'translateX(-50%)',
                backgroundColor: statusColor,
                color: COLORS.uiSlate,
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 700,
                fontSize: '12px',
              }}>
                {step.order}
              </div>
              
              <h4 style={{ margin: '8px 0', fontSize: '15px', fontWeight: 600 }}>
                {step.name}
              </h4>
              <p style={{ 
                margin: '0 0 12px', 
                fontSize: '12px', 
                color: COLORS.ancientStone,
                lineHeight: 1.4,
              }}>
                {step.description}
              </p>
              
              {/* Status badge */}
              <span style={{
                padding: '4px 10px',
                backgroundColor: `${statusColor}20`,
                color: statusColor,
                borderRadius: '4px',
                fontSize: '11px',
                fontWeight: 600,
                textTransform: 'uppercase',
              }}>
                {state?.status || 'pending'}
              </span>
              
              {/* Engines */}
              {step.required_engines.length > 0 && (
                <div style={{
                  marginTop: '12px',
                  display: 'flex',
                  gap: '6px',
                  justifyContent: 'center',
                  flexWrap: 'wrap',
                }}>
                  {step.required_engines.map(engine => (
                    <span
                      key={engine}
                      style={{
                        padding: '2px 8px',
                        backgroundColor: `${COLORS.cenoteTurquoise}15`,
                        color: COLORS.cenoteTurquoise,
                        borderRadius: '3px',
                        fontSize: '10px',
                      }}
                    >
                      ⚙️ {engine.replace('Engine', '')}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </React.Fragment>
        );
      })}
      
      {/* Final Connector */}
      <div style={{
        width: '2px',
        height: '30px',
        backgroundColor: COLORS.ancientStone,
      }} />
      
      {/* End Node */}
      <div style={{
        width: '60px',
        height: '60px',
        borderRadius: '50%',
        backgroundColor: COLORS.earthEmber,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <span style={{ fontSize: '24px' }}>🏁</span>
      </div>
    </div>
  );
}

function ProcessListView({ process, onStepSelect, selectedStepId }: ProcessViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: `1px solid ${COLORS.shadowMoss}` }}>
            <th style={{ padding: '12px', textAlign: 'left', color: COLORS.ancientStone, fontSize: '12px' }}>#</th>
            <th style={{ padding: '12px', textAlign: 'left', color: COLORS.ancientStone, fontSize: '12px' }}>STEP</th>
            <th style={{ padding: '12px', textAlign: 'left', color: COLORS.ancientStone, fontSize: '12px' }}>STATUS</th>
            <th style={{ padding: '12px', textAlign: 'left', color: COLORS.ancientStone, fontSize: '12px' }}>ENGINES</th>
            <th style={{ padding: '12px', textAlign: 'left', color: COLORS.ancientStone, fontSize: '12px' }}>I/O</th>
          </tr>
        </thead>
        <tbody>
          {process.steps.map(step => {
            const state = process.states.find(s => s.step_id === step.id);
            const statusColor = STATUS_COLORS[state?.status || 'pending'];
            const isSelected = selectedStepId === step.id;
            
            return (
              <tr
                key={step.id}
                onClick={() => onStepSelect(step)}
                style={{
                  backgroundColor: isSelected ? `${COLORS.sacredGold}15` : 'transparent',
                  cursor: 'pointer',
                  borderBottom: `1px solid ${COLORS.shadowMoss}`,
                }}
              >
                <td style={{ padding: '16px 12px' }}>
                  <span style={{
                    backgroundColor: statusColor,
                    color: COLORS.uiSlate,
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: '12px',
                  }}>
                    {step.order}
                  </span>
                </td>
                <td style={{ padding: '16px 12px' }}>
                  <div style={{ fontWeight: 500 }}>{step.name}</div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{step.description}</div>
                </td>
                <td style={{ padding: '16px 12px' }}>
                  <span style={{
                    padding: '4px 10px',
                    backgroundColor: `${statusColor}20`,
                    color: statusColor,
                    borderRadius: '4px',
                    fontSize: '11px',
                    fontWeight: 600,
                  }}>
                    {state?.status || 'pending'}
                  </span>
                </td>
                <td style={{ padding: '16px 12px' }}>
                  <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                    {step.required_engines.map(e => (
                      <span
                        key={e}
                        style={{
                          padding: '2px 6px',
                          backgroundColor: `${COLORS.cenoteTurquoise}15`,
                          color: COLORS.cenoteTurquoise,
                          borderRadius: '3px',
                          fontSize: '10px',
                        }}
                      >
                        {e.replace('Engine', '')}
                      </span>
                    ))}
                  </div>
                </td>
                <td style={{ padding: '16px 12px', fontSize: '12px', color: COLORS.ancientStone }}>
                  ↓{step.inputs.length} ↑{step.outputs.length}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function ProcessTimelineView({ process, onStepSelect, selectedStepId }: ProcessViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <div style={{ position: 'relative', paddingLeft: '40px' }}>
        {/* Timeline line */}
        <div style={{
          position: 'absolute',
          left: '15px',
          top: '0',
          bottom: '0',
          width: '2px',
          backgroundColor: COLORS.shadowMoss,
        }} />
        
        {process.steps.map((step, index) => {
          const state = process.states.find(s => s.step_id === step.id);
          const statusColor = STATUS_COLORS[state?.status || 'pending'];
          const isSelected = selectedStepId === step.id;
          
          return (
            <div
              key={step.id}
              onClick={() => onStepSelect(step)}
              style={{
                position: 'relative',
                marginBottom: '24px',
                cursor: 'pointer',
              }}
            >
              {/* Timeline dot */}
              <div style={{
                position: 'absolute',
                left: '-32px',
                top: '8px',
                width: '16px',
                height: '16px',
                borderRadius: '50%',
                backgroundColor: statusColor,
                border: `3px solid ${COLORS.uiSlate}`,
              }} />
              
              {/* Content card */}
              <div style={{
                padding: '16px',
                backgroundColor: isSelected ? `${COLORS.sacredGold}15` : COLORS.shadowMoss,
                borderRadius: '8px',
                borderLeft: `3px solid ${statusColor}`,
              }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'flex-start',
                  marginBottom: '8px',
                }}>
                  <h4 style={{ margin: 0, fontSize: '14px', fontWeight: 600 }}>
                    {step.order}. {step.name}
                  </h4>
                  <span style={{
                    padding: '2px 8px',
                    backgroundColor: `${statusColor}20`,
                    color: statusColor,
                    borderRadius: '3px',
                    fontSize: '10px',
                    fontWeight: 600,
                  }}>
                    {state?.status || 'pending'}
                  </span>
                </div>
                <p style={{ 
                  margin: '0 0 8px', 
                  fontSize: '12px', 
                  color: COLORS.ancientStone,
                }}>
                  {step.description}
                </p>
                <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
                  {state?.entered_at && (
                    <span>Entered: {new Date(state.entered_at).toLocaleString()}</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

interface StepDetailPanelProps {
  step: ProcessStep;
  state?: ProcessState;
  transitions: ProcessTransition[];
  onClose: () => void;
}

function StepDetailPanel({ step, state, transitions, onClose }: StepDetailPanelProps) {
  const statusColor = STATUS_COLORS[state?.status || 'pending'];
  
  return (
    <div>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '20px',
      }}>
        <div>
          <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 700 }}>
            Step {step.order}: {step.name}
          </h2>
          <span style={{
            display: 'inline-block',
            marginTop: '8px',
            padding: '4px 10px',
            backgroundColor: `${statusColor}20`,
            color: statusColor,
            borderRadius: '4px',
            fontSize: '12px',
            fontWeight: 600,
          }}>
            {state?.status || 'pending'}
          </span>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '8px',
            backgroundColor: 'transparent',
            border: 'none',
            color: COLORS.ancientStone,
            cursor: 'pointer',
          }}
        >
          ✕
        </button>
      </div>
      
      {/* Description */}
      <div style={{
        padding: '12px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '8px',
        marginBottom: '20px',
      }}>
        <p style={{ margin: 0, fontSize: '14px', lineHeight: 1.5 }}>
          {step.description}
        </p>
      </div>
      
      {/* Required Engines */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
          Required Engines
        </h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {step.required_engines.map(engine => (
            <span
              key={engine}
              style={{
                padding: '6px 12px',
                backgroundColor: `${COLORS.cenoteTurquoise}15`,
                color: COLORS.cenoteTurquoise,
                borderRadius: '6px',
                fontSize: '13px',
              }}
            >
              ⚙️ {engine}
            </span>
          ))}
          {step.required_engines.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>None required</span>
          )}
        </div>
      </div>
      
      {/* Suggested Agents */}
      {step.suggested_agents.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Suggested Agents
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {step.suggested_agents.map(agent => (
              <span
                key={agent}
                style={{
                  padding: '6px 12px',
                  backgroundColor: `${COLORS.sacredGold}15`,
                  color: COLORS.sacredGold,
                  borderRadius: '6px',
                  fontSize: '13px',
                }}
              >
                🤖 {agent}
              </span>
            ))}
          </div>
        </div>
      )}
      
      {/* Inputs & Outputs */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
        <div>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Inputs ({step.inputs.length})
          </h4>
          {step.inputs.map((input, i) => (
            <div
              key={i}
              style={{
                padding: '8px 12px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                marginBottom: '8px',
                borderLeft: `3px solid ${COLORS.jungleEmerald}`,
              }}
            >
              <div style={{ fontSize: '13px', fontWeight: 500 }}>↓ {input.name}</div>
              <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
                {input.type} {input.required && '(required)'}
              </div>
            </div>
          ))}
          {step.inputs.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '12px' }}>
              No inputs
            </span>
          )}
        </div>
        <div>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Outputs ({step.outputs.length})
          </h4>
          {step.outputs.map((output, i) => (
            <div
              key={i}
              style={{
                padding: '8px 12px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                marginBottom: '8px',
                borderLeft: `3px solid ${COLORS.cenoteTurquoise}`,
              }}
            >
              <div style={{ fontSize: '13px', fontWeight: 500 }}>↑ {output.name}</div>
              <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
                {output.type} {output.required && '(required)'}
              </div>
            </div>
          ))}
          {step.outputs.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '12px' }}>
              No outputs
            </span>
          )}
        </div>
      </div>
      
      {/* Transitions */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
          Transitions
        </h4>
        {transitions.map(trans => {
          const isIncoming = trans.to === step.id;
          const transColor = TRANSITION_COLORS[trans.type];
          
          return (
            <div
              key={trans.id}
              style={{
                padding: '10px 12px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
              }}
            >
              <span style={{
                padding: '2px 8px',
                backgroundColor: `${transColor}20`,
                color: transColor,
                borderRadius: '3px',
                fontSize: '10px',
                fontWeight: 600,
              }}>
                {trans.type}
              </span>
              <span style={{ fontSize: '13px' }}>
                {isIncoming ? `← from ${trans.from}` : `→ to ${trans.to}`}
              </span>
              <span style={{ fontSize: '11px', color: COLORS.ancientStone, marginLeft: 'auto' }}>
                {trans.condition}
              </span>
            </div>
          );
        })}
      </div>
      
      {/* Tags */}
      {step.tags.length > 0 && (
        <div>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Tags
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {step.tags.map(tag => (
              <span
                key={tag}
                style={{
                  padding: '4px 10px',
                  backgroundColor: COLORS.shadowMoss,
                  color: COLORS.softSand,
                  borderRadius: '4px',
                  fontSize: '12px',
                }}
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ProcessPage;

============================================================
SECTION — SYSTEM INDEX + ORCHESTRATOR UPDATES
============================================================

--- FILE: /che-nu-sdk/system_index.json (PROCESS LAYER ADDITIONS)

{
  "core_modules": {
    "ProcessEngine": {
      "path": "/che-nu-sdk/core/process.ts",
      "description": "Representational process/pipeline modeling",
      "category": "process_layer"
    }
  },
  
  "submodules": {
    "process_layer": {
      "StepEngine": "/che-nu-sdk/core/process/step.engine.ts",
      "TransitionEngine": "/che-nu-sdk/core/process/transition.engine.ts",
      "StateEngine": "/che-nu-sdk/core/process/state.engine.ts",
      "PipelineEngine": "/che-nu-sdk/core/process/pipeline.engine.ts",
      "ProcessTemplateEngine": "/che-nu-sdk/core/process/template.engine.ts"
    }
  },
  
  "schemas": {
    "process": "/che-nu-sdk/schemas/process.schema.json"
  },
  
  "frontend_pages": {
    "process": "/che-nu-frontend/pages/process.tsx"
  },
  
  "components": {
    "ProcessViewer": "/che-nu-frontend/components/ProcessViewer.tsx"
  }
}

--- FILE: /che-nu-sdk/core/orchestrator.ts (ADDITIONS)

// Add to domain routing:
// If domain === "Process" OR domain === "Pipeline" OR domain === "Workflow" → "ProcessEngine"

--- FILE: /che-nu-sdk/core/context_interpreter.ts (ADDITIONS)

// Add rule:
// If input contains "process", "pipeline", "workflow", "step", "transition", "state", "template"
// → return domain = "Process"

============================================================
END OF PROCESS LAYER COMPLETE
============================================================

✅ PROCESS LAYER COMPLETE:
- ProcessEngine (core)
- 5 sub-engines (step, transition, state, pipeline, template)
- process.schema.json
- process.tsx page
- ProcessViewer components
- 4 process templates (Research, Creative, XR Production, Personal Development)
- Orchestrator routing
- Context interpreter rules
- System index updates
