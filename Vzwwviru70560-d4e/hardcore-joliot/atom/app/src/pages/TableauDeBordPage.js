/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗ ██╗   ██╗██████╗ ███████╗ █████╗ ██╗   ██╗
 *      ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗██║   ██║
 *      ██████╔╝██║   ██║██████╔╝█████╗  ███████║██║   ██║
 *      ██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██║██║   ██║
 *      ██████╔╝╚██████╔╝██║  ██║███████╗██║  ██║╚██████╔╝
 *      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝
 *
 *                    🏛️ BUREAU CANONIQUE CHE·NU 🏛️
 *              Structure: 6 SECTIONS MAXIMUM (HARD LIMIT)
 *
 *   VÉRITÉS CANONIQUES RESPECTÉES:
 *   - 6 Sections Bureau (HARD LIMIT - JAMAIS PLUS)
 *   - Quick Capture, Resume Workspace, Threads, Data/Files, Active Agents, Meetings
 *   - Intégration avec CanonicalLayout (3 Hubs)
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import CanonicalLayout, { SPHERES, BUREAU_SECTIONS, useCanonicalLayout } from '../components/CanonicalLayout';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION CAPTURE RAPIDE (Quick Capture)
// Max 500 caractères
// ═══════════════════════════════════════════════════════════════════════════════

const QuickCaptureSection = () => {
  const [note, setNote] = useState('');
  const maxChars = 500;

  const handleSave = () => {
    if (note.trim()) {
      // Sauvegarder la note
      const notes = JSON.parse(localStorage.getItem('atom_quick_notes') || '[]');
      notes.unshift({
        id: Date.now(),
        text: note,
        createdAt: new Date().toISOString()
      });
      localStorage.setItem('atom_quick_notes', JSON.stringify(notes.slice(0, 50)));
      setNote('');
    }
  };

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-white flex items-center gap-2">
          <span>📝</span> Capture Rapide
        </h3>
        <span className={`text-xs ${note.length > maxChars * 0.8 ? 'text-yellow-500' : 'text-gray-600'}`}>
          {note.length}/{maxChars}
        </span>
      </div>
      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value.slice(0, maxChars))}
        placeholder="Notez une idée rapidement..."
        className="w-full h-20 bg-black/50 border border-gray-700 rounded-lg p-3 text-sm text-white
          placeholder-gray-600 resize-none focus:outline-none focus:border-yellow-500/50"
      />
      <button
        onClick={handleSave}
        disabled={!note.trim()}
        className={`mt-2 px-4 py-2 rounded-lg text-sm transition-all ${
          note.trim()
            ? 'bg-yellow-600 text-black hover:bg-yellow-500'
            : 'bg-gray-800 text-gray-600 cursor-not-allowed'
        }`}
      >
        Capturer
      </button>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION REPRENDRE (Resume Workspace)
// ═══════════════════════════════════════════════════════════════════════════════

