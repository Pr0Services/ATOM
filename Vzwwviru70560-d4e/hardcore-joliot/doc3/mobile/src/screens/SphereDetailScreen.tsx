// CHE·NU Mobile - Sphere Detail Screen
import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';
import { useSpheresStore, useAgentsStore } from '../store';

export default function SphereDetailScreen() {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();
  const { sphereId } = route.params;
  const { spheres } = useSpheresStore();
  const { allAgents } = useAgentsStore();
  
  const sphere = spheres.find(s => s.id === sphereId);
  const sphereAgents = allAgents.filter(a => a.sphere === sphere?.name);

  if (!sphere) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Sphère non trouvée</Text>
      </View>
    );
  }

  // Set header title
  React.useLayoutEffect(() => {
    navigation.setOptions({ title: sphere.name });
  }, [navigation, sphere.name]);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Sphere Header */}
      <LinearGradient colors={[sphere.color, sphere.color + '80']} style={styles.header}>
        <View style={styles.headerIcon}>
          <Ionicons name={sphere.icon as any} size={48} color={colors.text} />
        </View>
        <Text style={styles.headerTitle}>{sphere.name}</Text>
        <Text style={styles.headerDesc}>{sphere.description}</Text>
        
        {/* Quick Stats */}
        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{sphere.agent_count || sphereAgents.length}</Text>
            <Text style={styles.statLabel}>Agents</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{(sphere.budget.remaining / 1000).toFixed(0)}k</Text>
            <Text style={styles.statLabel}>Tokens</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{sphere.is_active ? 'Actif' : 'Inactif'}</Text>
            <Text style={styles.statLabel}>Status</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Chat with Chef */}
      <TouchableOpacity 
        style={styles.chefCard}
        onPress={() => navigation.navigate('Conversation', { 
          agentId: `chef_${sphere.id}`, 
          agentName: `Chef ${sphere.name}` 
        })}
      >
        <View style={[styles.chefAvatar, { backgroundColor: sphere.color }]}>
          <Ionicons name="person" size={24} color={colors.text} />
        </View>
        <View style={styles.chefInfo}>
          <Text style={styles.chefName}>Chef {sphere.name}</Text>
          <Text style={styles.chefRole}>Coordonnateur de sphère</Text>
        </View>
        <View style={styles.chefActions}>
          <TouchableOpacity style={styles.chefAction}>
            <Ionicons name="chatbubble" size={20} color={colors.primary} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.chefAction}>
            <Ionicons name="call" size={20} color={colors.success} />
          </TouchableOpacity>
        </View>
      </TouchableOpacity>

      {/* Agents */}
      <Text style={styles.sectionTitle}>Agents ({sphereAgents.length})</Text>
      {sphereAgents.length > 0 ? (
        sphereAgents.map(agent => (
          <TouchableOpacity 
            key={agent.id}
            style={styles.agentCard}
            onPress={() => navigation.navigate('Conversation', { 
              agentId: agent.id, 
              agentName: agent.name 
            })}
          >
            <View style={[styles.agentAvatar, { backgroundColor: agent.color + '30' }]}>
              <Ionicons name={(agent.icon || 'person') as any} size={24} color={agent.color} />
            </View>
            <View style={styles.agentInfo}>
              <Text style={styles.agentName}>{agent.name}</Text>
              <Text style={styles.agentRole}>{agent.role} • {agent.level}</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        ))
      ) : (
        <View style={styles.emptyState}>
          <Ionicons name="people-outline" size={48} color={colors.textMuted} />
          <Text style={styles.emptyText}>Aucun agent dans cette sphère</Text>
        </View>
      )}

      {/* Recent Activity */}
      <Text style={styles.sectionTitle}>Activité Récente</Text>
      <View style={styles.activityCard}>
        <View style={styles.activityItem}>
          <View style={styles.activityDot} />
          <View style={styles.activityInfo}>
            <Text style={styles.activityText}>Thread complété</Text>
            <Text style={styles.activityTime}>Il y a 2h</Text>
          </View>
        </View>
        <View style={styles.activityItem}>
          <View style={[styles.activityDot, { backgroundColor: colors.warning }]} />
          <View style={styles.activityInfo}>
            <Text style={styles.activityText}>Approbation en attente</Text>
            <Text style={styles.activityTime}>Il y a 5h</Text>
          </View>
        </View>
      </View>

      {/* Budget */}
      <Text style={styles.sectionTitle}>Budget Tokens</Text>
      <View style={styles.budgetCard}>
        <View style={styles.budgetHeader}>
          <Text style={styles.budgetLabel}>Utilisé</Text>
          <Text style={styles.budgetValue}>
            {((sphere.budget.total - sphere.budget.remaining) / 1000).toFixed(1)}k / {(sphere.budget.total / 1000).toFixed(0)}k
          </Text>
        </View>
        <View style={styles.budgetBar}>
          <View 
            style={[
              styles.budgetFill, 
              { 
                width: `${((sphere.budget.total - sphere.budget.remaining) / sphere.budget.total) * 100}%`,
                backgroundColor: sphere.color,
              }
            ]} 
          />
        </View>
        <Text style={styles.budgetRemaining}>
          {(sphere.budget.remaining / 1000).toFixed(1)}k tokens restants
        </Text>
      </View>

      <View style={styles.bottomSpace} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: {},
  errorText: { color: colors.error, textAlign: 'center', marginTop: spacing.xxl },
  header: { padding: spacing.xl, alignItems: 'center' },
  headerIcon: { width: 88, height: 88, borderRadius: 24, backgroundColor: 'rgba(255,255,255,0.2)', justifyContent: 'center', alignItems: 'center', marginBottom: spacing.md },
  headerTitle: { color: colors.text, fontSize: 28, fontWeight: 'bold' },
  headerDesc: { color: 'rgba(255,255,255,0.8)', fontSize: typography.fontSize.md, textAlign: 'center', marginTop: spacing.xs },
  statsRow: { flexDirection: 'row', marginTop: spacing.lg, gap: spacing.xl },
  statItem: { alignItems: 'center' },
  statValue: { color: colors.text, fontSize: 20, fontWeight: 'bold' },
  statLabel: { color: 'rgba(255,255,255,0.7)', fontSize: typography.fontSize.sm, marginTop: 2 },
  chefCard: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface,
    marginHorizontal: spacing.lg, marginTop: -spacing.lg, borderRadius: borderRadius.lg,
    padding: spacing.md, ...shadows.md,
  },
  chefAvatar: { width: 52, height: 52, borderRadius: 26, justifyContent: 'center', alignItems: 'center' },
  chefInfo: { flex: 1, marginLeft: spacing.md },
  chefName: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold' },
  chefRole: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  chefActions: { flexDirection: 'row', gap: spacing.sm },
  chefAction: { padding: spacing.sm, backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.full },
  sectionTitle: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold', marginHorizontal: spacing.lg, marginTop: spacing.xl, marginBottom: spacing.md },
  agentCard: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface,
    marginHorizontal: spacing.lg, marginBottom: spacing.sm, borderRadius: borderRadius.lg,
    padding: spacing.md, ...shadows.sm,
  },
  agentAvatar: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  agentInfo: { flex: 1, marginLeft: spacing.md },
  agentName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '600' },
  agentRole: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  emptyState: { alignItems: 'center', paddingVertical: spacing.xl },
  emptyText: { color: colors.textMuted, fontSize: typography.fontSize.md, marginTop: spacing.md },
  activityCard: { backgroundColor: colors.surface, marginHorizontal: spacing.lg, borderRadius: borderRadius.lg, padding: spacing.md },
  activityItem: { flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.sm },
  activityDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.success, marginRight: spacing.md },
  activityInfo: { flex: 1 },
  activityText: { color: colors.text, fontSize: typography.fontSize.md },
  activityTime: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  budgetCard: { backgroundColor: colors.surface, marginHorizontal: spacing.lg, borderRadius: borderRadius.lg, padding: spacing.md },
  budgetHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.sm },
  budgetLabel: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  budgetValue: { color: colors.text, fontSize: typography.fontSize.sm, fontWeight: '600' },
  budgetBar: { height: 8, backgroundColor: colors.border, borderRadius: 4, overflow: 'hidden' },
  budgetFill: { height: '100%', borderRadius: 4 },
  budgetRemaining: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: spacing.sm },
  bottomSpace: { height: spacing.xxl },
});
