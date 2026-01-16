// CHE·NU Mobile - Browser Internal Views

// === SPHERE VIEW ===
import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';
import { useSpheresStore } from '../../store';

interface SphereViewProps {
  sphereId: string | null;
}

export function SphereView({ sphereId }: SphereViewProps) {
  const { spheres } = useSpheresStore();
  const sphere = spheres.find(s => s.id === sphereId);

  if (!sphere) {
    return (
      <View style={sphereStyles.container}>
        <Text style={sphereStyles.errorText}>Sphère non trouvée</Text>
      </View>
    );
  }

  return (
    <ScrollView style={sphereStyles.container} contentContainerStyle={sphereStyles.content}>
      {/* Sphere Header */}
      <LinearGradient colors={[sphere.color, sphere.color + '80']} style={sphereStyles.header}>
        <View style={sphereStyles.headerIcon}>
          <Ionicons name={sphere.icon as any} size={40} color={colors.text} />
        </View>
        <Text style={sphereStyles.headerTitle}>{sphere.name}</Text>
        <Text style={sphereStyles.headerDesc}>{sphere.description}</Text>
      </LinearGradient>

      {/* Stats */}
      <View style={sphereStyles.statsRow}>
        <View style={sphereStyles.statItem}>
          <Text style={sphereStyles.statValue}>{sphere.agent_count || 0}</Text>
          <Text style={sphereStyles.statLabel}>Agents</Text>
        </View>
        <View style={sphereStyles.statItem}>
          <Text style={sphereStyles.statValue}>{(sphere.budget.remaining / 1000).toFixed(0)}k</Text>
          <Text style={sphereStyles.statLabel}>Tokens</Text>
        </View>
        <View style={sphereStyles.statItem}>
          <Text style={sphereStyles.statValue}>12</Text>
          <Text style={sphereStyles.statLabel}>Documents</Text>
        </View>
      </View>

      {/* Content sections would go here */}
      <Text style={sphereStyles.sectionTitle}>Contenu de la sphère</Text>
      <View style={sphereStyles.placeholder}>
        <Ionicons name="folder-open-outline" size={48} color={colors.textMuted} />
        <Text style={sphereStyles.placeholderText}>Documents et données de {sphere.name}</Text>
      </View>
    </ScrollView>
  );
}

const sphereStyles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { paddingBottom: spacing.xxl },
  header: { padding: spacing.xl, alignItems: 'center' },
  headerIcon: { width: 80, height: 80, borderRadius: 24, backgroundColor: 'rgba(255,255,255,0.2)', justifyContent: 'center', alignItems: 'center', marginBottom: spacing.md },
  headerTitle: { color: colors.text, fontSize: 28, fontWeight: 'bold' },
  headerDesc: { color: 'rgba(255,255,255,0.8)', fontSize: typography.fontSize.md, textAlign: 'center', marginTop: spacing.xs },
  statsRow: { flexDirection: 'row', justifyContent: 'space-around', padding: spacing.lg, backgroundColor: colors.surface },
  statItem: { alignItems: 'center' },
  statValue: { color: colors.text, fontSize: 24, fontWeight: 'bold' },
  statLabel: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  sectionTitle: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold', margin: spacing.lg },
  placeholder: { alignItems: 'center', padding: spacing.xxl },
  placeholderText: { color: colors.textMuted, fontSize: typography.fontSize.md, marginTop: spacing.md },
  errorText: { color: colors.error, textAlign: 'center', marginTop: spacing.xxl },
});

export default SphereView;
