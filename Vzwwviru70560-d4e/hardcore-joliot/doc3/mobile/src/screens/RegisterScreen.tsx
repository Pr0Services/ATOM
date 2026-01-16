// CHE·NU Mobile - Register Screen
import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  KeyboardAvoidingView, Platform, Alert, ScrollView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography } from '../theme';

export default function RegisterScreen() {
  const navigation = useNavigation<any>();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleRegister = () => {
    if (!name || !email || !password || !confirmPassword) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }
    if (password !== confirmPassword) {
      Alert.alert('Erreur', 'Les mots de passe ne correspondent pas');
      return;
    }
    // TODO: Implement registration
    Alert.alert('Succès', 'Compte créé! Vous pouvez maintenant vous connecter.', [
      { text: 'OK', onPress: () => navigation.navigate('Login') }
    ]);
  };

  return (
    <LinearGradient colors={[colors.background, colors.backgroundSecondary]} style={styles.container}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.content}>
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
          {/* Header */}
          <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
            <Ionicons name="arrow-back" size={24} color={colors.text} />
          </TouchableOpacity>

          <View style={styles.header}>
            <Text style={styles.title}>Créer un compte</Text>
            <Text style={styles.subtitle}>Rejoignez CHE·NU</Text>
          </View>

          {/* Form */}
          <View style={styles.form}>
            <View style={styles.inputContainer}>
              <Ionicons name="person-outline" size={20} color={colors.textMuted} />
              <TextInput
                style={styles.input}
                placeholder="Nom complet"
                placeholderTextColor={colors.textMuted}
                value={name}
                onChangeText={setName}
                autoCapitalize="words"
              />
            </View>

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
              />
              <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                <Ionicons name={showPassword ? 'eye-off-outline' : 'eye-outline'} size={20} color={colors.textMuted} />
              </TouchableOpacity>
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="lock-closed-outline" size={20} color={colors.textMuted} />
              <TextInput
                style={styles.input}
                placeholder="Confirmer le mot de passe"
                placeholderTextColor={colors.textMuted}
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                secureTextEntry={!showPassword}
              />
            </View>

            <TouchableOpacity style={styles.button} onPress={handleRegister}>
              <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.buttonGradient}>
                <Text style={styles.buttonText}>S'inscrire</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>

          {/* Login Link */}
          <View style={styles.loginContainer}>
            <Text style={styles.loginText}>Déjà un compte? </Text>
            <TouchableOpacity onPress={() => navigation.navigate('Login')}>
              <Text style={styles.loginLink}>Se connecter</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1 },
  scroll: { flexGrow: 1, justifyContent: 'center', paddingHorizontal: spacing.xl, paddingVertical: spacing.xxl },
  backButton: { position: 'absolute', top: 0 },
  header: { alignItems: 'center', marginBottom: spacing.xxl, marginTop: spacing.xxl },
  title: { color: colors.text, fontSize: 28, fontWeight: 'bold' },
  subtitle: { color: colors.textSecondary, fontSize: typography.fontSize.md, marginTop: spacing.xs },
  form: { gap: spacing.md },
  inputContainer: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface,
    borderRadius: borderRadius.lg, paddingHorizontal: spacing.md, gap: spacing.sm,
    borderWidth: 1, borderColor: colors.border,
  },
  input: { flex: 1, color: colors.text, fontSize: typography.fontSize.md, paddingVertical: spacing.md },
  button: { borderRadius: borderRadius.lg, overflow: 'hidden', marginTop: spacing.md },
  buttonGradient: { paddingVertical: spacing.md, alignItems: 'center' },
  buttonText: { color: colors.text, fontSize: typography.fontSize.lg, fontWeight: 'bold' },
  loginContainer: { flexDirection: 'row', justifyContent: 'center', marginTop: spacing.xl },
  loginText: { color: colors.textSecondary, fontSize: typography.fontSize.md },
  loginLink: { color: colors.primary, fontSize: typography.fontSize.md, fontWeight: 'bold' },
});
