import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useNavigation } from '@react-navigation/native';
import { useThreadsStore, useUIStore, useSpheresStore } from '../store';
import { lightTheme, darkTheme, colors, spacing, borderRadius } from '../theme';

const NovaScreen = () => {
  const navigation = useNavigation<any>();
  const { threads, currentThread, sendMessage, createThread, fetchThreads, setCurrentThread, isLoading } = useThreadsStore();
  const { theme } = useUIStore();
  const { currentSphere, getSphere } = useSpheresStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => { fetchThreads(); }, []);

  const handleSend = async () => {
    if (!message.trim() || sending) return;
    setSending(true);
    
    let thread = currentThread;
    if (!thread) {
      thread = await createThread('Nouvelle conversation', currentSphere);
      setCurrentThread(thread);
    }
    
    setMessage('');
    await sendMessage(thread.id, message);
    setSending(false);
    flatListRef.current?.scrollToEnd();
  };

  const sphere = getSphere(currentSphere);
  const messages = currentThread?.messages || [];

  return (
    <KeyboardAvoidingView style={[styles.container, { backgroundColor: themeColors.background }]} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      {/* Header */}
      <LinearGradient colors={[colors.primary[600], colors.accent.purple]} style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.novaAvatar}>✨</Text>
          <View style={styles.headerText}>
            <Text style={styles.novaTitle}>Nova</Text>
            <Text style={styles.novaStatus}>
              {sphere ? `Mode: ${sphere.nameFr}` : 'Assistant IA Universel'}
            </Text>
          </View>
          <TouchableOpacity style={styles.newChatButton} onPress={() => setCurrentThread(null)}>
            <Text style={styles.newChatIcon}>+</Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>

      {/* Messages */}
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item) => item.id}
        style={styles.messagesList}
        contentContainerStyle={styles.messagesContent}
        renderItem={({ item }) => (
          <View style={[styles.messageBubble, item.senderType === 'user' ? styles.userBubble : styles.novaBubble, { backgroundColor: item.senderType === 'user' ? themeColors.messageSent : themeColors.messageReceived }]}>
            <Text style={[styles.messageText, { color: item.senderType === 'user' ? themeColors.messageText : themeColors.messageTextReceived }]}>
              {item.content}
            </Text>
            {item.metadata?.tokens && (
              <Text style={styles.tokenCount}>{item.metadata.tokens} tokens</Text>
            )}
          </View>
        )}
        ListEmptyComponent={() => (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>✨</Text>
            <Text style={[styles.emptyTitle, { color: themeColors.text }]}>Bienvenue!</Text>
            <Text style={[styles.emptyText, { color: themeColors.textSecondary }]}>
              Commencez une conversation avec Nova, votre assistant IA universel.
            </Text>
          </View>
        )}
      />

      {/* Input */}
      <View style={[styles.inputContainer, { backgroundColor: themeColors.surface, borderTopColor: themeColors.border }]}>
        <TextInput
          style={[styles.input, { backgroundColor: themeColors.inputBackground, color: themeColors.inputText }]}
          placeholder="Écrivez votre message..."
          placeholderTextColor={themeColors.placeholder}
          value={message}
          onChangeText={setMessage}
          multiline
          maxLength={4000}
        />
        <TouchableOpacity style={[styles.sendButton, !message.trim() && styles.sendButtonDisabled]} onPress={handleSend} disabled={!message.trim() || sending}>
          {sending ? <ActivityIndicator color="#FFFFFF" size="small" /> : <Text style={styles.sendIcon}>➤</Text>}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { paddingTop: 60, paddingBottom: spacing.lg, paddingHorizontal: spacing.lg },
  headerContent: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  novaAvatar: { fontSize: 40 },
  headerText: { flex: 1 },
  novaTitle: { fontSize: 24, fontWeight: '700', color: '#FFFFFF' },
  novaStatus: { fontSize: 14, color: 'rgba(255,255,255,0.8)' },
  newChatButton: { width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.2)', alignItems: 'center', justifyContent: 'center' },
  newChatIcon: { fontSize: 24, color: '#FFFFFF' },
  messagesList: { flex: 1 },
  messagesContent: { padding: spacing.lg },
  messageBubble: { maxWidth: '85%', padding: spacing.md, borderRadius: borderRadius.lg, marginBottom: spacing.sm },
  userBubble: { alignSelf: 'flex-end', borderBottomRightRadius: 4 },
  novaBubble: { alignSelf: 'flex-start', borderBottomLeftRadius: 4 },
  messageText: { fontSize: 15, lineHeight: 22 },
  tokenCount: { fontSize: 10, opacity: 0.5, marginTop: 4, textAlign: 'right' },
  emptyState: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingTop: 100 },
  emptyIcon: { fontSize: 64, marginBottom: spacing.md },
  emptyTitle: { fontSize: 24, fontWeight: '600', marginBottom: spacing.sm },
  emptyText: { fontSize: 16, textAlign: 'center', paddingHorizontal: spacing.xl },
  inputContainer: { flexDirection: 'row', padding: spacing.md, gap: spacing.sm, borderTopWidth: 1 },
  input: { flex: 1, borderRadius: borderRadius.xl, padding: spacing.md, maxHeight: 100, fontSize: 16 },
  sendButton: { width: 44, height: 44, borderRadius: 22, backgroundColor: colors.primary[500], alignItems: 'center', justifyContent: 'center' },
  sendButtonDisabled: { opacity: 0.5 },
  sendIcon: { fontSize: 18, color: '#FFFFFF' },
});

export default NovaScreen;
