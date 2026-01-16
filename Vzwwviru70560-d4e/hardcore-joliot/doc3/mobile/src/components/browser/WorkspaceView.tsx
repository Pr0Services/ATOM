// CHE·NU Mobile - Workspace View (Browser Internal)
// Default view: notes, data entry, create/edit documents

import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, TextInput } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';

// Mock data
const recentFiles = [
  { id: '1', name: 'Rapport Q4 2024.docx', type: 'doc', modified: 'Il y a 2h', hasAgentChanges: true },
  { id: '2', name: 'Budget 2025.xlsx', type: 'xls', modified: 'Hier', hasAgentChanges: false },
  { id: '3', name: 'Pitch Deck v3.pptx', type: 'ppt', modified: 'Il y a 3j', hasAgentChanges: true },
];

const quickNotes = [
  { id: 'n1', content: 'Appeler le fournisseur demain', date: 'Aujourd\'hui' },
  { id: 'n2', content: 'Revoir les projections Q1', date: 'Hier' },
];

export default function WorkspaceView() {
  const [newNote, setNewNote] = useState('');

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'doc': return 'document-text';
      case 'xls': return 'grid';
      case 'ppt': return 'easel';
      default: return 'document';
    }
  };

  const getFileColor = (type: string) => {
    switch (type) {
      case 'doc': return '#2B579A';
      case 'xls': return '#217346';
      case 'ppt': return '#D24726';
      default: return colors.primary;
    }
  };

  const handleAddNote = () => {
    if (newNote.trim()) {
      // TODO: Save note
      setNewNote('');
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Quick Note Input */}
      <View style={styles.noteInputContainer}>
        <View style={styles.noteInput}>
          <Ionicons name="create-outline" size={20} color={colors.textMuted} />
          <TextInput
            style={styles.noteTextInput}
            placeholder="Ajouter une note rapide..."
            placeholderTextColor={colors.textMuted}
            value={newNote}
            onChangeText={setNewNote}
            multiline
          />
          {newNote.trim() && (
            <TouchableOpacity style={styles.noteAddButton} onPress={handleAddNote}>
              <Ionicons name="add-circle" size={28} color={colors.primary} />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Create New */}
      <Text style={styles.sectionTitle}>Créer</Text>
      <View style={styles.createGrid}>
        {[
          { id: 'doc', name: 'Document', icon: 'document-text', color: '#2B579A' },
          { id: 'sheet', name: 'Feuille', icon: 'grid', color: '#217346' },
          { id: 'slide', name: 'Présentation', icon: 'easel', color: '#D24726' },
          { id: 'note', name: 'Note', icon: 'create', color: colors.primary },
        ].map(item => (
          <TouchableOpacity key={item.id} style={styles.createItem}>
            <View style={[styles.createIcon, { backgroundColor: item.color + '20' }]}>
              <Ionicons name={item.icon as any} size={28} color={item.color} />
            </View>
            <Text style={styles.createLabel}>{item.name}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Agent Changes Banner */}
      <TouchableOpacity style={styles.agentBanner}>
        <LinearGradient colors={[colors.warning + '30', colors.accent + '20']} style={styles.agentBannerGradient}>
          <View style={styles.agentBannerIcon}>
            <Ionicons name="git-compare" size={24} color={colors.warning} />
          </View>
          <View style={styles.agentBannerContent}>
            <Text style={styles.agentBannerTitle}>2 fichiers modifiés par des agents</Text>
            <Text style={styles.agentBannerSubtitle}>Cliquez pour reviewer les changements</Text>
          </View>
          <Ionicons name="chevron-forward" size={24} color={colors.textMuted} />
        </LinearGradient>
      </TouchableOpacity>

      {/* Recent Files */}
      <Text style={styles.sectionTitle}>Fichiers Récents</Text>
      {recentFiles.map(file => (
        <TouchableOpacity key={file.id} style={styles.fileItem}>
          <View style={[styles.fileIcon, { backgroundColor: getFileColor(file.type) + '20' }]}>
            <Ionicons name={getFileIcon(file.type)} size={24} color={getFileColor(file.type)} />
          </View>
          <View style={styles.fileInfo}>
            <Text style={styles.fileName}>{file.name}</Text>
            <Text style={styles.fileMeta}>{file.modified}</Text>
          </View>
          {file.hasAgentChanges && (
            <View style={styles.changesBadge}>
              <Ionicons name="git-branch" size={14} color={colors.warning} />
            </View>
          )}
          <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
        </TouchableOpacity>
      ))}

      {/* Quick Notes */}
      <Text style={styles.sectionTitle}>Notes Rapides</Text>
      {quickNotes.map(note => (
        <View key={note.id} style={styles.noteItem}>
          <Text style={styles.noteContent}>{note.content}</Text>
          <Text style={styles.noteDate}>{note.date}</Text>
        </View>
      ))}

      {/* Storage Info */}
      <View style={styles.storageCard}>
        <View style={styles.storageHeader}>
          <Ionicons name="cloud" size={20} color={colors.primary} />
          <Text style={styles.storageTitle}>Stockage CHE·NU</Text>
        </View>
        <View style={styles.storageBar}>
          <View style={[styles.storageFill, { width: '35%' }]} />
        </View>
        <Text style={styles.storageText}>3.5 GB utilisés sur 10 GB</Text>
      </View>

      <View style={styles.bottomSpace} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  noteInputContainer: { marginBottom: spacing.lg },
  noteInput: {
    flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm,
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, ...shadows.sm,
  },
  noteTextInput: { flex: 1, color: colors.text, fontSize: typography.fontSize.md, minHeight: 40, maxHeight: 100 },
  noteAddButton: {},
  sectionTitle: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold', marginBottom: spacing.md, marginTop: spacing.md },
  createGrid: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: spacing.md },
  createItem: { alignItems: 'center', width: '22%' },
  createIcon: { width: 60, height: 60, borderRadius: 16, justifyContent: 'center', alignItems: 'center', marginBottom: spacing.xs },
  createLabel: { color: colors.textSecondary, fontSize: typography.fontSize.xs, textAlign: 'center' },
  agentBanner: { borderRadius: borderRadius.lg, overflow: 'hidden', marginBottom: spacing.lg },
  agentBannerGradient: { flexDirection: 'row', alignItems: 'center', padding: spacing.md },
  agentBannerIcon: { width: 48, height: 48, borderRadius: 24, backgroundColor: colors.warning + '30', justifyContent: 'center', alignItems: 'center', marginRight: spacing.md },
  agentBannerContent: { flex: 1 },
  agentBannerTitle: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '600' },
  agentBannerSubtitle: { color: colors.textSecondary, fontSize: typography.fontSize.sm, marginTop: 2 },
  fileItem: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, marginBottom: spacing.sm, ...shadows.sm,
  },
  fileIcon: { width: 44, height: 44, borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginRight: spacing.md },
  fileInfo: { flex: 1 },
  fileName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '500' },
  fileMeta: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  changesBadge: { marginRight: spacing.sm },
  noteItem: {
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, marginBottom: spacing.sm,
    borderLeftWidth: 3, borderLeftColor: colors.primary,
  },
  noteContent: { color: colors.text, fontSize: typography.fontSize.md },
  noteDate: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: spacing.xs },
  storageCard: {
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, marginTop: spacing.lg, ...shadows.sm,
  },
  storageHeader: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.md },
  storageTitle: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '600' },
  storageBar: { height: 8, backgroundColor: colors.border, borderRadius: 4, overflow: 'hidden', marginBottom: spacing.sm },
  storageFill: { height: '100%', backgroundColor: colors.primary, borderRadius: 4 },
  storageText: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  bottomSpace: { height: spacing.xxl },
});
