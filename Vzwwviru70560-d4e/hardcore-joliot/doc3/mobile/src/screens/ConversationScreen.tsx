// CHE·NU Mobile - Conversation Screen
// Chat with any agent (Nova or others)

import React, { useState, useRef, useEffect } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  FlatList, KeyboardAvoidingView, Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography } from '../theme';
import { useOverlay } from '../providers/OverlayProvider';

export default function ConversationScreen() {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();
  const { agentId, agentName } = route.params;
  const { startCall, addNotification } = useOverlay();
  
  const isNova = agentId === 'nova';
  const agentColor = isNova ? colors.primary : colors.governance.orchestration;

  const [messages, setMessages] = useState([
    { 
      id: '1', 
      role: 'agent', 
      content: isNova 
        ? "Bonjour! Je suis Nova, votre guide CHE·NU. Comment puis-je vous aider aujourd'hui?"
        : `Bonjour! Je suis ${agentName}. Comment puis-je vous assister?`, 
      timestamp: new Date().toISOString() 
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  const handleSend = async () => {
    if (!inputText.trim()) return;
    
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText.trim(),
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);
    
    // Simulate agent response
    setTimeout(() => {
      const agentMessage = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: isNova 
          ? "Je comprends votre demande. Je vais coordonner avec les agents appropriés pour vous aider. Souhaitez-vous que j'analyse cela plus en détail?"
          : `En tant que ${agentName}, je vais traiter votre demande de manière gouvernée. Voici mon analyse...`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, agentMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleCall = () => {
    startCall(agentId, agentName, agentColor);
    navigation.navigate('AgentCall', { agentId, agentName, agentColor });
  };

  const renderMessage = ({ item }: any) => {
    const isAgent = item.role === 'agent';
    return (
      <View style={[styles.messageRow, isAgent ? styles.agentRow : styles.userRow]}>
        {isAgent && (
          <View style={[styles.avatar, { backgroundColor: agentColor }]}>
            {isNova ? (
              <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.novaAvatar}>
                <Text style={styles.avatarText}>N</Text>
              </LinearGradient>
            ) : (
              <Text style={styles.avatarText}>{agentName.charAt(0)}</Text>
            )}
          </View>
        )}
        <View style={[styles.bubble, isAgent ? styles.agentBubble : styles.userBubble]}>
          <Text style={styles.messageText}>{item.content}</Text>
          <Text style={styles.timestamp}>
            {new Date(item.timestamp).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {/* Agent Header */}
      <View style={[styles.agentHeader, { backgroundColor: agentColor }]}>
        <View style={styles.agentInfo}>
          <View style={styles.statusDot} />
          <Text style={styles.agentStatus}>En ligne</Text>
        </View>
        <TouchableOpacity style={styles.callButton} onPress={handleCall}>
          <Ionicons name="call" size={20} color={colors.text} />
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView 
        style={styles.chatContainer}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={100}
      >
        {/* Messages */}
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id}
          style={styles.messagesList}
          contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
        />

        {/* Typing Indicator */}
        {isTyping && (
          <View style={styles.typingContainer}>
            <View style={styles.typingDots}>
              <View style={[styles.dot, { opacity: 0.4 }]} />
              <View style={[styles.dot, { opacity: 0.6 }]} />
              <View style={[styles.dot, { opacity: 0.8 }]} />
            </View>
            <Text style={styles.typingText}>{agentName} écrit...</Text>
          </View>
        )}

        {/* Quick Actions */}
        {isNova && (
          <View style={styles.quickActions}>
            {['Mes sphères', 'Créer un thread', 'Workspace'].map((action, i) => (
              <TouchableOpacity 
                key={i} 
                style={styles.quickAction}
                onPress={() => setInputText(action)}
              >
                <Text style={styles.quickActionText}>{action}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Input */}
        <View style={styles.inputContainer}>
          <TouchableOpacity style={styles.voiceButton}>
            <Ionicons name="mic" size={22} color={colors.primary} />
          </TouchableOpacity>
          <TextInput
            style={styles.input}
            placeholder={`Message à ${agentName}...`}
            placeholderTextColor={colors.textMuted}
            value={inputText}
            onChangeText={setInputText}
            multiline
            maxLength={2000}
          />
          <TouchableOpacity 
            style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
            onPress={handleSend}
            disabled={!inputText.trim()}
          >
            <LinearGradient
              colors={inputText.trim() ? [colors.primary, colors.secondary] : [colors.border, colors.border]}
              style={styles.sendGradient}
            >
              <Ionicons name="send" size={18} color={colors.text} />
            </LinearGradient>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  agentHeader: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingHorizontal: spacing.lg, paddingVertical: spacing.sm,
  },
  agentInfo: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  statusDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.success },
  agentStatus: { color: 'rgba(255,255,255,0.8)', fontSize: typography.fontSize.sm },
  callButton: { padding: spacing.sm, backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: borderRadius.full },
  chatContainer: { flex: 1 },
  messagesList: { flex: 1 },
  messagesContent: { padding: spacing.lg, paddingBottom: spacing.xxl },
  messageRow: { flexDirection: 'row', marginBottom: spacing.md, alignItems: 'flex-end' },
  agentRow: { justifyContent: 'flex-start' },
  userRow: { justifyContent: 'flex-end' },
  avatar: { width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center', marginRight: spacing.sm },
  novaAvatar: { width: '100%', height: '100%', borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  avatarText: { color: colors.text, fontSize: 14, fontWeight: 'bold' },
  bubble: { maxWidth: '75%', padding: spacing.md, borderRadius: borderRadius.lg },
  agentBubble: { backgroundColor: colors.surface, borderBottomLeftRadius: 4 },
  userBubble: { backgroundColor: colors.primary, borderBottomRightRadius: 4 },
  messageText: { color: colors.text, fontSize: typography.fontSize.md, lineHeight: 22 },
  timestamp: { color: 'rgba(255,255,255,0.5)', fontSize: typography.fontSize.xs, marginTop: spacing.xs, textAlign: 'right' },
  typingContainer: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, paddingVertical: spacing.sm },
  typingDots: { flexDirection: 'row', gap: 4, marginRight: spacing.sm },
  dot: { width: 6, height: 6, borderRadius: 3, backgroundColor: colors.primary },
  typingText: { color: colors.textMuted, fontSize: typography.fontSize.sm },
  quickActions: { flexDirection: 'row', paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, gap: spacing.sm },
  quickAction: { backgroundColor: colors.surface, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, borderRadius: borderRadius.full, borderWidth: 1, borderColor: colors.border },
  quickActionText: { color: colors.textSecondary, fontSize: typography.fontSize.sm },
  inputContainer: {
    flexDirection: 'row', alignItems: 'flex-end', gap: spacing.sm,
    paddingHorizontal: spacing.md, paddingVertical: spacing.md,
    backgroundColor: colors.surface, borderTopWidth: 1, borderTopColor: colors.border,
  },
  voiceButton: { padding: spacing.sm, backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.full },
  input: {
    flex: 1, backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md, paddingVertical: spacing.sm, color: colors.text,
    fontSize: typography.fontSize.md, maxHeight: 100,
  },
  sendButton: { borderRadius: borderRadius.full, overflow: 'hidden' },
  sendButtonDisabled: { opacity: 0.5 },
  sendGradient: { padding: spacing.sm },
});
