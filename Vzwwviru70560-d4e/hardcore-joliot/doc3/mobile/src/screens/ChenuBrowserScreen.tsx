// CHE·NU Mobile - CHE·NU Browser Screen (Tab 3)
// Unified browser: chenu:// protocol for internal + https:// for web
// Default: Workspace view

import React, { useState, useRef, useEffect } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  ScrollView, KeyboardAvoidingView, Platform,
} from 'react-native';
import { WebView } from 'react-native-webview';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useRoute, useIsFocused } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography, shadows } from '../theme';

// Internal content components
import WorkspaceView from '../components/browser/WorkspaceView';
import SphereView from '../components/browser/SphereView';
import DocumentView from '../components/browser/DocumentView';
import NotesView from '../components/browser/NotesView';
import QuickAccessBar from '../components/browser/QuickAccessBar';
import AgentVersionWidget from '../components/browser/AgentVersionWidget';

type ContentType = 'workspace' | 'sphere' | 'document' | 'notes' | 'web';

type VersionStatus = 'pending' | 'approved' | 'rejected';
type ChangeType = 'add' | 'remove' | 'modify';

interface VersionChange {
  id: string;
  type: ChangeType;
  location: string;
  original?: string;
  proposed: string;
}

interface Version {
  id: string;
  agentId: string;
  agentName: string;
  agentColor: string;
  timestamp: string;
  status: VersionStatus;
  changes: VersionChange[];
}

// Mock versions for demo
const mockVersions: Version[] = [
  {
    id: 'v1',
    agentId: 'agent_finance',
    agentName: 'Agent Finance',
    agentColor: '#10B981',
    timestamp: 'Il y a 2h',
    status: 'pending',
    changes: [
      { id: 'c1', type: 'modify', location: 'Section 2.3', original: 'Budget prévu: 50,000$', proposed: 'Budget prévu: 52,500$ (ajusté pour inflation)' },
      { id: 'c2', type: 'add', location: 'Section 4', proposed: 'Nouveau paragraphe sur les projections Q2' },
    ],
  },
  {
    id: 'v2',
    agentId: 'agent_design',
    agentName: 'Agent Design',
    agentColor: '#A855F7',
    timestamp: 'Il y a 5h',
    status: 'pending',
    changes: [
      { id: 'c3', type: 'modify', location: 'En-tête', original: 'Logo v1', proposed: 'Logo v2 (nouveau branding)' },
    ],
  },
];

