// CHE·NU Mobile - Nova Floating Button
// Quick access to Nova from any screen

import React, { useState, useRef } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet, Modal, TextInput,
  KeyboardAvoidingView, Platform, ScrollView, Animated, Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '../../theme';
import VoiceInput from './VoiceInput';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface Message {
  id: string;
  role: 'user' | 'nova';
  content: string;
  timestamp: string;
}

interface NovaFloatingButtonProps {
  isVisible?: boolean;
}

export default function NovaFloatingButton({ isVisible = true }: NovaFloatingButtonProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'nova',
      content: 'Je suis Nova, votre guide CHE·NU. Comment puis-je vous aider?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const scrollRef = useRef<ScrollView>(null);

  if (!isVisible) return null;

  const handleOpen = () => {
    setIsExpanded(true);
    Animated.spring(scaleAnim, {
      toValue: 1.2,
      friction: 3,
      useNativeDriver: true,
    }).start(() => {
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 3,
        useNativeDriver: true,
      }).start();
    });
  };

  const handleClose = () => {
    setIsExpanded(false);
  };

  const handleSend = () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simulate Nova response
    setTimeout(() => {
      const novaMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'nova',
        content: 'Je comprends. Voulez-vous que je crée un thread gouverné pour cette tâche?',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, novaMessage]);
      setIsTyping(false);
      scrollRef.current?.scrollToEnd({ animated: true });
    }, 1500);
  };

  const handleVoiceMessage = (audioData: string, duration: number) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: `🎤 Message vocal (${duration}s)`,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    setTimeout(() => {
      const novaMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'nova',
        content: 'J\'ai bien reçu votre message vocal. Je l\'analyse et vous réponds dans un instant.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, novaMessage]);
      setIsTyping(false);
    }, 2000);
  };

  return (
    <>
      {/* Floating Button */}
      {!isExpanded && (
        <TouchableOpacity
          style={styles.floatingButton}
          onPress={handleOpen}
          activeOpacity={0.9}
        >
          <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
            <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.buttonGradient}>
              <Text style={styles.novaLogo}>N</Text>
            </LinearGradient>
          </Animated.View>
        </TouchableOpacity>
      )}

      {/* Expanded Chat Modal */}
      <Modal
        visible={isExpanded}
        animationType="slide"
        transparent
        onRequestClose={handleClose}
      >
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.modalContainer}
        >
          <View style={styles.chatContainer}>
            {/* Header */}
            <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.header}>
              <View style={styles.headerContent}>
                <View style={styles.novaInfo}>
                  <View style={styles.novaAvatar}>
                    <Text style={styles.novaAvatarText}>N</Text>
                  </View>
                  <View>
                    <Text style={styles.novaName}>Nova</Text>
                    <View style={styles.statusRow}>
                      <View style={styles.statusDot} />
                      <Text style={styles.statusText}>En ligne</Text>
                    </View>
                  </View>
                </View>
                <View style={styles.headerActions}>
                  <TouchableOpacity style={styles.headerButton}>
                    <Ionicons name="call" size={20} color={colors.text} />
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.headerButton} onPress={handleClose}>
                    <Ionicons name="close" size={24} color={colors.text} />
                  </TouchableOpacity>
                </View>
              </View>
            </LinearGradient>

            {/* Messages */}
            <ScrollView
              ref={scrollRef}
              style={styles.messagesContainer}
              contentContainerStyle={styles.messagesContent}
              onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}
            >
              {messages.map(message => (
                <View
                  key={message.id}
                  style={[
                    styles.messageRow,
                    message.role === 'nova' ? styles.novaRow : styles.userRow,
                  ]}
                >
                  {message.role === 'nova' && (
                    <View style={styles.messageAvatar}>
                      <Text style={styles.messageAvatarText}>N</Text>
                    </View>
                  )}
                  <View
                    style={[
                      styles.messageBubble,
                      message.role === 'nova' ? styles.novaBubble : styles.userBubble,
                    ]}
                  >
                    <Text style={styles.messageText}>{message.content}</Text>
                  </View>
                </View>
              ))}

              {isTyping && (
                <View style={[styles.messageRow, styles.novaRow]}>
                  <View style={styles.messageAvatar}>
                    <Text style={styles.messageAvatarText}>N</Text>
                  </View>
                  <View style={[styles.messageBubble, styles.novaBubble]}>
                    <View style={styles.typingDots}>
                      <View style={styles.typingDot} />
                      <View style={styles.typingDot} />
                      <View style={styles.typingDot} />
                    </View>
                  </View>
                </View>
              )}
            </ScrollView>

            {/* Quick Actions */}
            <View style={styles.quickActions}>
              {['Créer thread', 'Mes sphères', 'Aide'].map((action, i) => (
                <TouchableOpacity
                  key={i}
                  style={styles.quickAction}
                  onPress={() => setInputText(action)}
                >
                  <Text style={styles.quickActionText}>{action}</Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Input */}
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Demandez à Nova..."
                placeholderTextColor={colors.textMuted}
                value={inputText}
                onChangeText={setInputText}
                multiline
                maxLength={500}
              />
              {inputText.trim() ? (
                <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
                  <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.sendGradient}>
                    <Ionicons name="send" size={18} color={colors.text} />
                  </LinearGradient>
                </TouchableOpacity>
              ) : (
                <VoiceInput onVoiceMessage={handleVoiceMessage} />
              )}
            </View>
          </View>
        </KeyboardAvoidingView>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  // Floating Button
  floatingButton: {
    position: 'absolute',
    bottom: 120,
    right: spacing.md,
    zIndex: 1000,
    ...shadows.lg,
  },
  buttonGradient: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: colors.background,
  },
  novaLogo: {
    color: colors.text,
    fontSize: 24,
    fontWeight: 'bold',
  },

  // Modal
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  chatContainer: {
    height: SCREEN_HEIGHT * 0.75,
    backgroundColor: colors.background,
    borderTopLeftRadius: borderRadius.xl,
    borderTopRightRadius: borderRadius.xl,
    overflow: 'hidden',
  },

  // Header
  header: {
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
    paddingHorizontal: spacing.lg,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  novaInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  novaAvatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  novaAvatarText: {
    color: colors.text,
    fontSize: 20,
    fontWeight: 'bold',
  },
  novaName: {
    color: colors.text,
    fontSize: typography.fontSize.lg,
    fontWeight: 'bold',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.success,
  },
  statusText: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: typography.fontSize.sm,
  },
  headerActions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  headerButton: {
    padding: spacing.sm,
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: borderRadius.full,
  },

  // Messages
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  messageRow: {
    flexDirection: 'row',
    marginBottom: spacing.md,
    alignItems: 'flex-end',
  },
  novaRow: {
    justifyContent: 'flex-start',
  },
  userRow: {
    justifyContent: 'flex-end',
  },
  messageAvatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.sm,
  },
  messageAvatarText: {
    color: colors.text,
    fontSize: 12,
    fontWeight: 'bold',
  },
  messageBubble: {
    maxWidth: '75%',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
  },
  novaBubble: {
    backgroundColor: colors.surface,
    borderBottomLeftRadius: 4,
  },
  userBubble: {
    backgroundColor: colors.primary,
    borderBottomRightRadius: 4,
  },
  messageText: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    lineHeight: 22,
  },
  typingDots: {
    flexDirection: 'row',
    gap: 4,
    paddingVertical: spacing.xs,
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.primary,
    opacity: 0.6,
  },

  // Quick Actions
  quickActions: {
    flexDirection: 'row',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    gap: spacing.sm,
  },
  quickAction: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.full,
    borderWidth: 1,
    borderColor: colors.border,
  },
  quickActionText: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.sm,
  },

  // Input
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: spacing.sm,
    padding: spacing.md,
    paddingBottom: spacing.xl,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  input: {
    flex: 1,
    backgroundColor: colors.backgroundTertiary,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    color: colors.text,
    fontSize: typography.fontSize.md,
    maxHeight: 100,
  },
  sendButton: {
    borderRadius: borderRadius.full,
    overflow: 'hidden',
  },
  sendGradient: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
