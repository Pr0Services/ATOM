############################################################
#                                                          #
#       CHE·NU OBJECT LAYER + KNOWLEDGE GRAPH LAYER        #
#       PART 2: OBJECT SCHEMA + FRONTEND                   #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A3 — OBJECT SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/object.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/object.schema.json",
  "title": "CHE·NU Object Schema",
  "description": "JSON Schema for CHE·NU representational objects and resources",
  "type": "object",
  "required": ["id", "name", "type", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique object identifier",
      "pattern": "^obj_[a-z0-9-]+_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Object display name",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Object description",
      "maxLength": 2000
    },
    "type": {
      "type": "string",
      "description": "Object type classification",
      "enum": [
        "document",
        "tool",
        "asset",
        "xr-object",
        "concept",
        "template",
        "component",
        "media",
        "link",
        "data",
        "reference",
        "artifact",
        "custom"
      ]
    },
    "subtype": {
      "type": "string",
      "description": "Optional subtype for further classification",
      "maxLength": 100
    },
    "sphereTags": {
      "type": "array",
      "description": "Spheres this object is relevant to",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "projectIds": {
      "type": "array",
      "description": "Linked project identifiers",
      "items": {
        "type": "string",
        "pattern": "^proj_[a-z0-9]+_[a-z0-9]+$"
      },
      "uniqueItems": true
    },
    "missionIds": {
      "type": "array",
      "description": "Linked mission identifiers",
      "items": {
        "type": "string",
        "pattern": "^miss_[a-z0-9]+_[a-z0-9]+$"
      },
      "uniqueItems": true
    },
    "ownerAgentIds": {
      "type": "array",
      "description": "Owner agent identifiers",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "engineRefs": {
      "type": "array",
      "description": "Referenced engine identifiers",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "status": {
      "type": "string",
      "description": "Object status",
      "enum": ["active", "archived", "draft", "deprecated", "pending"],
      "default": "active"
    },
    "visibility": {
      "type": "string",
      "description": "Object visibility level",
      "enum": ["private", "shared", "public", "restricted"],
      "default": "private"
    },
    "tags": {
      "type": "array",
      "description": "Object tags for categorization",
      "items": {
        "type": "string",
        "maxLength": 50
      },
      "uniqueItems": true
    },
    "categories": {
      "type": "array",
      "description": "Object categories",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "content": {
      "$ref": "#/definitions/object_content"
    },
    "metadata": {
      "$ref": "#/definitions/object_metadata"
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "object_content": {
      "type": "object",
      "description": "Object content representation",
      "properties": {
        "format": {
          "type": "string",
          "description": "Content format (e.g., json, markdown, binary-ref)"
        },
        "schema": {
          "type": "string",
          "description": "Optional schema reference"
        },
        "preview": {
          "type": "string",
          "description": "Short preview text",
          "maxLength": 500
        },
        "size": {
          "type": "string",
          "description": "Representational size"
        },
        "checksum": {
          "type": "string",
          "description": "Representational checksum"
        },
        "properties": {
          "type": "object",
          "description": "Additional content properties",
          "additionalProperties": true
        }
      }
    },
    "object_metadata": {
      "type": "object",
      "description": "Object metadata",
      "required": ["created_at", "updated_at", "version"],
      "properties": {
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Creation timestamp"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Last update timestamp"
        },
        "version": {
          "type": "string",
          "description": "Object version",
          "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        },
        "author": {
          "type": "string",
          "description": "Object author"
        },
        "source": {
          "type": "string",
          "description": "Object source"
        },
        "license": {
          "type": "string",
          "description": "Object license"
        },
        "custom": {
          "type": "object",
          "description": "Custom metadata fields",
          "additionalProperties": true
        }
      }
    },
    "safe_compliance": {
      "type": "object",
      "description": "SAFE compliance markers",
      "required": ["isRepresentational", "noAutonomy", "noExecution", "noPersistence"],
      "properties": {
        "isRepresentational": {
          "type": "boolean",
          "const": true,
          "description": "Object is representational only"
        },
        "noAutonomy": {
          "type": "boolean",
          "const": true,
          "description": "No autonomous behavior"
        },
        "noExecution": {
          "type": "boolean",
          "const": true,
          "description": "No execution capability"
        },
        "noPersistence": {
          "type": "boolean",
          "const": true,
          "description": "No persistent storage"
        }
      }
    }
  },
  "additionalProperties": false
}

============================================================
SECTION A6 — FRONTEND: OBJECTS PAGE
============================================================

--- FILE: /che-nu-frontend/pages/objects.tsx

/**
 * CHE·NU Frontend — Objects & Resources Page
 * ===========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays and manages CHE·NU objects and resources.
 * All data is representational only.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { ObjectViewer } from '../components/ObjectViewer';

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

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface CheNuObject {
  id: string;
  name: string;
  description: string;
  type: string;
  subtype?: string;
  sphereTags: string[];
  projectIds: string[];
  missionIds: string[];
  ownerAgentIds: string[];
  engineRefs: string[];
  status: string;
  visibility: string;
  tags: string[];
  categories: string[];
  content: {
    format: string;
    preview?: string;
    size?: string;
    properties: Record<string, unknown>;
  };
  metadata: {
    created_at: string;
    updated_at: string;
    version: string;
    author?: string;
    source?: string;
  };
}

// ============================================================
// SAMPLE DATA (REPRESENTATIONAL ONLY)
// ============================================================

const SAMPLE_OBJECTS: CheNuObject[] = [
  {
    id: 'obj_document_abc123_def456',
    name: 'CHE·NU Architecture Document',
    description: 'Main architecture documentation for CHE·NU platform',
    type: 'document',
    subtype: 'markdown',
    sphereTags: ['Scholar', 'Projets'],
    projectIds: ['proj_chenu_abc123'],
    missionIds: [],
    ownerAgentIds: ['DocumentSpecialist'],
    engineRefs: ['KnowledgeEngine', 'ContentEngine'],
    status: 'active',
    visibility: 'shared',
    tags: ['documentation', 'architecture', 'technical'],
    categories: ['Technical Docs'],
    content: {
      format: 'markdown',
      preview: '# CHE·NU Architecture\n\nThis document describes...',
      size: '45 KB',
      properties: { wordCount: 8500, sections: 12 },
    },
    metadata: {
      created_at: '2024-11-01T10:00:00Z',
      updated_at: '2024-12-10T15:30:00Z',
      version: '2.1.0',
      author: 'Jo',
      source: 'internal',
    },
  },
  {
    id: 'obj_xr-object_xyz789_ghi012',
    name: 'Nova 3D Avatar Model',
    description: '3D avatar model for Nova AI assistant',
    type: 'xr-object',
    subtype: '3d-model',
    sphereTags: ['Creative', 'XR'],
    projectIds: ['proj_chenu_abc123'],
    missionIds: ['miss_avatar_abc'],
    ownerAgentIds: ['NovaArchitect', 'XRSceneBuilder'],
    engineRefs: ['XRSceneEngine', 'CreativityEngine'],
    status: 'active',
    visibility: 'public',
    tags: ['avatar', '3d', 'nova', 'xr'],
    categories: ['XR Assets', 'Avatars'],
    content: {
      format: 'glb',
      preview: '[3D Model Preview]',
      size: '2.3 MB',
      properties: { polygons: 25000, textures: 4, animations: 8 },
    },
    metadata: {
      created_at: '2024-10-15T08:00:00Z',
      updated_at: '2024-12-08T12:00:00Z',
      version: '1.5.0',
      author: 'Creative Team',
    },
  },
  {
    id: 'obj_tool_tool123_jkl345',
    name: 'Project Estimation Calculator',
    description: 'Tool for estimating project timelines and resources',
    type: 'tool',
    subtype: 'calculator',
    sphereTags: ['Business', 'Projets'],
    projectIds: [],
    missionIds: [],
    ownerAgentIds: ['ProjectManager'],
    engineRefs: ['ProjectEngine', 'AnalysisEngine'],
    status: 'active',
    visibility: 'shared',
    tags: ['estimation', 'calculator', 'project'],
    categories: ['Tools', 'Project Management'],
    content: {
      format: 'json',
      preview: '{"type": "estimation_tool", ...}',
      size: '12 KB',
      properties: { inputFields: 8, outputMetrics: 5 },
    },
    metadata: {
      created_at: '2024-09-20T14:00:00Z',
      updated_at: '2024-11-25T09:00:00Z',
      version: '1.2.0',
    },
  },
  {
    id: 'obj_concept_con456_mno789',
    name: 'Decision Matrix Framework',
    description: 'Conceptual framework for structured decision making',
    type: 'concept',
    subtype: 'framework',
    sphereTags: ['Scholar', 'Personal'],
    projectIds: [],
    missionIds: ['miss_decision_xyz'],
    ownerAgentIds: ['StrategicAdvisor', 'MethodologyExpert'],
    engineRefs: ['DecisionEngine', 'MethodologyEngine'],
    status: 'active',
    visibility: 'public',
    tags: ['decision', 'framework', 'matrix', 'methodology'],
    categories: ['Concepts', 'Methodologies'],
    content: {
      format: 'json',
      preview: '{"framework": "decision_matrix", ...}',
      size: '8 KB',
      properties: { criteria: 6, weightingScheme: 'normalized' },
    },
    metadata: {
      created_at: '2024-08-10T16:00:00Z',
      updated_at: '2024-12-01T10:00:00Z',
      version: '1.0.0',
    },
  },
  {
    id: 'obj_media_med123_pqr456',
    name: 'CHE·NU Brand Logo Pack',
    description: 'Official brand logos in various formats and sizes',
    type: 'media',
    subtype: 'image',
    sphereTags: ['Creative', 'Business'],
    projectIds: ['proj_chenu_abc123'],
    missionIds: [],
    ownerAgentIds: ['CreativeDirector'],
    engineRefs: ['ContentEngine'],
    status: 'active',
    visibility: 'public',
    tags: ['logo', 'brand', 'identity', 'media'],
    categories: ['Brand Assets', 'Media'],
    content: {
      format: 'svg',
      preview: '[Logo Preview]',
      size: '156 KB',
      properties: { variants: 8, formats: ['svg', 'png', 'ico'] },
    },
    metadata: {
      created_at: '2024-07-01T12:00:00Z',
      updated_at: '2024-10-15T18:00:00Z',
      version: '2.0.0',
      license: 'Proprietary',
    },
  },
  {
    id: 'obj_data_data789_stu012',
    name: 'Agent Performance Metrics Dataset',
    description: 'Historical performance data for CHE·NU agents',
    type: 'data',
    subtype: 'dataset',
    sphereTags: ['Business', 'Projets'],
    projectIds: ['proj_chenu_abc123'],
    missionIds: [],
    ownerAgentIds: ['DataAnalyst'],
    engineRefs: ['DataEngine', 'AnalysisEngine'],
    status: 'active',
    visibility: 'restricted',
    tags: ['metrics', 'performance', 'agents', 'analytics'],
    categories: ['Datasets', 'Analytics'],
    content: {
      format: 'json',
      preview: '{"records": 15000, "fields": [...]}',
      size: '3.2 MB',
      properties: { records: 15000, fields: 24, timeRange: '12 months' },
    },
    metadata: {
      created_at: '2024-06-15T08:00:00Z',
      updated_at: '2024-12-12T06:00:00Z',
      version: '1.8.0',
    },
  },
];

// ============================================================
// HELPER COMPONENTS
// ============================================================

const TYPE_ICONS: Record<string, string> = {
  document: '📄',
  tool: '🔧',
  asset: '📦',
  'xr-object': '🥽',
  concept: '💡',
  template: '📋',
  component: '🧩',
  media: '🖼️',
  link: '🔗',
  data: '📊',
  reference: '📚',
  artifact: '🏺',
  custom: '⚙️',
};

const STATUS_COLORS: Record<string, string> = {
  active: COLORS.jungleEmerald,
  archived: COLORS.ancientStone,
  draft: COLORS.sacredGold,
  deprecated: COLORS.earthEmber,
  pending: COLORS.cenoteTurquoise,
};

const VISIBILITY_ICONS: Record<string, string> = {
  private: '🔒',
  shared: '👥',
  public: '🌐',
  restricted: '⚠️',
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function ObjectsPage() {
  const [selectedObject, setSelectedObject] = useState<CheNuObject | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterSphere, setFilterSphere] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  
  // Get unique values for filters
  const objectTypes = useMemo(() => {
    const types = new Set(SAMPLE_OBJECTS.map(o => o.type));
    return ['all', ...Array.from(types)];
  }, []);
  
  const spheres = useMemo(() => {
    const all = new Set<string>();
    SAMPLE_OBJECTS.forEach(o => o.sphereTags.forEach(s => all.add(s)));
    return ['all', ...Array.from(all)];
  }, []);
  
  // Filter objects
  const filteredObjects = useMemo(() => {
    return SAMPLE_OBJECTS.filter(obj => {
      // Search filter
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        const matchesSearch = 
          obj.name.toLowerCase().includes(term) ||
          obj.description.toLowerCase().includes(term) ||
          obj.tags.some(t => t.toLowerCase().includes(term));
        if (!matchesSearch) return false;
      }
      
      // Type filter
      if (filterType !== 'all' && obj.type !== filterType) {
        return false;
      }
      
      // Sphere filter
      if (filterSphere !== 'all' && !obj.sphereTags.includes(filterSphere)) {
        return false;
      }
      
      // Status filter
      if (filterStatus !== 'all' && obj.status !== filterStatus) {
        return false;
      }
      
      return true;
    });
  }, [searchTerm, filterType, filterSphere, filterStatus]);
  
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
              <span>📦</span>
              Objects & Resources
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Representational objects, assets, and resources
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button style={{
              padding: '10px 20px',
              backgroundColor: COLORS.sacredGold,
              color: COLORS.uiSlate,
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
            }}>
              + Create Object
            </button>
          </div>
        </div>
        
        {/* Filters */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '16px', 
          flexWrap: 'wrap',
          alignItems: 'center',
        }}>
          {/* Search */}
          <input
            type="text"
            placeholder="Search objects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
              minWidth: '250px',
            }}
          />
          
          {/* Type Filter */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
            }}
          >
            {objectTypes.map(type => (
              <option key={type} value={type}>
                {type === 'all' ? 'All Types' : `${TYPE_ICONS[type] || '📦'} ${type}`}
              </option>
            ))}
          </select>
          
          {/* Sphere Filter */}
          <select
            value={filterSphere}
            onChange={(e) => setFilterSphere(e.target.value)}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
            }}
          >
            {spheres.map(sphere => (
              <option key={sphere} value={sphere}>
                {sphere === 'all' ? 'All Spheres' : sphere}
              </option>
            ))}
          </select>
          
          {/* Status Filter */}
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
            }}
          >
            <option value="all">All Statuses</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
            <option value="archived">Archived</option>
            <option value="deprecated">Deprecated</option>
            <option value="pending">Pending</option>
          </select>
          
          {/* Results count */}
          <span style={{ color: COLORS.ancientStone, fontSize: '14px' }}>
            {filteredObjects.length} objects
          </span>
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ 
        flex: 1, 
        display: 'flex', 
        overflow: 'hidden',
      }}>
        {/* Object List */}
        <div style={{
          flex: selectedObject ? '0 0 400px' : 1,
          overflowY: 'auto',
          padding: '20px',
          borderRight: selectedObject ? `1px solid ${COLORS.shadowMoss}` : 'none',
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: selectedObject ? '1fr' : 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '16px',
          }}>
            {filteredObjects.map(obj => (
              <ObjectCard
                key={obj.id}
                object={obj}
                isSelected={selectedObject?.id === obj.id}
                onClick={() => setSelectedObject(obj)}
              />
            ))}
          </div>
          
          {filteredObjects.length === 0 && (
            <div style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: COLORS.ancientStone,
            }}>
              <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>📭</span>
              <p>No objects match your filters</p>
            </div>
          )}
        </div>
        
        {/* Object Viewer */}
        {selectedObject && (
          <div style={{ flex: 1, overflowY: 'auto' }}>
            <ObjectViewer
              object={selectedObject}
              onClose={() => setSelectedObject(null)}
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
          SAFE · NON-AUTONOMOUS · All objects are representational structures only — no actual file system access
        </span>
      </div>
    </div>
  );
}