export default function ChenuBrowserScreen() {
  const route = useRoute<any>();
  const isFocused = useIsFocused();
  const initialUrl = route.params?.url || 'chenu://workspace';
  
  const [currentUrl, setCurrentUrl] = useState(initialUrl);
  const [inputUrl, setInputUrl] = useState(initialUrl);
  const [isLoading, setIsLoading] = useState(false);
  const [canGoBack, setCanGoBack] = useState(false);
  const [canGoForward, setCanGoForward] = useState(false);
  const [history, setHistory] = useState<string[]>([initialUrl]);
  const [historyIndex, setHistoryIndex] = useState(0);
  const [versions, setVersions] = useState<Version[]>(mockVersions);
  const webViewRef = useRef<WebView>(null);

  // Update URL when navigating from other tabs
  useEffect(() => {
    if (route.params?.url && route.params.url !== currentUrl) {
      navigateToUrl(route.params.url);
    }
  }, [route.params?.url, isFocused]);

  // Parse URL to determine content type
  const getContentType = (url: string): ContentType => {
    if (url.startsWith('chenu://workspace')) return 'workspace';
    if (url.startsWith('chenu://sphere')) return 'sphere';
    if (url.startsWith('chenu://doc') || url.startsWith('chenu://documents')) return 'document';
    if (url.startsWith('chenu://notes')) return 'notes';
    if (url.startsWith('http://') || url.startsWith('https://')) return 'web';
    return 'workspace';
  };

  const contentType = getContentType(currentUrl);

  // Extract params from chenu:// URL
  const getUrlParams = (url: string) => {
    const parts = url.replace('chenu://', '').split('/');
    return {
      type: parts[0],
      id: parts[1] || null,
    };
  };

  const navigateToUrl = (url: string) => {
    // Auto-add protocol if needed
    if (!url.startsWith('chenu://') && !url.startsWith('http://') && !url.startsWith('https://')) {
      if (url.includes('.')) {
        url = 'https://' + url;
      } else {
        url = 'chenu://workspace';
      }
    }
    
    // Update history
    const newHistory = [...history.slice(0, historyIndex + 1), url];
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
    
    setCurrentUrl(url);
    setInputUrl(url);
  };

  const handleNavigate = () => {
    navigateToUrl(inputUrl.trim());
  };

  const handleRefresh = () => {
    if (contentType === 'web' && webViewRef.current) {
      webViewRef.current.reload();
    }
  };

  const handleGoBack = () => {
    if (contentType === 'web' && webViewRef.current && canGoBack) {
      webViewRef.current.goBack();
    } else if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setCurrentUrl(history[newIndex]);
      setInputUrl(history[newIndex]);
    }
  };

  const handleGoForward = () => {
    if (contentType === 'web' && webViewRef.current && canGoForward) {
      webViewRef.current.goForward();
    } else if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setCurrentUrl(history[newIndex]);
      setInputUrl(history[newIndex]);
    }
  };

  const handleHome = () => {
    navigateToUrl('chenu://workspace');
  };

  const handleApproveVersion = (versionId: string) => {
    setVersions(versions.map(v => 
      v.id === versionId ? { ...v, status: 'approved' as VersionStatus } : v
    ));
  };

  const handleRejectVersion = (versionId: string) => {
    setVersions(versions.map(v => 
      v.id === versionId ? { ...v, status: 'rejected' as VersionStatus } : v
    ));
  };

  // Render internal content based on URL
  const renderInternalContent = () => {
    const params = getUrlParams(currentUrl);

    switch (contentType) {
      case 'workspace':
        return <WorkspaceView />;
      case 'sphere':
        return <SphereView sphereId={params.id} />;
      case 'document':
        return <DocumentView documentId={params.id} />;
      case 'notes':
        return <NotesView />;
      default:
        return <WorkspaceView />;
    }
  };

  const canGoBackInternal = historyIndex > 0;
  const canGoForwardInternal = historyIndex < history.length - 1;

  return (
    <View style={styles.container}>
      {/* Browser Header */}
      <View style={styles.header}>
        {/* Navigation Controls */}
        <View style={styles.navControls}>
          <TouchableOpacity 
            style={[styles.navButton, !canGoBackInternal && contentType !== 'web' && styles.navButtonDisabled]}
            onPress={handleGoBack}
          >
            <Ionicons name="chevron-back" size={24} color={canGoBackInternal || canGoBack ? colors.text : colors.textMuted} />
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.navButton, !canGoForwardInternal && contentType !== 'web' && styles.navButtonDisabled]}
            onPress={handleGoForward}
          >
            <Ionicons name="chevron-forward" size={24} color={canGoForwardInternal || canGoForward ? colors.text : colors.textMuted} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.navButton} onPress={handleRefresh}>
            <Ionicons name="refresh" size={22} color={colors.text} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.navButton} onPress={handleHome}>
            <Ionicons name="home" size={22} color={colors.text} />
          </TouchableOpacity>
        </View>

        {/* URL Bar */}
        <View style={styles.urlBarContainer}>
          <View style={styles.urlBar}>
            <Ionicons 
              name={contentType === 'web' ? 'globe' : 'apps'} 
              size={18} 
              color={contentType === 'web' ? colors.success : colors.primary} 
            />
            <TextInput
              style={styles.urlInput}
              value={inputUrl}
              onChangeText={setInputUrl}
              onSubmitEditing={handleNavigate}
              placeholder="Entrer une URL..."
              placeholderTextColor={colors.textMuted}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="url"
              returnKeyType="go"
            />
            {isLoading && contentType === 'web' && (
              <View style={styles.loadingIndicator} />
            )}
          </View>
        </View>

        {/* Bookmark Button */}
        <TouchableOpacity style={styles.bookmarkButton}>
          <Ionicons name="bookmark-outline" size={22} color={colors.text} />
        </TouchableOpacity>
      </View>

      {/* Quick Access Bar */}
      <QuickAccessBar onNavigate={navigateToUrl} />

      {/* Content Area */}
      <View style={styles.content}>
        {contentType === 'web' ? (
          <WebView
            ref={webViewRef}
            source={{ uri: currentUrl }}
            style={styles.webview}
            onLoadStart={() => setIsLoading(true)}
            onLoadEnd={() => setIsLoading(false)}
            onNavigationStateChange={(navState) => {
              setCanGoBack(navState.canGoBack);
              setCanGoForward(navState.canGoForward);
              setInputUrl(navState.url);
            }}
            allowsInlineMediaPlayback
            javaScriptEnabled
            domStorageEnabled
          />
        ) : (
          renderInternalContent()
        )}

        {/* Agent Version Widget */}
        {contentType !== 'web' && (
          <AgentVersionWidget
            documentId={currentUrl}
            versions={versions}
            onApprove={handleApproveVersion}
            onReject={handleRejectVersion}
            onApproveChange={(vId, cId) => console.log('Approve change', vId, cId)}
            onRejectChange={(vId, cId) => console.log('Reject change', vId, cId)}
          />
        )}
      </View>

      {/* Quick Actions Bar (for internal content) */}
      {contentType !== 'web' && (
        <View style={styles.quickBar}>
          <TouchableOpacity 
            style={styles.quickBarItem}
            onPress={() => navigateToUrl('chenu://workspace')}
          >
            <Ionicons name="folder" size={20} color={contentType === 'workspace' ? colors.primary : colors.textMuted} />
            <Text style={[styles.quickBarText, contentType === 'workspace' && styles.quickBarTextActive]}>Workspace</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={styles.quickBarItem}
            onPress={() => navigateToUrl('chenu://notes')}
          >
            <Ionicons name="create" size={20} color={contentType === 'notes' ? colors.primary : colors.textMuted} />
            <Text style={[styles.quickBarText, contentType === 'notes' && styles.quickBarTextActive]}>Notes</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={styles.quickBarItem}
            onPress={() => navigateToUrl('chenu://documents')}
          >
            <Ionicons name="document-text" size={20} color={contentType === 'document' ? colors.primary : colors.textMuted} />
            <Text style={[styles.quickBarText, contentType === 'document' && styles.quickBarTextActive]}>Documents</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.sm,
    paddingTop: 60, paddingBottom: spacing.md, paddingHorizontal: spacing.md,
    backgroundColor: colors.surface, borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  navControls: { flexDirection: 'row', gap: 2 },
  navButton: { padding: spacing.xs },
  navButtonDisabled: { opacity: 0.4 },
  urlBarContainer: { flex: 1 },
  urlBar: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.sm,
    backgroundColor: colors.backgroundTertiary, borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md, paddingVertical: spacing.sm,
  },
  urlInput: { flex: 1, color: colors.text, fontSize: typography.fontSize.sm },
  loadingIndicator: {
    width: 16, height: 16, borderRadius: 8,
    borderWidth: 2, borderColor: colors.primary, borderTopColor: 'transparent',
  },
  bookmarkButton: { padding: spacing.xs },
  content: { flex: 1 },
  webview: { flex: 1 },
  quickBar: {
    flexDirection: 'row', justifyContent: 'space-around',
    backgroundColor: colors.surface, borderTopWidth: 1, borderTopColor: colors.border,
    paddingVertical: spacing.sm, paddingBottom: spacing.lg,
  },
  quickBarItem: { alignItems: 'center', gap: 2 },
  quickBarText: { color: colors.textMuted, fontSize: typography.fontSize.xs },
  quickBarTextActive: { color: colors.primary },
});
