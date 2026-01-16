// CHE·NU™ React Native Providers
// Context providers for mobile app

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import * as Localization from 'expo-localization';

// ============================================================
// AUTH PROVIDER
// ============================================================

interface User {
  id: string;
  email: string;
  name: string;
  // Governance consent (Memory Prompt)
  consentTerms: boolean;
  consentGovernance: boolean;
  consentDataProcessing: boolean;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
  // Memory Prompt: Governance consent required
  consentTerms: boolean;
  consentGovernance: boolean;
  consentDataProcessing: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const token = await SecureStore.getItemAsync('accessToken');
      if (token) {
        const userJson = await AsyncStorage.getItem('user');
        if (userJson) {
          setUser(JSON.parse(userJson));
        }
      }
    } catch (error) {
      console.error('Error loading auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        await SecureStore.setItemAsync('accessToken', data.accessToken);
        await SecureStore.setItemAsync('refreshToken', data.refreshToken);
        await AsyncStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        return { success: true };
      }

      return { success: false, error: data.error?.message || 'Login failed' };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const register = async (data: RegisterData) => {
    // Memory Prompt: Verify governance consent
    if (!data.consentTerms || !data.consentGovernance || !data.consentDataProcessing) {
      return { success: false, error: 'All governance consents are required' };
    }

    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
          name: data.name,
          consent_terms: data.consentTerms,
          consent_governance: data.consentGovernance,
          consent_data_processing: data.consentDataProcessing,
        }),
      });

      const result = await response.json();

      if (result.success) {
        return { success: true };
      }

      return { success: false, error: result.error?.message || 'Registration failed' };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const logout = async () => {
    try {
      const refreshToken = await SecureStore.getItemAsync('refreshToken');
      
      await fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      await SecureStore.deleteItemAsync('accessToken');
      await SecureStore.deleteItemAsync('refreshToken');
      await AsyncStorage.removeItem('user');
      setUser(null);
    }
  };

  const refreshToken = async () => {
    try {
      const storedRefreshToken = await SecureStore.getItemAsync('refreshToken');
      if (!storedRefreshToken) return false;

      const response = await fetch(`${API_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: storedRefreshToken }),
      });

      const data = await response.json();

      if (data.success) {
        await SecureStore.setItemAsync('accessToken', data.accessToken);
        await SecureStore.setItemAsync('refreshToken', data.refreshToken);
        return true;
      }

      return false;
    } catch (error) {
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        refreshToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// ============================================================
// THEME PROVIDER
// ============================================================

// CHE·NU Brand Colors (Memory Prompt)
const CHENU_COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

interface ThemeColors {
  primary: string;
  primaryLight: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  error: string;
  success: string;
  warning: string;
}

interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
  colors: ThemeColors;
}

const lightColors: ThemeColors = {
  primary: CHENU_COLORS.sacredGold,
  primaryLight: '#F5E6C8',
  background: '#FFFFFF',
  surface: '#F5F5F5',
  text: '#1A1A1A',
  textSecondary: '#666666',
  border: '#E0E0E0',
  error: '#D32F2F',
  success: CHENU_COLORS.jungleEmerald,
  warning: '#FFA726',
};

const darkColors: ThemeColors = {
  primary: CHENU_COLORS.sacredGold,
  primaryLight: '#4A4035',
  background: CHENU_COLORS.uiSlate,
  surface: '#2A2B2F',
  text: '#FFFFFF',
  textSecondary: '#A0A0A0',
  border: '#3A3B3F',
  error: '#EF5350',
  success: CHENU_COLORS.cenoteTurquoise,
  warning: '#FFB74D',
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    loadThemePreference();
  }, []);

  const loadThemePreference = async () => {
    try {
      const savedTheme = await AsyncStorage.getItem('theme');
      if (savedTheme) {
        setIsDark(savedTheme === 'dark');
      }
    } catch (error) {
      console.error('Error loading theme:', error);
    }
  };

  const toggleTheme = async () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    await AsyncStorage.setItem('theme', newTheme ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider
      value={{
        isDark,
        toggleTheme,
        colors: isDark ? darkColors : lightColors,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// ============================================================
// I18N PROVIDER
// ============================================================

type SupportedLanguage = 'en' | 'fr' | 'es' | 'de' | 'it' | 'pt' | 'zh' | 'ja' | 'ko' | 'ar';

interface I18nContextType {
  language: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => void;
  t: (key: string, params?: Record<string, string>) => string;
}

// Translations
const translations: Record<SupportedLanguage, Record<string, string>> = {
  en: {
    'common.welcome': 'Welcome',
    'common.logout': 'Logout',
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.loading': 'Loading...',
    
    'dashboard.subtitle': 'Your governed intelligence dashboard',
    
    'spheres.title': 'Spheres',
    'spheres.description': 'Choose a context to work in',
    'spheres.personal.description': 'Personal life management',
    'spheres.business.description': 'Business operations',
    'spheres.government.description': 'Government interactions',
    'spheres.studio.description': 'Creative projects',
    'spheres.community.description': 'Community engagement',
    'spheres.social.description': 'Social media management',
    'spheres.entertainment.description': 'Entertainment activities',
    'spheres.team.description': 'Team collaboration',
    
    'tokens.budget': 'Token Budget',
    'tokens.allocated': 'Allocated',
    'tokens.used': 'Used',
    'tokens.remaining': 'Remaining',
    'tokens.disclaimer': 'Tokens are internal utility credits, NOT cryptocurrency.',
    
    'threads.recent': 'Recent Threads',
    'threads.typeMessage': 'Type a message...',
    
    'nova.systemIntelligence': 'System Intelligence',
    'nova.askNova': 'Ask Nova...',
    'nova.insights': 'Insights',
    'nova.suggestions': 'Suggestions',
    
    'governance.laws': '10 Laws of Governance',
    'governance.audit': 'Audit Log',
    
    'settings.appearance': 'Appearance',
    'settings.theme': 'Theme',
    'settings.light': 'Light',
    'settings.dark': 'Dark',
    'settings.language': 'Language',
    'settings.governance': 'Governance',
    
    'auth.login': 'Login',
    'auth.register': 'Create Account',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.confirmPassword': 'Confirm Password',
    'auth.name': 'Name',
    'auth.consentTerms': 'I accept the Terms of Service',
    'auth.consentGovernance': 'I accept the 10 Laws of Governance',
    'auth.consentData': 'I consent to data processing',
  },
  fr: {
    'common.welcome': 'Bienvenue',
    'common.logout': 'Déconnexion',
    'common.save': 'Enregistrer',
    'common.cancel': 'Annuler',
    'common.loading': 'Chargement...',
    
    'dashboard.subtitle': 'Votre tableau de bord d\'intelligence gouvernée',
    
    'spheres.title': 'Sphères',
    'spheres.description': 'Choisissez un contexte de travail',
    'spheres.personal.description': 'Gestion personnelle',
    'spheres.business.description': 'Opérations commerciales',
    'spheres.government.description': 'Interactions gouvernementales',
    'spheres.studio.description': 'Projets créatifs',
    'spheres.community.description': 'Engagement communautaire',
    'spheres.social.description': 'Gestion des réseaux sociaux',
    'spheres.entertainment.description': 'Activités de divertissement',
    'spheres.team.description': 'Collaboration d\'équipe',
    
    'tokens.budget': 'Budget de Tokens',
    'tokens.allocated': 'Alloués',
    'tokens.used': 'Utilisés',
    'tokens.remaining': 'Restants',
    'tokens.disclaimer': 'Les tokens sont des crédits utilitaires internes, PAS une cryptomonnaie.',
    
    'threads.recent': 'Threads Récents',
    'threads.typeMessage': 'Tapez un message...',
    
    'nova.systemIntelligence': 'Intelligence Système',
    'nova.askNova': 'Demandez à Nova...',
    'nova.insights': 'Aperçus',
    'nova.suggestions': 'Suggestions',
    
    'governance.laws': '10 Lois de Gouvernance',
    'governance.audit': 'Journal d\'Audit',
    
    'settings.appearance': 'Apparence',
    'settings.theme': 'Thème',
    'settings.light': 'Clair',
    'settings.dark': 'Sombre',
    'settings.language': 'Langue',
    'settings.governance': 'Gouvernance',
    
    'auth.login': 'Connexion',
    'auth.register': 'Créer un compte',
    'auth.email': 'Email',
    'auth.password': 'Mot de passe',
    'auth.confirmPassword': 'Confirmer le mot de passe',
    'auth.name': 'Nom',
    'auth.consentTerms': 'J\'accepte les Conditions d\'Utilisation',
    'auth.consentGovernance': 'J\'accepte les 10 Lois de Gouvernance',
    'auth.consentData': 'Je consens au traitement des données',
  },
  es: {
    'common.welcome': 'Bienvenido',
    'common.logout': 'Cerrar sesión',
    'spheres.title': 'Esferas',
    'tokens.budget': 'Presupuesto de Tokens',
    'tokens.disclaimer': 'Los tokens son créditos de utilidad internos, NO criptomoneda.',
    'nova.systemIntelligence': 'Inteligencia del Sistema',
    // ... add more translations
  },
  de: {
    'common.welcome': 'Willkommen',
    'spheres.title': 'Sphären',
    'tokens.disclaimer': 'Tokens sind interne Nutzungsguthaben, KEINE Kryptowährung.',
    // ... add more translations
  },
  it: {
    'common.welcome': 'Benvenuto',
    'spheres.title': 'Sfere',
    'tokens.disclaimer': 'I token sono crediti di utilità interni, NON criptovaluta.',
    // ... add more translations
  },
  pt: {
    'common.welcome': 'Bem-vindo',
    'spheres.title': 'Esferas',
    'tokens.disclaimer': 'Tokens são créditos utilitários internos, NÃO criptomoeda.',
    // ... add more translations
  },
  zh: {
    'common.welcome': '欢迎',
    'spheres.title': '领域',
    'tokens.disclaimer': '代币是内部实用积分，不是加密货币。',
    // ... add more translations
  },
  ja: {
    'common.welcome': 'ようこそ',
    'spheres.title': 'スフィア',
    'tokens.disclaimer': 'トークンは内部ユーティリティクレジットであり、暗号通貨ではありません。',
    // ... add more translations
  },
  ko: {
    'common.welcome': '환영합니다',
    'spheres.title': '영역',
    'tokens.disclaimer': '토큰은 내부 유틸리티 크레딧이며 암호화폐가 아닙니다.',
    // ... add more translations
  },
  ar: {
    'common.welcome': 'مرحباً',
    'spheres.title': 'المجالات',
    'tokens.disclaimer': 'الرموز هي اعتمادات مرافق داخلية، وليست عملة مشفرة.',
    // ... add more translations
  },
};

const I18nContext = createContext<I18nContextType | undefined>(undefined);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<SupportedLanguage>('en');

  useEffect(() => {
    loadLanguagePreference();
  }, []);

  const loadLanguagePreference = async () => {
    try {
      const savedLang = await AsyncStorage.getItem('language');
      if (savedLang && savedLang in translations) {
        setLanguageState(savedLang as SupportedLanguage);
      } else {
        // Use device locale
        const deviceLang = Localization.locale.split('-')[0] as SupportedLanguage;
        if (deviceLang in translations) {
          setLanguageState(deviceLang);
        }
      }
    } catch (error) {
      console.error('Error loading language:', error);
    }
  };

  const setLanguage = async (lang: SupportedLanguage) => {
    setLanguageState(lang);
    await AsyncStorage.setItem('language', lang);
  };

  const t = (key: string, params?: Record<string, string>): string => {
    let translation = translations[language][key] || translations['en'][key] || key;
    
    if (params) {
      Object.entries(params).forEach(([param, value]) => {
        translation = translation.replace(`{${param}}`, value);
      });
    }
    
    return translation;
  };

  return (
    <I18nContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
}

// ============================================================
// EXPORTS
// ============================================================

export default {
  AuthProvider,
  useAuth,
  ThemeProvider,
  useTheme,
  I18nProvider,
  useI18n,
};
