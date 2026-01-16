// CHE·NU™ Mobile Auth Screens
// Login, Register, Forgot Password with Governance Consent

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Switch,
  Alert,
  Image,
} from 'react-native';
import { useAuth, useTheme, useI18n } from '../providers';

// ============================================================
// LOGIN SCREEN
// ============================================================

export function LoginScreen({ navigation }: { navigation: any }) {
  const { login } = useAuth();
  const { colors } = useTheme();
  const { t } = useI18n();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) {
      setError(t('auth.fillAllFields'));
      return;
    }

    setIsLoading(true);
    setError(null);

    const result = await login(email.trim(), password);

    setIsLoading(false);

    if (!result.success) {
      setError(result.error || t('auth.loginFailed'));
    }
  };

  const styles = createStyles(colors);

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        {/* Logo */}
        <View style={styles.logoContainer}>
          <View style={styles.logoPlaceholder}>
            <Text style={styles.logoText}>🏠</Text>
          </View>
          <Text style={styles.title}>CHE·NU™</Text>
          <Text style={styles.subtitle}>{t('auth.governedIntelligence')}</Text>
        </View>

        {/* Login Form */}
        <View style={styles.formContainer}>
          <Text style={styles.formTitle}>{t('auth.welcomeBack')}</Text>

          {/* Error Message */}
          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Email Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.email')}</Text>
            <TextInput
              style={styles.input}
              placeholder="you@example.com"
              placeholderTextColor={colors.textSecondary}
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
          </View>

          {/* Password Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.password')}</Text>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[styles.input, styles.passwordInput]}
                placeholder="••••••••"
                placeholderTextColor={colors.textSecondary}
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                editable={!isLoading}
              />
              <TouchableOpacity
                style={styles.showPasswordButton}
                onPress={() => setShowPassword(!showPassword)}
              >
                <Text style={styles.showPasswordText}>
                  {showPassword ? '🙈' : '👁️'}
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Forgot Password */}
          <TouchableOpacity
            style={styles.forgotPassword}
            onPress={() => navigation.navigate('ForgotPassword')}
          >
            <Text style={styles.forgotPasswordText}>
              {t('auth.forgotPassword')}
            </Text>
          </TouchableOpacity>

          {/* Login Button */}
          <TouchableOpacity
            style={[styles.primaryButton, isLoading && styles.buttonDisabled]}
            onPress={handleLogin}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.primaryButtonText}>{t('auth.login')}</Text>
            )}
          </TouchableOpacity>

          {/* Divider */}
          <View style={styles.divider}>
            <View style={styles.dividerLine} />
            <Text style={styles.dividerText}>{t('auth.or')}</Text>
            <View style={styles.dividerLine} />
          </View>

          {/* Register Link */}
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Register')}
          >
            <Text style={styles.secondaryButtonText}>
              {t('auth.createAccount')}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            {t('auth.byLoggingIn')}
          </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Terms')}>
            <Text style={styles.footerLink}>{t('auth.termsOfService')}</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

// ============================================================
// REGISTER SCREEN
// ============================================================

