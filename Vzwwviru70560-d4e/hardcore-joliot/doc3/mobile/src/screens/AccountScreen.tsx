// CHE·NU Mobile - Account Screen
import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';
import { useAuthStore, useThreadsStore } from '../store';

export default function AccountScreen() {
  const navigation = useNavigation<any>();
  const { user, logout } = useAuthStore();
  const { threads } = useThreadsStore();

  const totalTokens = threads.reduce((sum, t) => sum + (t.execution?.actual_tokens || 0), 0);
  const completedThreads = threads.filter(t => t.status === 'completed').length;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Profile Header */}
      <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{user?.name?.charAt(0) || 'U'}</Text>
        </View>
        <Text style={styles.userName}>{user?.name || 'Utilisateur'}</Text>
        <Text style={styles.userEmail}>{user?.email}</Text>
        <View style={styles.roleBadge}>
          <Text style={styles.roleText}>{user?.role || 'user'}</Text>
        </View>
      </LinearGradient>

      {/* Stats */}
      <View style={styles.statsCard}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{threads.length}</Text>
          <Text style={styles.statLabel}>Threads</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{completedThreads}</Text>
          <Text style={styles.statLabel}>Complétés</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{(totalTokens / 1000).toFixed(1)}k</Text>
          <Text style={styles.statLabel}>Tokens</Text>
        </View>
      </View>

      {/* Menu */}
      <View style={styles.menu}>
        {[
          { icon: 'settings-outline', label: 'Paramètres', screen: 'Settings' },
          { icon: 'shield-checkmark-outline', label: 'Gouvernance', screen: null },
          { icon: 'card-outline', label: 'Budget & Tokens', screen: null },
          { icon: 'key-outline', label: 'BYOLLM (Mes clés API)', screen: null },
          { icon: 'help-circle-outline', label: 'Aide', screen: null },
        ].map((item, i) => (
          <TouchableOpacity 
            key={i} 
            style={styles.menuItem}
            onPress={() => item.screen && navigation.navigate(item.screen)}
          >
            <Ionicons name={item.icon as any} size={24} color={colors.text} />
            <Text style={styles.menuText}>{item.label}</Text>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        ))}
      </View>

      {/* Logout */}
      <TouchableOpacity style={styles.logoutButton} onPress={logout}>
        <Ionicons name="log-out-outline" size={24} color={colors.error} />
        <Text style={styles.logoutText}>Se déconnecter</Text>
      </TouchableOpacity>

      <Text style={styles.version}>CHE·NU Mobile v1.0.0</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { paddingBottom: spacing.xxl },
  header: { alignItems: 'center', paddingTop: spacing.xxl, paddingBottom: spacing.xxl, marginBottom: -spacing.lg },
  avatar: { width: 80, height: 80, borderRadius: 40, backgroundColor: 'rgba(255,255,255,0.2)', justifyContent: 'center', alignItems: 'center', marginBottom: spacing.md },
  avatarText: { color: colors.text, fontSize: 32, fontWeight: 'bold' },
  userName: { color: colors.text, fontSize: typography.fontSize.xxl, fontWeight: 'bold' },
  userEmail: { color: 'rgba(255,255,255,0.7)', fontSize: typography.fontSize.md, marginTop: spacing.xs },
  roleBadge: { backgroundColor: 'rgba(255,255,255,0.2)', paddingHorizontal: spacing.md, paddingVertical: spacing.xs, borderRadius: borderRadius.full, marginTop: spacing.md },
  roleText: { color: colors.text, fontSize: typography.fontSize.sm, textTransform: 'capitalize' },
  statsCard: {
    flexDirection: 'row', backgroundColor: colors.surface, marginHorizontal: spacing.lg,
    borderRadius: borderRadius.lg, padding: spacing.lg, ...shadows.md,
  },
  statItem: { flex: 1, alignItems: 'center' },
  statValue: { color: colors.text, fontSize: typography.fontSize.xxl, fontWeight: 'bold' },
  statLabel: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: spacing.xs },
  statDivider: { width: 1, backgroundColor: colors.border },
  menu: { backgroundColor: colors.surface, marginHorizontal: spacing.lg, marginTop: spacing.lg, borderRadius: borderRadius.lg },
  menuItem: { flexDirection: 'row', alignItems: 'center', padding: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border, gap: spacing.md },
  menuText: { flex: 1, color: colors.text, fontSize: typography.fontSize.md },
  logoutButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginHorizontal: spacing.lg, marginTop: spacing.lg, padding: spacing.md, backgroundColor: colors.surface, borderRadius: borderRadius.lg, gap: spacing.sm },
  logoutText: { color: colors.error, fontSize: typography.fontSize.md, fontWeight: '600' },
  version: { color: colors.textMuted, fontSize: typography.fontSize.sm, textAlign: 'center', marginTop: spacing.lg },
});
