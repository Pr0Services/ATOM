/**
 * CHE·NU Mobile - Navigation System
 * Navigation complète avec tous les écrans
 */
import React from 'react';
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useUIStore, useAuthStore, useNotificationsStore } from '../store';
import { lightTheme, darkTheme, colors } from '../theme';
import type { RootStackParamList } from '../types';

// Import Screens
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import ForgotPasswordScreen from '../screens/ForgotPasswordScreen';
import HomeScreen from '../screens/HomeScreen';
import SpheresScreen from '../screens/SpheresScreen';
import SphereDetailScreen from '../screens/SphereDetailScreen';
import NovaScreen from '../screens/NovaScreen';
import ThreadDetailScreen from '../screens/ThreadDetailScreen';
import ProjectsScreen from '../screens/ProjectsScreen';
import ProjectDetailScreen from '../screens/ProjectDetailScreen';
import AgentsScreen from '../screens/AgentsScreen';
import AgentDetailScreen from '../screens/AgentDetailScreen';
import AgentCallScreen from '../screens/AgentCallScreen';
import CommunicationsScreen from '../screens/CommunicationsScreen';
import CalendarScreen from '../screens/CalendarScreen';
import ConstructionScreen from '../screens/ConstructionScreen';
import SiteDetailScreen from '../screens/SiteDetailScreen';
import SettingsScreen from '../screens/SettingsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import NotificationsScreen from '../screens/NotificationsScreen';
import SearchScreen from '../screens/SearchScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();
const Drawer = createDrawerNavigator();

// ============== TAB ICONS ==============
const TabIcon = ({ name, focused, color }: { name: string; focused: boolean; color: string }) => {
  const icons: Record<string, string> = {
    Home: '🏠',
    Spheres: '🌐',
    Nova: '✨',
    Projects: '📋',
    More: '☰',
  };
  
  return (
    <View style={[styles.tabIcon, focused && styles.tabIconActive]}>
      <Text style={{ fontSize: focused ? 24 : 20 }}>{icons[name]}</Text>
    </View>
  );
};

// ============== BOTTOM TAB NAVIGATOR ==============
const MainTabs = () => {
  const { theme } = useUIStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color }) => (
          <TabIcon name={route.name} focused={focused} color={color} />
        ),
        tabBarActiveTintColor: themeColors.tabBarActive,
        tabBarInactiveTintColor: themeColors.tabBarInactive,
        tabBarStyle: {
          backgroundColor: themeColors.tabBar,
          borderTopColor: themeColors.border,
          height: 80,
          paddingBottom: 20,
          paddingTop: 10,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
        headerShown: false,
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ tabBarLabel: 'Accueil' }}
      />
      <Tab.Screen 
        name="Spheres" 
        component={SpheresScreen}
        options={{ tabBarLabel: 'Sphères' }}
      />
      <Tab.Screen 
        name="Nova" 
        component={NovaScreen}
        options={{ tabBarLabel: 'Nova' }}
      />
      <Tab.Screen 
        name="Projects" 
        component={ProjectsScreen}
        options={{ tabBarLabel: 'Projets' }}
      />
      <Tab.Screen 
        name="More" 
        component={MoreStack}
        options={{ tabBarLabel: 'Plus' }}
      />
    </Tab.Navigator>
  );
};

// ============== MORE STACK ==============
const MoreStackNav = createNativeStackNavigator();

const MoreStack = () => {
  const { theme } = useUIStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  return (
    <MoreStackNav.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: themeColors.surface },
        headerTintColor: themeColors.text,
      }}
    >
      <MoreStackNav.Screen 
        name="MoreMenu" 
        component={MoreMenuScreen}
        options={{ title: 'Plus' }}
      />
      <MoreStackNav.Screen 
        name="Agents" 
        component={AgentsScreen}
        options={{ title: 'Agents IA' }}
      />
      <MoreStackNav.Screen 
        name="Communications" 
        component={CommunicationsScreen}
        options={{ title: 'Communications' }}
      />
      <MoreStackNav.Screen 
        name="Calendar" 
        component={CalendarScreen}
        options={{ title: 'Calendrier' }}
      />
      <MoreStackNav.Screen 
        name="Construction" 
        component={ConstructionScreen}
        options={{ title: 'Construction' }}
      />
      <MoreStackNav.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: 'Paramètres' }}
      />
      <MoreStackNav.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{ title: 'Profil' }}
      />
      <MoreStackNav.Screen 
        name="Notifications" 
        component={NotificationsScreen}
        options={{ title: 'Notifications' }}
      />
    </MoreStackNav.Navigator>
  );
};

