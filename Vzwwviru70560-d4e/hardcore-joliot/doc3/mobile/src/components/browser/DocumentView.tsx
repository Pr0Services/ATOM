// CHE·NU Mobile - Document View (Browser Internal)
import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';

interface DocumentViewProps {
  documentId: string | null;
}

export function DocumentView({ documentId }: DocumentViewProps) {
  // Mock documents list if no specific document
  const documents = [
    { id: '1', name: 'Rapport Q4 2024.docx', type: 'doc', size: '245 KB', modified: 'Il y a 2h' },
    { id: '2', name: 'Budget 2025.xlsx', type: 'xls', size: '89 KB', modified: 'Hier' },
    { id: '3', name: 'Pitch Deck v3.pptx', type: 'ppt', size: '1.2 MB', modified: 'Il y a 3j' },
    { id: '4', name: 'Contrat Client.pdf', type: 'pdf', size: '567 KB', modified: 'Il y a 1 sem' },
  ];

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'doc': return 'document-text';
      case 'xls': return 'grid';
      case 'ppt': return 'easel';
      case 'pdf': return 'document';
      default: return 'document';
    }
  };

  const getFileColor = (type: string) => {
    switch (type) {
      case 'doc': return '#2B579A';
      case 'xls': return '#217346';
      case 'ppt': return '#D24726';
      case 'pdf': return '#FF0000';
      default: return colors.primary;
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Documents</Text>
      <Text style={styles.subtitle}>{documents.length} fichiers</Text>

      {/* Sort/Filter */}
      <View style={styles.filterRow}>
        <TouchableOpacity style={styles.filterButton}>
          <Ionicons name="funnel-outline" size={18} color={colors.textMuted} />
          <Text style={styles.filterText}>Filtrer</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.filterButton}>
          <Ionicons name="swap-vertical" size={18} color={colors.textMuted} />
          <Text style={styles.filterText}>Trier</Text>
        </TouchableOpacity>
      </View>

      {/* Documents List */}
      {documents.map(doc => (
        <TouchableOpacity key={doc.id} style={styles.docItem}>
          <View style={[styles.docIcon, { backgroundColor: getFileColor(doc.type) + '20' }]}>
            <Ionicons name={getFileIcon(doc.type)} size={24} color={getFileColor(doc.type)} />
          </View>
          <View style={styles.docInfo}>
            <Text style={styles.docName}>{doc.name}</Text>
            <Text style={styles.docMeta}>{doc.size} • {doc.modified}</Text>
          </View>
          <TouchableOpacity style={styles.docAction}>
            <Ionicons name="ellipsis-vertical" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  title: { color: colors.text, fontSize: 24, fontWeight: 'bold' },
  subtitle: { color: colors.textMuted, fontSize: typography.fontSize.md, marginTop: spacing.xs, marginBottom: spacing.lg },
  filterRow: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.lg },
  filterButton: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs, backgroundColor: colors.surface, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: borderRadius.full },
  filterText: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  docItem: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface, borderRadius: borderRadius.lg, padding: spacing.md, marginBottom: spacing.sm, ...shadows.sm },
  docIcon: { width: 48, height: 48, borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginRight: spacing.md },
  docInfo: { flex: 1 },
  docName: { color: colors.text, fontSize: typography.fontSize.md, fontWeight: '500' },
  docMeta: { color: colors.textMuted, fontSize: typography.fontSize.sm, marginTop: 2 },
  docAction: { padding: spacing.sm },
});

export default DocumentView;
