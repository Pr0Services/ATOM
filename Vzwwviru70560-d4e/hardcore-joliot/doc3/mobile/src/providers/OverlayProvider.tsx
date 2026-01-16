// CHE·NU Mobile - Overlay Provider
// Manages calls and notifications visible across ALL tabs

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';
import NovaFloatingButton from '../components/common/NovaFloatingButton';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

// Types
interface CallState {
  isActive: boolean;
  agentId: string | null;
  agentName: string;
  agentColor: string;
  duration: number;
  isMuted: boolean;
  isSpeaker: boolean;
  isMinimized: boolean;
}

interface Notification {
  id: string;
  agentId: string;
  agentName: string;
  message: string;
  timestamp: Date;
}

interface OverlayContextType {
  // Call
  call: CallState;
  startCall: (agentId: string, agentName: string, agentColor?: string) => void;
  endCall: () => void;
  toggleMute: () => void;
  toggleSpeaker: () => void;
  minimizeCall: () => void;
  maximizeCall: () => void;
  // Notifications
  notifications: Notification[];
  addNotification: (agentId: string, agentName: string, message: string) => void;
  dismissNotification: (id: string) => void;
  unreadCount: number;
  clearUnread: () => void;
}

const OverlayContext = createContext<OverlayContextType | null>(null);

export function useOverlay() {
  const context = useContext(OverlayContext);
  if (!context) throw new Error('useOverlay must be used within OverlayProvider');
  return context;
}