// ============== MORE MENU SCREEN ==============
const MoreMenuScreen = ({ navigation }: any) => {
  const { theme } = useUIStore();
  const { unreadCount } = useNotificationsStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  const menuItems = [
    { name: 'Agents', icon: '🤖', label: 'Agents IA', badge: null },
    { name: 'Communications', icon: '📧', label: 'Communications', badge: 3 },
    { name: 'Calendar', icon: '📅', label: 'Calendrier', badge: null },
    { name: 'Construction', icon: '🏗️', label: 'Construction', badge: null },
    { name: 'Notifications', icon: '🔔', label: 'Notifications', badge: unreadCount },
    { name: 'Profile', icon: '👤', label: 'Profil', badge: null },
    { name: 'Settings', icon: '⚙️', label: 'Paramètres', badge: null },
  ];
  
  return (
    <View style={[styles.moreMenu, { backgroundColor: themeColors.background }]}>
      {menuItems.map((item) => (
        <TouchableOpacity
          key={item.name}
          style={[styles.menuItem, { backgroundColor: themeColors.surface }]}
          onPress={() => navigation.navigate(item.name)}
        >
          <Text style={styles.menuIcon}>{item.icon}</Text>
          <Text style={[styles.menuLabel, { color: themeColors.text }]}>{item.label}</Text>
          {item.badge !== null && item.badge > 0 && (
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{item.badge}</Text>
            </View>
          )}
          <Text style={[styles.menuArrow, { color: themeColors.textMuted }]}>›</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
};

// ============== AUTH STACK ==============
const AuthStack = () => {
  const { theme } = useUIStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: themeColors.background },
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
    </Stack.Navigator>
  );
};

// ============== MAIN STACK ==============
const MainStack = () => {
  const { theme } = useUIStore();
  const isDark = theme === 'dark';
  const themeColors = isDark ? darkTheme.colors : lightTheme.colors;
  
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: themeColors.surface },
        headerTintColor: themeColors.text,
        headerBackTitle: 'Retour',
      }}
    >
      <Stack.Screen 
        name="Main" 
        component={MainTabs}
        options={{ headerShown: false }}
      />
      <Stack.Screen 
        name="SphereDetail" 
        component={SphereDetailScreen}
        options={{ title: 'Sphère' }}
      />
      <Stack.Screen 
        name="NovaThread" 
        component={ThreadDetailScreen}
        options={{ title: 'Conversation' }}
      />
      <Stack.Screen 
        name="ProjectDetail" 
        component={ProjectDetailScreen}
        options={{ title: 'Projet' }}
      />
      <Stack.Screen 
        name="AgentDetail" 
        component={AgentDetailScreen}
        options={{ title: 'Agent' }}
      />
      <Stack.Screen 
        name="AgentCall" 
        component={AgentCallScreen}
        options={{ 
          title: 'Appel Agent',
          presentation: 'fullScreenModal',
        }}
      />
      <Stack.Screen 
        name="SiteDetail" 
        component={SiteDetailScreen}
        options={{ title: 'Chantier' }}
      />
      <Stack.Screen 
        name="Search" 
        component={SearchScreen}
        options={{ 
          title: 'Recherche',
          presentation: 'modal',
        }}
      />
    </Stack.Navigator>
  );
};

// ============== ROOT NAVIGATOR ==============
export const AppNavigator = () => {
  const { theme } = useUIStore();
  const { isAuthenticated } = useAuthStore();
  const isDark = theme === 'dark';
  
  const navigationTheme = isDark ? {
    ...DarkTheme,
    colors: {
      ...DarkTheme.colors,
      background: darkTheme.colors.background,
      card: darkTheme.colors.card,
      text: darkTheme.colors.text,
      border: darkTheme.colors.border,
      primary: darkTheme.colors.primary,
    },
  } : {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      background: lightTheme.colors.background,
      card: lightTheme.colors.card,
      text: lightTheme.colors.text,
      border: lightTheme.colors.border,
      primary: lightTheme.colors.primary,
    },
  };
  
  return (
    <NavigationContainer theme={navigationTheme}>
      {isAuthenticated ? <MainStack /> : <AuthStack />}
    </NavigationContainer>
  );
};

// ============== STYLES ==============
const styles = StyleSheet.create({
  tabIcon: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 40,
    height: 40,
    borderRadius: 20,
  },
  tabIconActive: {
    backgroundColor: 'rgba(99, 102, 241, 0.15)',
  },
  moreMenu: {
    flex: 1,
    padding: 16,
    gap: 12,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  menuIcon: {
    fontSize: 24,
  },
  menuLabel: {
    flex: 1,
    fontSize: 16,
    fontWeight: '500',
  },
  badge: {
    backgroundColor: colors.status.error,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
    minWidth: 20,
    alignItems: 'center',
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  menuArrow: {
    fontSize: 24,
    fontWeight: '300',
  },
});

export default AppNavigator;
