############################################################
#                                                          #
#       CHE·NU OBJECT LAYER + KNOWLEDGE GRAPH LAYER        #
#       PART 1: OBJECT LAYER CORE                          #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A1 — OBJECT ENGINE (CORE)
============================================================

--- FILE: /che-nu-sdk/core/object.ts

/**
 * CHE·NU SDK — Object Engine
 * ===========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents objects, resources, items, and entities within
 * the CHE·NU ecosystem. Links to spheres, projects, missions,
 * and agents.
 * 
 * CLASSIFICATION: REPRESENTATIONAL ONLY
 * - No actual file system access
 * - No real asset management
 * - No storage operations
 * - Structures describe, not execute
 * 
 * @module ObjectEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Object type classifications
 */
export type ObjectType = 
  | 'document'
  | 'tool'
  | 'asset'
  | 'xr-object'
  | 'concept'
  | 'template'
  | 'component'
  | 'media'
  | 'link'
  | 'data'
  | 'reference'
  | 'artifact'
  | 'custom';

/**
 * Object status
 */
export type ObjectStatus = 
  | 'active'
  | 'archived'
  | 'draft'
  | 'deprecated'
  | 'pending';

/**
 * Object visibility
 */
export type ObjectVisibility = 
  | 'private'
  | 'shared'
  | 'public'
  | 'restricted';

/**
 * Core CHE·NU Object model
 */
export interface CheNuObject {
  id: string;
  name: string;
  description: string;
  type: ObjectType;
  subtype?: string;
  
  // Linking
  sphereTags: string[];
  projectIds: string[];
  missionIds: string[];
  ownerAgentIds: string[];
  engineRefs: string[];
  
  // Classification
  status: ObjectStatus;
  visibility: ObjectVisibility;
  tags: string[];
  categories: string[];
  
  // Content representation
  content: ObjectContent;
  
  // Metadata
  metadata: ObjectMetadata;
  
  // SAFE compliance
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
    noPersistence: true;
  };
}

/**
 * Object content representation
 */
export interface ObjectContent {
  format: string;           // e.g., "json", "markdown", "binary-ref", "url"
  schema?: string;          // optional schema reference
  preview?: string;         // short preview text
  size?: string;            // representational size (e.g., "2.3 MB")
  checksum?: string;        // representational checksum
  properties: Record<string, unknown>;
}

/**
 * Object metadata
 */
export interface ObjectMetadata {
  created_at: string;
  updated_at: string;
  version: string;
  author?: string;
  source?: string;
  license?: string;
  custom: Record<string, unknown>;
}

/**
 * Object creation input
 */
export interface CreateObjectInput {
  name: string;
  description?: string;
  type: ObjectType;
  subtype?: string;
  sphereTags?: string[];
  tags?: string[];
  categories?: string[];
  visibility?: ObjectVisibility;
  content?: Partial<ObjectContent>;
  metadata?: Partial<ObjectMetadata>;
}

/**
 * Object summary
 */
export interface ObjectSummary {
  id: string;
  name: string;
  type: ObjectType;
  subtype?: string;
  spheres: string[];
  links: {
    projects: number;
    missions: number;
    agents: number;
    engines: number;
  };
  status: ObjectStatus;
  tags: string[];
}

/**
 * Object link result
 */
export interface ObjectLinkResult {
  object_id: string;
  link_type: 'project' | 'mission' | 'agent' | 'engine' | 'sphere';
  target_id: string;
  linked_at: string;
  success: boolean;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

/**
 * Generate unique object ID
 */
function generateObjectId(type: ObjectType): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `obj_${type}_${timestamp}_${random}`;
}

/**
 * Get current ISO timestamp
 */
function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a new CHE·NU Object
 * REPRESENTATIONAL ONLY — no actual resource creation
 */
export function createObject(input: CreateObjectInput): CheNuObject {
  const id = generateObjectId(input.type);
  const timestamp = now();
  
  const object: CheNuObject = {
    id,
    name: input.name,
    description: input.description || '',
    type: input.type,
    subtype: input.subtype,
    
    // Linking (empty by default)
    sphereTags: input.sphereTags || [],
    projectIds: [],
    missionIds: [],
    ownerAgentIds: [],
    engineRefs: [],
    
    // Classification
    status: 'active',
    visibility: input.visibility || 'private',
    tags: input.tags || [],
    categories: input.categories || [],
    
    // Content
    content: {
      format: input.content?.format || 'unknown',
      schema: input.content?.schema,
      preview: input.content?.preview,
      size: input.content?.size,
      checksum: input.content?.checksum,
      properties: input.content?.properties || {},
    },
    
    // Metadata
    metadata: {
      created_at: timestamp,
      updated_at: timestamp,
      version: '1.0.0',
      author: input.metadata?.author,
      source: input.metadata?.source,
      license: input.metadata?.license,
      custom: input.metadata?.custom || {},
    },
    
    // SAFE compliance
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
  };
  
  return object;
}

/**
 * Link object to a project
 */
export function linkToProject(object: CheNuObject, projectId: string): ObjectLinkResult {
  if (!object.projectIds.includes(projectId)) {
    object.projectIds.push(projectId);
    object.metadata.updated_at = now();
  }
  
  return {
    object_id: object.id,
    link_type: 'project',
    target_id: projectId,
    linked_at: now(),
    success: true,
  };
}

/**
 * Link object to a mission
 */
export function linkToMission(object: CheNuObject, missionId: string): ObjectLinkResult {
  if (!object.missionIds.includes(missionId)) {
    object.missionIds.push(missionId);
    object.metadata.updated_at = now();
  }
  
  return {
    object_id: object.id,
    link_type: 'mission',
    target_id: missionId,
    linked_at: now(),
    success: true,
  };
}

/**
 * Link object to an agent
 */
export function linkToAgent(object: CheNuObject, agentId: string): ObjectLinkResult {
  if (!object.ownerAgentIds.includes(agentId)) {
    object.ownerAgentIds.push(agentId);
    object.metadata.updated_at = now();
  }
  
  return {
    object_id: object.id,
    link_type: 'agent',
    target_id: agentId,
    linked_at: now(),
    success: true,
  };
}

/**
 * Link object to an engine
 */
