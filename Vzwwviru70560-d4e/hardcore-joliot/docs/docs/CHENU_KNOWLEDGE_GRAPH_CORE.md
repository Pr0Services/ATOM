############################################################
#                                                          #
#       CHE·NU OBJECT LAYER + KNOWLEDGE GRAPH LAYER        #
#       PART 3: KNOWLEDGE GRAPH LAYER CORE                 #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
PART B — GLOBAL KNOWLEDGE GRAPH LAYER
============================================================

OVERVIEW:
The Knowledge Graph Layer provides a global representational
graph connecting all CHE·NU entities:
- Spheres
- Projects
- Missions
- Agents
- Engines
- Objects
- Knowledge Domains

This is a STRUCTURAL layer only - no actual graph database,
no persistence, no autonomous behavior.

============================================================
SECTION B1 — KNOWLEDGE GRAPH ENGINE (CORE)
============================================================

--- FILE: /che-nu-sdk/core/knowledge_graph.ts

/**
 * CHE·NU SDK — Knowledge Graph Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Global knowledge graph connecting all CHE·NU entities.
 * In-memory representational structure only.
 * 
 * CLASSIFICATION: REPRESENTATIONAL ONLY
 * - No graph database
 * - No persistent storage
 * - No autonomous traversal
 * - Structure describes relationships
 * 
 * @module KnowledgeGraphEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Node types in the knowledge graph
 */
export type GraphNodeType = 
  | 'sphere'
  | 'project'
  | 'mission'
  | 'agent'
  | 'engine'
  | 'object'
  | 'domain'
  | 'concept'
  | 'user'
  | 'workflow';

/**
 * Edge/relationship types
 */
export type EdgeType = 
  | 'belongs_to'
  | 'contains'
  | 'uses'
  | 'creates'
  | 'manages'
  | 'processes'
  | 'relates_to'
  | 'depends_on'
  | 'derives_from'
  | 'supports'
  | 'conflicts_with'
  | 'precedes'
  | 'follows'
  | 'tagged_with'
  | 'owned_by'
  | 'linked_to';

/**
 * Graph node
 */
export interface GraphNode {
  id: string;
  type: GraphNodeType;
  label: string;
  properties: Record<string, unknown>;
  metadata: {
    created_at: string;
    updated_at: string;
    weight: number; // importance 0-1
  };
}

/**
 * Graph edge (relationship)
 */
export interface GraphEdge {
  id: string;
  source: string;      // source node id
  target: string;      // target node id
  type: EdgeType;
  label?: string;
  weight: number;      // strength 0-1
  bidirectional: boolean;
  properties: Record<string, unknown>;
  metadata: {
    created_at: string;
  };
}

/**
 * Knowledge Graph structure
 */
export interface KnowledgeGraph {
  id: string;
  name: string;
  description: string;
  nodes: Map<string, GraphNode>;
  edges: Map<string, GraphEdge>;
  indexes: GraphIndexes;
  statistics: GraphStatistics;
  metadata: {
    created_at: string;
    updated_at: string;
    version: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
    noPersistence: true;
  };
}

/**
 * Graph indexes for efficient lookups
 */
export interface GraphIndexes {
  byType: Map<GraphNodeType, Set<string>>;
  edgesBySource: Map<string, Set<string>>;
  edgesByTarget: Map<string, Set<string>>;
  edgesByType: Map<EdgeType, Set<string>>;
}

/**
 * Graph statistics
 */
export interface GraphStatistics {
  total_nodes: number;
  total_edges: number;
  nodes_by_type: Record<string, number>;
  edges_by_type: Record<string, number>;
  average_connections: number;
  most_connected_nodes: { id: string; connections: number }[];
}

/**
 * Path in the graph
 */
export interface GraphPath {
  nodes: string[];
  edges: string[];
  length: number;
  total_weight: number;
}

/**
 * Subgraph extraction
 */
export interface SubGraph {
  root_node: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  depth: number;
}

/**
 * Node creation input
 */
export interface CreateNodeInput {
  type: GraphNodeType;
  label: string;
  properties?: Record<string, unknown>;
  weight?: number;
}

/**
 * Edge creation input
 */
export interface CreateEdgeInput {
  source: string;
  target: string;
  type: EdgeType;
  label?: string;
  weight?: number;
  bidirectional?: boolean;
  properties?: Record<string, unknown>;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateNodeId(type: GraphNodeType): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `gn_${type}_${timestamp}_${random}`;
}

function generateEdgeId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `ge_${timestamp}_${random}`;
}

