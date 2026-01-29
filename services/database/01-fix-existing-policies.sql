-- ===============================================================================
-- AT·OM - SCRIPT DE CORRECTION DES POLITIQUES EXISTANTES
-- À exécuter EN PREMIER avant founder-features.sql
-- ===============================================================================
--
-- Ce script corrige les politiques RLS pour les tables qui existent déjà
-- avec la structure participant_ids (TEXT[]) au lieu de participants (UUID[])
--
-- ===============================================================================

-- ===============================================================================
-- 1. NETTOYER TOUTES LES POLITIQUES SUR PRIVATE_THREADS
-- ===============================================================================

DO $$
DECLARE
  pol RECORD;
BEGIN
  -- Supprimer toutes les politiques existantes sur private_threads
  FOR pol IN
    SELECT policyname FROM pg_policies WHERE tablename = 'private_threads'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON private_threads', pol.policyname);
  END LOOP;
END $$;

-- ===============================================================================
-- 2. NETTOYER TOUTES LES POLITIQUES SUR THREAD_MESSAGES
-- ===============================================================================

DO $$
DECLARE
  pol RECORD;
BEGIN
  -- Supprimer toutes les politiques existantes sur thread_messages
  FOR pol IN
    SELECT policyname FROM pg_policies WHERE tablename = 'thread_messages'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON thread_messages', pol.policyname);
  END LOOP;
END $$;

-- ===============================================================================
-- 3. RECRÉER LES POLITIQUES POUR PRIVATE_THREADS (avec participant_ids)
-- ===============================================================================

-- Politique de lecture
CREATE POLICY "Participants can view threads"
ON private_threads FOR SELECT
USING (
  auth.uid()::text = ANY(participant_ids)
  OR created_by = auth.uid()::text
);

-- Politique d'insertion
CREATE POLICY "Users can create threads"
ON private_threads FOR INSERT
WITH CHECK (auth.uid()::text = created_by);

-- Politique de mise à jour (créateur seulement)
CREATE POLICY "Creators can update threads"
ON private_threads FOR UPDATE
USING (created_by = auth.uid()::text);

-- ===============================================================================
-- 4. RECRÉER LES POLITIQUES POUR THREAD_MESSAGES (avec participant_ids)
-- ===============================================================================

-- Politique de lecture
CREATE POLICY "Thread participants can view messages"
ON thread_messages FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE id = thread_messages.thread_id
    AND (auth.uid()::text = ANY(participant_ids) OR created_by = auth.uid()::text)
  )
);

-- Politique d'insertion
CREATE POLICY "Thread participants can send messages"
ON thread_messages FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE id = thread_messages.thread_id
    AND (auth.uid()::text = ANY(participant_ids) OR created_by = auth.uid()::text)
  )
);

-- ===============================================================================
-- 5. VÉRIFICATION
-- ===============================================================================

-- Afficher les politiques créées
SELECT tablename, policyname, cmd, qual
FROM pg_policies
WHERE tablename IN ('private_threads', 'thread_messages')
ORDER BY tablename, policyname;

-- ===============================================================================
-- FIN DU SCRIPT DE CORRECTION
-- ===============================================================================
