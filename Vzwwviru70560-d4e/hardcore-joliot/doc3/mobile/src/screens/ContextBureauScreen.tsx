/**
 * CHE·NU™ — Mobile Context Bureau Screen
 */

import React, { useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NavContext } from '../context/NavContext';
import { colors } from '../styles/colors';
import { SPHERE_CONFIG } from '../../../shared/constants';

export function ContextBureauScreen() {
  const navigation = useNavigation();
  const { state, send } = useContext(NavContext);
  const ctx = state.context;
  const { selection, prefilled, data, contextSummary } = ctx;

  const currentIdentity = selection.identityId
    ? data.identities.find((i) => i.id === selection.identityId)
    : null;

  const availableSpheres = selection.identityId
    ? data.spheresByIdentity[selection.identityId] ?? []
    : [];

  const currentSphere = selection.sphereId
    ? availableSpheres.find((s) => s.id === selection.sphereId)
    : null;

  const isContextValid = !!selection.identityId && !!selection.sphereId;

  const handleConfirm = () => {
    send({ type: 'CONFIRM_CONTEXT' });
    navigation.navigate('ActionBureau' as never);
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.subtitle}>Sur quoi je travaille?</Text>

      {/* Identity Selection */}
      <View style={styles.section}>
        <Text style={styles.sectionLabel}>IDENTITÉ</Text>
        {currentIdentity ? (
          <View style={styles.selectedRow}>
            <Text style={styles.selectedIcon}>
              {currentIdentity.type === 'personal' ? '🏠' : currentIdentity.type === 'business' ? '💼' : '🏛️'}
            </Text>
            <Text style={styles.selectedText}>{currentIdentity.name}</Text>
            {prefilled.identity && <View style={styles.autoBadge}><Text style={styles.autoBadgeText}>Auto</Text></View>}
            <TouchableOpacity
              style={styles.changeBtn}
              onPress={() => send({ type: 'SELECT_IDENTITY', identityId: '' })}
            >
              <Text style={styles.changeBtnText}>Changer</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.optionsList}>
            {data.identities.map((identity) => (
              <TouchableOpacity
                key={identity.id}
                style={styles.optionBtn}
                onPress={() => send({ type: 'SELECT_IDENTITY', identityId: identity.id })}
              >
                <Text style={styles.optionIcon}>
                  {identity.type === 'personal' ? '🏠' : identity.type === 'business' ? '💼' : '🏛️'}
                </Text>
                <Text style={styles.optionText}>{identity.name}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </View>

      {/* Sphere Selection */}
      {selection.identityId && (
        <View style={styles.section}>
          <Text style={styles.sectionLabel}>SPHÈRE</Text>
          {currentSphere ? (
            <View style={styles.selectedRow}>
              <Text style={styles.selectedIcon}>{SPHERE_CONFIG[currentSphere.key]?.emoji}</Text>
              <Text style={styles.selectedText}>{currentSphere.label}</Text>
              {prefilled.sphere && <View style={styles.autoBadge}><Text style={styles.autoBadgeText}>Auto</Text></View>}
              <TouchableOpacity
                style={styles.changeBtn}
                onPress={() => send({ type: 'SELECT_SPHERE', sphereId: '' })}
              >
                <Text style={styles.changeBtnText}>Changer</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.sphereGrid}>
              {availableSpheres.map((sphere) => {
                const config = SPHERE_CONFIG[sphere.key];
                return (
                  <TouchableOpacity
                    key={sphere.id}
                    style={[styles.sphereBtn, { borderLeftColor: config?.color }]}
                    onPress={() => send({ type: 'SELECT_SPHERE', sphereId: sphere.id })}
                  >
                    <Text style={styles.sphereEmoji}>{config?.emoji}</Text>
                    <Text style={styles.sphereLabel}>{sphere.label}</Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          )}
        </View>
      )}

      {/* Context Summary */}
      {isContextValid && (
        <View style={styles.summarySection}>
          <Text style={styles.summaryTitle}>Résumé</Text>
          <View style={styles.summaryGrid}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>{contextSummary.urgentTasks}</Text>
              <Text style={styles.summaryLabel}>Tâches urgentes</Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>{contextSummary.upcomingMeetings}</Text>
              <Text style={styles.summaryLabel}>Réunions proches</Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>{contextSummary.alerts}</Text>
              <Text style={styles.summaryLabel}>Alertes</Text>
            </View>
          </View>
        </View>
      )}

      {/* Confirm Button */}
      <View style={styles.actions}>
        {isContextValid ? (
          <TouchableOpacity style={styles.confirmBtn} onPress={handleConfirm}>
            <Text style={styles.confirmBtnText}>Aller travailler →</Text>
          </TouchableOpacity>
        ) : (
          <Text style={styles.hint}>Sélectionnez une identité et une sphère pour continuer</Text>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bgPrimary,
    padding: 16,
  },
  subtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 24,
  },
  section: {
    backgroundColor: colors.bgSurface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  sectionLabel: {
    fontSize: 11,
    color: colors.textSecondary,
    marginBottom: 12,
    letterSpacing: 1,
  },
  selectedRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  selectedIcon: {
    fontSize: 20,
    marginRight: 8,
  },
  selectedText: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  autoBadge: {
    backgroundColor: colors.cenoteTurquoise,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    marginRight: 8,
  },
  autoBadgeText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#000',
  },
  changeBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 6,
  },
  changeBtnText: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  optionsList: {
    gap: 8,
  },
  optionBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: colors.bgElevated,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
  },
  optionIcon: {
    fontSize: 18,
    marginRight: 12,
  },
  optionText: {
    fontSize: 14,
    color: colors.textPrimary,
  },
  sphereGrid: {
    gap: 8,
  },
  sphereBtn: {
    padding: 12,
    backgroundColor: colors.bgElevated,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    borderLeftWidth: 3,
  },
  sphereEmoji: {
    fontSize: 24,
    marginBottom: 4,
  },
  sphereLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  summarySection: {
    backgroundColor: colors.shadowMoss,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: colors.jungleEmerald,
  },
  summaryTitle: {
    fontSize: 14,
    color: colors.cenoteTurquoise,
    marginBottom: 16,
  },
  summaryGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.textPrimary,
  },
  summaryLabel: {
    fontSize: 11,
    color: colors.textSecondary,
  },
  actions: {
    marginTop: 24,
    alignItems: 'center',
  },
  confirmBtn: {
    backgroundColor: colors.cenoteTurquoise,
    paddingVertical: 16,
    paddingHorizontal: 48,
    borderRadius: 12,
  },
  confirmBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
  },
  hint: {
    color: colors.textMuted,
    textAlign: 'center',
  },
});
