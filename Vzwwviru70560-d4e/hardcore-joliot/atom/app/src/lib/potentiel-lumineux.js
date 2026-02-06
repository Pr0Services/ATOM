/**
 * AT·OM — Potentiel Lumineux des Nations
 * Données harmonisées pour la Carte de Gaïa
 */

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES PAR PAYS
// Sources: Global Solar Atlas (GHI kWh/m²/an), indices composites
// ═══════════════════════════════════════════════════════════════════════════════

export const PAYS_LUMINEUX = [
  // ─── AFRIQUE ───
  { code: 'DZ', nom: 'Algérie',       continent: 'afrique',  lat: 28.03, lng: 1.66,   ghi: 2100, indiceEveil: 0.45, population: 45600000 },
  { code: 'AO', nom: 'Angola',        continent: 'afrique',  lat: -11.20, lng: 17.87,  ghi: 1950, indiceEveil: 0.35, population: 35600000 },
  { code: 'BJ', nom: 'Bénin',         continent: 'afrique',  lat: 9.31, lng: 2.32,     ghi: 1850, indiceEveil: 0.40, population: 13300000 },
  { code: 'BW', nom: 'Botswana',      continent: 'afrique',  lat: -22.33, lng: 24.68,  ghi: 2200, indiceEveil: 0.50, population: 2630000 },
  { code: 'BF', nom: 'Burkina Faso',  continent: 'afrique',  lat: 12.36, lng: -1.52,   ghi: 2000, indiceEveil: 0.38, population: 22100000 },
  { code: 'CM', nom: 'Cameroun',      continent: 'afrique',  lat: 7.37, lng: 12.35,    ghi: 1750, indiceEveil: 0.42, population: 28600000 },
  { code: 'TD', nom: 'Tchad',         continent: 'afrique',  lat: 15.45, lng: 18.73,   ghi: 2200, indiceEveil: 0.30, population: 17700000 },
  { code: 'CD', nom: 'RD Congo',      continent: 'afrique',  lat: -4.04, lng: 21.76,   ghi: 1650, indiceEveil: 0.32, population: 102300000 },
  { code: 'CI', nom: 'Côte d\'Ivoire',continent: 'afrique',  lat: 7.54, lng: -5.55,    ghi: 1800, indiceEveil: 0.43, population: 28200000 },
  { code: 'EG', nom: 'Égypte',        continent: 'afrique',  lat: 26.82, lng: 30.80,   ghi: 2400, indiceEveil: 0.55, population: 109300000 },
  { code: 'ET', nom: 'Éthiopie',      continent: 'afrique',  lat: 9.15, lng: 40.49,    ghi: 2050, indiceEveil: 0.40, population: 126500000 },
  { code: 'GH', nom: 'Ghana',         continent: 'afrique',  lat: 7.95, lng: -1.02,    ghi: 1850, indiceEveil: 0.48, population: 33500000 },
  { code: 'KE', nom: 'Kenya',         continent: 'afrique',  lat: -0.02, lng: 37.91,   ghi: 2000, indiceEveil: 0.52, population: 55100000 },
  { code: 'LY', nom: 'Libye',         continent: 'afrique',  lat: 26.34, lng: 17.23,   ghi: 2300, indiceEveil: 0.33, population: 7000000 },
  { code: 'MG', nom: 'Madagascar',    continent: 'afrique',  lat: -18.77, lng: 46.87,  ghi: 1900, indiceEveil: 0.42, population: 30300000 },
  { code: 'ML', nom: 'Mali',          continent: 'afrique',  lat: 17.57, lng: -4.00,   ghi: 2150, indiceEveil: 0.36, population: 22400000 },
  { code: 'MA', nom: 'Maroc',         continent: 'afrique',  lat: 31.79, lng: -7.09,   ghi: 2050, indiceEveil: 0.58, population: 37800000 },
  { code: 'MZ', nom: 'Mozambique',    continent: 'afrique',  lat: -18.67, lng: 35.53,  ghi: 1900, indiceEveil: 0.35, population: 33900000 },
  { code: 'NA', nom: 'Namibie',       continent: 'afrique',  lat: -22.96, lng: 18.49,  ghi: 2350, indiceEveil: 0.52, population: 2600000 },
  { code: 'NE', nom: 'Niger',         continent: 'afrique',  lat: 17.61, lng: 8.08,    ghi: 2250, indiceEveil: 0.32, population: 26200000 },
  { code: 'NG', nom: 'Nigéria',       continent: 'afrique',  lat: 9.08, lng: 7.49,     ghi: 1850, indiceEveil: 0.45, population: 223800000 },
  { code: 'RW', nom: 'Rwanda',        continent: 'afrique',  lat: -1.94, lng: 29.87,   ghi: 1700, indiceEveil: 0.55, population: 14100000 },
  { code: 'SN', nom: 'Sénégal',       continent: 'afrique',  lat: 14.50, lng: -14.45,  ghi: 2000, indiceEveil: 0.50, population: 17700000 },
  { code: 'ZA', nom: 'Afrique du Sud',continent: 'afrique',  lat: -30.56, lng: 22.94,  ghi: 2100, indiceEveil: 0.60, population: 60400000 },
  { code: 'TZ', nom: 'Tanzanie',      continent: 'afrique',  lat: -6.37, lng: 34.89,   ghi: 1950, indiceEveil: 0.45, population: 65500000 },
  { code: 'TN', nom: 'Tunisie',       continent: 'afrique',  lat: 33.89, lng: 9.54,    ghi: 1950, indiceEveil: 0.55, population: 12300000 },
  { code: 'UG', nom: 'Ouganda',       continent: 'afrique',  lat: 1.37, lng: 32.29,    ghi: 1800, indiceEveil: 0.42, population: 48600000 },
  { code: 'ZM', nom: 'Zambie',        continent: 'afrique',  lat: -13.13, lng: 27.85,  ghi: 2050, indiceEveil: 0.42, population: 20600000 },
  { code: 'ZW', nom: 'Zimbabwe',      continent: 'afrique',  lat: -19.02, lng: 29.15,  ghi: 2100, indiceEveil: 0.40, population: 16300000 },

  // ─── AMÉRIQUES ───
  { code: 'AR', nom: 'Argentine',     continent: 'ameriques', lat: -38.42, lng: -63.62, ghi: 1750, indiceEveil: 0.55, population: 46300000 },
  { code: 'BO', nom: 'Bolivie',       continent: 'ameriques', lat: -16.29, lng: -63.59, ghi: 1900, indiceEveil: 0.45, population: 12400000 },
  { code: 'BR', nom: 'Brésil',        continent: 'ameriques', lat: -14.24, lng: -51.93, ghi: 1800, indiceEveil: 0.58, population: 216400000 },
  { code: 'CA', nom: 'Canada',        continent: 'ameriques', lat: 56.13, lng: -106.35, ghi: 1150, indiceEveil: 0.72, population: 40100000 },
  { code: 'CL', nom: 'Chili',         continent: 'ameriques', lat: -35.68, lng: -71.54, ghi: 1900, indiceEveil: 0.60, population: 19600000 },
  { code: 'CO', nom: 'Colombie',      continent: 'ameriques', lat: 4.57, lng: -74.30,   ghi: 1700, indiceEveil: 0.50, population: 52100000 },
  { code: 'CR', nom: 'Costa Rica',    continent: 'ameriques', lat: 9.75, lng: -83.75,   ghi: 1650, indiceEveil: 0.68, population: 5200000 },
  { code: 'CU', nom: 'Cuba',          continent: 'ameriques', lat: 21.52, lng: -77.78,  ghi: 1850, indiceEveil: 0.48, population: 11100000 },
  { code: 'DO', nom: 'Rép. Dominicaine', continent: 'ameriques', lat: 18.74, lng: -70.16, ghi: 1800, indiceEveil: 0.45, population: 11200000 },
  { code: 'EC', nom: 'Équateur',      continent: 'ameriques', lat: -1.83, lng: -78.18,  ghi: 1600, indiceEveil: 0.50, population: 18200000 },
  { code: 'SV', nom: 'El Salvador',   continent: 'ameriques', lat: 13.79, lng: -88.90,  ghi: 1800, indiceEveil: 0.42, population: 6300000 },
  { code: 'GT', nom: 'Guatemala',     continent: 'ameriques', lat: 15.78, lng: -90.23,  ghi: 1750, indiceEveil: 0.45, population: 17600000 },
  { code: 'HT', nom: 'Haïti',         continent: 'ameriques', lat: 18.97, lng: -72.29,  ghi: 1800, indiceEveil: 0.38, population: 11600000 },
  { code: 'HN', nom: 'Honduras',      continent: 'ameriques', lat: 15.20, lng: -86.24,  ghi: 1750, indiceEveil: 0.40, population: 10400000 },
  { code: 'JM', nom: 'Jamaïque',      continent: 'ameriques', lat: 18.11, lng: -77.30,  ghi: 1850, indiceEveil: 0.50, population: 2800000 },
  { code: 'MX', nom: 'Mexique',       continent: 'ameriques', lat: 23.63, lng: -102.55, ghi: 1950, indiceEveil: 0.55, population: 128900000 },
  { code: 'NI', nom: 'Nicaragua',     continent: 'ameriques', lat: 12.87, lng: -85.21,  ghi: 1750, indiceEveil: 0.40, population: 7000000 },
  { code: 'PA', nom: 'Panama',        continent: 'ameriques', lat: 8.54, lng: -80.78,   ghi: 1600, indiceEveil: 0.52, population: 4400000 },
  { code: 'PY', nom: 'Paraguay',      continent: 'ameriques', lat: -23.44, lng: -58.44, ghi: 1800, indiceEveil: 0.42, population: 7400000 },
  { code: 'PE', nom: 'Pérou',         continent: 'ameriques', lat: -9.19, lng: -75.02,  ghi: 1750, indiceEveil: 0.50, population: 34300000 },
  { code: 'PR', nom: 'Porto Rico',    continent: 'ameriques', lat: 18.22, lng: -66.59,  ghi: 1800, indiceEveil: 0.48, population: 3200000 },
  { code: 'US', nom: 'États-Unis',    continent: 'ameriques', lat: 37.09, lng: -95.71,  ghi: 1600, indiceEveil: 0.62, population: 339900000 },
  { code: 'UY', nom: 'Uruguay',       continent: 'ameriques', lat: -32.52, lng: -55.77, ghi: 1600, indiceEveil: 0.65, population: 3400000 },
  { code: 'VE', nom: 'Venezuela',     continent: 'ameriques', lat: 6.42, lng: -66.59,   ghi: 1750, indiceEveil: 0.42, population: 28400000 },

  // ─── ASIE ───
  { code: 'AF', nom: 'Afghanistan',   continent: 'asie',     lat: 33.94, lng: 67.71,   ghi: 1900, indiceEveil: 0.30, population: 41100000 },
  { code: 'BD', nom: 'Bangladesh',    continent: 'asie',     lat: 23.68, lng: 90.36,   ghi: 1600, indiceEveil: 0.40, population: 172800000 },
  { code: 'BT', nom: 'Bhoutan',       continent: 'asie',     lat: 27.51, lng: 90.43,   ghi: 1500, indiceEveil: 0.75, population: 800000 },
  { code: 'KH', nom: 'Cambodge',      continent: 'asie',     lat: 12.57, lng: 104.99,  ghi: 1750, indiceEveil: 0.48, population: 16900000 },
  { code: 'CN', nom: 'Chine',         continent: 'asie',     lat: 35.86, lng: 104.20,  ghi: 1450, indiceEveil: 0.50, population: 1425700000 },
  { code: 'IN', nom: 'Inde',          continent: 'asie',     lat: 20.59, lng: 78.96,   ghi: 1900, indiceEveil: 0.65, population: 1428600000 },
  { code: 'ID', nom: 'Indonésie',     continent: 'asie',     lat: -0.79, lng: 113.92,  ghi: 1650, indiceEveil: 0.50, population: 277500000 },
  { code: 'IR', nom: 'Iran',          continent: 'asie',     lat: 32.43, lng: 53.69,   ghi: 2050, indiceEveil: 0.48, population: 87900000 },
  { code: 'IQ', nom: 'Irak',          continent: 'asie',     lat: 33.22, lng: 43.68,   ghi: 2050, indiceEveil: 0.38, population: 44500000 },
  { code: 'IL', nom: 'Israël',        continent: 'asie',     lat: 31.05, lng: 34.85,   ghi: 2100, indiceEveil: 0.65, population: 9800000 },
  { code: 'JP', nom: 'Japon',         continent: 'asie',     lat: 36.20, lng: 138.25,  ghi: 1350, indiceEveil: 0.72, population: 123300000 },
  { code: 'JO', nom: 'Jordanie',      continent: 'asie',     lat: 30.59, lng: 36.24,   ghi: 2200, indiceEveil: 0.50, population: 11300000 },
  { code: 'KZ', nom: 'Kazakhstan',    continent: 'asie',     lat: 48.02, lng: 66.92,   ghi: 1450, indiceEveil: 0.45, population: 19600000 },
  { code: 'KR', nom: 'Corée du Sud',  continent: 'asie',     lat: 35.91, lng: 127.77,  ghi: 1350, indiceEveil: 0.65, population: 51700000 },
  { code: 'KW', nom: 'Koweït',        continent: 'asie',     lat: 29.31, lng: 47.48,   ghi: 2150, indiceEveil: 0.45, population: 4300000 },
  { code: 'MY', nom: 'Malaisie',      continent: 'asie',     lat: 4.21, lng: 101.98,   ghi: 1600, indiceEveil: 0.52, population: 34300000 },
  { code: 'MN', nom: 'Mongolie',      continent: 'asie',     lat: 46.86, lng: 103.85,  ghi: 1500, indiceEveil: 0.48, population: 3400000 },
  { code: 'MM', nom: 'Myanmar',       continent: 'asie',     lat: 21.91, lng: 95.96,   ghi: 1700, indiceEveil: 0.40, population: 54800000 },
  { code: 'NP', nom: 'Népal',         continent: 'asie',     lat: 28.39, lng: 84.12,   ghi: 1650, indiceEveil: 0.60, population: 30900000 },
  { code: 'OM', nom: 'Oman',          continent: 'asie',     lat: 21.47, lng: 55.98,   ghi: 2250, indiceEveil: 0.48, population: 4600000 },
  { code: 'PK', nom: 'Pakistan',      continent: 'asie',     lat: 30.38, lng: 69.35,   ghi: 1900, indiceEveil: 0.42, population: 231400000 },
  { code: 'PH', nom: 'Philippines',   continent: 'asie',     lat: 12.88, lng: 121.77,  ghi: 1650, indiceEveil: 0.52, population: 117300000 },
  { code: 'SA', nom: 'Arabie Saoudite', continent: 'asie',   lat: 23.89, lng: 45.08,   ghi: 2350, indiceEveil: 0.42, population: 36900000 },
  { code: 'SG', nom: 'Singapour',     continent: 'asie',     lat: 1.35, lng: 103.82,   ghi: 1600, indiceEveil: 0.70, population: 5900000 },
  { code: 'LK', nom: 'Sri Lanka',     continent: 'asie',     lat: 7.87, lng: 80.77,    ghi: 1750, indiceEveil: 0.55, population: 22200000 },
  { code: 'TW', nom: 'Taïwan',        continent: 'asie',     lat: 23.70, lng: 120.96,  ghi: 1450, indiceEveil: 0.65, population: 23900000 },
  { code: 'TH', nom: 'Thaïlande',     continent: 'asie',     lat: 15.87, lng: 100.99,  ghi: 1700, indiceEveil: 0.58, population: 71800000 },
  { code: 'TR', nom: 'Turquie',       continent: 'asie',     lat: 38.96, lng: 35.24,   ghi: 1700, indiceEveil: 0.52, population: 85300000 },
  { code: 'AE', nom: 'Émirats Arabes', continent: 'asie',    lat: 23.42, lng: 53.85,   ghi: 2200, indiceEveil: 0.55, population: 9400000 },
  { code: 'UZ', nom: 'Ouzbékistan',   continent: 'asie',     lat: 41.38, lng: 64.59,   ghi: 1600, indiceEveil: 0.42, population: 35300000 },
  { code: 'VN', nom: 'Vietnam',       continent: 'asie',     lat: 14.06, lng: 108.28,  ghi: 1550, indiceEveil: 0.52, population: 99500000 },

  // ─── EUROPE ───
  { code: 'AT', nom: 'Autriche',      continent: 'europe',   lat: 47.52, lng: 14.55,   ghi: 1150, indiceEveil: 0.70, population: 9100000 },
  { code: 'BE', nom: 'Belgique',      continent: 'europe',   lat: 50.50, lng: 4.47,    ghi: 1050, indiceEveil: 0.68, population: 11600000 },
  { code: 'BG', nom: 'Bulgarie',      continent: 'europe',   lat: 42.73, lng: 25.49,   ghi: 1400, indiceEveil: 0.50, population: 6700000 },
  { code: 'HR', nom: 'Croatie',       continent: 'europe',   lat: 45.10, lng: 15.20,   ghi: 1350, indiceEveil: 0.55, population: 3900000 },
  { code: 'CZ', nom: 'Tchéquie',      continent: 'europe',   lat: 49.82, lng: 15.47,   ghi: 1100, indiceEveil: 0.62, population: 10900000 },
  { code: 'DK', nom: 'Danemark',      continent: 'europe',   lat: 56.26, lng: 9.50,    ghi: 1000, indiceEveil: 0.78, population: 5900000 },
  { code: 'FI', nom: 'Finlande',      continent: 'europe',   lat: 61.92, lng: 25.75,   ghi: 900, indiceEveil: 0.80, population: 5500000 },
  { code: 'FR', nom: 'France',        continent: 'europe',   lat: 46.23, lng: 2.21,    ghi: 1300, indiceEveil: 0.72, population: 68000000 },
  { code: 'DE', nom: 'Allemagne',     continent: 'europe',   lat: 51.17, lng: 10.45,   ghi: 1100, indiceEveil: 0.72, population: 84400000 },
  { code: 'GR', nom: 'Grèce',         continent: 'europe',   lat: 39.07, lng: 21.82,   ghi: 1700, indiceEveil: 0.58, population: 10400000 },
  { code: 'HU', nom: 'Hongrie',       continent: 'europe',   lat: 47.16, lng: 19.50,   ghi: 1300, indiceEveil: 0.55, population: 9600000 },
  { code: 'IS', nom: 'Islande',       continent: 'europe',   lat: 64.96, lng: -19.02,  ghi: 800, indiceEveil: 0.82, population: 400000 },
  { code: 'IE', nom: 'Irlande',       continent: 'europe',   lat: 53.14, lng: -7.69,   ghi: 950, indiceEveil: 0.72, population: 5100000 },
  { code: 'IT', nom: 'Italie',        continent: 'europe',   lat: 41.87, lng: 12.57,   ghi: 1500, indiceEveil: 0.62, population: 59000000 },
  { code: 'NL', nom: 'Pays-Bas',      continent: 'europe',   lat: 52.13, lng: 5.29,    ghi: 1050, indiceEveil: 0.75, population: 17600000 },
  { code: 'NO', nom: 'Norvège',       continent: 'europe',   lat: 60.47, lng: 8.47,    ghi: 850, indiceEveil: 0.82, population: 5500000 },
  { code: 'PL', nom: 'Pologne',       continent: 'europe',   lat: 51.92, lng: 19.15,   ghi: 1100, indiceEveil: 0.58, population: 37700000 },
  { code: 'PT', nom: 'Portugal',      continent: 'europe',   lat: 39.40, lng: -8.22,   ghi: 1700, indiceEveil: 0.65, population: 10300000 },
  { code: 'RO', nom: 'Roumanie',      continent: 'europe',   lat: 45.94, lng: 24.97,   ghi: 1350, indiceEveil: 0.50, population: 19100000 },
  { code: 'RU', nom: 'Russie',        continent: 'europe',   lat: 61.52, lng: 105.32,  ghi: 1000, indiceEveil: 0.48, population: 144100000 },
  { code: 'RS', nom: 'Serbie',        continent: 'europe',   lat: 44.02, lng: 21.01,   ghi: 1350, indiceEveil: 0.48, population: 6600000 },
  { code: 'SK', nom: 'Slovaquie',     continent: 'europe',   lat: 48.67, lng: 19.70,   ghi: 1150, indiceEveil: 0.55, population: 5500000 },
  { code: 'ES', nom: 'Espagne',       continent: 'europe',   lat: 40.46, lng: -3.75,   ghi: 1700, indiceEveil: 0.62, population: 47500000 },
  { code: 'SE', nom: 'Suède',         continent: 'europe',   lat: 60.13, lng: 18.64,   ghi: 950, indiceEveil: 0.80, population: 10500000 },
  { code: 'CH', nom: 'Suisse',        continent: 'europe',   lat: 46.82, lng: 8.23,    ghi: 1200, indiceEveil: 0.78, population: 8800000 },
  { code: 'UA', nom: 'Ukraine',       continent: 'europe',   lat: 48.38, lng: 31.17,   ghi: 1250, indiceEveil: 0.48, population: 37000000 },
  { code: 'GB', nom: 'Royaume-Uni',   continent: 'europe',   lat: 55.38, lng: -3.44,   ghi: 1000, indiceEveil: 0.70, population: 67700000 },

  // ─── OCÉANIE ───
  { code: 'AU', nom: 'Australie',     continent: 'oceanie',  lat: -25.27, lng: 133.78, ghi: 2100, indiceEveil: 0.68, population: 26500000 },
  { code: 'FJ', nom: 'Fidji',         continent: 'oceanie',  lat: -17.71, lng: 178.07, ghi: 1700, indiceEveil: 0.52, population: 900000 },
  { code: 'NZ', nom: 'Nouvelle-Zélande', continent: 'oceanie', lat: -40.90, lng: 174.89, ghi: 1450, indiceEveil: 0.75, population: 5200000 },
  { code: 'PG', nom: 'Papouasie-N.-G.', continent: 'oceanie', lat: -6.31, lng: 143.96, ghi: 1650, indiceEveil: 0.38, population: 10100000 },
];

