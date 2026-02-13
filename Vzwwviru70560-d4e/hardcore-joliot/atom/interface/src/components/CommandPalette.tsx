// ═══════════════════════════════════════════════════════════════════════════
// AT·OM COMMAND PALETTE
// Quick navigation and actions (Cmd+K / Ctrl+K)
// ═══════════════════════════════════════════════════════════════════════════

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  Heart,
  Wallet,
  GraduationCap,
  Building2,
  Zap,
  MessageCircle,
  Scale,
  Truck,
  Utensils,
  Cpu,
  Settings,
  User,
  Shield,
  RefreshCw,
  Download,
  Moon,
  Sun,
  Command,
  ArrowRight,
  Languages,
  Sparkles,
  BookOpen,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAtomStore, SPHERE_CONFIG } from '@/stores/atom.store';
import type { SphereId } from '@/types';
import { cn } from '@/utils';
import { getSphereLabel, getUILabel } from '@/services/navigation-labels.service';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

interface CommandItem {
  id: string;
  label: string;
  description?: string;
  icon: React.ElementType;
  category: 'sphere' | 'action' | 'settings';
  action: () => void;
  keywords?: string[];
}

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

// ─────────────────────────────────────────────────────────────────────────────
// SPHERE ICONS MAPPING
// ─────────────────────────────────────────────────────────────────────────────

const SPHERE_ICONS: Record<SphereId, React.ElementType> = {
  health: Heart,
  finance: Wallet,
  education: GraduationCap,
  governance: Building2,
  energy: Zap,
  communication: MessageCircle,
  justice: Scale,
  logistics: Truck,
  food: Utensils,
  technology: Cpu,
};

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

