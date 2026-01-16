import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, RefreshControl } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useProjectsStore, useUIStore, useSpheresStore } from '../store';
import { lightTheme, darkTheme, colors, spacing, borderRadius, shadows } from '../theme';

const ProjectsScreen = () => {
  const navigation = useNavigation<any>();
  const { projects, fetchProjects, isLoading } = useProjectsStore();
  const { theme } = useUIStore();
  const { spheres } = useSpheresStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState<string | null>(null);

  useEffect(() => { fetchProjects(); }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchProjects();
    setRefreshing(false);
  };

  const filteredProjects = filter ? projects.filter(p => p.status === filter) : projects;
  const statusFilters = ['all', 'active', 'draft', 'completed'];

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, string> = {
      draft: colors.status.info, planning: colors.status.info, active: colors.status.success,
      on_hold: colors.status.warning, completed: colors.primary[500], cancelled: colors.status.error,
    };
    return statusColors[status] || colors.primary[500];
  };

  return (
    <View style={[styles.container, { backgroundColor: themeColors.background }]}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: themeColors.text }]}>Projets</Text>
        <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('NewProject')}>
          <Text style={styles.addIcon}>+</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.filters}>
        {statusFilters.map((status) => (
          <TouchableOpacity
            key={status}
            style={[styles.filterChip, (filter === status || (status === 'all' && !filter)) && { backgroundColor: colors.primary[500] }]}
            onPress={() => setFilter(status === 'all' ? null : status)}
          >
            <Text style={[styles.filterText, (filter === status || (status === 'all' && !filter)) && { color: '#FFFFFF' }]}>
              {status === 'all' ? 'Tous' : status === 'active' ? 'Actifs' : status === 'draft' ? 'Brouillons' : 'Terminés'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <FlatList
        data={filteredProjects}
        keyExtractor={(item) => item.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        contentContainerStyle={styles.list}
        renderItem={({ item }) => {
          const sphere = spheres.find(s => s.id === item.sphere);
          return (
            <TouchableOpacity style={[styles.card, { backgroundColor: themeColors.surface }]} onPress={() => navigation.navigate('ProjectDetail', { projectId: item.id })}>
              <View style={styles.cardHeader}>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
                  <Text style={styles.statusText}>{item.status}</Text>
                </View>
                <Text style={[styles.sphereBadge, { backgroundColor: sphere?.color }]}>{sphere?.icon}</Text>
              </View>
              <Text style={[styles.cardTitle, { color: themeColors.text }]}>{item.name}</Text>
              <Text style={[styles.cardDesc, { color: themeColors.textSecondary }]} numberOfLines={2}>{item.description}</Text>
              <View style={styles.progressContainer}>
                <View style={[styles.progressBar, { backgroundColor: themeColors.inputBackground }]}>
                  <View style={[styles.progressFill, { width: `${item.progress}%`, backgroundColor: sphere?.color || colors.primary[500] }]} />
                </View>
                <Text style={[styles.progressText, { color: themeColors.textSecondary }]}>{item.progress}%</Text>
              </View>
              <View style={styles.cardFooter}>
                <Text style={[styles.taskCount, { color: themeColors.textMuted }]}>
                  {item.tasks.length} tâches
                </Text>
                {item.budget && (
                  <Text style={[styles.budget, { color: themeColors.textMuted }]}>
                    ${(item.budget.spent / 1000).toFixed(0)}k / ${(item.budget.total / 1000).toFixed(0)}k
                  </Text>
                )}
              </View>
            </TouchableOpacity>
          );
        }}
        ListEmptyComponent={() => (
          <View style={styles.empty}>
            <Text style={styles.emptyIcon}>📋</Text>
            <Text style={[styles.emptyText, { color: themeColors.textSecondary }]}>Aucun projet trouvé</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: spacing.lg, paddingTop: 60 },
  title: { fontSize: 32, fontWeight: '700' },
  addButton: { width: 44, height: 44, borderRadius: 22, backgroundColor: colors.primary[500], alignItems: 'center', justifyContent: 'center' },
  addIcon: { fontSize: 24, color: '#FFFFFF' },
  filters: { flexDirection: 'row', paddingHorizontal: spacing.lg, gap: spacing.sm, marginBottom: spacing.md },
  filterChip: { paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: borderRadius.full, backgroundColor: 'rgba(99,102,241,0.1)' },
  filterText: { fontSize: 14, fontWeight: '500', color: colors.primary[500] },
  list: { padding: spacing.lg, paddingTop: 0 },
  card: { padding: spacing.lg, borderRadius: borderRadius.xl, marginBottom: spacing.md, ...shadows.sm },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.sm },
  statusBadge: { paddingHorizontal: spacing.sm, paddingVertical: 2, borderRadius: borderRadius.sm },
  statusText: { fontSize: 12, color: '#FFFFFF', fontWeight: '500', textTransform: 'capitalize' },
  sphereBadge: { width: 28, height: 28, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  cardTitle: { fontSize: 18, fontWeight: '600', marginBottom: spacing.xs },
  cardDesc: { fontSize: 14, marginBottom: spacing.md },
  progressContainer: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.sm },
  progressBar: { flex: 1, height: 8, borderRadius: 4, overflow: 'hidden' },
  progressFill: { height: '100%' },
  progressText: { fontSize: 12, fontWeight: '600', width: 40 },
  cardFooter: { flexDirection: 'row', justifyContent: 'space-between' },
  taskCount: { fontSize: 12 },
  budget: { fontSize: 12 },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyIcon: { fontSize: 48, marginBottom: spacing.md },
  emptyText: { fontSize: 16 },
});

export default ProjectsScreen;
