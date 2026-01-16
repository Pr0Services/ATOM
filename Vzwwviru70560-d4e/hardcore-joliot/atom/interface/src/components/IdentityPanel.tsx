// ═══════════════════════════════════════════════════════════════════════════
// AT·OM IDENTITY PANEL
// Split Identity management - Zero-knowledge sovereign identity
// ═══════════════════════════════════════════════════════════════════════════

import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  User,
  Shield,
  Key,
  Copy,
  Check,
  Eye,
  EyeOff,
  Download,
  Upload,
  RefreshCw,
  AlertTriangle,
  Lock,
  Fingerprint,
} from 'lucide-react';
import { useAtomStore } from '@/stores/atom.store';
import {
  createSplitIdentity,
  saveIdentitySecurely,
  exportAllData,
} from '@/services';
import type { SplitIdentity } from '@/types';
import { cn } from '@/utils';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

interface IdentityPanelProps {
  onClose: () => void;
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

export function IdentityPanel({ onClose }: IdentityPanelProps) {
  const identity = useAtomStore((state) => state.identity);
  const setIdentity = useAtomStore((state) => state.setIdentity);
  const [activeTab, setActiveTab] = useState<'overview' | 'security' | 'export'>('overview');
  const [showCreateModal, setShowCreateModal] = useState(!identity);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-2xl max-h-[85vh] bg-slate-900 rounded-2xl border border-white/10 overflow-hidden flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-atom-600/20 flex items-center justify-center">
              <Fingerprint className="w-6 h-6 text-atom-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Identité Souveraine</h2>
              <p className="text-sm text-white/50">Split Identity • Zero-Knowledge</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white/60" />
          </button>
        </div>

        {identity ? (
          <>
            {/* Tabs */}
            <div className="flex border-b border-white/10">
              {[
                { id: 'overview', label: 'Identité', icon: User },
                { id: 'security', label: 'Sécurité', icon: Shield },
                { id: 'export', label: 'Export', icon: Download },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as typeof activeTab)}
                  className={cn(
                    'flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors',
                    activeTab === tab.id
                      ? 'text-white border-b-2 border-atom-500'
                      : 'text-white/50 hover:text-white/70'
                  )}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              <AnimatePresence mode="wait">
                {activeTab === 'overview' && (
                  <OverviewTab key="overview" identity={identity} />
                )}
                {activeTab === 'security' && (
                  <SecurityTab key="security" identity={identity} />
                )}
                {activeTab === 'export' && (
                  <ExportTab key="export" identity={identity} />
                )}
              </AnimatePresence>
            </div>
          </>
        ) : (
          <div className="flex-1 p-6">
            <CreateIdentityPrompt onCreateIdentity={setIdentity} />
          </div>
        )}

        {/* Create Identity Modal */}
        <AnimatePresence>
          {showCreateModal && !identity && (
            <CreateIdentityModal
              onClose={() => setShowCreateModal(false)}
              onCreated={(newIdentity) => {
                setIdentity(newIdentity);
                setShowCreateModal(false);
              }}
            />
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// OVERVIEW TAB
// ─────────────────────────────────────────────────────────────────────────────

function OverviewTab({ identity }: { identity: SplitIdentity }) {
  const [copied, setCopied] = useState(false);

  const copyPublicId = useCallback(() => {
    navigator.clipboard.writeText(identity.publicId);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [identity.publicId]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* Public ID */}
      <div className="p-4 bg-white/5 rounded-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-white/60">Identifiant Public</span>
          <button
            onClick={copyPublicId}
            className="flex items-center gap-1 text-sm text-atom-400 hover:text-atom-300 transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                Copié
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copier
              </>
            )}
          </button>
        </div>
        <div className="font-mono text-lg text-white bg-black/30 rounded-lg p-3 break-all">
          {identity.publicId}
        </div>
        <p className="text-xs text-white/40 mt-2">
          Cet identifiant peut être partagé publiquement. Il ne révèle aucune information personnelle.
        </p>
      </div>

      {/* Identity Info */}
      <div className="grid grid-cols-2 gap-4">
        <InfoCard
          icon={Key}
          label="Clé publique"
          value={truncateKey(identity.publicKey)}
          color="blue"
        />
        <InfoCard
          icon={Lock}
          label="Statut"
          value="Sécurisé"
          color="green"
        />
      </div>

      {/* Creation Date */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h3 className="text-sm font-medium text-white/60 mb-3">Informations</h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-white/50">Créé le</span>
            <span className="text-white">
              {new Date(identity.createdAt).toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
              })}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-white/50">Type</span>
            <span className="text-white">Split Identity (NaCl)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-white/50">Récupération</span>
            <span className={identity.recoveryEnabled ? 'text-emerald-400' : 'text-yellow-400'}>
              {identity.recoveryEnabled ? 'Activée' : 'Non configurée'}
            </span>
          </div>
        </div>
      </div>

      {/* Security Notice */}
      <div className="p-4 bg-atom-600/10 border border-atom-500/20 rounded-xl">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-atom-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-atom-300">Souveraineté des données</h4>
            <p className="text-sm text-white/60 mt-1">
              Votre clé privée ne quitte jamais votre appareil. Toutes vos données sont chiffrées 
              localement avec cette clé. Nous n'avons aucun accès à vos informations.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SECURITY TAB
// ─────────────────────────────────────────────────────────────────────────────

function SecurityTab({ identity }: { identity: SplitIdentity }) {
  const [showPrivateKey, setShowPrivateKey] = useState(false);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSaveWithPassword = async () => {
    if (password !== confirmPassword) {
      alert('Les mots de passe ne correspondent pas');
      return;
    }
    if (password.length < 8) {
      alert('Le mot de passe doit contenir au moins 8 caractères');
      return;
    }

    setSaving(true);
    try {
      await saveIdentitySecurely(identity, password);
      alert('Identité sauvegardée avec succès');
      setPassword('');
      setConfirmPassword('');
    } catch (error) {
      console.error('Save error:', error);
      alert('Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* Private Key (Hidden) */}
      <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2 text-red-400">
            <AlertTriangle className="w-5 h-5" />
            <span className="font-medium">Clé privée</span>
          </div>
          <button
            onClick={() => setShowPrivateKey(!showPrivateKey)}
            className="flex items-center gap-1 text-sm text-white/50 hover:text-white/70"
          >
            {showPrivateKey ? (
              <>
                <EyeOff className="w-4 h-4" />
                Masquer
              </>
            ) : (
              <>
                <Eye className="w-4 h-4" />
                Afficher
              </>
            )}
          </button>
        </div>
        
        {showPrivateKey ? (
          <div className="font-mono text-sm text-white bg-black/30 rounded-lg p-3 break-all">
            {identity.privateKey}
          </div>
        ) : (
          <div className="font-mono text-sm text-white/30 bg-black/30 rounded-lg p-3">
            ••••••••••••••••••••••••••••••••••••••••••••••••••••
          </div>
        )}
        
        <p className="text-xs text-red-300/60 mt-2">
          ⚠️ Ne partagez JAMAIS votre clé privée. Quiconque la possède a accès à toutes vos données.
        </p>
      </div>

      {/* Password Protection */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h3 className="text-sm font-medium text-white/60 mb-4">Protection par mot de passe</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-white/50 mb-1">Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Minimum 8 caractères"
              className="w-full bg-black/30 border border-white/10 rounded-lg px-4 py-2 text-white placeholder:text-white/30 focus:border-atom-500 focus:outline-none"
            />
          </div>
          
          <div>
            <label className="block text-sm text-white/50 mb-1">Confirmer</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirmer le mot de passe"
              className="w-full bg-black/30 border border-white/10 rounded-lg px-4 py-2 text-white placeholder:text-white/30 focus:border-atom-500 focus:outline-none"
            />
          </div>

          <button
            onClick={handleSaveWithPassword}
            disabled={saving || !password || password !== confirmPassword}
            className={cn(
              'w-full py-2 rounded-lg font-medium transition-colors',
              saving || !password || password !== confirmPassword
                ? 'bg-white/10 text-white/30 cursor-not-allowed'
                : 'bg-atom-600 hover:bg-atom-700 text-white'
            )}
          >
            {saving ? 'Sauvegarde...' : 'Sauvegarder avec mot de passe'}
          </button>
        </div>
      </div>

      {/* Recovery Setup */}
      <div className="p-4 bg-white/5 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium text-white">Récupération</h3>
            <p className="text-sm text-white/50">
              Configurer une phrase de récupération
            </p>
          </div>
          <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm text-white transition-colors">
            Configurer
          </button>
        </div>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// EXPORT TAB
// ─────────────────────────────────────────────────────────────────────────────

function ExportTab({ identity }: { identity: SplitIdentity }) {
  const [exporting, setExporting] = useState(false);

  const handleExportData = async () => {
    setExporting(true);
    try {
      const data = await exportAllData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `atom-backup-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export error:', error);
      alert('Erreur lors de l\'export');
    } finally {
      setExporting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* Export Data */}
      <div className="p-6 bg-white/5 rounded-xl text-center">
        <Download className="w-12 h-12 mx-auto text-atom-400 mb-4" />
        <h3 className="text-lg font-medium text-white mb-2">Exporter vos données</h3>
        <p className="text-sm text-white/50 mb-6">
          Téléchargez une copie complète de toutes vos données au format JSON.
          Vos données sont chiffrées avec votre clé privée.
        </p>
        <button
          onClick={handleExportData}
          disabled={exporting}
          className={cn(
            'px-6 py-3 rounded-lg font-medium transition-colors',
            exporting
              ? 'bg-white/10 text-white/30 cursor-not-allowed'
              : 'bg-atom-600 hover:bg-atom-700 text-white'
          )}
        >
          {exporting ? (
            <span className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4 animate-spin" />
              Export en cours...
            </span>
          ) : (
            'Télécharger backup'
          )}
        </button>
      </div>

      {/* Import Data */}
      <div className="p-6 bg-white/5 rounded-xl text-center">
        <Upload className="w-12 h-12 mx-auto text-white/30 mb-4" />
        <h3 className="text-lg font-medium text-white mb-2">Importer des données</h3>
        <p className="text-sm text-white/50 mb-6">
          Restaurez vos données à partir d'un fichier de backup.
        </p>
        <label className="px-6 py-3 rounded-lg font-medium bg-white/10 hover:bg-white/20 text-white cursor-pointer transition-colors inline-block">
          <input type="file" accept=".json" className="hidden" />
          Sélectionner un fichier
        </label>
      </div>

      {/* Danger Zone */}
      <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
        <h3 className="text-sm font-medium text-red-400 mb-3">Zone dangereuse</h3>
        <p className="text-sm text-white/50 mb-4">
          Supprimer votre identité et toutes vos données locales. Cette action est irréversible.
        </p>
        <button className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-sm text-red-400 transition-colors">
          Supprimer mon identité
        </button>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// CREATE IDENTITY
// ─────────────────────────────────────────────────────────────────────────────

function CreateIdentityPrompt({ onCreateIdentity }: { onCreateIdentity: (identity: SplitIdentity) => void }) {
  const [creating, setCreating] = useState(false);

  const handleCreate = async () => {
    setCreating(true);
    try {
      const identity = await createSplitIdentity();
      onCreateIdentity(identity);
    } catch (error) {
      console.error('Create identity error:', error);
      alert('Erreur lors de la création');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="text-center py-12">
      <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-atom-600/20 flex items-center justify-center">
        <Fingerprint className="w-10 h-10 text-atom-400" />
      </div>
      
      <h3 className="text-xl font-bold text-white mb-2">Créer votre identité</h3>
      <p className="text-white/50 max-w-md mx-auto mb-8">
        Votre identité AT·OM est unique et souveraine. Elle vous permet de contrôler 
        vos données de manière sécurisée et privée.
      </p>

      <div className="space-y-4 max-w-sm mx-auto text-left mb-8">
        <FeatureItem icon={Shield} text="Chiffrement de bout en bout" />
        <FeatureItem icon={Key} text="Clés générées localement" />
        <FeatureItem icon={Lock} text="Zero-knowledge design" />
      </div>

      <button
        onClick={handleCreate}
        disabled={creating}
        className={cn(
          'px-8 py-3 rounded-xl font-medium transition-all',
          creating
            ? 'bg-white/10 text-white/30 cursor-not-allowed'
            : 'bg-gradient-to-r from-atom-600 to-atom-500 hover:from-atom-500 hover:to-atom-400 text-white shadow-lg shadow-atom-500/25'
        )}
      >
        {creating ? (
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin" />
            Génération...
          </span>
        ) : (
          'Créer mon identité'
        )}
      </button>
    </div>
  );
}

function CreateIdentityModal({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: (identity: SplitIdentity) => void;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="absolute inset-0 bg-slate-900 flex items-center justify-center p-6"
    >
      <CreateIdentityPrompt onCreateIdentity={onCreated} />
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HELPER COMPONENTS
// ─────────────────────────────────────────────────────────────────────────────

function InfoCard({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  color: 'blue' | 'green' | 'purple';
}) {
  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    green: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  };

  return (
    <div className={cn('p-4 rounded-xl border', colorClasses[color])}>
      <Icon className="w-5 h-5 mb-2" />
      <div className="text-xs opacity-70 mb-1">{label}</div>
      <div className="font-mono text-sm truncate">{value}</div>
    </div>
  );
}

function FeatureItem({ icon: Icon, text }: { icon: React.ElementType; text: string }) {
  return (
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-atom-600/20 flex items-center justify-center">
        <Icon className="w-4 h-4 text-atom-400" />
      </div>
      <span className="text-white/70">{text}</span>
    </div>
  );
}

function truncateKey(key: string): string {
  if (key.length <= 16) return key;
  return `${key.slice(0, 8)}...${key.slice(-8)}`;
}

export default IdentityPanel;