export function linkToEngine(object: CheNuObject, engineRef: string): ObjectLinkResult {
  if (!object.engineRefs.includes(engineRef)) {
    object.engineRefs.push(engineRef);
    object.metadata.updated_at = now();
  }
  
  return {
    object_id: object.id,
    link_type: 'engine',
    target_id: engineRef,
    linked_at: now(),
    success: true,
  };
}

/**
 * Add sphere tag to object
 */
export function addSphereTag(object: CheNuObject, sphere: string): ObjectLinkResult {
  if (!object.sphereTags.includes(sphere)) {
    object.sphereTags.push(sphere);
    object.metadata.updated_at = now();
  }
  
  return {
    object_id: object.id,
    link_type: 'sphere',
    target_id: sphere,
    linked_at: now(),
    success: true,
  };
}

/**
 * Remove link from object
 */
export function removeLink(
  object: CheNuObject, 
  linkType: 'project' | 'mission' | 'agent' | 'engine' | 'sphere',
  targetId: string
): boolean {
  let removed = false;
  
  switch (linkType) {
    case 'project':
      const pIdx = object.projectIds.indexOf(targetId);
      if (pIdx > -1) {
        object.projectIds.splice(pIdx, 1);
        removed = true;
      }
      break;
    case 'mission':
      const mIdx = object.missionIds.indexOf(targetId);
      if (mIdx > -1) {
        object.missionIds.splice(mIdx, 1);
        removed = true;
      }
      break;
    case 'agent':
      const aIdx = object.ownerAgentIds.indexOf(targetId);
      if (aIdx > -1) {
        object.ownerAgentIds.splice(aIdx, 1);
        removed = true;
      }
      break;
    case 'engine':
      const eIdx = object.engineRefs.indexOf(targetId);
      if (eIdx > -1) {
        object.engineRefs.splice(eIdx, 1);
        removed = true;
      }
      break;
    case 'sphere':
      const sIdx = object.sphereTags.indexOf(targetId);
      if (sIdx > -1) {
        object.sphereTags.splice(sIdx, 1);
        removed = true;
      }
      break;
  }
  
  if (removed) {
    object.metadata.updated_at = now();
  }
  
  return removed;
}

/**
 * Update object status
 */
export function updateStatus(object: CheNuObject, status: ObjectStatus): CheNuObject {
  object.status = status;
  object.metadata.updated_at = now();
  return object;
}

/**
 * Update object content
 */
export function updateContent(
  object: CheNuObject, 
  content: Partial<ObjectContent>
): CheNuObject {
  object.content = { ...object.content, ...content };
  object.metadata.updated_at = now();
  object.metadata.version = incrementVersion(object.metadata.version);
  return object;
}

/**
 * Increment version string
 */
function incrementVersion(version: string): string {
  const parts = version.split('.').map(Number);
  parts[2] = (parts[2] || 0) + 1;
  return parts.join('.');
}

/**
 * Add tags to object
 */
export function addTags(object: CheNuObject, tags: string[]): CheNuObject {
  tags.forEach(tag => {
    if (!object.tags.includes(tag)) {
      object.tags.push(tag);
    }
  });
  object.metadata.updated_at = now();
  return object;
}

/**
 * Add categories to object
 */
export function addCategories(object: CheNuObject, categories: string[]): CheNuObject {
  categories.forEach(cat => {
    if (!object.categories.includes(cat)) {
      object.categories.push(cat);
    }
  });
  object.metadata.updated_at = now();
  return object;
}

/**
 * Generate object summary
 */
export function summarizeObject(object: CheNuObject): ObjectSummary {
  return {
    id: object.id,
    name: object.name,
    type: object.type,
    subtype: object.subtype,
    spheres: [...object.sphereTags],
    links: {
      projects: object.projectIds.length,
      missions: object.missionIds.length,
      agents: object.ownerAgentIds.length,
      engines: object.engineRefs.length,
    },
    status: object.status,
    tags: [...object.tags],
  };
}

/**
 * Get all links for an object
 */
export function getAllLinks(object: CheNuObject): {
  type: string;
  id: string;
}[] {
  const links: { type: string; id: string }[] = [];
  
  object.sphereTags.forEach(s => links.push({ type: 'sphere', id: s }));
  object.projectIds.forEach(p => links.push({ type: 'project', id: p }));
  object.missionIds.forEach(m => links.push({ type: 'mission', id: m }));
  object.ownerAgentIds.forEach(a => links.push({ type: 'agent', id: a }));
  object.engineRefs.forEach(e => links.push({ type: 'engine', id: e }));
  
  return links;
}

/**
 * Clone object as template
 */
export function cloneAsTemplate(object: CheNuObject, newName: string): CheNuObject {
  const cloned = createObject({
    name: newName,
    description: `Template based on ${object.name}`,
    type: object.type,
    subtype: object.subtype,
    sphereTags: [...object.sphereTags],
    tags: [...object.tags, 'template', 'cloned'],
    categories: [...object.categories],
    visibility: object.visibility,
    content: { ...object.content },
    metadata: {
      source: object.id,
      custom: { cloned_from: object.id },
    },
  });
  
  return cloned;
}

/**
 * Validate object structure
 */
export function validateObject(object: CheNuObject): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];
  
  if (!object.id || !object.id.startsWith('obj_')) {
    errors.push('Invalid object ID format');
  }
  
  if (!object.name || object.name.trim() === '') {
    errors.push('Object name is required');
  }
  
  if (!object.type) {
    errors.push('Object type is required');
  }
  
  if (!object.safe?.isRepresentational) {
    errors.push('Object must be marked as representational');
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectEngine',
    version: '1.0.0',
    description: 'Representational object/resource management for CHE·NU',
    supportedTypes: [
      'document', 'tool', 'asset', 'xr-object', 'concept',
      'template', 'component', 'media', 'link', 'data',
      'reference', 'artifact', 'custom'
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
    subModules: [
      'ObjectCatalogEngine',
      'ObjectResourceEngine',
      'ObjectInventoryEngine',
      'ObjectContextEngine',
    ],
  };
}

