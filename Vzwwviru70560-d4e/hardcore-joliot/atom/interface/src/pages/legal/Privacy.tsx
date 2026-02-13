/**
 * PRIVACY - Politique de Confidentialité
 * =======================================
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

export function Privacy() {
  const navigate = useNavigate();

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#000',
      color: '#fff',
      fontFamily: TYPOGRAPHY.fontFamily.system,
      padding: '40px 20px',
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <button
          onClick={() => navigate(-1)}
          style={{
            background: 'transparent',
            border: 'none',
            color: COLORS.cobalt,
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            fontSize: '14px',
            cursor: 'pointer',
            marginBottom: '40px',
          }}
        >
          ← Retour
        </button>

        <h1 style={{ color: COLORS.gold, marginBottom: '40px' }}>
          Politique de Confidentialité
        </h1>

        <p style={{ color: 'rgba(255,255,255,0.5)', marginBottom: '40px' }}>
          Dernière mise à jour: 13 février 2026
        </p>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            1. Données Collectées
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            AT·OM collecte uniquement les données nécessaires au fonctionnement du service:
          </p>
          <ul style={{ lineHeight: 2, color: 'rgba(255,255,255,0.8)', marginTop: '16px', paddingLeft: '20px' }}>
            <li>Email (si inscription waitlist)</li>
            <li>Données de session anonymisées</li>
            <li>Interactions avec les agents (localement)</li>
          </ul>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            2. Utilisation des Données
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Vos données sont utilisées exclusivement pour:
          </p>
          <ul style={{ lineHeight: 2, color: 'rgba(255,255,255,0.8)', marginTop: '16px', paddingLeft: '20px' }}>
            <li>Améliorer l'expérience utilisateur</li>
            <li>Vous informer des mises à jour (si inscrit)</li>
            <li>Assurer le bon fonctionnement de la plateforme</li>
          </ul>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            3. Stockage et Sécurité
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Vos données sont stockées de manière sécurisée sur des serveurs chiffrés.
            Nous appliquons les meilleures pratiques de sécurité pour protéger vos informations.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            4. Vos Droits (RGPD)
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Conformément au RGPD, vous disposez des droits suivants:
          </p>
          <ul style={{ lineHeight: 2, color: 'rgba(255,255,255,0.8)', marginTop: '16px', paddingLeft: '20px' }}>
            <li><strong>Droit d'accès:</strong> Demander une copie de vos données</li>
            <li><strong>Droit de rectification:</strong> Corriger vos informations</li>
            <li><strong>Droit à l'effacement:</strong> Supprimer vos données</li>
            <li><strong>Droit à la portabilité:</strong> Exporter vos données</li>
          </ul>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            5. Cookies
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            AT·OM utilise des cookies techniques essentiels au fonctionnement.
            Aucun cookie de tracking publicitaire n'est utilisé.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            6. Contact DPO
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Pour exercer vos droits ou pour toute question sur vos données:
            <br />
            <span style={{ color: COLORS.gold }}>privacy@atom-platform.io</span>
          </p>
        </section>

        <footer style={{
          borderTop: '1px solid rgba(255,255,255,0.1)',
          paddingTop: '40px',
          marginTop: '60px',
          textAlign: 'center',
          color: 'rgba(255,255,255,0.3)',
          fontSize: '12px',
        }}>
          © 2026 AT·OM · Jonathan Rodrigue
        </footer>
      </div>
    </div>
  );
}

export default Privacy;
