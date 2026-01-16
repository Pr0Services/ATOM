/**
 * CHE·NU Demo System V51
 * Incident Mode - Forensic Event Viewer
 */

import React, { useState, useMemo } from 'react';

interface SystemEvent {
  event_id: string;
  event_type: string;
  category: string;
  timestamp: string;
  actor: string;
  module_id?: string;
  severity: string;
  payload: any;
}

interface IncidentModeProps {
  events: SystemEvent[];
  onEventSelect?: (event: SystemEvent) => void;
  onExport?: (events: SystemEvent[]) => void;
}

export const IncidentMode: React.FC<IncidentModeProps> = ({
  events,
  onEventSelect,
  onExport
}) => {
  const [selectedEvent, setSelectedEvent] = useState<SystemEvent | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [severityFilter, setSeverityFilter] = useState<string>('all');
  const [flaggedEvents, setFlaggedEvents] = useState<Set<string>>(new Set());

  const categories = ['all', 'navigation', 'module', 'proposal', 'memory', 'demo', 'export', 'system', 'error'];
  const severities = ['all', 'debug', 'info', 'warning', 'error', 'critical'];

  const filteredEvents = useMemo(() => {
    return events.filter(event => {
      const matchesCategory = categoryFilter === 'all' || event.category === categoryFilter;
      const matchesSeverity = severityFilter === 'all' || event.severity === severityFilter;
      return matchesCategory && matchesSeverity;
    });
  }, [events, categoryFilter, severityFilter]);

  const handleEventClick = (event: SystemEvent) => {
    setSelectedEvent(event);
    onEventSelect?.(event);
  };

  const toggleFlag = (eventId: string) => {
    setFlaggedEvents(prev => {
      const next = new Set(prev);
      if (next.has(eventId)) {
        next.delete(eventId);
      } else {
        next.add(eventId);
      }
      return next;
    });
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerLeft}>
          <h1 style={styles.title}>🚨 Mode Incident</h1>
          <span style={styles.badge}>FORENSIQUE</span>
        </div>
        <div style={styles.headerRight}>
          <span style={styles.eventCount}>{filteredEvents.length} événements</span>
          <button 
            onClick={() => onExport?.(filteredEvents)}
            style={styles.exportButton}
          >
            📤 Exporter
          </button>
        </div>
      </header>

      {/* Filters */}
      <div style={styles.filters}>
        <div style={styles.filterGroup}>
          <label>Catégorie:</label>
          <select 
            value={categoryFilter} 
            onChange={(e) => setCategoryFilter(e.target.value)}
            style={styles.select}
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat === 'all' ? 'Toutes' : cat}</option>
            ))}
          </select>
        </div>
        <div style={styles.filterGroup}>
          <label>Sévérité:</label>
          <select 
            value={severityFilter} 
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={styles.select}
          >
            {severities.map(sev => (
              <option key={sev} value={sev}>{sev === 'all' ? 'Toutes' : sev}</option>
            ))}
          </select>
        </div>
        {flaggedEvents.size > 0 && (
          <span style={styles.flaggedCount}>🚩 {flaggedEvents.size} marqués</span>
        )}
      </div>

      <div style={styles.main}>
        {/* Timeline */}
        <div style={styles.timeline}>
          {filteredEvents.map((event, index) => (
            <div
              key={event.event_id}
              onClick={() => handleEventClick(event)}
              style={{
                ...styles.eventRow,
                backgroundColor: selectedEvent?.event_id === event.event_id ? '#2a2a4a' : 
                                 flaggedEvents.has(event.event_id) ? '#4a2a2a' : 'transparent',
                borderLeftColor: getSeverityColor(event.severity)
              }}
            >
              <span style={styles.eventIndex}>#{index + 1}</span>
              <span style={styles.eventTime}>
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
              <span style={{
                ...styles.severityBadge,
                backgroundColor: getSeverityColor(event.severity)
              }}>
                {event.severity}
              </span>
              <span style={styles.eventType}>{event.event_type}</span>
              <span style={styles.eventCategory}>{event.category}</span>
              <button
                onClick={(e) => { e.stopPropagation(); toggleFlag(event.event_id); }}
                style={{
                  ...styles.flagButton,
                  color: flaggedEvents.has(event.event_id) ? '#ff6b6b' : '#666'
                }}
              >
                🚩
              </button>
            </div>
          ))}
        </div>

        {/* Detail Panel */}
        {selectedEvent && (
          <aside style={styles.detailPanel}>
            <div style={styles.detailHeader}>
              <h3>Détail Événement</h3>
              <button onClick={() => setSelectedEvent(null)} style={styles.closeButton}>×</button>
            </div>
            <div style={styles.detailContent}>
              <div style={styles.detailRow}>
                <label>ID:</label>
                <code>{selectedEvent.event_id}</code>
              </div>
              <div style={styles.detailRow}>
                <label>Type:</label>
                <span>{selectedEvent.event_type}</span>
              </div>
              <div style={styles.detailRow}>
                <label>Catégorie:</label>
                <span>{selectedEvent.category}</span>
              </div>
              <div style={styles.detailRow}>
                <label>Sévérité:</label>
                <span style={{
                  ...styles.severityBadge,
                  backgroundColor: getSeverityColor(selectedEvent.severity)
                }}>
                  {selectedEvent.severity}
                </span>
              </div>
              <div style={styles.detailRow}>
                <label>Timestamp:</label>
                <span>{new Date(selectedEvent.timestamp).toLocaleString()}</span>
              </div>
              <div style={styles.detailRow}>
                <label>Acteur:</label>
                <span>{selectedEvent.actor}</span>
              </div>
              {selectedEvent.module_id && (
                <div style={styles.detailRow}>
                  <label>Module:</label>
                  <span>{selectedEvent.module_id}</span>
                </div>
              )}
              <div style={styles.payloadSection}>
                <label>Payload:</label>
                <pre style={styles.payload}>
                  {JSON.stringify(selectedEvent.payload, null, 2)}
                </pre>
              </div>
            </div>
          </aside>
        )}
      </div>

      {/* Tree Laws Status */}
      <footer style={styles.footer}>
        <div style={styles.treeLawsStatus}>
          <span>🌳 Tree Law 3: Total Transparency</span>
          <span style={styles.statusOk}>✓ {events.length} événements tracés</span>
        </div>
      </footer>
    </div>
  );
};

