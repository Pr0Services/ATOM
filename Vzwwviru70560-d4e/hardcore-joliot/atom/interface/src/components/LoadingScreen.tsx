// ═══════════════════════════════════════════════════════════════════════════
// AT·OM LOADING SCREEN
// Animated loading screen with AT·OM branding
// ═══════════════════════════════════════════════════════════════════════════

import React from 'react';
import { motion } from 'framer-motion';

interface LoadingScreenProps {
  message?: string;
  progress?: number;
}

export function LoadingScreen({ message = 'Initialisation...', progress }: LoadingScreenProps) {
  return (
    <div className="fixed inset-0 bg-slate-950 flex flex-col items-center justify-center">
      {/* Background gradient */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-radial from-atom-600/10 to-transparent" />
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-radial from-purple-600/10 to-transparent" />
      </div>

      {/* Logo */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="relative mb-8"
      >
        {/* Outer ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
          className="w-32 h-32 rounded-full border-2 border-atom-500/30"
        >
          {/* Orbit dots */}
          {[0, 1, 2, 3].map((i) => (
            <motion.div
              key={i}
              className="absolute w-3 h-3 bg-atom-500 rounded-full"
              style={{
                top: '50%',
                left: '50%',
                transform: `rotate(${i * 90}deg) translateX(60px) translateY(-50%)`,
              }}
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.5,
              }}
            />
          ))}
        </motion.div>

        {/* Inner core */}
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            boxShadow: [
              '0 0 20px rgba(168, 85, 247, 0.3)',
              '0 0 40px rgba(168, 85, 247, 0.5)',
              '0 0 20px rgba(168, 85, 247, 0.3)',
            ],
          }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-gradient-to-br from-atom-500 to-purple-600 rounded-full"
        />

        {/* Center text */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-white font-bold text-lg">
          AT
        </div>
      </motion.div>

      {/* Brand */}
      <motion.h1
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-3xl font-bold text-white mb-2"
      >
        AT·OM
      </motion.h1>

      {/* Message */}
      <motion.p
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="text-white/50 mb-8"
      >
        {message}
      </motion.p>

      {/* Progress bar */}
      {progress !== undefined && (
        <motion.div
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 200, opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="relative h-1 bg-white/10 rounded-full overflow-hidden"
        >
          <motion.div
            initial={{ width: '0%' }}
            animate={{ width: `${progress}%` }}
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-atom-500 to-purple-500"
          />
        </motion.div>
      )}

      {/* Loading dots */}
      {progress === undefined && (
        <div className="flex gap-2">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{
                y: [0, -10, 0],
                opacity: [0.3, 1, 0.3],
              }}
              transition={{
                duration: 0.8,
                repeat: Infinity,
                delay: i * 0.2,
              }}
              className="w-2 h-2 bg-atom-500 rounded-full"
            />
          ))}
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// INLINE LOADING SPINNER
// ─────────────────────────────────────────────────────────────────────────────

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  return (
    <svg
      className={`animate-spin ${sizes[size]} ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SKELETON LOADER
// ─────────────────────────────────────────────────────────────────────────────

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circle' | 'rect';
}

export function Skeleton({ className = '', variant = 'rect' }: SkeletonProps) {
  const variants = {
    text: 'h-4 rounded',
    circle: 'rounded-full',
    rect: 'rounded-lg',
  };

  return (
    <div
      className={`bg-white/10 animate-pulse ${variants[variant]} ${className}`}
    />
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SKELETON CARD
// ─────────────────────────────────────────────────────────────────────────────

export function SkeletonCard() {
  return (
    <div className="p-4 bg-white/5 rounded-xl space-y-4">
      <div className="flex items-center gap-3">
        <Skeleton variant="circle" className="w-10 h-10" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-3 w-1/3" />
        </div>
      </div>
      <Skeleton className="h-20 w-full" />
      <div className="flex gap-2">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  );
}

export default LoadingScreen;
