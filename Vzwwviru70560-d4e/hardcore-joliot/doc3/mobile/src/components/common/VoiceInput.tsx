// CHE·NU Mobile - Voice Input Component
// Voice message recording for agents

import React, { useState, useRef, useEffect } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet, Animated, Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography } from '../../theme';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface VoiceInputProps {
  onVoiceMessage: (audioData: string, duration: number) => void;
  onTranscript?: (text: string) => void;
  isActive?: boolean;
}

export default function VoiceInput({ onVoiceMessage, onTranscript, isActive = false }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const [amplitude, setAmplitude] = useState(0);
  
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const waveAnim = useRef(new Animated.Value(0)).current;

  // Simulate recording
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRecording) {
      interval = setInterval(() => {
        setDuration(d => d + 1);
        // Simulate amplitude changes
        setAmplitude(Math.random() * 0.8 + 0.2);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  // Pulse animation when recording
  useEffect(() => {
    if (isRecording) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, { toValue: 1.3, duration: 500, useNativeDriver: true }),
          Animated.timing(pulseAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isRecording]);

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartRecording = () => {
    setIsRecording(true);
    setDuration(0);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    // Simulate sending voice data
    onVoiceMessage('audio_data_placeholder', duration);
    // Simulate transcript
    if (onTranscript) {
      setTimeout(() => {
        onTranscript('Message vocal transcrit par l\'IA');
      }, 1000);
    }
    setDuration(0);
  };

  const handleCancelRecording = () => {
    setIsRecording(false);
    setDuration(0);
  };

  if (!isRecording) {
    return (
      <TouchableOpacity
        style={styles.micButton}
        onPress={handleStartRecording}
        activeOpacity={0.7}
      >
        <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.micGradient}>
          <Ionicons name="mic" size={24} color={colors.text} />
        </LinearGradient>
      </TouchableOpacity>
    );
  }

  return (
    <View style={styles.recordingContainer}>
      {/* Cancel Button */}
      <TouchableOpacity style={styles.cancelButton} onPress={handleCancelRecording}>
        <Ionicons name="trash-outline" size={22} color={colors.error} />
      </TouchableOpacity>

      {/* Waveform Visualization */}
      <View style={styles.waveformContainer}>
        {[...Array(15)].map((_, i) => (
          <Animated.View
            key={i}
            style={[
              styles.waveBar,
              {
                height: 10 + Math.random() * amplitude * 30,
                backgroundColor: colors.primary,
                opacity: 0.5 + amplitude * 0.5,
              },
            ]}
          />
        ))}
      </View>

      {/* Duration */}
      <View style={styles.durationContainer}>
        <View style={styles.recordingDot} />
        <Text style={styles.durationText}>{formatDuration(duration)}</Text>
      </View>

      {/* Stop Button */}
      <TouchableOpacity onPress={handleStopRecording}>
        <Animated.View style={[styles.stopButton, { transform: [{ scale: pulseAnim }] }]}>
          <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.stopGradient}>
            <Ionicons name="send" size={20} color={colors.text} />
          </LinearGradient>
        </Animated.View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  micButton: {
    borderRadius: borderRadius.full,
    overflow: 'hidden',
  },
  micGradient: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  recordingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.full,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    borderWidth: 2,
    borderColor: colors.error,
  },
  cancelButton: {
    padding: spacing.xs,
  },
  waveformContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 3,
    height: 40,
  },
  waveBar: {
    width: 3,
    borderRadius: 2,
  },
  durationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  recordingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.error,
  },
  durationText: {
    color: colors.text,
    fontSize: typography.fontSize.sm,
    fontWeight: '600',
    minWidth: 40,
  },
  stopButton: {
    borderRadius: borderRadius.full,
    overflow: 'hidden',
  },
  stopGradient: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
