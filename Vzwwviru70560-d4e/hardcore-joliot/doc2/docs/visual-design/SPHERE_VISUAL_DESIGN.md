# CHE·NU™ — Design Visuel des Sphères

> *"Chaque sphère est un monde, pas juste un cercle"*

## 🎯 Philosophie de Design

Les sphères CHE·NU ne sont pas de simples conteneurs — ce sont des **contextes de vie**.
Leur représentation visuelle doit:

1. **Être reconnaissable instantanément** (même sans emoji)
2. **Refléter l'essence** de ce qu'elle contient
3. **Être cohérente** avec l'esthétique Solarpunk
4. **Être animable** (réagir à l'activité, la sélection)

---

## 🏛️ Options de Style Global

### Option A: Bâtiments Architecturaux
```
Style: Structures Solarpunk avec dômes, végétation, lumières
Avantage: Cohérent avec le campus 3D existant
Inconvénient: Complexe en 2D
```

### Option B: Gemmes/Cristaux
```
Style: Formes facettées, translucides, brillantes
Avantage: Élégant, moderne, facile à animer
Inconvénient: Moins "vivant"
```

### Option C: Formes Organiques
```
Style: Inspiré de la nature (fruits, cocons, nids, cellules)
Avantage: Unique, mémorable, "vivant"
Inconvénient: Peut être abstrait
```

### Option D: Icônes Stylisées (RECOMMANDÉ)
```
Style: Forme distinctive par sphère + détails animés
Avantage: Reconnaissable, scalable, personnalisé
Approche: Chaque sphère a sa propre silhouette
```

---

## 🎨 Design par Sphère (Option D)

### 🏠 Personal — La Maison
```
Forme: Hexagone (stabilité) avec toit
Détails:
  • Toit triangulaire avec cheminée
  • Fenêtre lumineuse au centre
  • Petit jardin à la base
  • Fumée animée de la cheminée
Couleur: Vert nature #4CAF50
Émotion: Chaleur, sécurité, intimité
```

### 💼 Business — La Tour
```
Forme: Rectangle vertical avec étages
Détails:
  • Plusieurs étages lumineux
  • Antenne/flèche au sommet
  • Fenêtres en grille
  • Données qui montent (animation)
Couleur: Bleu corporate #2196F3
Émotion: Ambition, structure, croissance
```

### 🏛️ Government — Le Temple
```
Forme: Structure classique avec colonnes
Détails:
  • Fronton triangulaire
  • Colonnes (2-4)
  • Escaliers à la base
  • Drapeau ou balance au sommet
Couleur: Gris institutionnel #607D8B
Émotion: Stabilité, justice, ordre
```

### 🎨 Studio — La Palette
```
Forme: Forme libre/artistique
Détails:
  • Palette de peintre ou chevalet
  • Taches de couleurs multiples
  • Pinceau ou plume
  • Particules créatives (animation)
Couleur: Violet créatif #9C27B0
Émotion: Expression, liberté, inspiration
```

### 👥 Community — Le Cercle
```
Forme: Cercle avec personnages
Détails:
  • Silhouettes de personnes en cercle
  • Mains qui se touchent
  • Feu de camp au centre (optionnel)
  • Pulsation de groupe (animation)
Couleur: Orange chaleur #FF9800
Émotion: Appartenance, partage, solidarité
```

### 📱 Social — Le Réseau
```
Forme: Nuage/bulle avec connexions
Détails:
  • Bulle centrale avec icônes sociales
  • Petites bulles satellites
  • Lignes de connexion (réseau)
  • Notifications qui apparaissent (animation)
Couleur: Rose social #E91E63
Émotion: Connexion, visibilité, partage
```

### 🎬 Entertainment — Le Projecteur
```
Forme: Écran de cinéma ou scène
Détails:
  • Écran avec bords arrondis
  • Rayons de lumière (projecteur)
  • Pop-corn ou note de musique
  • Lumières qui scintillent (animation)
Couleur: Rouge passion #F44336
Émotion: Plaisir, évasion, culture
```

### 🤝 My Team — La Table Ronde
```
Forme: Table vue du dessus avec chaises
Détails:
  • Table ronde centrale
  • Chaises autour (5-6)
  • Documents au centre
  • Personnes qui bougent (animation)
Couleur: Cyan collaboration #00BCD4
Émotion: Collaboration, synergie, équipe
```

### 📚 Scholar — Le Livre
```
Forme: Livre ouvert ou bibliothèque
Détails:
  • Livre ouvert avec pages
  • Lunettes ou graduation cap
  • Étoiles de connaissance
  • Pages qui tournent (animation)
Couleur: Brun sagesse #795548
Émotion: Curiosité, croissance, sagesse
```

---

## 🔄 États et Animations

### État Normal
```
• Forme visible mais sobre
• Couleur à 70% d'opacité
• Léger glow de la couleur
```

### État Hover (survol)
```
• Légère augmentation de taille (+10%)
• Couleur à 100%
• Glow plus intense
• Animation spécifique activée
```

### État Sélectionné
```
• Taille augmentée (+20%)
• Anneau lumineux or autour
• Animation continue
• Connexions vers autres sphères visibles
```

### État Actif (activité en cours)
```
• Pulsation rythmique
• Particules qui émanent
• Couleur plus vive
```

---

## 📐 Structure SVG Type

```svg
<g class="sphere" data-id="personal">
  <!-- Ombre portée -->
  <ellipse class="shadow" />
  
  <!-- Forme principale -->
  <path class="main-shape" />
  
  <!-- Détails intérieurs -->
  <g class="details">
    <!-- Fenêtres, éléments décoratifs -->
  </g>
  
  <!-- Glow/Aura -->
  <circle class="glow" />
  
  <!-- Icône/Emoji (optionnel) -->
  <text class="icon">🏠</text>
  
  <!-- Label -->
  <text class="label">Personal</text>
  
  <!-- Indicateur d'activité -->
  <g class="activity-indicator" />
</g>
```

---

## 🎯 Décision à Prendre

### Questions pour Jo:

1. **Style global**: Préfères-tu des formes distinctes par sphère (Option D)
   ou un style uniforme avec variations de couleur?

2. **Niveau de détail**: 
   - Minimaliste (silhouettes simples)?
   - Moyen (quelques détails)?
   - Riche (beaucoup de détails)?

3. **Emoji visible**: Garder l'emoji en plus de la forme, ou la forme remplace l'emoji?

4. **3D ou 2D**: 
   - 2D plat (SVG) pour la démo
   - 2.5D (perspective isométrique)
   - 3D complet (Three.js dans le vrai produit)

---

## 💡 Ma Recommandation

Pour le Ceiba et le campus CHE·NU, je recommande:

```
STYLE: Icônes stylisées distinctes (Option D)
DÉTAIL: Moyen (reconnaissable sans être surchargé)
EMOJI: Visible au centre de la forme
PERSPECTIVE: 2.5D isométrique (cohérent avec le campus)
```

Cela donne:
- Une identité visuelle forte par sphère
- Une cohérence avec l'esthétique Solarpunk
- Une flexibilité pour les animations
- Une reconnaissance instantanée

---

*Document créé le 25 décembre 2024*
*CHE·NU™ — Governed Intelligence Operating System*
