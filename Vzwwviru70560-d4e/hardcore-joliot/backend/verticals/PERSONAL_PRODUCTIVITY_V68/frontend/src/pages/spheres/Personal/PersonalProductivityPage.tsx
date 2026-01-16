/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║              CHE·NU™ PERSONAL PRODUCTIVITY — MAIN PAGE                       ║
 * ║                                                                              ║
 * ║  Unified productivity interface for notes and tasks.                         ║
 * ║  COS: 93/100 — Notion/Todoist Competitor                                     ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import React, { useEffect, useState, useCallback } from 'react';
import { usePersonalProductivityStore, Note, Task, TaskPriority } from '../../../stores/personalProductivityStore';

// ═══════════════════════════════════════════════════════════════════════════════
// ICONS (Simple SVG components)
// ═══════════════════════════════════════════════════════════════════════════════

const Icons = {
  Note: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  Task: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
    </svg>
  ),
  Today: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  ),
  Stats: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  ),
  Plus: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
    </svg>
  ),
  Check: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
  ),
  Sparkles: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
    </svg>
  ),
  Trash: () => (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
  ),
};

// ═══════════════════════════════════════════════════════════════════════════════
// PRIORITY BADGE
// ═══════════════════════════════════════════════════════════════════════════════

const PriorityBadge: React.FC<{ priority: TaskPriority }> = ({ priority }) => {
  const colors: Record<TaskPriority, string> = {
    urgent: 'bg-red-100 text-red-800 border-red-200',
    high: 'bg-orange-100 text-orange-800 border-orange-200',
    medium: 'bg-blue-100 text-blue-800 border-blue-200',
    low: 'bg-gray-100 text-gray-800 border-gray-200',
    someday: 'bg-gray-50 text-gray-600 border-gray-100',
  };
  
  return (
    <span className={`px-2 py-0.5 text-xs font-medium rounded border ${colors[priority]}`}>
      {priority.charAt(0).toUpperCase() + priority.slice(1)}
    </span>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// TODAY VIEW TAB
// ═══════════════════════════════════════════════════════════════════════════════

const TodayTab: React.FC = () => {
  const { todayView, fetchTodayView, completeTask, isLoading } = usePersonalProductivityStore();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const { createTask } = usePersonalProductivityStore();
  
  useEffect(() => {
    fetchTodayView();
  }, [fetchTodayView]);
  
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;
    
    await createTask(newTaskTitle);
    setNewTaskTitle('');
    fetchTodayView();
  };
  
  if (isLoading && !todayView) {
    return <div className="flex justify-center p-8"><div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" /></div>;
  }
  
  return (
    <div className="space-y-6">
      {/* Quick Add */}
      <form onSubmit={handleCreateTask} className="flex gap-2">
        <input
          type="text"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          placeholder="Add a task... (AI will suggest priority & due date)"
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Icons.Plus /> Add
        </button>
      </form>
      
      {/* Stats Summary */}
      {todayView && (
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-red-50 p-4 rounded-lg border border-red-100">
            <div className="text-2xl font-bold text-red-700">{todayView.stats.overdue_count}</div>
            <div className="text-sm text-red-600">Overdue</div>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
            <div className="text-2xl font-bold text-blue-700">{todayView.stats.due_today_count}</div>
            <div className="text-sm text-blue-600">Due Today</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-100">
            <div className="text-2xl font-bold text-green-700">{todayView.stats.completed_count}</div>
            <div className="text-sm text-green-600">Completed</div>
          </div>
        </div>
      )}
      
      {/* Overdue Tasks */}
      {todayView && todayView.overdue.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-red-700 mb-3">⚠️ Overdue</h3>
          <div className="space-y-2">
            {todayView.overdue.map(task => (
              <TaskItem key={task.id} task={task} onComplete={completeTask} />
            ))}
          </div>
        </div>
      )}
      
      {/* Due Today */}
      {todayView && todayView.due_today.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">📅 Due Today</h3>
          <div className="space-y-2">
            {todayView.due_today.map(task => (
              <TaskItem key={task.id} task={task} onComplete={completeTask} />
            ))}
          </div>
        </div>
      )}
      
      {/* High Priority */}
      {todayView && todayView.high_priority.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">🔥 High Priority</h3>
          <div className="space-y-2">
            {todayView.high_priority.map(task => (
              <TaskItem key={task.id} task={task} onComplete={completeTask} />
            ))}
          </div>
        </div>
      )}
      
      {/* Empty State */}
      {todayView && 
       todayView.overdue.length === 0 && 
       todayView.due_today.length === 0 && 
       todayView.high_priority.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <Icons.Check />
          <p className="mt-2">All caught up! Add a task to get started.</p>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// TASK ITEM
// ═══════════════════════════════════════════════════════════════════════════════

const TaskItem: React.FC<{ 
  task: Task; 
  onComplete: (id: string) => Promise<void>;
}> = ({ task, onComplete }) => {
  const [completing, setCompleting] = useState(false);
  
  const handleComplete = async () => {
    setCompleting(true);
    await onComplete(task.id);
    setCompleting(false);
  };
  
  return (
    <div className={`flex items-center gap-3 p-3 bg-white rounded-lg border hover:shadow-sm transition-shadow ${task.status === 'done' ? 'opacity-60' : ''}`}>
      <button
        onClick={handleComplete}
        disabled={completing || task.status === 'done'}
        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors
          ${task.status === 'done' 
            ? 'bg-green-500 border-green-500 text-white' 
            : 'border-gray-300 hover:border-green-500'
          }
          ${completing ? 'animate-pulse' : ''}
        `}
      >
        {task.status === 'done' && <Icons.Check />}
      </button>
      
      <div className="flex-1 min-w-0">
        <div className={`font-medium ${task.status === 'done' ? 'line-through text-gray-500' : 'text-gray-800'}`}>
          {task.title}
        </div>
        {task.due_date && (
          <div className="text-xs text-gray-500 mt-0.5">
            Due: {new Date(task.due_date).toLocaleDateString()}
          </div>
        )}
      </div>
      
      <div className="flex items-center gap-2">
        <PriorityBadge priority={task.priority} />
        {task.ai_score && (
          <span className="text-xs text-gray-400" title="AI Score">
            {Math.round(task.ai_score)}
          </span>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// NOTES TAB
// ═══════════════════════════════════════════════════════════════════════════════

const NotesTab: React.FC = () => {
  const { 
    notes, folders, fetchNotes, createNote, deleteNote, enhanceNote,
    noteFilter, setNoteFilter, isLoading 
  } = usePersonalProductivityStore();
  
  const [newNoteContent, setNewNoteContent] = useState('');
  const [showEditor, setShowEditor] = useState(false);
  
  useEffect(() => {
    fetchNotes();
  }, [fetchNotes, noteFilter]);
  
  const handleCreateNote = async () => {
    if (!newNoteContent.trim()) return;
    
    await createNote(newNoteContent);
    setNewNoteContent('');
    setShowEditor(false);
  };
  
  return (
    <div className="flex gap-6">
      {/* Sidebar */}
      <div className="w-48 shrink-0">
        <h3 className="font-semibold text-gray-700 mb-3">Folders</h3>
        <ul className="space-y-1">
          <li>
            <button
              onClick={() => setNoteFilter({ folder: null })}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors
                ${!noteFilter.folder ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}
              `}
            >
              All Notes
            </button>
          </li>
          {folders.map(folder => (
            <li key={folder.name}>
              <button
                onClick={() => setNoteFilter({ folder: folder.name })}
                className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex justify-between
                  ${noteFilter.folder === folder.name ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}
                `}
              >
                <span>{folder.name}</span>
                <span className="text-gray-400 text-sm">{folder.count}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Main Content */}
      <div className="flex-1">
        {/* New Note Button */}
        {!showEditor ? (
          <button
            onClick={() => setShowEditor(true)}
            className="w-full mb-4 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors flex items-center justify-center gap-2 text-gray-600"
          >
            <Icons.Plus /> New Note
          </button>
        ) : (
          <div className="mb-4 p-4 bg-white rounded-lg border shadow-sm">
            <textarea
              value={newNoteContent}
              onChange={(e) => setNewNoteContent(e.target.value)}
              placeholder="Start writing your note... AI will auto-title and tag it!"
              className="w-full h-32 p-3 border border-gray-200 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              autoFocus
            />
            <div className="flex justify-end gap-2 mt-3">
              <button
                onClick={() => { setShowEditor(false); setNewNoteContent(''); }}
                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateNote}
                disabled={!newNoteContent.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              >
                <Icons.Sparkles /> Save with AI Enhancement
              </button>
            </div>
          </div>
        )}
        
        {/* Search */}
        <input
          type="text"
          value={noteFilter.search}
          onChange={(e) => setNoteFilter({ search: e.target.value })}
          placeholder="Search notes..."
          className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg"
        />
        
        {/* Notes List */}
        {isLoading ? (
          <div className="flex justify-center p-8">
            <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
          </div>
        ) : notes.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <Icons.Note />
            <p className="mt-2">No notes yet. Create your first note!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {notes.map(note => (
              <NoteCard 
                key={note.id} 
                note={note} 
                onDelete={() => deleteNote(note.id)}
                onEnhance={() => enhanceNote(note.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// NOTE CARD
// ═══════════════════════════════════════════════════════════════════════════════

const NoteCard: React.FC<{
  note: Note;
  onDelete: () => void;
  onEnhance: () => void;
}> = ({ note, onDelete, onEnhance }) => {
  return (
    <div className="p-4 bg-white rounded-lg border hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-gray-800 truncate">{note.title}</h4>
          <p className="text-sm text-gray-600 mt-1 line-clamp-2">{note.content}</p>
          
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            {note.folder && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                {note.folder}
              </span>
            )}
            {note.tags.slice(0, 3).map(tag => (
              <span key={tag} className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs">
                #{tag}
              </span>
            ))}
            {note.ai_enhanced && (
              <span className="text-xs text-purple-600 flex items-center gap-1">
                <Icons.Sparkles /> AI Enhanced
              </span>
            )}
          </div>
        </div>
        
        <div className="flex items-center gap-1 ml-4">
          {!note.ai_enhanced && (
            <button
              onClick={onEnhance}
              className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg"
              title="Enhance with AI"
            >
              <Icons.Sparkles />
            </button>
          )}
          <button
            onClick={onDelete}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
            title="Delete"
          >
            <Icons.Trash />
          </button>
        </div>
      </div>
      
      <div className="flex items-center justify-between mt-3 pt-3 border-t text-xs text-gray-400">
        <span>{note.word_count} words</span>
        <span>{new Date(note.updated_at).toLocaleDateString()}</span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// TASKS TAB
// ═══════════════════════════════════════════════════════════════════════════════

const TasksTab: React.FC = () => {
  const { 
    tasks, projects, fetchTasks, fetchProjects, createTask, completeTask, deleteTask,
    taskFilter, setTaskFilter, isLoading 
  } = usePersonalProductivityStore();
  
  const [newTaskTitle, setNewTaskTitle] = useState('');
  
  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, [fetchTasks, fetchProjects, taskFilter]);
  
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;
    
    await createTask(newTaskTitle);
    setNewTaskTitle('');
  };
  
  return (
    <div className="flex gap-6">
      {/* Sidebar */}
      <div className="w-48 shrink-0">
        <h3 className="font-semibold text-gray-700 mb-3">Projects</h3>
        <ul className="space-y-1">
          <li>
            <button
              onClick={() => setTaskFilter({ project_id: null })}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors
                ${!taskFilter.project_id ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}
              `}
            >
              All Tasks
            </button>
          </li>
          {projects.map(project => (
            <li key={project.id}>
              <button
                onClick={() => setTaskFilter({ project_id: project.id })}
                className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center gap-2
                  ${taskFilter.project_id === project.id ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}
                `}
              >
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: project.color }} />
                <span className="flex-1 truncate">{project.name}</span>
                <span className="text-gray-400 text-sm">{project.task_count}</span>
              </button>
            </li>
          ))}
        </ul>
        
        <h3 className="font-semibold text-gray-700 mb-3 mt-6">Filters</h3>
        <ul className="space-y-1">
          <li>
            <button
              onClick={() => setTaskFilter({ overdue: !taskFilter.overdue })}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors
                ${taskFilter.overdue ? 'bg-red-100 text-red-800' : 'hover:bg-gray-100'}
              `}
            >
              🔴 Overdue
            </button>
          </li>
          <li>
            <button
              onClick={() => setTaskFilter({ due_today: !taskFilter.due_today })}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors
                ${taskFilter.due_today ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}
              `}
            >
              📅 Due Today
            </button>
          </li>
        </ul>
      </div>
      
      {/* Main Content */}
      <div className="flex-1">
        {/* Quick Add */}
        <form onSubmit={handleCreateTask} className="flex gap-2 mb-4">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Add a task..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Add
          </button>
        </form>
        
        {/* Tasks List */}
        {isLoading ? (
          <div className="flex justify-center p-8">
            <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <Icons.Task />
            <p className="mt-2">No tasks. Add your first task!</p>
          </div>
        ) : (
          <div className="space-y-2">
            {tasks.map(task => (
              <TaskItem 
                key={task.id} 
                task={task} 
                onComplete={completeTask}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// STATS TAB
// ═══════════════════════════════════════════════════════════════════════════════

const StatsTab: React.FC = () => {
  const { noteStats, taskStats, fetchStats } = usePersonalProductivityStore();
  
  useEffect(() => {
    fetchStats();
  }, [fetchStats]);
  
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-gray-800">Productivity Statistics</h2>
      
      <div className="grid grid-cols-2 gap-6">
        {/* Note Stats */}
        <div className="bg-white p-6 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <Icons.Note /> Notes
          </h3>
          {noteStats ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-blue-700">{noteStats.total_notes}</div>
                  <div className="text-sm text-blue-600">Total Notes</div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-purple-700">{noteStats.total_words.toLocaleString()}</div>
                  <div className="text-sm text-purple-600">Total Words</div>
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-600 mb-2">By Type</h4>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(noteStats.by_type).map(([type, count]) => (
                    <span key={type} className="px-2 py-1 bg-gray-100 rounded text-sm">
                      {type}: {count}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="animate-pulse h-32 bg-gray-100 rounded" />
          )}
        </div>
        
        {/* Task Stats */}
        <div className="bg-white p-6 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <Icons.Task /> Tasks
          </h3>
          {taskStats ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-green-700">{taskStats.completion_rate}%</div>
                  <div className="text-sm text-green-600">Completion Rate</div>
                </div>
                <div className="bg-red-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-red-700">{taskStats.overdue}</div>
                  <div className="text-sm text-red-600">Overdue</div>
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-600 mb-2">By Priority</h4>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(taskStats.by_priority).map(([priority, count]) => (
                    <span key={priority} className="px-2 py-1 bg-gray-100 rounded text-sm">
                      {priority}: {count}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="animate-pulse h-32 bg-gray-100 rounded" />
          )}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ═══════════════════════════════════════════════════════════════════════════════

export const PersonalProductivityPage: React.FC = () => {
  const { activeTab, setActiveTab, error, clearError } = usePersonalProductivityStore();
  
  const tabs = [
    { id: 'today' as const, label: 'Today', icon: Icons.Today },
    { id: 'tasks' as const, label: 'Tasks', icon: Icons.Task },
    { id: 'notes' as const, label: 'Notes', icon: Icons.Note },
    { id: 'stats' as const, label: 'Stats', icon: Icons.Stats },
  ];
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Personal Productivity</h1>
              <p className="text-sm text-gray-500">AI-powered notes & task management</p>
            </div>
            <div className="flex items-center gap-2 text-sm text-purple-600">
              <Icons.Sparkles /> 28 AI Agents Active
            </div>
          </div>
          
          {/* Tabs */}
          <div className="flex gap-1 mt-4">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors
                  ${activeTab === tab.id 
                    ? 'bg-blue-100 text-blue-800' 
                    : 'text-gray-600 hover:bg-gray-100'
                  }
                `}
              >
                <tab.icon /> {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>
      
      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-3 flex items-center justify-between">
          <span className="text-red-700">{error}</span>
          <button onClick={clearError} className="text-red-600 hover:text-red-800">×</button>
        </div>
      )}
      
      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        {activeTab === 'today' && <TodayTab />}
        {activeTab === 'tasks' && <TasksTab />}
        {activeTab === 'notes' && <NotesTab />}
        {activeTab === 'stats' && <StatsTab />}
      </div>
    </div>
  );
};

export default PersonalProductivityPage;
