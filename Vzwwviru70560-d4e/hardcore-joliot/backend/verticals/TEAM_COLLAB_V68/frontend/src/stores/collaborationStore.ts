/**
 * CHE·NU™ V68 - Team Collaboration Store
 * Zustand state management for Slack/Teams killer
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ============================================================
// TYPES
// ============================================================

export type ChannelType = 'public' | 'private' | 'announcement' | 'archived';
export type MessageType = 'text' | 'file' | 'image' | 'video' | 'audio' | 'system' | 'poll';
export type ConversationType = 'channel' | 'direct' | 'group_dm' | 'thread';
export type MemberRole = 'owner' | 'admin' | 'member' | 'guest';
export type UserStatus = 'online' | 'away' | 'do_not_disturb' | 'offline';
export type MessagePriority = 'urgent' | 'high' | 'normal' | 'low';
export type SentimentType = 'positive' | 'neutral' | 'negative' | 'mixed';

export interface Workspace {
  id: string;
  name: string;
  description: string;
  icon_url?: string;
  owner_id: string;
  created_at: string;
}

export interface Channel {
  id: string;
  workspace_id: string;
  name: string;
  description: string;
  channel_type: ChannelType;
  topic: string;
  icon_emoji: string;
  is_default: boolean;
  member_count: number;
  created_at: string;
}

export interface Message {
  id: string;
  workspace_id: string;
  channel_id?: string;
  conversation_id?: string;
  thread_id?: string;
  sender_id: string;
  message_type: MessageType;
  content: string;
  mentions: string[];
  reactions: Record<string, string[]>;
  is_edited: boolean;
  is_pinned: boolean;
  reply_count: number;
  created_at: string;
}

export interface DirectConversation {
  id: string;
  workspace_id: string;
  participant_ids: string[];
  conversation_type: ConversationType;
  name?: string;
  created_at: string;
  last_message_at?: string;
}

export interface Thread {
  id: string;
  parent_message_id: string;
  channel_id: string;
  participant_ids: string[];
  reply_count: number;
  last_reply_at?: string;
  created_at: string;
}

export interface WorkspaceMember {
  id: string;
  workspace_id: string;
  user_id: string;
  display_name: string;
  avatar_url?: string;
  role: MemberRole;
  status: UserStatus;
  status_text: string;
  status_emoji: string;
  joined_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  workspace_id: string;
  channel_id?: string;
  message_id?: string;
  notification_type: string;
  title: string;
  body: string;
  is_read: boolean;
  created_at: string;
}

export interface Poll {
  id: string;
  message_id: string;
  question: string;
  options: string[];
  is_anonymous: boolean;
  is_multiple_choice: boolean;
  ends_at?: string;
}

export interface PollResults {
  question: string;
  options: Record<string, { count: number; voters: string[] }>;
  total_votes: number;
  is_ended: boolean;
}

export interface MessageAnalysis {
  message_id: string;
  priority: MessagePriority;
  sentiment: SentimentType;
  topics: string[];
  action_items: string[];
  questions: string[];
  key_points: string[];
  requires_response: boolean;
  confidence: number;
}

export interface ChannelSummary {
  channel_id: string;
  period_start: string;
  period_end: string;
  message_count: number;
  participant_count: number;
  key_topics: string[];
  decisions_made: string[];
  action_items: string[];
  unresolved_questions: string[];
  sentiment_breakdown: Record<string, number>;
  most_active_members: Array<{ user_id: string; message_count: number }>;
  summary_text: string;
  generated_at: string;
}

export interface SmartReply {
  suggestion: string;
  tone: string;
  confidence: number;
}

export interface Dashboard {
  workspace_id: string;
  channels_count: number;
  conversations_count: number;
  unread_notifications: number;
  members_count: number;
  online_members: number;
  recent_activity: Array<{
    message_id: string;
    channel_id: string;
    sender_id: string;
    content: string;
    created_at: string;
  }>;
}

// ============================================================
// STORE STATE
// ============================================================

interface CollaborationState {
  // Current context
  currentWorkspaceId: string | null;
  currentChannelId: string | null;
  currentConversationId: string | null;
  currentThreadId: string | null;
  currentUserId: string;
  
  // Data
  workspaces: Workspace[];
  channels: Channel[];
  messages: Message[];
  conversations: DirectConversation[];
  threads: Record<string, Thread>;
  members: WorkspaceMember[];
  notifications: Notification[];
  polls: Record<string, Poll>;
  
  // UI State
  isLoading: boolean;
  error: string | null;
  showSidebar: boolean;
  showThreadPanel: boolean;
  showMembersList: boolean;
  searchQuery: string;
  
  // AI Analysis cache
  messageAnalysis: Record<string, MessageAnalysis>;
  channelSummaries: Record<string, ChannelSummary>;
  smartReplies: Record<string, SmartReply[]>;
  
  // Actions
  setCurrentWorkspace: (workspaceId: string) => void;
  setCurrentChannel: (channelId: string | null) => void;
  setCurrentConversation: (conversationId: string | null) => void;
  setCurrentThread: (threadId: string | null) => void;
  
  // Workspace actions
  fetchWorkspaces: () => Promise<void>;
  createWorkspace: (name: string, description?: string) => Promise<Workspace>;
  
  // Channel actions
  fetchChannels: (workspaceId: string) => Promise<void>;
  createChannel: (name: string, description?: string, type?: ChannelType) => Promise<Channel>;
  joinChannel: (channelId: string) => Promise<void>;
  leaveChannel: (channelId: string) => Promise<void>;
  archiveChannel: (channelId: string) => Promise<void>;
  setChannelTopic: (channelId: string, topic: string) => Promise<void>;
  
  // Message actions
  fetchMessages: (channelId?: string, conversationId?: string, threadId?: string) => Promise<void>;
  sendMessage: (content: string, channelId?: string, conversationId?: string, threadId?: string) => Promise<Message>;
  editMessage: (messageId: string, content: string) => Promise<void>;
  deleteMessage: (messageId: string) => Promise<void>;
  pinMessage: (messageId: string) => Promise<void>;
  unpinMessage: (messageId: string) => Promise<void>;
  searchMessages: (query: string) => Promise<Message[]>;
  
  // Reaction actions
  addReaction: (messageId: string, emoji: string) => Promise<void>;
  removeReaction: (messageId: string, emoji: string) => Promise<void>;
  
  // Thread actions
  fetchThread: (parentMessageId: string) => Promise<void>;
  fetchThreadReplies: (parentMessageId: string) => Promise<void>;
  
  // DM actions
  fetchConversations: () => Promise<void>;
  createDM: (participantIds: string[]) => Promise<DirectConversation>;
  
  // Member actions
  fetchMembers: () => Promise<void>;
  updateStatus: (status: UserStatus, statusText?: string, statusEmoji?: string) => Promise<void>;
  inviteToChannel: (channelId: string, userId: string) => Promise<void>;
  
  // Notification actions
  fetchNotifications: (unreadOnly?: boolean) => Promise<void>;
  markNotificationRead: (notificationId: string) => Promise<void>;
  markAllNotificationsRead: () => Promise<void>;
  
  // Poll actions
  createPoll: (messageId: string, question: string, options: string[], isAnonymous?: boolean, isMultipleChoice?: boolean) => Promise<Poll>;
  votePoll: (pollId: string, option: string) => Promise<void>;
  fetchPollResults: (pollId: string) => Promise<PollResults>;
  
  // AI actions
  analyzeMessage: (messageId: string) => Promise<MessageAnalysis>;
  getChannelSummary: (channelId: string, periodHours?: number) => Promise<ChannelSummary>;
  getSmartReplies: (messageId: string) => Promise<SmartReply[]>;
  getImportantMessages: (channelId: string) => Promise<Message[]>;
  
  // Dashboard
  fetchDashboard: () => Promise<Dashboard>;
  
  // UI actions
  toggleSidebar: () => void;
  toggleThreadPanel: () => void;
  toggleMembersList: () => void;
  setSearchQuery: (query: string) => void;
  clearError: () => void;
}

// ============================================================
// API BASE URL
// ============================================================

const API_BASE = '/api/v2/collaboration';

// ============================================================
// STORE IMPLEMENTATION
// ============================================================

export const useCollaborationStore = create<CollaborationState>()(
  persist(
    (set, get) => ({
      // Initial state
      currentWorkspaceId: null,
      currentChannelId: null,
      currentConversationId: null,
      currentThreadId: null,
      currentUserId: 'current_user', // Would come from auth
      
      workspaces: [],
      channels: [],
      messages: [],
      conversations: [],
      threads: {},
      members: [],
      notifications: [],
      polls: {},
      
      isLoading: false,
      error: null,
      showSidebar: true,
      showThreadPanel: false,
      showMembersList: true,
      searchQuery: '',
      
      messageAnalysis: {},
      channelSummaries: {},
      smartReplies: {},
      
      // Navigation
      setCurrentWorkspace: (workspaceId) => set({ currentWorkspaceId: workspaceId }),
      setCurrentChannel: (channelId) => set({ 
        currentChannelId: channelId, 
        currentConversationId: null,
        currentThreadId: null 
      }),
      setCurrentConversation: (conversationId) => set({ 
        currentConversationId: conversationId, 
        currentChannelId: null,
        currentThreadId: null 
      }),
      setCurrentThread: (threadId) => set({ currentThreadId: threadId, showThreadPanel: !!threadId }),
      
      // Workspace actions
      fetchWorkspaces: async () => {
        const { currentUserId } = get();
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/workspaces?user_id=${currentUserId}`);
          const workspaces = await response.json();
          set({ workspaces, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to fetch workspaces', isLoading: false });
        }
      },
      
      createWorkspace: async (name, description = '') => {
        const { currentUserId } = get();
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/workspaces`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description, owner_id: currentUserId }),
          });
          const workspace = await response.json();
          set((state) => ({ workspaces: [...state.workspaces, workspace], isLoading: false }));
          return workspace;
        } catch (error) {
          set({ error: 'Failed to create workspace', isLoading: false });
          throw error;
        }
      },
      
      // Channel actions
      fetchChannels: async (workspaceId) => {
        const { currentUserId } = get();
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/channels?workspace_id=${workspaceId}&user_id=${currentUserId}`);
          const channels = await response.json();
          set({ channels, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to fetch channels', isLoading: false });
        }
      },
      
      createChannel: async (name, description = '', type: ChannelType = 'public') => {
        const { currentWorkspaceId, currentUserId } = get();
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/channels`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              workspace_id: currentWorkspaceId,
              name,
              description,
              channel_type: type,
              created_by: currentUserId,
            }),
          });
          const channel = await response.json();
          set((state) => ({ channels: [...state.channels, channel], isLoading: false }));
          return channel;
        } catch (error) {
          set({ error: 'Failed to create channel', isLoading: false });
          throw error;
        }
      },
      
      joinChannel: async (channelId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/channels/${channelId}/join?user_id=${currentUserId}`, { method: 'POST' });
      },
      
      leaveChannel: async (channelId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/channels/${channelId}/leave?user_id=${currentUserId}`, { method: 'POST' });
      },
      
      archiveChannel: async (channelId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/channels/${channelId}/archive?archived_by=${currentUserId}`, { method: 'POST' });
        set((state) => ({
          channels: state.channels.filter(c => c.id !== channelId)
        }));
      },
      
      setChannelTopic: async (channelId, topic) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/channels/${channelId}/topic`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic, set_by: currentUserId }),
        });
        set((state) => ({
          channels: state.channels.map(c => c.id === channelId ? { ...c, topic } : c)
        }));
      },
      
      // Message actions
      fetchMessages: async (channelId, conversationId, threadId) => {
        set({ isLoading: true, error: null });
        try {
          let url = `${API_BASE}/messages?limit=50`;
          if (channelId) url += `&channel_id=${channelId}`;
          if (conversationId) url += `&conversation_id=${conversationId}`;
          if (threadId) url += `&thread_id=${threadId}`;
          
          const response = await fetch(url);
          const messages = await response.json();
          set({ messages, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to fetch messages', isLoading: false });
        }
      },
      
      sendMessage: async (content, channelId, conversationId, threadId) => {
        const { currentWorkspaceId, currentUserId } = get();
        const response = await fetch(`${API_BASE}/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            workspace_id: currentWorkspaceId,
            sender_id: currentUserId,
            content,
            channel_id: channelId,
            conversation_id: conversationId,
            thread_id: threadId,
          }),
        });
        const message = await response.json();
        set((state) => ({ messages: [message, ...state.messages] }));
        return message;
      },
      
      editMessage: async (messageId, content) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/messages/${messageId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content, edited_by: currentUserId }),
        });
        set((state) => ({
          messages: state.messages.map(m => 
            m.id === messageId ? { ...m, content, is_edited: true } : m
          )
        }));
      },
      
      deleteMessage: async (messageId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/messages/${messageId}?deleted_by=${currentUserId}`, { method: 'DELETE' });
        set((state) => ({
          messages: state.messages.filter(m => m.id !== messageId)
        }));
      },
      
      pinMessage: async (messageId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/messages/${messageId}/pin?pinned_by=${currentUserId}`, { method: 'POST' });
        set((state) => ({
          messages: state.messages.map(m => m.id === messageId ? { ...m, is_pinned: true } : m)
        }));
      },
      
      unpinMessage: async (messageId) => {
        await fetch(`${API_BASE}/messages/${messageId}/unpin`, { method: 'POST' });
        set((state) => ({
          messages: state.messages.map(m => m.id === messageId ? { ...m, is_pinned: false } : m)
        }));
      },
      
      searchMessages: async (query) => {
        const { currentWorkspaceId, currentUserId } = get();
        const response = await fetch(
          `${API_BASE}/messages/search?workspace_id=${currentWorkspaceId}&query=${encodeURIComponent(query)}&user_id=${currentUserId}`
        );
        const data = await response.json();
        return data.messages;
      },
      
      // Reaction actions
      addReaction: async (messageId, emoji) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/messages/${messageId}/reactions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: currentUserId, emoji }),
        });
        set((state) => ({
          messages: state.messages.map(m => {
            if (m.id === messageId) {
              const reactions = { ...m.reactions };
              if (!reactions[emoji]) reactions[emoji] = [];
              if (!reactions[emoji].includes(currentUserId)) {
                reactions[emoji] = [...reactions[emoji], currentUserId];
              }
              return { ...m, reactions };
            }
            return m;
          })
        }));
      },
      
      removeReaction: async (messageId, emoji) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/messages/${messageId}/reactions?user_id=${currentUserId}&emoji=${encodeURIComponent(emoji)}`, {
          method: 'DELETE'
        });
        set((state) => ({
          messages: state.messages.map(m => {
            if (m.id === messageId) {
              const reactions = { ...m.reactions };
              if (reactions[emoji]) {
                reactions[emoji] = reactions[emoji].filter(id => id !== currentUserId);
                if (reactions[emoji].length === 0) delete reactions[emoji];
              }
              return { ...m, reactions };
            }
            return m;
          })
        }));
      },
      
      // Thread actions
      fetchThread: async (parentMessageId) => {
        const response = await fetch(`${API_BASE}/threads/${parentMessageId}`);
        const thread = await response.json();
        set((state) => ({
          threads: { ...state.threads, [parentMessageId]: thread }
        }));
      },
      
      fetchThreadReplies: async (parentMessageId) => {
        const response = await fetch(`${API_BASE}/threads/${parentMessageId}/replies`);
        const replies = await response.json();
        set({ messages: replies });
      },
      
      // DM actions
      fetchConversations: async () => {
        const { currentWorkspaceId, currentUserId } = get();
        const response = await fetch(`${API_BASE}/dms?workspace_id=${currentWorkspaceId}&user_id=${currentUserId}`);
        const conversations = await response.json();
        set({ conversations });
      },
      
      createDM: async (participantIds) => {
        const { currentWorkspaceId } = get();
        const response = await fetch(`${API_BASE}/dms`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ workspace_id: currentWorkspaceId, participant_ids: participantIds }),
        });
        const dm = await response.json();
        set((state) => ({ conversations: [...state.conversations, dm] }));
        return dm;
      },
      
      // Member actions
      fetchMembers: async () => {
        const { currentWorkspaceId } = get();
        const response = await fetch(`${API_BASE}/members?workspace_id=${currentWorkspaceId}`);
        const members = await response.json();
        set({ members });
      },
      
      updateStatus: async (status, statusText = '', statusEmoji = '') => {
        const { currentWorkspaceId, currentUserId } = get();
        await fetch(`${API_BASE}/members/${currentWorkspaceId}/${currentUserId}/status`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status, status_text: statusText, status_emoji: statusEmoji }),
        });
        set((state) => ({
          members: state.members.map(m => 
            m.user_id === currentUserId ? { ...m, status, status_text: statusText, status_emoji: statusEmoji } : m
          )
        }));
      },
      
      inviteToChannel: async (channelId, userId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/channels/${channelId}/invite`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, invited_by: currentUserId }),
        });
      },
      
      // Notification actions
      fetchNotifications: async (unreadOnly = false) => {
        const { currentUserId } = get();
        const response = await fetch(`${API_BASE}/notifications?user_id=${currentUserId}&unread_only=${unreadOnly}`);
        const notifications = await response.json();
        set({ notifications });
      },
      
      markNotificationRead: async (notificationId) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/notifications/${notificationId}/read?user_id=${currentUserId}`, { method: 'POST' });
        set((state) => ({
          notifications: state.notifications.map(n => 
            n.id === notificationId ? { ...n, is_read: true } : n
          )
        }));
      },
      
      markAllNotificationsRead: async () => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/notifications/read-all?user_id=${currentUserId}`, { method: 'POST' });
        set((state) => ({
          notifications: state.notifications.map(n => ({ ...n, is_read: true }))
        }));
      },
      
      // Poll actions
      createPoll: async (messageId, question, options, isAnonymous = false, isMultipleChoice = false) => {
        const response = await fetch(`${API_BASE}/polls`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message_id: messageId,
            question,
            options,
            is_anonymous: isAnonymous,
            is_multiple_choice: isMultipleChoice,
          }),
        });
        const poll = await response.json();
        set((state) => ({ polls: { ...state.polls, [poll.id]: poll } }));
        return poll;
      },
      
      votePoll: async (pollId, option) => {
        const { currentUserId } = get();
        await fetch(`${API_BASE}/polls/${pollId}/vote`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: currentUserId, option }),
        });
      },
      
      fetchPollResults: async (pollId) => {
        const response = await fetch(`${API_BASE}/polls/${pollId}/results`);
        return response.json();
      },
      
      // AI actions
      analyzeMessage: async (messageId) => {
        const response = await fetch(`${API_BASE}/ai/analyze/${messageId}`);
        const analysis = await response.json();
        set((state) => ({
          messageAnalysis: { ...state.messageAnalysis, [messageId]: analysis }
        }));
        return analysis;
      },
      
      getChannelSummary: async (channelId, periodHours = 24) => {
        const response = await fetch(`${API_BASE}/ai/channel-summary/${channelId}?period_hours=${periodHours}`);
        const summary = await response.json();
        set((state) => ({
          channelSummaries: { ...state.channelSummaries, [channelId]: summary }
        }));
        return summary;
      },
      
      getSmartReplies: async (messageId) => {
        const response = await fetch(`${API_BASE}/ai/smart-replies/${messageId}`);
        const data = await response.json();
        set((state) => ({
          smartReplies: { ...state.smartReplies, [messageId]: data.suggestions }
        }));
        return data.suggestions;
      },
      
      getImportantMessages: async (channelId) => {
        const response = await fetch(`${API_BASE}/ai/important-messages/${channelId}`);
        const data = await response.json();
        return data.messages;
      },
      
      // Dashboard
      fetchDashboard: async () => {
        const { currentWorkspaceId, currentUserId } = get();
        const response = await fetch(`${API_BASE}/dashboard/${currentWorkspaceId}?user_id=${currentUserId}`);
        return response.json();
      },
      
      // UI actions
      toggleSidebar: () => set((state) => ({ showSidebar: !state.showSidebar })),
      toggleThreadPanel: () => set((state) => ({ showThreadPanel: !state.showThreadPanel })),
      toggleMembersList: () => set((state) => ({ showMembersList: !state.showMembersList })),
      setSearchQuery: (query) => set({ searchQuery: query }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'chenu-collaboration-storage',
      partialize: (state) => ({
        currentWorkspaceId: state.currentWorkspaceId,
        showSidebar: state.showSidebar,
        showMembersList: state.showMembersList,
      }),
    }
  )
);

export default useCollaborationStore;
