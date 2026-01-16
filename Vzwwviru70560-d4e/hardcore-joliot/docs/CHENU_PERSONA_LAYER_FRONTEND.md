############################################################
#                                                          #
#       CHE·NU PERSONA LAYER                               #
#       PART 2: FRONTEND + SCHEMA + UPDATES                #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION B4 — PERSONA SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/persona.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/persona.schema.json",
  "title": "CHE·NU Persona Schema",
  "description": "JSON Schema for CHE·NU representational personas",
  "type": "object",
  "required": ["id", "name", "category", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique persona identifier",
      "pattern": "^persona_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Persona name"
    },
    "description": {
      "type": "string",
      "description": "Persona description"
    },
    "avatar_icon": {
      "type": "string",
      "description": "Emoji or icon for persona"
    },
    "category": {
      "type": "string",
      "description": "Persona category",
      "enum": ["user", "work", "creative", "analytical", "collaborative"]
    },
    "traits": {
      "type": "array",
      "description": "Abstract structural traits",
      "items": {
        "$ref": "#/definitions/persona_trait"
      }
    },
    "styles": {
      "type": "array",
      "description": "Work styles",
      "items": {
        "$ref": "#/definitions/persona_style"
      }
    },
    "domain_affinities": {
      "type": "array",
      "description": "Domain affinity mappings",
      "items": {
        "$ref": "#/definitions/domain_affinity"
      }
    },
    "engine_affinities": {
      "type": "array",
      "description": "Engine affinity mappings",
      "items": {
        "$ref": "#/definitions/engine_affinity"
      }
    },
    "capability_influences": {
      "type": "array",
      "description": "Capability influence mappings",
      "items": {
        "$ref": "#/definitions/capability_influence"
      }
    },
    "process_preferences": {
      "$ref": "#/definitions/process_preferences"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" },
        "template_source": { "type": "string" },
        "version": { "type": "string" }
      }
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "persona_trait": {
      "type": "object",
      "required": ["id", "name", "category", "intensity"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "category": {
          "type": "string",
          "enum": ["cognitive", "behavioral", "communicative", "organizational"]
        },
        "description": { "type": "string" },
        "intensity": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "metadata": { "type": "object" }
      }
    },
    "persona_style": {
      "type": "object",
      "required": ["id", "name", "type"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["workflow", "communication", "decision_making", "collaboration"]
        },
        "description": { "type": "string" },
        "preferences": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": { "type": "object" }
      }
    },
    "domain_affinity": {
      "type": "object",
      "required": ["domain", "affinity_level"],
      "properties": {
        "domain": { "type": "string" },
        "affinity_level": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "expertise_tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "notes": { "type": "string" }
      }
    },
    "engine_affinity": {
      "type": "object",
      "required": ["engine", "affinity_level"],
      "properties": {
        "engine": { "type": "string" },
        "affinity_level": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "usage_frequency": {
          "type": "string",
          "enum": ["rare", "occasional", "frequent", "primary"]
        },
        "notes": { "type": "string" }
      }
    },
    "capability_influence": {
      "type": "object",
      "required": ["capability", "influence_type", "strength"],
      "properties": {
        "capability": { "type": "string" },
        "influence_type": {
          "type": "string",
          "enum": ["enhances", "challenges", "neutral"]
        },
        "strength": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "description": { "type": "string" }
      }
    },
    "process_preferences": {
      "type": "object",
      "properties": {
        "preferred_complexity": {
          "type": "string",
          "enum": ["simple", "moderate", "complex"]
        },
        "preferred_pace": {
          "type": "string",
          "enum": ["slow", "moderate", "fast"]
        },
        "iteration_preference": {
          "type": "string",
          "enum": ["minimal", "moderate", "extensive"]
        }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noAutonomy", "noPsychology", "noAdvice"],
      "properties": {
        "isRepresentational": { "type": "boolean", "const": true },
        "noAutonomy": { "type": "boolean", "const": true },
        "noPsychology": { "type": "boolean", "const": true },
        "noAdvice": { "type": "boolean", "const": true }
      }
    }
  },
  "additionalProperties": false
}

