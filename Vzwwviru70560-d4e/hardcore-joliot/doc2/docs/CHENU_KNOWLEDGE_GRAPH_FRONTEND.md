############################################################
#                                                          #
#       CHE·NU OBJECT LAYER + KNOWLEDGE GRAPH LAYER        #
#       PART 4: KNOWLEDGE GRAPH SCHEMA + FRONTEND          #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION B3 — KNOWLEDGE GRAPH SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/knowledge_graph.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/knowledge_graph.schema.json",
  "title": "CHE·NU Knowledge Graph Schema",
  "description": "JSON Schema for CHE·NU global knowledge graph structures",
  "type": "object",
  "required": ["id", "name", "nodes", "edges", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique knowledge graph identifier",
      "pattern": "^kg_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Knowledge graph name",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Knowledge graph description",
      "maxLength": 2000
    },
    "nodes": {
      "type": "array",
      "description": "Graph nodes",
      "items": {
        "$ref": "#/definitions/graph_node"
      }
    },
    "edges": {
      "type": "array",
      "description": "Graph edges/relationships",
      "items": {
        "$ref": "#/definitions/graph_edge"
      }
    },
    "statistics": {
      "$ref": "#/definitions/graph_statistics"
    },
    "metadata": {
      "$ref": "#/definitions/graph_metadata"
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "graph_node": {
      "type": "object",
      "required": ["id", "type", "label"],
      "properties": {
        "id": {
          "type": "string",
          "description": "Node identifier",
          "pattern": "^gn_[a-z]+_[a-z0-9]+_[a-z0-9]+$"
        },
        "type": {
          "type": "string",
          "description": "Node type",
          "enum": [
            "sphere",
            "project",
            "mission",
            "agent",
            "engine",
            "object",
            "domain",
            "concept",
            "user",
            "workflow"
          ]
        },
        "label": {
          "type": "string",
          "description": "Node display label"
        },
        "properties": {
          "type": "object",
          "description": "Node properties",
          "additionalProperties": true
        },
        "metadata": {
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
            "weight": {
              "type": "number",
              "minimum": 0,
              "maximum": 1
            }
          }
        }
      }
    },
    "graph_edge": {
      "type": "object",
      "required": ["id", "source", "target", "type"],
      "properties": {
        "id": {
          "type": "string",
          "description": "Edge identifier",
          "pattern": "^ge_[a-z0-9]+_[a-z0-9]+$"
        },
        "source": {
          "type": "string",
          "description": "Source node ID"
        },
        "target": {
          "type": "string",
          "description": "Target node ID"
        },
        "type": {
          "type": "string",
          "description": "Edge/relationship type",
          "enum": [
            "belongs_to",
            "contains",
            "uses",
            "creates",
            "manages",
            "processes",
            "relates_to",
            "depends_on",
            "derives_from",
            "supports",
            "conflicts_with",
            "precedes",
            "follows",
            "tagged_with",
            "owned_by",
            "linked_to"
          ]
        },
        "label": {
          "type": "string",
          "description": "Edge label"
        },
        "weight": {
          "type": "number",
          "description": "Edge weight/strength",
          "minimum": 0,
          "maximum": 1
        },
        "bidirectional": {
          "type": "boolean",
          "description": "Whether edge is bidirectional"
        },
        "properties": {
          "type": "object",
          "description": "Edge properties",
          "additionalProperties": true
        },
        "metadata": {
          "type": "object",
          "properties": {
            "created_at": {
              "type": "string",
              "format": "date-time"
            }
          }
        }
      }
    },
    "graph_statistics": {
      "type": "object",
      "properties": {
        "total_nodes": {
          "type": "integer",
          "minimum": 0
        },
        "total_edges": {
          "type": "integer",
          "minimum": 0
        },
        "nodes_by_type": {
          "type": "object",
          "additionalProperties": {
            "type": "integer"
          }
        },
        "edges_by_type": {
          "type": "object",
          "additionalProperties": {
            "type": "integer"
          }
        },
        "average_connections": {
          "type": "number"
        },
        "most_connected_nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "connections": { "type": "integer" }
            }
          }
        }
      }
    },
    "graph_metadata": {
      "type": "object",
      "required": ["created_at", "updated_at", "version"],
      "properties": {
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "version": {
          "type": "string",
          "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        }
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
SECTION B7 — FRONTEND: KNOWLEDGE GRAPH PAGE
============================================================

--- FILE: /che-nu-frontend/pages/knowledge_graph.tsx

/**
 * CHE·NU Frontend — Knowledge Graph Page
 * ========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Interactive knowledge graph explorer and builder.
 * All data is representational only.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo, useCallback } from 'react';
import { KnowledgeGraphViewer } from '../components/KnowledgeGraphViewer';

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

const NODE_TYPE_COLORS: Record<string, string> = {
  sphere: '#D8B26A',
  project: '#3F7249',
  mission: '#3EB4A2',
  agent: '#7A593A',
  engine: '#8D8371',
  object: '#2F4C39',
  domain: '#B8A88A',
  concept: '#5C9A84',
  user: '#E9E4D6',
  workflow: '#4A8B7C',
};

const NODE_TYPE_ICONS: Record<string, string> = {
  sphere: '🌐',
  project: '📋',
  mission: '🎯',
  agent: '🤖',
  engine: '⚙️',
  object: '📦',
  domain: '🏛️',
  concept: '💡',
  user: '👤',
  workflow: '🔄',
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface GraphNode {
  id: string;
  type: string;
  label: string;
  properties: Record<string, unknown>;
  metadata: {
    created_at: string;
    updated_at: string;
    weight: number;
  };
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
  weight: number;
  bidirectional: boolean;
}

interface KnowledgeGraphData {
  id: string;
  name: string;
  description: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  statistics: {
    total_nodes: number;
    total_edges: number;
    nodes_by_type: Record<string, number>;
    edges_by_type: Record<string, number>;
    average_connections: number;
  };
}

// ============================================================
// SAMPLE DATA (REPRESENTATIONAL ONLY)
// ============================================================

const SAMPLE_GRAPH: KnowledgeGraphData = {
  id: 'kg_main_abc123',
  name: 'CHE·NU Main Knowledge Graph',
  description: 'Global knowledge graph connecting all CHE·NU entities',
  nodes: [
    // Spheres
    { id: 'gn_sphere_1', type: 'sphere', label: 'Maison', properties: { domain: 'personal' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.9 } },
    { id: 'gn_sphere_2', type: 'sphere', label: 'Entreprise', properties: { domain: 'business' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.9 } },
    { id: 'gn_sphere_3', type: 'sphere', label: 'Projets', properties: { domain: 'projects' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.9 } },
    { id: 'gn_sphere_4', type: 'sphere', label: 'Creative Studio', properties: { domain: 'creative' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.85 } },
    { id: 'gn_sphere_5', type: 'sphere', label: 'Scholar', properties: { domain: 'knowledge' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.8 } },
    
    // Projects
    { id: 'gn_project_1', type: 'project', label: 'CHE·NU Platform', properties: { status: 'active', priority: 'high' }, metadata: { created_at: '2024-06-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 1.0 } },
    { id: 'gn_project_2', type: 'project', label: 'XR Experience', properties: { status: 'active', priority: 'medium' }, metadata: { created_at: '2024-08-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.8 } },
    
    // Missions
    { id: 'gn_mission_1', type: 'mission', label: 'SDK Development', properties: { urgency: 'high' }, metadata: { created_at: '2024-10-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 0.9 } },
    { id: 'gn_mission_2', type: 'mission', label: 'Frontend Build', properties: { urgency: 'medium' }, metadata: { created_at: '2024-10-15T00:00:00Z', updated_at: '2024-12-11T00:00:00Z', weight: 0.85 } },
    
    // Agents
    { id: 'gn_agent_1', type: 'agent', label: 'Nova', properties: { role: 'orchestrator' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 1.0 } },
    { id: 'gn_agent_2', type: 'agent', label: 'DocumentSpecialist', properties: { role: 'specialist' }, metadata: { created_at: '2024-03-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.7 } },
    { id: 'gn_agent_3', type: 'agent', label: 'XRSceneBuilder', properties: { role: 'builder' }, metadata: { created_at: '2024-05-01T00:00:00Z', updated_at: '2024-12-08T00:00:00Z', weight: 0.75 } },
    
    // Engines
    { id: 'gn_engine_1', type: 'engine', label: 'KnowledgeEngine', properties: { category: 'core' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 0.95 } },
    { id: 'gn_engine_2', type: 'engine', label: 'ProjectEngine', properties: { category: 'core' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 0.9 } },
    { id: 'gn_engine_3', type: 'engine', label: 'XRSceneEngine', properties: { category: 'xr' }, metadata: { created_at: '2024-04-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.85 } },
    { id: 'gn_engine_4', type: 'engine', label: 'ObjectEngine', properties: { category: 'core' }, metadata: { created_at: '2024-11-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 0.8 } },
    
    // Objects
    { id: 'gn_object_1', type: 'object', label: 'Architecture Doc', properties: { object_type: 'document' }, metadata: { created_at: '2024-09-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.7 } },
    { id: 'gn_object_2', type: 'object', label: 'Nova Avatar', properties: { object_type: 'xr-object' }, metadata: { created_at: '2024-07-01T00:00:00Z', updated_at: '2024-12-08T00:00:00Z', weight: 0.65 } },
    
    // Concepts
    { id: 'gn_concept_1', type: 'concept', label: 'SAFE Architecture', properties: { abstract: true }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 1.0 } },
    { id: 'gn_concept_2', type: 'concept', label: 'Representational Design', properties: { abstract: true }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-12T00:00:00Z', weight: 0.95 } },
    
    // Domains
    { id: 'gn_domain_1', type: 'domain', label: 'AI/ML', properties: { category: 'technology' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.9 } },
    { id: 'gn_domain_2', type: 'domain', label: 'XR/Immersive', properties: { category: 'technology' }, metadata: { created_at: '2024-01-01T00:00:00Z', updated_at: '2024-12-10T00:00:00Z', weight: 0.85 } },
  ],
  edges: [
    // Project → Sphere
    { id: 'ge_1', source: 'gn_project_1', target: 'gn_sphere_3', type: 'belongs_to', weight: 0.9, bidirectional: false },
    { id: 'ge_2', source: 'gn_project_2', target: 'gn_sphere_4', type: 'belongs_to', weight: 0.85, bidirectional: false },
    
    // Project → Mission
    { id: 'ge_3', source: 'gn_project_1', target: 'gn_mission_1', type: 'contains', weight: 0.9, bidirectional: false },
    { id: 'ge_4', source: 'gn_project_1', target: 'gn_mission_2', type: 'contains', weight: 0.85, bidirectional: false },
    
    // Mission → Agent
    { id: 'ge_5', source: 'gn_mission_1', target: 'gn_agent_1', type: 'uses', weight: 0.9, bidirectional: false },
    { id: 'ge_6', source: 'gn_mission_2', target: 'gn_agent_2', type: 'uses', weight: 0.8, bidirectional: false },
    
    // Agent → Engine
    { id: 'ge_7', source: 'gn_agent_1', target: 'gn_engine_1', type: 'uses', weight: 0.95, bidirectional: false },
    { id: 'ge_8', source: 'gn_agent_1', target: 'gn_engine_2', type: 'uses', weight: 0.9, bidirectional: false },
    { id: 'ge_9', source: 'gn_agent_3', target: 'gn_engine_3', type: 'uses', weight: 0.85, bidirectional: false },
    
    // Agent → Object
    { id: 'ge_10', source: 'gn_agent_2', target: 'gn_object_1', type: 'creates', weight: 0.8, bidirectional: false },
    { id: 'ge_11', source: 'gn_agent_3', target: 'gn_object_2', type: 'creates', weight: 0.75, bidirectional: false },
    
    // Object → Sphere
    { id: 'ge_12', source: 'gn_object_1', target: 'gn_sphere_5', type: 'tagged_with', weight: 0.7, bidirectional: false },
    { id: 'ge_13', source: 'gn_object_2', target: 'gn_sphere_4', type: 'tagged_with', weight: 0.7, bidirectional: false },
    
    // Engine → Domain
    { id: 'ge_14', source: 'gn_engine_1', target: 'gn_domain_1', type: 'processes', weight: 0.9, bidirectional: false },
    { id: 'ge_15', source: 'gn_engine_3', target: 'gn_domain_2', type: 'processes', weight: 0.85, bidirectional: false },
    
    // Concept → Sphere
    { id: 'ge_16', source: 'gn_concept_1', target: 'gn_sphere_3', type: 'supports', weight: 1.0, bidirectional: false },
    { id: 'ge_17', source: 'gn_concept_2', target: 'gn_sphere_3', type: 'supports', weight: 0.95, bidirectional: false },
    
    // Concept relationships
    { id: 'ge_18', source: 'gn_concept_2', target: 'gn_concept_1', type: 'derives_from', weight: 0.9, bidirectional: false },
    
    // Engine dependencies
    { id: 'ge_19', source: 'gn_engine_4', target: 'gn_engine_1', type: 'depends_on', weight: 0.6, bidirectional: false },
  ],
  statistics: {
    total_nodes: 20,
    total_edges: 19,
    nodes_by_type: {
      sphere: 5,
      project: 2,
      mission: 2,
      agent: 3,
      engine: 4,
      object: 2,
      concept: 2,
      domain: 2,
    },
    edges_by_type: {
      belongs_to: 2,
      contains: 2,
      uses: 5,
      creates: 2,
      tagged_with: 2,
      processes: 2,
      supports: 2,
      derives_from: 1,
      depends_on: 1,
    },
    average_connections: 1.9,
  },
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function KnowledgeGraphPage() {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [filterType, setFilterType] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'graph' | 'list' | 'stats'>('graph');
  const [searchTerm, setSearchTerm] = useState('');
  
  // Get unique node types
  const nodeTypes = useMemo(() => {
    const types = new Set(SAMPLE_GRAPH.nodes.map(n => n.type));
    return ['all', ...Array.from(types)];
  }, []);
  
  // Filter nodes
  const filteredNodes = useMemo(() => {
    return SAMPLE_GRAPH.nodes.filter(node => {
      if (filterType !== 'all' && node.type !== filterType) {
        return false;
      }
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        return node.label.toLowerCase().includes(term);
      }
      return true;
    });
  }, [filterType, searchTerm]);
  
  // Filter edges (only show edges where both nodes are visible)
  const filteredEdges = useMemo(() => {
    const nodeIds = new Set(filteredNodes.map(n => n.id));
    return SAMPLE_GRAPH.edges.filter(edge => 
      nodeIds.has(edge.source) && nodeIds.has(edge.target)
    );
  }, [filteredNodes]);
  
  // Handle node selection
  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode(node);
  }, []);
  
  // Get connected nodes for selected node
  const connectedNodes = useMemo(() => {
    if (!selectedNode) return [];
    
    const connected = new Set<string>();
    SAMPLE_GRAPH.edges.forEach(edge => {
      if (edge.source === selectedNode.id) connected.add(edge.target);
      if (edge.target === selectedNode.id) connected.add(edge.source);
    });
    
    return SAMPLE_GRAPH.nodes.filter(n => connected.has(n.id));
  }, [selectedNode]);
  
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
              <span>🕸️</span>
              Knowledge Graph
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              {SAMPLE_GRAPH.name} • {SAMPLE_GRAPH.statistics.total_nodes} nodes • {SAMPLE_GRAPH.statistics.total_edges} edges
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
              + Add Node
            </button>
            <button style={{
              padding: '10px 20px',
              backgroundColor: COLORS.cenoteTurquoise,
              color: COLORS.uiSlate,
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
            }}>
              + Add Edge
            </button>
          </div>
        </div>
        
        {/* Controls */}
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
            placeholder="Search nodes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
              minWidth: '200px',
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
            {nodeTypes.map(type => (
              <option key={type} value={type}>
                {type === 'all' ? 'All Types' : `${NODE_TYPE_ICONS[type] || '📍'} ${type}`}
              </option>
            ))}
          </select>
          
          {/* View Mode */}
          <div style={{ 
            display: 'flex', 
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
            overflow: 'hidden',
          }}>
            {(['graph', 'list', 'stats'] as const).map(mode => (
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
                {mode === 'graph' ? '🗺️' : mode === 'list' ? '📋' : '📊'} {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
          
          {/* Results count */}
          <span style={{ color: COLORS.ancientStone, fontSize: '14px' }}>
            {filteredNodes.length} nodes • {filteredEdges.length} edges
          </span>
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Graph / List / Stats View */}
        <div style={{
          flex: selectedNode ? '1 1 60%' : 1,
          overflow: 'hidden',
          borderRight: selectedNode ? `1px solid ${COLORS.shadowMoss}` : 'none',
        }}>
          {viewMode === 'graph' && (
            <KnowledgeGraphViewer
              nodes={filteredNodes}
              edges={filteredEdges}
              onNodeClick={handleNodeClick}
              selectedNodeId={selectedNode?.id}
            />
          )}
          
          {viewMode === 'list' && (
            <NodeListView 
              nodes={filteredNodes}
              edges={filteredEdges}
              onNodeClick={handleNodeClick}
              selectedNodeId={selectedNode?.id}
            />
          )}
          
          {viewMode === 'stats' && (
            <GraphStatsView statistics={SAMPLE_GRAPH.statistics} />
          )}
        </div>
        
        {/* Node Detail Panel */}
        {selectedNode && (
          <div style={{
            flex: '0 0 400px',
            overflowY: 'auto',
            padding: '20px',
            backgroundColor: '#16171a',
          }}>
            <NodeDetailPanel 
              node={selectedNode}
              connectedNodes={connectedNodes}
              edges={SAMPLE_GRAPH.edges.filter(e => 
                e.source === selectedNode.id || e.target === selectedNode.id
              )}
              onClose={() => setSelectedNode(null)}
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
          SAFE · NON-AUTONOMOUS · Knowledge graph is representational only — no actual graph database
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

interface NodeListViewProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onNodeClick: (node: GraphNode) => void;
  selectedNodeId?: string;
}

function NodeListView({ nodes, edges, onNodeClick, selectedNodeId }: NodeListViewProps) {
  // Group nodes by type
  const groupedNodes = useMemo(() => {
    const groups: Record<string, GraphNode[]> = {};
    nodes.forEach(node => {
      if (!groups[node.type]) groups[node.type] = [];
      groups[node.type].push(node);
    });
    return groups;
  }, [nodes]);
  
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      {Object.entries(groupedNodes).map(([type, typeNodes]) => (
        <div key={type} style={{ marginBottom: '24px' }}>
          <h3 style={{
            margin: '0 0 12px',
            fontSize: '14px',
            fontWeight: 600,
            color: NODE_TYPE_COLORS[type],
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>{NODE_TYPE_ICONS[type]}</span>
            {type.toUpperCase()}
            <span style={{ color: COLORS.ancientStone, fontWeight: 400 }}>({typeNodes.length})</span>
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {typeNodes.map(node => {
              const connectionCount = edges.filter(e => 
                e.source === node.id || e.target === node.id
              ).length;
              
              return (
                <div
                  key={node.id}
                  onClick={() => onNodeClick(node)}
                  style={{
                    padding: '12px 16px',
                    backgroundColor: selectedNodeId === node.id 
                      ? `${COLORS.sacredGold}20` 
                      : COLORS.shadowMoss,
                    borderRadius: '8px',
                    borderLeft: `3px solid ${NODE_TYPE_COLORS[node.type]}`,
                    cursor: 'pointer',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <div>
                    <span style={{ fontWeight: 500 }}>{node.label}</span>
                    <span style={{ 
                      marginLeft: '8px', 
                      fontSize: '12px', 
                      color: COLORS.ancientStone,
                      fontFamily: 'monospace',
                    }}>
                      {node.id}
                    </span>
                  </div>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '12px',
                    fontSize: '12px',
                    color: COLORS.ancientStone,
                  }}>
                    <span>🔗 {connectionCount}</span>
                    <span>⚖️ {(node.metadata.weight * 100).toFixed(0)}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

interface GraphStatsViewProps {
  statistics: KnowledgeGraphData['statistics'];
}

function GraphStatsView({ statistics }: GraphStatsViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      {/* Summary Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '16px',
        marginBottom: '32px',
      }}>
        <StatCard label="Total Nodes" value={statistics.total_nodes} icon="📍" color={COLORS.sacredGold} />
        <StatCard label="Total Edges" value={statistics.total_edges} icon="🔗" color={COLORS.cenoteTurquoise} />
        <StatCard label="Avg Connections" value={statistics.average_connections.toFixed(1)} icon="📊" color={COLORS.jungleEmerald} />
        <StatCard label="Node Types" value={Object.keys(statistics.nodes_by_type).length} icon="🏷️" color={COLORS.earthEmber} />
      </div>
      
      {/* Nodes by Type */}
      <div style={{ marginBottom: '32px' }}>
        <h3 style={{ margin: '0 0 16px', color: COLORS.softSand }}>Nodes by Type</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {Object.entries(statistics.nodes_by_type)
            .sort((a, b) => b[1] - a[1])
            .map(([type, count]) => {
              const maxCount = Math.max(...Object.values(statistics.nodes_by_type));
              const percentage = (count / maxCount) * 100;
              
              return (
                <div key={type} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ width: '24px', fontSize: '16px' }}>{NODE_TYPE_ICONS[type]}</span>
                  <span style={{ width: '100px', fontSize: '14px' }}>{type}</span>
                  <div style={{ 
                    flex: 1, 
                    height: '24px', 
                    backgroundColor: COLORS.shadowMoss,
                    borderRadius: '4px',
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      width: `${percentage}%`,
                      height: '100%',
                      backgroundColor: NODE_TYPE_COLORS[type],
                      display: 'flex',
                      alignItems: 'center',
                      paddingLeft: '8px',
                    }}>
                      <span style={{ fontSize: '12px', fontWeight: 600, color: COLORS.uiSlate }}>
                        {count}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      </div>
      
      {/* Edges by Type */}
      <div>
        <h3 style={{ margin: '0 0 16px', color: COLORS.softSand }}>Edges by Type</h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(3, 1fr)', 
          gap: '12px',
        }}>
          {Object.entries(statistics.edges_by_type)
            .sort((a, b) => b[1] - a[1])
            .map(([type, count]) => (
              <div
                key={type}
                style={{
                  padding: '12px',
                  backgroundColor: COLORS.shadowMoss,
                  borderRadius: '8px',
                  textAlign: 'center',
                }}
              >
                <div style={{ fontSize: '20px', fontWeight: 700, color: COLORS.cenoteTurquoise }}>
                  {count}
                </div>
                <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginTop: '4px' }}>
                  {type.replace(/_/g, ' ')}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

interface NodeDetailPanelProps {
  node: GraphNode;
  connectedNodes: GraphNode[];
  edges: GraphEdge[];
  onClose: () => void;
}

function NodeDetailPanel({ node, connectedNodes, edges, onClose }: NodeDetailPanelProps) {
  return (
    <div>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '20px',
      }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ 
            fontSize: '32px', 
            padding: '12px',
            backgroundColor: `${NODE_TYPE_COLORS[node.type]}20`,
            borderRadius: '12px',
          }}>
            {NODE_TYPE_ICONS[node.type]}
          </span>
          <div>
            <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 700 }}>{node.label}</h2>
            <span style={{ 
              display: 'inline-block',
              marginTop: '4px',
              padding: '4px 8px',
              backgroundColor: `${NODE_TYPE_COLORS[node.type]}30`,
              color: NODE_TYPE_COLORS[node.type],
              borderRadius: '4px',
              fontSize: '12px',
              fontWeight: 600,
            }}>
              {node.type.toUpperCase()}
            </span>
          </div>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '8px',
            backgroundColor: 'transparent',
            border: 'none',
            color: COLORS.ancientStone,
            cursor: 'pointer',
            fontSize: '18px',
          }}
        >
          ✕
        </button>
      </div>
      
      {/* ID */}
      <div style={{
        padding: '12px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '8px',
        marginBottom: '16px',
        fontFamily: 'monospace',
        fontSize: '12px',
        color: COLORS.ancientStone,
        wordBreak: 'break-all',
      }}>
        {node.id}
      </div>
      
      {/* Weight */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          marginBottom: '8px',
          fontSize: '12px',
        }}>
          <span style={{ color: COLORS.ancientStone }}>Weight/Importance</span>
          <span style={{ color: COLORS.sacredGold, fontWeight: 600 }}>
            {(node.metadata.weight * 100).toFixed(0)}%
          </span>
        </div>
        <div style={{
          height: '8px',
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '4px',
          overflow: 'hidden',
        }}>
          <div style={{
            width: `${node.metadata.weight * 100}%`,
            height: '100%',
            backgroundColor: COLORS.sacredGold,
          }} />
        </div>
      </div>
      
      {/* Properties */}
      {Object.keys(node.properties).length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ margin: '0 0 12px', fontSize: '14px', color: COLORS.softSand }}>
            Properties
          </h4>
          <div style={{
            padding: '12px',
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
          }}>
            {Object.entries(node.properties).map(([key, value]) => (
              <div
                key={key}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '6px 0',
                  borderBottom: `1px solid ${COLORS.uiSlate}`,
                }}
              >
                <span style={{ color: COLORS.ancientStone, fontSize: '13px' }}>{key}</span>
                <span style={{ color: COLORS.softSand, fontSize: '13px', fontWeight: 500 }}>
                  {String(value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Connections */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ margin: '0 0 12px', fontSize: '14px', color: COLORS.softSand }}>
          Connections ({connectedNodes.length})
        </h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {connectedNodes.map(cn => {
            const edge = edges.find(e => 
              (e.source === node.id && e.target === cn.id) ||
              (e.target === node.id && e.source === cn.id)
            );
            const isOutgoing = edge?.source === node.id;
            
            return (
              <div
                key={cn.id}
                style={{
                  padding: '10px 12px',
                  backgroundColor: COLORS.shadowMoss,
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                }}
              >
                <span style={{ fontSize: '16px' }}>{NODE_TYPE_ICONS[cn.type]}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '13px', fontWeight: 500 }}>{cn.label}</div>
                  <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
                    {isOutgoing ? '→' : '←'} {edge?.type}
                  </div>
                </div>
                <span style={{ 
                  fontSize: '11px', 
                  color: COLORS.cenoteTurquoise,
                  fontWeight: 500,
                }}>
                  {cn.type}
                </span>
              </div>
            );
          })}
          
          {connectedNodes.length === 0 && (
            <p style={{ color: COLORS.ancientStone, fontStyle: 'italic', margin: 0 }}>
              No connections
            </p>
          )}
        </div>
      </div>
      
      {/* Timestamps */}
      <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>
        <div>Created: {new Date(node.metadata.created_at).toLocaleDateString()}</div>
        <div>Updated: {new Date(node.metadata.updated_at).toLocaleDateString()}</div>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, color }: { label: string; value: number | string; icon: string; color: string }) {
  return (
    <div style={{
      padding: '20px',
      backgroundColor: COLORS.shadowMoss,
      borderRadius: '12px',
      textAlign: 'center',
      border: `1px solid ${color}30`,
    }}>
      <span style={{ fontSize: '24px', display: 'block', marginBottom: '8px' }}>{icon}</span>
      <span style={{ 
        fontSize: '28px', 
        fontWeight: 700, 
        color,
        display: 'block',
      }}>
        {value}
      </span>
      <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>{label}</span>
    </div>
  );
}

export default KnowledgeGraphPage;

============================================================
SECTION B7 (cont.) — KNOWLEDGE GRAPH VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/KnowledgeGraphViewer.tsx

/**
 * CHE·NU Frontend — Knowledge Graph Viewer Component
 * ===================================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Interactive graph visualization component.
 * Uses Canvas for rendering (representational only).
 * 
 * @version 1.0.0
 */

import React, { useRef, useEffect, useState, useCallback } from 'react';

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

const NODE_TYPE_COLORS: Record<string, string> = {
  sphere: '#D8B26A',
  project: '#3F7249',
  mission: '#3EB4A2',
  agent: '#7A593A',
  engine: '#8D8371',
  object: '#2F4C39',
  domain: '#B8A88A',
  concept: '#5C9A84',
  user: '#E9E4D6',
  workflow: '#4A8B7C',
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface GraphNode {
  id: string;
  type: string;
  label: string;
  properties: Record<string, unknown>;
  metadata: {
    weight: number;
  };
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  weight: number;
  bidirectional: boolean;
}

interface VisualNode extends GraphNode {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
}

interface KnowledgeGraphViewerProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onNodeClick: (node: GraphNode) => void;
  selectedNodeId?: string;
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export function KnowledgeGraphViewer({ 
  nodes, 
  edges, 
  onNodeClick, 
  selectedNodeId 
}: KnowledgeGraphViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [visualNodes, setVisualNodes] = useState<VisualNode[]>([]);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragNode, setDragNode] = useState<string | null>(null);
  const animationRef = useRef<number>();
  
  // Initialize visual nodes with positions
  useEffect(() => {
    const centerX = dimensions.width / 2;
    const centerY = dimensions.height / 2;
    
    // Group nodes by type for radial layout
    const typeGroups: Record<string, GraphNode[]> = {};
    nodes.forEach(node => {
      if (!typeGroups[node.type]) typeGroups[node.type] = [];
      typeGroups[node.type].push(node);
    });
    
    const newVisualNodes: VisualNode[] = [];
    const types = Object.keys(typeGroups);
    
    types.forEach((type, typeIndex) => {
      const groupNodes = typeGroups[type];
      const ringRadius = 100 + typeIndex * 70;
      
      groupNodes.forEach((node, nodeIndex) => {
        const angle = (2 * Math.PI * nodeIndex) / groupNodes.length + (typeIndex * 0.5);
        const radius = 15 + node.metadata.weight * 15;
        
        newVisualNodes.push({
          ...node,
          x: centerX + ringRadius * Math.cos(angle),
          y: centerY + ringRadius * Math.sin(angle),
          vx: 0,
          vy: 0,
          radius,
        });
      });
    });
    
    setVisualNodes(newVisualNodes);
  }, [nodes, dimensions]);
  
  // Handle resize
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);
  
  // Render loop
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;
    
    const render = () => {
      ctx.clearRect(0, 0, dimensions.width, dimensions.height);
      
      // Draw edges
      edges.forEach(edge => {
        const sourceNode = visualNodes.find(n => n.id === edge.source);
        const targetNode = visualNodes.find(n => n.id === edge.target);
        
        if (sourceNode && targetNode) {
          const isHighlighted = 
            selectedNodeId === sourceNode.id || 
            selectedNodeId === targetNode.id ||
            hoveredNode === sourceNode.id ||
            hoveredNode === targetNode.id;
          
          ctx.beginPath();
          ctx.moveTo(sourceNode.x, sourceNode.y);
          ctx.lineTo(targetNode.x, targetNode.y);
          ctx.strokeStyle = isHighlighted 
            ? COLORS.sacredGold 
            : `${COLORS.ancientStone}40`;
          ctx.lineWidth = isHighlighted ? 2 : 1;
          ctx.stroke();
          
          // Draw arrow
          const angle = Math.atan2(targetNode.y - sourceNode.y, targetNode.x - sourceNode.x);
          const midX = (sourceNode.x + targetNode.x) / 2;
          const midY = (sourceNode.y + targetNode.y) / 2;
          
          ctx.save();
          ctx.translate(midX, midY);
          ctx.rotate(angle);
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.lineTo(-8, -4);
          ctx.lineTo(-8, 4);
          ctx.closePath();
          ctx.fillStyle = isHighlighted ? COLORS.sacredGold : `${COLORS.ancientStone}60`;
          ctx.fill();
          ctx.restore();
        }
      });
      
      // Draw nodes
      visualNodes.forEach(node => {
        const isSelected = selectedNodeId === node.id;
        const isHovered = hoveredNode === node.id;
        const color = NODE_TYPE_COLORS[node.type] || COLORS.ancientStone;
        
        // Node circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        
        // Selection/hover ring
        if (isSelected || isHovered) {
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.radius + 4, 0, Math.PI * 2);
          ctx.strokeStyle = COLORS.sacredGold;
          ctx.lineWidth = 3;
          ctx.stroke();
        }
        
        // Label
        ctx.font = '12px system-ui';
        ctx.fillStyle = COLORS.softSand;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(node.label, node.x, node.y + node.radius + 6);
      });
      
      animationRef.current = requestAnimationFrame(render);
    };
    
    render();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [visualNodes, edges, dimensions, selectedNodeId, hoveredNode]);
  
  // Mouse handlers
  const findNodeAtPosition = useCallback((x: number, y: number): VisualNode | null => {
    for (const node of visualNodes) {
      const dx = x - node.x;
      const dy = y - node.y;
      if (Math.sqrt(dx * dx + dy * dy) <= node.radius) {
        return node;
      }
    }
    return null;
  }, [visualNodes]);
  
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    if (isDragging && dragNode) {
      setVisualNodes(prev => prev.map(n => 
        n.id === dragNode ? { ...n, x, y } : n
      ));
    } else {
      const node = findNodeAtPosition(x, y);
      setHoveredNode(node?.id || null);
      
      if (canvasRef.current) {
        canvasRef.current.style.cursor = node ? 'pointer' : 'default';
      }
    }
  }, [isDragging, dragNode, findNodeAtPosition]);
  
  const handleMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const node = findNodeAtPosition(x, y);
    
    if (node) {
      setIsDragging(true);
      setDragNode(node.id);
    }
  }, [findNodeAtPosition]);
  
  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
    setDragNode(null);
  }, []);
  
  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (isDragging) return;
    
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const node = findNodeAtPosition(x, y);
    
    if (node) {
      onNodeClick(node);
    }
  }, [isDragging, findNodeAtPosition, onNodeClick]);
  
  return (
    <div 
      ref={containerRef}
      style={{ 
        width: '100%', 
        height: '100%', 
        position: 'relative',
        backgroundColor: COLORS.uiSlate,
      }}
    >
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onClick={handleClick}
        style={{ display: 'block' }}
      />
      
      {/* Legend */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        padding: '16px',
        backgroundColor: `${COLORS.shadowMoss}e0`,
        borderRadius: '12px',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '12px',
        maxWidth: '400px',
      }}>
        {Object.entries(NODE_TYPE_COLORS).map(([type, color]) => {
          const count = nodes.filter(n => n.type === type).length;
          if (count === 0) return null;
          
          return (
            <div key={type} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                backgroundColor: color,
              }} />
              <span style={{ fontSize: '11px', color: COLORS.softSand }}>
                {type} ({count})
              </span>
            </div>
          );
        })}
      </div>
      
      {/* Controls hint */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        padding: '12px 16px',
        backgroundColor: `${COLORS.shadowMoss}e0`,
        borderRadius: '8px',
        fontSize: '12px',
        color: COLORS.ancientStone,
      }}>
        <div>🖱️ Click to select • Drag to move</div>
      </div>
    </div>
  );
}

