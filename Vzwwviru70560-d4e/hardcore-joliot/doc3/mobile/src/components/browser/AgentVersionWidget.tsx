// CHE·NU Mobile - Agent Version Widget
// Floating widget to review agent modifications on documents

import React, { useState } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet, ScrollView,
  Animated, Dimensions, Modal,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface Version {
  id: string;
  agentId: string;
  agentName: string;
  agentColor: string;
  timestamp: string;
  changes: Change[];
  status: 'pending' | 'approved' | 'rejected';
}

interface Change {
  id: string;
  type: 'add' | 'remove' | 'modify';
  location: string;
  original?: string;
  proposed: string;
}

interface AgentVersionWidgetProps {
  documentId: string;
  versions: Version[];
  onApprove: (versionId: string) => void;
  onReject: (versionId: string) => void;
  onApproveChange: (versionId: string, changeId: string) => void;
  onRejectChange: (versionId: string, changeId: string) => void;
}

export default function AgentVersionWidget({
  documentId,
  versions,
  onApprove,
  onReject,
  onApproveChange,
  onRejectChange,
}: AgentVersionWidgetProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState<Version | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);

  const pendingVersions = versions.filter(v => v.status === 'pending');
  const pendingCount = pendingVersions.length;

  if (pendingCount === 0) return null;

  const handleVersionPress = (version: Version) => {
    setSelectedVersion(version);
    setShowDetailModal(true);
  };

  const getChangeIcon = (type: Change['type']) => {
    switch (type) {
      case 'add': return 'add-circle';
      case 'remove': return 'remove-circle';
      case 'modify': return 'create';
    }
  };

  const getChangeColor = (type: Change['type']) => {
    switch (type) {
      case 'add': return colors.success;
      case 'remove': return colors.error;
      case 'modify': return colors.warning;
    }
  };

  return (
    <>
      {/* Floating Widget Button */}
      <TouchableOpacity
        style={styles.floatingButton}
        onPress={() => setIsExpanded(!isExpanded)}
        activeOpacity={0.9}
      >
        <LinearGradient
          colors={[colors.warning, colors.accent]}
          style={styles.floatingGradient}
        >
          <Ionicons name="git-compare" size={24} color={colors.text} />
          {pendingCount > 0 && (
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{pendingCount}</Text>
            </View>
          )}
        </LinearGradient>
      </TouchableOpacity>

      {/* Expanded Panel */}
      {isExpanded && (
        <View style={styles.expandedPanel}>
          <View style={styles.panelHeader}>
            <Text style={styles.panelTitle}>Modifications en attente</Text>
            <TouchableOpacity onPress={() => setIsExpanded(false)}>
              <Ionicons name="close" size={24} color={colors.textMuted} />
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.versionsList}>
            {pendingVersions.map(version => (
              <TouchableOpacity
                key={version.id}
                style={styles.versionItem}
                onPress={() => handleVersionPress(version)}
              >
                <View style={[styles.versionAvatar, { backgroundColor: version.agentColor }]}>
                  <Text style={styles.versionAvatarText}>{version.agentName.charAt(0)}</Text>
                </View>
                <View style={styles.versionInfo}>
                  <Text style={styles.versionAgent}>{version.agentName}</Text>
                  <Text style={styles.versionMeta}>
                    {version.changes.length} modification{version.changes.length > 1 ? 's' : ''} • {version.timestamp}
                  </Text>
                </View>
                <View style={styles.versionActions}>
                  <TouchableOpacity
                    style={styles.actionButtonSmall}
                    onPress={() => onApprove(version.id)}
                  >
                    <Ionicons name="checkmark" size={18} color={colors.success} />
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={styles.actionButtonSmall}
                    onPress={() => onReject(version.id)}
                  >
                    <Ionicons name="close" size={18} color={colors.error} />
                  </TouchableOpacity>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {pendingVersions.length > 1 && (
            <View style={styles.panelFooter}>
              <TouchableOpacity style={styles.approveAllButton}>
                <Text style={styles.approveAllText}>Approuver tout</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      )}

      {/* Detail Modal */}
      <Modal
        visible={showDetailModal}
        animationType="slide"
        transparent
        onRequestClose={() => setShowDetailModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            {/* Modal Header */}
            <View style={styles.modalHeader}>
              <View style={styles.modalHeaderInfo}>
                {selectedVersion && (
                  <View style={[styles.modalAvatar, { backgroundColor: selectedVersion.agentColor }]}>
                    <Text style={styles.modalAvatarText}>{selectedVersion.agentName.charAt(0)}</Text>
                  </View>
                )}
                <View>
                  <Text style={styles.modalTitle}>{selectedVersion?.agentName}</Text>
                  <Text style={styles.modalSubtitle}>{selectedVersion?.timestamp}</Text>
                </View>
              </View>
              <TouchableOpacity onPress={() => setShowDetailModal(false)}>
                <Ionicons name="close" size={28} color={colors.textMuted} />
              </TouchableOpacity>
            </View>

            {/* Changes List */}
            <ScrollView style={styles.changesList}>
              <Text style={styles.changesTitle}>
                {selectedVersion?.changes.length} modification{(selectedVersion?.changes.length || 0) > 1 ? 's' : ''}
              </Text>

              {selectedVersion?.changes.map(change => (
                <View key={change.id} style={styles.changeItem}>
                  <View style={styles.changeHeader}>
                    <View style={styles.changeType}>
                      <Ionicons
                        name={getChangeIcon(change.type)}
                        size={20}
                        color={getChangeColor(change.type)}
                      />
                      <Text style={[styles.changeTypeText, { color: getChangeColor(change.type) }]}>
                        {change.type === 'add' ? 'Ajout' : change.type === 'remove' ? 'Suppression' : 'Modification'}
                      </Text>
                    </View>
                    <Text style={styles.changeLocation}>{change.location}</Text>
                  </View>

                  {change.original && (
                    <View style={styles.changeOriginal}>
                      <Text style={styles.changeLabel}>Original:</Text>
                      <Text style={styles.changeText}>{change.original}</Text>
                    </View>
                  )}

                  <View style={styles.changeProposed}>
                    <Text style={styles.changeLabel}>Proposé:</Text>
                    <Text style={styles.changeText}>{change.proposed}</Text>
                  </View>

                  <View style={styles.changeActions}>
                    <TouchableOpacity
                      style={[styles.changeActionButton, styles.changeApprove]}
                      onPress={() => onApproveChange(selectedVersion.id, change.id)}
                    >
                      <Ionicons name="checkmark" size={16} color={colors.text} />
                      <Text style={styles.changeActionText}>Approuver</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.changeActionButton, styles.changeReject]}
                      onPress={() => onRejectChange(selectedVersion.id, change.id)}
                    >
                      <Ionicons name="close" size={16} color={colors.text} />
                      <Text style={styles.changeActionText}>Rejeter</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ))}
            </ScrollView>

            {/* Modal Footer */}
            <View style={styles.modalFooter}>
              <TouchableOpacity
                style={styles.rejectAllButton}
                onPress={() => {
                  if (selectedVersion) onReject(selectedVersion.id);
                  setShowDetailModal(false);
                }}
              >
                <Text style={styles.rejectAllText}>Tout rejeter</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.approveAllModalButton}
                onPress={() => {
                  if (selectedVersion) onApprove(selectedVersion.id);
                  setShowDetailModal(false);
                }}
              >
                <LinearGradient
                  colors={[colors.success, '#059669']}
                  style={styles.approveAllGradient}
                >
                  <Ionicons name="checkmark-done" size={20} color={colors.text} />
                  <Text style={styles.approveAllModalText}>Tout approuver</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  // Floating Button
  floatingButton: {
    position: 'absolute',
    bottom: 100,
    right: spacing.md,
    zIndex: 100,
    borderRadius: 28,
    overflow: 'hidden',
    ...shadows.lg,
  },
  floatingGradient: {
    width: 56,
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badge: {
    position: 'absolute',
    top: -4,
    right: -4,
    backgroundColor: colors.error,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 4,
  },
  badgeText: {
    color: colors.text,
    fontSize: 11,
    fontWeight: 'bold',
  },

  // Expanded Panel
  expandedPanel: {
    position: 'absolute',
    bottom: 170,
    right: spacing.md,
    width: SCREEN_WIDTH - spacing.lg * 2,
    maxHeight: 300,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    ...shadows.lg,
  },
  panelHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  panelTitle: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: 'bold',
  },
  versionsList: {
    maxHeight: 200,
  },
  versionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  versionAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  versionAvatarText: {
    color: colors.text,
    fontSize: 14,
    fontWeight: 'bold',
  },
  versionInfo: {
    flex: 1,
    marginLeft: spacing.sm,
  },
  versionAgent: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: '600',
  },
  versionMeta: {
    color: colors.textMuted,
    fontSize: typography.fontSize.sm,
  },
  versionActions: {
    flexDirection: 'row',
    gap: spacing.xs,
  },
  actionButtonSmall: {
    padding: spacing.xs,
    backgroundColor: colors.backgroundTertiary,
    borderRadius: borderRadius.full,
  },
  panelFooter: {
    padding: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  approveAllButton: {
    backgroundColor: colors.success + '20',
    padding: spacing.sm,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
  },
  approveAllText: {
    color: colors.success,
    fontSize: typography.fontSize.md,
    fontWeight: '600',
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
    maxHeight: SCREEN_HEIGHT * 0.8,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  modalHeaderInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  modalAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalAvatarText: {
    color: colors.text,
    fontSize: 20,
    fontWeight: 'bold',
  },
  modalTitle: {
    color: colors.text,
    fontSize: typography.fontSize.xl,
    fontWeight: 'bold',
  },
  modalSubtitle: {
    color: colors.textMuted,
    fontSize: typography.fontSize.sm,
  },
  changesList: {
    padding: spacing.lg,
  },
  changesTitle: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.sm,
    marginBottom: spacing.md,
    textTransform: 'uppercase',
    fontWeight: '600',
  },
  changeItem: {
    backgroundColor: colors.backgroundTertiary,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  changeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  changeType: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  changeTypeText: {
    fontSize: typography.fontSize.sm,
    fontWeight: '600',
  },
  changeLocation: {
    color: colors.textMuted,
    fontSize: typography.fontSize.xs,
  },
  changeOriginal: {
    backgroundColor: colors.error + '15',
    padding: spacing.sm,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
  },
  changeProposed: {
    backgroundColor: colors.success + '15',
    padding: spacing.sm,
    borderRadius: borderRadius.md,
    marginBottom: spacing.md,
  },
  changeLabel: {
    color: colors.textMuted,
    fontSize: typography.fontSize.xs,
    marginBottom: 4,
  },
  changeText: {
    color: colors.text,
    fontSize: typography.fontSize.sm,
  },
  changeActions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  changeActionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    padding: spacing.sm,
    borderRadius: borderRadius.md,
  },
  changeApprove: {
    backgroundColor: colors.success,
  },
  changeReject: {
    backgroundColor: colors.error,
  },
  changeActionText: {
    color: colors.text,
    fontSize: typography.fontSize.sm,
    fontWeight: '600',
  },
  modalFooter: {
    flexDirection: 'row',
    gap: spacing.md,
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  rejectAllButton: {
    flex: 1,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    borderWidth: 1,
    borderColor: colors.error,
    alignItems: 'center',
  },
  rejectAllText: {
    color: colors.error,
    fontSize: typography.fontSize.md,
    fontWeight: '600',
  },
  approveAllModalButton: {
    flex: 1,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  approveAllGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    padding: spacing.md,
  },
  approveAllModalText: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: 'bold',
  },
});