const ResumeWorkspaceSection = () => {
  const [recentItems, setRecentItems] = useState([]);

  useEffect(() => {
    // Charger les items récents
    const items = [
      { id: 1, name: 'Projet Camping', type: 'project', lastAccess: '2 min' },
      { id: 2, name: 'Thread Nova', type: 'thread', lastAccess: '15 min' },
      { id: 3, name: 'Besoin: Énergie', type: 'need', lastAccess: '1h' }
    ];
    setRecentItems(items);
  }, []);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'project': return '📁';
      case 'thread': return '💬';
      case 'need': return '📊';
      default: return '📄';
    }
  };

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <h3 className="text-sm font-medium text-white flex items-center gap-2 mb-3">
        <span>▶️</span> Reprendre
      </h3>
      {recentItems.length > 0 ? (
        <div className="space-y-2">
          {recentItems.map(item => (
            <button
              key={item.id}
              className="w-full flex items-center gap-3 p-2 rounded-lg bg-black/30 hover:bg-black/50
                transition-all text-left group"
            >
              <span className="text-lg">{getTypeIcon(item.type)}</span>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-white truncate">{item.name}</div>
                <div className="text-xs text-gray-600">Il y a {item.lastAccess}</div>
              </div>
              <span className="text-gray-600 group-hover:text-white transition-colors">→</span>
            </button>
          ))}
        </div>
      ) : (
        <p className="text-gray-600 text-sm text-center py-4">Aucun élément récent</p>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION THREADS
// Conversations .chenu persistence
// ═══════════════════════════════════════════════════════════════════════════════

const ThreadsSection = () => {
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    // Charger les threads
    setThreads([
      { id: 1, name: 'Discussion Projet', agent: 'Nova', messages: 12, unread: 2 },
      { id: 2, name: 'Analyse Besoins', agent: 'Aria', messages: 8, unread: 0 }
    ]);
  }, []);

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <h3 className="text-sm font-medium text-white flex items-center gap-2 mb-3">
        <span>💬</span> Threads
      </h3>
      {threads.length > 0 ? (
        <div className="space-y-2">
          {threads.map(thread => (
            <button
              key={thread.id}
              className="w-full flex items-center gap-3 p-2 rounded-lg bg-black/30 hover:bg-black/50
                transition-all text-left"
            >
              <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center text-sm">
                {thread.agent[0]}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-white truncate">{thread.name}</div>
                <div className="text-xs text-gray-600">{thread.messages} messages</div>
              </div>
              {thread.unread > 0 && (
                <span className="px-2 py-0.5 bg-yellow-500 text-black text-xs rounded-full">
                  {thread.unread}
                </span>
              )}
            </button>
          ))}
        </div>
      ) : (
        <p className="text-gray-600 text-sm text-center py-4">Aucun thread actif</p>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION DONNÉES/FICHIERS (Data/Files)
// ═══════════════════════════════════════════════════════════════════════════════

const DataFilesSection = () => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    setFiles([
      { id: 1, name: 'Mapping_CHE-NU.json', size: '24 KB', type: 'json' },
      { id: 2, name: 'Perceptions_2026.md', size: '12 KB', type: 'md' }
    ]);
  }, []);

  const getFileIcon = (type) => {
    switch (type) {
      case 'json': return '📋';
      case 'md': return '📝';
      case 'pdf': return '📕';
      default: return '📄';
    }
  };

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <h3 className="text-sm font-medium text-white flex items-center gap-2 mb-3">
        <span>📁</span> Données & Fichiers
      </h3>
      {files.length > 0 ? (
        <div className="space-y-2">
          {files.map(file => (
            <button
              key={file.id}
              className="w-full flex items-center gap-3 p-2 rounded-lg bg-black/30 hover:bg-black/50
                transition-all text-left"
            >
              <span className="text-lg">{getFileIcon(file.type)}</span>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-white truncate">{file.name}</div>
                <div className="text-xs text-gray-600">{file.size}</div>
              </div>
            </button>
          ))}
        </div>
      ) : (
        <p className="text-gray-600 text-sm text-center py-4">Aucun fichier</p>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION AGENTS ACTIFS
// ═══════════════════════════════════════════════════════════════════════════════

const ActiveAgentsSection = () => {
  const [activeAgents, setActiveAgents] = useState([]);

  useEffect(() => {
    // Les agents actifs seraient chargés dynamiquement
    setActiveAgents([]);
  }, []);

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <h3 className="text-sm font-medium text-white flex items-center gap-2 mb-3">
        <span>🤖</span> Agents Actifs
      </h3>
      {activeAgents.length > 0 ? (
        <div className="space-y-2">
          {activeAgents.map(agent => (
            <div key={agent.id} className="flex items-center gap-3 p-2 rounded-lg bg-black/30">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center">
                <span className="text-green-400 text-sm">●</span>
              </div>
              <div className="flex-1">
                <div className="text-sm text-white">{agent.name}</div>
                <div className="text-xs text-gray-600">{agent.task}</div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-4">
          <span className="text-2xl mb-2 block">😴</span>
          <p className="text-gray-600 text-sm">Aucun agent actif</p>
          <p className="text-gray-700 text-xs mt-1">Utilisez QuickConnect pour démarrer</p>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SECTION RÉUNIONS (Meetings)
// ═══════════════════════════════════════════════════════════════════════════════

const MeetingsSection = () => {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    setMeetings([
      { id: 1, title: 'Sync Équipe', time: '14:00', participants: 3 }
    ]);
  }, []);

  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
      <h3 className="text-sm font-medium text-white flex items-center gap-2 mb-3">
        <span>📅</span> Réunions
      </h3>
      {meetings.length > 0 ? (
        <div className="space-y-2">
          {meetings.map(meeting => (
            <div key={meeting.id} className="flex items-center gap-3 p-2 rounded-lg bg-black/30">
              <div className="text-center">
                <div className="text-lg font-mono text-yellow-500">{meeting.time}</div>
              </div>
              <div className="flex-1">
                <div className="text-sm text-white">{meeting.title}</div>
                <div className="text-xs text-gray-600">{meeting.participants} participants</div>
              </div>
              <button className="px-3 py-1 bg-green-600 text-white text-xs rounded-lg hover:bg-green-500">
                Rejoindre
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-600 text-sm text-center py-4">Aucune réunion prévue</p>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BUREAU CANONIQUE (6 Sections)
// ═══════════════════════════════════════════════════════════════════════════════

const BureauCanonique = ({ sphereId }) => {
  const sphere = SPHERES.find(s => s.id === sphereId) || SPHERES[0];

  return (
    <div className="p-6">
      {/* Header du Bureau */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">{sphere.icon}</span>
          <div>
            <h1 className="text-xl font-bold text-white">Bureau {sphere.name}</h1>
            <p className="text-sm text-gray-500">6 sections • Structure canonique</p>
          </div>
        </div>
      </div>

      {/* Les 6 Sections Bureau (HARD LIMIT) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <QuickCaptureSection />
        <ResumeWorkspaceSection />
        <ThreadsSection />
        <DataFilesSection />
        <ActiveAgentsSection />
        <MeetingsSection />
      </div>

      {/* Avertissement HARD LIMIT */}
      <div className="mt-6 text-center">
        <p className="text-xs text-gray-700">
          ⚠️ HARD LIMIT: 6 sections maximum par Bureau (vérité canonique)
        </p>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: TABLEAU DE BORD CANONIQUE
// ═══════════════════════════════════════════════════════════════════════════════

const TableauDeBordPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Vérifier si la charte a été acceptée
  useEffect(() => {
    const charteAccepted = localStorage.getItem('atom_charte_accepted');
    if (!charteAccepted) {
      navigate('/entree');
    }
  }, [navigate]);

  return (
    <CanonicalLayout>
      <BureauCanonique sphereId="personal" />
    </CanonicalLayout>
  );
};

export default TableauDeBordPage;
