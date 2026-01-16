/**
 * CHENU - Mobile App (React Native)
 * ==================================
 * Application mobile pour iOS et Android
 */

// ============================================
// App.tsx - Point d'entrée principal
// ============================================

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';

// Screens
import HomeScreen from './screens/HomeScreen';
import ChatScreen from './screens/ChatScreen';
import TasksScreen from './screens/TasksScreen';
import AgentsScreen from './screens/AgentsScreen';
import SettingsScreen from './screens/SettingsScreen';
import LoginScreen from './screens/LoginScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;
          switch (route.name) {
            case 'Home': iconName = focused ? 'home' : 'home-outline'; break;
            case 'Chat': iconName = focused ? 'chatbubbles' : 'chatbubbles-outline'; break;
            case 'Tasks': iconName = focused ? 'list' : 'list-outline'; break;
            case 'Agents': iconName = focused ? 'people' : 'people-outline'; break;
            case 'Settings': iconName = focused ? 'settings' : 'settings-outline'; break;
            default: iconName = 'ellipse';
          }
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#8B5CF6',
        tabBarInactiveTintColor: '#6B7280',
        tabBarStyle: { backgroundColor: '#1F2937', borderTopColor: '#374151' },
        headerStyle: { backgroundColor: '#1F2937' },
        headerTintColor: '#FFFFFF',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: 'Accueil' }} />
      <Tab.Screen name="Chat" component={ChatScreen} options={{ title: 'Chat' }} />
      <Tab.Screen name="Tasks" component={TasksScreen} options={{ title: 'Tâches' }} />
      <Tab.Screen name="Agents" component={AgentsScreen} options={{ title: 'Agents' }} />
      <Tab.Screen name="Settings" component={SettingsScreen} options={{ title: 'Paramètres' }} />
    </Tab.Navigator>
  );
}

function AppNavigator() {
  const { isAuthenticated } = useAuth();
  
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name="Main" component={MainTabs} />
      ) : (
        <Stack.Screen name="Login" component={LoginScreen} />
      )}
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar style="light" />
          <AppNavigator />
        </NavigationContainer>
      </AuthProvider>
    </ThemeProvider>
  );
}

// ============================================
// screens/HomeScreen.tsx
// ============================================

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useAPI } from '../hooks/useAPI';

interface Stats {
  activeTasks: number;
  completedToday: number;
  successRate: number;
  tokensUsed: number;
}

interface Activity {
  time: string;
  event: string;
  agent: string;
}

