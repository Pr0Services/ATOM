/**
 * CHE·NU™ — Mobile Workspace Screen
 */

import React, { useContext, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NavContext } from '../context/NavContext';
import { colors } from '../styles/colors';

type WorkspaceMode = 'draft' | 'staging' | 'review';

export function WorkspaceScreen() {
  const navigation = useNavigation();
  const { state, send } = useContext(NavContext);
  const ctx = state.context;
  const { selection, data, diamond } = ctx;

  const [mode, setMode] = useState<WorkspaceMode>('draft');
  const [content, setContent] = useState('');

  const keyIS = selection.identityId && selection.sphereId
    ? `${selection.identityId}:${selection.sphereId}`
    : null;

  const workspaces = keyIS ? data.workspacesByIdentitySphere[keyIS] ?? [] : [];
  const currentWorkspace = selection.workspaceId
    ? workspaces.find((w) => w.id === selection.workspaceId)
    : null;

  const workspaceName = currentWorkspace?.name ?? 'Nouveau Workspace';

  const handleBack = () => {
    send({ type: 'BACK_TO_ACTIONS' });
    navigation.navigate('ActionBureau' as never);
  };

  const handleChangeContext = () => {
    send({ type: 'CHANGE_CONTEXT' });
    navigation.navigate('ContextBureau' as never);
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <Text style={styles.workspaceName}>{workspaceName}</Text>
          <View style={styles.lockedBadge}>
            <Text style={styles.lockedText}>🔒 Verrouillé</Text>
          </View>
        </View>
        <Text style={styles.contextLabel}>{diamond.contextLabel}</Text>
      </View>

      {/* Mode Tabs */}
      <View style={styles.modeTabs}>
        {(['draft', 'staging', 'review'] as WorkspaceMode[]).map((m) => (
          <TouchableOpacity
            key={m}
            style={[styles.modeTab, mode === m && styles.modeTabActive]}
            onPress={() => setMode(m)}
          >
            <Text style={[styles.modeTabText, mode === m && styles.modeTabTextActive]}>
              {m === 'draft' && '📝 Draft'}
              {m === 'staging' && '🔄 Staging'}
              {m === 'review' && '✅ Review'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Canvas */}
      <View style={styles.canvas}>
        {mode === 'draft' && (
          <TextInput
            style={styles.editor}
            multiline
            placeholder="Commencez à écrire..."
            placeholderTextColor={colors.textMuted}
            value={content}
            onChangeText={setContent}
          />
        )}

        {mode === 'staging' && (
          <View style={styles.stagingView}>
            <Text style={styles.stagingTitle}>Aperçu</Text>
            <View style={styles.preview}>
              <Text style={styles.previewText}>
                {content || 'Aucun contenu à prévisualiser'}
              </Text>
            </View>
            <View style={styles.stagingActions}>
              <TouchableOpacity style={styles.stagingBtn}>
                <Text style={styles.stagingBtnText}>Soumettre à review</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.stagingBtn, styles.stagingBtnSecondary]}>
                <Text style={styles.stagingBtnText}>Envoyer à agent</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {mode === 'review' && (
          <View style={styles.reviewView}>
            <Text style={styles.reviewTitle}>En attente d'approbation</Text>
            <View style={styles.preview}>
              <Text style={styles.previewText}>
                {content || 'Aucun contenu soumis'}
              </Text>
            </View>
            <View style={styles.reviewActions}>
              <TouchableOpacity style={[styles.reviewBtn, styles.approveBtn]}>
                <Text style={styles.reviewBtnText}>✓ Approuver</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.reviewBtn, styles.rejectBtn]}>
                <Text style={styles.reviewBtnText}>✗ Rejeter</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.reviewBtn, styles.reviseBtn]}>
                <Text style={styles.reviewBtnText}>↩ Réviser</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>

      {/* Toolbar */}
      <View style={styles.toolbar}>
        <TouchableOpacity style={styles.toolbarBtn}>
          <Text style={styles.toolbarBtnText}>📋 Diff</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.toolbarBtn}>
          <Text style={styles.toolbarBtnText}>🕐 Historique</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.toolbarBtn}>
          <Text style={styles.toolbarBtnText}>🤖 Agent</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.toolbarBtn, styles.saveBtn]}>
          <Text style={styles.saveBtnText}>💾 Sauvegarder</Text>
        </TouchableOpacity>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <TouchableOpacity onPress={handleBack}>
          <Text style={styles.footerLink}>← Retour aux actions</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={handleChangeContext}>
          <Text style={styles.footerLink}>Changer contexte</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bgPrimary,
  },
  header: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerTop: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  workspaceName: {
    flex: 1,
    fontSize: 18,
    fontWeight: '700',
    color: colors.textPrimary,
  },
  lockedBadge: {
    backgroundColor: colors.warning,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  lockedText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#000',
  },
  contextLabel: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  modeTabs: {
    flexDirection: 'row',
    padding: 16,
    gap: 8,
  },
  modeTab: {
    flex: 1,
    paddingVertical: 10,
    alignItems: 'center',
    backgroundColor: colors.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
  },
  modeTabActive: {
    backgroundColor: colors.cenoteTurquoise,
    borderColor: colors.cenoteTurquoise,
  },
  modeTabText: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  modeTabTextActive: {
    color: '#000',
    fontWeight: '600',
  },
  canvas: {
    flex: 1,
    margin: 16,
    backgroundColor: colors.bgSurface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    padding: 16,
  },
  editor: {
    flex: 1,
    color: colors.textPrimary,
    fontSize: 16,
    textAlignVertical: 'top',
  },
  stagingView: {
    flex: 1,
  },
  stagingTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 12,
  },
  preview: {
    flex: 1,
    backgroundColor: colors.bgElevated,
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  previewText: {
    color: colors.textSecondary,
  },
  stagingActions: {
    gap: 8,
  },
  stagingBtn: {
    backgroundColor: colors.bgElevated,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  stagingBtnSecondary: {
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: 'transparent',
  },
  stagingBtnText: {
    color: colors.textPrimary,
    fontWeight: '600',
  },
  reviewView: {
    flex: 1,
  },
  reviewTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 12,
  },
  reviewActions: {
    flexDirection: 'row',
    gap: 8,
  },
  reviewBtn: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  approveBtn: {
    backgroundColor: colors.success,
  },
  rejectBtn: {
    backgroundColor: colors.error,
  },
  reviseBtn: {
    backgroundColor: colors.bgElevated,
  },
  reviewBtnText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 12,
  },
  toolbar: {
    flexDirection: 'row',
    padding: 12,
    gap: 8,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  toolbarBtn: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: colors.bgSurface,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: colors.border,
  },
  toolbarBtnText: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  saveBtn: {
    marginLeft: 'auto',
    backgroundColor: colors.cenoteTurquoise,
    borderColor: colors.cenoteTurquoise,
  },
  saveBtnText: {
    fontSize: 12,
    color: '#000',
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  footerLink: {
    color: colors.textSecondary,
    fontSize: 14,
  },
});