// ============================================================
// OBJECT CARD COMPONENT
// ============================================================

interface ObjectCardProps {
  object: CheNuObject;
  isSelected: boolean;
  onClick: () => void;
}

function ObjectCard({ object, isSelected, onClick }: ObjectCardProps) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: '16px',
        backgroundColor: isSelected ? `${COLORS.sacredGold}20` : COLORS.shadowMoss,
        border: `2px solid ${isSelected ? COLORS.sacredGold : 'transparent'}`,
        borderRadius: '12px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      }}
    >
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'flex-start',
        marginBottom: '12px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '24px' }}>{TYPE_ICONS[object.type] || '📦'}</span>
          <div>
            <h3 style={{ 
              margin: 0, 
              fontSize: '15px', 
              fontWeight: 600,
              color: COLORS.softSand,
            }}>
              {object.name}
            </h3>
            <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>
              {object.type}{object.subtype ? ` / ${object.subtype}` : ''}
            </span>
          </div>
        </div>
        <span style={{ fontSize: '16px' }}>{VISIBILITY_ICONS[object.visibility]}</span>
      </div>
      
      {/* Description */}
      <p style={{
        margin: '0 0 12px',
        fontSize: '13px',
        color: COLORS.ancientStone,
        lineHeight: 1.4,
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        display: '-webkit-box',
        WebkitLineClamp: 2,
        WebkitBoxOrient: 'vertical',
      }}>
        {object.description}
      </p>
      
      {/* Sphere Tags */}
      <div style={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: '6px',
        marginBottom: '12px',
      }}>
        {object.sphereTags.map(sphere => (
          <span
            key={sphere}
            style={{
              padding: '4px 8px',
              backgroundColor: `${COLORS.cenoteTurquoise}20`,
              color: COLORS.cenoteTurquoise,
              borderRadius: '4px',
              fontSize: '11px',
              fontWeight: 500,
            }}
          >
            {sphere}
          </span>
        ))}
      </div>
      
      {/* Footer */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: '12px',
        borderTop: `1px solid ${COLORS.uiSlate}`,
      }}>
        <span
          style={{
            padding: '4px 10px',
            backgroundColor: `${STATUS_COLORS[object.status]}20`,
            color: STATUS_COLORS[object.status],
            borderRadius: '4px',
            fontSize: '11px',
            fontWeight: 600,
          }}
        >
          {object.status}
        </span>
        
        <div style={{ 
          display: 'flex', 
          gap: '12px', 
          fontSize: '11px', 
          color: COLORS.ancientStone,
        }}>
          {object.projectIds.length > 0 && (
            <span>📋 {object.projectIds.length}</span>
          )}
          {object.missionIds.length > 0 && (
            <span>🎯 {object.missionIds.length}</span>
          )}
          {object.ownerAgentIds.length > 0 && (
            <span>🤖 {object.ownerAgentIds.length}</span>
          )}
        </div>
      </div>
    </div>
  );
}

