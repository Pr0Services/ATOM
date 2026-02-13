/**
 * MENTIONS LEGALES
 * =================
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

export function Mentions() {
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
          Mentions Légales
        </h1>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Éditeur du Site
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            <strong>AT·OM</strong>
            <br />
            Plateforme d'Intelligence Collective
            <br />
            <br />
            <strong>Fondateur & Architecte:</strong> Jonathan Rodrigue
            <br />
            <strong>Email:</strong> <span style={{ color: COLORS.gold }}>contact@atom-platform.io</span>
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Hébergement
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            <strong>Frontend:</strong> Vercel Inc.
            <br />
            440 N Barranca Ave #4133, Covina, CA 91723, USA
            <br />
            <br />
            <strong>Backend:</strong> DigitalOcean LLC
            <br />
            101 Avenue of the Americas, 10th Floor, New York, NY 10013, USA
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Propriété Intellectuelle
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            L'ensemble du contenu de ce site (textes, images, code source, design, agents IA)
            est protégé par les lois sur la propriété intellectuelle.
            <br /><br />
            Toute reproduction, même partielle, est interdite sans autorisation préalable.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Données Personnelles
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Conformément au Règlement Général sur la Protection des Données (RGPD),
            vous disposez d'un droit d'accès, de rectification et de suppression de vos données.
            <br /><br />
            Consultez notre <a href="/legal/privacy" style={{ color: COLORS.gold }}>Politique de Confidentialité</a> pour plus d'informations.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Crédits
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            <strong>Design & Architecture:</strong> Jonathan Rodrigue
            <br />
            <strong>Technologies:</strong> React, TypeScript, FastAPI, PostgreSQL
            <br />
            <strong>Fréquence d'ancrage:</strong> 444 Hz · 999 Hz
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            Loi Applicable
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Le présent site est soumis au droit français.
            Tout litige sera de la compétence exclusive des tribunaux français.
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
          © 2026 AT·OM · Jonathan Rodrigue · 999 Hz
        </footer>
      </div>
    </div>
  );
}

export default Mentions;