export default {
  createObject,
  linkToProject,
  linkToMission,
  linkToAgent,
  linkToEngine,
  addSphereTag,
  removeLink,
  updateStatus,
  updateContent,
  addTags,
  addCategories,
  summarizeObject,
  getAllLinks,
  cloneAsTemplate,
  validateObject,
  meta,
};

============================================================
SECTION A2 — OBJECT SUB-ENGINES
============================================================

--- FILE: /che-nu-sdk/core/object/catalog.engine.ts

/**
 * CHE·NU SDK — Object Catalog Engine
 * ====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Maintains a representational catalog of CHE·NU objects.
 * In-memory only, no persistence.
 * 
 * @module ObjectCatalogEngine
 * @version 1.0.0
 */

import type { CheNuObject, ObjectType, ObjectStatus, ObjectSummary } from '../object';
import { summarizeObject } from '../object';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Catalog structure
 */
export interface ObjectCatalog {
  id: string;
  name: string;
  description: string;
  objects: CheNuObject[];
  indexes: CatalogIndexes;
  metadata: {
    created_at: string;
    updated_at: string;
    total_objects: number;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noPersistence: true;
  };
}

/**
 * Catalog indexes for faster lookups
 */
export interface CatalogIndexes {
  byType: Map<ObjectType, string[]>;
  bySphere: Map<string, string[]>;
  byStatus: Map<ObjectStatus, string[]>;
  byTag: Map<string, string[]>;
  byProject: Map<string, string[]>;
  byMission: Map<string, string[]>;
}

/**
 * Catalog filter options
 */
export interface CatalogFilter {
  type?: ObjectType;
  sphere?: string;
  status?: ObjectStatus;
  tag?: string;
  projectId?: string;
  missionId?: string;
  searchTerm?: string;
}

/**
 * Catalog statistics
 */