export default KnowledgeGraphViewer;

============================================================
SECTION A4 + B5 — SYSTEM INDEX UPDATE (OBJECT + KNOWLEDGE GRAPH)
============================================================

--- FILE: /che-nu-sdk/system_index.json (ADDITIONS)

{
  "version": "2.0.0",
  "updated_at": "2024-12-12T00:00:00Z",
  
  "core_modules": {
    "ObjectEngine": {
      "path": "/che-nu-sdk/core/object.ts",
      "description": "Representational object/resource management",
      "category": "object_layer"
    },
    "KnowledgeGraphEngine": {
      "path": "/che-nu-sdk/core/knowledge_graph.ts",
      "description": "Global knowledge graph connections",
      "category": "knowledge_graph_layer"
    }
  },
  
  "submodules": {
    "object_layer": {
      "ObjectCatalogEngine": "/che-nu-sdk/core/object/catalog.engine.ts",
      "ObjectResourceEngine": "/che-nu-sdk/core/object/resource.engine.ts",
      "ObjectInventoryEngine": "/che-nu-sdk/core/object/inventory.engine.ts",
      "ObjectContextEngine": "/che-nu-sdk/core/object/context.engine.ts"
    },
    "knowledge_graph_layer": {
      "GraphNodeEngine": "/che-nu-sdk/core/knowledge_graph/nodes.engine.ts",
      "GraphEdgeEngine": "/che-nu-sdk/core/knowledge_graph/edges.engine.ts",
      "GraphTraversalEngine": "/che-nu-sdk/core/knowledge_graph/traversal.engine.ts",
      "GraphVisualizationEngine": "/che-nu-sdk/core/knowledge_graph/visualization.engine.ts"
    }
  },
  
  "schemas": {
    "object": "/che-nu-sdk/schemas/object.schema.json",
    "knowledge_graph": "/che-nu-sdk/schemas/knowledge_graph.schema.json"
  },
  
  "frontend_pages": {
    "objects": "/che-nu-frontend/pages/objects.tsx",
    "knowledge_graph": "/che-nu-frontend/pages/knowledge_graph.tsx"
  },
  
  "components": {
    "ObjectViewer": "/che-nu-frontend/components/ObjectViewer.tsx",
    "KnowledgeGraphViewer": "/che-nu-frontend/components/KnowledgeGraphViewer.tsx"
  }
}

