/**
 * CHE·NU Demo System V51
 * Reflection Room - Core Entry Module
 * 
 * Context-free entry point for cognitive reflection.
 * Generates proposals governed by humans.
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ============================================
// TYPES
// ============================================

export interface CanvasBlock {
  id: string;
  type: 'text' | 'thought' | 'question' | 'connection';
  content: string;
  position: { x: number; y: number };
  created_at: string;
}

export interface DraftProposal {
  id: string;
  type: 'memory_addition' | 'memory_update' | 'relation_create';
  title: string;
  content: string;
  confidence: number;
  source_blocks: string[];
  status: 'draft' | 'pending' | 'approved' | 'rejected';
  created_at: string;
}

export interface ReflectionRoomProps {
  presenterMode?: boolean;
  onNavigate?: (moduleId: string) => void;
  onProposalCreate?: (proposal: DraftProposal) => void;
  className?: string;
}

// ============================================
// COMPONENT
// ============================================

export const ReflectionRoom: React.FC<ReflectionRoomProps> = ({
  presenterMode = false,
  onNavigate,
  onProposalCreate,
  className = ''
}) => {
  // State
  const [blocks, setBlocks] = useState<CanvasBlock[]>([]);
  const [proposals, setProposals] = useState<DraftProposal[]>([]);
  const [inputText, setInputText] = useState('');
  const [selectedBlock, setSelectedBlock] = useState<string | null>(null);
  const [contextLoaded, setContextLoaded] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  
  const canvasRef = useRef<HTMLDivElement>(null);

  // Add block to canvas
  const handleAddBlock = useCallback((type: CanvasBlock['type'] = 'text') => {
    if (!inputText.trim()) return;
    
    const newBlock: CanvasBlock = {
      id: `block_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
      type,
      content: inputText,
      position: {
        x: 50 + Math.random() * 200,
        y: 50 + blocks.length * 80
      },
      created_at: new Date().toISOString()
    };
    
    setBlocks(prev => [...prev, newBlock]);
    setInputText('');
    
    // Simulate proposal generation
    if (blocks.length >= 2) {
      generateProposal([...blocks, newBlock]);
    }
  }, [inputText, blocks]);

  // Generate proposal from blocks
  const generateProposal = useCallback((currentBlocks: CanvasBlock[]) => {
    setIsProcessing(true);
    
    // Simulate AI processing
    setTimeout(() => {
      const newProposal: DraftProposal = {
        id: `prop_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
        type: 'memory_addition',
        title: `Insight from reflection #${proposals.length + 1}`,
        content: currentBlocks.map(b => b.content).join(' → '),
        confidence: 0.75 + Math.random() * 0.2,
        source_blocks: currentBlocks.slice(-3).map(b => b.id),
        status: 'draft',
        created_at: new Date().toISOString()
      };
      
      setProposals(prev => [...prev, newProposal]);
      setIsProcessing(false);
      
      if (onProposalCreate) {
        onProposalCreate(newProposal);
      }
    }, 1000);
  }, [proposals.length, onProposalCreate]);

  // Submit proposal for review
  const handleSubmitProposal = useCallback((proposalId: string) => {
    setProposals(prev => prev.map(p => 
      p.id === proposalId ? { ...p, status: 'pending' } : p
    ));
  }, []);

  // Approve proposal
  const handleApproveProposal = useCallback((proposalId: string) => {
    setProposals(prev => prev.map(p => 
      p.id === proposalId ? { ...p, status: 'approved' } : p
    ));
  }, []);

  // Reject proposal
  const handleRejectProposal = useCallback((proposalId: string) => {
    setProposals(prev => prev.map(p => 
      p.id === proposalId ? { ...p, status: 'rejected' } : p
    ));
  }, []);

  // Clear canvas
  const handleClear = useCallback(() => {
    setBlocks([]);
    setProposals([]);
    setSelectedBlock(null);
  }, []);

  return (
    <div className={`reflection-room ${className}`} style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerLeft}>
          <h1 style={styles.title}>🔮 Salle de Réflexion</h1>
          <span style={styles.badge}>CONTEXT-FREE</span>
          {presenterMode && <span style={styles.presenterBadge}>📺</span>}
        </div>
        <div style={styles.headerRight}>
          <button 
            onClick={() => setContextLoaded(!contextLoaded)}
            style={{
              ...styles.contextButton,
              backgroundColor: contextLoaded ? '#4a6a4a' : '#4a4a6a'
            }}
          >
            {contextLoaded ? '🔓 Context Loaded' : '🔒 Load Context'}
          </button>
          <button onClick={handleClear} style={styles.clearButton}>
            Clear
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div style={styles.main}>
        {/* Canvas Area */}
        <div style={styles.canvasContainer}>
          <div ref={canvasRef} style={styles.canvas}>
            {/* Blocks */}
            {blocks.map((block, index) => (
              <div
                key={block.id}
                onClick={() => setSelectedBlock(block.id)}
                style={{
                  ...styles.block,
                  ...getBlockStyle(block.type),
                  left: block.position.x,
                  top: block.position.y,
                  border: selectedBlock === block.id ? '2px solid #4a9eff' : '1px solid #333'
                }}
              >
                <span style={styles.blockIcon}>{getBlockIcon(block.type)}</span>
                <p style={styles.blockContent}>{block.content}</p>
                <span style={styles.blockIndex}>#{index + 1}</span>
              </div>
            ))}

            {/* Empty State */}
            {blocks.length === 0 && (
              <div style={styles.emptyState}>
                <p>Commencez à réfléchir...</p>
                <p style={styles.emptyHint}>Ajoutez des pensées, questions ou idées</p>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div style={styles.inputArea}>
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddBlock('text')}
              placeholder="Entrez une pensée, question ou idée..."
              style={styles.input}
            />
            <div style={styles.inputButtons}>
              <button 
                onClick={() => handleAddBlock('text')} 
                style={{...styles.addButton, backgroundColor: '#4a4a6a'}}
                disabled={!inputText.trim()}
              >
                📝 Texte
              </button>
              <button 
                onClick={() => handleAddBlock('thought')} 
                style={{...styles.addButton, backgroundColor: '#6a4a6a'}}
                disabled={!inputText.trim()}
              >
                💭 Pensée
              </button>
              <button 
                onClick={() => handleAddBlock('question')} 
                style={{...styles.addButton, backgroundColor: '#4a6a6a'}}
                disabled={!inputText.trim()}
              >
                ❓ Question
              </button>
            </div>
          </div>
        </div>

        {/* Proposals Sidebar */}
        <div style={styles.sidebar}>
          <h3 style={styles.sidebarTitle}>
            📋 Propositions
            {isProcessing && <span style={styles.processing}>⏳</span>}
          </h3>
          
          {proposals.length === 0 ? (
            <p style={styles.noProposals}>
              Aucune proposition générée.
              <br/>
              <small>Continuez à réfléchir pour en générer.</small>
            </p>
          ) : (
            <div style={styles.proposalList}>
              {proposals.map(proposal => (
                <div 
                  key={proposal.id} 
                  style={{
                    ...styles.proposalCard,
                    borderLeftColor: getStatusColor(proposal.status)
                  }}
                >
                  <div style={styles.proposalHeader}>
                    <span style={styles.proposalTitle}>{proposal.title}</span>
                    <span style={{
                      ...styles.statusBadge,
                      backgroundColor: getStatusColor(proposal.status)
                    }}>
                      {proposal.status}
                    </span>
                  </div>
                  <p style={styles.proposalContent}>{proposal.content}</p>
                  <div style={styles.proposalMeta}>
                    <span>Confiance: {Math.round(proposal.confidence * 100)}%</span>
                  </div>
                  
                  {proposal.status === 'draft' && (
                    <div style={styles.proposalActions}>
                      <button 
                        onClick={() => handleSubmitProposal(proposal.id)}
                        style={styles.submitButton}
                      >
                        Soumettre pour révision
                      </button>
                    </div>
                  )}
                  
                  {proposal.status === 'pending' && (
                    <div style={styles.proposalActions}>
                      <button 
                        onClick={() => handleApproveProposal(proposal.id)}
                        style={styles.approveButton}
                      >
                        ✓ Approuver
                      </button>
                      <button 
                        onClick={() => handleRejectProposal(proposal.id)}
                        style={styles.rejectButton}
                      >
                        ✗ Rejeter
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Tree Laws Reminder */}
          <div style={styles.treeLawsReminder}>
            <h4>🌳 Tree Laws</h4>
            <ul>
              <li>✓ Pas d'écriture auto</li>
              <li>✓ Humain décide</li>
              <li>✓ Tout est tracé</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Presenter Notes */}
      {presenterMode && (
        <div style={styles.presenterNotes}>
          <strong>Notes Présentateur:</strong>
          <ul>
            <li>Démontrer l'ajout de blocs</li>
            <li>Montrer la génération de propositions</li>
            <li>Souligner le contrôle humain</li>
          </ul>
        </div>
      )}
    </div>
  );
};

// ============================================
// HELPERS
// ============================================

function getBlockIcon(type: CanvasBlock['type']): string {
  const icons: Record<CanvasBlock['type'], string> = {
    text: '📝',
    thought: '💭',
    question: '❓',
    connection: '🔗'
  };
  return icons[type];
}

function getBlockStyle(type: CanvasBlock['type']): React.CSSProperties {
  const baseStyle: React.CSSProperties = {
    position: 'absolute',
    padding: '12px 15px',
    borderRadius: '8px',
    maxWidth: '250px',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s'
  };
  
  const typeStyles: Record<CanvasBlock['type'], React.CSSProperties> = {
    text: { backgroundColor: '#1a2a4a' },
    thought: { backgroundColor: '#2a1a4a' },
    question: { backgroundColor: '#1a4a4a' },
    connection: { backgroundColor: '#4a4a1a' }
  };
  
  return { ...baseStyle, ...typeStyles[type] };
}

function getStatusColor(status: DraftProposal['status']): string {
  const colors: Record<DraftProposal['status'], string> = {
    draft: '#6a6a6a',
    pending: '#ff9e4a',
    approved: '#81c784',
    rejected: '#e57373'
  };
  return colors[status];
}

// ============================================
// STYLES
// ============================================

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
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px'
  },
  headerRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  },
  title: {
    fontSize: '18px',
    fontWeight: 'bold',
    margin: 0
  },
  badge: {
    fontSize: '10px',
    padding: '3px 8px',
    backgroundColor: '#4a4a6a',
    borderRadius: '4px',
    color: '#a0c0ff'
  },
  presenterBadge: {
    fontSize: '16px'
  },
  contextButton: {
    padding: '8px 16px',
    fontSize: '12px',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  clearButton: {
    padding: '8px 16px',
    fontSize: '12px',
    backgroundColor: 'transparent',
    border: '1px solid #444',
    borderRadius: '4px',
    color: '#888',
    cursor: 'pointer'
  },
  main: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden'
  },
  canvasContainer: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column'
  },
  canvas: {
    flex: 1,
    position: 'relative',
    backgroundColor: '#0a0a1a',
    backgroundImage: 'radial-gradient(circle, #1a1a2e 1px, transparent 1px)',
    backgroundSize: '20px 20px',
    overflow: 'auto'
  },
  block: {
    boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
  },
  blockIcon: {
    marginRight: '8px'
  },
  blockContent: {
    margin: 0,
    fontSize: '13px',
    lineHeight: 1.5
  },
  blockIndex: {
    position: 'absolute',
    top: '-8px',
    right: '-8px',
    fontSize: '10px',
    backgroundColor: '#4a9eff',
    borderRadius: '50%',
    width: '20px',
    height: '20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  emptyState: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    textAlign: 'center',
    color: '#666'
  },
  emptyHint: {
    fontSize: '12px',
    marginTop: '10px'
  },
  inputArea: {
    padding: '15px 20px',
    borderTop: '1px solid #333',
    backgroundColor: '#0f0f1a'
  },
  input: {
    width: '100%',
    padding: '12px 15px',
    fontSize: '14px',
    backgroundColor: '#1a1a2e',
    border: '1px solid #333',
    borderRadius: '6px',
    color: '#e0e0e0',
    marginBottom: '10px',
    boxSizing: 'border-box'
  },
  inputButtons: {
    display: 'flex',
    gap: '8px'
  },
  addButton: {
    padding: '8px 16px',
    fontSize: '12px',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  sidebar: {
    width: '320px',
    borderLeft: '1px solid #333',
    padding: '15px',
    backgroundColor: '#0f0f1a',
    overflow: 'auto'
  },
  sidebarTitle: {
    fontSize: '14px',
    marginBottom: '15px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  },
  processing: {
    animation: 'pulse 1s infinite'
  },
  noProposals: {
    color: '#666',
    fontSize: '13px',
    textAlign: 'center',
    padding: '20px'
  },
  proposalList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  proposalCard: {
    padding: '12px',
    backgroundColor: '#1a1a2e',
    borderRadius: '8px',
    borderLeft: '3px solid'
  },
  proposalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px'
  },
  proposalTitle: {
    fontSize: '13px',
    fontWeight: 'bold'
  },
  statusBadge: {
    fontSize: '10px',
    padding: '2px 8px',
    borderRadius: '4px',
    color: '#fff'
  },
  proposalContent: {
    fontSize: '12px',
    color: '#888',
    margin: '0 0 8px 0'
  },
  proposalMeta: {
    fontSize: '11px',
    color: '#666'
  },
  proposalActions: {
    display: 'flex',
    gap: '8px',
    marginTop: '10px'
  },
  submitButton: {
    flex: 1,
    padding: '8px',
    fontSize: '11px',
    backgroundColor: '#4a4a6a',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  approveButton: {
    flex: 1,
    padding: '8px',
    fontSize: '11px',
    backgroundColor: '#4a6a4a',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  rejectButton: {
    flex: 1,
    padding: '8px',
    fontSize: '11px',
    backgroundColor: '#6a4a4a',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer'
  },
  treeLawsReminder: {
    marginTop: 'auto',
    padding: '15px',
    backgroundColor: 'rgba(129, 199, 132, 0.1)',
    borderRadius: '8px',
    fontSize: '11px'
  },
  presenterNotes: {
    position: 'fixed',
    bottom: '80px',
    right: '20px',
    width: '250px',
    padding: '15px',
    backgroundColor: 'rgba(106, 74, 106, 0.9)',
    borderRadius: '8px',
    fontSize: '12px',
    zIndex: 1000
  }
};

export default ReflectionRoom;