export interface CatalogStats {
  total_objects: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  by_sphere: Record<string, number>;
  most_linked: { id: string; name: string; links: number }[];
  recent_additions: ObjectSummary[];
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateCatalogId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `cat_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a new object catalog
 */
export function createCatalog(name: string, description?: string): ObjectCatalog {
  return {
    id: generateCatalogId(),
    name,
    description: description || 'CHE·NU Object Catalog',
    objects: [],
    indexes: {
      byType: new Map(),
      bySphere: new Map(),
      byStatus: new Map(),
      byTag: new Map(),
      byProject: new Map(),
      byMission: new Map(),
    },
    metadata: {
      created_at: now(),
      updated_at: now(),
      total_objects: 0,
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPersistence: true,
    },
  };
}

/**
 * Add object to catalog
 */
export function addToCatalog(catalog: ObjectCatalog, object: CheNuObject): ObjectCatalog {
  // Check for duplicates
  if (catalog.objects.find(o => o.id === object.id)) {
    return catalog;
  }
  
  // Add object
  catalog.objects.push(object);
  
  // Update indexes
  updateIndexes(catalog, object, 'add');
  
  // Update metadata
  catalog.metadata.total_objects = catalog.objects.length;
  catalog.metadata.updated_at = now();
  
  return catalog;
}

/**
 * Remove object from catalog
 */
export function removeFromCatalog(catalog: ObjectCatalog, objectId: string): boolean {
  const index = catalog.objects.findIndex(o => o.id === objectId);
  
  if (index === -1) {
    return false;
  }
  
  const object = catalog.objects[index];
  
  // Update indexes
  updateIndexes(catalog, object, 'remove');
  
  // Remove object
  catalog.objects.splice(index, 1);
  
  // Update metadata
  catalog.metadata.total_objects = catalog.objects.length;
  catalog.metadata.updated_at = now();
  
  return true;
}

/**
 * Update catalog indexes
 */
function updateIndexes(
  catalog: ObjectCatalog, 
  object: CheNuObject, 
  action: 'add' | 'remove'
): void {
  const { indexes } = catalog;
  
  if (action === 'add') {
    // Type index
    const typeList = indexes.byType.get(object.type) || [];
    typeList.push(object.id);
    indexes.byType.set(object.type, typeList);
    
    // Sphere index
    object.sphereTags.forEach(sphere => {
      const sphereList = indexes.bySphere.get(sphere) || [];
      sphereList.push(object.id);
      indexes.bySphere.set(sphere, sphereList);
    });
    
    // Status index
    const statusList = indexes.byStatus.get(object.status) || [];
    statusList.push(object.id);
    indexes.byStatus.set(object.status, statusList);
    
    // Tag index
    object.tags.forEach(tag => {
      const tagList = indexes.byTag.get(tag) || [];
      tagList.push(object.id);
      indexes.byTag.set(tag, tagList);
    });
    
    // Project index
    object.projectIds.forEach(pid => {
      const projList = indexes.byProject.get(pid) || [];
      projList.push(object.id);
      indexes.byProject.set(pid, projList);
    });
    
    // Mission index
    object.missionIds.forEach(mid => {
      const missList = indexes.byMission.get(mid) || [];
      missList.push(object.id);
      indexes.byMission.set(mid, missList);
    });
  } else {
    // Remove from all indexes
    indexes.byType.get(object.type)?.filter(id => id !== object.id);
    indexes.byStatus.get(object.status)?.filter(id => id !== object.id);
    
    object.sphereTags.forEach(sphere => {
      const list = indexes.bySphere.get(sphere);
      if (list) {
        indexes.bySphere.set(sphere, list.filter(id => id !== object.id));
      }
    });
    
    object.tags.forEach(tag => {
      const list = indexes.byTag.get(tag);
      if (list) {
        indexes.byTag.set(tag, list.filter(id => id !== object.id));
      }
    });
    
    object.projectIds.forEach(pid => {
      const list = indexes.byProject.get(pid);
      if (list) {
        indexes.byProject.set(pid, list.filter(id => id !== object.id));
      }
    });
    
    object.missionIds.forEach(mid => {
      const list = indexes.byMission.get(mid);
      if (list) {
        indexes.byMission.set(mid, list.filter(id => id !== object.id));
      }
    });
  }
}

/**
 * List all objects in catalog
 */
export function listCatalog(catalog: ObjectCatalog): CheNuObject[] {
  return [...catalog.objects];
}

/**
 * Get catalog as summaries
 */
export function listCatalogSummaries(catalog: ObjectCatalog): ObjectSummary[] {
  return catalog.objects.map(summarizeObject);
}

/**
 * Find objects by type
 */
export function findByType(catalog: ObjectCatalog, type: ObjectType): CheNuObject[] {
  const ids = catalog.indexes.byType.get(type) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Find objects by sphere
 */
export function findBySphere(catalog: ObjectCatalog, sphere: string): CheNuObject[] {
  const ids = catalog.indexes.bySphere.get(sphere) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Find objects by status
 */
export function findByStatus(catalog: ObjectCatalog, status: ObjectStatus): CheNuObject[] {
  const ids = catalog.indexes.byStatus.get(status) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Find objects by tag
 */
export function findByTag(catalog: ObjectCatalog, tag: string): CheNuObject[] {
  const ids = catalog.indexes.byTag.get(tag) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Find objects by project
 */
export function findByProject(catalog: ObjectCatalog, projectId: string): CheNuObject[] {
  const ids = catalog.indexes.byProject.get(projectId) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Find objects by mission
 */
export function findByMission(catalog: ObjectCatalog, missionId: string): CheNuObject[] {
  const ids = catalog.indexes.byMission.get(missionId) || [];
  return catalog.objects.filter(o => ids.includes(o.id));
}

/**
 * Filter catalog with multiple criteria
 */
export function filterCatalog(
  catalog: ObjectCatalog, 
  filter: CatalogFilter
): CheNuObject[] {
  let results = [...catalog.objects];
  
  if (filter.type) {
    results = results.filter(o => o.type === filter.type);
  }
  
  if (filter.sphere) {
    results = results.filter(o => o.sphereTags.includes(filter.sphere!));
  }
  
  if (filter.status) {
    results = results.filter(o => o.status === filter.status);
  }
  
  if (filter.tag) {
    results = results.filter(o => o.tags.includes(filter.tag!));
  }
  
  if (filter.projectId) {
    results = results.filter(o => o.projectIds.includes(filter.projectId!));
  }
  
  if (filter.missionId) {
    results = results.filter(o => o.missionIds.includes(filter.missionId!));
  }
  
  if (filter.searchTerm) {
    const term = filter.searchTerm.toLowerCase();
    results = results.filter(o => 
      o.name.toLowerCase().includes(term) ||
      o.description.toLowerCase().includes(term) ||
      o.tags.some(t => t.toLowerCase().includes(term))
    );
  }
  
  return results;
}

/**
 * Get object by ID
 */
export function getById(catalog: ObjectCatalog, objectId: string): CheNuObject | undefined {
  return catalog.objects.find(o => o.id === objectId);
}

/**
 * Get catalog statistics
 */
export function getCatalogStats(catalog: ObjectCatalog): CatalogStats {
  const byType: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  const bySphere: Record<string, number> = {};
  
  catalog.indexes.byType.forEach((ids, type) => {
    byType[type] = ids.length;
  });
  
  catalog.indexes.byStatus.forEach((ids, status) => {
    byStatus[status] = ids.length;
  });
  
  catalog.indexes.bySphere.forEach((ids, sphere) => {
    bySphere[sphere] = ids.length;
  });
  
  // Most linked objects
  const mostLinked = catalog.objects
    .map(o => ({
      id: o.id,
      name: o.name,
      links: o.projectIds.length + o.missionIds.length + o.ownerAgentIds.length + o.engineRefs.length,
    }))
    .sort((a, b) => b.links - a.links)
    .slice(0, 5);
  
  // Recent additions (last 5)
  const recent = catalog.objects
    .sort((a, b) => new Date(b.metadata.created_at).getTime() - new Date(a.metadata.created_at).getTime())
    .slice(0, 5)
    .map(summarizeObject);
  
  return {
    total_objects: catalog.objects.length,
    by_type: byType,
    by_status: byStatus,
    by_sphere: bySphere,
    most_linked: mostLinked,
    recent_additions: recent,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectCatalogEngine',
    version: '1.0.0',
    description: 'In-memory catalog management for CHE·NU objects',
    parent: 'ObjectEngine',
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPersistence: true,
    },
  };
}

export default {
  createCatalog,
  addToCatalog,
  removeFromCatalog,
  listCatalog,
  listCatalogSummaries,
  findByType,
  findBySphere,
  findByStatus,
  findByTag,
  findByProject,
  findByMission,
  filterCatalog,
  getById,
  getCatalogStats,
  meta,
};

--- FILE: /che-nu-sdk/core/object/resource.engine.ts

/**
 * CHE·NU SDK — Object Resource Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Specializes in resource-type objects: documents, links, 
 * assets, media files (representational only).
 * 
 * @module ObjectResourceEngine
 * @version 1.0.0
 */

import type { CheNuObject, CreateObjectInput, ObjectContent } from '../object';
import { createObject } from '../object';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Resource classification
 */
export type ResourceClass = 
  | 'document'
  | 'media'
  | 'link'
  | 'data'
  | 'binary'
  | 'code'
  | 'configuration'
  | 'template';

/**
 * Document subtypes
 */
export type DocumentSubtype = 
  | 'pdf'
  | 'word'
  | 'spreadsheet'
  | 'presentation'
  | 'text'
  | 'markdown'
  | 'html'
  | 'json'
  | 'yaml'
  | 'xml';

/**
 * Media subtypes
 */
export type MediaSubtype = 
  | 'image'
  | 'video'
  | 'audio'
  | 'animation'
  | '3d-model';

/**
 * Resource object (extends CheNuObject)
 */
export interface ResourceObject extends CheNuObject {
  resourceClass: ResourceClass;
  resourceMeta: ResourceMeta;
}

/**
 * Resource metadata
 */
export interface ResourceMeta {
  mime_type?: string;
  file_extension?: string;
  encoding?: string;
  dimensions?: {
    width?: number;
    height?: number;
    duration?: number; // for media
    pages?: number;    // for documents
  };
  source_url?: string;
  local_reference?: string;
}

/**
 * Resource creation input
 */
export interface CreateResourceInput {
  name: string;
  description?: string;
  resourceClass: ResourceClass;
  subtype?: string;
  sphereTags?: string[];
  tags?: string[];
  mime_type?: string;
  file_extension?: string;
  source_url?: string;
  content?: Partial<ObjectContent>;
}

/**
 * Resource summary
 */
export interface ResourceSummary {
  id: string;
  name: string;
  class: ResourceClass;
  subtype?: string;
  mime_type?: string;
  size?: string;
  source?: string;
}

// ============================================================
// CLASSIFICATION RULES
// ============================================================

const MIME_TO_CLASS: Record<string, ResourceClass> = {
  'application/pdf': 'document',
  'application/msword': 'document',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'document',
  'application/vnd.ms-excel': 'document',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'document',
  'application/vnd.ms-powerpoint': 'document',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'document',
  'text/plain': 'document',
  'text/markdown': 'document',
  'text/html': 'document',
  'application/json': 'data',
  'application/xml': 'data',
  'text/yaml': 'configuration',
  'image/png': 'media',
  'image/jpeg': 'media',
  'image/gif': 'media',
  'image/svg+xml': 'media',
  'video/mp4': 'media',
  'video/webm': 'media',
  'audio/mpeg': 'media',
  'audio/wav': 'media',
  'model/gltf-binary': 'media',
  'model/gltf+json': 'media',
  'application/octet-stream': 'binary',
  'text/javascript': 'code',
  'text/typescript': 'code',
  'text/x-python': 'code',
};

const EXTENSION_TO_CLASS: Record<string, ResourceClass> = {
  '.pdf': 'document',
  '.doc': 'document',
  '.docx': 'document',
  '.xls': 'document',
  '.xlsx': 'document',
  '.ppt': 'document',
  '.pptx': 'document',
  '.txt': 'document',
  '.md': 'document',
  '.html': 'document',
  '.json': 'data',
  '.xml': 'data',
  '.yaml': 'configuration',
  '.yml': 'configuration',
  '.png': 'media',
  '.jpg': 'media',
  '.jpeg': 'media',
  '.gif': 'media',
  '.svg': 'media',
  '.mp4': 'media',
  '.webm': 'media',
  '.mp3': 'media',
  '.wav': 'media',
  '.glb': 'media',
  '.gltf': 'media',
  '.js': 'code',
  '.ts': 'code',
  '.py': 'code',
  '.exe': 'binary',
  '.bin': 'binary',
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a resource object
 */
export function createResourceObject(input: CreateResourceInput): ResourceObject {
  const baseObject = createObject({
    name: input.name,
    description: input.description,
    type: mapClassToObjectType(input.resourceClass),
    subtype: input.subtype,
    sphereTags: input.sphereTags,
    tags: input.tags || [],
    content: {
      format: input.mime_type || 'unknown',
      ...input.content,
    },
    metadata: {
      source: input.source_url,
    },
  });
  
  const resourceObject: ResourceObject = {
    ...baseObject,
    resourceClass: input.resourceClass,
    resourceMeta: {
      mime_type: input.mime_type,
      file_extension: input.file_extension,
      source_url: input.source_url,
    },
  };
  
  return resourceObject;
}

/**
 * Map resource class to object type
 */
function mapClassToObjectType(resourceClass: ResourceClass): 'document' | 'media' | 'link' | 'data' | 'asset' {
  switch (resourceClass) {
    case 'document':
    case 'template':
      return 'document';
    case 'media':
      return 'media';
    case 'link':
      return 'link';
    case 'data':
    case 'configuration':
      return 'data';
    case 'binary':
    case 'code':
    default:
      return 'asset';
  }
}

/**
 * Classify resource based on input hints
 */
export function classifyResource(input: {
  mime_type?: string;
  file_extension?: string;
  url?: string;
  name?: string;
}): ResourceClass {
  // Try MIME type first
  if (input.mime_type && MIME_TO_CLASS[input.mime_type]) {
    return MIME_TO_CLASS[input.mime_type];
  }
  
  // Try extension
  if (input.file_extension) {
    const ext = input.file_extension.startsWith('.') 
      ? input.file_extension.toLowerCase() 
      : `.${input.file_extension.toLowerCase()}`;
    if (EXTENSION_TO_CLASS[ext]) {
      return EXTENSION_TO_CLASS[ext];
    }
  }
  
  // Try URL detection
  if (input.url) {
    if (input.url.startsWith('http://') || input.url.startsWith('https://')) {
      return 'link';
    }
  }
  
  // Try name extension
  if (input.name) {
    const parts = input.name.split('.');
    if (parts.length > 1) {
      const ext = `.${parts[parts.length - 1].toLowerCase()}`;
      if (EXTENSION_TO_CLASS[ext]) {
        return EXTENSION_TO_CLASS[ext];
      }
    }
  }
  
  // Default
  return 'binary';
}

/**
 * Get resource summary
 */
export function resourceSummary(resource: ResourceObject): ResourceSummary {
  return {
    id: resource.id,
    name: resource.name,
    class: resource.resourceClass,
    subtype: resource.subtype,
    mime_type: resource.resourceMeta.mime_type,
    size: resource.content.size,
    source: resource.resourceMeta.source_url,
  };
}

/**
 * Create document resource shorthand
 */
export function createDocument(
  name: string,
  subtype: DocumentSubtype,
  options?: Partial<CreateResourceInput>
): ResourceObject {
  return createResourceObject({
    name,
    resourceClass: 'document',
    subtype,
    ...options,
  });
}

/**
 * Create media resource shorthand
 */
export function createMedia(
  name: string,
  subtype: MediaSubtype,
  options?: Partial<CreateResourceInput>
): ResourceObject {
  return createResourceObject({
    name,
    resourceClass: 'media',
    subtype,
    ...options,
  });
}

/**
 * Create link resource shorthand
 */
export function createLink(
  name: string,
  url: string,
  options?: Partial<CreateResourceInput>
): ResourceObject {
  return createResourceObject({
    name,
    resourceClass: 'link',
    source_url: url,
    ...options,
  });
}

/**
 * Update resource metadata
 */
export function updateResourceMeta(
  resource: ResourceObject,
  meta: Partial<ResourceMeta>
): ResourceObject {
  resource.resourceMeta = { ...resource.resourceMeta, ...meta };
  resource.metadata.updated_at = new Date().toISOString();
  return resource;
}

/**
 * Check if resource is media type
 */
export function isMedia(resource: ResourceObject): boolean {
  return resource.resourceClass === 'media';
}

/**
 * Check if resource is document type
 */
export function isDocument(resource: ResourceObject): boolean {
  return resource.resourceClass === 'document';
}

/**
 * Check if resource is linkable
 */
export function isLinkable(resource: ResourceObject): boolean {
  return resource.resourceClass === 'link' || !!resource.resourceMeta.source_url;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectResourceEngine',
    version: '1.0.0',
    description: 'Resource-type object specialization',
    parent: 'ObjectEngine',
    resourceClasses: ['document', 'media', 'link', 'data', 'binary', 'code', 'configuration', 'template'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  createResourceObject,
  classifyResource,
  resourceSummary,
  createDocument,
  createMedia,
  createLink,
  updateResourceMeta,
  isMedia,
  isDocument,
  isLinkable,
  meta,
};

--- FILE: /che-nu-sdk/core/object/inventory.engine.ts

/**
 * CHE·NU SDK — Object Inventory Engine
 * ======================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents collections of objects per user, agent, project,
 * or context. In-memory only.
 * 
 * @module ObjectInventoryEngine
 * @version 1.0.0
 */

import type { CheNuObject, ObjectSummary } from '../object';
import { summarizeObject } from '../object';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Inventory owner type
 */
export type InventoryOwnerType = 
  | 'user'
  | 'agent'
  | 'project'
  | 'mission'
  | 'sphere'
  | 'system';

/**
 * Inventory structure
 */
export interface ObjectInventory {
  id: string;
  name: string;
  ownerType: InventoryOwnerType;
  ownerId: string;
  objects: CheNuObject[];
  capacity?: number; // optional max capacity
  metadata: {
    created_at: string;
    updated_at: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noPersistence: true;
  };
}

/**
 * Inventory context for building
 */
export interface InventoryContext {
  ownerType: InventoryOwnerType;
  ownerId: string;
  name?: string;
  capacity?: number;
  initialObjects?: CheNuObject[];
}

/**
 * Inventory statistics
 */
export interface InventoryStats {
  total_items: number;
  capacity?: number;
  capacity_used?: string; // percentage
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  most_recent: ObjectSummary | null;
  oldest: ObjectSummary | null;
}

/**
 * Inventory comparison result
 */
export interface InventoryComparison {
  inventory_a_id: string;
  inventory_b_id: string;
  common_objects: string[];
  only_in_a: string[];
  only_in_b: string[];
  total_unique: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateInventoryId(ownerType: InventoryOwnerType): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `inv_${ownerType}_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Build a new inventory from context
 */
export function buildInventory(context: InventoryContext): ObjectInventory {
  return {
    id: generateInventoryId(context.ownerType),
    name: context.name || `${context.ownerType} Inventory`,
    ownerType: context.ownerType,
    ownerId: context.ownerId,
    objects: context.initialObjects ? [...context.initialObjects] : [],
    capacity: context.capacity,
    metadata: {
      created_at: now(),
      updated_at: now(),
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPersistence: true,
    },
  };
}

/**
 * Add object to inventory
 */
export function addToInventory(
  inventory: ObjectInventory, 
  object: CheNuObject
): { success: boolean; reason?: string } {
  // Check capacity
  if (inventory.capacity && inventory.objects.length >= inventory.capacity) {
    return { success: false, reason: 'Inventory at capacity' };
  }
  
  // Check duplicates
  if (inventory.objects.find(o => o.id === object.id)) {
    return { success: false, reason: 'Object already in inventory' };
  }
  
  inventory.objects.push(object);
  inventory.metadata.updated_at = now();
  
  return { success: true };
}

/**
 * Remove object from inventory
 */
export function removeFromInventory(
  inventory: ObjectInventory, 
  objectId: string
): { success: boolean; object?: CheNuObject } {
  const index = inventory.objects.findIndex(o => o.id === objectId);
  
  if (index === -1) {
    return { success: false };
  }
  
  const [removed] = inventory.objects.splice(index, 1);
  inventory.metadata.updated_at = now();
  
  return { success: true, object: removed };
}

/**
 * List all objects in inventory
 */
export function listInventory(inventory: ObjectInventory): CheNuObject[] {
  return [...inventory.objects];
}

/**
 * List inventory as summaries
 */
export function listInventorySummaries(inventory: ObjectInventory): ObjectSummary[] {
  return inventory.objects.map(summarizeObject);
}

/**
 * Get inventory statistics
 */
export function inventoryStats(inventory: ObjectInventory): InventoryStats {
  const byType: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  
  inventory.objects.forEach(obj => {
    byType[obj.type] = (byType[obj.type] || 0) + 1;
    byStatus[obj.status] = (byStatus[obj.status] || 0) + 1;
  });
  
  // Sort by date
  const sorted = [...inventory.objects].sort(
    (a, b) => new Date(b.metadata.created_at).getTime() - new Date(a.metadata.created_at).getTime()
  );
  
  const mostRecent = sorted.length > 0 ? summarizeObject(sorted[0]) : null;
  const oldest = sorted.length > 0 ? summarizeObject(sorted[sorted.length - 1]) : null;
  
  let capacityUsed: string | undefined;
  if (inventory.capacity) {
    capacityUsed = `${((inventory.objects.length / inventory.capacity) * 100).toFixed(1)}%`;
  }
  
  return {
    total_items: inventory.objects.length,
    capacity: inventory.capacity,
    capacity_used: capacityUsed,
    by_type: byType,
    by_status: byStatus,
    most_recent: mostRecent,
    oldest,
  };
}

/**
 * Find object in inventory by ID
 */
export function findInInventory(
  inventory: ObjectInventory, 
  objectId: string
): CheNuObject | undefined {
  return inventory.objects.find(o => o.id === objectId);
}

/**
 * Search inventory by criteria
 */
export function searchInventory(
  inventory: ObjectInventory,
  criteria: {
    type?: string;
    status?: string;
    tag?: string;
    searchTerm?: string;
  }
): CheNuObject[] {
  let results = [...inventory.objects];
  
  if (criteria.type) {
    results = results.filter(o => o.type === criteria.type);
  }
  
  if (criteria.status) {
    results = results.filter(o => o.status === criteria.status);
  }
  
  if (criteria.tag) {
    results = results.filter(o => o.tags.includes(criteria.tag!));
  }
  
  if (criteria.searchTerm) {
    const term = criteria.searchTerm.toLowerCase();
    results = results.filter(o =>
      o.name.toLowerCase().includes(term) ||
      o.description.toLowerCase().includes(term)
    );
  }
  
  return results;
}

/**
 * Transfer object between inventories
 */
export function transferObject(
  from: ObjectInventory,
  to: ObjectInventory,
  objectId: string
): { success: boolean; reason?: string } {
  const removeResult = removeFromInventory(from, objectId);
  
  if (!removeResult.success || !removeResult.object) {
    return { success: false, reason: 'Object not found in source inventory' };
  }
  
  const addResult = addToInventory(to, removeResult.object);
  
  if (!addResult.success) {
    // Rollback
    addToInventory(from, removeResult.object);
    return { success: false, reason: addResult.reason };
  }
  
  return { success: true };
}

/**
 * Compare two inventories
 */
export function compareInventories(
  inventoryA: ObjectInventory,
  inventoryB: ObjectInventory
): InventoryComparison {
  const idsA = new Set(inventoryA.objects.map(o => o.id));
  const idsB = new Set(inventoryB.objects.map(o => o.id));
  
  const common: string[] = [];
  const onlyA: string[] = [];
  const onlyB: string[] = [];
  
  idsA.forEach(id => {
    if (idsB.has(id)) {
      common.push(id);
    } else {
      onlyA.push(id);
    }
  });
  
  idsB.forEach(id => {
    if (!idsA.has(id)) {
      onlyB.push(id);
    }
  });
  
  return {
    inventory_a_id: inventoryA.id,
    inventory_b_id: inventoryB.id,
    common_objects: common,
    only_in_a: onlyA,
    only_in_b: onlyB,
    total_unique: common.length + onlyA.length + onlyB.length,
  };
}

/**
 * Merge two inventories
 */
export function mergeInventories(
  inventoryA: ObjectInventory,
  inventoryB: ObjectInventory,
  newName?: string
): ObjectInventory {
  const allObjects = [...inventoryA.objects];
  const seenIds = new Set(allObjects.map(o => o.id));
  
  inventoryB.objects.forEach(obj => {
    if (!seenIds.has(obj.id)) {
      allObjects.push(obj);
    }
  });
  
  return buildInventory({
    ownerType: 'system',
    ownerId: 'merged',
    name: newName || `Merged: ${inventoryA.name} + ${inventoryB.name}`,
    initialObjects: allObjects,
  });
}

/**
 * Clear inventory
 */
export function clearInventory(inventory: ObjectInventory): CheNuObject[] {
  const removed = [...inventory.objects];
  inventory.objects = [];
  inventory.metadata.updated_at = now();
  return removed;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectInventoryEngine',
    version: '1.0.0',
    description: 'Object collection/inventory management',
    parent: 'ObjectEngine',
    ownerTypes: ['user', 'agent', 'project', 'mission', 'sphere', 'system'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPersistence: true,
    },
  };
}