export function RegisterScreen({ navigation }: { navigation: any }) {
  const { register } = useAuth();
  const { colors } = useTheme();
  const { t } = useI18n();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  // Memory Prompt: Governance consent REQUIRED
  const [consents, setConsents] = useState({
    terms: false,
    governance: false,
    dataProcessing: false,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const updateFormData = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const toggleConsent = (field: keyof typeof consents) => {
    setConsents(prev => ({ ...prev, [field]: !prev[field] }));
  };

  const validateForm = (): string | null => {
    if (!formData.name.trim()) return t('auth.nameRequired');
    if (!formData.email.trim()) return t('auth.emailRequired');
    if (!formData.password) return t('auth.passwordRequired');
    if (formData.password.length < 8) return t('auth.passwordMinLength');
    if (formData.password !== formData.confirmPassword) {
      return t('auth.passwordsMustMatch');
    }

    // Memory Prompt: ALL governance consents required
    if (!consents.terms) return t('auth.mustAcceptTerms');
    if (!consents.governance) return t('auth.mustAcceptGovernance');
    if (!consents.dataProcessing) return t('auth.mustAcceptDataProcessing');

    return null;
  };

  const handleRegister = async () => {
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);
    setError(null);

    const result = await register({
      name: formData.name.trim(),
      email: formData.email.trim(),
      password: formData.password,
      consentTerms: consents.terms,
      consentGovernance: consents.governance,
      consentDataProcessing: consents.dataProcessing,
    });

    setIsLoading(false);

    if (result.success) {
      Alert.alert(
        t('auth.registrationSuccess'),
        t('auth.pleaseCheckEmail'),
        [{ text: 'OK', onPress: () => navigation.navigate('Login') }]
      );
    } else {
      setError(result.error || t('auth.registrationFailed'));
    }
  };

  const styles = createStyles(colors);

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>{t('auth.createAccount')}</Text>
          <View style={styles.backButton} />
        </View>

        {/* Form */}
        <View style={styles.formContainer}>
          {/* Error Message */}
          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Name Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.name')}</Text>
            <TextInput
              style={styles.input}
              placeholder={t('auth.yourName')}
              placeholderTextColor={colors.textSecondary}
              value={formData.name}
              onChangeText={(v) => updateFormData('name', v)}
              autoCapitalize="words"
              editable={!isLoading}
            />
          </View>

          {/* Email Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.email')}</Text>
            <TextInput
              style={styles.input}
              placeholder="you@example.com"
              placeholderTextColor={colors.textSecondary}
              value={formData.email}
              onChangeText={(v) => updateFormData('email', v)}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
          </View>

          {/* Password Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.password')}</Text>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[styles.input, styles.passwordInput]}
                placeholder="••••••••"
                placeholderTextColor={colors.textSecondary}
                value={formData.password}
                onChangeText={(v) => updateFormData('password', v)}
                secureTextEntry={!showPassword}
                editable={!isLoading}
              />
              <TouchableOpacity
                style={styles.showPasswordButton}
                onPress={() => setShowPassword(!showPassword)}
              >
                <Text style={styles.showPasswordText}>
                  {showPassword ? '🙈' : '👁️'}
                </Text>
              </TouchableOpacity>
            </View>
            <Text style={styles.inputHint}>{t('auth.passwordHint')}</Text>
          </View>

          {/* Confirm Password Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.confirmPassword')}</Text>
            <TextInput
              style={styles.input}
              placeholder="••••••••"
              placeholderTextColor={colors.textSecondary}
              value={formData.confirmPassword}
              onChangeText={(v) => updateFormData('confirmPassword', v)}
              secureTextEntry={!showPassword}
              editable={!isLoading}
            />
          </View>

          {/* Governance Consents Section */}
          <View style={styles.consentsSection}>
            <Text style={styles.consentsSectionTitle}>
              ⚖️ {t('auth.governanceConsents')}
            </Text>
            <Text style={styles.consentsSectionSubtitle}>
              {t('auth.allConsentsRequired')}
            </Text>

            {/* Terms Consent */}
            <TouchableOpacity
              style={styles.consentRow}
              onPress={() => toggleConsent('terms')}
            >
              <Switch
                value={consents.terms}
                onValueChange={() => toggleConsent('terms')}
                trackColor={{ false: colors.border, true: colors.primary }}
                thumbColor="#FFFFFF"
              />
              <View style={styles.consentTextContainer}>
                <Text style={styles.consentText}>
                  {t('auth.acceptTerms')}
                </Text>
                <TouchableOpacity
                  onPress={() => navigation.navigate('Terms')}
                >
                  <Text style={styles.consentLink}>{t('auth.viewTerms')}</Text>
                </TouchableOpacity>
              </View>
            </TouchableOpacity>

            {/* Governance Consent (Memory Prompt: 10 Laws) */}
            <TouchableOpacity
              style={styles.consentRow}
              onPress={() => toggleConsent('governance')}
            >
              <Switch
                value={consents.governance}
                onValueChange={() => toggleConsent('governance')}
                trackColor={{ false: colors.border, true: colors.primary }}
                thumbColor="#FFFFFF"
              />
              <View style={styles.consentTextContainer}>
                <Text style={styles.consentText}>
                  {t('auth.acceptGovernance')}
                </Text>
                <TouchableOpacity
                  onPress={() => navigation.navigate('GovernanceLaws')}
                >
                  <Text style={styles.consentLink}>
                    {t('auth.view10Laws')}
                  </Text>
                </TouchableOpacity>
              </View>
            </TouchableOpacity>

            {/* Data Processing Consent */}
            <TouchableOpacity
              style={styles.consentRow}
              onPress={() => toggleConsent('dataProcessing')}
            >
              <Switch
                value={consents.dataProcessing}
                onValueChange={() => toggleConsent('dataProcessing')}
                trackColor={{ false: colors.border, true: colors.primary }}
                thumbColor="#FFFFFF"
              />
              <View style={styles.consentTextContainer}>
                <Text style={styles.consentText}>
                  {t('auth.acceptDataProcessing')}
                </Text>
                <TouchableOpacity
                  onPress={() => navigation.navigate('Privacy')}
                >
                  <Text style={styles.consentLink}>
                    {t('auth.viewPrivacy')}
                  </Text>
                </TouchableOpacity>
              </View>
            </TouchableOpacity>
          </View>

          {/* Register Button */}
          <TouchableOpacity
            style={[styles.primaryButton, isLoading && styles.buttonDisabled]}
            onPress={handleRegister}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.primaryButtonText}>
                {t('auth.createAccount')}
              </Text>
            )}
          </TouchableOpacity>

          {/* Login Link */}
          <View style={styles.linkContainer}>
            <Text style={styles.linkText}>{t('auth.alreadyHaveAccount')}</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Login')}>
              <Text style={styles.link}>{t('auth.login')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

// ============================================================
// FORGOT PASSWORD SCREEN
// ============================================================

export function ForgotPasswordScreen({ navigation }: { navigation: any }) {
  const { colors } = useTheme();
  const { t } = useI18n();

  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleResetPassword = async () => {
    if (!email.trim()) {
      setError(t('auth.emailRequired'));
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}/auth/forgot-password`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email.trim() }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setSuccess(true);
      } else {
        setError(data.error?.message || t('auth.resetFailed'));
      }
    } catch (err) {
      setError(t('auth.networkError'));
    } finally {
      setIsLoading(false);
    }
  };

  const styles = createStyles(colors);

  if (success) {
    return (
      <View style={styles.container}>
        <View style={styles.successContainer}>
          <Text style={styles.successIcon}>✉️</Text>
          <Text style={styles.successTitle}>{t('auth.checkYourEmail')}</Text>
          <Text style={styles.successText}>
            {t('auth.resetEmailSent', { email })}
          </Text>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => navigation.navigate('Login')}
          >
            <Text style={styles.primaryButtonText}>
              {t('auth.backToLogin')}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>{t('auth.resetPassword')}</Text>
          <View style={styles.backButton} />
        </View>

        {/* Form */}
        <View style={styles.formContainer}>
          <Text style={styles.formDescription}>
            {t('auth.resetPasswordDescription')}
          </Text>

          {/* Error Message */}
          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Email Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>{t('auth.email')}</Text>
            <TextInput
              style={styles.input}
              placeholder="you@example.com"
              placeholderTextColor={colors.textSecondary}
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
          </View>

          {/* Reset Button */}
          <TouchableOpacity
            style={[styles.primaryButton, isLoading && styles.buttonDisabled]}
            onPress={handleResetPassword}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.primaryButtonText}>
                {t('auth.sendResetLink')}
              </Text>
            )}
          </TouchableOpacity>

          {/* Back to Login */}
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Login')}
          >
            <Text style={styles.secondaryButtonText}>
              {t('auth.backToLogin')}
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

// ============================================================
// GOVERNANCE LAWS SCREEN (Memory Prompt: 10 Laws)
// ============================================================

export function GovernanceLawsScreen({ navigation }: { navigation: any }) {
  const { colors } = useTheme();
  const { t } = useI18n();

  const styles = createStyles(colors);

  // Memory Prompt: The 10 Laws
  const laws = [
    { number: 1, name: 'Consent Primacy', icon: '✋', description: 'User consent before any action' },
    { number: 2, name: 'Temporal Sovereignty', icon: '⏰', description: 'User controls their time' },
    { number: 3, name: 'Contextual Fidelity', icon: '🎯', description: 'Respect sphere boundaries' },
    { number: 4, name: 'Hierarchical Respect', icon: '📊', description: 'Honor permission levels' },
    { number: 5, name: 'Audit Completeness', icon: '📝', description: 'Log all actions' },
    { number: 6, name: 'Encoding Transparency', icon: '🔐', description: 'Clear token optimization' },
    { number: 7, name: 'Agent Non-Autonomy', icon: '🤖', description: 'Agents never act alone' },
    { number: 8, name: 'Budget Accountability', icon: '💰', description: 'Respect token budgets' },
    { number: 9, name: 'Cross-Sphere Isolation', icon: '🔒', description: 'Data stays in context' },
    { number: 10, name: 'Deletion Completeness', icon: '🗑️', description: 'Full data removal on request' },
  ];

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>⚖️ {t('governance.10Laws')}</Text>
        <View style={styles.backButton} />
      </View>

      <ScrollView style={styles.lawsContainer}>
        <Text style={styles.lawsIntro}>
          {t('governance.lawsIntro')}
        </Text>

        {laws.map((law) => (
          <View key={law.number} style={styles.lawCard}>
            <View style={styles.lawHeader}>
              <Text style={styles.lawIcon}>{law.icon}</Text>
              <View style={styles.lawTitleContainer}>
                <Text style={styles.lawNumber}>Law {law.number}</Text>
                <Text style={styles.lawName}>{law.name}</Text>
              </View>
            </View>
            <Text style={styles.lawDescription}>{law.description}</Text>
          </View>
        ))}

        <View style={styles.lawsFooter}>
          <Text style={styles.lawsFooterText}>
            {t('governance.footerText')}
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}

// ============================================================
// STYLES
// ============================================================

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  logoPlaceholder: {
    width: 80,
    height: 80,
    borderRadius: 20,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  logoText: {
    fontSize: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  formContainer: {
    flex: 1,
  },
  formTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 24,
  },
  formDescription: {
    fontSize: 16,
    color: colors.textSecondary,
    marginBottom: 24,
    lineHeight: 22,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  backButton: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  backButtonText: {
    fontSize: 24,
    color: colors.text,
  },
  inputContainer: {
    marginBottom: 20,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: colors.text,
    marginBottom: 8,
  },
  input: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: colors.text,
  },
  inputHint: {
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 6,
  },
  passwordContainer: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 50,
  },
  showPasswordButton: {
    position: 'absolute',
    right: 16,
    top: 14,
  },
  showPasswordText: {
    fontSize: 20,
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginBottom: 24,
  },
  forgotPasswordText: {
    fontSize: 14,
    color: colors.primary,
    fontWeight: '500',
  },
  primaryButton: {
    backgroundColor: colors.primary,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 16,
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: colors.primary,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: '600',
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 24,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: colors.border,
  },
  dividerText: {
    marginHorizontal: 16,
    color: colors.textSecondary,
    fontSize: 14,
  },
  errorContainer: {
    backgroundColor: '#FFEBEE',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  errorText: {
    color: '#D32F2F',
    fontSize: 14,
  },
  footer: {
    marginTop: 'auto',
    alignItems: 'center',
    paddingTop: 24,
  },
  footerText: {
    fontSize: 12,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  footerLink: {
    fontSize: 12,
    color: colors.primary,
    fontWeight: '500',
    marginTop: 4,
  },
  linkContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  linkText: {
    color: colors.textSecondary,
    fontSize: 14,
  },
  link: {
    color: colors.primary,
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 4,
  },
  consentsSection: {
    marginVertical: 24,
    padding: 16,
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
  },
  consentsSectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 4,
  },
  consentsSectionSubtitle: {
    fontSize: 12,
    color: colors.textSecondary,
    marginBottom: 16,
  },
  consentRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  consentTextContainer: {
    flex: 1,
    marginLeft: 12,
  },
  consentText: {
    fontSize: 14,
    color: colors.text,
    marginBottom: 2,
  },
  consentLink: {
    fontSize: 12,
    color: colors.primary,
  },
  successContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  successIcon: {
    fontSize: 64,
    marginBottom: 24,
  },
  successTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 16,
    textAlign: 'center',
  },
  successText: {
    fontSize: 16,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 22,
  },
  lawsContainer: {
    flex: 1,
    padding: 16,
  },
  lawsIntro: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 20,
    lineHeight: 20,
  },
  lawCard: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: colors.border,
  },
  lawHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  lawIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  lawTitleContainer: {
    flex: 1,
  },
  lawNumber: {
    fontSize: 12,
    color: colors.primary,
    fontWeight: '600',
  },
  lawName: {
    fontSize: 16,
    color: colors.text,
    fontWeight: '600',
  },
  lawDescription: {
    fontSize: 14,
    color: colors.textSecondary,
    lineHeight: 20,
  },
  lawsFooter: {
    padding: 16,
    marginTop: 8,
    marginBottom: 32,
  },
  lawsFooterText: {
    fontSize: 14,
    color: colors.textSecondary,
    fontStyle: 'italic',
    textAlign: 'center',
  },
});

// ============================================================
// EXPORTS
// ============================================================

export default {
  LoginScreen,
  RegisterScreen,
  ForgotPasswordScreen,
  GovernanceLawsScreen,
};
