############################################################
#                                                          #
#       CHE·NU TEMPLATE FACTORY LAYER                      #
#       SCHEMA + FRONTEND                                  #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION B7 — TEMPLATE SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/template.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/template.schema.json",
  "title": "CHE·NU Template Schema",
  "description": "JSON Schema for CHE·NU representational templates",
  "type": "object",
  "required": ["id", "name", "type", "structure", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique template identifier",
      "pattern": "^tpl_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Template name"
    },
    "type": {
      "type": "string",
      "description": "Template type",
      "enum": ["project", "mission", "process", "persona", "object", "simulation", "xr-scene"]
    },
    "description": {
      "type": "string",
      "description": "Template description"
    },
    "structure": {
      "$ref": "#/definitions/template_structure"
    },
    "recommended_engines": {
      "type": "array",
      "description": "Recommended engines for this template",
      "items": { "type": "string" }
    },
    "compatible_spheres": {
      "type": "array",
      "description": "Compatible spheres",
      "items": { "type": "string" }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" },
        "generator_version": { "type": "string" },
        "category": { "type": "string" },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "template_structure": {
      "type": "object",
      "required": ["sections", "fields"],
      "properties": {
        "sections": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/template_section"
          }
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/template_field"
          }
        },
        "relationships": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/template_relationship"
          }
        },
        "placeholders": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "template_section": {
      "type": "object",
      "required": ["id", "name", "order", "required"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "order": { "type": "integer", "minimum": 1 },
        "required": { "type": "boolean" }
      }
    },
    "template_field": {
      "type": "object",
      "required": ["id", "name", "type", "section_id", "required"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["text", "number", "date", "list", "reference", "enum"]
        },
        "section_id": { "type": "string" },
        "required": { "type": "boolean" },
        "default_value": {},
        "placeholder": { "type": "string" }
      }
    },
    "template_relationship": {
      "type": "object",
      "required": ["id", "source_section", "target_section", "relationship_type"],
      "properties": {
        "id": { "type": "string" },
        "source_section": { "type": "string" },
        "target_section": { "type": "string" },
        "relationship_type": {
          "type": "string",
          "enum": ["parent", "child", "sibling", "reference"]
        }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noAutonomy", "noExecution", "noRealPlans"],
      "properties": {
        "isRepresentational": { "type": "boolean", "const": true },
        "noAutonomy": { "type": "boolean", "const": true },
        "noExecution": { "type": "boolean", "const": true },
        "noRealPlans": { "type": "boolean", "const": true }
      }
    }
  },
  "additionalProperties": false
}

============================================================
SECTION B8 — FRONTEND: TEMPLATES PAGE
============================================================

--- FILE: /che-nu-frontend/pages/templates.tsx

