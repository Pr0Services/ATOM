// CHE·NU Mobile - Communications Screen (Tab 1)
// Phone-style interface: Nova chat by default + all agents
// Can call or text any agent

import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  FlatList, SectionList,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';
import { useAgentsStore } from '../store';
import { useOverlay } from '../providers/OverlayProvider';

// Tabs: Conversations | Contacts | Keypad
type TabType = 'conversations' | 'contacts' | 'keypad';

export default function CommunicationsScreen() {
  const navigation = useNavigation<any>();
  const { startCall, clearUnread } = useOverlay();
  const { allAgents, recentConversations } = useAgentsStore();
  const [activeTab, setActiveTab] = useState<TabType>('conversations');
  const [searchQuery, setSearchQuery] = useState('');

  // Clear unread when viewing conversations
  React.useEffect(() => {
    if (activeTab === 'conversations') clearUnread();
  }, [activeTab]);

  // Filter agents by search
  const filteredAgents = allAgents.filter(a => 
    a.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group agents by sphere for contacts
  const groupedAgents = filteredAgents.reduce((acc: any, agent: any) => {
    const sphere = agent.sphere || 'Autre';
    if (!acc[sphere]) acc[sphere] = [];
    acc[sphere].push(agent);
    return acc;
  }, {});

  const contactSections = Object.keys(groupedAgents).map(sphere => ({
    title: sphere,
    data: groupedAgents[sphere],
  }));

  const handleCall = (agent: any) => {
    startCall(agent.id, agent.name, agent.color);
    navigation.navigate('AgentCall', { 
      agentId: agent.id, 
      agentName: agent.name, 
      agentColor: agent.color 
    });
  };

  const handleChat = (agent: any) => {
    navigation.navigate('Conversation', { 
      agentId: agent.id, 
      agentName: agent.name 
    });
  };

  // Render conversation item
  const renderConversation = ({ item }: any) => {
    const isNova = item.agentId === 'nova';
    return (
      <TouchableOpacity 
        style={styles.conversationItem}
        onPress={() => handleChat(item)}
      >
        <View style={[styles.avatar, { backgroundColor: item.color || colors.primary }]}>
          {isNova ? (
            <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.novaAvatar}>
              <Text style={styles.avatarText}>N</Text>
            </LinearGradient>
          ) : (
            <Text style={styles.avatarText}>{item.name.charAt(0)}</Text>
          )}
        </View>
        <View style={styles.conversationInfo}>
          <View style={styles.conversationHeader}>
            <Text style={styles.conversationName}>{item.name}</Text>
            <Text style={styles.conversationTime}>{item.lastMessageTime || 'maintenant'}</Text>
          </View>
          <Text style={styles.conversationPreview} numberOfLines={1}>
            {item.lastMessage || 'Commencer une conversation...'}
          </Text>
        </View>
        {item.unread > 0 && (
          <View style={styles.unreadBadge}>
            <Text style={styles.unreadText}>{item.unread}</Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  // Render contact item
  const renderContact = ({ item }: any) => (
    <View style={styles.contactItem}>
      <View style={[styles.contactAvatar, { backgroundColor: item.color + '30' }]}>
        <Ionicons name={item.icon || 'person'} size={24} color={item.color} />
      </View>
      <View style={styles.contactInfo}>
        <Text style={styles.contactName}>{item.name}</Text>
        <Text style={styles.contactRole}>{item.role} • {item.level}</Text>
      </View>
      <View style={styles.contactActions}>
        <TouchableOpacity style={styles.actionButton} onPress={() => handleChat(item)}>
          <Ionicons name="chatbubble" size={20} color={colors.primary} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton} onPress={() => handleCall(item)}>
          <Ionicons name="call" size={20} color={colors.success} />
        </TouchableOpacity>
      </View>
    </View>
  );

  // Render section header
  const renderSectionHeader = ({ section }: any) => (
    <View style={styles.sectionHeader}>
      <Text style={styles.sectionTitle}>{section.title}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Messages</Text>
        <TouchableOpacity style={styles.headerButton}>
          <Ionicons name="create-outline" size={24} color={colors.primary} />
        </TouchableOpacity>
      </View>

      {/* Search */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color={colors.textMuted} />
        <TextInput
          style={styles.searchInput}
          placeholder="Rechercher..."
          placeholderTextColor={colors.textMuted}
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>

      {/* Tabs */}
      <View style={styles.tabs}>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'conversations' && styles.tabActive]}
          onPress={() => setActiveTab('conversations')}
        >
          <Ionicons 
            name="chatbubbles" 
            size={20} 
            color={activeTab === 'conversations' ? colors.primary : colors.textMuted} 
          />
          <Text style={[styles.tabText, activeTab === 'conversations' && styles.tabTextActive]}>
            Conversations
          </Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'contacts' && styles.tabActive]}
          onPress={() => setActiveTab('contacts')}
        >
          <Ionicons 
            name="people" 
            size={20} 
            color={activeTab === 'contacts' ? colors.primary : colors.textMuted} 
          />
          <Text style={[styles.tabText, activeTab === 'contacts' && styles.tabTextActive]}>
            Agents
          </Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'keypad' && styles.tabActive]}
          onPress={() => setActiveTab('keypad')}
        >
          <Ionicons 
            name="keypad" 
            size={20} 
            color={activeTab === 'keypad' ? colors.primary : colors.textMuted} 
          />
          <Text style={[styles.tabText, activeTab === 'keypad' && styles.tabTextActive]}>
            Clavier
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {activeTab === 'conversations' && (
        <FlatList
          data={[
            // Nova always first
            { 
              id: 'nova', 
              agentId: 'nova', 
              name: 'Nova', 
              color: colors.primary,
              lastMessage: 'Bonjour! Comment puis-je vous aider?',
              lastMessageTime: 'maintenant',
              unread: 0,
            },
            ...recentConversations,
          ]}
          renderItem={renderConversation}
          keyExtractor={(item) => item.id}
          style={styles.list}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyState}>
              <Ionicons name="chatbubbles-outline" size={64} color={colors.textMuted} />
              <Text style={styles.emptyTitle}>Aucune conversation</Text>
              <Text style={styles.emptyText}>Commencez par parler à Nova!</Text>
            </View>
          }
        />
      )}

      {activeTab === 'contacts' && (
        <SectionList
          sections={contactSections}
          renderItem={renderContact}
          renderSectionHeader={renderSectionHeader}
          keyExtractor={(item) => item.id}
          style={styles.list}
          contentContainerStyle={styles.listContent}
          stickySectionHeadersEnabled={false}
        />
      )}

      {activeTab === 'keypad' && (
        <View style={styles.keypadContainer}>
          <View style={styles.keypadDisplay}>
            <Text style={styles.keypadNumber}>Nova</Text>
          </View>
          <View style={styles.keypad}>
            {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map((key) => (
              <TouchableOpacity key={key} style={styles.keypadKey}>
                <Text style={styles.keypadKeyText}>{key}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <TouchableOpacity 
            style={styles.callButton}
            onPress={() => handleCall({ id: 'nova', name: 'Nova', color: colors.primary })}
          >
            <LinearGradient colors={[colors.success, '#059669']} style={styles.callButtonGradient}>
              <Ionicons name="call" size={28} color={colors.text} />
            </LinearGradient>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingTop: 60, paddingBottom: spacing.md, paddingHorizontal: spacing.lg,
    backgroundColor: colors.surface,
  },
  headerTitle: { color: colors.text, fontSize: typography.fontSize.xxl, fontWeight: 'bold' },
  headerButton: { padding: spacing.sm },
  searchContainer: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.sm,
    marginHorizontal: spacing.lg, marginVertical: spacing.md, padding: spacing.md,
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
  },
  searchInput: { flex: 1, color: colors.text, fontSize: typography.fontSize.md },
  tabs: {
    flexDirection: 'row', paddingHorizontal: spacing.lg, gap: spacing.sm,
    borderBottomWidth: 1, borderBottomColor: colors.border, paddingBottom: spacing.md,
  },
  tab: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs,
    paddingVertical: spacing.sm, borderRadius: borderRadius.lg,
  },
  tabActive: { backgroundColor: colors.primary + '20' },
  tabText: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  tabTextActive: { color: colors.primary, fontWeight: '600' },
  list: { flex: 1 },
  listContent: { paddingHorizontal: spacing.lg, paddingBottom: spacing.xxl },
  conversationItem: {
    flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.md,
    borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  avatar: { width: 52, height: 52, borderRadius: 26, justifyContent: 'center', alignItems: 'center' },
  novaAvatar: { width: '100%', height: '100%', borderRadius: 26, justifyContent: 'center', alignItems: 'center' },
  avatarText: { color: colors.text, fontSize: 20, fontWeight: 'bold' },
  conversationInfo: { flex: 1, marginLeft: spacing.md },
  conversationHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 },
  conversationName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '600' },
  conversationTime: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  conversationPreview: { color: colors.textSecondary, fontSize: typography.fontSize.sm },
  unreadBadge: {
    backgroundColor: colors.primary, borderRadius: 12, minWidth: 24, height: 24,
    justifyContent: 'center', alignItems: 'center', paddingHorizontal: 6,
  },
  unreadText: { color: colors.text, fontSize: 12, fontWeight: 'bold' },
  contactItem: {
    flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.md,
    backgroundColor: colors.surface, borderRadius: borderRadius.lg, marginBottom: spacing.sm,
    padding: spacing.md, ...shadows.sm,
  },
  contactAvatar: { width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center' },
  contactInfo: { flex: 1, marginLeft: spacing.md },
  contactName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '600' },
  contactRole: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  contactActions: { flexDirection: 'row', gap: spacing.sm },
  actionButton: { padding: spacing.sm, backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.full },
  sectionHeader: { paddingVertical: spacing.md, marginTop: spacing.md },
  sectionTitle: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold' },
  emptyState: { alignItems: 'center', paddingVertical: spacing.xxl * 2 },
  emptyTitle: { color: colors.text, fontSize: typography.fontSize.xl, marginTop: spacing.lg },
  emptyText: { color: colors.textMuted, fontSize: typography.fontSize.md, marginTop: spacing.xs },
  keypadContainer: { flex: 1, alignItems: 'center', paddingTop: spacing.xl },
  keypadDisplay: { marginBottom: spacing.xl },
  keypadNumber: { color: colors.text, fontSize: 32, fontWeight: 'bold' },
  keypad: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', width: 280 },
  keypadKey: {
    width: 80, height: 80, margin: 8, borderRadius: 40,
    backgroundColor: colors.surface, justifyContent: 'center', alignItems: 'center',
  },
  keypadKeyText: { color: colors.text, fontSize: 28, fontWeight: '500' },
  callButton: { marginTop: spacing.xl, borderRadius: 40, overflow: 'hidden' },
  callButtonGradient: { width: 72, height: 72, justifyContent: 'center', alignItems: 'center' },
});