export function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  
  const setActiveSphere = useAtomStore((state) => state.setActiveSphere);
  const toggleSidebar = useAtomStore((state) => state.toggleSidebar);
  const setTheme = useAtomStore((state) => state.setTheme);
  const setLanguage = useAtomStore((state) => state.setLanguage);
  const setExperienceMode = useAtomStore((state) => state.setExperienceMode);
  const theme = useAtomStore((state) => state.ui.theme);
  const language = useAtomStore((state) => state.ui.language);
  const experienceMode = useAtomStore((state) => state.ui.experienceMode);
  const openModal = useAtomStore((state) => state.openModal);

  // Build command list
  const commands = useMemo<CommandItem[]>(() => {
    const sphereCommands: CommandItem[] = Object.entries(SPHERE_CONFIG).map(([id, config]) => {
      const label = language === 'clair' ? config.name : getSphereLabel(id, 'symbolique');
      const alias = language === 'clair' ? getSphereLabel(id, 'symbolique') : config.name;
      return {
        id: `sphere-${id}`,
        label,
        description: `${alias} — ${config.description}`,
        icon: SPHERE_ICONS[id as SphereId],
        category: 'sphere',
        action: () => {
          setActiveSphere(id as SphereId);
          navigate(`/sphere/${id}`);
          onClose();
        },
        keywords: [config.name.toLowerCase(), id, alias.toLowerCase()],
      };
    });

    const actionCommands: CommandItem[] = [
      {
        id: 'sync',
        label: 'Synchroniser',
        description: 'Synchroniser toutes les données',
        icon: RefreshCw,
        category: 'action',
        action: () => {
          // Trigger sync
          onClose();
        },
        keywords: ['sync', 'synchroniser', 'refresh'],
      },
      {
        id: 'export',
        label: 'Exporter les données',
        description: 'Télécharger une copie de vos données',
        icon: Download,
        category: 'action',
        action: () => {
          openModal('export');
          onClose();
        },
        keywords: ['export', 'download', 'backup'],
      },
    ];

    const settingsCommands: CommandItem[] = [
      {
        id: 'identity',
        label: 'Identité',
        description: 'Gérer votre identité souveraine',
        icon: User,
        category: 'settings',
        action: () => {
          openModal('identity');
          onClose();
        },
        keywords: ['identity', 'identité', 'profile'],
      },
      {
        id: 'security',
        label: 'Sécurité',
        description: 'Paramètres de sécurité',
        icon: Shield,
        category: 'settings',
        action: () => {
          openModal('security');
          onClose();
        },
        keywords: ['security', 'sécurité', 'password'],
      },
      {
        id: 'settings',
        label: 'Paramètres',
        description: 'Paramètres généraux',
        icon: Settings,
        category: 'settings',
        action: () => {
          openModal('settings');
          onClose();
        },
        keywords: ['settings', 'paramètres', 'config'],
      },
      {
        id: 'theme',
        label: theme === 'dark' ? 'Mode clair' : 'Mode sombre',
        description: 'Changer le thème',
        icon: theme === 'dark' ? Sun : Moon,
        category: 'settings',
        action: () => {
          setTheme(theme === 'dark' ? 'light' : 'dark');
          onClose();
        },
        keywords: ['theme', 'dark', 'light', 'mode'],
      },
      {
        id: 'language',
        label: language === 'symbolique' ? 'Mode Clair' : 'Mode Symbolique',
        description: language === 'symbolique'
          ? 'Noms simples et explicites (Accueil, Agents IA...)'
          : 'Noms symboliques AT·OM (Le Sceau, L\'Essaim...)',
        icon: Languages,
        category: 'settings',
        action: () => {
          setLanguage(language === 'symbolique' ? 'clair' : 'symbolique');
          onClose();
        },
        keywords: ['langage', 'language', 'symbolique', 'clair', 'français', 'noms'],
      },
      {
        id: 'experience-mode',
        label: experienceMode === 'debutant' ? 'Mode Expert' : 'Mode Débutant',
        description: experienceMode === 'debutant'
          ? 'Afficher toutes les options avancées'
          : 'Interface simplifiée avec guidage',
        icon: experienceMode === 'debutant' ? Sparkles : BookOpen,
        category: 'settings',
        action: () => {
          setExperienceMode(experienceMode === 'debutant' ? 'expert' : 'debutant');
          onClose();
        },
        keywords: ['expert', 'debutant', 'débutant', 'mode', 'avancé', 'simple'],
      },
    ];

    return [...sphereCommands, ...actionCommands, ...settingsCommands];
  }, [theme, language, experienceMode, setActiveSphere, navigate, onClose, openModal, setTheme, setLanguage, setExperienceMode]);

  // Filter commands based on query
  const filteredCommands = useMemo(() => {
    if (!query) return commands;
    
    const lowerQuery = query.toLowerCase();
    return commands.filter((cmd) => {
      if (cmd.label.toLowerCase().includes(lowerQuery)) return true;
      if (cmd.description?.toLowerCase().includes(lowerQuery)) return true;
      if (cmd.keywords?.some((kw) => kw.includes(lowerQuery))) return true;
      return false;
    });
  }, [commands, query]);

  // Group by category
  const groupedCommands = useMemo(() => {
    const groups: Record<string, CommandItem[]> = {
      sphere: [],
      action: [],
      settings: [],
    };
    
    filteredCommands.forEach((cmd) => {
      groups[cmd.category].push(cmd);
    });
    
    return groups;
  }, [filteredCommands]);

  // Reset selection when query changes
  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
      setQuery('');
    }
  }, [isOpen]);

  // Keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex((i) => Math.min(i + 1, filteredCommands.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex((i) => Math.max(i - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action();
        }
        break;
      case 'Escape':
        e.preventDefault();
        onClose();
        break;
    }
  }, [filteredCommands, selectedIndex, onClose]);

  // Global keyboard shortcut
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) {
          onClose();
        }
      }
    };

    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] px-4 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="w-full max-w-xl bg-slate-900 rounded-2xl border border-white/10 overflow-hidden shadow-2xl"
        >
          {/* Search Input */}
          <div className="flex items-center gap-3 p-4 border-b border-white/10">
            <Search className="w-5 h-5 text-white/40" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Rechercher une commande..."
              className="flex-1 bg-transparent text-white placeholder:text-white/40 focus:outline-none"
            />
            <div className="flex items-center gap-1 px-2 py-1 bg-white/10 rounded text-xs text-white/40">
              <Command className="w-3 h-3" />
              <span>K</span>
            </div>
          </div>

          {/* Results */}
          <div className="max-h-[400px] overflow-y-auto p-2">
            {filteredCommands.length > 0 ? (
              <>
                {/* Spheres */}
                {groupedCommands.sphere.length > 0 && (
                  <CommandGroup label="Sphères">
                    {groupedCommands.sphere.map((cmd, i) => (
                      <CommandRow
                        key={cmd.id}
                        command={cmd}
                        isSelected={filteredCommands.indexOf(cmd) === selectedIndex}
                        onSelect={cmd.action}
                      />
                    ))}
                  </CommandGroup>
                )}

                {/* Actions */}
                {groupedCommands.action.length > 0 && (
                  <CommandGroup label="Actions">
                    {groupedCommands.action.map((cmd) => (
                      <CommandRow
                        key={cmd.id}
                        command={cmd}
                        isSelected={filteredCommands.indexOf(cmd) === selectedIndex}
                        onSelect={cmd.action}
                      />
                    ))}
                  </CommandGroup>
                )}

                {/* Settings */}
                {groupedCommands.settings.length > 0 && (
                  <CommandGroup label="Paramètres">
                    {groupedCommands.settings.map((cmd) => (
                      <CommandRow
                        key={cmd.id}
                        command={cmd}
                        isSelected={filteredCommands.indexOf(cmd) === selectedIndex}
                        onSelect={cmd.action}
                      />
                    ))}
                  </CommandGroup>
                )}
              </>
            ) : (
              <div className="text-center py-12 text-white/40">
                <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Aucun résultat pour "{query}"</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between px-4 py-2 border-t border-white/10 text-xs text-white/40">
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1">
                <span className="px-1.5 py-0.5 bg-white/10 rounded">↑↓</span>
                naviguer
              </span>
              <span className="flex items-center gap-1">
                <span className="px-1.5 py-0.5 bg-white/10 rounded">↵</span>
                sélectionner
              </span>
              <span className="flex items-center gap-1">
                <span className="px-1.5 py-0.5 bg-white/10 rounded">esc</span>
                fermer
              </span>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HELPER COMPONENTS
// ─────────────────────────────────────────────────────────────────────────────

function CommandGroup({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mb-4">
      <div className="px-3 py-2 text-xs font-medium text-white/40 uppercase tracking-wider">
        {label}
      </div>
      {children}
    </div>
  );
}

function CommandRow({
  command,
  isSelected,
  onSelect,
}: {
  command: CommandItem;
  isSelected: boolean;
  onSelect: () => void;
}) {
  const Icon = command.icon;

  return (
    <button
      onClick={onSelect}
      className={cn(
        'w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-left',
        isSelected ? 'bg-atom-600/30 text-white' : 'text-white/70 hover:bg-white/5'
      )}
    >
      <div className={cn(
        'w-8 h-8 rounded-lg flex items-center justify-center',
        isSelected ? 'bg-atom-600/50' : 'bg-white/10'
      )}>
        <Icon className="w-4 h-4" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="font-medium truncate">{command.label}</div>
        {command.description && (
          <div className="text-sm text-white/40 truncate">{command.description}</div>
        )}
      </div>
      {isSelected && <ArrowRight className="w-4 h-4 text-atom-400" />}
    </button>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HOOK FOR COMMAND PALETTE
// ─────────────────────────────────────────────────────────────────────────────

export function useCommandPalette() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return {
    isOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen((prev) => !prev),
  };
}

export default CommandPalette;
