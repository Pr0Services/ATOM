// CHE·NU Mobile - Settings Screen
import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Switch } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography } from '../theme';
import { useAuthStore } from '../store';

export default function SettingsScreen() {
  const { user, updatePreferences } = useAuthStore();
  
  const [notifications, setNotifications] = useState(user?.preferences?.notifications ?? true);
  const [darkMode, setDarkMode] = useState(true);
  const [biometric, setBiometric] = useState(false);

  const handleNotificationsToggle = (value: boolean) => {
    setNotifications(value);
    updatePreferences({ notifications: value });
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Appearance */}
      <Text style={styles.sectionTitle}>Apparence</Text>
      <View style={styles.section}>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="moon-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Mode sombre</Text>
          </View>
          <Switch
            value={darkMode}
            onValueChange={setDarkMode}
            trackColor={{ false: colors.border, true: colors.primary }}
            thumbColor={colors.text}
          />
        </View>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="language-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Langue</Text>
          </View>
          <View style={styles.settingValue}>
            <Text style={styles.settingValueText}>Français</Text>
            <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
          </View>
        </View>
      </View>

      {/* Notifications */}
      <Text style={styles.sectionTitle}>Notifications</Text>
      <View style={styles.section}>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="notifications-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Notifications push</Text>
          </View>
          <Switch
            value={notifications}
            onValueChange={handleNotificationsToggle}
            trackColor={{ false: colors.border, true: colors.primary }}
            thumbColor={colors.text}
          />
        </View>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="chatbubble-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Réponses agents</Text>
          </View>
          <Switch
            value={true}
            onValueChange={() => {}}
            trackColor={{ false: colors.border, true: colors.primary }}
            thumbColor={colors.text}
          />
        </View>
      </View>

      {/* Security */}
      <Text style={styles.sectionTitle}>Sécurité</Text>
      <View style={styles.section}>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="finger-print-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Authentification biométrique</Text>
          </View>
          <Switch
            value={biometric}
            onValueChange={setBiometric}
            trackColor={{ false: colors.border, true: colors.primary }}
            thumbColor={colors.text}
          />
        </View>
        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="lock-closed-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Changer le mot de passe</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </TouchableOpacity>
      </View>

      {/* Data */}
      <Text style={styles.sectionTitle}>Données</Text>
      <View style={styles.section}>
        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="cloud-download-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Exporter mes données</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="trash-outline" size={22} color={colors.error} />
            <Text style={[styles.settingLabel, { color: colors.error }]}>Supprimer mon compte</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </TouchableOpacity>
      </View>

      {/* About */}
      <Text style={styles.sectionTitle}>À propos</Text>
      <View style={styles.section}>
        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="information-circle-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Version</Text>
          </View>
          <Text style={styles.settingValueText}>1.0.0</Text>
        </View>
        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="document-text-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Conditions d'utilisation</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Ionicons name="shield-outline" size={22} color={colors.text} />
            <Text style={styles.settingLabel}>Politique de confidentialité</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { paddingBottom: spacing.xxl },
  sectionTitle: { color: colors.textMuted, fontSize: typography.fontSize.sm, fontWeight: '600', marginLeft: spacing.lg, marginTop: spacing.lg, marginBottom: spacing.sm, textTransform: 'uppercase' },
  section: { backgroundColor: colors.surface, marginHorizontal: spacing.lg, borderRadius: borderRadius.lg },
  settingItem: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border },
  settingInfo: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  settingLabel: { color: colors.text, fontSize: typography.fontSize.md },
  settingValue: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  settingValueText: { color: colors.textMuted, fontSize: typography.fontSize.md },
});