export default {
  buildInventory,
  addToInventory,
  removeFromInventory,
  listInventory,
  listInventorySummaries,
  inventoryStats,
  findInInventory,
  searchInventory,
  transferObject,
  compareInventories,
  mergeInventories,
  clearInventory,
  meta,
};

--- FILE: /che-nu-sdk/core/object/context.engine.ts

/**
 * CHE·NU SDK — Object Context Engine
 * ====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Connects objects with context: spheres, projects, missions,
 * agents, and engines.
 * 
 * @module ObjectContextEngine
 * @version 1.0.0
 */

import type { CheNuObject } from '../object';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Context link type
 */
export type ContextLinkType = 
  | 'sphere'
  | 'project'
  | 'mission'
  | 'agent'
  | 'engine';

/**
 * Context link
 */
export interface ContextLink {
  type: ContextLinkType;
  id: string;
  name?: string;
  relation: string; // e.g., "belongs_to", "used_by", "created_by"
  strength: 'strong' | 'moderate' | 'weak';
  metadata?: Record<string, unknown>;
}

/**
 * Object context map
 */
export interface ObjectContextMap {
  object_id: string;
  object_name: string;
  links: ContextLink[];
  context_depth: number;
  primary_sphere?: string;
  primary_project?: string;
}

/**
 * Contextual query result
 */
