// CHE·NU™ React Native Screens
// Mobile screens for all features

import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
  RefreshControl,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useTheme } from '../providers/ThemeProvider';
import { useAuth } from '../providers/AuthProvider';
import { useI18n } from '../providers/I18nProvider';

const { width } = Dimensions.get('window');

// ============================================================
// 8 SPHERES (FROZEN - Memory Prompt)
// ============================================================

const SPHERES = [
  { code: 'personal', name: 'Personal', icon: '🏠', color: '#4CAF50' },
  { code: 'business', name: 'Business', icon: '💼', color: '#2196F3' },
  { code: 'government', name: 'Government & Institutions', icon: '🏛️', color: '#9C27B0' },
  { code: 'studio', name: 'Creative Studio', icon: '🎨', color: '#FF5722' },
  { code: 'community', name: 'Community', icon: '👥', color: '#00BCD4' },
  { code: 'social', name: 'Social & Media', icon: '📱', color: '#E91E63' },
  { code: 'entertainment', name: 'Entertainment', icon: '🎬', color: '#FF9800' },
  { code: 'team', name: 'My Team', icon: '🤝', color: '#795548' },
] as const;

// 10 Bureau Sections (NON-NEGOTIABLE - Memory Prompt)
const BUREAU_SECTIONS = [
  { id: 1, name: 'Dashboard', icon: '📊' },
  { id: 2, name: 'Notes', icon: '📝' },
  { id: 3, name: 'Tasks', icon: '✅' },
  { id: 4, name: 'Projects', icon: '📁' },
  { id: 5, name: 'Threads', icon: '💬' },
  { id: 6, name: 'Meetings', icon: '📅' },
  { id: 7, name: 'Data', icon: '🗄️' },
  { id: 8, name: 'Agents', icon: '🤖' },
  { id: 9, name: 'Reports', icon: '📈' },
  { id: 10, name: 'Budget', icon: '💰' },
] as const;

// ============================================================
// DASHBOARD SCREEN
// ============================================================