============================================================
SECTION A5 + B6 — ORCHESTRATOR UPDATE
============================================================

--- FILE: /che-nu-sdk/core/orchestrator.ts (ADDITIONS)

// Add to domain routing logic:

/**
 * Route domain to appropriate engine
 */
function routeDomainToEngine(domain: string): string {
  const routingMap: Record<string, string> = {
    // Existing routes...
    'Knowledge': 'KnowledgeEngine',
    'Project': 'ProjectEngine',
    'Mission': 'MissionEngine',
    
    // NEW: Object Layer routes
    'Object': 'ObjectEngine',
    'Resource': 'ObjectEngine',
    'Asset': 'ObjectEngine',
    'Inventory': 'ObjectEngine',
    
    // NEW: Knowledge Graph routes
    'KnowledgeGraph': 'KnowledgeGraphEngine',
    'Graph': 'KnowledgeGraphEngine',
    'GraphNode': 'KnowledgeGraphEngine',
    'GraphEdge': 'KnowledgeGraphEngine',
    'Relationship': 'KnowledgeGraphEngine',
  };
  
  return routingMap[domain] || 'DefaultEngine';
}

============================================================
SECTION A5 + B6 — CONTEXT INTERPRETER UPDATE
============================================================

--- FILE: /che-nu-sdk/core/context_interpreter.ts (ADDITIONS)