function getSeverityColor(severity: string): string {
  const colors: Record<string, string> = {
    debug: '#666666',
    info: '#4a9eff',
    warning: '#ffb74d',
    error: '#e57373',
    critical: '#ff1744'
  };
  return colors[severity] || '#666';
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    backgroundColor: '#0d0d0d',
    color: '#e0e0e0',
    fontFamily: "'Courier New', monospace"
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px 20px',
    borderBottom: '1px solid #4a2a2a',
    backgroundColor: '#1a0a0a'
  },
  headerLeft: { display: 'flex', alignItems: 'center', gap: '15px' },
  headerRight: { display: 'flex', alignItems: 'center', gap: '15px' },
  title: { fontSize: '18px', fontWeight: 'bold', margin: 0, color: '#ff6b6b' },
  badge: {
    fontSize: '10px',
    padding: '3px 8px',
    backgroundColor: '#4a2a2a',
    borderRadius: '4px',
    color: '#ff9999'
  },
  eventCount: { fontSize: '13px', color: '#888' },
  exportButton: {
    padding: '8px 16px',
    backgroundColor: '#4a2a2a',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  filters: {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
    padding: '10px 20px',
    borderBottom: '1px solid #333',
    backgroundColor: '#1a0a0a'
  },
  filterGroup: { display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px' },
  select: {
    padding: '5px 10px',
    backgroundColor: '#2a1a1a',
    border: '1px solid #4a2a2a',
    borderRadius: '4px',
    color: '#e0e0e0',
    fontSize: '12px'
  },
  flaggedCount: { marginLeft: 'auto', color: '#ff6b6b', fontSize: '13px' },
  main: { display: 'flex', flex: 1, overflow: 'hidden' },
  timeline: { flex: 1, overflow: 'auto', padding: '10px' },
  eventRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    padding: '8px 12px',
    borderLeft: '3px solid',
    marginBottom: '2px',
    cursor: 'pointer',
    fontSize: '12px',
    transition: 'background-color 0.2s'
  },
  eventIndex: { color: '#666', width: '40px' },
  eventTime: { color: '#888', width: '80px', fontFamily: 'monospace' },
  severityBadge: {
    padding: '2px 6px',
    borderRadius: '4px',
    fontSize: '10px',
    color: '#fff',
    textTransform: 'uppercase',
    width: '60px',
    textAlign: 'center'
  },
  eventType: { flex: 1 },
  eventCategory: { color: '#666', width: '100px' },
  flagButton: {
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    fontSize: '14px'
  },
  detailPanel: {
    width: '350px',
    borderLeft: '1px solid #4a2a2a',
    backgroundColor: '#1a0a0a',
    overflow: 'auto'
  },
  detailHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    borderBottom: '1px solid #4a2a2a'
  },
  closeButton: {
    background: 'none',
    border: 'none',
    color: '#888',
    fontSize: '20px',
    cursor: 'pointer'
  },
  detailContent: { padding: '15px' },
  detailRow: { marginBottom: '12px', fontSize: '12px' },
  payloadSection: { marginTop: '15px' },
  payload: {
    backgroundColor: '#0a0a0a',
    padding: '10px',
    borderRadius: '4px',
    fontSize: '11px',
    overflow: 'auto',
    maxHeight: '300px'
  },
  footer: {
    padding: '10px 20px',
    borderTop: '1px solid #4a2a2a',
    backgroundColor: '#1a0a0a'
  },
  treeLawsStatus: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '12px',
    color: '#81c784'
  },
  statusOk: { color: '#81c784' }
};

export default IncidentMode;
