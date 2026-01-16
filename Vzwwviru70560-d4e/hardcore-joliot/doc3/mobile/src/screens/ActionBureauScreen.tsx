/**
 * CHE·NU™ — Mobile Action Bureau Screen
 */

import React, { useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NavContext } from '../context/NavContext';
import { colors } from '../styles/colors';

export function ActionBureauScreen() {
  const navigation = useNavigation();
  const { state, send } = useContext(NavContext);
  const ctx = state.context;
  const { selection, data, contextSummary } = ctx;

  const keyIS = selection.identityId && selection.sphereId
    ? `${selection.identityId}:${selection.sphereId}`
    : null;

  const workspaces = keyIS ? data.workspacesByIdentitySphere[keyIS] ?? [] : [];
  const pinnedWorkspaces = workspaces.filter((w) => w.pinned);
  const recentWorkspaces = workspaces
    .filter((w) => !w.pinned && w.lastOpenedAt)
    .sort((a, b) => (b.lastOpenedAt ?? 0) - (a.lastOpenedAt ?? 0))
    .slice(0, 5);

  const handleOpenWorkspace = (id: string) => {
    send({ type: 'OPEN_WORKSPACE', workspaceId: id });
    navigation.navigate('Workspace' as never);
  };

  const handleChangeContext = () => {
    send({ type: 'CHANGE_CONTEXT' });
    navigation.navigate('ContextBureau' as never);
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.subtitle}>Que faire maintenant?</Text>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Actions rapides</Text>
        <View style={styles.quickActionsGrid}>
          <TouchableOpacity style={styles.quickActionBtn} onPress={() => handleOpenWorkspace('new')}>
            <Text style={styles.quickActionEmoji}>📝</Text>
            <Text style={styles.quickActionLabel}>Note</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.quickActionBtn}>
            <Text style={styles.quickActionEmoji}>✅</Text>
            <Text style={styles.quickActionLabel}>Tâche</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.quickActionBtn}>
            <Text style={styles.quickActionEmoji}>📹</Text>
            <Text style={styles.quickActionLabel}>Réunion</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.quickActionBtn}>
            <Text style={styles.quickActionEmoji}>🤖</Text>
            <Text style={styles.quickActionLabel}>Agent</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Pinned Workspaces */}
      {pinnedWorkspaces.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>📌 Workspaces épinglés</Text>
          {pinnedWorkspaces.map((ws) => (
            <TouchableOpacity
              key={ws.id}
              style={styles.workspaceCard}
              onPress={() => handleOpenWorkspace(ws.id)}
            >
              <Text style={styles.wsIcon}>🔧</Text>
              <View style={styles.wsInfo}>
                <Text style={styles.wsName}>{ws.name}</Text>
                <Text style={styles.wsType}>{ws.type}</Text>
              </View>
              <Text style={styles.wsArrow}>→</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      {/* Recent Workspaces */}
      {recentWorkspaces.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🕐 Récents</Text>
          {recentWorkspaces.map((ws) => (
            <TouchableOpacity
              key={ws.id}
              style={styles.workspaceCard}
              onPress={() => handleOpenWorkspace(ws.id)}
            >
              <Text style={styles.wsIcon}>📄</Text>
              <View style={styles.wsInfo}>
                <Text style={styles.wsName}>{ws.name}</Text>
                <Text style={styles.wsMeta}>
                  {ws.lastOpenedAt
                    ? new Date(ws.lastOpenedAt).toLocaleDateString('fr-FR')
                    : ''}
                </Text>
              </View>
              <Text style={styles.wsArrow}>→</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      {/* Nova Suggestion */}
      <View style={styles.novaSection}>
        <Text style={styles.sectionTitle}>💡 Suggestion Nova</Text>
        <View style={styles.novaSuggestion}>
          <Text style={styles.novaAvatar}>✦</Text>
          <Text style={styles.novaText}>
            "Vous avez {contextSummary.urgentTasks} tâches urgentes. Commencer par là?"
          </Text>
        </View>
      </View>

      {/* Footer */}
      <TouchableOpacity style={styles.changeContextBtn} onPress={handleChangeContext}>
        <Text style={styles.changeContextText}>← Changer de contexte</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bgPrimary,
    padding: 16,
  },
  subtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 24,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 13,
    color: colors.textSecondary,
    marginBottom: 12,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    gap: 8,
  },
  quickActionBtn: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
    backgroundColor: colors.bgSurface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
  },
  quickActionEmoji: {
    fontSize: 24,
    marginBottom: 4,
  },
  quickActionLabel: {
    fontSize: 11,
    color: colors.textSecondary,
  },
  workspaceCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: colors.bgSurface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: 8,
  },
  wsIcon: {
    fontSize: 20,
    marginRight: 12,
  },
  wsInfo: {
    flex: 1,
  },
  wsName: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  wsType: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  wsMeta: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  wsArrow: {
    color: colors.textMuted,
    fontSize: 16,
  },
  novaSection: {
    backgroundColor: colors.bgSurface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: 24,
  },
  novaSuggestion: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  novaAvatar: {
    fontSize: 18,
    color: colors.cenoteTurquoise,
    marginRight: 8,
  },
  novaText: {
    flex: 1,
    fontSize: 14,
    color: colors.textSecondary,
    fontStyle: 'italic',
  },
  changeContextBtn: {
    alignItems: 'center',
    padding: 12,
    marginBottom: 32,
  },
  changeContextText: {
    color: colors.textSecondary,
    fontSize: 14,
  },
});
