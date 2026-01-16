/**
 * CHE·NU Demo System V51
 * Memory Inspector - Read-Only Memory Browser
 */

import React, { useState, useEffect, useMemo } from 'react';

// Types
interface MemoryUnit {
  unit_id: string;
  type: string;
  sphere: string;
  content: {
    title: string;
    summary: string;
  };
  relations: Array<{ target: string; type: string; strength: number }>;
  tags: string[];
  confidence: number;
  status: string;
}

interface Sphere {
  sphere_id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
  unit_count: number;
}

interface MemoryInspectorProps {
  units: MemoryUnit[];
  spheres: Record<string, Sphere>;
  onUnitSelect?: (unit: MemoryUnit) => void;
}

export const MemoryInspector: React.FC<MemoryInspectorProps> = ({
  units,
  spheres,
  onUnitSelect
}) => {
  const [selectedSphere, setSelectedSphere] = useState<string | null>(null);
  const [selectedUnit, setSelectedUnit] = useState<MemoryUnit | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'list' | 'grid' | 'graph'>('list');

  // Filter units
  const filteredUnits = useMemo(() => {
    return units.filter(unit => {
      const matchesSphere = !selectedSphere || unit.sphere === selectedSphere;
      const matchesSearch = !searchQuery || 
        unit.content.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        unit.unit_id.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesSphere && matchesSearch;
    });
  }, [units, selectedSphere, searchQuery]);

  const handleUnitClick = (unit: MemoryUnit) => {
    setSelectedUnit(unit);
    onUnitSelect?.(unit);
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerLeft}>
          <h1 style={styles.title}>🔍 Inspecteur Mémoire</h1>
          <span style={styles.badge}>LECTURE SEULE</span>
        </div>
        <div style={styles.headerRight}>
          <input
            type="text"
            placeholder="Rechercher..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={styles.searchInput}
          />
          <div style={styles.viewToggle}>
            <button 
              onClick={() => setViewMode('list')}
              style={{...styles.viewButton, backgroundColor: viewMode === 'list' ? '#4a9eff' : 'transparent'}}
            >
              ☰
            </button>
            <button 
              onClick={() => setViewMode('grid')}
              style={{...styles.viewButton, backgroundColor: viewMode === 'grid' ? '#4a9eff' : 'transparent'}}
            >
              ⊞
            </button>
            <button 
              onClick={() => setViewMode('graph')}
              style={{...styles.viewButton, backgroundColor: viewMode === 'graph' ? '#4a9eff' : 'transparent'}}
            >
              ◉
            </button>
          </div>
        </div>
      </header>

      <div style={styles.main}>
        {/* Spheres Sidebar */}
        <aside style={styles.spheresSidebar}>
          <h3 style={styles.sidebarTitle}>Sphères</h3>
          <button
            onClick={() => setSelectedSphere(null)}
            style={{
              ...styles.sphereButton,
              backgroundColor: !selectedSphere ? '#2a2a4a' : 'transparent'
            }}
          >
            <span>🌐</span>
            <span>Toutes ({units.length})</span>
          </button>
          {Object.values(spheres).map(sphere => (
            <button
              key={sphere.sphere_id}
              onClick={() => setSelectedSphere(sphere.sphere_id.replace('SPH_', '').toLowerCase())}
              style={{
                ...styles.sphereButton,
                backgroundColor: selectedSphere === sphere.sphere_id.replace('SPH_', '').toLowerCase() 
                  ? sphere.color + '33' 
                  : 'transparent',
                borderLeftColor: sphere.color
              }}
            >
              <span>{sphere.icon}</span>
              <span>{sphere.name}</span>
              <span style={styles.sphereCount}>{sphere.unit_count}</span>
            </button>
          ))}
        </aside>

        {/* Units List */}
        <div style={styles.unitsList}>
          <div style={styles.unitsHeader}>
            <span>{filteredUnits.length} unités</span>
          </div>
          <div style={viewMode === 'grid' ? styles.unitsGrid : styles.unitsListView}>
            {filteredUnits.map(unit => (
              <div
                key={unit.unit_id}
                onClick={() => handleUnitClick(unit)}
                style={{
                  ...styles.unitCard,
                  borderLeftColor: spheres[`SPH_${unit.sphere.toUpperCase()}`]?.color || '#666',
                  backgroundColor: selectedUnit?.unit_id === unit.unit_id ? '#2a2a4a' : '#1a1a2e'
                }}
              >
                <div style={styles.unitHeader}>
                  <span style={styles.unitId}>{unit.unit_id}</span>
                  <span style={{
                    ...styles.typeBadge,
                    backgroundColor: getTypeColor(unit.type)
                  }}>
                    {unit.type}
                  </span>
                </div>
                <h4 style={styles.unitTitle}>{unit.content.title}</h4>
                <p style={styles.unitSummary}>{unit.content.summary}</p>
                <div style={styles.unitMeta}>
                  <span>Confiance: {Math.round(unit.confidence * 100)}%</span>
                  <span>{unit.relations.length} relations</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Detail Panel */}
        {selectedUnit && (
          <aside style={styles.detailPanel}>
            <div style={styles.detailHeader}>
              <h3>{selectedUnit.content.title}</h3>
              <button onClick={() => setSelectedUnit(null)} style={styles.closeButton}>×</button>
            </div>
            <div style={styles.detailContent}>
              <div style={styles.detailSection}>
                <label>ID</label>
                <code>{selectedUnit.unit_id}</code>
              </div>
              <div style={styles.detailSection}>
                <label>Type</label>
                <span>{selectedUnit.type}</span>
              </div>
              <div style={styles.detailSection}>
                <label>Sphère</label>
                <span>{selectedUnit.sphere}</span>
              </div>
              <div style={styles.detailSection}>
                <label>Status</label>
                <span>{selectedUnit.status}</span>
              </div>
              <div style={styles.detailSection}>
                <label>Confiance</label>
                <span>{Math.round(selectedUnit.confidence * 100)}%</span>
              </div>
              <div style={styles.detailSection}>
                <label>Résumé</label>
                <p>{selectedUnit.content.summary}</p>
              </div>
              <div style={styles.detailSection}>
                <label>Relations ({selectedUnit.relations.length})</label>
                <ul style={styles.relationsList}>
                  {selectedUnit.relations.map((rel, i) => (
                    <li key={i}>
                      {rel.type} → {rel.target} ({Math.round(rel.strength * 100)}%)
                    </li>
                  ))}
                </ul>
              </div>
              <div style={styles.detailSection}>
                <label>Tags</label>
                <div style={styles.tagsList}>
                  {selectedUnit.tags.map(tag => (
                    <span key={tag} style={styles.tag}>{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};

function getTypeColor(type: string): string {
  const colors: Record<string, string> = {
    core: '#4a9eff',
    system: '#4a9eff',
    agent: '#9e4aff',
    project: '#ff9e4a',
    knowledge: '#4dd0e1',
    config: '#81c784',
    module: '#e57373',
    contract: '#ffb74d',
    demo: '#ba68c8'
  };
  return colors[type] || '#666';
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    backgroundColor: '#0a0a1a',
    color: '#e0e0e0'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px 20px',
    borderBottom: '1px solid #333',
    backgroundColor: '#0f0f1a'
  },
  headerLeft: { display: 'flex', alignItems: 'center', gap: '15px' },
  headerRight: { display: 'flex', alignItems: 'center', gap: '15px' },
  title: { fontSize: '18px', fontWeight: 'bold', margin: 0 },
  badge: {
    fontSize: '10px',
    padding: '3px 8px',
    backgroundColor: '#6a4a4a',
    borderRadius: '4px',
    color: '#ffa0a0'
  },
  searchInput: {
    padding: '8px 12px',
    fontSize: '13px',
    backgroundColor: '#1a1a2e',
    border: '1px solid #333',
    borderRadius: '4px',
    color: '#e0e0e0',
    width: '200px'
  },
  viewToggle: { display: 'flex', gap: '4px' },
  viewButton: {
    padding: '6px 10px',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  main: { display: 'flex', flex: 1, overflow: 'hidden' },
  spheresSidebar: {
    width: '200px',
    padding: '15px',
    borderRight: '1px solid #333',
    backgroundColor: '#0f0f1a',
    overflow: 'auto'
  },
  sidebarTitle: { fontSize: '12px', color: '#888', marginBottom: '10px', textTransform: 'uppercase' },
  sphereButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    width: '100%',
    padding: '10px',
    border: 'none',
    borderLeft: '3px solid transparent',
    borderRadius: '0 4px 4px 0',
    color: '#e0e0e0',
    cursor: 'pointer',
    textAlign: 'left',
    marginBottom: '4px'
  },
  sphereCount: { marginLeft: 'auto', fontSize: '11px', color: '#666' },
  unitsList: { flex: 1, padding: '15px', overflow: 'auto' },
  unitsHeader: { marginBottom: '15px', fontSize: '13px', color: '#888' },
  unitsListView: { display: 'flex', flexDirection: 'column', gap: '10px' },
  unitsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '15px' },
  unitCard: {
    padding: '15px',
    backgroundColor: '#1a1a2e',
    borderRadius: '8px',
    borderLeft: '3px solid',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  },
  unitHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' },
  unitId: { fontSize: '11px', fontFamily: 'monospace', color: '#666' },
  typeBadge: { fontSize: '10px', padding: '2px 6px', borderRadius: '4px', color: '#fff' },
  unitTitle: { fontSize: '14px', margin: '0 0 6px 0' },
  unitSummary: { fontSize: '12px', color: '#888', margin: 0 },
  unitMeta: { display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '11px', color: '#666' },
  detailPanel: {
    width: '320px',
    borderLeft: '1px solid #333',
    backgroundColor: '#0f0f1a',
    overflow: 'auto'
  },
  detailHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    borderBottom: '1px solid #333'
  },
  closeButton: {
    background: 'none',
    border: 'none',
    color: '#888',
    fontSize: '20px',
    cursor: 'pointer'
  },
  detailContent: { padding: '15px' },
  detailSection: { marginBottom: '15px' },
  relationsList: { listStyle: 'none', padding: 0, margin: 0, fontSize: '12px' },
  tagsList: { display: 'flex', flexWrap: 'wrap', gap: '5px' },
  tag: {
    fontSize: '10px',
    padding: '2px 8px',
    backgroundColor: '#2a2a4a',
    borderRadius: '10px'
  }
};

export default MemoryInspector;