export function OverlayProvider({ children }: { children: ReactNode }) {
  // Call state
  const [call, setCall] = useState<CallState>({
    isActive: false,
    agentId: null,
    agentName: '',
    agentColor: colors.primary,
    duration: 0,
    isMuted: false,
    isSpeaker: false,
    isMinimized: false,
  });

  // Notifications state
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  // Call timer
  React.useEffect(() => {
    let interval: NodeJS.Timeout;
    if (call.isActive && !call.isMinimized) {
      interval = setInterval(() => {
        setCall(prev => ({ ...prev, duration: prev.duration + 1 }));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [call.isActive, call.isMinimized]);

  // Call functions
  const startCall = useCallback((agentId: string, agentName: string, agentColor = colors.primary) => {
    setCall({
      isActive: true,
      agentId,
      agentName,
      agentColor,
      duration: 0,
      isMuted: false,
      isSpeaker: false,
      isMinimized: false,
    });
  }, []);

  const endCall = useCallback(() => {
    setCall(prev => ({ ...prev, isActive: false, agentId: null, duration: 0 }));
  }, []);

  const toggleMute = useCallback(() => {
    setCall(prev => ({ ...prev, isMuted: !prev.isMuted }));
  }, []);

  const toggleSpeaker = useCallback(() => {
    setCall(prev => ({ ...prev, isSpeaker: !prev.isSpeaker }));
  }, []);

  const minimizeCall = useCallback(() => {
    setCall(prev => ({ ...prev, isMinimized: true }));
  }, []);

  const maximizeCall = useCallback(() => {
    setCall(prev => ({ ...prev, isMinimized: false }));
  }, []);

  // Notification functions
  const addNotification = useCallback((agentId: string, agentName: string, message: string) => {
    const notification: Notification = {
      id: Date.now().toString(),
      agentId,
      agentName,
      message,
      timestamp: new Date(),
    };
    setNotifications(prev => [notification, ...prev]);
    setUnreadCount(prev => prev + 1);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  }, []);

  const dismissNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const clearUnread = useCallback(() => {
    setUnreadCount(0);
  }, []);

  // Format duration
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <OverlayContext.Provider value={{
      call, startCall, endCall, toggleMute, toggleSpeaker, minimizeCall, maximizeCall,
      notifications, addNotification, dismissNotification, unreadCount, clearUnread,
    }}>
      {children}

      {/* CALL OVERLAY - Visible on all tabs */}
      {call.isActive && (
        call.isMinimized ? (
          // Minimized call bubble
          <TouchableOpacity style={styles.callBubble} onPress={maximizeCall}>
            <LinearGradient colors={[call.agentColor, colors.primaryDark]} style={styles.callBubbleGradient}>
              <Ionicons name="call" size={20} color={colors.text} />
              <Text style={styles.callBubbleTime}>{formatDuration(call.duration)}</Text>
            </LinearGradient>
          </TouchableOpacity>
        ) : (
          // Full call overlay
          <View style={styles.callOverlay}>
            <LinearGradient colors={[call.agentColor, colors.primaryDark]} style={styles.callOverlayGradient}>
              <View style={styles.callInfo}>
                <View style={styles.callAvatar}>
                  <Text style={styles.callAvatarText}>{call.agentName.charAt(0)}</Text>
                </View>
                <View style={styles.callDetails}>
                  <Text style={styles.callName}>{call.agentName}</Text>
                  <Text style={styles.callDuration}>{formatDuration(call.duration)}</Text>
                </View>
              </View>

              <View style={styles.callControls}>
                <TouchableOpacity 
                  style={[styles.callControl, call.isMuted && styles.callControlActive]}
                  onPress={toggleMute}
                >
                  <Ionicons name={call.isMuted ? 'mic-off' : 'mic'} size={20} color={colors.text} />
                </TouchableOpacity>
                <TouchableOpacity 
                  style={[styles.callControl, call.isSpeaker && styles.callControlActive]}
                  onPress={toggleSpeaker}
                >
                  <Ionicons name={call.isSpeaker ? 'volume-high' : 'volume-medium'} size={20} color={colors.text} />
                </TouchableOpacity>
                <TouchableOpacity style={styles.callControl} onPress={minimizeCall}>
                  <Ionicons name="chevron-down" size={20} color={colors.text} />
                </TouchableOpacity>
                <TouchableOpacity style={styles.callControlEnd} onPress={endCall}>
                  <Ionicons name="call" size={20} color={colors.text} style={{ transform: [{ rotate: '135deg' }] }} />
                </TouchableOpacity>
              </View>
            </LinearGradient>
          </View>
        )
      )}

      {/* NOTIFICATION TOASTS - Visible on all tabs */}
      <View style={styles.notificationsContainer}>
        {notifications.map((notification, index) => (
          <Animated.View key={notification.id} style={[styles.notificationToast, { top: index * 80 }]}>
            <View style={styles.notificationContent}>
              <View style={styles.notificationAvatar}>
                <Text style={styles.notificationAvatarText}>{notification.agentName.charAt(0)}</Text>
              </View>
              <View style={styles.notificationText}>
                <Text style={styles.notificationName}>{notification.agentName}</Text>
                <Text style={styles.notificationMessage} numberOfLines={2}>{notification.message}</Text>
              </View>
              <TouchableOpacity onPress={() => dismissNotification(notification.id)}>
                <Ionicons name="close" size={20} color={colors.textMuted} />
              </TouchableOpacity>
            </View>
          </Animated.View>
        ))}
      </View>

      {/* NOVA FLOATING BUTTON - Quick access to Nova from anywhere */}
      <NovaFloatingButton isVisible={!call.isActive} />
    </OverlayContext.Provider>
  );
}

const styles = StyleSheet.create({
  // Call Overlay (full)
  callOverlay: {
    position: 'absolute',
    top: 50,
    left: spacing.md,
    right: spacing.md,
    zIndex: 1000,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    ...shadows.lg,
  },
  callOverlayGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
  },
  callInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  callAvatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  callAvatarText: {
    color: colors.text,
    fontSize: 18,
    fontWeight: 'bold',
  },
  callDetails: {},
  callName: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: 'bold',
  },
  callDuration: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: typography.fontSize.sm,
  },
  callControls: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  callControl: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  callControlActive: {
    backgroundColor: 'rgba(255,255,255,0.4)',
  },
  callControlEnd: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: colors.error,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Call Bubble (minimized)
  callBubble: {
    position: 'absolute',
    top: 60,
    right: spacing.md,
    zIndex: 1000,
    borderRadius: borderRadius.full,
    overflow: 'hidden',
    ...shadows.lg,
  },
  callBubbleGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
  },
  callBubbleTime: {
    color: colors.text,
    fontSize: typography.fontSize.sm,
    fontWeight: 'bold',
  },

  // Notifications
  notificationsContainer: {
    position: 'absolute',
    top: 100,
    left: spacing.md,
    right: spacing.md,
    zIndex: 999,
  },
  notificationToast: {
    position: 'absolute',
    left: 0,
    right: 0,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.md,
    borderLeftWidth: 4,
    borderLeftColor: colors.primary,
  },
  notificationContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  notificationAvatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationAvatarText: {
    color: colors.text,
    fontSize: 16,
    fontWeight: 'bold',
  },
  notificationText: {
    flex: 1,
  },
  notificationName: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: '600',
  },
  notificationMessage: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.sm,
    marginTop: 2,
  },
});

export default OverlayProvider;
