/**
 * CGU - Conditions Générales d'Utilisation
 * =========================================
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

export function CGU() {
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
          Conditions Générales d'Utilisation
        </h1>

        <p style={{ color: 'rgba(255,255,255,0.5)', marginBottom: '40px' }}>
          Dernière mise à jour: 13 février 2026
        </p>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            1. Acceptation des Conditions
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            En accédant à AT·OM, vous acceptez d'être lié par ces conditions d'utilisation.
            Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser la plateforme.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            2. Description du Service
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            AT·OM est une plateforme d'intelligence collective offrant accès à des agents IA
            dans 9 domaines de vie. Le service est fourni "tel quel" sans garantie de
            disponibilité continue.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            3. Utilisation Acceptable
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Vous vous engagez à utiliser AT·OM de manière légale et éthique.
            Toute utilisation abusive, frauduleuse ou nuisible est interdite.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            4. Propriété Intellectuelle
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Tout le contenu d'AT·OM (code, design, textes, agents) est protégé par
            les droits d'auteur. Vous conservez la propriété de vos données personnelles.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            5. Limitation de Responsabilité
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            AT·OM n'est pas responsable des dommages directs ou indirects résultant
            de l'utilisation de la plateforme. Les recommandations des agents ne
            constituent pas des conseils professionnels.
          </p>
        </section>

        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ color: COLORS.gold, fontSize: '20px', marginBottom: '16px' }}>
            6. Contact
          </h2>
          <p style={{ lineHeight: 1.8, color: 'rgba(255,255,255,0.8)' }}>
            Pour toute question concernant ces conditions, contactez-nous à:
            <br />
            <span style={{ color: COLORS.gold }}>legal@atom-platform.io</span>
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

export default CGU;
