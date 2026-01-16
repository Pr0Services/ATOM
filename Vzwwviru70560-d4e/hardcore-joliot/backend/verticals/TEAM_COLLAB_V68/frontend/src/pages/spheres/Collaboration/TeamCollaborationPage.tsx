/**
 * CHE·NU™ V68 - Team Collaboration Page
 * 
 * Slack/Teams killer at $29/mo flat vs $8.75/user/mo
 * Complete team communication with AI-powered features
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useCollaborationStore } from '../../../stores/collaborationStore';
import {
  MessageSquare, Hash, Lock, Volume2, Archive,
  Send, Smile, Paperclip, MoreVertical, Pin, Edit2, Trash2,
  Users, Bell, Search, Plus, Settings, ChevronDown, ChevronRight,
  AtSign, Reply, ThumbsUp, Heart, Star, Check, Clock,
  Zap, Brain, TrendingUp, AlertCircle, HelpCircle,
  BarChart3, MessageCircle, UserPlus, LogOut, Eye, EyeOff,
  Circle, Moon, MinusCircle, X, Home, Inbox, Bookmark
} from 'lucide-react';

// ============================================================================
// TYPES
// ============================================================================

type ViewMode = 'channels' | 'dms' | 'threads' | 'mentions' | 'search';
type StatusType = 'online' | 'away' | 'dnd' | 'offline';

interface EmojiOption {
  emoji: string;
  name: string;
}

const QUICK_REACTIONS: EmojiOption[] = [
  { emoji: '👍', name: 'thumbsup' },
  { emoji: '❤️', name: 'heart' },
  { emoji: '😄', name: 'smile' },
  { emoji: '🎉', name: 'tada' },
  { emoji: '👀', name: 'eyes' },
  { emoji: '🚀', name: 'rocket' },
];

const STATUS_OPTIONS: { value: StatusType; label: string; icon: React.ReactNode; color: string }[] = [
  { value: 'online', label: 'Online', icon: <Circle className="w-3 h-3 fill-green-500 text-green-500" />, color: 'text-green-500' },
  { value: 'away', label: 'Away', icon: <Clock className="w-3 h-3 text-yellow-500" />, color: 'text-yellow-500' },
  { value: 'dnd', label: 'Do Not Disturb', icon: <MinusCircle className="w-3 h-3 text-red-500" />, color: 'text-red-500' },
  { value: 'offline', label: 'Offline', icon: <Circle className="w-3 h-3 text-gray-400" />, color: 'text-gray-400' },
];

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const TeamCollaborationPage: React.FC = () => {
  const store = useCollaborationStore();
  const [viewMode, setViewMode] = useState<ViewMode>('channels');
  const [messageInput, setMessageInput] = useState('');
  const [showNewChannel, setShowNewChannel] = useState(false);
  const [showNewDM, setShowNewDM] = useState(false);
  const [showNewWorkspace, setShowNewWorkspace] = useState(false);
  const [showPollCreator, setShowPollCreator] = useState(false);
  const [editingMessage, setEditingMessage] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');
  const [showAIPanel, setShowAIPanel] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    channels: true,
    dms: true,
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Initialize
  useEffect(() => {
    store.fetchWorkspaces();
  }, []);

  // Load workspace data when changed
  useEffect(() => {
    if (store.currentWorkspaceId) {
      store.fetchChannels(store.currentWorkspaceId);
      store.fetchDirectConversations(store.currentWorkspaceId);
      store.fetchMembers(store.currentWorkspaceId);
      store.fetchNotifications();
    }
  }, [store.currentWorkspaceId]);

  // Load messages when channel changes
  useEffect(() => {
    if (store.currentChannelId) {
      store.fetchMessages(store.currentChannelId);
    }
  }, [store.currentChannelId]);

  // Load DM messages
  useEffect(() => {
    if (store.currentConversationId) {
      // DMs use conversation ID as channel for messages
      store.fetchMessages(store.currentConversationId);
    }
  }, [store.currentConversationId]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [store.messages]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setViewMode('search');
      }
      if (e.key === 'Escape') {
        setShowAIPanel(false);
        setShowNewChannel(false);
        setShowNewDM(false);
        setEditingMessage(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Get current workspace
  const currentWorkspace = store.workspaces.find(w => w.id === store.currentWorkspaceId);
  const currentChannel = store.channels.find(c => c.id === store.currentChannelId);
  const currentConversation = store.directConversations.find(d => d.id === store.currentConversationId);

  // Send message handler
  const handleSendMessage = async () => {
    if (!messageInput.trim()) return;
    
    const channelId = store.currentChannelId || store.currentConversationId;
    if (!channelId) return;

    await store.sendMessage(channelId, messageInput, 'current_user');
    setMessageInput('');
    inputRef.current?.focus();
  };

  // Toggle section
  const toggleSection = (section: 'channels' | 'dms') => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  // Render status indicator
  const renderStatus = (status: StatusType) => {
    const option = STATUS_OPTIONS.find(s => s.value === status);
    return option?.icon || <Circle className="w-3 h-3 text-gray-400" />;
  };

  // ============================================================================
  // SIDEBAR
  // ============================================================================

  const renderSidebar = () => (
    <div className="w-64 bg-gray-900 text-gray-300 flex flex-col h-full">
      {/* Workspace Header */}
      <div className="p-4 border-b border-gray-700">
        <button 
          className="flex items-center justify-between w-full hover:bg-gray-800 rounded p-2 -m-2"
          onClick={() => setShowNewWorkspace(true)}
        >
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center text-white font-bold">
              {currentWorkspace?.name?.[0] || 'W'}
            </div>
            <div className="text-left">
              <div className="font-semibold text-white truncate max-w-[140px]">
                {currentWorkspace?.name || 'Select Workspace'}
              </div>
              <div className="text-xs text-gray-500">
                {store.members.length} members
              </div>
            </div>
          </div>
          <ChevronDown className="w-4 h-4" />
        </button>
      </div>

      {/* Quick Actions */}
      <div className="p-2 border-b border-gray-700">
        <button
          onClick={() => setViewMode('threads')}
          className={`flex items-center gap-2 w-full p-2 rounded hover:bg-gray-800 ${viewMode === 'threads' ? 'bg-gray-800 text-white' : ''}`}
        >
          <MessageCircle className="w-4 h-4" />
          <span>Threads</span>
        </button>
        <button
          onClick={() => setViewMode('mentions')}
          className={`flex items-center gap-2 w-full p-2 rounded hover:bg-gray-800 ${viewMode === 'mentions' ? 'bg-gray-800 text-white' : ''}`}
        >
          <AtSign className="w-4 h-4" />
          <span>Mentions</span>
          {store.notifications.filter(n => !n.read).length > 0 && (
            <span className="ml-auto bg-red-500 text-white text-xs px-1.5 rounded-full">
              {store.notifications.filter(n => !n.read).length}
            </span>
          )}
        </button>
        <button
          onClick={() => setViewMode('search')}
          className="flex items-center gap-2 w-full p-2 rounded hover:bg-gray-800 text-gray-400"
        >
          <Search className="w-4 h-4" />
          <span>Search</span>
          <span className="ml-auto text-xs">⌘K</span>
        </button>
      </div>

      {/* Channels Section */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-2">
          <button
            onClick={() => toggleSection('channels')}
            className="flex items-center gap-1 w-full p-1 text-sm text-gray-400 hover:text-white"
          >
            {expandedSections.channels ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
            <span>Channels</span>
          </button>
          
          {expandedSections.channels && (
            <div className="mt-1 space-y-0.5">
              {store.channels.filter(c => c.type !== 'archived').map(channel => (
                <button
                  key={channel.id}
                  onClick={() => {
                    store.setCurrentChannel(channel.id);
                    store.setCurrentConversation(null);
                    setViewMode('channels');
                  }}
                  className={`flex items-center gap-2 w-full p-1.5 rounded text-sm hover:bg-gray-800 ${
                    store.currentChannelId === channel.id ? 'bg-purple-600 text-white' : ''
                  }`}
                >
                  {channel.type === 'private' ? (
                    <Lock className="w-4 h-4" />
                  ) : channel.type === 'announcement' ? (
                    <Volume2 className="w-4 h-4" />
                  ) : (
                    <Hash className="w-4 h-4" />
                  )}
                  <span className="truncate">{channel.name}</span>
                </button>
              ))}
              
              <button
                onClick={() => setShowNewChannel(true)}
                className="flex items-center gap-2 w-full p-1.5 rounded text-sm text-gray-500 hover:bg-gray-800 hover:text-white"
              >
                <Plus className="w-4 h-4" />
                <span>Add channel</span>
              </button>
            </div>
          )}
        </div>

        {/* Direct Messages Section */}
        <div className="p-2">
          <button
            onClick={() => toggleSection('dms')}
            className="flex items-center gap-1 w-full p-1 text-sm text-gray-400 hover:text-white"
          >
            {expandedSections.dms ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
            <span>Direct Messages</span>
          </button>
          
          {expandedSections.dms && (
            <div className="mt-1 space-y-0.5">
              {store.directConversations.map(dm => (
                <button
                  key={dm.id}
                  onClick={() => {
                    store.setCurrentConversation(dm.id);
                    store.setCurrentChannel(null);
                    setViewMode('dms');
                  }}
                  className={`flex items-center gap-2 w-full p-1.5 rounded text-sm hover:bg-gray-800 ${
                    store.currentConversationId === dm.id ? 'bg-purple-600 text-white' : ''
                  }`}
                >
                  <div className="relative">
                    <div className="w-5 h-5 bg-gray-600 rounded-full flex items-center justify-center text-xs">
                      {dm.is_group ? dm.participant_ids.length : dm.participant_ids[0]?.[0]?.toUpperCase() || 'U'}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5">
                      {renderStatus('online')}
                    </div>
                  </div>
                  <span className="truncate">
                    {dm.name || dm.participant_ids.slice(0, 2).join(', ')}
                  </span>
                </button>
              ))}
              
              <button
                onClick={() => setShowNewDM(true)}
                className="flex items-center gap-2 w-full p-1.5 rounded text-sm text-gray-500 hover:bg-gray-800 hover:text-white"
              >
                <Plus className="w-4 h-4" />
                <span>New message</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* User Status */}
      <div className="p-3 border-t border-gray-700">
        <div className="flex items-center gap-2">
          <div className="relative">
            <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
              U
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-gray-900 rounded-full flex items-center justify-center">
              {renderStatus('online')}
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-white truncate">Current User</div>
            <div className="text-xs text-gray-500">Active</div>
          </div>
          <button className="p-1.5 hover:bg-gray-800 rounded">
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );

  // ============================================================================
  // MESSAGE AREA
  // ============================================================================

  const renderMessageArea = () => {
    const channelName = currentChannel?.name || currentConversation?.name || 'Select a channel';
    const channelTopic = currentChannel?.topic;

    return (
      <div className="flex-1 flex flex-col bg-white">
        {/* Channel Header */}
        <div className="h-14 border-b flex items-center justify-between px-4">
          <div className="flex items-center gap-2">
            {currentChannel ? (
              currentChannel.type === 'private' ? <Lock className="w-5 h-5 text-gray-500" /> : <Hash className="w-5 h-5 text-gray-500" />
            ) : (
              <MessageSquare className="w-5 h-5 text-gray-500" />
            )}
            <div>
              <h2 className="font-semibold">{channelName}</h2>
              {channelTopic && (
                <p className="text-xs text-gray-500 truncate max-w-md">{channelTopic}</p>
              )}
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowAIPanel(!showAIPanel)}
              className={`p-2 rounded hover:bg-gray-100 ${showAIPanel ? 'bg-purple-100 text-purple-600' : ''}`}
              title="AI Assistant"
            >
              <Brain className="w-5 h-5" />
            </button>
            <button
              onClick={() => store.toggleMembersList()}
              className={`p-2 rounded hover:bg-gray-100 ${store.showMembersList ? 'bg-gray-200' : ''}`}
            >
              <Users className="w-5 h-5" />
            </button>
            <button className="p-2 rounded hover:bg-gray-100">
              <MoreVertical className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {store.messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <MessageSquare className="w-16 h-16 mb-4 text-gray-300" />
              <p className="text-lg font-medium">No messages yet</p>
              <p className="text-sm">Start the conversation!</p>
            </div>
          ) : (
            store.messages.map(message => (
              <div key={message.id} className="group flex gap-3 hover:bg-gray-50 -mx-4 px-4 py-1 rounded">
                {/* Avatar */}
                <div className="w-9 h-9 bg-gradient-to-br from-green-500 to-blue-500 rounded-lg flex items-center justify-center text-white font-semibold flex-shrink-0">
                  {message.sender_id[0]?.toUpperCase() || 'U'}
                </div>
                
                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-2">
                    <span className="font-semibold">{message.sender_id}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    {message.is_pinned && (
                      <span className="text-xs bg-yellow-100 text-yellow-700 px-1.5 rounded">📌 Pinned</span>
                    )}
                    {message.is_edited && (
                      <span className="text-xs text-gray-400">(edited)</span>
                    )}
                  </div>
                  
                  {editingMessage === message.id ? (
                    <div className="mt-1">
                      <textarea
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        className="w-full p-2 border rounded resize-none"
                        rows={2}
                        autoFocus
                      />
                      <div className="flex gap-2 mt-1">
                        <button
                          onClick={async () => {
                            await store.editMessage(message.channel_id, message.id, editContent, message.sender_id);
                            setEditingMessage(null);
                          }}
                          className="px-3 py-1 bg-green-500 text-white rounded text-sm"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setEditingMessage(null)}
                          className="px-3 py-1 bg-gray-200 rounded text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-800 whitespace-pre-wrap">{message.content}</p>
                  )}
                  
                  {/* Attachments */}
                  {message.attachments && message.attachments.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {message.attachments.map((att, i) => (
                        <div key={i} className="flex items-center gap-1 bg-gray-100 px-2 py-1 rounded text-sm">
                          <Paperclip className="w-3 h-3" />
                          <span>{att}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {/* Reactions */}
                  {message.reactions && Object.keys(message.reactions).length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {Object.entries(message.reactions).map(([emoji, users]) => (
                        <button
                          key={emoji}
                          onClick={() => store.addReaction(message.channel_id, message.id, emoji, 'current_user')}
                          className="flex items-center gap-1 px-2 py-0.5 bg-gray-100 hover:bg-gray-200 rounded-full text-sm"
                        >
                          <span>{emoji}</span>
                          <span className="text-gray-600">{(users as string[]).length}</span>
                        </button>
                      ))}
                    </div>
                  )}
                  
                  {/* Thread indicator */}
                  {message.thread_id && (
                    <button
                      onClick={() => store.setCurrentThread(message.thread_id!)}
                      className="flex items-center gap-1 mt-2 text-sm text-purple-600 hover:underline"
                    >
                      <Reply className="w-4 h-4" />
                      <span>View thread</span>
                    </button>
                  )}
                </div>
                
                {/* Actions (hover) */}
                <div className="opacity-0 group-hover:opacity-100 flex items-start gap-1">
                  {QUICK_REACTIONS.slice(0, 3).map(({ emoji, name }) => (
                    <button
                      key={name}
                      onClick={() => store.addReaction(message.channel_id, message.id, emoji, 'current_user')}
                      className="p-1 hover:bg-gray-200 rounded"
                      title={name}
                    >
                      {emoji}
                    </button>
                  ))}
                  <button
                    onClick={() => {
                      setEditingMessage(message.id);
                      setEditContent(message.content);
                    }}
                    className="p-1 hover:bg-gray-200 rounded"
                    title="Edit"
                  >
                    <Edit2 className="w-4 h-4 text-gray-500" />
                  </button>
                  <button
                    onClick={() => store.pinMessage(message.channel_id, message.id, 'current_user')}
                    className="p-1 hover:bg-gray-200 rounded"
                    title="Pin"
                  >
                    <Pin className="w-4 h-4 text-gray-500" />
                  </button>
                  <button
                    onClick={() => store.deleteMessage(message.channel_id, message.id, message.sender_id)}
                    className="p-1 hover:bg-gray-200 rounded"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div className="p-4 border-t">
          <div className="flex items-end gap-2 bg-gray-100 rounded-lg p-2">
            <button className="p-2 hover:bg-gray-200 rounded">
              <Plus className="w-5 h-5 text-gray-500" />
            </button>
            <textarea
              ref={inputRef}
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder={`Message ${currentChannel ? '#' + currentChannel.name : 'here'}...`}
              className="flex-1 bg-transparent resize-none outline-none max-h-32"
              rows={1}
            />
            <button className="p-2 hover:bg-gray-200 rounded">
              <Smile className="w-5 h-5 text-gray-500" />
            </button>
            <button className="p-2 hover:bg-gray-200 rounded">
              <Paperclip className="w-5 h-5 text-gray-500" />
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!messageInput.trim()}
              className={`p-2 rounded ${messageInput.trim() ? 'bg-purple-600 text-white hover:bg-purple-700' : 'bg-gray-300 text-gray-500'}`}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            <button
              onClick={() => setShowPollCreator(true)}
              className="flex items-center gap-1 hover:text-purple-600"
            >
              <BarChart3 className="w-4 h-4" />
              Create Poll
            </button>
            <span>
              <strong>Enter</strong> to send, <strong>Shift+Enter</strong> for new line
            </span>
          </div>
        </div>
      </div>
    );
  };

  // ============================================================================
  // AI PANEL
  // ============================================================================

  const renderAIPanel = () => {
    if (!showAIPanel) return null;

    return (
      <div className="w-80 border-l bg-gray-50 flex flex-col">
        <div className="p-4 border-b bg-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-600" />
              <h3 className="font-semibold">AI Assistant</h3>
            </div>
            <button onClick={() => setShowAIPanel(false)} className="p-1 hover:bg-gray-100 rounded">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Channel Summary */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="w-4 h-4 text-blue-500" />
              <h4 className="font-medium">Channel Summary</h4>
            </div>
            <button
              onClick={async () => {
                if (store.currentChannelId) {
                  await store.getChannelSummary(store.currentChannelId, 24);
                }
              }}
              className="w-full px-3 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 text-sm"
            >
              Generate 24h Summary
            </button>
            {store.channelSummary && (
              <div className="mt-3 text-sm text-gray-600">
                <p className="mb-2">{store.channelSummary.summary}</p>
                <div className="flex flex-wrap gap-1 mt-2">
                  {store.channelSummary.key_topics.map((topic, i) => (
                    <span key={i} className="px-2 py-0.5 bg-gray-100 rounded text-xs">{topic}</span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Smart Replies */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-4 h-4 text-yellow-500" />
              <h4 className="font-medium">Smart Replies</h4>
            </div>
            {store.smartReplies.length > 0 ? (
              <div className="space-y-2">
                {store.smartReplies.map((reply, i) => (
                  <button
                    key={i}
                    onClick={() => setMessageInput(reply.text)}
                    className="w-full text-left p-2 bg-gray-50 hover:bg-gray-100 rounded text-sm"
                  >
                    <span className="block">{reply.text}</span>
                    <span className="text-xs text-gray-500">{reply.tone}</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500">Select a message to get suggestions</p>
            )}
          </div>

          {/* Message Analysis */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-4 h-4 text-orange-500" />
              <h4 className="font-medium">Important Messages</h4>
            </div>
            <button
              onClick={async () => {
                if (store.currentChannelId) {
                  await store.getImportantMessages(store.currentChannelId, 24);
                }
              }}
              className="w-full px-3 py-2 bg-orange-50 text-orange-600 rounded hover:bg-orange-100 text-sm"
            >
              Find Important Messages
            </button>
          </div>

          {/* Action Items */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <Check className="w-4 h-4 text-green-500" />
              <h4 className="font-medium">Action Items</h4>
            </div>
            {store.messageAnalysis?.action_items && store.messageAnalysis.action_items.length > 0 ? (
              <ul className="space-y-1 text-sm">
                {store.messageAnalysis.action_items.map((item, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <Check className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500">No action items detected</p>
            )}
          </div>

          {/* Questions */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <HelpCircle className="w-4 h-4 text-purple-500" />
              <h4 className="font-medium">Open Questions</h4>
            </div>
            {store.messageAnalysis?.questions && store.messageAnalysis.questions.length > 0 ? (
              <ul className="space-y-1 text-sm">
                {store.messageAnalysis.questions.map((q, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <HelpCircle className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
                    <span>{q}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500">No open questions</p>
            )}
          </div>
        </div>
      </div>
    );
  };

  // ============================================================================
  // MEMBERS PANEL
  // ============================================================================

  const renderMembersPanel = () => {
    if (!store.showMembersList) return null;

    const onlineMembers = store.members.filter(m => m.status === 'online');
    const awayMembers = store.members.filter(m => m.status === 'away');
    const offlineMembers = store.members.filter(m => m.status === 'offline' || m.status === 'dnd');

    return (
      <div className="w-64 border-l bg-white flex flex-col">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Members ({store.members.length})</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {/* Online */}
          {onlineMembers.length > 0 && (
            <div className="mb-4">
              <div className="text-xs text-gray-500 uppercase px-2 mb-2">Online — {onlineMembers.length}</div>
              {onlineMembers.map(member => (
                <div key={member.user_id} className="flex items-center gap-2 p-2 rounded hover:bg-gray-50">
                  <div className="relative">
                    <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      {member.display_name?.[0] || member.user_id[0]}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5">
                      {renderStatus(member.status as StatusType)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{member.display_name || member.user_id}</div>
                    {member.status_text && (
                      <div className="text-xs text-gray-500 truncate">
                        {member.status_emoji} {member.status_text}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Away */}
          {awayMembers.length > 0 && (
            <div className="mb-4">
              <div className="text-xs text-gray-500 uppercase px-2 mb-2">Away — {awayMembers.length}</div>
              {awayMembers.map(member => (
                <div key={member.user_id} className="flex items-center gap-2 p-2 rounded hover:bg-gray-50">
                  <div className="relative">
                    <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      {member.display_name?.[0] || member.user_id[0]}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5">
                      {renderStatus(member.status as StatusType)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate text-gray-600">{member.display_name || member.user_id}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Offline */}
          {offlineMembers.length > 0 && (
            <div>
              <div className="text-xs text-gray-500 uppercase px-2 mb-2">Offline — {offlineMembers.length}</div>
              {offlineMembers.map(member => (
                <div key={member.user_id} className="flex items-center gap-2 p-2 rounded hover:bg-gray-50 opacity-60">
                  <div className="relative">
                    <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      {member.display_name?.[0] || member.user_id[0]}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5">
                      {renderStatus(member.status as StatusType)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate text-gray-500">{member.display_name || member.user_id}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  // ============================================================================
  // MODALS
  // ============================================================================

  const renderNewChannelModal = () => {
    if (!showNewChannel) return null;

    const [name, setName] = useState('');
    const [isPrivate, setIsPrivate] = useState(false);
    const [topic, setTopic] = useState('');

    const handleCreate = async () => {
      if (!name.trim() || !store.currentWorkspaceId) return;
      await store.createChannel(store.currentWorkspaceId, name, isPrivate ? 'private' : 'public', 'current_user', topic || undefined);
      setShowNewChannel(false);
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h2 className="text-xl font-bold mb-4">Create a channel</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Channel name</label>
              <div className="flex items-center gap-2 border rounded-lg p-2">
                <Hash className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value.toLowerCase().replace(/\s+/g, '-'))}
                  placeholder="e.g. marketing"
                  className="flex-1 outline-none"
                  autoFocus
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Topic (optional)</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="What's this channel about?"
                className="w-full border rounded-lg p-2 outline-none"
              />
            </div>

            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer">
              <input
                type="checkbox"
                checked={isPrivate}
                onChange={(e) => setIsPrivate(e.target.checked)}
                className="w-5 h-5 rounded"
              />
              <div>
                <div className="font-medium flex items-center gap-1">
                  <Lock className="w-4 h-4" />
                  Make private
                </div>
                <div className="text-sm text-gray-500">Only invited members can see this channel</div>
              </div>
            </label>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <button
              onClick={() => setShowNewChannel(false)}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleCreate}
              disabled={!name.trim()}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              Create Channel
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderNewDMModal = () => {
    if (!showNewDM) return null;

    const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState('');

    const filteredMembers = store.members.filter(m => 
      m.user_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.display_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleCreate = async () => {
      if (selectedUsers.length === 0 || !store.currentWorkspaceId) return;
      await store.createDirectConversation(store.currentWorkspaceId, [...selectedUsers, 'current_user']);
      setShowNewDM(false);
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h2 className="text-xl font-bold mb-4">New Message</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">To:</label>
              <div className="flex flex-wrap gap-2 mb-2">
                {selectedUsers.map(userId => (
                  <span key={userId} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-2 py-1 rounded">
                    {userId}
                    <button onClick={() => setSelectedUsers(prev => prev.filter(u => u !== userId))}>
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for people..."
                className="w-full border rounded-lg p-2 outline-none"
                autoFocus
              />
            </div>

            <div className="max-h-48 overflow-y-auto border rounded-lg">
              {filteredMembers.map(member => (
                <button
                  key={member.user_id}
                  onClick={() => {
                    if (!selectedUsers.includes(member.user_id)) {
                      setSelectedUsers(prev => [...prev, member.user_id]);
                    }
                    setSearchQuery('');
                  }}
                  className="flex items-center gap-2 w-full p-2 hover:bg-gray-50 text-left"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-sm">
                    {member.display_name?.[0] || member.user_id[0]}
                  </div>
                  <span>{member.display_name || member.user_id}</span>
                  {selectedUsers.includes(member.user_id) && (
                    <Check className="w-4 h-4 text-green-500 ml-auto" />
                  )}
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <button
              onClick={() => setShowNewDM(false)}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleCreate}
              disabled={selectedUsers.length === 0}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              Start Conversation
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderPollModal = () => {
    if (!showPollCreator) return null;

    const [question, setQuestion] = useState('');
    const [options, setOptions] = useState(['', '']);
    const [allowMultiple, setAllowMultiple] = useState(false);
    const [anonymous, setAnonymous] = useState(false);

    const handleCreate = async () => {
      if (!question.trim() || !store.currentChannelId) return;
      const validOptions = options.filter(o => o.trim());
      if (validOptions.length < 2) return;

      await store.createPoll(
        store.currentChannelId,
        question,
        validOptions,
        'current_user',
        allowMultiple,
        anonymous
      );
      setShowPollCreator(false);
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h2 className="text-xl font-bold mb-4">Create a Poll</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Question</label>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What would you like to ask?"
                className="w-full border rounded-lg p-2 outline-none"
                autoFocus
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Options</label>
              {options.map((opt, i) => (
                <div key={i} className="flex items-center gap-2 mb-2">
                  <input
                    type="text"
                    value={opt}
                    onChange={(e) => {
                      const newOptions = [...options];
                      newOptions[i] = e.target.value;
                      setOptions(newOptions);
                    }}
                    placeholder={`Option ${i + 1}`}
                    className="flex-1 border rounded-lg p-2 outline-none"
                  />
                  {options.length > 2 && (
                    <button
                      onClick={() => setOptions(options.filter((_, idx) => idx !== i))}
                      className="p-1 hover:bg-gray-100 rounded"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  )}
                </div>
              ))}
              {options.length < 10 && (
                <button
                  onClick={() => setOptions([...options, ''])}
                  className="text-purple-600 text-sm hover:underline"
                >
                  + Add option
                </button>
              )}
            </div>

            <div className="space-y-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={allowMultiple}
                  onChange={(e) => setAllowMultiple(e.target.checked)}
                  className="w-4 h-4 rounded"
                />
                <span className="text-sm">Allow multiple selections</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={anonymous}
                  onChange={(e) => setAnonymous(e.target.checked)}
                  className="w-4 h-4 rounded"
                />
                <span className="text-sm">Anonymous voting</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <button
              onClick={() => setShowPollCreator(false)}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleCreate}
              disabled={!question.trim() || options.filter(o => o.trim()).length < 2}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              Create Poll
            </button>
          </div>
        </div>
      </div>
    );
  };

  // ============================================================================
  // MAIN RENDER
  // ============================================================================

  return (
    <div className="h-screen flex bg-gray-100">
      {/* Sidebar */}
      {renderSidebar()}

      {/* Main Content */}
      <div className="flex-1 flex">
        {renderMessageArea()}
        {renderAIPanel()}
        {renderMembersPanel()}
      </div>

      {/* Modals */}
      {renderNewChannelModal()}
      {renderNewDMModal()}
      {renderPollModal()}

      {/* Thread Panel */}
      {store.currentThreadId && store.showThreadPanel && (
        <div className="w-96 border-l bg-white flex flex-col">
          <div className="p-4 border-b flex items-center justify-between">
            <h3 className="font-semibold">Thread</h3>
            <button
              onClick={() => store.toggleThreadPanel()}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            {/* Thread messages would go here */}
            <p className="text-gray-500 text-sm">Thread replies...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamCollaborationPage;