export default function HomeScreen() {
  const [stats, setStats] = useState<Stats>({ activeTasks: 12, completedToday: 47, successRate: 98, tokensUsed: 24000 });
  const [activities, setActivities] = useState<Activity[]>([
    { time: '14:32', event: '✅ Article blog terminé', agent: 'Copywriter' },
    { time: '14:28', event: '🚀 Campagne lancée', agent: 'Social Writer' },
    { time: '14:15', event: '📊 Rapport en cours', agent: 'Data Analyst' },
    { time: '14:02', event: '🎨 Visuels approuvés', agent: 'Designer' },
  ]);
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    // Fetch new data
    await new Promise(r => setTimeout(r, 1000));
    setRefreshing(false);
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#8B5CF6" />}
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Bonjour, Jo 👋</Text>
        <Text style={styles.subtitle}>Voici l'état de ton équipe</Text>
      </View>

      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <StatCard title="Tâches actives" value={stats.activeTasks} color={['#8B5CF6', '#7C3AED']} />
        <StatCard title="Complétées" value={stats.completedToday} color={['#3B82F6', '#2563EB']} />
        <StatCard title="Succès" value={`${stats.successRate}%`} color={['#10B981', '#059669']} />
        <StatCard title="Tokens" value={`${(stats.tokensUsed/1000).toFixed(1)}k`} color={['#F59E0B', '#D97706']} />
      </View>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Actions rapides</Text>
        <View style={styles.actionsRow}>
          <ActionButton icon="✍️" label="Contenu" />
          <ActionButton icon="📣" label="Marketing" />
          <ActionButton icon="📊" label="Analyse" />
          <ActionButton icon="🎬" label="Vidéo" />
        </View>
      </View>

      {/* Activity Feed */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Activité récente</Text>
        {activities.map((activity, idx) => (
          <View key={idx} style={styles.activityItem}>
            <Text style={styles.activityTime}>{activity.time}</Text>
            <View style={styles.activityContent}>
              <Text style={styles.activityEvent}>{activity.event}</Text>
              <Text style={styles.activityAgent}>{activity.agent}</Text>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const StatCard = ({ title, value, color }: { title: string; value: string | number; color: string[] }) => (
  <LinearGradient colors={color} style={styles.statCard}>
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statTitle}>{title}</Text>
  </LinearGradient>
);

const ActionButton = ({ icon, label }: { icon: string; label: string }) => (
  <TouchableOpacity style={styles.actionButton}>
    <Text style={styles.actionIcon}>{icon}</Text>
    <Text style={styles.actionLabel}>{label}</Text>
  </TouchableOpacity>
);

// ============================================
// screens/ChatScreen.tsx
// ============================================

import React, { useState, useRef } from 'react';
import { View, Text, TextInput, FlatList, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'assistant', content: 'Bonjour ! Je suis CHENU. Comment puis-je t\'aider ?', timestamp: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate API call
    await new Promise(r => setTimeout(r, 1500));

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: `🧠 Analyse de votre demande...\n\n📋 Tâche créée: "${userMessage.content.slice(0, 50)}"\n👤 Agent assigné: Creative Director\n⚡ Priorité: Medium\n\n✅ Le workflow a été lancé !`,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const renderMessage = ({ item }: { item: Message }) => (
    <View style={[styles.messageContainer, item.role === 'user' ? styles.userMessage : styles.assistantMessage]}>
      <Text style={styles.messageText}>{item.content}</Text>
    </View>
  );

  return (
    <KeyboardAvoidingView style={styles.chatContainer} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.messagesList}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
      />
      
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          value={input}
          onChangeText={setInput}
          placeholder="Demande quelque chose à CHENU..."
          placeholderTextColor="#6B7280"
          multiline
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage} disabled={isLoading}>
          <Ionicons name={isLoading ? "hourglass" : "send"} size={24} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

// ============================================
// screens/TasksScreen.tsx
// ============================================

import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity } from 'react-native';

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed';
  agent: string;
  priority: 'low' | 'medium' | 'high';
}

export default function TasksScreen() {
  const [tasks] = useState<Task[]>([
    { id: '1', title: 'Article blog IA', status: 'completed', agent: 'Copywriter', priority: 'high' },
    { id: '2', title: 'Campagne LinkedIn', status: 'in_progress', agent: 'Social Writer', priority: 'medium' },
    { id: '3', title: 'Analyse Q4', status: 'in_progress', agent: 'Data Analyst', priority: 'high' },
    { id: '4', title: 'Newsletter', status: 'pending', agent: 'Email Writer', priority: 'low' },
    { id: '5', title: 'Vidéo produit', status: 'pending', agent: 'Video Editor', priority: 'medium' },
  ]);
  const [filter, setFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all');

  const filteredTasks = tasks.filter(t => filter === 'all' || t.status === filter);

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'completed': return '#10B981';
      case 'in_progress': return '#3B82F6';
      default: return '#6B7280';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch(priority) {
      case 'high': return '#EF4444';
      case 'medium': return '#F59E0B';
      default: return '#6B7280';
    }
  };

  return (
    <View style={styles.container}>
      {/* Filters */}
      <View style={styles.filterRow}>
        {['all', 'pending', 'in_progress', 'completed'].map(f => (
          <TouchableOpacity 
            key={f} 
            style={[styles.filterButton, filter === f && styles.filterActive]}
            onPress={() => setFilter(f as any)}
          >
            <Text style={[styles.filterText, filter === f && styles.filterTextActive]}>
              {f === 'all' ? 'Tous' : f === 'pending' ? 'En attente' : f === 'in_progress' ? 'En cours' : 'Terminés'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Tasks List */}
      <FlatList
        data={filteredTasks}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.taskCard}>
            <View style={styles.taskHeader}>
              <Text style={styles.taskTitle}>{item.title}</Text>
              <View style={[styles.priorityBadge, { backgroundColor: getPriorityColor(item.priority) }]}>
                <Text style={styles.priorityText}>{item.priority}</Text>
              </View>
            </View>
            <View style={styles.taskFooter}>
              <Text style={styles.taskAgent}>👤 {item.agent}</Text>
              <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
                <Text style={styles.statusText}>
                  {item.status === 'completed' ? '✓' : item.status === 'in_progress' ? '⏳' : '○'}
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

// ============================================
// screens/AgentsScreen.tsx  
// ============================================

import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Modal } from 'react-native';

interface Agent {
  id: string;
  name: string;
  icon: string;
  level: 'L1' | 'L2' | 'L3';
  department: string;
  status: 'active' | 'busy' | 'idle';
  activeTasks: number;
}

export default function AgentsScreen() {
  const [agents] = useState<Agent[]>([
    { id: '1', name: 'Creative Director', icon: '🎬', level: 'L1', department: 'Création', status: 'active', activeTasks: 3 },
    { id: '2', name: 'Copywriter', icon: '✍️', level: 'L3', department: 'Contenu', status: 'active', activeTasks: 5 },
    { id: '3', name: 'Graphic Designer', icon: '🎨', level: 'L3', department: 'Design', status: 'active', activeTasks: 2 },
    { id: '4', name: 'Data Analyst', icon: '📊', level: 'L3', department: 'Data', status: 'busy', activeTasks: 4 },
    { id: '5', name: 'Social Writer', icon: '📱', level: 'L3', department: 'Marketing', status: 'active', activeTasks: 1 },
    { id: '6', name: 'SEO Specialist', icon: '🔍', level: 'L3', department: 'Marketing', status: 'idle', activeTasks: 0 },
  ]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'active': return '#10B981';
      case 'busy': return '#F59E0B';
      default: return '#6B7280';
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={agents}
        numColumns={2}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.agentCard} onPress={() => setSelectedAgent(item)}>
            <Text style={styles.agentIcon}>{item.icon}</Text>
            <Text style={styles.agentName}>{item.name}</Text>
            <View style={styles.agentMeta}>
              <View style={[styles.levelBadge, { backgroundColor: item.level === 'L1' ? '#8B5CF6' : item.level === 'L2' ? '#3B82F6' : '#6B7280' }]}>
                <Text style={styles.levelText}>{item.level}</Text>
              </View>
              <View style={[styles.statusDot, { backgroundColor: getStatusColor(item.status) }]} />
            </View>
            <Text style={styles.agentTasks}>{item.activeTasks} tâches</Text>
          </TouchableOpacity>
        )}
      />

      {/* Agent Detail Modal */}
      <Modal visible={!!selectedAgent} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            {selectedAgent && (
              <>
                <Text style={styles.modalIcon}>{selectedAgent.icon}</Text>
                <Text style={styles.modalTitle}>{selectedAgent.name}</Text>
                <Text style={styles.modalSubtitle}>{selectedAgent.department} • {selectedAgent.level}</Text>
                <View style={styles.modalStats}>
                  <View style={styles.modalStat}>
                    <Text style={styles.modalStatValue}>{selectedAgent.activeTasks}</Text>
                    <Text style={styles.modalStatLabel}>Tâches</Text>
                  </View>
                  <View style={styles.modalStat}>
                    <Text style={[styles.modalStatValue, { color: getStatusColor(selectedAgent.status) }]}>●</Text>
                    <Text style={styles.modalStatLabel}>{selectedAgent.status}</Text>
                  </View>
                </View>
                <TouchableOpacity style={styles.modalClose} onPress={() => setSelectedAgent(null)}>
                  <Text style={styles.modalCloseText}>Fermer</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ============================================
// styles.ts
// ============================================

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#111827' },
  header: { padding: 20, paddingTop: 10 },
  greeting: { fontSize: 28, fontWeight: 'bold', color: '#FFFFFF' },
  subtitle: { fontSize: 16, color: '#9CA3AF', marginTop: 4 },
  
  // Stats
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', padding: 10 },
  statCard: { width: '46%', margin: '2%', padding: 16, borderRadius: 16 },
  statValue: { fontSize: 28, fontWeight: 'bold', color: '#FFFFFF' },
  statTitle: { fontSize: 12, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  
  // Sections
  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '600', color: '#FFFFFF', marginBottom: 12 },
  
  // Actions
  actionsRow: { flexDirection: 'row', justifyContent: 'space-between' },
  actionButton: { backgroundColor: '#374151', padding: 16, borderRadius: 12, alignItems: 'center', width: '23%' },
  actionIcon: { fontSize: 24, marginBottom: 4 },
  actionLabel: { fontSize: 12, color: '#9CA3AF' },
  
  // Activity
  activityItem: { flexDirection: 'row', marginBottom: 12 },
  activityTime: { width: 50, color: '#6B7280', fontSize: 12 },
  activityContent: { flex: 1 },
  activityEvent: { color: '#FFFFFF', fontSize: 14 },
  activityAgent: { color: '#6B7280', fontSize: 12 },
  
  // Chat
  chatContainer: { flex: 1, backgroundColor: '#111827' },
  messagesList: { padding: 16 },
  messageContainer: { maxWidth: '80%', padding: 12, borderRadius: 16, marginBottom: 8 },
  userMessage: { alignSelf: 'flex-end', backgroundColor: '#8B5CF6' },
  assistantMessage: { alignSelf: 'flex-start', backgroundColor: '#374151' },
  messageText: { color: '#FFFFFF', fontSize: 15 },
  inputContainer: { flexDirection: 'row', padding: 12, backgroundColor: '#1F2937' },
  textInput: { flex: 1, backgroundColor: '#374151', borderRadius: 24, paddingHorizontal: 16, paddingVertical: 10, color: '#FFFFFF', marginRight: 8 },
  sendButton: { backgroundColor: '#8B5CF6', width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center' },
  
  // Tasks
  filterRow: { flexDirection: 'row', padding: 12 },
  filterButton: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 20, marginRight: 8, backgroundColor: '#374151' },
  filterActive: { backgroundColor: '#8B5CF6' },
  filterText: { color: '#9CA3AF', fontSize: 13 },
  filterTextActive: { color: '#FFFFFF' },
  taskCard: { backgroundColor: '#1F2937', margin: 8, padding: 16, borderRadius: 12 },
  taskHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  taskTitle: { color: '#FFFFFF', fontSize: 16, fontWeight: '500', flex: 1 },
  priorityBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  priorityText: { color: '#FFFFFF', fontSize: 10, fontWeight: '600' },
  taskFooter: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12 },
  taskAgent: { color: '#9CA3AF', fontSize: 13 },
  statusBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  statusText: { color: '#FFFFFF', fontSize: 12 },
  
  // Agents
  agentCard: { backgroundColor: '#1F2937', margin: 8, padding: 16, borderRadius: 12, width: '45%', alignItems: 'center' },
  agentIcon: { fontSize: 40, marginBottom: 8 },
  agentName: { color: '#FFFFFF', fontSize: 14, fontWeight: '500', textAlign: 'center' },
  agentMeta: { flexDirection: 'row', alignItems: 'center', marginTop: 8 },
  levelBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 4, marginRight: 8 },
  levelText: { color: '#FFFFFF', fontSize: 10, fontWeight: '600' },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  agentTasks: { color: '#9CA3AF', fontSize: 12, marginTop: 4 },
  
  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: '#1F2937', borderTopLeftRadius: 24, borderTopRightRadius: 24, padding: 24, alignItems: 'center' },
  modalIcon: { fontSize: 60, marginBottom: 12 },
  modalTitle: { fontSize: 24, fontWeight: 'bold', color: '#FFFFFF' },
  modalSubtitle: { fontSize: 14, color: '#9CA3AF', marginTop: 4 },
  modalStats: { flexDirection: 'row', marginTop: 24 },
  modalStat: { alignItems: 'center', marginHorizontal: 24 },
  modalStatValue: { fontSize: 28, fontWeight: 'bold', color: '#FFFFFF' },
  modalStatLabel: { fontSize: 12, color: '#9CA3AF', marginTop: 4 },
  modalClose: { backgroundColor: '#8B5CF6', paddingHorizontal: 32, paddingVertical: 12, borderRadius: 24, marginTop: 24 },
  modalCloseText: { color: '#FFFFFF', fontSize: 16, fontWeight: '600' },
});
