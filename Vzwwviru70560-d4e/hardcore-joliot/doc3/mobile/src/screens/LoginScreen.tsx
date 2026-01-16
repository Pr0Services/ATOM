// CHE·NU Mobile - Login Screen
// Simple: Google, Microsoft, Email, Sign up, Forgot password

import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  KeyboardAvoidingView, Platform, Alert, ActivityIndicator,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography } from '../theme';
import { useAuthStore } from '../store';

export default function LoginScreen() {
  const navigation = useNavigation<any>();
  const { login, isLoading } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleEmailLogin = async () => {
    if (!email || !password) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }
    try {
      await login(email, password);
    } catch (error: any) {
      Alert.alert('Erreur', error.message || 'Connexion échouée');
    }
  };

  const handleGoogleLogin = () => {
    // Demo: direct login
    useAuthStore.setState({
      user: {
        id: 'google_user',
        email: 'user@gmail.com',
        name: 'Jo',
        role: 'admin',
        preferences: { theme: 'dark', language: 'fr', notifications: true, defaultSphere: 'personal' },
        created_at: new Date().toISOString(),
      },
      token: 'google_token',
      isAuthenticated: true,
      isLoading: false,
    });
  };

  const handleMicrosoftLogin = () => {
    // Demo: direct login
    useAuthStore.setState({
      user: {
        id: 'microsoft_user',
        email: 'user@outlook.com',
        name: 'Jo',
        role: 'admin',
        preferences: { theme: 'dark', language: 'fr', notifications: true, defaultSphere: 'personal' },
        created_at: new Date().toISOString(),
      },
      token: 'microsoft_token',
      isAuthenticated: true,
      isLoading: false,
    });
  };

  return (
    <LinearGradient colors={[colors.background, colors.backgroundSecondary]} style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
        style={styles.content}
      >
        {/* Logo & Branding */}
        <View style={styles.header}>
          <LinearGradient colors={[colors.primary, colors.secondary]} style={styles.logo}>
            <Text style={styles.logoText}>C·N</Text>
          </LinearGradient>
          <Text style={styles.title}>CHE·NU</Text>
          <Text style={styles.tagline}>Governed Intelligence</Text>
          <Text style={styles.taglineSub}>Operating System</Text>
        </View>

        {/* OAuth Buttons */}
        <View style={styles.oauthContainer}>
          <TouchableOpacity style={styles.oauthButton} onPress={handleGoogleLogin}>
            <View style={styles.oauthIconContainer}>
              <Ionicons name="logo-google" size={20} color="#DB4437" />
            </View>
            <Text style={styles.oauthText}>Continuer avec Google</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.oauthButton} onPress={handleMicrosoftLogin}>
            <View style={styles.oauthIconContainer}>
              <Ionicons name="logo-microsoft" size={20} color="#00A4EF" />
            </View>
            <Text style={styles.oauthText}>Continuer avec Microsoft</Text>
          </TouchableOpacity>
        </View>

        {/* Divider */}
        <View style={styles.divider}>
          <View style={styles.dividerLine} />
          <Text style={styles.dividerText}>ou</Text>
          <View style={styles.dividerLine} />
        </View>

        {/* Email/Password Form */}
        <View style={styles.form}>
          <View style={styles.inputContainer}>
            <Ionicons name="mail-outline" size={20} color={colors.textMuted} />
            <TextInput
              style={styles.input}
              placeholder="Email"
              placeholderTextColor={colors.textMuted}
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoComplete="email"
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={20} color={colors.textMuted} />
            <TextInput
              style={styles.input}
              placeholder="Mot de passe"
              placeholderTextColor={colors.textMuted}
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              autoComplete="password"
            />
            <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
              <Ionicons 
                name={showPassword ? 'eye-off-outline' : 'eye-outline'} 
                size={20} 
                color={colors.textMuted} 
              />
            </TouchableOpacity>
          </View>

          {/* Forgot Password */}
          <TouchableOpacity 
            style={styles.forgotButton}
            onPress={() => navigation.navigate('ForgotPassword')}
          >
            <Text style={styles.forgotText}>Mot de passe oublié?</Text>
          </TouchableOpacity>

          {/* Login Button */}
          <TouchableOpacity 
            style={styles.loginButton} 
            onPress={handleEmailLogin} 
            disabled={isLoading}
          >
            <LinearGradient 
              colors={[colors.primary, colors.primaryDark]} 
              style={styles.loginButtonGradient}
            >
              {isLoading ? (
                <ActivityIndicator color={colors.text} />
              ) : (
                <Text style={styles.loginButtonText}>Se connecter</Text>
              )}
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Sign Up Link */}
        <View style={styles.signupContainer}>
          <Text style={styles.signupText}>Pas encore de compte? </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Register')}>
            <Text style={styles.signupLink}>S'inscrire</Text>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <Text style={styles.footer}>
          En continuant, vous acceptez nos{'\n'}
          <Text style={styles.footerLink}>Conditions d'utilisation</Text> et{' '}
          <Text style={styles.footerLink}>Politique de confidentialité</Text>
        </Text>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: spacing.xl,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xxl,
  },
  logo: {
    width: 80,
    height: 80,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  logoText: {
    color: colors.text,
    fontSize: 28,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  title: {
    color: colors.text,
    fontSize: 36,
    fontWeight: 'bold',
    letterSpacing: 3,
  },
  tagline: {
    color: colors.primary,
    fontSize: typography.fontSize.lg,
    fontWeight: '600',
    marginTop: spacing.xs,
  },
  taglineSub: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.md,
    marginTop: 2,
  },
  oauthContainer: {
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  oauthButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  oauthIconContainer: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: colors.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  oauthText: {
    color: colors.text,
    fontSize: typography.fontSize.md,
    fontWeight: '500',
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: spacing.lg,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: colors.border,
  },
  dividerText: {
    color: colors.textMuted,
    fontSize: typography.fontSize.sm,
    marginHorizontal: spacing.md,
  },
  form: {
    gap: spacing.md,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    gap: spacing.sm,
    borderWidth: 1,
    borderColor: colors.border,
  },
  input: {
    flex: 1,
    color: colors.text,
    fontSize: typography.fontSize.md,
    paddingVertical: spacing.md,
  },
  forgotButton: {
    alignSelf: 'flex-end',
  },
  forgotText: {
    color: colors.primary,
    fontSize: typography.fontSize.sm,
  },
  loginButton: {
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    marginTop: spacing.sm,
  },
  loginButtonGradient: {
    paddingVertical: spacing.md,
    alignItems: 'center',
  },
  loginButtonText: {
    color: colors.text,
    fontSize: typography.fontSize.lg,
    fontWeight: 'bold',
  },
  signupContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: spacing.xl,
  },
  signupText: {
    color: colors.textSecondary,
    fontSize: typography.fontSize.md,
  },
  signupLink: {
    color: colors.primary,
    fontSize: typography.fontSize.md,
    fontWeight: 'bold',
  },
  footer: {
    color: colors.textMuted,
    fontSize: typography.fontSize.xs,
    textAlign: 'center',
    marginTop: spacing.xl,
    lineHeight: 18,
  },
  footerLink: {
    color: colors.primary,
  },
});
