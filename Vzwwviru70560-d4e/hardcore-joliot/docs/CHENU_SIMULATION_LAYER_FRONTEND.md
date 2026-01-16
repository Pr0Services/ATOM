############################################################
#                                                          #
#       CHE·NU SIMULATION LAYER                            #
#       PART 2: FRONTEND PAGE + VIEWER                     #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A7 — FRONTEND: SIMULATION PAGE
============================================================

--- FILE: /che-nu-frontend/pages/simulation.tsx

/**
 * CHE·NU Frontend — Simulation Tools Page
 * =========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Simulation visualization and what-if exploration.
 * All simulations are representational only — no predictions.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { SimulationViewer } from '../components/SimulationViewer';

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

const SUBJECT_TYPE_ICONS: Record<string, string> = {
  project: '📋',
  mission: '🎯',
  process: '🔄',
  persona: '👤',
  workflow: '⚡',
  pipeline: '🔗',
};

const SUBJECT_TYPE_COLORS: Record<string, string> = {
  project: COLORS.jungleEmerald,
  mission: COLORS.sacredGold,
  process: COLORS.cenoteTurquoise,
  persona: COLORS.earthEmber,
  workflow: COLORS.shadowMoss,
  pipeline: COLORS.ancientStone,
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface SimulationFrame {
  id: string;
  timestamp: number;
  state_id: string;
  description: string;
  involved_engines: string[];
  involved_agents: string[];
  inputs: string[];
  outputs: string[];
}

interface SimulationBranch {
  id: string;
  name: string;
  description: string;
  branch_point: number;
  condition: string;
  frames: SimulationFrame[];
  probability_weight: number;
}

interface SimulationRun {
  id: string;
  name: string;
  subject_type: string;
  subject_id: string;
  subject_name: string;
  main_timeline: SimulationFrame[];
  branches: SimulationBranch[];
  total_frames: number;
  total_branches: number;
  engines_involved: string[];
  agents_involved: string[];
  created_at: string;
}

interface SubjectOption {
  id: string;
  name: string;
  type: string;
  description: string;
}

// ============================================================
// SAMPLE DATA
// ============================================================

const SAMPLE_SUBJECTS: SubjectOption[] = [
  { id: 'proj_1', name: 'CHE·NU Platform', type: 'project', description: 'Main platform development' },
  { id: 'proc_1', name: 'Research Pipeline', type: 'process', description: 'Standard research workflow' },
  { id: 'mission_1', name: 'SDK Development', type: 'mission', description: 'Build core SDK modules' },
  { id: 'persona_1', name: 'Analyst Persona', type: 'persona', description: 'Data-focused work style' },
];

const SAMPLE_SIMULATION: SimulationRun = {
  id: 'sim_abc123_def456',
  name: 'Simulation: Research Pipeline',
  subject_type: 'process',
  subject_id: 'proc_1',
  subject_name: 'Research Pipeline',
  main_timeline: [
    {
      id: 'frame_0',
      timestamp: 0,
      state_id: 'START',
      description: 'Begin process: Research Pipeline',
      involved_engines: [],
      involved_agents: [],
      inputs: [],
      outputs: [],
    },
    {
      id: 'frame_1',
      timestamp: 1,
      state_id: 'step_1',
      description: 'Define Research Question',
      involved_engines: ['KnowledgeEngine'],
      involved_agents: ['ResearchLead'],
      inputs: [],
      outputs: ['research_question'],
    },
    {
      id: 'frame_2',
      timestamp: 2,
      state_id: 'step_2',
      description: 'Conduct Literature Review',
      involved_engines: ['KnowledgeEngine', 'ContentEngine'],
      involved_agents: ['Researcher'],
      inputs: ['research_question'],
      outputs: ['literature_review'],
    },
    {
      id: 'frame_3',
      timestamp: 3,
      state_id: 'step_3',
      description: 'Collect Data',
      involved_engines: ['DataEngine'],
      involved_agents: ['DataAnalyst'],
      inputs: ['methodology'],
      outputs: ['raw_data'],
    },
    {
      id: 'frame_4',
      timestamp: 4,
      state_id: 'step_4',
      description: 'Analyze Data',
      involved_engines: ['AnalysisEngine', 'DataEngine'],
      involved_agents: ['DataAnalyst', 'Researcher'],
      inputs: ['raw_data'],
      outputs: ['analysis_results'],
    },
    {
      id: 'frame_5',
      timestamp: 5,
      state_id: 'step_5',
      description: 'Synthesize Findings',
      involved_engines: ['ContentEngine', 'KnowledgeEngine'],
      involved_agents: ['ResearchLead'],
      inputs: ['analysis_results', 'literature_review'],
      outputs: ['research_findings'],
    },
    {
      id: 'frame_6',
      timestamp: 6,
      state_id: 'END',
      description: 'Complete process: Research Pipeline',
      involved_engines: [],
      involved_agents: [],
      inputs: [],
      outputs: ['final_output'],
    },
  ],
  branches: [
    {
      id: 'branch_1',
      name: 'Insufficient Data Branch',
      description: 'Alternative path when data collection is insufficient',
      branch_point: 3,
      condition: 'insufficient_data',
      frames: [
        {
          id: 'branch_frame_1',
          timestamp: 3,
          state_id: 'alt_step_3a',
          description: 'Data insufficient — expand collection scope',
          involved_engines: ['DataEngine'],
          involved_agents: ['DataAnalyst'],
          inputs: ['methodology'],
          outputs: ['expanded_scope'],
        },
        {
          id: 'branch_frame_2',
          timestamp: 4,
          state_id: 'alt_step_3b',
          description: 'Retry data collection with expanded scope',
          involved_engines: ['DataEngine'],
          involved_agents: ['DataAnalyst'],
          inputs: ['expanded_scope'],
          outputs: ['raw_data'],
        },
      ],
      probability_weight: 0.3,
    },
    {
      id: 'branch_2',
      name: 'Review Revision Branch',
      description: 'Alternative when literature review needs revision',
      branch_point: 2,
      condition: 'review_incomplete',
      frames: [
        {
          id: 'branch_frame_3',
          timestamp: 2,
          state_id: 'alt_step_2a',
          description: 'Expand literature search scope',
          involved_engines: ['KnowledgeEngine'],
          involved_agents: ['Researcher'],
          inputs: ['research_question'],
          outputs: ['expanded_search'],
        },
      ],
      probability_weight: 0.2,
    },
  ],
  total_frames: 9,
  total_branches: 2,
  engines_involved: ['KnowledgeEngine', 'ContentEngine', 'DataEngine', 'AnalysisEngine'],
  agents_involved: ['ResearchLead', 'Researcher', 'DataAnalyst'],
  created_at: '2024-12-12T10:00:00Z',
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function SimulationPage() {
  const [selectedSubject, setSelectedSubject] = useState<SubjectOption | null>(SAMPLE_SUBJECTS[1]);
  const [simulation, setSimulation] = useState<SimulationRun | null>(SAMPLE_SIMULATION);
  const [selectedFrame, setSelectedFrame] = useState<SimulationFrame | null>(null);
  const [viewMode, setViewMode] = useState<'timeline' | 'flow' | 'branches'>('timeline');
  const [showBranches, setShowBranches] = useState(true);
  const [currentTimestamp, setCurrentTimestamp] = useState(0);
  
  // Get current frame
  const currentFrame = useMemo(() => {
    if (!simulation) return null;
    return simulation.main_timeline.find(f => f.timestamp === currentTimestamp);
  }, [simulation, currentTimestamp]);
  
  // Get frames at current timestamp (including branches)
  const framesAtTimestamp = useMemo(() => {
    if (!simulation) return [];
    const frames: Array<{ frame: SimulationFrame; branch?: string }> = [];
    
    const mainFrame = simulation.main_timeline.find(f => f.timestamp === currentTimestamp);
    if (mainFrame) {
      frames.push({ frame: mainFrame });
    }
    
    if (showBranches) {
      simulation.branches.forEach(branch => {
        const branchFrame = branch.frames.find(f => f.timestamp === currentTimestamp);
        if (branchFrame) {
          frames.push({ frame: branchFrame, branch: branch.name });
        }
      });
    }
    
    return frames;
  }, [simulation, currentTimestamp, showBranches]);
  
  // Max timestamp
  const maxTimestamp = useMemo(() => {
    if (!simulation) return 0;
    return Math.max(...simulation.main_timeline.map(f => f.timestamp));
  }, [simulation]);
  
  // Handle simulation trigger (representational)
  const handleRunSimulation = () => {
    if (selectedSubject) {
      // In real implementation, this would call SimulationEngine.simulate()
      setSimulation(SAMPLE_SIMULATION);
      setCurrentTimestamp(0);
    }
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
              <span>🎬</span>
              Simulation Tools
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Explore representational state flows and what-if variations
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              onClick={handleRunSimulation}
              disabled={!selectedSubject}
              style={{
                padding: '10px 20px',
                backgroundColor: selectedSubject ? COLORS.sacredGold : COLORS.shadowMoss,
                color: selectedSubject ? COLORS.uiSlate : COLORS.ancientStone,
                border: 'none',
                borderRadius: '8px',
                fontWeight: 600,
                cursor: selectedSubject ? 'pointer' : 'not-allowed',
              }}
            >
              ▶️ Run Simulation
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
          {/* Subject selector */}
          <select
            value={selectedSubject?.id || ''}
            onChange={(e) => {
              const subject = SAMPLE_SUBJECTS.find(s => s.id === e.target.value);
              setSelectedSubject(subject || null);
            }}
            style={{
              padding: '10px 16px',
              backgroundColor: COLORS.shadowMoss,
              border: `1px solid ${COLORS.ancientStone}40`,
              borderRadius: '8px',
              color: COLORS.softSand,
              fontSize: '14px',
              minWidth: '200px',
            }}
          >
            <option value="">Select subject...</option>
            {SAMPLE_SUBJECTS.map(subject => (
              <option key={subject.id} value={subject.id}>
                {SUBJECT_TYPE_ICONS[subject.type]} {subject.name}
              </option>
            ))}
          </select>
          
          {/* View mode toggle */}
          <div style={{ 
            display: 'flex', 
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
            overflow: 'hidden',
          }}>
            {(['timeline', 'flow', 'branches'] as const).map(mode => (
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
                {mode === 'timeline' ? '📅' : mode === 'flow' ? '🔀' : '🌳'} {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
          
          {/* Branch toggle */}
          <label style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            cursor: 'pointer',
          }}>
            <input
              type="checkbox"
              checked={showBranches}
              onChange={(e) => setShowBranches(e.target.checked)}
              style={{ accentColor: COLORS.sacredGold }}
            />
            <span style={{ fontSize: '14px' }}>Show Branches</span>
          </label>
          
          {/* Stats */}
          {simulation && (
            <div style={{ 
              marginLeft: 'auto', 
              display: 'flex', 
              gap: '16px',
              fontSize: '13px',
            }}>
              <span style={{ color: COLORS.cenoteTurquoise }}>
                {simulation.total_frames} frames
              </span>
              <span style={{ color: COLORS.earthEmber }}>
                {simulation.total_branches} branches
              </span>
              <span style={{ color: COLORS.jungleEmerald }}>
                {simulation.engines_involved.length} engines
              </span>
            </div>
          )}
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Simulation Viewer */}
        <div style={{
          flex: selectedFrame ? '1 1 60%' : 1,
          overflow: 'hidden',
          borderRight: selectedFrame ? `1px solid ${COLORS.shadowMoss}` : 'none',
        }}>
          {simulation ? (
            <>
              {/* Timeline Scrubber */}
              <div style={{
                padding: '16px 24px',
                backgroundColor: COLORS.shadowMoss,
                borderBottom: `1px solid ${COLORS.uiSlate}`,
              }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '16px',
                }}>
                  <button
                    onClick={() => setCurrentTimestamp(Math.max(0, currentTimestamp - 1))}
                    disabled={currentTimestamp === 0}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: COLORS.uiSlate,
                      border: 'none',
                      borderRadius: '4px',
                      color: currentTimestamp === 0 ? COLORS.ancientStone : COLORS.softSand,
                      cursor: currentTimestamp === 0 ? 'not-allowed' : 'pointer',
                    }}
                  >
                    ⏮️
                  </button>
                  
                  <div style={{ flex: 1 }}>
                    <input
                      type="range"
                      min={0}
                      max={maxTimestamp}
                      value={currentTimestamp}
                      onChange={(e) => setCurrentTimestamp(parseInt(e.target.value))}
                      style={{ width: '100%', accentColor: COLORS.sacredGold }}
                    />
                  </div>
                  
                  <button
                    onClick={() => setCurrentTimestamp(Math.min(maxTimestamp, currentTimestamp + 1))}
                    disabled={currentTimestamp === maxTimestamp}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: COLORS.uiSlate,
                      border: 'none',
                      borderRadius: '4px',
                      color: currentTimestamp === maxTimestamp ? COLORS.ancientStone : COLORS.softSand,
                      cursor: currentTimestamp === maxTimestamp ? 'not-allowed' : 'pointer',
                    }}
                  >
                    ⏭️
                  </button>
                  
                  <span style={{ 
                    fontWeight: 600, 
                    color: COLORS.sacredGold,
                    minWidth: '100px',
                    textAlign: 'center',
                  }}>
                    Step {currentTimestamp} / {maxTimestamp}
                  </span>
                </div>
              </div>
              
              {/* View Content */}
              {viewMode === 'timeline' && (
                <SimulationTimelineView
                  simulation={simulation}
                  currentTimestamp={currentTimestamp}
                  showBranches={showBranches}
                  onFrameSelect={setSelectedFrame}
                  selectedFrameId={selectedFrame?.id}
                />
              )}
              {viewMode === 'flow' && (
                <SimulationFlowView
                  simulation={simulation}
                  currentTimestamp={currentTimestamp}
                  showBranches={showBranches}
                  onFrameSelect={setSelectedFrame}
                />
              )}
              {viewMode === 'branches' && (
                <SimulationBranchesView
                  simulation={simulation}
                  onFrameSelect={setSelectedFrame}
                />
              )}
            </>
          ) : (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>🎬</span>
                <p>Select a subject and run a simulation</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Frame Detail Panel */}
        {selectedFrame && simulation && (
          <div style={{
            flex: '0 0 400px',
            overflowY: 'auto',
            padding: '20px',
            backgroundColor: '#16171a',
          }}>
            <FrameDetailPanel
              frame={selectedFrame}
              simulation={simulation}
              onClose={() => setSelectedFrame(null)}
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
          SAFE · NON-AUTONOMOUS · NO PREDICTION · Simulations are representational only — no actual forecasting
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

interface SimulationTimelineViewProps {
  simulation: SimulationRun;
  currentTimestamp: number;
  showBranches: boolean;
  onFrameSelect: (frame: SimulationFrame) => void;
  selectedFrameId?: string;
}

function SimulationTimelineView({
  simulation,
  currentTimestamp,
  showBranches,
  onFrameSelect,
  selectedFrameId,
}: SimulationTimelineViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: 'calc(100% - 80px)' }}>
      <div style={{ position: 'relative', paddingLeft: '60px' }}>
        {/* Timeline line */}
        <div style={{
          position: 'absolute',
          left: '25px',
          top: '0',
          bottom: '0',
          width: '2px',
          backgroundColor: COLORS.shadowMoss,
        }} />
        
        {simulation.main_timeline.map((frame, index) => {
          const isActive = frame.timestamp === currentTimestamp;
          const isPast = frame.timestamp < currentTimestamp;
          const isSelected = frame.id === selectedFrameId;
          
          // Find any branch at this timestamp
          const branchAtTimestamp = showBranches 
            ? simulation.branches.find(b => b.branch_point === frame.timestamp)
            : null;
          
          return (
            <div key={frame.id} style={{ marginBottom: '24px', position: 'relative' }}>
              {/* Timeline marker */}
              <div style={{
                position: 'absolute',
                left: '-45px',
                top: '12px',
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                backgroundColor: isActive 
                  ? COLORS.sacredGold 
                  : isPast 
                    ? COLORS.jungleEmerald 
                    : COLORS.shadowMoss,
                border: `3px solid ${COLORS.uiSlate}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '10px',
                fontWeight: 700,
                color: COLORS.uiSlate,
              }}>
                {frame.timestamp}
              </div>
              
              {/* Frame card */}
              <div
                onClick={() => onFrameSelect(frame)}
                style={{
                  padding: '16px',
                  backgroundColor: isSelected 
                    ? `${COLORS.sacredGold}20` 
                    : isActive 
                      ? `${COLORS.sacredGold}10` 
                      : COLORS.shadowMoss,
                  borderRadius: '8px',
                  cursor: 'pointer',
                  borderLeft: `3px solid ${
                    isActive ? COLORS.sacredGold : isPast ? COLORS.jungleEmerald : COLORS.ancientStone
                  }`,
                  opacity: isPast ? 0.7 : 1,
                }}
              >
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'flex-start',
                  marginBottom: '8px',
                }}>
                  <div style={{ fontWeight: 600, fontSize: '14px' }}>
                    {frame.description}
                  </div>
                  <span style={{
                    padding: '2px 8px',
                    backgroundColor: `${COLORS.cenoteTurquoise}20`,
                    color: COLORS.cenoteTurquoise,
                    borderRadius: '4px',
                    fontSize: '10px',
                  }}>
                    {frame.state_id}
                  </span>
                </div>
                
                {/* Engines & Agents */}
                <div style={{ 
                  display: 'flex', 
                  gap: '8px', 
                  flexWrap: 'wrap',
                  fontSize: '11px',
                }}>
                  {frame.involved_engines.map(engine => (
                    <span
                      key={engine}
                      style={{
                        padding: '2px 6px',
                        backgroundColor: `${COLORS.cenoteTurquoise}15`,
                        color: COLORS.cenoteTurquoise,
                        borderRadius: '3px',
                      }}
                    >
                      ⚙️ {engine.replace('Engine', '')}
                    </span>
                  ))}
                  {frame.involved_agents.map(agent => (
                    <span
                      key={agent}
                      style={{
                        padding: '2px 6px',
                        backgroundColor: `${COLORS.sacredGold}15`,
                        color: COLORS.sacredGold,
                        borderRadius: '3px',
                      }}
                    >
                      🤖 {agent}
                    </span>
                  ))}
                </div>
              </div>
              
              {/* Branch indicator */}
              {branchAtTimestamp && (
                <div style={{
                  marginTop: '12px',
                  marginLeft: '20px',
                  padding: '12px',
                  backgroundColor: `${COLORS.earthEmber}15`,
                  borderRadius: '8px',
                  borderLeft: `3px solid ${COLORS.earthEmber}`,
                }}>
                  <div style={{ 
                    fontSize: '12px', 
                    fontWeight: 600, 
                    color: COLORS.earthEmber,
                    marginBottom: '4px',
                  }}>
                    🌳 Branch: {branchAtTimestamp.name}
                  </div>
                  <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
                    Condition: {branchAtTimestamp.condition}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

interface SimulationFlowViewProps {
  simulation: SimulationRun;
  currentTimestamp: number;
  showBranches: boolean;
  onFrameSelect: (frame: SimulationFrame) => void;
}

function SimulationFlowView({
  simulation,
  currentTimestamp,
  showBranches,
  onFrameSelect,
}: SimulationFlowViewProps) {
  return (
    <div style={{ 
      padding: '40px', 
      overflowY: 'auto', 
      height: 'calc(100% - 80px)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}>
      {simulation.main_timeline.map((frame, index) => {
        const isActive = frame.timestamp === currentTimestamp;
        const isPast = frame.timestamp < currentTimestamp;
        const branchAtTimestamp = showBranches 
          ? simulation.branches.find(b => b.branch_point === frame.timestamp)
          : null;
        
        return (
          <React.Fragment key={frame.id}>
            {/* Connector */}
            {index > 0 && (
              <div style={{
                width: '2px',
                height: '30px',
                backgroundColor: isPast ? COLORS.jungleEmerald : COLORS.ancientStone,
              }} />
            )}
            
            {/* Flow with potential branch */}
            <div style={{ 
              display: 'flex', 
              alignItems: 'center',
              gap: '40px',
            }}>
              {/* Main frame */}
              <div
                onClick={() => onFrameSelect(frame)}
                style={{
                  padding: '16px 24px',
                  backgroundColor: isActive 
                    ? `${COLORS.sacredGold}20` 
                    : COLORS.shadowMoss,
                  border: `2px solid ${
                    isActive ? COLORS.sacredGold : isPast ? COLORS.jungleEmerald : COLORS.ancientStone
                  }`,
                  borderRadius: '12px',
                  cursor: 'pointer',
                  textAlign: 'center',
                  minWidth: '200px',
                  position: 'relative',
                }}
              >
                {/* Timestamp badge */}
                <div style={{
                  position: 'absolute',
                  top: '-10px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  backgroundColor: isActive ? COLORS.sacredGold : isPast ? COLORS.jungleEmerald : COLORS.ancientStone,
                  color: COLORS.uiSlate,
                  padding: '2px 8px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  fontWeight: 700,
                }}>
                  T{frame.timestamp}
                </div>
                
                <div style={{ fontWeight: 600, fontSize: '13px', marginTop: '4px' }}>
                  {frame.description}
                </div>
                
                {frame.involved_engines.length > 0 && (
                  <div style={{ 
                    marginTop: '8px', 
                    fontSize: '11px', 
                    color: COLORS.cenoteTurquoise,
                  }}>
                    {frame.involved_engines.join(', ')}
                  </div>
                )}
              </div>
              
              {/* Branch */}
              {branchAtTimestamp && (
                <>
                  <div style={{
                    width: '40px',
                    height: '2px',
                    backgroundColor: COLORS.earthEmber,
                  }} />
                  <div style={{
                    padding: '12px 16px',
                    backgroundColor: `${COLORS.earthEmber}15`,
                    border: `2px dashed ${COLORS.earthEmber}`,
                    borderRadius: '8px',
                    textAlign: 'center',
                    minWidth: '150px',
                  }}>
                    <div style={{ 
                      fontSize: '11px', 
                      fontWeight: 600, 
                      color: COLORS.earthEmber,
                    }}>
                      🌳 {branchAtTimestamp.name}
                    </div>
                    <div style={{ fontSize: '10px', color: COLORS.ancientStone, marginTop: '4px' }}>
                      {branchAtTimestamp.frames.length} alt frames
                    </div>
                  </div>
                </>
              )}
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
}

interface SimulationBranchesViewProps {
  simulation: SimulationRun;
  onFrameSelect: (frame: SimulationFrame) => void;
}

function SimulationBranchesView({
  simulation,
  onFrameSelect,
}: SimulationBranchesViewProps) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: 'calc(100% - 80px)' }}>
      <h3 style={{ margin: '0 0 20px', color: COLORS.sacredGold }}>
        🌳 Branches ({simulation.branches.length})
      </h3>
      
      {simulation.branches.length === 0 ? (
        <div style={{ 
          textAlign: 'center', 
          padding: '40px',
          color: COLORS.ancientStone,
        }}>
          No branches in this simulation
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {simulation.branches.map(branch => (
            <div
              key={branch.id}
              style={{
                padding: '20px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '12px',
                borderLeft: `4px solid ${COLORS.earthEmber}`,
              }}
            >
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'flex-start',
                marginBottom: '12px',
              }}>
                <div>
                  <h4 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>
                    {branch.name}
                  </h4>
                  <p style={{ 
                    margin: '4px 0 0', 
                    fontSize: '13px', 
                    color: COLORS.ancientStone,
                  }}>
                    {branch.description}
                  </p>
                </div>
                <span style={{
                  padding: '4px 10px',
                  backgroundColor: `${COLORS.cenoteTurquoise}20`,
                  color: COLORS.cenoteTurquoise,
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontWeight: 600,
                }}>
                  Branch @ T{branch.branch_point}
                </span>
              </div>
              
              <div style={{
                padding: '12px',
                backgroundColor: COLORS.uiSlate,
                borderRadius: '8px',
                marginBottom: '12px',
              }}>
                <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '4px' }}>
                  Condition
                </div>
                <div style={{ fontSize: '14px', fontFamily: 'monospace' }}>
                  {branch.condition}
                </div>
              </div>
              
              <div style={{ fontSize: '13px', color: COLORS.ancientStone, marginBottom: '12px' }}>
                Weight: {(branch.probability_weight * 100).toFixed(0)}% (representational)
              </div>
              
              {/* Branch frames */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {branch.frames.map(frame => (
                  <div
                    key={frame.id}
                    onClick={() => onFrameSelect(frame)}
                    style={{
                      padding: '12px',
                      backgroundColor: `${COLORS.earthEmber}10`,
                      borderRadius: '6px',
                      cursor: 'pointer',
                      borderLeft: `2px solid ${COLORS.earthEmber}`,
                    }}
                  >
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between',
                      fontSize: '13px',
                    }}>
                      <span style={{ fontWeight: 500 }}>{frame.description}</span>
                      <span style={{ color: COLORS.ancientStone }}>T{frame.timestamp}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

interface FrameDetailPanelProps {
  frame: SimulationFrame;
  simulation: SimulationRun;
  onClose: () => void;
}

function FrameDetailPanel({ frame, simulation, onClose }: FrameDetailPanelProps) {
  // Check if this frame is in a branch
  const branch = simulation.branches.find(b => 
    b.frames.some(f => f.id === frame.id)
  );
  
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
            Frame Detail
          </h2>
          <div style={{ 
            display: 'flex', 
            gap: '8px', 
            marginTop: '8px',
          }}>
            <span style={{
              padding: '4px 10px',
              backgroundColor: `${COLORS.sacredGold}20`,
              color: COLORS.sacredGold,
              borderRadius: '4px',
              fontSize: '12px',
              fontWeight: 600,
            }}>
              T{frame.timestamp}
            </span>
            {branch && (
              <span style={{
                padding: '4px 10px',
                backgroundColor: `${COLORS.earthEmber}20`,
                color: COLORS.earthEmber,
                borderRadius: '4px',
                fontSize: '12px',
                fontWeight: 600,
              }}>
                🌳 Branch
              </span>
            )}
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
          }}
        >
          ✕
        </button>
      </div>
      
      {/* Description */}
      <div style={{
        padding: '16px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '8px',
        marginBottom: '20px',
      }}>
        <h3 style={{ margin: '0 0 8px', fontSize: '14px', color: COLORS.softSand }}>
          {frame.description}
        </h3>
        <div style={{ fontSize: '12px', color: COLORS.ancientStone, fontFamily: 'monospace' }}>
          State ID: {frame.state_id}
        </div>
      </div>
      
      {/* Engines */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
          Involved Engines
        </h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {frame.involved_engines.map(engine => (
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
          {frame.involved_engines.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>None</span>
          )}
        </div>
      </div>
      
      {/* Agents */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
          Involved Agents
        </h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {frame.involved_agents.map(agent => (
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
          {frame.involved_agents.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>None</span>
          )}
        </div>
      </div>
      
      {/* Inputs & Outputs */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
        <div>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Inputs ({frame.inputs.length})
          </h4>
          {frame.inputs.map((input, i) => (
            <div
              key={i}
              style={{
                padding: '8px 12px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                marginBottom: '8px',
                borderLeft: `3px solid ${COLORS.jungleEmerald}`,
                fontSize: '13px',
              }}
            >
              ↓ {input}
            </div>
          ))}
          {frame.inputs.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '12px' }}>
              No inputs
            </span>
          )}
        </div>
        <div>
          <h4 style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
            Outputs ({frame.outputs.length})
          </h4>
          {frame.outputs.map((output, i) => (
            <div
              key={i}
              style={{
                padding: '8px 12px',
                backgroundColor: COLORS.shadowMoss,
                borderRadius: '6px',
                marginBottom: '8px',
                borderLeft: `3px solid ${COLORS.cenoteTurquoise}`,
                fontSize: '13px',
              }}
            >
              ↑ {output}
            </div>
          ))}
          {frame.outputs.length === 0 && (
            <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '12px' }}>
              No outputs
            </span>
          )}
        </div>
      </div>
      
      {/* Branch info if applicable */}
      {branch && (
        <div style={{
          padding: '16px',
          backgroundColor: `${COLORS.earthEmber}15`,
          borderRadius: '8px',
          borderLeft: `3px solid ${COLORS.earthEmber}`,
        }}>
          <h4 style={{ margin: '0 0 8px', fontSize: '13px', color: COLORS.earthEmber }}>
            🌳 Branch: {branch.name}
          </h4>
          <p style={{ margin: '0 0 8px', fontSize: '12px', color: COLORS.ancientStone }}>
            {branch.description}
          </p>
          <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>
            Condition: {branch.condition}
          </div>
        </div>
      )}
    </div>
  );
}

export default SimulationPage;

============================================================
END OF SIMULATION FRONTEND
============================================================