export function DashboardScreen() {
  const { colors } = useTheme();
  const { user } = useAuth();
  const { t } = useI18n();
  const navigation = useNavigation();
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    // Refresh data
    await new Promise(resolve => setTimeout(resolve, 1000));
    setRefreshing(false);
  }, []);

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={[styles.greeting, { color: colors.text }]}>
            {t('common.welcome')}, {user?.name || 'User'}
          </Text>
          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
            {t('dashboard.subtitle')}
          </Text>
        </View>

        {/* Quick Access Spheres */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>
            {t('spheres.title')}
          </Text>
          <View style={styles.spheresGrid}>
            {SPHERES.map((sphere) => (
              <TouchableOpacity
                key={sphere.code}
                style={[styles.sphereCard, { backgroundColor: colors.surface }]}
                onPress={() => navigation.navigate('Bureau', { 
                  sphereCode: sphere.code,
                  sphereName: sphere.name 
                })}
              >
                <Text style={styles.sphereIcon}>{sphere.icon}</Text>
                <Text style={[styles.sphereName, { color: colors.text }]} numberOfLines={1}>
                  {sphere.name}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Token Budget Overview */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>
            {t('tokens.budget')}
          </Text>
          <View style={[styles.tokenCard, { backgroundColor: colors.surface }]}>
            <View style={styles.tokenRow}>
              <Text style={[styles.tokenLabel, { color: colors.textSecondary }]}>
                {t('tokens.allocated')}
              </Text>
              <Text style={[styles.tokenValue, { color: colors.text }]}>
                100,000
              </Text>
            </View>
            <View style={styles.tokenProgressBar}>
              <View style={[styles.tokenProgress, { width: '35%' }]} />
            </View>
            <View style={styles.tokenRow}>
              <Text style={[styles.tokenLabel, { color: colors.textSecondary }]}>
                {t('tokens.used')}: 35,000
              </Text>
              <Text style={[styles.tokenLabel, { color: colors.textSecondary }]}>
                {t('tokens.remaining')}: 65,000
              </Text>
            </View>
            {/* Memory Prompt: Token disclaimer */}
            <Text style={[styles.tokenDisclaimer, { color: colors.textSecondary }]}>
              ⚠️ {t('tokens.disclaimer')}
            </Text>
          </View>
        </View>

        {/* Recent Threads */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>
            {t('threads.recent')}
          </Text>
          {/* Thread list would go here */}
        </View>
      </ScrollView>

      {/* Nova FAB */}
      <TouchableOpacity
        style={styles.novaFab}
        onPress={() => navigation.navigate('Nova')}
      >
        <Text style={styles.novaFabIcon}>🌟</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

// ============================================================
// SPHERE SCREEN
// ============================================================

export function SphereScreen() {
  const { colors } = useTheme();
  const { t } = useI18n();
  const navigation = useNavigation();

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.header}>
        <Text style={[styles.screenTitle, { color: colors.text }]}>
          {t('spheres.title')}
        </Text>
        <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
          {t('spheres.description')}
        </Text>
      </View>

      <FlatList
        data={SPHERES}
        keyExtractor={(item) => item.code}
        numColumns={2}
        contentContainerStyle={styles.spheresList}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.sphereCardLarge, { backgroundColor: colors.surface }]}
            onPress={() => navigation.navigate('Bureau', {
              sphereCode: item.code,
              sphereName: item.name
            })}
          >
            <View style={[styles.sphereIconLarge, { backgroundColor: item.color + '20' }]}>
              <Text style={styles.sphereIconText}>{item.icon}</Text>
            </View>
            <Text style={[styles.sphereNameLarge, { color: colors.text }]}>
              {item.name}
            </Text>
            <Text style={[styles.sphereDescription, { color: colors.textSecondary }]}>
              {t(`spheres.${item.code}.description`)}
            </Text>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
}

// ============================================================
// BUREAU SCREEN
// ============================================================

export function BureauScreen({ route }) {
  const { sphereCode, sphereName } = route.params;
  const { colors } = useTheme();
  const { t } = useI18n();
  const [activeSection, setActiveSection] = useState(1);

  const sphere = SPHERES.find(s => s.code === sphereCode);

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Sphere Header */}
      <View style={[styles.bureauHeader, { backgroundColor: colors.surface }]}>
        <Text style={styles.bureauIcon}>{sphere?.icon}</Text>
        <Text style={[styles.bureauTitle, { color: colors.text }]}>
          {sphereName}
        </Text>
      </View>

      {/* Bureau Tabs - 10 Sections (NON-NEGOTIABLE) */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.bureauTabs}
      >
        {BUREAU_SECTIONS.map((section) => (
          <TouchableOpacity
            key={section.id}
            style={[
              styles.bureauTab,
              activeSection === section.id && styles.bureauTabActive,
              { backgroundColor: activeSection === section.id ? colors.primary : colors.surface }
            ]}
            onPress={() => setActiveSection(section.id)}
          >
            <Text style={styles.bureauTabIcon}>{section.icon}</Text>
            <Text style={[
              styles.bureauTabText,
              { color: activeSection === section.id ? '#fff' : colors.text }
            ]}>
              {section.name}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Section Content */}
      <View style={styles.bureauContent}>
        <Text style={[styles.sectionContentTitle, { color: colors.text }]}>
          {BUREAU_SECTIONS.find(s => s.id === activeSection)?.name}
        </Text>
        {/* Section-specific content would go here */}
      </View>
    </SafeAreaView>
  );
}

// ============================================================
// THREAD SCREEN
// ============================================================

export function ThreadScreen({ route }) {
  const { threadId, threadTitle } = route.params || {};
  const { colors } = useTheme();
  const { t } = useI18n();
  const [message, setMessage] = useState('');
  const [encodingEnabled, setEncodingEnabled] = useState(true);

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Thread Header */}
      <View style={[styles.threadHeader, { backgroundColor: colors.surface }]}>
        <View style={styles.threadInfo}>
          <Text style={[styles.threadTitle, { color: colors.text }]}>
            {threadTitle || 'New Thread'}
          </Text>
          <View style={styles.chenuBadge}>
            <Text style={styles.chenuBadgeText}>.chenu</Text>
          </View>
        </View>
        
        {/* Token Budget */}
        <View style={styles.threadTokens}>
          <Text style={[styles.tokenSmall, { color: colors.textSecondary }]}>
            5,000 / 10,000 tokens
          </Text>
        </View>
      </View>

      {/* Messages */}
      <ScrollView style={styles.messagesContainer}>
        {/* Messages would render here */}
      </ScrollView>

      {/* Input Area */}
      <View style={[styles.inputArea, { backgroundColor: colors.surface }]}>
        {/* Encoding Toggle */}
        <TouchableOpacity
          style={[
            styles.encodingToggle,
            encodingEnabled && styles.encodingToggleActive
          ]}
          onPress={() => setEncodingEnabled(!encodingEnabled)}
        >
          <Text style={styles.encodingToggleText}>
            {encodingEnabled ? '🔐' : '🔓'}
          </Text>
        </TouchableOpacity>

        <TextInput
          style={[styles.messageInput, { color: colors.text }]}
          placeholder={t('threads.typeMessage')}
          placeholderTextColor={colors.textSecondary}
          value={message}
          onChangeText={setMessage}
          multiline
        />

        <TouchableOpacity style={styles.sendButton}>
          <Text style={styles.sendButtonText}>➤</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// ============================================================
// NOVA SCREEN
// ============================================================

export function NovaScreen() {
  const { colors } = useTheme();
  const { t } = useI18n();
  const [query, setQuery] = useState('');

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Nova Header */}
      <View style={styles.novaHeader}>
        <View style={styles.novaAvatar}>
          <Text style={styles.novaAvatarEmoji}>🌟</Text>
        </View>
        <Text style={[styles.novaTitle, { color: colors.text }]}>Nova</Text>
        {/* Memory Prompt: Nova is SYSTEM intelligence */}
        <Text style={[styles.novaSubtitle, { color: colors.textSecondary }]}>
          {t('nova.systemIntelligence')}
        </Text>
      </View>

      {/* Nova Insights */}
      <ScrollView style={styles.novaContent}>
        <View style={[styles.insightCard, { backgroundColor: colors.surface }]}>
          <Text style={styles.insightIcon}>💡</Text>
          <Text style={[styles.insightTitle, { color: colors.text }]}>
            {t('nova.insights')}
          </Text>
          <Text style={[styles.insightText, { color: colors.textSecondary }]}>
            Based on your activity, you've been productive in the Business sphere this week.
          </Text>
        </View>

        <View style={[styles.insightCard, { backgroundColor: colors.surface }]}>
          <Text style={styles.insightIcon}>✨</Text>
          <Text style={[styles.insightTitle, { color: colors.text }]}>
            {t('nova.suggestions')}
          </Text>
          <Text style={[styles.insightText, { color: colors.textSecondary }]}>
            Consider enabling encoding on your marketing thread to save tokens.
          </Text>
        </View>
      </ScrollView>

      {/* Nova Input */}
      <View style={[styles.novaInputArea, { backgroundColor: colors.surface }]}>
        <TextInput
          style={[styles.novaInput, { color: colors.text }]}
          placeholder={t('nova.askNova')}
          placeholderTextColor={colors.textSecondary}
          value={query}
          onChangeText={setQuery}
        />
        <TouchableOpacity style={styles.novaAskButton}>
          <Text style={styles.novaAskButtonText}>Ask</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// ============================================================
// SETTINGS SCREEN
// ============================================================

export function SettingsScreen() {
  const { colors, isDark, toggleTheme } = useTheme();
  const { t, language, setLanguage } = useI18n();
  const { logout } = useAuth();

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView>
        <View style={styles.settingsSection}>
          <Text style={[styles.settingsSectionTitle, { color: colors.textSecondary }]}>
            {t('settings.appearance')}
          </Text>
          
          <TouchableOpacity
            style={[styles.settingsItem, { backgroundColor: colors.surface }]}
            onPress={toggleTheme}
          >
            <Text style={[styles.settingsItemText, { color: colors.text }]}>
              {t('settings.theme')}
            </Text>
            <Text style={[styles.settingsItemValue, { color: colors.textSecondary }]}>
              {isDark ? t('settings.dark') : t('settings.light')}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.settingsItem, { backgroundColor: colors.surface }]}
          >
            <Text style={[styles.settingsItemText, { color: colors.text }]}>
              {t('settings.language')}
            </Text>
            <Text style={[styles.settingsItemValue, { color: colors.textSecondary }]}>
              {language.toUpperCase()}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.settingsSection}>
          <Text style={[styles.settingsSectionTitle, { color: colors.textSecondary }]}>
            {t('settings.governance')}
          </Text>
          
          <TouchableOpacity style={[styles.settingsItem, { backgroundColor: colors.surface }]}>
            <Text style={[styles.settingsItemText, { color: colors.text }]}>
              {t('governance.laws')}
            </Text>
            <Text style={styles.settingsItemArrow}>→</Text>
          </TouchableOpacity>

          <TouchableOpacity style={[styles.settingsItem, { backgroundColor: colors.surface }]}>
            <Text style={[styles.settingsItemText, { color: colors.text }]}>
              {t('governance.audit')}
            </Text>
            <Text style={styles.settingsItemArrow}>→</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          style={[styles.logoutButton, { backgroundColor: colors.error }]}
          onPress={logout}
        >
          <Text style={styles.logoutButtonText}>{t('common.logout')}</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

