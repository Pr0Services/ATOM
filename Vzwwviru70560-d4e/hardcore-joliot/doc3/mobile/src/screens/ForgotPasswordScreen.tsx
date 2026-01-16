// CHE·NU Mobile - Forgot Password Screen
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, borderRadius, typography } from '../theme';

export default function ForgotPasswordScreen() {
  const navigation = useNavigation<any>();
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  const handleReset = () => {
    if (!email) {
      Alert.alert('Erreur', 'Veuillez entrer votre email');
      return;
    }
    setSent(true);
  };

  return (
    <LinearGradient colors={[colors.background, colors.backgroundSecondary]} style={styles.container}>
      <View style={styles.content}>
        {/* Back Button */}
        <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>

        {/* Header */}
        <View style={styles.header}>
          <View style={styles.iconContainer}>
            <Ionicons name={sent ? 'mail' : 'lock-open-outline'} size={48} color={colors.primary} />
          </View>
          <Text style={styles.title}>{sent ? 'Email envoyé!' : 'Mot de passe oublié?'}</Text>
          <Text style={styles.subtitle}>
            {sent 
              ? `Un lien de réinitialisation a été envoyé à ${email}` 
              : 'Entrez votre email pour recevoir un lien de réinitialisation'
            }
          </Text>
        </View>

        {!sent ? (
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
              />
            </View>

            <TouchableOpacity style={styles.button} onPress={handleReset}>
              <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.buttonGradient}>
                <Text style={styles.buttonText}>Envoyer le lien</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.successActions}>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Login')}>
              <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.buttonGradient}>
                <Text style={styles.buttonText}>Retour à la connexion</Text>
              </LinearGradient>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.resendButton} onPress={() => Alert.alert('Info', 'Email renvoyé!')}>
              <Text style={styles.resendText}>Renvoyer l'email</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1, justifyContent: 'center', paddingHorizontal: spacing.xl },
  backButton: { position: 'absolute', top: 60, left: spacing.xl },
  header: { alignItems: 'center', marginBottom: spacing.xxl },
  iconContainer: {
    width: 100, height: 100, borderRadius: 50, backgroundColor: colors.primary + '20',
    justifyContent: 'center', alignItems: 'center', marginBottom: spacing.lg,
  },
  title: { color: colors.text, fontSize: 24, fontWeight: 'bold', textAlign: 'center' },
  subtitle: { color: colors.textSecondary, fontSize: typography.fontSize.md, textAlign: 'center', marginTop: spacing.md, lineHeight: 22 },
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
  successActions: { gap: spacing.md },
  resendButton: { alignItems: 'center', paddingVertical: spacing.md },
  resendText: { color: colors.primary, fontSize: typography.fontSize.md },
});
