import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useNavigation } from '@react-navigation/native';
import { useSpheresStore, useUIStore } from '../store';
import { lightTheme, darkTheme, spacing, borderRadius, shadows } from '../theme';

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - spacing.lg * 2 - spacing.md) / 2;

const SpheresScreen = () => {
  const navigation = useNavigation<any>();
  const { spheres, currentSphere, setCurrentSphere } = useSpheresStore();
  const { theme } = useUIStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;

  return (
    <ScrollView style={[styles.container, { backgroundColor: themeColors.background }]}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: themeColors.text }]}>Sphères</Text>
        <Text style={[styles.subtitle, { color: themeColors.textSecondary }]}>
          11 espaces de vie pour organiser votre univers
        </Text>
      </View>
      
      <View style={styles.grid}>
        {spheres.map((sphere) => (
          <TouchableOpacity
            key={sphere.id}
            style={[styles.card, currentSphere === sphere.id && styles.cardActive]}
            onPress={() => {
              setCurrentSphere(sphere.id);
              navigation.navigate('SphereDetail', { sphereId: sphere.id });
            }}
          >
            <LinearGradient
              colors={sphere.gradient}
              style={styles.cardGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              <Text style={styles.cardIcon}>{sphere.icon}</Text>
              <Text style={styles.cardName}>{sphere.nameFr}</Text>
              <Text style={styles.cardDescription} numberOfLines={2}>
                {sphere.description}
              </Text>
              {!sphere.isActive && (
                <View style={styles.inactiveBadge}>
                  <Text style={styles.inactiveBadgeText}>Désactivée</Text>
                </View>
              )}
            </LinearGradient>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { padding: spacing.lg, paddingTop: 60 },
  title: { fontSize: 32, fontWeight: '700' },
  subtitle: { fontSize: 14, marginTop: spacing.xs },
  grid: { flexDirection: 'row', flexWrap: 'wrap', padding: spacing.lg, paddingTop: 0, gap: spacing.md },
  card: { width: CARD_WIDTH, borderRadius: borderRadius.xl, overflow: 'hidden', ...shadows.md },
  cardActive: { borderWidth: 2, borderColor: '#FFFFFF' },
  cardGradient: { padding: spacing.md, minHeight: 140 },
  cardIcon: { fontSize: 32, marginBottom: spacing.sm },
  cardName: { fontSize: 16, fontWeight: '600', color: '#FFFFFF', marginBottom: spacing.xs },
  cardDescription: { fontSize: 12, color: 'rgba(255,255,255,0.8)' },
  inactiveBadge: { position: 'absolute', top: 8, right: 8, backgroundColor: 'rgba(0,0,0,0.3)', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 4 },
  inactiveBadgeText: { color: '#FFFFFF', fontSize: 10 },
});

export default SpheresScreen;
