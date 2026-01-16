// ═══════════════════════════════════════════════════════════════════════════
// AT·OM NOTIFICATION TOAST
// Toast notifications system
// ═══════════════════════════════════════════════════════════════════════════

import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  Info,
  X,
} from 'lucide-react';
import { useAtomStore } from '@/stores/atom.store';
import type { Notification } from '@/types';
import { cn } from '@/utils';

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

export function NotificationToastContainer() {
  const notifications = useAtomStore((state) => state.ui.notifications);
  const removeNotification = useAtomStore((state) => state.removeNotification);

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      <AnimatePresence mode="popLayout">
        {notifications.map((notification) => (
          <NotificationToast
            key={notification.id}
            notification={notification}
            onDismiss={() => removeNotification(notification.id)}
          />
        ))}
      </AnimatePresence>
    </div>
  );
}

function NotificationToast({
  notification,
  onDismiss,
}: {
  notification: Notification;
  onDismiss: () => void;
}) {
  // Auto-dismiss after duration
  useEffect(() => {
    if (notification.duration && notification.duration > 0) {
      const timer = setTimeout(onDismiss, notification.duration);
      return () => clearTimeout(timer);
    }
  }, [notification.duration, onDismiss]);

  const icons = {
    success: CheckCircle,
    warning: AlertTriangle,
    error: XCircle,
    info: Info,
  };

  const colors = {
    success: 'bg-emerald-500/20 border-emerald-500/30 text-emerald-400',
    warning: 'bg-yellow-500/20 border-yellow-500/30 text-yellow-400',
    error: 'bg-red-500/20 border-red-500/30 text-red-400',
    info: 'bg-blue-500/20 border-blue-500/30 text-blue-400',
  };

  const Icon = icons[notification.type];

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: 50, scale: 0.9 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 50, scale: 0.9 }}
      className={cn(
        'pointer-events-auto max-w-sm w-full p-4 rounded-xl border backdrop-blur-lg shadow-lg',
        colors[notification.type]
      )}
    >
      <div className="flex items-start gap-3">
        <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-white">{notification.title}</h4>
          {notification.message && (
            <p className="text-sm mt-1 opacity-80">{notification.message}</p>
          )}
          {notification.action && (
            <button
              onClick={notification.action.onClick}
              className="mt-2 text-sm font-medium underline underline-offset-2 hover:no-underline"
            >
              {notification.action.label}
            </button>
          )}
        </div>
        <button
          onClick={onDismiss}
          className="flex-shrink-0 p-1 hover:bg-white/10 rounded transition-colors"
        >
          <X className="w-4 h-4 text-white/60" />
        </button>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HOOK FOR NOTIFICATIONS
// ─────────────────────────────────────────────────────────────────────────────

export function useNotifications() {
  const addNotification = useAtomStore((state) => state.addNotification);
  const removeNotification = useAtomStore((state) => state.removeNotification);
  const clearNotifications = useAtomStore((state) => state.clearNotifications);

  const notify = {
    success: (title: string, message?: string, duration: number = 5000) => {
      addNotification({
        id: crypto.randomUUID(),
        type: 'success',
        title,
        message,
        duration,
        timestamp: new Date(),
      });
    },
    warning: (title: string, message?: string, duration: number = 7000) => {
      addNotification({
        id: crypto.randomUUID(),
        type: 'warning',
        title,
        message,
        duration,
        timestamp: new Date(),
      });
    },
    error: (title: string, message?: string, duration: number = 10000) => {
      addNotification({
        id: crypto.randomUUID(),
        type: 'error',
        title,
        message,
        duration,
        timestamp: new Date(),
      });
    },
    info: (title: string, message?: string, duration: number = 5000) => {
      addNotification({
        id: crypto.randomUUID(),
        type: 'info',
        title,
        message,
        duration,
        timestamp: new Date(),
      });
    },
  };

  return { notify, removeNotification, clearNotifications };
}

export default NotificationToastContainer;
