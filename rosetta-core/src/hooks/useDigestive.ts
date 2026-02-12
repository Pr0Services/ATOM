/**
 * AT·OM — useDigestive
 * Hook React pour consommer le DigestiveSystem
 *
 * "Le système digestif nourrit chaque cellule de l'organisme
 *  — le hook nourrit chaque composant du UI."
 *
 * Expose :
 *   - digestUrl(url, rawContent)    → Digérer une page web
 *   - digestText(text, source?)     → Digérer du texte brut
 *   - digestRss(rssContent, feedUrl)→ Digérer un flux RSS
 *   - digestBatch(items)            → Digérer plusieurs items
 *   - stats                         → Statistiques du système
 *   - wasteArchive                  → Déchets archivés avec raisons
 *   - absorptionRate                → Taux d'absorption (0-1)
 */

import { useMemo, useCallback } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import { DigestiveSystem } from '../engines/DigestiveSystem';
import type { FoodSource, DigestedFood, DigestiveStats } from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// HOOK
// ═══════════════════════════════════════════════════════════

export function useDigestive() {
  const { parser, amygdala } = useATOM();

  // Instance partagée (mémorisée)
  const digestive = useMemo(
    () => new DigestiveSystem(parser, amygdala),
    [parser, amygdala],
  );

  // ── Digérer une URL ──────────────────────────────────────

  /** Digère le contenu brut d'une page web */
  const digestUrl = useCallback(
    (url: string, rawContent: string): DigestedFood =>
      digestive.digest('url', url, rawContent, 'text/html'),
    [digestive],
  );

  // ── Digérer du texte brut ────────────────────────────────

  /** Digère du texte brut (saisie manuelle, copier-coller) */
  const digestText = useCallback(
    (text: string, source?: string): DigestedFood =>
      digestive.digest('manual', source ?? 'manual', text, 'text/plain'),
    [digestive],
  );

  // ── Digérer un flux RSS ──────────────────────────────────

  /** Digère du contenu RSS */
  const digestRss = useCallback(
    (rssContent: string, feedUrl: string): DigestedFood =>
      digestive.digest('rss', feedUrl, rssContent, 'application/rss+xml'),
    [digestive],
  );

  // ── Digestion par lot ────────────────────────────────────

  /** Digère plusieurs items d'un coup */
  const digestBatch = useCallback(
    (items: { source: FoodSource; url: string; content: string; contentType?: string }[]) =>
      digestive.digestBatch(items),
    [digestive],
  );

  // ── Statistiques ─────────────────────────────────────────

  const stats = useMemo(
    (): DigestiveStats => digestive.getStats(),
    [digestive],
  );

  const wasteArchive = useMemo(
    (): DigestedFood[] => digestive.getWasteArchive(),
    [digestive],
  );

  // ── Return ───────────────────────────────────────────────

  return {
    // Digestion
    digestUrl,
    digestText,
    digestRss,
    digestBatch,

    // Statistiques
    stats,
    wasteArchive,
    absorptionRate: stats.absorption_rate,

    // Accès direct à l'instance (pour les cas avancés)
    digestive,
  };
}