// ============================================================
// STYLES
// ============================================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 14,
    marginTop: 4,
  },
  screenTitle: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
  },
  
  // Spheres Grid
  spheresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  sphereCard: {
    width: (width - 60) / 4,
    padding: 12,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
  sphereIcon: {
    fontSize: 24,
    marginBottom: 4,
  },
  sphereName: {
    fontSize: 10,
    textAlign: 'center',
  },
  
  // Spheres List
  spheresList: {
    padding: 16,
  },
  sphereCardLarge: {
    flex: 1,
    margin: 8,
    padding: 16,
    borderRadius: 16,
    alignItems: 'center',
  },
  sphereIconLarge: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  sphereIconText: {
    fontSize: 28,
  },
  sphereNameLarge: {
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
  sphereDescription: {
    fontSize: 12,
    textAlign: 'center',
    marginTop: 4,
  },

  // Token Card
  tokenCard: {
    padding: 16,
    borderRadius: 12,
  },
  tokenRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  tokenLabel: {
    fontSize: 12,
  },
  tokenValue: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  tokenProgressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginVertical: 8,
  },
  tokenProgress: {
    height: '100%',
    backgroundColor: '#4CAF50',
    borderRadius: 4,
  },
  tokenDisclaimer: {
    fontSize: 10,
    marginTop: 8,
    fontStyle: 'italic',
  },

  // Bureau
  bureauHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  bureauIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  bureauTitle: {
    fontSize: 20,
    fontWeight: '600',
  },
  bureauTabs: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  bureauTab: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    marginHorizontal: 4,
  },
  bureauTabActive: {},
  bureauTabIcon: {
    fontSize: 16,
    marginRight: 6,
  },
  bureauTabText: {
    fontSize: 13,
    fontWeight: '500',
  },
  bureauContent: {
    flex: 1,
    padding: 20,
  },
  sectionContentTitle: {
    fontSize: 18,
    fontWeight: '600',
  },

  // Thread
  threadHeader: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  threadInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  threadTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  chenuBadge: {
    backgroundColor: '#D8B26A',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
    marginLeft: 8,
  },
  chenuBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '600',
  },
  threadTokens: {
    marginTop: 8,
  },
  tokenSmall: {
    fontSize: 12,
  },
  messagesContainer: {
    flex: 1,
  },
  inputArea: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  encodingToggle: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: '#e0e0e0',
  },
  encodingToggleActive: {
    backgroundColor: '#4CAF50',
  },
  encodingToggleText: {
    fontSize: 16,
  },
  messageInput: {
    flex: 1,
    marginHorizontal: 12,
    fontSize: 16,
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#D8B26A',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonText: {
    color: '#fff',
    fontSize: 18,
  },

  // Nova
  novaHeader: {
    alignItems: 'center',
    padding: 24,
  },
  novaAvatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#D8B26A',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  novaAvatarEmoji: {
    fontSize: 40,
  },
  novaTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  novaSubtitle: {
    fontSize: 14,
    marginTop: 4,
  },
  novaContent: {
    flex: 1,
    padding: 16,
  },
  insightCard: {
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  insightIcon: {
    fontSize: 20,
    marginBottom: 8,
  },
  insightTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  insightText: {
    fontSize: 14,
    lineHeight: 20,
  },
  novaInputArea: {
    flexDirection: 'row',
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  novaInput: {
    flex: 1,
    fontSize: 16,
    marginRight: 12,
  },
  novaAskButton: {
    backgroundColor: '#D8B26A',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  novaAskButtonText: {
    color: '#fff',
    fontWeight: '600',
  },

  // Nova FAB
  novaFab: {
    position: 'absolute',
    bottom: 90,
    right: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#D8B26A',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  novaFabIcon: {
    fontSize: 28,
  },

  // Settings
  settingsSection: {
    marginBottom: 24,
  },
  settingsSectionTitle: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
    paddingHorizontal: 16,
    marginBottom: 8,
  },
  settingsItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  settingsItemText: {
    fontSize: 16,
  },
  settingsItemValue: {
    fontSize: 14,
  },
  settingsItemArrow: {
    fontSize: 16,
    color: '#999',
  },
  logoutButton: {
    margin: 16,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default {
  DashboardScreen,
  SphereScreen,
  BureauScreen,
  ThreadScreen,
  NovaScreen,
  SettingsScreen,
};
