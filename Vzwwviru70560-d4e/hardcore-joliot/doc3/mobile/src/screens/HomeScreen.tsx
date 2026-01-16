/**
 * CHE·NU Mobile - Home Screen
 * Écran d'accueil avec dashboard et raccourcis
 */
import React, { useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  RefreshControl,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useNavigation } from '@react-navigation/native';
import { useUIStore, useAuthStore, useSpheresStore, useProjectsStore, useNotificationsStore } from '../store';
import { lightTheme, darkTheme, colors, spacing, borderRadius, shadows } from '../theme';

const { width } = Dimensions.get('window');

const HomeScreen = () => {
  const navigation = useNavigation<any>();
  const { theme } = useUIStore();
  const { user } = useAuthStore();
  const { spheres, currentSphere } = useSpheresStore();
  const { projects, fetchProjects } = useProjectsStore();
  const { unreadCount } = useNotificationsStore();
  
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  const [refreshing, setRefreshing] = React.useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchProjects();
    setRefreshing(false);
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Bonjour';
    if (hour < 18) return 'Bon après-midi';
    return 'Bonsoir';
  };

  const activeProjects = projects.filter(p => p.status === 'active');
  const activeSpheres = spheres.filter(s => s.isActive).slice(0, 6);

  return (
    <ScrollView
      style={[styles.container, { backgroundColor: themeColors.background }]}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header avec gradient */}
      <LinearGradient
        colors={[colors.primary[600], colors.primary[800]]}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View style={styles.headerTop}>
            <View>
              <Text style={styles.greeting}>{getGreeting()},</Text>
              <Text style={styles.userName}>{user?.name || 'Utilisateur'}</Text>
            </View>
            <TouchableOpacity 
              style={styles.notifButton}
              onPress={() => navigation.navigate('Notifications')}
            >
              <Text style={styles.notifIcon}>🔔</Text>
              {unreadCount > 0 && (
                <View style={styles.notifBadge}>
                  <Text style={styles.notifBadgeText}>{unreadCount}</Text>
                </View>
              )}
            </TouchableOpacity>
          </View>
          
          {/* Search bar */}
          <TouchableOpacity 
            style={styles.searchBar}
            onPress={() => navigation.navigate('Search')}
          >
            <Text style={styles.searchIcon}>🔍</Text>
            <Text style={styles.searchPlaceholder}>Rechercher...</Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>

      {/* Nova Quick Action */}
      <TouchableOpacity 
        style={styles.novaCard}
        onPress={() => navigation.navigate('Nova')}
      >
        <LinearGradient
          colors={[colors.primary[500], colors.accent.purple]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.novaGradient}
        >
          <View style={styles.novaContent}>
            <Text style={styles.novaAvatar}>✨</Text>
            <View style={styles.novaText}>
              <Text style={styles.novaTitle}>Nova</Text>
              <Text style={styles.novaSubtitle}>Votre assistant IA universel</Text>
            </View>
            <Text style={styles.novaArrow}>→</Text>
          </View>
        </LinearGradient>
      </TouchableOpacity>

      {/* Quick Stats */}
      <View style={styles.section}>
        <Text style={[styles.sectionTitle, { color: themeColors.text }]}>
          Aperçu rapide
        </Text>
        <View style={styles.statsGrid}>
          <View style={[styles.statCard, { backgroundColor: themeColors.surface }]}>
            <Text style={styles.statIcon}>📋</Text>
            <Text style={[styles.statValue, { color: themeColors.text }]}>
              {activeProjects.length}
            </Text>
            <Text style={[styles.statLabel, { color: themeColors.textSecondary }]}>
              Projets actifs
            </Text>
          </View>
          <View style={[styles.statCard, { backgroundColor: themeColors.surface }]}>
            <Text style={styles.statIcon}>✅</Text>
            <Text style={[styles.statValue, { color: themeColors.text }]}>12</Text>
            <Text style={[styles.statLabel, { color: themeColors.textSecondary }]}>
              Tâches aujourd'hui
            </Text>
          </View>
          <View style={[styles.statCard, { backgroundColor: themeColors.surface }]}>
            <Text style={styles.statIcon}>📅</Text>
            <Text style={[styles.statValue, { color: themeColors.text }]}>3</Text>
            <Text style={[styles.statLabel, { color: themeColors.textSecondary }]}>
              Réunions
            </Text>
          </View>
          <View style={[styles.statCard, { backgroundColor: themeColors.surface }]}>
            <Text style={styles.statIcon}>🤖</Text>
            <Text style={[styles.statValue, { color: themeColors.text }]}>168</Text>
            <Text style={[styles.statLabel, { color: themeColors.textSecondary }]}>
              Agents IA
            </Text>
          </View>
        </View>
      </View>

      {/* Sphères rapides */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={[styles.sectionTitle, { color: themeColors.text }]}>
            Vos Sphères
          </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Spheres')}>
            <Text style={[styles.seeAll, { color: colors.primary[500] }]}>
              Voir tout →
            </Text>
          </TouchableOpacity>
        </View>
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.spheresScroll}
        >
          {activeSpheres.map((sphere) => (
            <TouchableOpacity
              key={sphere.id}
              style={styles.sphereCard}
              onPress={() => navigation.navigate('SphereDetail', { sphereId: sphere.id })}
            >
              <LinearGradient
                colors={sphere.gradient}
                style={styles.sphereGradient}
              >
                <Text style={styles.sphereIcon}>{sphere.icon}</Text>
                <Text style={styles.sphereName}>{sphere.nameFr}</Text>
              </LinearGradient>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Projets récents */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={[styles.sectionTitle, { color: themeColors.text }]}>
            Projets récents
          </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Projects')}>
            <Text style={[styles.seeAll, { color: colors.primary[500] }]}>
              Voir tout →
            </Text>
          </TouchableOpacity>
        </View>
        {activeProjects.slice(0, 3).map((project) => (
          <TouchableOpacity
            key={project.id}
            style={[styles.projectCard, { backgroundColor: themeColors.surface }]}
            onPress={() => navigation.navigate('ProjectDetail', { projectId: project.id })}
          >
            <View style={styles.projectHeader}>
              <View style={[
                styles.priorityDot, 
                { backgroundColor: colors.priority[project.priority] }
              ]} />
              <Text style={[styles.projectName, { color: themeColors.text }]}>
                {project.name}
              </Text>
            </View>
            <View style={styles.projectProgress}>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { 
                      width: `${project.progress}%`,
                      backgroundColor: colors.spheres[project.sphere],
                    }
                  ]} 
                />
              </View>
              <Text style={[styles.progressText, { color: themeColors.textSecondary }]}>
                {project.progress}%
              </Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Actions rapides */}
      <View style={styles.section}>
        <Text style={[styles.sectionTitle, { color: themeColors.text }]}>
          Actions rapides
        </Text>
        <View style={styles.quickActions}>
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: themeColors.surface }]}
            onPress={() => navigation.navigate('Communications')}
          >
            <Text style={styles.actionIcon}>📧</Text>
            <Text style={[styles.actionLabel, { color: themeColors.text }]}>
              Emails
            </Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: themeColors.surface }]}
            onPress={() => navigation.navigate('Calendar')}
          >
            <Text style={styles.actionIcon}>📅</Text>
            <Text style={[styles.actionLabel, { color: themeColors.text }]}>
              Calendrier
            </Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: themeColors.surface }]}
            onPress={() => navigation.navigate('Construction')}
          >
            <Text style={styles.actionIcon}>🏗️</Text>
            <Text style={[styles.actionLabel, { color: themeColors.text }]}>
              Chantiers
            </Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: themeColors.surface }]}
            onPress={() => navigation.navigate('Agents')}
          >
            <Text style={styles.actionIcon}>🤖</Text>
            <Text style={[styles.actionLabel, { color: themeColors.text }]}>
              Agents
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerContent: {
    paddingHorizontal: spacing.lg,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.lg,
  },
  greeting: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.8)',
  },
  userName: {
    fontSize: 28,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  notifButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  notifIcon: {
    fontSize: 20,
  },
  notifBadge: {
    position: 'absolute',
    top: -4,
    right: -4,
    backgroundColor: colors.status.error,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  notifBadgeText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: borderRadius.xl,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm + 4,
    gap: spacing.sm,
  },
  searchIcon: {
    fontSize: 16,
  },
  searchPlaceholder: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 16,
  },
  novaCard: {
    marginHorizontal: spacing.lg,
    marginTop: -20,
    borderRadius: borderRadius.xl,
    overflow: 'hidden',
    ...shadows.lg,
  },
  novaGradient: {
    padding: spacing.lg,
  },
  novaContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  novaAvatar: {
    fontSize: 40,
  },
  novaText: {
    flex: 1,
  },
  novaTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  novaSubtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
  },
  novaArrow: {
    fontSize: 24,
    color: '#FFFFFF',
  },
  section: {
    marginTop: spacing.xl,
    paddingHorizontal: spacing.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  seeAll: {
    fontSize: 14,
    fontWeight: '500',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  statCard: {
    width: (width - spacing.lg * 2 - spacing.sm) / 2,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    ...shadows.sm,
  },
  statIcon: {
    fontSize: 28,
    marginBottom: spacing.xs,
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
  },
  statLabel: {
    fontSize: 12,
    textAlign: 'center',
  },
  spheresScroll: {
    paddingRight: spacing.lg,
    gap: spacing.sm,
  },
  sphereCard: {
    width: 100,
    height: 100,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    ...shadows.md,
  },
  sphereGradient: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.sm,
  },
  sphereIcon: {
    fontSize: 32,
    marginBottom: spacing.xs,
  },
  sphereName: {
    fontSize: 11,
    fontWeight: '600',
    color: '#FFFFFF',
    textAlign: 'center',
  },
  projectCard: {
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  projectHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  projectName: {
    fontSize: 16,
    fontWeight: '500',
    flex: 1,
  },
  projectProgress: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  progressBar: {
    flex: 1,
    height: 6,
    backgroundColor: 'rgba(0,0,0,0.1)',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  progressText: {
    fontSize: 12,
    fontWeight: '500',
    width: 40,
    textAlign: 'right',
  },
  quickActions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  actionButton: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  actionIcon: {
    fontSize: 24,
    marginBottom: spacing.xs,
  },
  actionLabel: {
    fontSize: 12,
    fontWeight: '500',
  },
});

export default HomeScreen;