============================================================
SECTION B5 — FRONTEND: PERSONA PAGE
============================================================

--- FILE: /che-nu-frontend/pages/persona.tsx

/**
 * CHE·NU Frontend — Persona Builder Page
 * ========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Create and manage representational personas.
 * NOT psychology — structural modeling only.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { PersonaViewer } from '../components/PersonaViewer';

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

const CATEGORY_ICONS: Record<string, string> = {
  user: '👤',
  work: '💼',
  creative: '🎨',
  analytical: '📊',
  collaborative: '🤝',
};

const CATEGORY_COLORS: Record<string, string> = {
  user: COLORS.cenoteTurquoise,
  work: COLORS.sacredGold,
  creative: COLORS.earthEmber,
  analytical: COLORS.jungleEmerald,
  collaborative: COLORS.ancientStone,
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface PersonaTrait {
  id: string;
  name: string;
  category: 'cognitive' | 'behavioral' | 'communicative' | 'organizational';
  description: string;
  intensity: number;
}

interface PersonaStyle {
  id: string;
  name: string;
  type: 'workflow' | 'communication' | 'decision_making' | 'collaboration';
  description: string;
  preferences: string[];
}

interface DomainAffinity {
  domain: string;
  affinity_level: number;
  expertise_tags: string[];
}

interface EngineAffinity {
  engine: string;
  affinity_level: number;
  usage_frequency: 'rare' | 'occasional' | 'frequent' | 'primary';
}

interface PersonaModel {
  id: string;
  name: string;
  description: string;
  avatar_icon: string;
  category: 'user' | 'work' | 'creative' | 'analytical' | 'collaborative';
  traits: PersonaTrait[];
  styles: PersonaStyle[];
  domain_affinities: DomainAffinity[];
  engine_affinities: EngineAffinity[];
  process_preferences: {
    preferred_complexity: 'simple' | 'moderate' | 'complex';
    preferred_pace: 'slow' | 'moderate' | 'fast';
    iteration_preference: 'minimal' | 'moderate' | 'extensive';
  };
}

interface PersonaTemplate {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
}

// ============================================================
// SAMPLE DATA
// ============================================================

const PERSONA_TEMPLATES: PersonaTemplate[] = [
  { id: 'explorer', name: 'Explorer', description: 'Discovery and learning focused', icon: '🧭', category: 'creative' },
  { id: 'architect', name: 'Architect', description: 'Structure and design focused', icon: '🏗️', category: 'analytical' },
  { id: 'analyst', name: 'Analyst', description: 'Data and insights focused', icon: '📊', category: 'analytical' },
  { id: 'creative', name: 'Creative', description: 'Innovation and expression focused', icon: '🎨', category: 'creative' },
  { id: 'strategist', name: 'Strategist', description: 'Vision and planning focused', icon: '♟️', category: 'analytical' },
  { id: 'maker', name: 'Maker', description: 'Building and execution focused', icon: '🛠️', category: 'work' },
];

const TRAIT_CATALOG: Record<string, { name: string; category: string; description: string }> = {
  analytical: { name: 'Analytical', category: 'cognitive', description: 'Preference for data-driven analysis' },
  creative: { name: 'Creative', category: 'cognitive', description: 'Preference for novel approaches' },
  systematic: { name: 'Systematic', category: 'cognitive', description: 'Preference for methodical approaches' },
  exploratory: { name: 'Exploratory', category: 'cognitive', description: 'Preference for discovery' },
  focused: { name: 'Focused', category: 'behavioral', description: 'Deep concentration preference' },
  proactive: { name: 'Proactive', category: 'behavioral', description: 'Initiative-taking tendency' },
  concise: { name: 'Concise', category: 'communicative', description: 'Brief communication preference' },
  verbose: { name: 'Verbose', category: 'communicative', description: 'Detailed communication preference' },
  structured: { name: 'Structured', category: 'organizational', description: 'Organized approach preference' },
  flexible: { name: 'Flexible', category: 'organizational', description: 'Adaptable approach preference' },
};

const SAMPLE_PERSONA: PersonaModel = {
  id: 'persona_abc123_def456',
  name: 'Research Explorer',
  description: 'A discovery-focused persona oriented toward research and learning',
  avatar_icon: '🧭',
  category: 'creative',
  traits: [
    { id: 'trait_1', name: 'Exploratory', category: 'cognitive', description: 'Preference for discovery', intensity: 0.9 },
    { id: 'trait_2', name: 'Creative', category: 'cognitive', description: 'Preference for novel approaches', intensity: 0.7 },
    { id: 'trait_3', name: 'Flexible', category: 'organizational', description: 'Adaptable approach', intensity: 0.8 },
  ],
  styles: [
    { id: 'style_1', name: 'Iterative', type: 'workflow', description: 'Cyclic refinement', preferences: ['Multiple passes', 'Feedback loops'] },
    { id: 'style_2', name: 'Informal', type: 'communication', description: 'Casual communication', preferences: ['Quick chats', 'Direct messages'] },
  ],
  domain_affinities: [
    { domain: 'knowledge', affinity_level: 0.9, expertise_tags: ['Research', 'Discovery'] },
    { domain: 'creative', affinity_level: 0.7, expertise_tags: ['Ideation'] },
  ],
  engine_affinities: [
    { engine: 'KnowledgeEngine', affinity_level: 0.9, usage_frequency: 'primary' },
    { engine: 'SimulationEngine', affinity_level: 0.7, usage_frequency: 'frequent' },
  ],
  process_preferences: {
    preferred_complexity: 'moderate',
    preferred_pace: 'moderate',
    iteration_preference: 'extensive',
  },
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function PersonaPage() {
  const [personas, setPersonas] = useState<PersonaModel[]>([SAMPLE_PERSONA]);
  const [selectedPersona, setSelectedPersona] = useState<PersonaModel | null>(SAMPLE_PERSONA);
  const [viewMode, setViewMode] = useState<'list' | 'detail' | 'builder'>('detail');
  const [showTemplates, setShowTemplates] = useState(false);
  
  // Create new persona from template
  const handleCreateFromTemplate = (templateId: string) => {
    const template = PERSONA_TEMPLATES.find(t => t.id === templateId);
    if (!template) return;
    
    const newPersona: PersonaModel = {
      id: `persona_${Date.now().toString(36)}_new`,
      name: `New ${template.name}`,
      description: template.description,
      avatar_icon: template.icon,
      category: template.category as PersonaModel['category'],
      traits: [],
      styles: [],
      domain_affinities: [],
      engine_affinities: [],
      process_preferences: {
        preferred_complexity: 'moderate',
        preferred_pace: 'moderate',
        iteration_preference: 'moderate',
      },
    };
    
    setPersonas([...personas, newPersona]);
    setSelectedPersona(newPersona);
    setShowTemplates(false);
    setViewMode('builder');
  };
  
  // Add trait to persona
  const handleAddTrait = (traitKey: string, intensity: number) => {
    if (!selectedPersona) return;
    
    const traitDef = TRAIT_CATALOG[traitKey];
    if (!traitDef) return;
    
    const newTrait: PersonaTrait = {
      id: `trait_${Date.now().toString(36)}`,
      name: traitDef.name,
      category: traitDef.category as PersonaTrait['category'],
      description: traitDef.description,
      intensity,
    };
    
    const updated = {
      ...selectedPersona,
      traits: [...selectedPersona.traits, newTrait],
    };
    
    setSelectedPersona(updated);
    setPersonas(personas.map(p => p.id === updated.id ? updated : p));
  };
  
  // Remove trait
  const handleRemoveTrait = (traitId: string) => {
    if (!selectedPersona) return;
    
    const updated = {
      ...selectedPersona,
      traits: selectedPersona.traits.filter(t => t.id !== traitId),
    };
    
    setSelectedPersona(updated);
    setPersonas(personas.map(p => p.id === updated.id ? updated : p));
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
              <span>👤</span>
              Persona Builder
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Create representational personas for CHE·NU workflows
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              onClick={() => setShowTemplates(true)}
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
              + New Persona
            </button>
          </div>
        </div>
        
        {/* Controls */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '16px', 
          alignItems: 'center',
        }}>
          {/* View mode toggle */}
          <div style={{ 
            display: 'flex', 
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
            overflow: 'hidden',
          }}>
            {(['list', 'detail', 'builder'] as const).map(mode => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                style={{
                  padding: '10px 16px',
                  backgroundColor: viewMode === mode ? COLORS.sacredGold : 'transparent',
                  color: viewMode === mode ? COLORS.uiSlate : COLORS.softSand,
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: viewMode === mode ? 600 : 400,
                }}
              >
                {mode === 'list' ? '📋' : mode === 'detail' ? '👁️' : '🔧'} {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
          
          {/* Stats */}
          <div style={{ 
            marginLeft: 'auto', 
            display: 'flex', 
            gap: '16px',
            fontSize: '13px',
          }}>
            <span style={{ color: COLORS.cenoteTurquoise }}>
              {personas.length} personas
            </span>
            {selectedPersona && (
              <>
                <span style={{ color: COLORS.earthEmber }}>
                  {selectedPersona.traits.length} traits
                </span>
                <span style={{ color: COLORS.jungleEmerald }}>
                  {selectedPersona.engine_affinities.length} engines
                </span>
              </>
            )}
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Sidebar: Persona List */}
        <div style={{
          width: '280px',
          borderRight: `1px solid ${COLORS.shadowMoss}`,
          overflowY: 'auto',
          padding: '16px',
        }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
            My Personas
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {personas.map(persona => (
              <div
                key={persona.id}
                onClick={() => setSelectedPersona(persona)}
                style={{
                  padding: '12px',
                  backgroundColor: selectedPersona?.id === persona.id 
                    ? `${COLORS.sacredGold}20` 
                    : COLORS.shadowMoss,
                  borderRadius: '8px',
                  cursor: 'pointer',
                  borderLeft: selectedPersona?.id === persona.id 
                    ? `3px solid ${COLORS.sacredGold}` 
                    : '3px solid transparent',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '24px' }}>{persona.avatar_icon}</span>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '14px' }}>{persona.name}</div>
                    <div style={{ 
                      fontSize: '11px', 
                      color: CATEGORY_COLORS[persona.category],
                      textTransform: 'capitalize',
                    }}>
                      {persona.category}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Main View */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {viewMode === 'list' && (
            <PersonaListView 
              personas={personas}
              onSelect={setSelectedPersona}
              selectedId={selectedPersona?.id}
            />
          )}
          {viewMode === 'detail' && selectedPersona && (
            <PersonaViewer persona={selectedPersona} />
          )}
          {viewMode === 'builder' && selectedPersona && (
            <PersonaBuilderView
              persona={selectedPersona}
              traitCatalog={TRAIT_CATALOG}
              onAddTrait={handleAddTrait}
              onRemoveTrait={handleRemoveTrait}
            />
          )}
          {!selectedPersona && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>👤</span>
                <p>Select a persona or create a new one</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Template Modal */}
      {showTemplates && (
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
              <h2 style={{ margin: 0, fontSize: '20px' }}>Choose a Template</h2>
              <button
                onClick={() => setShowTemplates(false)}
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
            
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(2, 1fr)', 
              gap: '12px',
            }}>
              {PERSONA_TEMPLATES.map(template => (
                <div
                  key={template.id}
                  onClick={() => handleCreateFromTemplate(template.id)}
                  style={{
                    padding: '16px',
                    backgroundColor: COLORS.shadowMoss,
                    borderRadius: '12px',
                    cursor: 'pointer',
                    border: '2px solid transparent',
                    transition: 'border-color 0.2s',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = COLORS.sacredGold}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'transparent'}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '32px' }}>{template.icon}</span>
                    <div>
                      <div style={{ fontWeight: 600 }}>{template.name}</div>
                      <div style={{ 
                        fontSize: '11px', 
                        color: CATEGORY_COLORS[template.category],
                        textTransform: 'capitalize',
                      }}>
                        {template.category}
                      </div>
                    </div>
                  </div>
                  <p style={{ margin: 0, fontSize: '13px', color: COLORS.ancientStone }}>
                    {template.description}
                  </p>
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
          SAFE · NON-AUTONOMOUS · NO PSYCHOLOGY · Personas are representational structures only
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

interface PersonaListViewProps {
  personas: PersonaModel[];
  onSelect: (persona: PersonaModel) => void;
  selectedId?: string;
}

function PersonaListView({ personas, onSelect, selectedId }: PersonaListViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
        gap: '16px',
      }}>
        {personas.map(persona => (
          <div
            key={persona.id}
            onClick={() => onSelect(persona)}
            style={{
              padding: '20px',
              backgroundColor: selectedId === persona.id 
                ? `${COLORS.sacredGold}15` 
                : COLORS.shadowMoss,
              borderRadius: '12px',
              cursor: 'pointer',
              border: `2px solid ${selectedId === persona.id ? COLORS.sacredGold : 'transparent'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
              <span style={{ fontSize: '40px' }}>{persona.avatar_icon}</span>
              <div>
                <h3 style={{ margin: 0, fontSize: '16px' }}>{persona.name}</h3>
                <span style={{
                  fontSize: '11px',
                  padding: '2px 8px',
                  backgroundColor: `${CATEGORY_COLORS[persona.category]}20`,
                  color: CATEGORY_COLORS[persona.category],
                  borderRadius: '4px',
                  textTransform: 'capitalize',
                }}>
                  {persona.category}
                </span>
              </div>
            </div>
            
            <p style={{ 
              margin: '0 0 12px', 
              fontSize: '13px', 
              color: COLORS.ancientStone,
              lineHeight: 1.4,
            }}>
              {persona.description}
            </p>
            
            <div style={{ display: 'flex', gap: '16px', fontSize: '12px' }}>
              <span style={{ color: COLORS.earthEmber }}>
                {persona.traits.length} traits
              </span>
              <span style={{ color: COLORS.cenoteTurquoise }}>
                {persona.styles.length} styles
              </span>
              <span style={{ color: COLORS.jungleEmerald }}>
                {persona.engine_affinities.length} engines
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

interface PersonaBuilderViewProps {
  persona: PersonaModel;
  traitCatalog: Record<string, { name: string; category: string; description: string }>;
  onAddTrait: (traitKey: string, intensity: number) => void;
  onRemoveTrait: (traitId: string) => void;
}

function PersonaBuilderView({ 
  persona, 
  traitCatalog, 
  onAddTrait, 
  onRemoveTrait 
}: PersonaBuilderViewProps) {
  const [selectedTraitKey, setSelectedTraitKey] = useState<string>('');
  const [traitIntensity, setTraitIntensity] = useState(0.5);
  
  const existingTraitNames = persona.traits.map(t => t.name.toLowerCase());
  const availableTraits = Object.entries(traitCatalog).filter(
    ([key, trait]) => !existingTraitNames.includes(trait.name.toLowerCase())
  );
  
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      {/* Persona Header */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ fontSize: '56px' }}>{persona.avatar_icon}</span>
          <div>
            <h2 style={{ margin: '0 0 4px', fontSize: '24px' }}>{persona.name}</h2>
            <p style={{ margin: 0, color: COLORS.ancientStone }}>{persona.description}</p>
          </div>
        </div>
      </div>
      
      {/* Traits Section */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        marginBottom: '24px',
      }}>
        <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>
          Traits ({persona.traits.length})
        </h3>
        
        {/* Existing traits */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
          {persona.traits.map(trait => (
            <div
              key={trait.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
              }}
            >
              <span style={{ fontWeight: 500 }}>{trait.name}</span>
              <span style={{ 
                fontSize: '11px', 
                color: COLORS.sacredGold,
              }}>
                {(trait.intensity * 100).toFixed(0)}%
              </span>
              <button
                onClick={() => onRemoveTrait(trait.id)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: COLORS.ancientStone,
                  cursor: 'pointer',
                  padding: '0 4px',
                }}
              >
                ✕
              </button>
            </div>
          ))}
          {persona.traits.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
              No traits added yet
            </span>
          )}
        </div>
        
        {/* Add trait */}
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.uiSlate,
          borderRadius: '8px',
        }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '12px', marginBottom: '6px', color: COLORS.ancientStone }}>
                Select Trait
              </label>
              <select
                value={selectedTraitKey}
                onChange={(e) => setSelectedTraitKey(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px',
                  backgroundColor: COLORS.shadowMoss,
                  border: `1px solid ${COLORS.ancientStone}40`,
                  borderRadius: '6px',
                  color: COLORS.softSand,
                }}
              >
                <option value="">Choose a trait...</option>
                {availableTraits.map(([key, trait]) => (
                  <option key={key} value={key}>
                    {trait.name} ({trait.category})
                  </option>
                ))}
              </select>
            </div>
            <div style={{ width: '150px' }}>
              <label style={{ display: 'block', fontSize: '12px', marginBottom: '6px', color: COLORS.ancientStone }}>
                Intensity: {(traitIntensity * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min={0}
                max={100}
                value={traitIntensity * 100}
                onChange={(e) => setTraitIntensity(parseInt(e.target.value) / 100)}
                style={{ width: '100%', accentColor: COLORS.sacredGold }}
              />
            </div>
            <button
              onClick={() => {
                if (selectedTraitKey) {
                  onAddTrait(selectedTraitKey, traitIntensity);
                  setSelectedTraitKey('');
                  setTraitIntensity(0.5);
                }
              }}
              disabled={!selectedTraitKey}
              style={{
                padding: '10px 20px',
                backgroundColor: selectedTraitKey ? COLORS.sacredGold : COLORS.ancientStone,
                color: COLORS.uiSlate,
                border: 'none',
                borderRadius: '6px',
                fontWeight: 600,
                cursor: selectedTraitKey ? 'pointer' : 'not-allowed',
              }}
            >
              Add
            </button>
          </div>
        </div>
      </div>
      
      {/* Process Preferences */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
      }}>
        <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>Process Preferences</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', marginBottom: '6px', color: COLORS.ancientStone }}>
              Complexity
            </label>
            <div style={{
              padding: '10px',
              backgroundColor: COLORS.uiSlate,
              borderRadius: '6px',
              textAlign: 'center',
              textTransform: 'capitalize',
            }}>
              {persona.process_preferences.preferred_complexity}
            </div>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', marginBottom: '6px', color: COLORS.ancientStone }}>
              Pace
            </label>
            <div style={{
              padding: '10px',
              backgroundColor: COLORS.uiSlate,
              borderRadius: '6px',
              textAlign: 'center',
              textTransform: 'capitalize',
            }}>
              {persona.process_preferences.preferred_pace}
            </div>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', marginBottom: '6px', color: COLORS.ancientStone }}>
              Iteration
            </label>
            <div style={{
              padding: '10px',
              backgroundColor: COLORS.uiSlate,
              borderRadius: '6px',
              textAlign: 'center',
              textTransform: 'capitalize',
            }}>
              {persona.process_preferences.iteration_preference}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PersonaPage;

============================================================
SECTION B6 — FRONTEND: PERSONA VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/PersonaViewer.tsx

/**
 * CHE·NU Frontend — Persona Viewer Component
 * ===========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays a complete persona with all attributes.
 * 
 * @version 1.0.0
 */

import React from 'react';

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

const TRAIT_CATEGORY_COLORS: Record<string, string> = {
  cognitive: COLORS.cenoteTurquoise,
  behavioral: COLORS.sacredGold,
  communicative: COLORS.earthEmber,
  organizational: COLORS.jungleEmerald,
};

const STYLE_TYPE_COLORS: Record<string, string> = {
  workflow: COLORS.jungleEmerald,
  communication: COLORS.cenoteTurquoise,
  decision_making: COLORS.sacredGold,
  collaboration: COLORS.earthEmber,
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface PersonaTrait {
  id: string;
  name: string;
  category: 'cognitive' | 'behavioral' | 'communicative' | 'organizational';
  description: string;
  intensity: number;
}

interface PersonaStyle {
  id: string;
  name: string;
  type: 'workflow' | 'communication' | 'decision_making' | 'collaboration';
  description: string;
  preferences: string[];
}

interface DomainAffinity {
  domain: string;
  affinity_level: number;
  expertise_tags: string[];
}

interface EngineAffinity {
  engine: string;
  affinity_level: number;
  usage_frequency: 'rare' | 'occasional' | 'frequent' | 'primary';
}

interface PersonaModel {
  id: string;
  name: string;
  description: string;
  avatar_icon: string;
  category: string;
  traits: PersonaTrait[];
  styles: PersonaStyle[];
  domain_affinities: DomainAffinity[];
  engine_affinities: EngineAffinity[];
  process_preferences: {
    preferred_complexity: string;
    preferred_pace: string;
    iteration_preference: string;
  };
}

interface PersonaViewerProps {
  persona: PersonaModel;
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export function PersonaViewer({ persona }: PersonaViewerProps) {
  return (
    <div style={{ 
      padding: '24px', 
      overflowY: 'auto', 
      height: '100%',
      backgroundColor: '#16171a',
    }}>
      {/* Header Card */}
      <div style={{
        padding: '32px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '16px',
        marginBottom: '24px',
        display: 'flex',
        alignItems: 'center',
        gap: '24px',
      }}>
        <div style={{
          width: '100px',
          height: '100px',
          backgroundColor: COLORS.uiSlate,
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '48px',
        }}>
          {persona.avatar_icon}
        </div>
        <div style={{ flex: 1 }}>
          <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: 700 }}>
            {persona.name}
          </h1>
          <p style={{ margin: '0 0 12px', color: COLORS.ancientStone, lineHeight: 1.5 }}>
            {persona.description}
          </p>
          <span style={{
            display: 'inline-block',
            padding: '4px 12px',
            backgroundColor: `${COLORS.cenoteTurquoise}20`,
            color: COLORS.cenoteTurquoise,
            borderRadius: '6px',
            fontSize: '12px',
            fontWeight: 600,
            textTransform: 'capitalize',
          }}>
            {persona.category} Persona
          </span>
        </div>
      </div>
      
      {/* Grid Layout */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(2, 1fr)', 
        gap: '24px',
      }}>
        {/* Traits */}
        <div style={{
          padding: '24px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
        }}>
          <h3 style={{ 
            margin: '0 0 16px', 
            fontSize: '16px', 
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>🧠</span> Traits
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {persona.traits.map(trait => (
              <div key={trait.id} style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 600 }}>{trait.name}</span>
                  <span style={{
                    padding: '2px 8px',
                    backgroundColor: `${TRAIT_CATEGORY_COLORS[trait.category]}20`,
                    color: TRAIT_CATEGORY_COLORS[trait.category],
                    borderRadius: '4px',
                    fontSize: '10px',
                    textTransform: 'capitalize',
                  }}>
                    {trait.category}
                  </span>
                </div>
                <div style={{ 
                  height: '6px', 
                  backgroundColor: COLORS.shadowMoss,
                  borderRadius: '3px',
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${trait.intensity * 100}%`,
                    backgroundColor: COLORS.sacredGold,
                    borderRadius: '3px',
                  }} />
                </div>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  marginTop: '6px',
                  fontSize: '11px',
                  color: COLORS.ancientStone,
                }}>
                  <span>{trait.description}</span>
                  <span>{(trait.intensity * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
            {persona.traits.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No traits defined
              </div>
            )}
          </div>
        </div>
        
        {/* Styles */}
        <div style={{
          padding: '24px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
        }}>
          <h3 style={{ 
            margin: '0 0 16px', 
            fontSize: '16px', 
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>🎭</span> Work Styles
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {persona.styles.map(style => (
              <div key={style.id} style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 600 }}>{style.name}</span>
                  <span style={{
                    padding: '2px 8px',
                    backgroundColor: `${STYLE_TYPE_COLORS[style.type]}20`,
                    color: STYLE_TYPE_COLORS[style.type],
                    borderRadius: '4px',
                    fontSize: '10px',
                    textTransform: 'capitalize',
                  }}>
                    {style.type.replace('_', ' ')}
                  </span>
                </div>
                <p style={{ margin: '0 0 8px', fontSize: '12px', color: COLORS.ancientStone }}>
                  {style.description}
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                  {style.preferences.map((pref, i) => (
                    <span key={i} style={{
                      padding: '2px 6px',
                      backgroundColor: COLORS.shadowMoss,
                      borderRadius: '3px',
                      fontSize: '10px',
                    }}>
                      {pref}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {persona.styles.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No styles defined
              </div>
            )}
          </div>
        </div>
        
        {/* Domain Affinities */}
        <div style={{
          padding: '24px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
        }}>
          <h3 style={{ 
            margin: '0 0 16px', 
            fontSize: '16px', 
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>🌐</span> Domain Affinities
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {persona.domain_affinities.map(affinity => (
              <div key={affinity.domain} style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 600, textTransform: 'capitalize' }}>
                    {affinity.domain.replace('_', ' ')}
                  </span>
                  <span style={{ color: COLORS.sacredGold }}>
                    {(affinity.affinity_level * 100).toFixed(0)}%
                  </span>
                </div>
                <div style={{ 
                  height: '6px', 
                  backgroundColor: COLORS.shadowMoss,
                  borderRadius: '3px',
                  overflow: 'hidden',
                  marginBottom: '8px',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${affinity.affinity_level * 100}%`,
                    backgroundColor: COLORS.cenoteTurquoise,
                    borderRadius: '3px',
                  }} />
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                  {affinity.expertise_tags.map((tag, i) => (
                    <span key={i} style={{
                      padding: '2px 6px',
                      backgroundColor: `${COLORS.cenoteTurquoise}15`,
                      color: COLORS.cenoteTurquoise,
                      borderRadius: '3px',
                      fontSize: '10px',
                    }}>
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {persona.domain_affinities.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No domain affinities defined
              </div>
            )}
          </div>
        </div>
        
        {/* Engine Affinities */}
        <div style={{
          padding: '24px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
        }}>
          <h3 style={{ 
            margin: '0 0 16px', 
            fontSize: '16px', 
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>⚙️</span> Engine Affinities
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {persona.engine_affinities.map(affinity => {
              const frequencyColors: Record<string, string> = {
                primary: COLORS.sacredGold,
                frequent: COLORS.jungleEmerald,
                occasional: COLORS.cenoteTurquoise,
                rare: COLORS.ancientStone,
              };
              
              return (
                <div key={affinity.engine} style={{
                  padding: '12px',
                  backgroundColor: COLORS.uiSlate,
                  borderRadius: '8px',
                  borderLeft: `3px solid ${frequencyColors[affinity.usage_frequency]}`,
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600 }}>
                      {affinity.engine.replace('Engine', '')}
                    </span>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      <span style={{ 
                        fontSize: '11px', 
                        color: frequencyColors[affinity.usage_frequency],
                        textTransform: 'capitalize',
                      }}>
                        {affinity.usage_frequency}
                      </span>
                      <span style={{ 
                        color: COLORS.sacredGold,
                        fontSize: '13px',
                      }}>
                        {(affinity.affinity_level * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
            {persona.engine_affinities.length === 0 && (
              <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>
                No engine affinities defined
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Process Preferences */}
      <div style={{
        padding: '24px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        marginTop: '24px',
      }}>
        <h3 style={{ 
          margin: '0 0 16px', 
          fontSize: '16px', 
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}>
          <span>⚡</span> Process Preferences
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div style={{
            padding: '16px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
              Complexity
            </div>
            <div style={{ fontSize: '18px', fontWeight: 600, textTransform: 'capitalize' }}>
              {persona.process_preferences.preferred_complexity}
            </div>
          </div>
          <div style={{
            padding: '16px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
              Pace
            </div>
            <div style={{ fontSize: '18px', fontWeight: 600, textTransform: 'capitalize' }}>
              {persona.process_preferences.preferred_pace}
            </div>
          </div>
          <div style={{
            padding: '16px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
              Iteration
            </div>
            <div style={{ fontSize: '18px', fontWeight: 600, textTransform: 'capitalize' }}>
              {persona.process_preferences.iteration_preference}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PersonaViewer;

============================================================
END OF PERSONA LAYER FRONTEND
============================================================