export default ObjectsPage;

============================================================
SECTION A6 (cont.) — OBJECT VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/ObjectViewer.tsx

/**
 * CHE·NU Frontend — Object Viewer Component
 * ==========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays detailed view of a CHE·NU object.
 * 
 * @version 1.0.0
 */

import React, { useState } from 'react';

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

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface CheNuObject {
  id: string;
  name: string;
  description: string;
  type: string;
  subtype?: string;
  sphereTags: string[];
  projectIds: string[];
  missionIds: string[];
  ownerAgentIds: string[];
  engineRefs: string[];
  status: string;
  visibility: string;
  tags: string[];
  categories: string[];
  content: {
    format: string;
    preview?: string;
    size?: string;
    properties: Record<string, unknown>;
  };
  metadata: {
    created_at: string;
    updated_at: string;
    version: string;
    author?: string;
    source?: string;
    license?: string;
  };
}

interface ObjectViewerProps {
  object: CheNuObject;
  onClose: () => void;
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

const TYPE_ICONS: Record<string, string> = {
  document: '📄',
  tool: '🔧',
  asset: '📦',
  'xr-object': '🥽',
  concept: '💡',
  template: '📋',
  component: '🧩',
  media: '🖼️',
  link: '🔗',
  data: '📊',
  reference: '📚',
  artifact: '🏺',
  custom: '⚙️',
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function ObjectViewer({ object, onClose }: ObjectViewerProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'content' | 'links' | 'metadata'>('overview');
  
  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'content', label: 'Content', icon: '📝' },
    { id: 'links', label: 'Links', icon: '🔗' },
    { id: 'metadata', label: 'Metadata', icon: '📋' },
  ];
  