// Add to domain detection rules:

/**
 * Detect domain from input text
 */
function detectDomain(input: string): string {
  const lowerInput = input.toLowerCase();
  
  // Object Layer detection
  if (
    lowerInput.includes('object') ||
    lowerInput.includes('resource') ||
    lowerInput.includes('asset') ||
    lowerInput.includes('inventory') ||
    lowerInput.includes('catalog') ||
    lowerInput.includes('item')
  ) {
    return 'Object';
  }
  
  // Knowledge Graph detection
  if (
    lowerInput.includes('knowledge graph') ||
    lowerInput.includes('graph') ||
    lowerInput.includes('node') ||
    lowerInput.includes('edge') ||
    lowerInput.includes('relationship') ||
    lowerInput.includes('connection') ||
    lowerInput.includes('linked') ||
    lowerInput.includes('traversal') ||
    lowerInput.includes('path between')
  ) {
    return 'KnowledgeGraph';
  }
  
  // ... existing detection logic ...
  
  return 'Default';
}

============================================================
SECTION — WORKFLOW GRID UPDATE
============================================================

--- FILE: /che-nu-frontend/components/WorkflowGrid.tsx (ADDITIONS)

// Add to workflow grid items:

const WORKFLOW_ITEMS = [
  // ... existing items ...
  
  {
    id: 'objects',
    label: 'Objects & Resources',
    icon: '📦',
    description: 'Manage objects, assets, and resources',
    path: '/objects',
    color: '#2F4C39',
  },
  {
    id: 'knowledge-graph',
    label: 'Knowledge Graph',
    icon: '🕸️',
    description: 'Explore entity connections and relationships',
    path: '/knowledge-graph',
    color: '#3EB4A2',
  },
];

============================================================
END OF OBJECT LAYER + KNOWLEDGE GRAPH LAYER
============================================================

✅ OBJECT LAYER COMPLETE:
- ObjectEngine (core)
- 4 sub-engines (catalog, resource, inventory, context)
- object.schema.json
- objects.tsx page
- ObjectViewer component
- Orchestrator routing
- Context interpreter rules

✅ KNOWLEDGE GRAPH LAYER COMPLETE:
- KnowledgeGraphEngine (core)
- 4 sub-engines (nodes, edges, traversal, visualization)
- knowledge_graph.schema.json
- knowledge_graph.tsx page
- KnowledgeGraphViewer component
- Orchestrator routing
- Context interpreter rules
- System index updates
