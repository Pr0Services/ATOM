/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║              CHE·NU™ — MOBILE APPLICATION                                    ║
 * ║              React Native / Expo                                             ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useMachine } from '@xstate/react';
import { navMachine } from '../shared/machines/navMachine';
import { MOCK_DATA } from './src/utils/mockData';

// Screens
import { EntryScreen } from './src/screens/EntryScreen';
import { ContextBureauScreen } from './src/screens/ContextBureauScreen';
import { ActionBureauScreen } from './src/screens/ActionBureauScreen';
import { WorkspaceScreen } from './src/screens/WorkspaceScreen';

// Context
import { NavContext, NavContextProvider } from './src/context/NavContext';

const Stack = createNativeStackNavigator();

function AppNavigator() {
  const { state, send } = React.useContext(NavContext);
  const currentState = state.context.currentState;

  // Map app state to screen name
  const getInitialRoute = () => {
    switch (currentState) {
      case 'entry': return 'Entry';
      case 'context_bureau': return 'ContextBureau';
      case 'action_bureau': return 'ActionBureau';
      case 'workspace': return 'Workspace';
      default: return 'Entry';
    }
  };

  return (
    <Stack.Navigator
      initialRouteName={getInitialRoute()}
      screenOptions={{
        headerStyle: {
          backgroundColor: '#0a0a0a',
        },
        headerTintColor: '#e0e0e0',
        headerTitleStyle: {
          fontWeight: '700',
        },
        contentStyle: {
          backgroundColor: '#0a0a0a',
        },
      }}
    >
      <Stack.Screen
        name="Entry"
        component={EntryScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="ContextBureau"
        component={ContextBureauScreen}
        options={{ 
          title: '📍 Context Bureau',
          headerBackVisible: false,
        }}
      />
      <Stack.Screen
        name="ActionBureau"
        component={ActionBureauScreen}
        options={{ 
          title: '⚡ Action Bureau',
        }}
      />
      <Stack.Screen
        name="Workspace"
        component={WorkspaceScreen}
        options={{ 
          title: '🔧 Workspace',
        }}
      />
    </Stack.Navigator>
  );
}

export default function App() {
  const [state, send] = useMachine(navMachine, {
    input: { data: MOCK_DATA },
  });

  return (
    <NavContextProvider value={{ state, send }}>
      <NavigationContainer>
        <StatusBar style="light" />
        <AppNavigator />
      </NavigationContainer>
    </NavContextProvider>
  );
}