// ═══════════════════════════════════════════════════════════════════════════════
// CONTINENTS — MÉTADONNÉES
// ═══════════════════════════════════════════════════════════════════════════════

export const CONTINENTS = {
  afrique:   { nom: 'Afrique',   emoji: '🌍', color: '#D4AF37', colorGlow: '#FFD700' },
  ameriques: { nom: 'Amériques', emoji: '🌎', color: '#22C55E', colorGlow: '#4ADE80' },
  asie:      { nom: 'Asie',      emoji: '🌏', color: '#EF4444', colorGlow: '#F87171' },
  europe:    { nom: 'Europe',    emoji: '🏛️', color: '#3B82F6', colorGlow: '#60A5FA' },
  oceanie:   { nom: 'Océanie',   emoji: '🐚', color: '#8B5CF6', colorGlow: '#A78BFA' },
};

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL DU POTENTIEL LUMINEUX
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule le Potentiel Lumineux d'un pays (0-100)
 * Formule: (GHI normalisé × 0.4) + (indice d'éveil × 0.6) × 100
 * Le solaire nourrit, la conscience illumine
 */
export const calculerPotentielLumineux = (pays) => {
  const GHI_MAX = 2500; // Max mondial (kWh/m²/an)
  const ghiNorm = Math.min(pays.ghi / GHI_MAX, 1);
  const potentiel = (ghiNorm * 0.4 + pays.indiceEveil * 0.6) * 100;
  return Math.round(potentiel * 10) / 10;
};

/**
 * Retourne la couleur du potentiel (gradient rouge → or → blanc)
 */
export const getCouleurPotentiel = (potentiel) => {
  if (potentiel >= 75) return { bg: '#FFFFFF', text: '#000000', glow: 'rgba(255,255,255,0.8)', label: 'Éclairé' };
  if (potentiel >= 60) return { bg: '#FFD700', text: '#000000', glow: 'rgba(255,215,0,0.6)', label: 'Lumineux' };
  if (potentiel >= 45) return { bg: '#FF8C00', text: '#FFFFFF', glow: 'rgba(255,140,0,0.5)', label: 'Éveillé' };
  if (potentiel >= 30) return { bg: '#FF4500', text: '#FFFFFF', glow: 'rgba(255,69,0,0.4)', label: 'Naissant' };
  return { bg: '#8B0000', text: '#FFFFFF', glow: 'rgba(139,0,0,0.3)', label: 'Dormant' };
};

/**
 * Retourne la fréquence harmonique d'un pays (Hz)
 * Basée sur le potentiel lumineux, alignée aux fréquences AT·OM
 */
export const getFrequencePays = (potentiel) => {
  // Échelle: 44.4 Hz (base) → 444 Hz (coeur) → 999 Hz (source)
  const freq = 44.4 + (potentiel / 100) * (999 - 44.4);
  return Math.round(freq * 10) / 10;
};

// ═══════════════════════════════════════════════════════════════════════════════
// STATISTIQUES GLOBALES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule les statistiques globales de Gaïa
 */
export const getStatsGlobales = () => {
  const potentiels = PAYS_LUMINEUX.map(p => calculerPotentielLumineux(p));
  const total = potentiels.reduce((a, b) => a + b, 0);
  const moyenne = total / potentiels.length;
  const max = Math.max(...potentiels);
  const min = Math.min(...potentiels);

  // Population couverte
  const popTotale = PAYS_LUMINEUX.reduce((a, p) => a + p.population, 0);

  // Par continent
  const parContinent = {};
  Object.keys(CONTINENTS).forEach(c => {
    const paysDuContinent = PAYS_LUMINEUX.filter(p => p.continent === c);
    const potC = paysDuContinent.map(p => calculerPotentielLumineux(p));
    parContinent[c] = {
      ...CONTINENTS[c],
      nbPays: paysDuContinent.length,
      moyennePotentiel: Math.round((potC.reduce((a, b) => a + b, 0) / potC.length) * 10) / 10,
      population: paysDuContinent.reduce((a, p) => a + p.population, 0)
    };
  });

  // Fréquence moyenne de Gaïa
  const freqGaia = getFrequencePays(moyenne);

  return {
    nbPays: PAYS_LUMINEUX.length,
    moyennePotentiel: Math.round(moyenne * 10) / 10,
    maxPotentiel: max,
    minPotentiel: min,
    populationCouverte: popTotale,
    frequenceGaia: freqGaia,
    parContinent
  };
};

/**
 * Trie les pays par potentiel lumineux (décroissant)
 */
export const getClassement = () => {
  return PAYS_LUMINEUX
    .map(p => ({
      ...p,
      potentiel: calculerPotentielLumineux(p),
      frequence: getFrequencePays(calculerPotentielLumineux(p)),
      couleur: getCouleurPotentiel(calculerPotentielLumineux(p))
    }))
    .sort((a, b) => b.potentiel - a.potentiel);
};

/**
 * Recherche un pays par code ou nom
 */
export const chercherPays = (query) => {
  const q = query.toLowerCase();
  return PAYS_LUMINEUX.filter(p =>
    p.code.toLowerCase() === q ||
    p.nom.toLowerCase().includes(q)
  ).map(p => ({
    ...p,
    potentiel: calculerPotentielLumineux(p),
    frequence: getFrequencePays(calculerPotentielLumineux(p)),
    couleur: getCouleurPotentiel(calculerPotentielLumineux(p))
  }));
};