/**
 * CHE·NU Frontend — Template Factory Page
 * ========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Create and manage representational templates.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { TemplateViewer } from '../components/TemplateViewer';

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

const TYPE_ICONS: Record<string, string> = {
  project: '📁',
  mission: '🎯',
  process: '⚙️',
  persona: '👤',
  object: '📦',
  simulation: '🎬',
  'xr-scene': '🥽',
};

const TYPE_COLORS: Record<string, string> = {
  project: COLORS.sacredGold,
  mission: COLORS.earthEmber,
  process: COLORS.jungleEmerald,
  persona: COLORS.cenoteTurquoise,
  object: COLORS.ancientStone,
  simulation: '#9B59B6',
  'xr-scene': '#3498DB',
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

type TemplateType = 'project' | 'mission' | 'process' | 'persona' | 'object' | 'simulation' | 'xr-scene';

interface TemplateSection {
  id: string;
  name: string;
  description: string;
  order: number;
  required: boolean;
}

interface TemplateField {
  id: string;
  name: string;
  type: string;
  section_id: string;
  required: boolean;
}

interface TemplateModel {
  id: string;
  name: string;
  type: TemplateType;
  description: string;
  structure: {
    sections: TemplateSection[];
    fields: TemplateField[];
    placeholders: string[];
  };
  recommended_engines: string[];
  compatible_spheres: string[];
}

interface TemplateCategory {
  id: string;
  name: string;
  icon: string;
  types: TemplateType[];
}

// ============================================================
// SAMPLE DATA
// ============================================================

const TEMPLATE_CATEGORIES: TemplateCategory[] = [
  { id: 'planning', name: 'Planning', icon: '📋', types: ['project', 'mission'] },
  { id: 'workflow', name: 'Workflow', icon: '⚙️', types: ['process'] },
  { id: 'modeling', name: 'Modeling', icon: '🎭', types: ['persona', 'object'] },
  { id: 'analysis', name: 'Analysis', icon: '📊', types: ['simulation'] },
  { id: 'immersive', name: 'Immersive', icon: '🥽', types: ['xr-scene'] },
];

const SAMPLE_TEMPLATES: TemplateModel[] = [
  {
    id: 'tpl_proj_001',
    name: 'Research Project Template',
    type: 'project',
    description: 'Template for research and discovery projects',
    structure: {
      sections: [
        { id: 'overview', name: 'Overview', description: 'Project overview', order: 1, required: true },
        { id: 'methodology', name: 'Methodology', description: 'Research methodology', order: 2, required: true },
        { id: 'findings', name: 'Findings', description: 'Research findings', order: 3, required: false },
      ],
      fields: [
        { id: 'name', name: 'Project Name', type: 'text', section_id: 'overview', required: true },
        { id: 'question', name: 'Research Question', type: 'text', section_id: 'overview', required: true },
      ],
      placeholders: ['[PROJECT_NAME]', '[RESEARCH_QUESTION]'],
    },
    recommended_engines: ['KnowledgeEngine', 'SimulationEngine'],
    compatible_spheres: ['knowledge', 'research'],
  },
  {
    id: 'tpl_msn_001',
    name: 'Investigation Mission Template',
    type: 'mission',
    description: 'Template for investigative missions',
    structure: {
      sections: [
        { id: 'brief', name: 'Mission Brief', description: 'Mission overview', order: 1, required: true },
        { id: 'objectives', name: 'Objectives', description: 'Mission objectives', order: 2, required: true },
      ],
      fields: [
        { id: 'name', name: 'Mission Name', type: 'text', section_id: 'brief', required: true },
      ],
      placeholders: ['[MISSION_NAME]'],
    },
    recommended_engines: ['MissionEngine'],
    compatible_spheres: ['mission'],
  },
  {
    id: 'tpl_proc_001',
    name: 'Iterative Cycle Template',
    type: 'process',
    description: 'Template for iterative processes',
    structure: {
      sections: [
        { id: 'plan', name: 'Plan', description: 'Planning phase', order: 1, required: true },
        { id: 'do', name: 'Do', description: 'Execution phase', order: 2, required: true },
        { id: 'check', name: 'Check', description: 'Review phase', order: 3, required: true },
        { id: 'act', name: 'Act', description: 'Action phase', order: 4, required: true },
      ],
      fields: [],
      placeholders: [],
    },
    recommended_engines: ['ProcessEngine'],
    compatible_spheres: ['process', 'workflow'],
  },
  {
    id: 'tpl_xr_001',
    name: 'Studio Scene Template',
    type: 'xr-scene',
    description: 'Template for creative studio XR scenes',
    structure: {
      sections: [
        { id: 'environment', name: 'Environment', description: 'Scene environment', order: 1, required: true },
        { id: 'objects', name: 'Objects', description: 'Scene objects', order: 2, required: false },
      ],
      fields: [
        { id: 'name', name: 'Scene Name', type: 'text', section_id: 'environment', required: true },
      ],
      placeholders: ['[SCENE_NAME]'],
    },
    recommended_engines: ['XREngine'],
    compatible_spheres: ['xr', 'creative'],
  },
];

// ============================================================
// MAIN COMPONENT
// ============================================================

export function TemplatesPage() {
  const [templates, setTemplates] = useState<TemplateModel[]>(SAMPLE_TEMPLATES);
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateModel | null>(SAMPLE_TEMPLATES[0]);
  const [selectedType, setSelectedType] = useState<TemplateType | 'all'>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'detail'>('detail');
  const [showGenerator, setShowGenerator] = useState(false);
  
  // Filter templates by type
  const filteredTemplates = useMemo(() => {
    if (selectedType === 'all') return templates;
    return templates.filter(t => t.type === selectedType);
  }, [templates, selectedType]);
  
  // Generate new template
  const handleGenerateTemplate = (type: TemplateType) => {
    const newTemplate: TemplateModel = {
      id: `tpl_${Date.now().toString(36)}_new`,
      name: `New ${type.charAt(0).toUpperCase() + type.slice(1)} Template`,
      type,
      description: `Generated ${type} template`,
      structure: {
        sections: [
          { id: 'main', name: 'Main Section', description: 'Primary section', order: 1, required: true },
        ],
        fields: [
          { id: 'name', name: 'Name', type: 'text', section_id: 'main', required: true },
        ],
        placeholders: ['[NAME]'],
      },
      recommended_engines: [],
      compatible_spheres: [],
    };
    
    setTemplates([...templates, newTemplate]);
    setSelectedTemplate(newTemplate);
    setShowGenerator(false);
  };
  
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
              <span>🏭</span>
              Template Factory
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Generate representational templates for CHE·NU structures
            </p>
          </div>
          <button
            onClick={() => setShowGenerator(true)}
            style={{
              padding: '10px 20px',
              backgroundColor: COLORS.sacredGold,
              color: COLORS.uiSlate,
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            + Generate Template
          </button>
        </div>
        
        {/* Controls */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '16px', 
          alignItems: 'center',
        }}>
          {/* Type filter */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              onClick={() => setSelectedType('all')}
              style={{
                padding: '8px 16px',
                backgroundColor: selectedType === 'all' ? COLORS.sacredGold : COLORS.shadowMoss,
                color: selectedType === 'all' ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: selectedType === 'all' ? 600 : 400,
              }}
            >
              All
            </button>
            {(['project', 'mission', 'process', 'persona', 'object', 'simulation', 'xr-scene'] as TemplateType[]).map(type => (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                style={{
                  padding: '8px 16px',
                  backgroundColor: selectedType === type ? TYPE_COLORS[type] : COLORS.shadowMoss,
                  color: selectedType === type ? COLORS.uiSlate : COLORS.softSand,
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: selectedType === type ? 600 : 400,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                }}
              >
                <span>{TYPE_ICONS[type]}</span>
                {type.charAt(0).toUpperCase() + type.slice(1).replace('-', ' ')}
              </button>
            ))}
          </div>
          
          {/* View mode */}
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
            <button
              onClick={() => setViewMode('grid')}
              style={{
                padding: '8px 12px',
                backgroundColor: viewMode === 'grid' ? COLORS.sacredGold : COLORS.shadowMoss,
                color: viewMode === 'grid' ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
              }}
            >
              📋 Grid
            </button>
            <button
              onClick={() => setViewMode('detail')}
              style={{
                padding: '8px 12px',
                backgroundColor: viewMode === 'detail' ? COLORS.sacredGold : COLORS.shadowMoss,
                color: viewMode === 'detail' ? COLORS.uiSlate : COLORS.softSand,
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
              }}
            >
              👁️ Detail
            </button>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Sidebar */}
        <div style={{
          width: '300px',
          borderRight: `1px solid ${COLORS.shadowMoss}`,
          overflowY: 'auto',
          padding: '16px',
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '16px',
          }}>
            <h3 style={{ margin: 0, fontSize: '14px', color: COLORS.ancientStone }}>
              Templates ({filteredTemplates.length})
            </h3>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {filteredTemplates.map(tpl => (
              <div
                key={tpl.id}
                onClick={() => setSelectedTemplate(tpl)}
                style={{
                  padding: '12px',
                  backgroundColor: selectedTemplate?.id === tpl.id 
                    ? `${TYPE_COLORS[tpl.type]}20` 
                    : COLORS.shadowMoss,
                  borderRadius: '8px',
                  cursor: 'pointer',
                  borderLeft: selectedTemplate?.id === tpl.id 
                    ? `3px solid ${TYPE_COLORS[tpl.type]}` 
                    : '3px solid transparent',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '24px' }}>{TYPE_ICONS[tpl.type]}</span>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '14px' }}>{tpl.name}</div>
                    <div style={{ 
                      fontSize: '11px', 
                      color: TYPE_COLORS[tpl.type],
                      textTransform: 'capitalize',
                    }}>
                      {tpl.type.replace('-', ' ')}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {filteredTemplates.length === 0 && (
              <div style={{ 
                padding: '20px', 
                textAlign: 'center', 
                color: COLORS.ancientStone,
              }}>
                No templates found
              </div>
            )}
          </div>
        </div>
        
        {/* Main View */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {viewMode === 'detail' && selectedTemplate && (
            <TemplateViewer template={selectedTemplate} />
          )}
          {viewMode === 'grid' && (
            <TemplateGridView 
              templates={filteredTemplates} 
              onSelect={setSelectedTemplate}
              selectedId={selectedTemplate?.id}
            />
          )}
          {!selectedTemplate && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>🏭</span>
                <p>Select a template or generate a new one</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Generator Modal */}
      {showGenerator && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{
            backgroundColor: COLORS.uiSlate,
            borderRadius: '16px',
            padding: '24px',
            width: '600px',
            maxHeight: '80vh',
            overflowY: 'auto',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, fontSize: '20px' }}>Generate Template</h2>
              <button
                onClick={() => setShowGenerator(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: COLORS.ancientStone,
                  cursor: 'pointer',
                  fontSize: '20px',
                }}
              >
                ✕
              </button>
            </div>
            
            <p style={{ margin: '0 0 20px', color: COLORS.ancientStone }}>
              Choose a template type to generate:
            </p>
            
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(2, 1fr)', 
              gap: '12px',
            }}>
              {(['project', 'mission', 'process', 'persona', 'object', 'simulation', 'xr-scene'] as TemplateType[]).map(type => (
                <div
                  key={type}
                  onClick={() => handleGenerateTemplate(type)}
                  style={{
                    padding: '16px',
                    backgroundColor: COLORS.shadowMoss,
                    borderRadius: '12px',
                    cursor: 'pointer',
                    border: '2px solid transparent',
                    transition: 'border-color 0.2s',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = TYPE_COLORS[type]}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'transparent'}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '32px' }}>{TYPE_ICONS[type]}</span>
                    <div>
                      <div style={{ fontWeight: 600, textTransform: 'capitalize' }}>
                        {type.replace('-', ' ')}
                      </div>
                      <div style={{ fontSize: '12px', color: TYPE_COLORS[type] }}>
                        Generate new template
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      
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
          SAFE · NON-AUTONOMOUS · NO REAL PLANS · Templates are representational structures only
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

interface TemplateGridViewProps {
  templates: TemplateModel[];
  onSelect: (tpl: TemplateModel) => void;
  selectedId?: string;
}

function TemplateGridView({ templates, onSelect, selectedId }: TemplateGridViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
        gap: '16px',
      }}>
        {templates.map(tpl => (
          <div
            key={tpl.id}
            onClick={() => onSelect(tpl)}
            style={{
              padding: '20px',
              backgroundColor: selectedId === tpl.id 
                ? `${TYPE_COLORS[tpl.type]}15` 
                : COLORS.shadowMoss,
              borderRadius: '12px',
              cursor: 'pointer',
              border: `2px solid ${selectedId === tpl.id ? TYPE_COLORS[tpl.type] : 'transparent'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
              <span style={{ fontSize: '36px' }}>{TYPE_ICONS[tpl.type]}</span>
              <div>
                <h3 style={{ margin: 0, fontSize: '16px' }}>{tpl.name}</h3>
                <span style={{
                  fontSize: '11px',
                  padding: '2px 8px',
                  backgroundColor: `${TYPE_COLORS[tpl.type]}20`,
                  color: TYPE_COLORS[tpl.type],
                  borderRadius: '4px',
                  textTransform: 'capitalize',
                }}>
                  {tpl.type.replace('-', ' ')}
                </span>
              </div>
            </div>
            
            <p style={{ 
              margin: '0 0 12px', 
              fontSize: '13px', 
              color: COLORS.ancientStone,
              lineHeight: 1.4,
            }}>
              {tpl.description}
            </p>
            
            <div style={{ display: 'flex', gap: '16px', fontSize: '12px' }}>
              <span style={{ color: COLORS.cenoteTurquoise }}>
                {tpl.structure.sections.length} sections
              </span>
              <span style={{ color: COLORS.earthEmber }}>
                {tpl.structure.fields.length} fields
              </span>
              <span style={{ color: COLORS.jungleEmerald }}>
                {tpl.recommended_engines.length} engines
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TemplatesPage;

============================================================
SECTION B9 — FRONTEND: TEMPLATE VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/TemplateViewer.tsx

/**
 * CHE·NU Frontend — Template Viewer Component
 * ============================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
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
  project: '📁',
  mission: '🎯',
  process: '⚙️',
  persona: '👤',
  object: '📦',
  simulation: '🎬',
  'xr-scene': '🥽',
};

const TYPE_COLORS: Record<string, string> = {
  project: COLORS.sacredGold,
  mission: COLORS.earthEmber,
  process: COLORS.jungleEmerald,
  persona: COLORS.cenoteTurquoise,
  object: COLORS.ancientStone,
  simulation: '#9B59B6',
  'xr-scene': '#3498DB',
};

interface TemplateViewerProps {
  template: any;
}

export function TemplateViewer({ template }: TemplateViewerProps) {
  const typeColor = TYPE_COLORS[template.type] || COLORS.ancientStone;
  
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
            {TYPE_ICONS[template.type]}
          </div>
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: 700 }}>
              {template.name}
            </h1>
            <p style={{ margin: '0 0 12px', color: COLORS.ancientStone }}>
              {template.description}
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
              {template.type.replace('-', ' ')} Template
            </span>
          </div>
        </div>
      </div>
      
      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
        {/* Sections */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>📑</span> Sections ({template.structure.sections.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {template.structure.sections.map((section: any, index: number) => (
              <div key={section.id} style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
              }}>
                <div style={{
                  width: '28px',
                  height: '28px',
                  backgroundColor: `${typeColor}20`,
                  color: typeColor,
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 600,
                  fontSize: '12px',
                }}>
                  {section.order}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600, fontSize: '14px' }}>{section.name}</div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{section.description}</div>
                </div>
                {section.required && (
                  <span style={{
                    padding: '2px 8px',
                    backgroundColor: `${COLORS.earthEmber}20`,
                    color: COLORS.earthEmber,
                    borderRadius: '4px',
                    fontSize: '10px',
                  }}>
                    Required
                  </span>
                )}
              </div>
            ))}
            {template.structure.sections.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No sections defined
              </div>
            )}
          </div>
        </div>
        
        {/* Fields */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>📝</span> Fields ({template.structure.fields.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {template.structure.fields.map((field: any) => (
              <div key={field.id} style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ fontWeight: 600, fontSize: '14px' }}>{field.name}</div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <span style={{
                      padding: '2px 8px',
                      backgroundColor: `${COLORS.cenoteTurquoise}20`,
                      color: COLORS.cenoteTurquoise,
                      borderRadius: '4px',
                      fontSize: '10px',
                    }}>
                      {field.type}
                    </span>
                    {field.required && (
                      <span style={{
                        padding: '2px 8px',
                        backgroundColor: `${COLORS.earthEmber}20`,
                        color: COLORS.earthEmber,
                        borderRadius: '4px',
                        fontSize: '10px',
                      }}>
                        Required
                      </span>
                    )}
                  </div>
                </div>
                <div style={{ fontSize: '11px', color: COLORS.ancientStone, marginTop: '4px' }}>
                  Section: {field.section_id}
                </div>
              </div>
            ))}
            {template.structure.fields.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No fields defined
              </div>
            )}
          </div>
        </div>
        
        {/* Placeholders */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🏷️</span> Placeholders
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {template.structure.placeholders?.map((ph: string, i: number) => (
              <span key={i} style={{
                padding: '6px 12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '6px',
                fontSize: '12px',
                fontFamily: 'monospace',
                color: COLORS.sacredGold,
              }}>
                {ph}
              </span>
            ))}
            {(!template.structure.placeholders || template.structure.placeholders.length === 0) && (
              <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No placeholders
              </span>
            )}
          </div>
        </div>
        
        {/* Engines & Spheres */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>⚙️</span> Engines & Spheres
          </h3>
          
          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
              Recommended Engines
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {template.recommended_engines?.map((engine: string) => (
                <span key={engine} style={{
                  padding: '6px 12px',
                  backgroundColor: `${COLORS.sacredGold}20`,
                  color: COLORS.sacredGold,
                  borderRadius: '6px',
                  fontSize: '12px',
                }}>
                  {engine}
                </span>
              ))}
              {(!template.recommended_engines || template.recommended_engines.length === 0) && (
                <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '13px' }}>
                  No engines recommended
                </span>
              )}
            </div>
          </div>
          
          <div>
            <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
              Compatible Spheres
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {template.compatible_spheres?.map((sphere: string) => (
                <span key={sphere} style={{
                  padding: '6px 12px',
                  backgroundColor: `${COLORS.jungleEmerald}20`,
                  color: COLORS.jungleEmerald,
                  borderRadius: '6px',
                  fontSize: '12px',
                }}>
                  {sphere}
                </span>
              ))}
              {(!template.compatible_spheres || template.compatible_spheres.length === 0) && (
                <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '13px' }}>
                  No spheres specified
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* Structure Preview */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        marginTop: '24px',
      }}>
        <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🔍</span> Structure Preview
        </h3>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.uiSlate,
          borderRadius: '8px',
          fontFamily: 'monospace',
          fontSize: '12px',
          lineHeight: 1.6,
          overflowX: 'auto',
        }}>
          <pre style={{ margin: 0 }}>
{JSON.stringify({
  type: template.type,
  sections: template.structure.sections.map((s: any) => s.name),
  fields: template.structure.fields.map((f: any) => ({ name: f.name, type: f.type })),
  engines: template.recommended_engines,
  spheres: template.compatible_spheres,
}, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}

export default TemplateViewer;

============================================================
END OF TEMPLATE FACTORY SCHEMA + FRONTEND
============================================================
