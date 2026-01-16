// CHE·NU Mobile - Agent Call Screen
// Full screen voice call interface

import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography } from '../theme';
import { useOverlay } from '../providers/OverlayProvider';

export default function AgentCallScreen() {
  const navigation = useNavigation();
  const route = useRoute<any>();
  const { agentId, agentName, agentColor = colors.primary } = route.params;
  const { call, endCall, toggleMute, toggleSpeaker } = useOverlay();
  
  const [callState, setCallState] = useState<'connecting' | 'connected' | 'ended'>('connecting');
  const [duration, setDuration] = useState(0);
  
  const pulseAnim = React.useRef(new Animated.Value(1)).current;

  useEffect(() => {
    const timer = setTimeout(() => setCallState('connected'), 2000);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (callState === 'connected') {
      interval = setInterval(() => setDuration(d => d + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [callState]);

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.2, duration: 1000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleEndCall = () => {
    setCallState('ended');
    endCall();
    setTimeout(() => navigation.goBack(), 500);
  };

  const handleMinimize = () => {
    navigation.goBack();
  };

  const isNova = agentId === 'nova';

  return (
    <LinearGradient colors={[colors.background, colors.backgroundSecondary]} style={styles.container}>
      <View style={styles.safeTop} />

      {/* Minimize Button */}
      <TouchableOpacity style={styles.minimizeButton} onPress={handleMinimize}>
        <Ionicons name="chevron-down" size={28} color={colors.text} />
      </TouchableOpacity>

      {/* Agent Info */}
      <View style={styles.agentSection}>
        <Animated.View style={[styles.avatarContainer, { transform: [{ scale: callState === 'connecting' ? pulseAnim : 1 }] }]}>
          <LinearGradient colors={[agentColor, colors.primaryDark]} style={styles.avatar}>
            <Text style={styles.avatarText}>{isNova ? 'N' : agentName.charAt(0)}</Text>
          </LinearGradient>
        </Animated.View>
        
        <Text style={styles.agentName}>{agentName}</Text>
        <Text style={styles.agentRole}>{isNova ? 'Guide CHE·NU' : 'Agent CHE·NU'}</Text>
        
        <View style={styles.statusContainer}>
          {callState === 'connecting' && (
            <>
              <View style={styles.statusDot} />
              <Text style={styles.statusText}>Connexion en cours...</Text>
            </>
          )}
          {callState === 'connected' && (
            <>
              <View style={[styles.statusDot, { backgroundColor: colors.success }]} />
              <Text style={styles.statusText}>{formatDuration(duration)}</Text>
            </>
          )}
          {callState === 'ended' && (
            <Text style={styles.statusText}>Appel terminé</Text>
          )}
        </View>
      </View>

      {/* Waveform */}
      <View style={styles.waveformContainer}>
        {[...Array(20)].map((_, i) => (
          <Animated.View 
            key={i} 
            style={[
              styles.waveBar,
              { 
                height: callState === 'connected' ? Math.random() * 40 + 10 : 10,
                backgroundColor: agentColor,
                opacity: callState === 'connected' ? 0.6 : 0.2,
              }
            ]} 
          />
        ))}
      </View>

      {/* Controls */}
      <View style={styles.controls}>
        <TouchableOpacity 
          style={[styles.controlButton, call.isMuted && styles.controlButtonActive]}
          onPress={toggleMute}
        >
          <Ionicons name={call.isMuted ? 'mic-off' : 'mic'} size={28} color={colors.text} />
          <Text style={styles.controlLabel}>Muet</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.controlButton, call.isSpeaker && styles.controlButtonActive]}
          onPress={toggleSpeaker}
        >
          <Ionicons name={call.isSpeaker ? 'volume-high' : 'volume-medium'} size={28} color={colors.text} />
          <Text style={styles.controlLabel}>Haut-parleur</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.controlButton}
          onPress={() => (navigation as any).navigate('Conversation', { agentId, agentName })}
        >
          <Ionicons name="chatbubble" size={28} color={colors.text} />
          <Text style={styles.controlLabel}>Chat</Text>
        </TouchableOpacity>
      </View>

      {/* End Call */}
      <TouchableOpacity style={styles.endCallButton} onPress={handleEndCall}>
        <LinearGradient colors={[colors.error, '#B91C1C']} style={styles.endCallGradient}>
          <Ionicons name="call" size={32} color={colors.text} style={{ transform: [{ rotate: '135deg' }] }} />
        </LinearGradient>
      </TouchableOpacity>

      <Text style={styles.hint}>
        {callState === 'connected' ? 'Conversation vocale active' : 'En attente...'}
      </Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeTop: { height: 50 },
  minimizeButton: { position: 'absolute', top: 60, left: spacing.lg, zIndex: 10, padding: spacing.sm },
  agentSection: { alignItems: 'center', marginTop: spacing.xxl },
  avatarContainer: { position: 'relative' },
  avatar: {
    width: 120, height: 120, borderRadius: 60,
    justifyContent: 'center', alignItems: 'center',
    borderWidth: 4, borderColor: colors.surface,
  },
  avatarText: { color: colors.text, fontSize: 48, fontWeight: 'bold' },
  agentName: { color: colors.text, fontSize: typography.fontSize.xxl, fontWeight: 'bold', marginTop: spacing.lg },
  agentRole: { color: colors.textSecondary, fontSize: typography.fontSize.md, marginTop: spacing.xs },
  statusContainer: { flexDirection: 'row', alignItems: 'center', marginTop: spacing.lg, gap: spacing.sm },
  statusDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.warning },
  statusText: { color: colors.textSecondary, fontSize: typography.fontSize.lg },
  waveformContainer: {
    flexDirection: 'row', justifyContent: 'center', alignItems: 'center',
    height: 80, marginVertical: spacing.xxl, gap: 4, paddingHorizontal: spacing.lg,
  },
  waveBar: { width: 4, borderRadius: 2 },
  controls: {
    flexDirection: 'row', justifyContent: 'center', gap: spacing.xxl,
    marginBottom: spacing.xxl,
  },
  controlButton: {
    alignItems: 'center', padding: spacing.md,
    backgroundColor: colors.surface, borderRadius: borderRadius.lg, minWidth: 80,
  },
  controlButtonActive: { backgroundColor: colors.primary },
  controlLabel: { color: colors.textSecondary, fontSize: typography.fontSize.sm, marginTop: spacing.xs },
  endCallButton: { alignSelf: 'center', marginBottom: spacing.lg },
  endCallGradient: {
    width: 72, height: 72, borderRadius: 36,
    justifyContent: 'center', alignItems: 'center',
    shadowColor: colors.error, shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4, shadowRadius: 8, elevation: 8,
  },
  hint: { color: colors.textMuted, fontSize: typography.fontSize.sm, textAlign: 'center', marginBottom: spacing.xxl },
});
