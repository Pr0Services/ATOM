/**
 * AT·OM — useTabSystem
 * Hook consumer pour le système d'onglets du panneau central
 *
 * Expose l'état des onglets et les actions pour les gérer.
 * Même pattern que les 6 hooks existants (useGovernance, etc.)
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import type { ContentTab } from '../types/atom-types';

export function useTabSystem() {
  const { state, openTab, closeTab, activateTab, dispatch } = useATOM();

  const activeTab = useMemo<ContentTab | null>(() =>
    state.tabs.find(t => t.id === state.active_tab_id) ?? null,
  [state.tabs, state.active_tab_id]);

  const sphereTabs = useMemo(() =>
    state.tabs.filter(t => t.source === 'sphere'),
  [state.tabs]);

  const commTabs = useMemo(() =>
    state.tabs.filter(t => t.source === 'comm'),
  [state.tabs]);

  const tabCount = useMemo(() => state.tabs.length, [state.tabs]);

  const pinnedTabs = useMemo(() =>
    state.tabs.filter(t => t.is_pinned),
  [state.tabs]);

  const closeAllUnpinned = useCallback(() => {
    state.tabs
      .filter(t => !t.is_pinned)
      .forEach(t => closeTab(t.id));
  }, [state.tabs, closeTab]);

  const pinTab = useCallback((tabId: string) => {
    dispatch({ type: 'PIN_TAB', tab_id: tabId, pinned: true });
  }, [dispatch]);

  const unpinTab = useCallback((tabId: string) => {
    dispatch({ type: 'PIN_TAB', tab_id: tabId, pinned: false });
  }, [dispatch]);

  return {
    // État
    tabs: state.tabs,
    activeTab,
    activeTabId: state.active_tab_id,
    sphereTabs,
    commTabs,
    pinnedTabs,
    tabCount,

    // Actions
    openTab,
    closeTab,
    activateTab,
    pinTab,
    unpinTab,
    closeAllUnpinned,
  };
}
