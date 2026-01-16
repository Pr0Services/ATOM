// CHE·NU Mobile - Quick Access Bar
// Favorites and history management for CHE·NU Browser

import React, { useState } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet, ScrollView, Modal, TextInput, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';

interface Favorite {
  id: string;
  title: string;
  url: string;
  icon: string;
  color: string;
}

interface HistoryItem {
  id: string;
  title: string;
  url: string;
  timestamp: string;
}

interface QuickAccessBarProps {
  onNavigate: (url: string) => void;
}

export default function QuickAccessBar({ onNavigate }: QuickAccessBarProps) {
  const [showFavorites, setShowFavorites] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showAddFavorite, setShowAddFavorite] = useState(false);
  const [newFavoriteTitle, setNewFavoriteTitle] = useState('');
  const [newFavoriteUrl, setNewFavoriteUrl] = useState('');

  // Mock data
  const [favorites, setFavorites] = useState<Favorite[]>([
    { id: '1', title: 'Workspace', url: 'chenu://workspace', icon: 'folder', color: colors.primary },
    { id: '2', title: 'Notes', url: 'chenu://notes', icon: 'create', color: colors.success },
    { id: '3', title: 'Google', url: 'https://google.com', icon: 'logo-google', color: '#4285F4' },
    { id: '4', title: 'Facebook', url: 'https://facebook.com', icon: 'logo-facebook', color: '#1877F2' },
  ]);

  const [history, setHistory] = useState<HistoryItem[]>([
    { id: '1', title: 'Workspace', url: 'chenu://workspace', timestamp: 'Il y a 5 min' },
    { id: '2', title: 'Rapport Q4', url: 'chenu://doc/rapport-q4', timestamp: 'Il y a 15 min' },
    { id: '3', title: 'Google', url: 'https://google.com', timestamp: 'Il y a 1h' },
    { id: '4', title: 'Amazon', url: 'https://amazon.ca', timestamp: 'Il y a 2h' },
    { id: '5', title: 'Sphère Enterprise', url: 'chenu://sphere/enterprise', timestamp: 'Hier' },
  ]);

  const handleAddFavorite = () => {
    if (!newFavoriteTitle || !newFavoriteUrl) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }

    const newFavorite: Favorite = {
      id: Date.now().toString(),
      title: newFavoriteTitle,
      url: newFavoriteUrl,
      icon: newFavoriteUrl.startsWith('chenu://') ? 'apps' : 'globe',
      color: colors.primary,
    };

    setFavorites([...favorites, newFavorite]);
    setNewFavoriteTitle('');
    setNewFavoriteUrl('');
    setShowAddFavorite(false);
  };

  const handleRemoveFavorite = (id: string) => {
    setFavorites(favorites.filter(f => f.id !== id));
  };

  const handleClearHistory = () => {
    Alert.alert(
      'Effacer l\'historique',
      'Voulez-vous vraiment effacer tout l\'historique?',
      [
        { text: 'Annuler', style: 'cancel' },
        { text: 'Effacer', style: 'destructive', onPress: () => setHistory([]) },
      ]
    );
  };

  return (
    <>
      {/* Quick Access Buttons */}
      <View style={styles.container}>
        <TouchableOpacity
          style={styles.accessButton}
          onPress={() => setShowFavorites(true)}
        >
          <Ionicons name="star" size={20} color={colors.warning} />
          <Text style={styles.accessText}>Favoris</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.accessButton}
          onPress={() => setShowHistory(true)}
        >
          <Ionicons name="time" size={20} color={colors.primary} />
          <Text style={styles.accessText}>Historique</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.accessButton}
          onPress={() => onNavigate('chenu://workspace')}
        >
          <Ionicons name="home" size={20} color={colors.success} />
          <Text style={styles.accessText}>Accueil</Text>
        </TouchableOpacity>
      </View>

      {/* Favorites Modal */}
      <Modal
        visible={showFavorites}
        animationType="slide"
        transparent
        onRequestClose={() => setShowFavorites(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>⭐ Favoris</Text>
              <View style={styles.modalActions}>
                <TouchableOpacity
                  style={styles.addButton}
                  onPress={() => setShowAddFavorite(true)}
                >
                  <Ionicons name="add" size={24} color={colors.primary} />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setShowFavorites(false)}>
                  <Ionicons name="close" size={24} color={colors.textMuted} />
                </TouchableOpacity>
              </View>
            </View>

            <ScrollView style={styles.list}>
              {favorites.map(fav => (
                <TouchableOpacity
                  key={fav.id}
                  style={styles.listItem}
                  onPress={() => {
                    onNavigate(fav.url);
                    setShowFavorites(false);
                  }}
                >
                  <View style={[styles.itemIcon, { backgroundColor: fav.color + '20' }]}>
                    <Ionicons name={fav.icon as any} size={20} color={fav.color} />
                  </View>
                  <View style={styles.itemInfo}>
                    <Text style={styles.itemTitle}>{fav.title}</Text>
                    <Text style={styles.itemUrl} numberOfLines={1}>{fav.url}</Text>
                  </View>
                  <TouchableOpacity
                    style={styles.removeButton}
                    onPress={() => handleRemoveFavorite(fav.id)}
                  >
                    <Ionicons name="trash-outline" size={18} color={colors.error} />
                  </TouchableOpacity>
                </TouchableOpacity>
              ))}

              {favorites.length === 0 && (
                <View style={styles.emptyState}>
                  <Ionicons name="star-outline" size={48} color={colors.textMuted} />
                  <Text style={styles.emptyText}>Aucun favori</Text>
                </View>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* History Modal */}
      <Modal
        visible={showHistory}
        animationType="slide"
        transparent
        onRequestClose={() => setShowHistory(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>🕐 Historique</Text>
              <View style={styles.modalActions}>
                <TouchableOpacity
                  style={styles.clearButton}
                  onPress={handleClearHistory}
                >
                  <Text style={styles.clearText}>Effacer</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setShowHistory(false)}>
                  <Ionicons name="close" size={24} color={colors.textMuted} />
                </TouchableOpacity>
              </View>
            </View>

            <ScrollView style={styles.list}>
              {history.map(item => (
                <TouchableOpacity
                  key={item.id}
                  style={styles.listItem}
                  onPress={() => {
                    onNavigate(item.url);
                    setShowHistory(false);
                  }}
                >
                  <View style={[styles.itemIcon, { backgroundColor: colors.primary + '20' }]}>
                    <Ionicons
                      name={item.url.startsWith('chenu://') ? 'apps' : 'globe'}
                      size={20}
                      color={colors.primary}
                    />
                  </View>
                  <View style={styles.itemInfo}>
                    <Text style={styles.itemTitle}>{item.title}</Text>
                    <Text style={styles.itemUrl} numberOfLines={1}>{item.url}</Text>
                  </View>
                  <Text style={styles.itemTime}>{item.timestamp}</Text>
                </TouchableOpacity>
              ))}

              {history.length === 0 && (
                <View style={styles.emptyState}>
                  <Ionicons name="time-outline" size={48} color={colors.textMuted} />
                  <Text style={styles.emptyText}>Aucun historique</Text>
                </View>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Add Favorite Modal */}
      <Modal
        visible={showAddFavorite}
        animationType="fade"
        transparent
        onRequestClose={() => setShowAddFavorite(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.addFavoriteContent}>
            <Text style={styles.addFavoriteTitle}>Ajouter un favori</Text>

            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Titre</Text>
              <TextInput
                style={styles.input}
                placeholder="Mon site"
                placeholderTextColor={colors.textMuted}
                value={newFavoriteTitle}
                onChangeText={setNewFavoriteTitle}
              />
            </View>

            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>URL</Text>
              <TextInput
                style={styles.input}
                placeholder="https://example.com"
                placeholderTextColor={colors.textMuted}
                value={newFavoriteUrl}
                onChangeText={setNewFavoriteUrl}
                autoCapitalize="none"
                keyboardType="url"
              />
            </View>

            <View style={styles.addFavoriteActions}>
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() => setShowAddFavorite(false)}
              >
                <Text style={styles.cancelText}>Annuler</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.saveButton}
                onPress={handleAddFavorite}
              >
                <Text style={styles.saveText}>Ajouter</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: colors.surface,
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  accessButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.backgroundTertiary,
    borderRadius: borderRadius.full,
  },
  accessText: {
    color: colors.text,
    fontSize: typography.fontSize.sm,
  },

  // Modal
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: colors.surface,
    borderTopLeftRadius: borderRadius.xl,
    borderTopRightRadius: borderRadius.xl,
    maxHeight: '70%',
    paddingBottom: spacing.xxl,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  modalTitle: {
    color: colors.text,
    fontSize: typography.fontSize.xl,
    fontWeight: 'bold',
  },
  modalActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  addButton: {
    padding: spacing.xs,
  },
  clearButton: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    backgroundColor: colors.error + '20',
    borderRadius: borderRadius.full,
  },
  clearText: {
    color: colors.error,
    fontSize: typography.fontSize.sm,
  },
  list: {
    padding: spacing.lg,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  itemIcon: {
    width: 40,
    height: 40,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  itemInfo: {
    flex: 1,
  },
  itemTitle: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: '500',
  },
  itemUrl: {
    color: colors.textMuted,
    fontSize: typography.fontSize.sm,
    marginTop: 2,
  },
  itemTime: {
    color: colors.textMuted,
    fontSize: typography.fontSize.xs,
  },
  removeButton: {
    padding: spacing.sm,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: spacing.xxl,
  },
  emptyText: {
    color: colors.textMuted,
    fontSize: typography.fontSize.md,
    marginTop: spacing.md,
  },

  // Add Favorite Modal
  addFavoriteContent: {
    backgroundColor: colors.surface,
    margin: spacing.lg,
    borderRadius: borderRadius.xl,
    padding: spacing.lg,
  },
  addFavoriteTitle: {
    color: colors.text,
    fontSize: typography.fontSize.xl,
    fontWeight: 'bold',
    marginBottom: spacing.lg,
    textAlign: 'center',
  },
  inputContainer: {
    marginBottom: spacing.md,
  },
  inputLabel: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.sm,
    marginBottom: spacing.xs,
  },
  input: {
    backgroundColor: colors.backgroundTertiary,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    color: colors.text,
    fontSize: typography.fontSize.md,
  },
  addFavoriteActions: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.lg,
  },
  cancelButton: {
    flex: 1,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
  },
  cancelText: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.md,
  },
  saveButton: {
    flex: 1,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    backgroundColor: colors.primary,
    alignItems: 'center',
  },
  saveText: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: 'bold',
  },
});
