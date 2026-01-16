// CHE·NU Mobile - Navigation Hub Screen (Tab 2)
// Landing page after login
// Opens spheres, sites, documents → displays in Tab 3 (Browser)

import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, TextInput } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';
import { useAuthStore, useSpheresStore } from '../store';

export default function NavigationHubScreen() {
  const navigation = useNavigation<any>();
  const { user } = useAuthStore();
  const { spheres } = useSpheresStore();

  // Navigate to Browser tab with URL
  const openInBrowser = (url: string) => {
    navigation.navigate('ChenuBrowser', { url });
  };

  // Quick links / favorites
  const quickLinks = [
    { id: 'workspace', name: 'Workspace', icon: 'folder', url: 'chenu://workspace', color: colors.primary },
    { id: 'docs', name: 'Documents', icon: 'document-text', url: 'chenu://documents', color: colors.accent },
    { id: 'notes', name: 'Notes', icon: 'create', url: 'chenu://notes', color: colors.success },
  ];

  // External sites
  const externalSites = [
    { id: 'google', name: 'Google', icon: 'logo-google', url: 'https://google.com', color: '#4285F4' },
    { id: 'facebook', name: 'Facebook', icon: 'logo-facebook', url: 'https://facebook.com', color: '#1877F2' },
    { id: 'amazon', name: 'Amazon', icon: 'cart', url: 'https://amazon.ca', color: '#FF9900' },
    { id: 'youtube', name: 'YouTube', icon: 'logo-youtube', url: 'https://youtube.com', color: '#FF0000' },
  ];

  return (
    <View style={styles.container}>
      {/* Header */}
      <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.header}>
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.greeting}>Bonjour, {user?.name?.split(' ')[0] || 'Jo'}! 👋</Text>
            <Text style={styles.subtitle}>Que voulez-vous faire aujourd'hui?</Text>
          </View>
          <TouchableOpacity 
            style={styles.accountButton}
            onPress={() => navigation.navigate('Account')}
          >
            <View style={styles.accountAvatar}>
              <Text style={styles.accountAvatarText}>{user?.name?.charAt(0) || 'U'}</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* URL Bar */}
        <TouchableOpacity 
          style={styles.urlBar}
          onPress={() => openInBrowser('chenu://workspace')}
        >
          <Ionicons name="search" size={20} color={colors.textMuted} />
          <Text style={styles.urlBarText}>Rechercher ou entrer une URL...</Text>
          <Ionicons name="mic" size={20} color={colors.primary} />
        </TouchableOpacity>
      </LinearGradient>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Quick Access */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Accès Rapide</Text>
          <View style={styles.quickGrid}>
            {quickLinks.map(link => (
              <TouchableOpacity 
                key={link.id}
                style={styles.quickItem}
                onPress={() => openInBrowser(link.url)}
              >
                <View style={[styles.quickIcon, { backgroundColor: link.color + '20' }]}>
                  <Ionicons name={link.icon as any} size={24} color={link.color} />
                </View>
                <Text style={styles.quickLabel}>{link.name}</Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity style={styles.quickItem} onPress={() => navigation.navigate('Settings')}>
              <View style={[styles.quickIcon, { backgroundColor: colors.textMuted + '20' }]}>
                <Ionicons name="settings" size={24} color={colors.textMuted} />
              </View>
              <Text style={styles.quickLabel}>Paramètres</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Spheres */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Mes Sphères</Text>
            <TouchableOpacity>
              <Text style={styles.seeAll}>Voir tout</Text>
            </TouchableOpacity>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.spheresScroll}>
            {spheres.filter(s => s.is_active).map(sphere => (
              <TouchableOpacity 
                key={sphere.id}
                style={styles.sphereCard}
                onPress={() => openInBrowser(`chenu://sphere/${sphere.id}`)}
              >
                <LinearGradient colors={[sphere.color, sphere.color + 'CC']} style={styles.sphereGradient}>
                  <View style={styles.sphereIcon}>
                    <Ionicons name={sphere.icon as any} size={28} color={colors.text} />
                  </View>
                  <Text style={styles.sphereName}>{sphere.name}</Text>
                  <Text style={styles.sphereAgents}>{sphere.agent_count || 0} agents</Text>
                </LinearGradient>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* External Sites */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Sites Favoris</Text>
            <TouchableOpacity>
              <Ionicons name="add-circle-outline" size={24} color={colors.primary} />
            </TouchableOpacity>
          </View>
          <View style={styles.sitesGrid}>
            {externalSites.map(site => (
              <TouchableOpacity 
                key={site.id}
                style={styles.siteItem}
                onPress={() => openInBrowser(site.url)}
              >
                <View style={[styles.siteIcon, { backgroundColor: site.color + '20' }]}>
                  <Ionicons name={site.icon as any} size={28} color={site.color} />
                </View>
                <Text style={styles.siteName}>{site.name}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Recent Activity */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Activité Récente</Text>
          {[
            { id: '1', title: 'Rapport Q4 modifié', agent: 'Agent Finance', time: 'Il y a 2h', icon: 'document-text' },
            { id: '2', title: 'Nouvelle tâche créée', agent: 'Nova', time: 'Il y a 4h', icon: 'checkmark-circle' },
            { id: '3', title: 'Présentation révisée', agent: 'Agent Creative', time: 'Hier', icon: 'easel' },
          ].map(activity => (
            <TouchableOpacity key={activity.id} style={styles.activityItem}>
              <View style={styles.activityIcon}>
                <Ionicons name={activity.icon as any} size={20} color={colors.primary} />
              </View>
              <View style={styles.activityInfo}>
                <Text style={styles.activityTitle}>{activity.title}</Text>
                <Text style={styles.activityMeta}>{activity.agent} • {activity.time}</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.bottomSpace} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { paddingTop: 60, paddingBottom: spacing.lg, paddingHorizontal: spacing.lg },
  headerContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: spacing.lg },
  greeting: { color: colors.text, fontSize: typography.fontSize.xxl, fontWeight: 'bold' },
  subtitle: { color: 'rgba(255,255,255,0.8)', fontSize: typography.fontSize.md, marginTop: spacing.xs },
  accountButton: {},
  accountAvatar: {
    width: 44, height: 44, borderRadius: 22, backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center', alignItems: 'center',
  },
  accountAvatarText: { color: colors.text, fontSize: 18, fontWeight: 'bold' },
  urlBar: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.sm,
    backgroundColor: colors.surface, borderRadius: borderRadius.full,
    paddingHorizontal: spacing.md, paddingVertical: spacing.md,
  },
  urlBarText: { flex: 1, color: colors.textMuted, fontSize: typography.fontSize.md },
  content: { flex: 1 },
  section: { paddingHorizontal: spacing.lg, marginTop: spacing.lg },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: spacing.md },
  sectionTitle: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold', marginBottom: spacing.md },
  seeAll: { color: colors.primary, fontSize: typography.fontSize.sm },
  quickGrid: { flexDirection: 'row', justifyContent: 'space-between' },
  quickItem: { alignItems: 'center', width: '22%' },
  quickIcon: { width: 56, height: 56, borderRadius: 16, justifyContent: 'center', alignItems: 'center', marginBottom: spacing.xs },
  quickLabel: { color: colors.textSecondary, fontSize: typography.fontSize.xs, textAlign: 'center' },
  spheresScroll: { marginHorizontal: -spacing.lg, paddingHorizontal: spacing.lg },
  sphereCard: { width: 140, marginRight: spacing.md, borderRadius: borderRadius.lg, overflow: 'hidden', ...shadows.md },
  sphereGradient: { padding: spacing.md, height: 120 },
  sphereIcon: { marginBottom: spacing.sm },
  sphereName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: 'bold' },
  sphereAgents: { color: 'rgba(255,255,255,0.7)', fontSize: typography.fontSize.sm, marginTop: 4 },
  sitesGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  siteItem: { alignItems: 'center', width: '22%' },
  siteIcon: { width: 56, height: 56, borderRadius: borderRadius.lg, justifyContent: 'center', alignItems: 'center', marginBottom: spacing.xs },
  siteName: { color: colors.textSecondary, fontSize: typography.fontSize.xs, textAlign: 'center' },
  activityItem: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, marginBottom: spacing.sm, ...shadows.sm,
  },
  activityIcon: {
    width: 40, height: 40, borderRadius: 20, backgroundColor: colors.primary + '20',
    justifyContent: 'center', alignItems: 'center', marginRight: spacing.md,
  },
  activityInfo: { flex: 1 },
  activityTitle: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '500' },
  activityMeta: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  bottomSpace: { height: spacing.xxl * 2 },
});
