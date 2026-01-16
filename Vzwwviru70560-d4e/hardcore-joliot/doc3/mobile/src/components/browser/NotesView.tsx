// CHE·NU Mobile - Notes View (Browser Internal)
import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, TextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';

export function NotesView() {
  const [newNote, setNewNote] = useState('');
  const [notes, setNotes] = useState([
    { id: '1', content: 'Appeler le fournisseur demain matin', date: 'Aujourd\'hui, 14:30', color: colors.primary },
    { id: '2', content: 'Revoir les projections Q1 avec l\'équipe finance', date: 'Hier, 09:15', color: colors.accent },
    { id: '3', content: 'Idées pour la nouvelle campagne marketing:\n- Vidéo témoignages clients\n- Partenariat influenceurs\n- Webinaire gratuit', date: 'Il y a 2j', color: colors.success },
    { id: '4', content: 'RDV dentiste le 15 à 10h', date: 'Il y a 3j', color: colors.warning },
  ]);

  const handleAddNote = () => {
    if (newNote.trim()) {
      const note = {
        id: Date.now().toString(),
        content: newNote.trim(),
        date: 'Maintenant',
        color: colors.primary,
      };
      setNotes([note, ...notes]);
      setNewNote('');
    }
  };

  const handleDeleteNote = (id: string) => {
    setNotes(notes.filter(n => n.id !== id));
  };

  return (
    <View style={styles.container}>
      {/* New Note Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Nouvelle note..."
          placeholderTextColor={colors.textMuted}
          value={newNote}
          onChangeText={setNewNote}
          multiline
        />
        <TouchableOpacity 
          style={[styles.addButton, !newNote.trim() && styles.addButtonDisabled]}
          onPress={handleAddNote}
          disabled={!newNote.trim()}
        >
          <Ionicons name="add" size={24} color={newNote.trim() ? colors.text : colors.textMuted} />
        </TouchableOpacity>
      </View>

      {/* Notes List */}
      <ScrollView style={styles.notesList} contentContainerStyle={styles.notesContent}>
        <Text style={styles.title}>Mes Notes ({notes.length})</Text>
        
        {notes.map(note => (
          <View 
            key={note.id} 
            style={[styles.noteCard, { borderLeftColor: note.color }]}
          >
            <Text style={styles.noteContent}>{note.content}</Text>
            <View style={styles.noteFooter}>
              <Text style={styles.noteDate}>{note.date}</Text>
              <TouchableOpacity 
                style={styles.deleteButton}
                onPress={() => handleDeleteNote(note.id)}
              >
                <Ionicons name="trash-outline" size={18} color={colors.error} />
              </TouchableOpacity>
            </View>
          </View>
        ))}

        {notes.length === 0 && (
          <View style={styles.emptyState}>
            <Ionicons name="create-outline" size={64} color={colors.textMuted} />
            <Text style={styles.emptyTitle}>Aucune note</Text>
            <Text style={styles.emptyText}>Commencez à écrire ci-dessus</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  inputContainer: {
    flexDirection: 'row', alignItems: 'flex-end', gap: spacing.sm,
    padding: spacing.lg, backgroundColor: colors.surface,
    borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  input: {
    flex: 1, backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.lg,
    padding: spacing.md, color: colors.text, fontSize: typography.fontSize.md,
    minHeight: 50, maxHeight: 120,
  },
  addButton: {
    width: 50, height: 50, borderRadius: 25, backgroundColor: colors.primary,
    justifyContent: 'center', alignItems: 'center',
  },
  addButtonDisabled: { backgroundColor: colors.border },
  notesList: { flex: 1 },
  notesContent: { padding: spacing.lg },
  title: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold', marginBottom: spacing.lg },
  noteCard: {
    backgroundColor: colors.surface, borderRadius: borderRadius.lg,
    padding: spacing.md, marginBottom: spacing.md,
    borderLeftWidth: 4, ...shadows.sm,
  },
  noteContent: { color: colors.text, fontSize: typography.fontSize.md, lineHeight: 22 },
  noteFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: spacing.md },
  noteDate: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  deleteButton: { padding: spacing.xs },
  emptyState: { alignItems: 'center', paddingVertical: spacing.xxl * 2 },
  emptyTitle: { color: colors.text, fontSize: typography.fontSize.xl, marginTop: spacing.lg },
  emptyText: { color: colors.textMuted, fontSize: typography.fontSize.md, marginTop: spacing.xs },
});

export default NotesView;
