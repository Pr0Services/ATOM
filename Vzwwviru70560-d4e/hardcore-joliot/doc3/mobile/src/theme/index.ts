/**
 * CHE·NU Mobile - Theme System
 * Système de thème complet avec support dark/light
 */

export const colors = {
  // Primary palette
  primary: {
    50: '#EEF2FF',
    100: '#E0E7FF',
    200: '#C7D2FE',
    300: '#A5B4FC',
    400: '#818CF8',
    500: '#6366F1',
    600: '#4F46E5',
    700: '#4338CA',
    800: '#3730A3',
    900: '#312E81',
  },
  
  // Accent colors
  accent: {
    purple: '#8B5CF6',
    pink: '#EC4899',
    cyan: '#06B6D4',
    emerald: '#10B981',
    amber: '#F59E0B',
    red: '#EF4444',
  },
  
  // Sphere colors
  spheres: {
    personal: '#6366F1',
    social: '#EC4899',
    scholar: '#14B8A6',
    maison: '#F59E0B',
    business: '#3B82F6',
    projects: '#10B981',
    creative: '#8B5CF6',
    cinema: '#EF4444',
    government: '#64748B',
    realestate: '#0EA5E9',
    associations: '#22C55E',
  },
  
  // Status colors
  status: {
    success: '#22C55E',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6',
  },
  
  // Priority colors
  priority: {
    low: '#64748B',
    medium: '#F59E0B',
    high: '#F97316',
    urgent: '#EF4444',
    critical: '#DC2626',
  },
};

export const lightTheme = {
  dark: false,
  colors: {
    primary: colors.primary[600],
    background: '#FFFFFF',
    card: '#F8FAFC',
    text: '#1E293B',
    textSecondary: '#64748B',
    textMuted: '#94A3B8',
    border: '#E2E8F0',
    notification: colors.status.error,
    
    // Surfaces
    surface: '#FFFFFF',
    surfaceSecondary: '#F1F5F9',
    surfaceElevated: '#FFFFFF',
    
    // Inputs
    inputBackground: '#F1F5F9',
    inputBorder: '#CBD5E1',
    inputText: '#1E293B',
    placeholder: '#94A3B8',
    
    // Nova AI
    novaGradientStart: colors.primary[500],
    novaGradientEnd: colors.accent.purple,
    novaBubble: '#EEF2FF',
    
    // Messages
    messageSent: colors.primary[500],
    messageReceived: '#F1F5F9',
    messageText: '#FFFFFF',
    messageTextReceived: '#1E293B',
    
    // Overlays
    overlay: 'rgba(0, 0, 0, 0.5)',
    modalBackground: '#FFFFFF',
    
    // Misc
    divider: '#E2E8F0',
    shadow: 'rgba(0, 0, 0, 0.1)',
    tabBar: '#FFFFFF',
    tabBarActive: colors.primary[600],
    tabBarInactive: '#94A3B8',
  },
};

export const darkTheme = {
  dark: true,
  colors: {
    primary: colors.primary[400],
    background: '#0F172A',
    card: '#1E293B',
    text: '#F1F5F9',
    textSecondary: '#94A3B8',
    textMuted: '#64748B',
    border: '#334155',
    notification: colors.status.error,
    
    // Surfaces
    surface: '#1E293B',
    surfaceSecondary: '#334155',
    surfaceElevated: '#1E293B',
    
    // Inputs
    inputBackground: '#334155',
    inputBorder: '#475569',
    inputText: '#F1F5F9',
    placeholder: '#64748B',
    
    // Nova AI
    novaGradientStart: colors.primary[400],
    novaGradientEnd: colors.accent.purple,
    novaBubble: '#312E81',
    
    // Messages
    messageSent: colors.primary[500],
    messageReceived: '#334155',
    messageText: '#FFFFFF',
    messageTextReceived: '#F1F5F9',
    
    // Overlays
    overlay: 'rgba(0, 0, 0, 0.7)',
    modalBackground: '#1E293B',
    
    // Misc
    divider: '#334155',
    shadow: 'rgba(0, 0, 0, 0.3)',
    tabBar: '#1E293B',
    tabBarActive: colors.primary[400],
    tabBarInactive: '#64748B',
  },
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  xxl: 24,
  full: 9999,
};

export const typography = {
  // Font families
  fontFamily: {
    regular: 'System',
    medium: 'System',
    semibold: 'System',
    bold: 'System',
  },
  
  // Font sizes
  fontSize: {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 18,
    '2xl': 20,
    '3xl': 24,
    '4xl': 30,
    '5xl': 36,
  },
  
  // Line heights
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
  
  // Letter spacing
  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
  },
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 6,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
    elevation: 12,
  },
};

export const animations = {
  duration: {
    fast: 150,
    normal: 300,
    slow: 500,
  },
  easing: {
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
  },
};

// Utility function to get theme
export const getTheme = (isDark: boolean) => isDark ? darkTheme : lightTheme;

// Export combined theme object
export const theme = {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
  animations,
  light: lightTheme,
  dark: darkTheme,
};

export default theme;