  return (
    <div style={{
      padding: '24px',
      backgroundColor: COLORS.uiSlate,
      minHeight: '100%',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <span style={{ fontSize: '40px' }}>{TYPE_ICONS[object.type] || '📦'}</span>
          <div>
            <h2 style={{ margin: 0, fontSize: '22px', fontWeight: 700, color: COLORS.softSand }}>
              {object.name}
            </h2>
            <p style={{ margin: '4px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              {object.type}{object.subtype ? ` / ${object.subtype}` : ''} • v{object.metadata.version}
            </p>
          </div>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '8px 16px',
            backgroundColor: 'transparent',
            border: `1px solid ${COLORS.ancientStone}40`,
            borderRadius: '6px',
            color: COLORS.softSand,
            cursor: 'pointer',
          }}
        >
          ✕ Close
        </button>
      </div>
      
      {/* Description */}
      <p style={{
        margin: '0 0 24px',
        padding: '16px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '8px',
        color: COLORS.softSand,
        lineHeight: 1.6,
      }}>
        {object.description}
      </p>
      
      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '24px',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
        paddingBottom: '8px',
      }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as typeof activeTab)}
            style={{
              padding: '10px 16px',
              backgroundColor: activeTab === tab.id ? COLORS.shadowMoss : 'transparent',
              border: 'none',
              borderRadius: '6px 6px 0 0',
              color: activeTab === tab.id ? COLORS.sacredGold : COLORS.ancientStone,
              fontWeight: activeTab === tab.id ? 600 : 400,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      {activeTab === 'overview' && (
        <OverviewTab object={object} />
      )}
      
      {activeTab === 'content' && (
        <ContentTab object={object} />
      )}
      
      {activeTab === 'links' && (
        <LinksTab object={object} />
      )}
      
      {activeTab === 'metadata' && (
        <MetadataTab object={object} />
      )}
      
      {/* Action Buttons */}
      <div style={{
        marginTop: '32px',
        paddingTop: '20px',
        borderTop: `1px solid ${COLORS.shadowMoss}`,
        display: 'flex',
        gap: '12px',
        flexWrap: 'wrap',
      }}>
        <ActionButton label="View Context Map" icon="🗺️" color={COLORS.cenoteTurquoise} />
        <ActionButton label="Link to Project" icon="📋" color={COLORS.sacredGold} />
        <ActionButton label="Link to Mission" icon="🎯" color={COLORS.jungleEmerald} />
        <ActionButton label="Export Structure" icon="📤" color={COLORS.ancientStone} />
      </div>
    </div>
  );
}

// ============================================================
// TAB COMPONENTS
// ============================================================

function OverviewTab({ object }: { object: CheNuObject }) {
  return (
    <div>
      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <StatCard label="Projects" value={object.projectIds.length} icon="📋" />
        <StatCard label="Missions" value={object.missionIds.length} icon="🎯" />
        <StatCard label="Agents" value={object.ownerAgentIds.length} icon="🤖" />
        <StatCard label="Engines" value={object.engineRefs.length} icon="⚙️" />
      </div>
      
      {/* Status & Visibility */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          <h4 style={{ margin: '0 0 8px', color: COLORS.ancientStone, fontSize: '12px' }}>STATUS</h4>
          <span style={{
            padding: '6px 12px',
            backgroundColor: `${COLORS.jungleEmerald}20`,
            color: COLORS.jungleEmerald,
            borderRadius: '4px',
            fontWeight: 600,
          }}>
            {object.status.toUpperCase()}
          </span>
        </div>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          <h4 style={{ margin: '0 0 8px', color: COLORS.ancientStone, fontSize: '12px' }}>VISIBILITY</h4>
          <span style={{
            padding: '6px 12px',
            backgroundColor: `${COLORS.cenoteTurquoise}20`,
            color: COLORS.cenoteTurquoise,
            borderRadius: '4px',
            fontWeight: 600,
          }}>
            {object.visibility.toUpperCase()}
          </span>
        </div>
      </div>
      
      {/* Spheres */}
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{ margin: '0 0 12px', color: COLORS.softSand, fontSize: '14px' }}>Spheres</h4>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {object.sphereTags.map(sphere => (
            <span
              key={sphere}
              style={{
                padding: '8px 16px',
                backgroundColor: `${COLORS.sacredGold}20`,
                color: COLORS.sacredGold,
                borderRadius: '6px',
                fontWeight: 500,
              }}
            >
              {sphere}
            </span>
          ))}
        </div>
      </div>
      
      {/* Tags */}
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{ margin: '0 0 12px', color: COLORS.softSand, fontSize: '14px' }}>Tags</h4>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {object.tags.map(tag => (
            <span
              key={tag}
              style={{
                padding: '6px 12px',
                backgroundColor: COLORS.shadowMoss,
                color: COLORS.ancientStone,
                borderRadius: '4px',
                fontSize: '13px',
              }}
            >
              #{tag}
            </span>
          ))}
        </div>
      </div>
      
      {/* Categories */}
      {object.categories.length > 0 && (
        <div>
          <h4 style={{ margin: '0 0 12px', color: COLORS.softSand, fontSize: '14px' }}>Categories</h4>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {object.categories.map(cat => (
              <span
                key={cat}
                style={{
                  padding: '6px 12px',
                  backgroundColor: `${COLORS.jungleEmerald}15`,
                  color: COLORS.jungleEmerald,
                  borderRadius: '4px',
                  fontSize: '13px',
                }}
              >
                📁 {cat}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ContentTab({ object }: { object: CheNuObject }) {
  return (
    <div>
      {/* Content Info */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          <h4 style={{ margin: '0 0 8px', color: COLORS.ancientStone, fontSize: '12px' }}>FORMAT</h4>
          <span style={{ color: COLORS.softSand, fontWeight: 600 }}>{object.content.format}</span>
        </div>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          <h4 style={{ margin: '0 0 8px', color: COLORS.ancientStone, fontSize: '12px' }}>SIZE</h4>
          <span style={{ color: COLORS.softSand, fontWeight: 600 }}>{object.content.size || 'N/A'}</span>
        </div>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          <h4 style={{ margin: '0 0 8px', color: COLORS.ancientStone, fontSize: '12px' }}>VERSION</h4>
          <span style={{ color: COLORS.softSand, fontWeight: 600 }}>{object.metadata.version}</span>
        </div>
      </div>
      
      {/* Preview */}
      {object.content.preview && (
        <div style={{ marginBottom: '24px' }}>
          <h4 style={{ margin: '0 0 12px', color: COLORS.softSand, fontSize: '14px' }}>Preview</h4>
          <div style={{
            padding: '16px',
            backgroundColor: '#0d0d0d',
            borderRadius: '8px',
            fontFamily: 'monospace',
            fontSize: '13px',
            color: COLORS.ancientStone,
            whiteSpace: 'pre-wrap',
            overflow: 'auto',
            maxHeight: '200px',
          }}>
            {object.content.preview}
          </div>
        </div>
      )}
      
      {/* Properties */}
      <div>
        <h4 style={{ margin: '0 0 12px', color: COLORS.softSand, fontSize: '14px' }}>Content Properties</h4>
        <div style={{
          padding: '16px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '8px',
        }}>
          {Object.entries(object.content.properties).map(([key, value]) => (
            <div
              key={key}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '8px 0',
                borderBottom: `1px solid ${COLORS.uiSlate}`,
              }}
            >
              <span style={{ color: COLORS.ancientStone }}>{key}</span>
              <span style={{ color: COLORS.softSand, fontWeight: 500 }}>
                {typeof value === 'object' ? JSON.stringify(value) : String(value)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function LinksTab({ object }: { object: CheNuObject }) {
  return (
    <div>
      {/* Projects */}
      <LinkSection
        title="Linked Projects"
        icon="📋"
        items={object.projectIds}
        emptyMessage="No projects linked"
        color={COLORS.sacredGold}
      />
      
      {/* Missions */}
      <LinkSection
        title="Linked Missions"
        icon="🎯"
        items={object.missionIds}
        emptyMessage="No missions linked"
        color={COLORS.cenoteTurquoise}
      />
      
      {/* Agents */}
      <LinkSection
        title="Owner Agents"
        icon="🤖"
        items={object.ownerAgentIds}
        emptyMessage="No agents assigned"
        color={COLORS.jungleEmerald}
      />
      
      {/* Engines */}
      <LinkSection
        title="Referenced Engines"
        icon="⚙️"
        items={object.engineRefs}
        emptyMessage="No engines referenced"
        color={COLORS.earthEmber}
      />
    </div>
  );
}

function MetadataTab({ object }: { object: CheNuObject }) {
  return (
    <div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <MetaField label="Object ID" value={object.id} />
        <MetaField label="Version" value={object.metadata.version} />
        <MetaField label="Created" value={formatDate(object.metadata.created_at)} />
        <MetaField label="Updated" value={formatDate(object.metadata.updated_at)} />
        <MetaField label="Author" value={object.metadata.author || 'N/A'} />
        <MetaField label="Source" value={object.metadata.source || 'N/A'} />
        <MetaField label="License" value={object.metadata.license || 'N/A'} />
      </div>
      
      {/* SAFE Compliance */}
      <div style={{
        padding: '16px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderRadius: '8px',
        border: `1px solid ${COLORS.jungleEmerald}30`,
      }}>
        <h4 style={{ margin: '0 0 12px', color: COLORS.jungleEmerald, fontSize: '14px' }}>
          🔒 SAFE Compliance
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
          <SafeBadge label="Representational" checked />
          <SafeBadge label="No Autonomy" checked />
          <SafeBadge label="No Execution" checked />
          <SafeBadge label="No Persistence" checked />
        </div>
      </div>
    </div>
  );
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

function StatCard({ label, value, icon }: { label: string; value: number; icon: string }) {
  return (
    <div style={{
      padding: '16px',
      backgroundColor: COLORS.shadowMoss,
      borderRadius: '8px',
      textAlign: 'center',
    }}>
      <span style={{ fontSize: '24px', display: 'block', marginBottom: '8px' }}>{icon}</span>
      <span style={{ 
        fontSize: '24px', 
        fontWeight: 700, 
        color: COLORS.softSand,
        display: 'block',
      }}>
        {value}
      </span>
      <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>{label}</span>
    </div>
  );
}

function ActionButton({ label, icon, color }: { label: string; icon: string; color: string }) {
  return (
    <button style={{
      padding: '10px 16px',
      backgroundColor: `${color}20`,
      border: `1px solid ${color}40`,
      borderRadius: '6px',
      color: color,
      fontWeight: 500,
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    }}>
      <span>{icon}</span>
      {label}
    </button>
  );
}

function LinkSection({ 
  title, 
  icon, 
  items, 
  emptyMessage, 
  color 
}: { 
  title: string; 
  icon: string; 
  items: string[]; 
  emptyMessage: string;
  color: string;
}) {
  return (
    <div style={{ marginBottom: '24px' }}>
      <h4 style={{ 
        margin: '0 0 12px', 
        color: COLORS.softSand, 
        fontSize: '14px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
      }}>
        <span>{icon}</span>
        {title}
        <span style={{ color: COLORS.ancientStone }}>({items.length})</span>
      </h4>
      {items.length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {items.map(item => (
            <div
              key={item}
              style={{
                padding: '12px 16px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                borderLeft: `3px solid ${color}`,
                color: COLORS.softSand,
                fontSize: '13px',
                fontFamily: 'monospace',
              }}
            >
              {item}
            </div>
          ))}
        </div>
      ) : (
        <p style={{ color: COLORS.ancientStone, fontStyle: 'italic', margin: 0 }}>
          {emptyMessage}
        </p>
      )}
    </div>
  );
}

function MetaField({ label, value }: { label: string; value: string }) {
  return (
    <div style={{
      padding: '12px 16px',
      backgroundColor: COLORS.shadowMoss,
      borderRadius: '6px',
    }}>
      <span style={{ 
        display: 'block', 
        fontSize: '11px', 
        color: COLORS.ancientStone,
        marginBottom: '4px',
        textTransform: 'uppercase',
      }}>
        {label}
      </span>
      <span style={{ 
        color: COLORS.softSand, 
        fontSize: '13px',
        fontFamily: value.startsWith('obj_') ? 'monospace' : 'inherit',
        wordBreak: 'break-all',
      }}>
        {value}
      </span>
    </div>
  );
}

function SafeBadge({ label, checked }: { label: string; checked: boolean }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      color: checked ? COLORS.jungleEmerald : COLORS.ancientStone,
    }}>
      <span>{checked ? '✓' : '○'}</span>
      <span style={{ fontSize: '13px' }}>{label}</span>
    </div>
  );
}

function formatDate(isoString: string): string {
  return new Date(isoString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default ObjectViewer;