export interface ContextualQueryResult {
  query_type: ContextLinkType;
  query_id: string;
  matching_objects: string[];
  total_matches: number;
}

/**
 * Context relationship
 */
export interface ContextRelationship {
  source_object_id: string;
  target_object_id: string;
  shared_contexts: ContextLink[];
  relationship_strength: number; // 0-1
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Map all context links for an object
 */
export function mapObjectContext(object: CheNuObject): ObjectContextMap {
  const links: ContextLink[] = [];
  
  // Sphere links
  object.sphereTags.forEach(sphere => {
    links.push({
      type: 'sphere',
      id: sphere,
      relation: 'tagged_with',
      strength: 'strong',
    });
  });
  
  // Project links
  object.projectIds.forEach(pid => {
    links.push({
      type: 'project',
      id: pid,
      relation: 'belongs_to',
      strength: 'strong',
    });
  });
  
  // Mission links
  object.missionIds.forEach(mid => {
    links.push({
      type: 'mission',
      id: mid,
      relation: 'used_in',
      strength: 'moderate',
    });
  });
  
  // Agent links
  object.ownerAgentIds.forEach(aid => {
    links.push({
      type: 'agent',
      id: aid,
      relation: 'owned_by',
      strength: 'strong',
    });
  });
  
  // Engine links
  object.engineRefs.forEach(eid => {
    links.push({
      type: 'engine',
      id: eid,
      relation: 'processed_by',
      strength: 'moderate',
    });
  });
  
  return {
    object_id: object.id,
    object_name: object.name,
    links,
    context_depth: links.length,
    primary_sphere: object.sphereTags[0],
    primary_project: object.projectIds[0],
  };
}

/**
 * List all contextual links for an object
 */
export function listContextualLinks(object: CheNuObject): ContextLink[] {
  return mapObjectContext(object).links;
}

/**
 * Get links by type
 */
export function getLinksByType(
  object: CheNuObject, 
  type: ContextLinkType
): ContextLink[] {
  return listContextualLinks(object).filter(link => link.type === type);
}

/**
 * Check if object has context link
 */
export function hasContextLink(
  object: CheNuObject,
  type: ContextLinkType,
  targetId: string
): boolean {
  switch (type) {
    case 'sphere':
      return object.sphereTags.includes(targetId);
    case 'project':
      return object.projectIds.includes(targetId);
    case 'mission':
      return object.missionIds.includes(targetId);
    case 'agent':
      return object.ownerAgentIds.includes(targetId);
    case 'engine':
      return object.engineRefs.includes(targetId);
    default:
      return false;
  }
}

/**
 * Calculate context overlap between two objects
 */
export function calculateContextOverlap(
  objectA: CheNuObject,
  objectB: CheNuObject
): ContextRelationship {
  const sharedContexts: ContextLink[] = [];
  
  // Check sphere overlap
  objectA.sphereTags.forEach(sphere => {
    if (objectB.sphereTags.includes(sphere)) {
      sharedContexts.push({
        type: 'sphere',
        id: sphere,
        relation: 'shared',
        strength: 'strong',
      });
    }
  });
  
  // Check project overlap
  objectA.projectIds.forEach(pid => {
    if (objectB.projectIds.includes(pid)) {
      sharedContexts.push({
        type: 'project',
        id: pid,
        relation: 'shared',
        strength: 'strong',
      });
    }
  });
  
  // Check mission overlap
  objectA.missionIds.forEach(mid => {
    if (objectB.missionIds.includes(mid)) {
      sharedContexts.push({
        type: 'mission',
        id: mid,
        relation: 'shared',
        strength: 'moderate',
      });
    }
  });
  
  // Check agent overlap
  objectA.ownerAgentIds.forEach(aid => {
    if (objectB.ownerAgentIds.includes(aid)) {
      sharedContexts.push({
        type: 'agent',
        id: aid,
        relation: 'shared',
        strength: 'moderate',
      });
    }
  });
  
  // Check engine overlap
  objectA.engineRefs.forEach(eid => {
    if (objectB.engineRefs.includes(eid)) {
      sharedContexts.push({
        type: 'engine',
        id: eid,
        relation: 'shared',
        strength: 'weak',
      });
    }
  });
  
  // Calculate strength
  const totalLinksA = 
    objectA.sphereTags.length +
    objectA.projectIds.length +
    objectA.missionIds.length +
    objectA.ownerAgentIds.length +
    objectA.engineRefs.length;
  
  const totalLinksB = 
    objectB.sphereTags.length +
    objectB.projectIds.length +
    objectB.missionIds.length +
    objectB.ownerAgentIds.length +
    objectB.engineRefs.length;
  
  const maxPossible = Math.max(totalLinksA, totalLinksB);
  const strength = maxPossible > 0 ? sharedContexts.length / maxPossible : 0;
  
  return {
    source_object_id: objectA.id,
    target_object_id: objectB.id,
    shared_contexts: sharedContexts,
    relationship_strength: Math.round(strength * 100) / 100,
  };
}

/**
 * Find objects by context from a list
 */
export function findByContext(
  objects: CheNuObject[],
  type: ContextLinkType,
  targetId: string
): ContextualQueryResult {
  const matching = objects.filter(obj => hasContextLink(obj, type, targetId));
  
  return {
    query_type: type,
    query_id: targetId,
    matching_objects: matching.map(o => o.id),
    total_matches: matching.length,
  };
}

/**
 * Get context summary for an object
 */
export function getContextSummary(object: CheNuObject): {
  spheres: number;
  projects: number;
  missions: number;
  agents: number;
  engines: number;
  total: number;
  primary_context: string;
} {
  const total = 
    object.sphereTags.length +
    object.projectIds.length +
    object.missionIds.length +
    object.ownerAgentIds.length +
    object.engineRefs.length;
  
  // Determine primary context
  let primary = 'none';
  if (object.projectIds.length > 0) {
    primary = `project:${object.projectIds[0]}`;
  } else if (object.sphereTags.length > 0) {
    primary = `sphere:${object.sphereTags[0]}`;
  } else if (object.ownerAgentIds.length > 0) {
    primary = `agent:${object.ownerAgentIds[0]}`;
  }
  
  return {
    spheres: object.sphereTags.length,
    projects: object.projectIds.length,
    missions: object.missionIds.length,
    agents: object.ownerAgentIds.length,
    engines: object.engineRefs.length,
    total,
    primary_context: primary,
  };
}

/**
 * Suggest context links based on object type and tags
 */
export function suggestContextLinks(object: CheNuObject): ContextLink[] {
  const suggestions: ContextLink[] = [];
  
  // Suggest spheres based on type
  const typeToSphere: Record<string, string[]> = {
    'document': ['Scholar', 'Business'],
    'media': ['Creative', 'Personal'],
    'xr-object': ['Creative', 'XR'],
    'tool': ['Projets', 'Business'],
    'concept': ['Scholar', 'Personal'],
    'data': ['Business', 'Projets'],
  };
  
  const suggestedSpheres = typeToSphere[object.type] || ['Personal'];
  suggestedSpheres.forEach(sphere => {
    if (!object.sphereTags.includes(sphere)) {
      suggestions.push({
        type: 'sphere',
        id: sphere,
        relation: 'suggested',
        strength: 'weak',
        metadata: { reason: `Based on object type: ${object.type}` },
      });
    }
  });
  
  return suggestions;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectContextEngine',
    version: '1.0.0',
    description: 'Object context mapping and relationship analysis',
    parent: 'ObjectEngine',
    contextTypes: ['sphere', 'project', 'mission', 'agent', 'engine'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  mapObjectContext,
  listContextualLinks,
  getLinksByType,
  hasContextLink,
  calculateContextOverlap,
  findByContext,
  getContextSummary,
  suggestContextLinks,
  meta,
};