function generateGraphId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `kg_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a new knowledge graph
 */
export function createKnowledgeGraph(name: string, description?: string): KnowledgeGraph {
  return {
    id: generateGraphId(),
    name,
    description: description || 'CHE·NU Knowledge Graph',
    nodes: new Map(),
    edges: new Map(),
    indexes: {
      byType: new Map(),
      edgesBySource: new Map(),
      edgesByTarget: new Map(),
      edgesByType: new Map(),
    },
    statistics: {
      total_nodes: 0,
      total_edges: 0,
      nodes_by_type: {},
      edges_by_type: {},
      average_connections: 0,
      most_connected_nodes: [],
    },
    metadata: {
      created_at: now(),
      updated_at: now(),
      version: '1.0.0',
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
  };
}

/**
 * Add a node to the graph
 */
export function addNode(graph: KnowledgeGraph, input: CreateNodeInput): GraphNode {
  const node: GraphNode = {
    id: generateNodeId(input.type),
    type: input.type,
    label: input.label,
    properties: input.properties || {},
    metadata: {
      created_at: now(),
      updated_at: now(),
      weight: input.weight ?? 0.5,
    },
  };
  
  graph.nodes.set(node.id, node);
  
  // Update type index
  if (!graph.indexes.byType.has(input.type)) {
    graph.indexes.byType.set(input.type, new Set());
  }
  graph.indexes.byType.get(input.type)!.add(node.id);
  
  // Update statistics
  updateStatistics(graph);
  graph.metadata.updated_at = now();
  
  return node;
}

/**
 * Add node with existing ID (for importing)
 */
export function addNodeWithId(graph: KnowledgeGraph, id: string, input: CreateNodeInput): GraphNode {
  const node: GraphNode = {
    id,
    type: input.type,
    label: input.label,
    properties: input.properties || {},
    metadata: {
      created_at: now(),
      updated_at: now(),
      weight: input.weight ?? 0.5,
    },
  };
  
  graph.nodes.set(node.id, node);
  
  // Update type index
  if (!graph.indexes.byType.has(input.type)) {
    graph.indexes.byType.set(input.type, new Set());
  }
  graph.indexes.byType.get(input.type)!.add(node.id);
  
  updateStatistics(graph);
  graph.metadata.updated_at = now();
  
  return node;
}

/**
 * Remove a node from the graph
 */
export function removeNode(graph: KnowledgeGraph, nodeId: string): boolean {
  const node = graph.nodes.get(nodeId);
  if (!node) return false;
  
  // Remove all edges connected to this node
  const edgesToRemove: string[] = [];
  graph.edges.forEach((edge, edgeId) => {
    if (edge.source === nodeId || edge.target === nodeId) {
      edgesToRemove.push(edgeId);
    }
  });
  
  edgesToRemove.forEach(edgeId => removeEdge(graph, edgeId));
  
  // Remove from type index
  graph.indexes.byType.get(node.type)?.delete(nodeId);
  
  // Remove node
  graph.nodes.delete(nodeId);
  
  updateStatistics(graph);
  graph.metadata.updated_at = now();
  
  return true;
}

/**
 * Add an edge (relationship) to the graph
 */
export function addEdge(graph: KnowledgeGraph, input: CreateEdgeInput): GraphEdge | null {
  // Verify nodes exist
  if (!graph.nodes.has(input.source) || !graph.nodes.has(input.target)) {
    return null;
  }
  
  const edge: GraphEdge = {
    id: generateEdgeId(),
    source: input.source,
    target: input.target,
    type: input.type,
    label: input.label,
    weight: input.weight ?? 0.5,
    bidirectional: input.bidirectional ?? false,
    properties: input.properties || {},
    metadata: {
      created_at: now(),
    },
  };
  
  graph.edges.set(edge.id, edge);
  
  // Update indexes
  if (!graph.indexes.edgesBySource.has(input.source)) {
    graph.indexes.edgesBySource.set(input.source, new Set());
  }
  graph.indexes.edgesBySource.get(input.source)!.add(edge.id);
  
  if (!graph.indexes.edgesByTarget.has(input.target)) {
    graph.indexes.edgesByTarget.set(input.target, new Set());
  }
  graph.indexes.edgesByTarget.get(input.target)!.add(edge.id);
  
  if (!graph.indexes.edgesByType.has(input.type)) {
    graph.indexes.edgesByType.set(input.type, new Set());
  }
  graph.indexes.edgesByType.get(input.type)!.add(edge.id);
  
  updateStatistics(graph);
  graph.metadata.updated_at = now();
  
  return edge;
}

/**
 * Remove an edge from the graph
 */
export function removeEdge(graph: KnowledgeGraph, edgeId: string): boolean {
  const edge = graph.edges.get(edgeId);
  if (!edge) return false;
  
  // Remove from indexes
  graph.indexes.edgesBySource.get(edge.source)?.delete(edgeId);
  graph.indexes.edgesByTarget.get(edge.target)?.delete(edgeId);
  graph.indexes.edgesByType.get(edge.type)?.delete(edgeId);
  
  graph.edges.delete(edgeId);
  
  updateStatistics(graph);
  graph.metadata.updated_at = now();
  
  return true;
}

/**
 * Get node by ID
 */
export function getNode(graph: KnowledgeGraph, nodeId: string): GraphNode | undefined {
  return graph.nodes.get(nodeId);
}

/**
 * Get edge by ID
 */
export function getEdge(graph: KnowledgeGraph, edgeId: string): GraphEdge | undefined {
  return graph.edges.get(edgeId);
}

/**
 * Get all nodes of a specific type
 */
export function getNodesByType(graph: KnowledgeGraph, type: GraphNodeType): GraphNode[] {
  const ids = graph.indexes.byType.get(type);
  if (!ids) return [];
  return Array.from(ids).map(id => graph.nodes.get(id)!).filter(Boolean);
}

/**
 * Get edges from a node
 */
export function getOutgoingEdges(graph: KnowledgeGraph, nodeId: string): GraphEdge[] {
  const edgeIds = graph.indexes.edgesBySource.get(nodeId);
  if (!edgeIds) return [];
  return Array.from(edgeIds).map(id => graph.edges.get(id)!).filter(Boolean);
}

/**
 * Get edges to a node
 */
export function getIncomingEdges(graph: KnowledgeGraph, nodeId: string): GraphEdge[] {
  const edgeIds = graph.indexes.edgesByTarget.get(nodeId);
  if (!edgeIds) return [];
  return Array.from(edgeIds).map(id => graph.edges.get(id)!).filter(Boolean);
}

/**
 * Get all edges connected to a node
 */
export function getConnectedEdges(graph: KnowledgeGraph, nodeId: string): GraphEdge[] {
  return [...getOutgoingEdges(graph, nodeId), ...getIncomingEdges(graph, nodeId)];
}

/**
 * Get neighbors of a node
 */
export function getNeighbors(graph: KnowledgeGraph, nodeId: string): GraphNode[] {
  const neighborIds = new Set<string>();
  
  getOutgoingEdges(graph, nodeId).forEach(e => neighborIds.add(e.target));
  getIncomingEdges(graph, nodeId).forEach(e => neighborIds.add(e.source));
  
  return Array.from(neighborIds)
    .map(id => graph.nodes.get(id)!)
    .filter(Boolean);
}

/**
 * Find path between two nodes (BFS)
 */
export function findPath(
  graph: KnowledgeGraph, 
  startId: string, 
  endId: string,
  maxDepth: number = 10
): GraphPath | null {
  if (!graph.nodes.has(startId) || !graph.nodes.has(endId)) {
    return null;
  }
  
  if (startId === endId) {
    return { nodes: [startId], edges: [], length: 0, total_weight: 0 };
  }
  
  // BFS
  const visited = new Set<string>();
  const queue: { nodeId: string; path: string[]; edges: string[]; depth: number }[] = [
    { nodeId: startId, path: [startId], edges: [], depth: 0 }
  ];
  
  while (queue.length > 0) {
    const { nodeId, path, edges, depth } = queue.shift()!;
    
    if (depth > maxDepth) continue;
    
    if (visited.has(nodeId)) continue;
    visited.add(nodeId);
    
    const outgoing = getOutgoingEdges(graph, nodeId);
    
    for (const edge of outgoing) {
      const nextId = edge.target;
      
      if (nextId === endId) {
        const finalPath = [...path, nextId];
        const finalEdges = [...edges, edge.id];
        const totalWeight = finalEdges.reduce((sum, eid) => {
          const e = graph.edges.get(eid);
          return sum + (e?.weight || 0);
        }, 0);
        
        return {
          nodes: finalPath,
          edges: finalEdges,
          length: finalPath.length - 1,
          total_weight: totalWeight,
        };
      }
      
      if (!visited.has(nextId)) {
        queue.push({
          nodeId: nextId,
          path: [...path, nextId],
          edges: [...edges, edge.id],
          depth: depth + 1,
        });
      }
    }
  }
  
  return null;
}

/**
 * Extract subgraph around a node
 */
export function extractSubgraph(
  graph: KnowledgeGraph,
  rootId: string,
  depth: number = 2
): SubGraph | null {
  if (!graph.nodes.has(rootId)) return null;
  
  const collectedNodes = new Map<string, GraphNode>();
  const collectedEdges = new Map<string, GraphEdge>();
  
  const visited = new Set<string>();
  const queue: { nodeId: string; currentDepth: number }[] = [
    { nodeId: rootId, currentDepth: 0 }
  ];
  
  while (queue.length > 0) {
    const { nodeId, currentDepth } = queue.shift()!;
    
    if (visited.has(nodeId)) continue;
    visited.add(nodeId);
    
    const node = graph.nodes.get(nodeId);
    if (node) {
      collectedNodes.set(nodeId, node);
    }
    
    if (currentDepth >= depth) continue;
    
    // Get connected edges and neighbors
    const edges = getConnectedEdges(graph, nodeId);
    edges.forEach(edge => {
      collectedEdges.set(edge.id, edge);
      
      const neighborId = edge.source === nodeId ? edge.target : edge.source;
      if (!visited.has(neighborId)) {
        queue.push({ nodeId: neighborId, currentDepth: currentDepth + 1 });
      }
    });
  }
  
  return {
    root_node: rootId,
    nodes: Array.from(collectedNodes.values()),
    edges: Array.from(collectedEdges.values()),
    depth,
  };
}

/**
 * Update graph statistics
 */
function updateStatistics(graph: KnowledgeGraph): void {
  const nodesByType: Record<string, number> = {};
  const edgesByType: Record<string, number> = {};
  const connectionCounts: Map<string, number> = new Map();
  
  // Count nodes by type
  graph.indexes.byType.forEach((ids, type) => {
    nodesByType[type] = ids.size;
  });
  
  // Count edges by type
  graph.indexes.edgesByType.forEach((ids, type) => {
    edgesByType[type] = ids.size;
  });
  
  // Calculate connection counts
  graph.nodes.forEach((node, nodeId) => {
    const connections = (graph.indexes.edgesBySource.get(nodeId)?.size || 0) +
                       (graph.indexes.edgesByTarget.get(nodeId)?.size || 0);
    connectionCounts.set(nodeId, connections);
  });
  
  // Calculate average connections
  const totalConnections = Array.from(connectionCounts.values()).reduce((a, b) => a + b, 0);
  const avgConnections = graph.nodes.size > 0 ? totalConnections / graph.nodes.size : 0;
  
  // Most connected nodes
  const mostConnected = Array.from(connectionCounts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([id, connections]) => ({ id, connections }));
  
  graph.statistics = {
    total_nodes: graph.nodes.size,
    total_edges: graph.edges.size,
    nodes_by_type: nodesByType,
    edges_by_type: edgesByType,
    average_connections: Math.round(avgConnections * 100) / 100,
    most_connected_nodes: mostConnected,
  };
}

/**
 * Search nodes by label or properties
 */
export function searchNodes(
  graph: KnowledgeGraph,
  query: string,
  type?: GraphNodeType
): GraphNode[] {
  const lowerQuery = query.toLowerCase();
  let results = Array.from(graph.nodes.values());
  
  if (type) {
    const typeIds = graph.indexes.byType.get(type);
    if (typeIds) {
      results = results.filter(n => typeIds.has(n.id));
    } else {
      return [];
    }
  }
  
  return results.filter(node => {
    if (node.label.toLowerCase().includes(lowerQuery)) return true;
    
    // Search in properties
    const propsStr = JSON.stringify(node.properties).toLowerCase();
    return propsStr.includes(lowerQuery);
  });
}

/**
 * Get graph statistics
 */
export function getStatistics(graph: KnowledgeGraph): GraphStatistics {
  return { ...graph.statistics };
}

/**
 * Export graph to serializable format
 */
export function exportGraph(graph: KnowledgeGraph): {
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata: KnowledgeGraph['metadata'];
} {
  return {
    nodes: Array.from(graph.nodes.values()),
    edges: Array.from(graph.edges.values()),
    metadata: graph.metadata,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'KnowledgeGraphEngine',
    version: '1.0.0',
    description: 'Global knowledge graph for CHE·NU entity connections',
    nodeTypes: [
      'sphere', 'project', 'mission', 'agent', 'engine',
      'object', 'domain', 'concept', 'user', 'workflow'
    ],
    edgeTypes: [
      'belongs_to', 'contains', 'uses', 'creates', 'manages',
      'processes', 'relates_to', 'depends_on', 'derives_from',
      'supports', 'conflicts_with', 'precedes', 'follows',
      'tagged_with', 'owned_by', 'linked_to'
    ],
    subModules: [
      'GraphNodeEngine',
      'GraphEdgeEngine',
      'GraphTraversalEngine',
      'GraphVisualizationEngine',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
  };
}

export default {
  createKnowledgeGraph,
  addNode,
  addNodeWithId,
  removeNode,
  addEdge,
  removeEdge,
  getNode,
  getEdge,
  getNodesByType,
  getOutgoingEdges,
  getIncomingEdges,
  getConnectedEdges,
  getNeighbors,
  findPath,
  extractSubgraph,
  searchNodes,
  getStatistics,
  exportGraph,
  meta,
};

============================================================
SECTION B2 — KNOWLEDGE GRAPH SUB-ENGINES
============================================================

--- FILE: /che-nu-sdk/core/knowledge_graph/nodes.engine.ts

/**
 * CHE·NU SDK — Graph Nodes Engine
 * =================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Specialized node management for the knowledge graph.
 * 
 * @module GraphNodeEngine
 * @version 1.0.0
 */

import type { 
  KnowledgeGraph, 
  GraphNode, 
  GraphNodeType, 
  CreateNodeInput 
} from '../knowledge_graph';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Node template for common entity types
 */
export interface NodeTemplate {
  type: GraphNodeType;
  defaultProperties: Record<string, unknown>;
  requiredProperties: string[];
  suggestedEdgeTypes: string[];
}

/**
 * Node cluster
 */
export interface NodeCluster {
  id: string;
  name: string;
  nodes: string[];
  centroid?: string;
  cohesion: number; // 0-1
}

/**
 * Node importance analysis
 */
export interface NodeImportance {
  node_id: string;
  label: string;
  degree_centrality: number;
  importance_score: number;
  connected_types: GraphNodeType[];
}

// ============================================================
// NODE TEMPLATES
// ============================================================

const NODE_TEMPLATES: Record<GraphNodeType, NodeTemplate> = {
  sphere: {
    type: 'sphere',
    defaultProperties: { domain: 'general', active: true },
    requiredProperties: ['name'],
    suggestedEdgeTypes: ['contains', 'relates_to'],
  },
  project: {
    type: 'project',
    defaultProperties: { status: 'active', priority: 'medium' },
    requiredProperties: ['name', 'description'],
    suggestedEdgeTypes: ['belongs_to', 'contains', 'uses'],
  },
  mission: {
    type: 'mission',
    defaultProperties: { urgency: 'normal', scope: 'focused' },
    requiredProperties: ['name', 'objective'],
    suggestedEdgeTypes: ['belongs_to', 'depends_on', 'uses'],
  },
  agent: {
    type: 'agent',
    defaultProperties: { active: true, capability_level: 'intermediate' },
    requiredProperties: ['name', 'role'],
    suggestedEdgeTypes: ['manages', 'creates', 'processes'],
  },
  engine: {
    type: 'engine',
    defaultProperties: { version: '1.0.0', category: 'core' },
    requiredProperties: ['name'],
    suggestedEdgeTypes: ['processes', 'supports', 'derives_from'],
  },
  object: {
    type: 'object',
    defaultProperties: { status: 'active', visibility: 'private' },
    requiredProperties: ['name', 'object_type'],
    suggestedEdgeTypes: ['belongs_to', 'owned_by', 'linked_to'],
  },
  domain: {
    type: 'domain',
    defaultProperties: { category: 'knowledge' },
    requiredProperties: ['name'],
    suggestedEdgeTypes: ['contains', 'relates_to'],
  },
  concept: {
    type: 'concept',
    defaultProperties: { abstract: true },
    requiredProperties: ['name', 'definition'],
    suggestedEdgeTypes: ['relates_to', 'derives_from', 'supports'],
  },
  user: {
    type: 'user',
    defaultProperties: { role: 'standard', active: true },
    requiredProperties: ['identifier'],
    suggestedEdgeTypes: ['owns', 'creates', 'manages'],
  },
  workflow: {
    type: 'workflow',
    defaultProperties: { status: 'draft', automated: false },
    requiredProperties: ['name'],
    suggestedEdgeTypes: ['contains', 'uses', 'precedes', 'follows'],
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Get node template for a type
 */
export function getNodeTemplate(type: GraphNodeType): NodeTemplate {
  return NODE_TEMPLATES[type];
}

/**
 * Create node from template
 */
export function createFromTemplate(
  type: GraphNodeType,
  label: string,
  properties: Record<string, unknown> = {}
): CreateNodeInput {
  const template = NODE_TEMPLATES[type];
  
  return {
    type,
    label,
    properties: { ...template.defaultProperties, ...properties },
    weight: 0.5,
  };
}

/**
 * Validate node against template
 */
export function validateNode(node: GraphNode): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const template = NODE_TEMPLATES[node.type];
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Check required properties
  template.requiredProperties.forEach(prop => {
    if (!(prop in node.properties)) {
      errors.push(`Missing required property: ${prop}`);
    }
  });
  
  // Check weight range
  if (node.metadata.weight < 0 || node.metadata.weight > 1) {
    warnings.push('Weight should be between 0 and 1');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Calculate node importance in graph
 */
export function calculateNodeImportance(
  graph: KnowledgeGraph,
  nodeId: string
): NodeImportance | null {
  const node = graph.nodes.get(nodeId);
  if (!node) return null;
  
  // Get all connections
  const outgoing = graph.indexes.edgesBySource.get(nodeId)?.size || 0;
  const incoming = graph.indexes.edgesByTarget.get(nodeId)?.size || 0;
  const totalConnections = outgoing + incoming;
  
  // Degree centrality (normalized)
  const maxPossibleConnections = (graph.nodes.size - 1) * 2;
  const degreeCentrality = maxPossibleConnections > 0 
    ? totalConnections / maxPossibleConnections 
    : 0;
  
  // Get connected node types
  const connectedTypes = new Set<GraphNodeType>();
  graph.edges.forEach(edge => {
    if (edge.source === nodeId) {
      const targetNode = graph.nodes.get(edge.target);
      if (targetNode) connectedTypes.add(targetNode.type);
    }
    if (edge.target === nodeId) {
      const sourceNode = graph.nodes.get(edge.source);
      if (sourceNode) connectedTypes.add(sourceNode.type);
    }
  });
  
  // Importance score (combines weight, centrality, and type diversity)
  const typeDiversity = connectedTypes.size / Object.keys(NODE_TEMPLATES).length;
  const importanceScore = (
    node.metadata.weight * 0.3 +
    degreeCentrality * 0.4 +
    typeDiversity * 0.3
  );
  
  return {
    node_id: nodeId,
    label: node.label,
    degree_centrality: Math.round(degreeCentrality * 1000) / 1000,
    importance_score: Math.round(importanceScore * 1000) / 1000,
    connected_types: Array.from(connectedTypes),
  };
}

/**
 * Find similar nodes based on properties
 */
export function findSimilarNodes(
  graph: KnowledgeGraph,
  nodeId: string,
  threshold: number = 0.5
): { node: GraphNode; similarity: number }[] {
  const sourceNode = graph.nodes.get(nodeId);
  if (!sourceNode) return [];
  
  const results: { node: GraphNode; similarity: number }[] = [];
  const sourceProps = sourceNode.properties;
  const sourcePropKeys = Object.keys(sourceProps);
  
  graph.nodes.forEach((node, id) => {
    if (id === nodeId) return;
    if (node.type !== sourceNode.type) return; // Same type only
    
    // Calculate property similarity (Jaccard-like)
    const nodeProps = node.properties;
    const nodePropKeys = Object.keys(nodeProps);
    
    const allKeys = new Set([...sourcePropKeys, ...nodePropKeys]);
    let matchCount = 0;
    
    allKeys.forEach(key => {
      if (sourceProps[key] === nodeProps[key]) {
        matchCount++;
      }
    });
    
    const similarity = allKeys.size > 0 ? matchCount / allKeys.size : 0;
    
    if (similarity >= threshold) {
      results.push({ node, similarity: Math.round(similarity * 100) / 100 });
    }
  });
  
  return results.sort((a, b) => b.similarity - a.similarity);
}

/**
 * Get nodes by property value
 */
export function getNodesByProperty(
  graph: KnowledgeGraph,
  propertyKey: string,
  propertyValue: unknown
): GraphNode[] {
  return Array.from(graph.nodes.values()).filter(node => 
    node.properties[propertyKey] === propertyValue
  );
}

/**
 * Batch update node properties
 */
export function batchUpdateNodes(
  graph: KnowledgeGraph,
  nodeIds: string[],
  properties: Record<string, unknown>
): number {
  let updated = 0;
  
  nodeIds.forEach(id => {
    const node = graph.nodes.get(id);
    if (node) {
      node.properties = { ...node.properties, ...properties };
      node.metadata.updated_at = new Date().toISOString();
      updated++;
    }
  });
  
  if (updated > 0) {
    graph.metadata.updated_at = new Date().toISOString();
  }
  
  return updated;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'GraphNodeEngine',
    version: '1.0.0',
    description: 'Node management and analysis for knowledge graph',
    parent: 'KnowledgeGraphEngine',
    templateCount: Object.keys(NODE_TEMPLATES).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  getNodeTemplate,
  createFromTemplate,
  validateNode,
  calculateNodeImportance,
  findSimilarNodes,
  getNodesByProperty,
  batchUpdateNodes,
  meta,
};

--- FILE: /che-nu-sdk/core/knowledge_graph/edges.engine.ts

/**
 * CHE·NU SDK — Graph Edges Engine
 * =================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Specialized edge/relationship management for the knowledge graph.
 * 
 * @module GraphEdgeEngine
 * @version 1.0.0
 */

import type { 
  KnowledgeGraph, 
  GraphEdge, 
  EdgeType,
  GraphNodeType,
  CreateEdgeInput 
} from '../knowledge_graph';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Edge pattern (recommended relationships)
 */
export interface EdgePattern {
  sourceType: GraphNodeType;
  targetType: GraphNodeType;
  edgeType: EdgeType;
  description: string;
  weight: number;
}

/**
 * Relationship analysis
 */
export interface RelationshipAnalysis {
  edge_id: string;
  source_label: string;
  target_label: string;
  edge_type: EdgeType;
  relationship_strength: number;
  is_bidirectional: boolean;
  context: string;
}

/**
 * Edge statistics
 */
export interface EdgeStats {
  total: number;
  by_type: Record<string, number>;
  avg_weight: number;
  bidirectional_count: number;
  most_common_type: EdgeType;
}

// ============================================================
// EDGE PATTERNS (RECOMMENDED RELATIONSHIPS)
// ============================================================

const EDGE_PATTERNS: EdgePattern[] = [
  // Sphere relationships
  { sourceType: 'project', targetType: 'sphere', edgeType: 'belongs_to', description: 'Project belongs to sphere', weight: 0.8 },
  { sourceType: 'mission', targetType: 'sphere', edgeType: 'belongs_to', description: 'Mission belongs to sphere', weight: 0.8 },
  { sourceType: 'object', targetType: 'sphere', edgeType: 'tagged_with', description: 'Object tagged with sphere', weight: 0.6 },
  { sourceType: 'sphere', targetType: 'domain', edgeType: 'contains', description: 'Sphere contains domain', weight: 0.7 },
  
  // Project relationships
  { sourceType: 'project', targetType: 'mission', edgeType: 'contains', description: 'Project contains mission', weight: 0.9 },
  { sourceType: 'project', targetType: 'object', edgeType: 'contains', description: 'Project contains object', weight: 0.7 },
  { sourceType: 'project', targetType: 'agent', edgeType: 'uses', description: 'Project uses agent', weight: 0.6 },
  { sourceType: 'project', targetType: 'engine', edgeType: 'uses', description: 'Project uses engine', weight: 0.5 },
  
  // Mission relationships
  { sourceType: 'mission', targetType: 'object', edgeType: 'uses', description: 'Mission uses object', weight: 0.6 },
  { sourceType: 'mission', targetType: 'agent', edgeType: 'uses', description: 'Mission uses agent', weight: 0.7 },
  { sourceType: 'mission', targetType: 'mission', edgeType: 'depends_on', description: 'Mission depends on mission', weight: 0.5 },
  
  // Agent relationships
  { sourceType: 'agent', targetType: 'engine', edgeType: 'uses', description: 'Agent uses engine', weight: 0.8 },
  { sourceType: 'agent', targetType: 'object', edgeType: 'creates', description: 'Agent creates object', weight: 0.7 },
  { sourceType: 'agent', targetType: 'object', edgeType: 'manages', description: 'Agent manages object', weight: 0.6 },
  
  // Engine relationships
  { sourceType: 'engine', targetType: 'engine', edgeType: 'depends_on', description: 'Engine depends on engine', weight: 0.4 },
  { sourceType: 'engine', targetType: 'domain', edgeType: 'processes', description: 'Engine processes domain', weight: 0.5 },
  
  // Object relationships
  { sourceType: 'object', targetType: 'object', edgeType: 'linked_to', description: 'Object linked to object', weight: 0.5 },
  { sourceType: 'object', targetType: 'agent', edgeType: 'owned_by', description: 'Object owned by agent', weight: 0.7 },
  
  // Concept relationships
  { sourceType: 'concept', targetType: 'concept', edgeType: 'relates_to', description: 'Concept relates to concept', weight: 0.6 },
  { sourceType: 'concept', targetType: 'domain', edgeType: 'belongs_to', description: 'Concept belongs to domain', weight: 0.7 },
  
  // Workflow relationships
  { sourceType: 'workflow', targetType: 'agent', edgeType: 'uses', description: 'Workflow uses agent', weight: 0.8 },
  { sourceType: 'workflow', targetType: 'engine', edgeType: 'uses', description: 'Workflow uses engine', weight: 0.7 },
];

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Get recommended edge patterns for node types
 */
export function getRecommendedPatterns(
  sourceType: GraphNodeType,
  targetType?: GraphNodeType
): EdgePattern[] {
  return EDGE_PATTERNS.filter(p => {
    if (p.sourceType !== sourceType) return false;
    if (targetType && p.targetType !== targetType) return false;
    return true;
  });
}

/**
 * Suggest edge type based on node types
 */
export function suggestEdgeType(
  sourceType: GraphNodeType,
  targetType: GraphNodeType
): EdgeType {
  const pattern = EDGE_PATTERNS.find(
    p => p.sourceType === sourceType && p.targetType === targetType
  );
  
  return pattern?.edgeType || 'relates_to';
}

/**
 * Create edge with recommended weight
 */
export function createRecommendedEdge(
  sourceId: string,
  targetId: string,
  sourceType: GraphNodeType,
  targetType: GraphNodeType,
  label?: string
): CreateEdgeInput {
  const edgeType = suggestEdgeType(sourceType, targetType);
  const pattern = EDGE_PATTERNS.find(
    p => p.sourceType === sourceType && p.targetType === targetType
  );
  
  return {
    source: sourceId,
    target: targetId,
    type: edgeType,
    label,
    weight: pattern?.weight || 0.5,
    bidirectional: false,
  };
}

/**
 * Analyze relationship between nodes
 */
export function analyzeRelationship(
  graph: KnowledgeGraph,
  edgeId: string
): RelationshipAnalysis | null {
  const edge = graph.edges.get(edgeId);
  if (!edge) return null;
  
  const sourceNode = graph.nodes.get(edge.source);
  const targetNode = graph.nodes.get(edge.target);
  
  if (!sourceNode || !targetNode) return null;
  
  // Find pattern for context
  const pattern = EDGE_PATTERNS.find(
    p => p.sourceType === sourceNode.type && 
         p.targetType === targetNode.type &&
         p.edgeType === edge.type
  );
  
  return {
    edge_id: edgeId,
    source_label: sourceNode.label,
    target_label: targetNode.label,
    edge_type: edge.type,
    relationship_strength: edge.weight,
    is_bidirectional: edge.bidirectional,
    context: pattern?.description || `${sourceNode.type} → ${edge.type} → ${targetNode.type}`,
  };
}

/**
 * Get edges by type
 */
export function getEdgesByType(
  graph: KnowledgeGraph,
  edgeType: EdgeType
): GraphEdge[] {
  const edgeIds = graph.indexes.edgesByType.get(edgeType);
  if (!edgeIds) return [];
  return Array.from(edgeIds)
    .map(id => graph.edges.get(id)!)
    .filter(Boolean);
}

/**
 * Find edges between node types
 */
export function findEdgesBetweenTypes(
  graph: KnowledgeGraph,
  sourceType: GraphNodeType,
  targetType: GraphNodeType
): GraphEdge[] {
  return Array.from(graph.edges.values()).filter(edge => {
    const sourceNode = graph.nodes.get(edge.source);
    const targetNode = graph.nodes.get(edge.target);
    return sourceNode?.type === sourceType && targetNode?.type === targetType;
  });
}

/**
 * Calculate edge statistics
 */
export function calculateEdgeStats(graph: KnowledgeGraph): EdgeStats {
  const byType: Record<string, number> = {};
  let totalWeight = 0;
  let bidirectionalCount = 0;
  
  graph.edges.forEach(edge => {
    byType[edge.type] = (byType[edge.type] || 0) + 1;
    totalWeight += edge.weight;
    if (edge.bidirectional) bidirectionalCount++;
  });
  
  // Find most common type
  let mostCommonType: EdgeType = 'relates_to';
  let maxCount = 0;
  Object.entries(byType).forEach(([type, count]) => {
    if (count > maxCount) {
      maxCount = count;
      mostCommonType = type as EdgeType;
    }
  });
  
  return {
    total: graph.edges.size,
    by_type: byType,
    avg_weight: graph.edges.size > 0 
      ? Math.round((totalWeight / graph.edges.size) * 100) / 100 
      : 0,
    bidirectional_count: bidirectionalCount,
    most_common_type: mostCommonType,
  };
}

/**
 * Strengthen edge weight
 */
export function strengthenEdge(
  graph: KnowledgeGraph,
  edgeId: string,
  increment: number = 0.1
): boolean {
  const edge = graph.edges.get(edgeId);
  if (!edge) return false;
  
  edge.weight = Math.min(1, edge.weight + increment);
  graph.metadata.updated_at = new Date().toISOString();
  
  return true;
}

/**
 * Weaken edge weight
 */
export function weakenEdge(
  graph: KnowledgeGraph,
  edgeId: string,
  decrement: number = 0.1
): boolean {
  const edge = graph.edges.get(edgeId);
  if (!edge) return false;
  
  edge.weight = Math.max(0, edge.weight - decrement);
  graph.metadata.updated_at = new Date().toISOString();
  
  return true;
}

/**
 * Make edge bidirectional
 */
export function makeBidirectional(
  graph: KnowledgeGraph,
  edgeId: string
): boolean {
  const edge = graph.edges.get(edgeId);
  if (!edge) return false;
  
  edge.bidirectional = true;
  graph.metadata.updated_at = new Date().toISOString();
  
  return true;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'GraphEdgeEngine',
    version: '1.0.0',
    description: 'Edge/relationship management for knowledge graph',
    parent: 'KnowledgeGraphEngine',
    patternCount: EDGE_PATTERNS.length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  getRecommendedPatterns,
  suggestEdgeType,
  createRecommendedEdge,
  analyzeRelationship,
  getEdgesByType,
  findEdgesBetweenTypes,
  calculateEdgeStats,
  strengthenEdge,
  weakenEdge,
  makeBidirectional,
  meta,
};

--- FILE: /che-nu-sdk/core/knowledge_graph/traversal.engine.ts

/**
 * CHE·NU SDK — Graph Traversal Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Graph traversal algorithms for the knowledge graph.
 * 
 * @module GraphTraversalEngine
 * @version 1.0.0
 */

import type { 
  KnowledgeGraph, 
  GraphNode, 
  GraphEdge,
  GraphPath,
  GraphNodeType,
  EdgeType
} from '../knowledge_graph';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Traversal options
 */
export interface TraversalOptions {
  maxDepth?: number;
  nodeTypeFilter?: GraphNodeType[];
  edgeTypeFilter?: EdgeType[];
  minEdgeWeight?: number;
  direction?: 'outgoing' | 'incoming' | 'both';
}

/**
 * Traversal result
 */
export interface TraversalResult {
  visited_nodes: string[];
  visited_edges: string[];
  paths: GraphPath[];
  depth_reached: number;
  total_weight: number;
}

/**
 * Reachability result
 */
export interface ReachabilityResult {
  source: string;
  target: string;
  reachable: boolean;
  shortest_path?: GraphPath;
  alternative_paths: GraphPath[];
}

/**
 * Cluster result
 */
export interface ClusterResult {
  cluster_id: string;
  nodes: string[];
  density: number;
  central_node: string;
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Breadth-First Search traversal
 */
export function bfs(
  graph: KnowledgeGraph,
  startId: string,
  options: TraversalOptions = {}
): TraversalResult {
  const maxDepth = options.maxDepth ?? 10;
  const direction = options.direction ?? 'outgoing';
  
  const visitedNodes = new Set<string>();
  const visitedEdges = new Set<string>();
  const paths: GraphPath[] = [];
  let maxDepthReached = 0;
  let totalWeight = 0;
  
  const queue: { nodeId: string; depth: number; path: string[] }[] = [
    { nodeId: startId, depth: 0, path: [startId] }
  ];
  
  while (queue.length > 0) {
    const { nodeId, depth, path } = queue.shift()!;
    
    if (visitedNodes.has(nodeId)) continue;
    visitedNodes.add(nodeId);
    maxDepthReached = Math.max(maxDepthReached, depth);
    
    if (depth >= maxDepth) continue;
    
    // Get edges based on direction
    let edges: GraphEdge[] = [];
    if (direction === 'outgoing' || direction === 'both') {
      const outIds = graph.indexes.edgesBySource.get(nodeId);
      if (outIds) {
        outIds.forEach(eid => {
          const e = graph.edges.get(eid);
          if (e) edges.push(e);
        });
      }
    }
    if (direction === 'incoming' || direction === 'both') {
      const inIds = graph.indexes.edgesByTarget.get(nodeId);
      if (inIds) {
        inIds.forEach(eid => {
          const e = graph.edges.get(eid);
          if (e) edges.push(e);
        });
      }
    }
    
    // Apply filters
    edges = filterEdges(graph, edges, options);
    
    edges.forEach(edge => {
      visitedEdges.add(edge.id);
      totalWeight += edge.weight;
      
      const nextId = edge.source === nodeId ? edge.target : edge.source;
      const nextNode = graph.nodes.get(nextId);
      
      if (nextNode && !visitedNodes.has(nextId)) {
        // Apply node type filter
        if (options.nodeTypeFilter && !options.nodeTypeFilter.includes(nextNode.type)) {
          return;
        }
        
        queue.push({
          nodeId: nextId,
          depth: depth + 1,
          path: [...path, nextId],
        });
      }
    });
  }
  
  return {
    visited_nodes: Array.from(visitedNodes),
    visited_edges: Array.from(visitedEdges),
    paths,
    depth_reached: maxDepthReached,
    total_weight: Math.round(totalWeight * 100) / 100,
  };
}

/**
 * Depth-First Search traversal
 */
export function dfs(
  graph: KnowledgeGraph,
  startId: string,
  options: TraversalOptions = {}
): TraversalResult {
  const maxDepth = options.maxDepth ?? 10;
  const direction = options.direction ?? 'outgoing';
  
  const visitedNodes = new Set<string>();
  const visitedEdges = new Set<string>();
  let maxDepthReached = 0;
  let totalWeight = 0;
  
  function visit(nodeId: string, depth: number): void {
    if (visitedNodes.has(nodeId) || depth > maxDepth) return;
    
    visitedNodes.add(nodeId);
    maxDepthReached = Math.max(maxDepthReached, depth);
    
    // Get edges
    let edges: GraphEdge[] = [];
    if (direction === 'outgoing' || direction === 'both') {
      const outIds = graph.indexes.edgesBySource.get(nodeId);
      if (outIds) {
        outIds.forEach(eid => {
          const e = graph.edges.get(eid);
          if (e) edges.push(e);
        });
      }
    }
    if (direction === 'incoming' || direction === 'both') {
      const inIds = graph.indexes.edgesByTarget.get(nodeId);
      if (inIds) {
        inIds.forEach(eid => {
          const e = graph.edges.get(eid);
          if (e) edges.push(e);
        });
      }
    }
    
    edges = filterEdges(graph, edges, options);
    
    edges.forEach(edge => {
      visitedEdges.add(edge.id);
      totalWeight += edge.weight;
      
      const nextId = edge.source === nodeId ? edge.target : edge.source;
      const nextNode = graph.nodes.get(nextId);
      
      if (nextNode && !visitedNodes.has(nextId)) {
        if (options.nodeTypeFilter && !options.nodeTypeFilter.includes(nextNode.type)) {
          return;
        }
        visit(nextId, depth + 1);
      }
    });
  }
  
  visit(startId, 0);
  
  return {
    visited_nodes: Array.from(visitedNodes),
    visited_edges: Array.from(visitedEdges),
    paths: [],
    depth_reached: maxDepthReached,
    total_weight: Math.round(totalWeight * 100) / 100,
  };
}

/**
 * Filter edges based on options
 */
function filterEdges(
  graph: KnowledgeGraph,
  edges: GraphEdge[],
  options: TraversalOptions
): GraphEdge[] {
  return edges.filter(edge => {
    if (options.edgeTypeFilter && !options.edgeTypeFilter.includes(edge.type)) {
      return false;
    }
    if (options.minEdgeWeight !== undefined && edge.weight < options.minEdgeWeight) {
      return false;
    }
    return true;
  });
}

/**
 * Find all paths between two nodes
 */
export function findAllPaths(
  graph: KnowledgeGraph,
  startId: string,
  endId: string,
  maxDepth: number = 5,
  maxPaths: number = 10
): GraphPath[] {
  if (!graph.nodes.has(startId) || !graph.nodes.has(endId)) {
    return [];
  }
  
  const paths: GraphPath[] = [];
  
  function explore(
    currentId: string,
    visited: Set<string>,
    path: string[],
    edges: string[],
    weight: number
  ): void {
    if (paths.length >= maxPaths) return;
    if (path.length > maxDepth + 1) return;
    
    if (currentId === endId) {
      paths.push({
        nodes: [...path],
        edges: [...edges],
        length: path.length - 1,
        total_weight: Math.round(weight * 100) / 100,
      });
      return;
    }
    
    const outIds = graph.indexes.edgesBySource.get(currentId);
    if (!outIds) return;
    
    outIds.forEach(edgeId => {
      const edge = graph.edges.get(edgeId);
      if (!edge) return;
      
      const nextId = edge.target;
      if (visited.has(nextId)) return;
      
      visited.add(nextId);
      explore(
        nextId,
        visited,
        [...path, nextId],
        [...edges, edgeId],
        weight + edge.weight
      );
      visited.delete(nextId);
    });
  }
  
  const visited = new Set<string>([startId]);
  explore(startId, visited, [startId], [], 0);
  
  return paths.sort((a, b) => a.length - b.length);
}

/**
 * Check reachability between nodes
 */
export function checkReachability(
  graph: KnowledgeGraph,
  sourceId: string,
  targetId: string,
  maxDepth: number = 10
): ReachabilityResult {
  const allPaths = findAllPaths(graph, sourceId, targetId, maxDepth, 5);
  
  return {
    source: sourceId,
    target: targetId,
    reachable: allPaths.length > 0,
    shortest_path: allPaths[0],
    alternative_paths: allPaths.slice(1),
  };
}

/**
 * Find connected components
 */
export function findConnectedComponents(graph: KnowledgeGraph): ClusterResult[] {
  const visited = new Set<string>();
  const clusters: ClusterResult[] = [];
  let clusterId = 0;
  
  graph.nodes.forEach((node, nodeId) => {
    if (visited.has(nodeId)) return;
    
    // BFS to find all connected nodes
    const component: string[] = [];
    const queue = [nodeId];
    
    while (queue.length > 0) {
      const current = queue.shift()!;
      if (visited.has(current)) continue;
      
      visited.add(current);
      component.push(current);
      
      // Get all neighbors (both directions)
      const outIds = graph.indexes.edgesBySource.get(current);
      const inIds = graph.indexes.edgesByTarget.get(current);
      
      outIds?.forEach(eid => {
        const e = graph.edges.get(eid);
        if (e && !visited.has(e.target)) queue.push(e.target);
      });
      
      inIds?.forEach(eid => {
        const e = graph.edges.get(eid);
        if (e && !visited.has(e.source)) queue.push(e.source);
      });
    }
    
    if (component.length > 0) {
      // Find central node (most connections)
      let centralNode = component[0];
      let maxConnections = 0;
      
      component.forEach(nid => {
        const connections = 
          (graph.indexes.edgesBySource.get(nid)?.size || 0) +
          (graph.indexes.edgesByTarget.get(nid)?.size || 0);
        if (connections > maxConnections) {
          maxConnections = connections;
          centralNode = nid;
        }
      });
      
      // Calculate density
      const n = component.length;
      const maxEdges = n * (n - 1);
      let actualEdges = 0;
      
      component.forEach(nid => {
        graph.indexes.edgesBySource.get(nid)?.forEach(eid => {
          const e = graph.edges.get(eid);
          if (e && component.includes(e.target)) actualEdges++;
        });
      });
      
      const density = maxEdges > 0 ? actualEdges / maxEdges : 0;
      
      clusters.push({
        cluster_id: `cluster_${clusterId++}`,
        nodes: component,
        density: Math.round(density * 100) / 100,
        central_node: centralNode,
      });
    }
  });
  
  return clusters.sort((a, b) => b.nodes.length - a.nodes.length);
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'GraphTraversalEngine',
    version: '1.0.0',
    description: 'Graph traversal algorithms for knowledge graph',
    parent: 'KnowledgeGraphEngine',
    algorithms: ['BFS', 'DFS', 'findAllPaths', 'connectedComponents'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  bfs,
  dfs,
  findAllPaths,
  checkReachability,
  findConnectedComponents,
  meta,
};

--- FILE: /che-nu-sdk/core/knowledge_graph/visualization.engine.ts

/**
 * CHE·NU SDK — Graph Visualization Engine
 * =========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Generates visualization data for the knowledge graph.
 * Output is data structures for rendering, not actual rendering.
 * 
 * @module GraphVisualizationEngine
 * @version 1.0.0
 */

import type { 
  KnowledgeGraph, 
  GraphNode, 
  GraphEdge,
  GraphNodeType 
} from '../knowledge_graph';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Visualization node data
 */
export interface VisNode {
  id: string;
  label: string;
  type: GraphNodeType;
  x?: number;
  y?: number;
  size: number;
  color: string;
  group: string;
}

/**
 * Visualization edge data
 */
export interface VisEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  weight: number;
  color: string;
  style: 'solid' | 'dashed' | 'dotted';
}

/**
 * Complete visualization data
 */
export interface VisualizationData {
  nodes: VisNode[];
  edges: VisEdge[];
  layout: LayoutConfig;
  legend: LegendItem[];
  statistics: {
    node_count: number;
    edge_count: number;
    groups: string[];
  };
}

/**
 * Layout configuration
 */
export interface LayoutConfig {
  type: 'force' | 'radial' | 'hierarchical' | 'circular';
  center: { x: number; y: number };
  scale: number;
  spacing: number;
}

/**
 * Legend item
 */
export interface LegendItem {
  type: string;
  label: string;
  color: string;
  count: number;
}

/**
 * Visualization options
 */
export interface VisualizationOptions {
  layout?: 'force' | 'radial' | 'hierarchical' | 'circular';
  nodeSize?: 'fixed' | 'degree' | 'weight';
  colorScheme?: 'type' | 'group' | 'weight';
  showLabels?: boolean;
  filterTypes?: GraphNodeType[];
}

// ============================================================
// COLOR SCHEMES
// ============================================================

const TYPE_COLORS: Record<GraphNodeType, string> = {
  sphere: '#D8B26A',      // Sacred Gold
  project: '#3F7249',     // Jungle Emerald
  mission: '#3EB4A2',     // Cenote Turquoise
  agent: '#7A593A',       // Earth Ember
  engine: '#8D8371',      // Ancient Stone
  object: '#2F4C39',      // Shadow Moss
  domain: '#B8A88A',      // Light Stone
  concept: '#5C9A84',     // Soft Emerald
  user: '#E9E4D6',        // Soft Sand
  workflow: '#4A8B7C',    // Teal
};

const EDGE_COLORS: Record<string, string> = {
  belongs_to: '#D8B26A',
  contains: '#3F7249',
  uses: '#3EB4A2',
  creates: '#7A593A',
  manages: '#8D8371',
  processes: '#2F4C39',
  relates_to: '#B8A88A',
  depends_on: '#E53E3E',
  derives_from: '#5C9A84',
  default: '#6B7280',
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Generate visualization data from knowledge graph
 */
export function generateVisualization(
  graph: KnowledgeGraph,
  options: VisualizationOptions = {}
): VisualizationData {
  const layout = options.layout ?? 'force';
  const nodeSize = options.nodeSize ?? 'degree';
  const colorScheme = options.colorScheme ?? 'type';
  
  // Build nodes
  const visNodes: VisNode[] = [];
  const nodeDegrees = calculateDegrees(graph);
  
  graph.nodes.forEach((node, id) => {
    // Apply type filter
    if (options.filterTypes && !options.filterTypes.includes(node.type)) {
      return;
    }
    
    // Calculate size based on option
    let size = 20;
    if (nodeSize === 'degree') {
      const degree = nodeDegrees.get(id) || 0;
      size = 15 + Math.min(degree * 3, 30);
    } else if (nodeSize === 'weight') {
      size = 15 + node.metadata.weight * 30;
    }
    
    // Get color
    const color = getNodeColor(node, colorScheme);
    
    visNodes.push({
      id,
      label: node.label,
      type: node.type,
      size,
      color,
      group: node.type,
    });
  });
  
  // Build edges
  const visEdges: VisEdge[] = [];
  const nodeIds = new Set(visNodes.map(n => n.id));
  
  graph.edges.forEach((edge, id) => {
    // Only include edges where both nodes are visible
    if (!nodeIds.has(edge.source) || !nodeIds.has(edge.target)) {
      return;
    }
    
    visEdges.push({
      id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      weight: edge.weight,
      color: EDGE_COLORS[edge.type] || EDGE_COLORS.default,
      style: edge.bidirectional ? 'solid' : 'dashed',
    });
  });
  
  // Apply layout positions
  applyLayout(visNodes, layout);
  
  // Build legend
  const legend = buildLegend(visNodes);
  
  // Get unique groups
  const groups = [...new Set(visNodes.map(n => n.group))];
  
  return {
    nodes: visNodes,
    edges: visEdges,
    layout: {
      type: layout,
      center: { x: 400, y: 300 },
      scale: 1,
      spacing: 50,
    },
    legend,
    statistics: {
      node_count: visNodes.length,
      edge_count: visEdges.length,
      groups,
    },
  };
}

/**
 * Calculate node degrees
 */
function calculateDegrees(graph: KnowledgeGraph): Map<string, number> {
  const degrees = new Map<string, number>();
  
  graph.nodes.forEach((_, id) => {
    const outgoing = graph.indexes.edgesBySource.get(id)?.size || 0;
    const incoming = graph.indexes.edgesByTarget.get(id)?.size || 0;
    degrees.set(id, outgoing + incoming);
  });
  
  return degrees;
}

/**
 * Get node color based on scheme
 */
function getNodeColor(node: GraphNode, scheme: string): string {
  if (scheme === 'type') {
    return TYPE_COLORS[node.type] || '#6B7280';
  }
  if (scheme === 'weight') {
    const intensity = Math.floor(node.metadata.weight * 255);
    return `rgb(${intensity}, ${200 - intensity / 2}, ${100})`;
  }
  return TYPE_COLORS[node.type] || '#6B7280';
}

/**
 * Apply layout positions to nodes
 */
function applyLayout(nodes: VisNode[], layout: string): void {
  const centerX = 400;
  const centerY = 300;
  const radius = 200;
  
  if (layout === 'circular') {
    nodes.forEach((node, i) => {
      const angle = (2 * Math.PI * i) / nodes.length;
      node.x = centerX + radius * Math.cos(angle);
      node.y = centerY + radius * Math.sin(angle);
    });
  } else if (layout === 'radial') {
    // Group by type, then arrange in rings
    const groups = new Map<string, VisNode[]>();
    nodes.forEach(node => {
      const group = groups.get(node.type) || [];
      group.push(node);
      groups.set(node.type, group);
    });
    
    let ringIndex = 0;
    groups.forEach((groupNodes, type) => {
      const ringRadius = 100 + ringIndex * 80;
      groupNodes.forEach((node, i) => {
        const angle = (2 * Math.PI * i) / groupNodes.length;
        node.x = centerX + ringRadius * Math.cos(angle);
        node.y = centerY + ringRadius * Math.sin(angle);
      });
      ringIndex++;
    });
  } else {
    // Force-directed placeholder (random initial positions)
    nodes.forEach(node => {
      node.x = centerX + (Math.random() - 0.5) * 400;
      node.y = centerY + (Math.random() - 0.5) * 300;
    });
  }
}

/**
 * Build legend from nodes
 */
function buildLegend(nodes: VisNode[]): LegendItem[] {
  const typeCounts = new Map<string, number>();
  
  nodes.forEach(node => {
    typeCounts.set(node.type, (typeCounts.get(node.type) || 0) + 1);
  });
  
  return Array.from(typeCounts.entries()).map(([type, count]) => ({
    type,
    label: type.charAt(0).toUpperCase() + type.slice(1),
    color: TYPE_COLORS[type as GraphNodeType] || '#6B7280',
    count,
  }));
}

/**
 * Generate mini-map data
 */
export function generateMiniMap(
  graph: KnowledgeGraph,
  scale: number = 0.2
): { nodes: { x: number; y: number; color: string }[]; bounds: { width: number; height: number } } {
  const vis = generateVisualization(graph, { layout: 'circular' });
  
  return {
    nodes: vis.nodes.map(n => ({
      x: (n.x || 0) * scale,
      y: (n.y || 0) * scale,
      color: n.color,
    })),
    bounds: {
      width: 800 * scale,
      height: 600 * scale,
    },
  };
}

/**
 * Export to DOT format (Graphviz)
 */
export function exportToDOT(graph: KnowledgeGraph): string {
  let dot = 'digraph CHE_NU_KnowledgeGraph {\n';
  dot += '  rankdir=LR;\n';
  dot += '  node [shape=ellipse];\n\n';
  
  // Nodes
  graph.nodes.forEach((node, id) => {
    const color = TYPE_COLORS[node.type] || '#6B7280';
    dot += `  "${id}" [label="${node.label}" color="${color}" style=filled];\n`;
  });
  
  dot += '\n';
  
  // Edges
  graph.edges.forEach((edge, id) => {
    const style = edge.bidirectional ? 'both' : 'forward';
    dot += `  "${edge.source}" -> "${edge.target}" [label="${edge.type}" dir=${style}];\n`;
  });
  
  dot += '}\n';
  
  return dot;
}

/**
 * Export to JSON-LD format
 */
export function exportToJSONLD(graph: KnowledgeGraph): Record<string, unknown> {
  return {
    '@context': {
      '@vocab': 'https://che-nu.ai/ontology/',
      'node': 'https://che-nu.ai/ontology/node',
      'edge': 'https://che-nu.ai/ontology/edge',
    },
    '@type': 'KnowledgeGraph',
    '@id': graph.id,
    name: graph.name,
    nodes: Array.from(graph.nodes.values()).map(n => ({
      '@type': 'Node',
      '@id': n.id,
      label: n.label,
      nodeType: n.type,
    })),
    edges: Array.from(graph.edges.values()).map(e => ({
      '@type': 'Edge',
      '@id': e.id,
      source: e.source,
      target: e.target,
      edgeType: e.type,
    })),
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'GraphVisualizationEngine',
    version: '1.0.0',
    description: 'Visualization data generation for knowledge graph',
    parent: 'KnowledgeGraphEngine',
    layouts: ['force', 'radial', 'hierarchical', 'circular'],
    exportFormats: ['JSON', 'DOT', 'JSON-LD'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  generateVisualization,
  generateMiniMap,
  exportToDOT,
  exportToJSONLD,
  meta,
};
