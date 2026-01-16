# ðŸŽ¯ CHEÂ·NU V25 - WORKLIST POUR PROCHAIN AGENT

**Date:** 5 dÃ©cembre 2024  
**Session prÃ©cÃ©dente:** Consolidation + Restructuration  
**Prochain focus:** Upgrade graphique avatars + modules manquants

---

## ðŸ“‹ CONTEXTE RAPIDE

CHEÂ·NU est une plateforme de gestion unifiÃ©e:
- **7 Espaces:** Maison, Entreprise, Projets, Creative Studio, Gouvernement, Immobilier, Associations
- **Menu:** Dashboard, Social, Forum, Streaming, Creative Studio, Outils & Agents, CHE-Learn, ParamÃ¨tres
- **Nova:** Agent IA personnel (toujours visible)
- **RÃ¨gle:** Tout en â‰¤3 clics, Creative Studio en 1 clic

---

## âœ… CE QUI A Ã‰TÃ‰ FAIT

1. âœ… Consolidation de 114+ fichiers
2. âœ… CrÃ©ation structure `/home/claude/chenu-v25/` (71 dossiers)
3. âœ… Documentation architecture validÃ©e
4. âœ… Nova AI Brain complet (master_mind, task_decomposer, etc.)
5. âœ… Fichiers backend: security, multi-tenancy, websocket
6. âœ… Fichiers frontend: avatars, animations, widgets

---

## ðŸ”¥ TÃ‚CHES PRIORITAIRES

### 1. ðŸŽ¨ UPGRADE GRAPHIQUE AVATARS (DemandÃ© par user)

**Fichiers existants Ã  amÃ©liorer:**
- `/mnt/user-data/uploads/AvatarBuilder.tsx`
- `/mnt/user-data/uploads/AvatarGenerator.tsx`
- `/mnt/user-data/uploads/DirectorsAvatars.tsx`
- `/mnt/user-data/uploads/NovaAvatar3D.tsx`

**AmÃ©liorations Ã  faire:**
- [ ] Ajouter les 6 styles d'avatars:
  - Humain rÃ©aliste
  - Cartoon
  - Animal
  - CrÃ©ature mythique
  - Avatar 3D
  - Minimaliste / Flat
- [ ] Switch instantanÃ© entre styles
- [ ] Morphing facial (sourire, yeux, nez)
- [ ] Coiffures multiples
- [ ] Accessoires (lunettes, bijoux, casques)
- [ ] Expressions (neutre, joyeux, concentrÃ©)
- [ ] Preview en temps rÃ©el

**RÃ©fÃ©rence:** PDF `CHE_NU_Avatar_System_Deck.pdf` pages 2-15

---

### 2. ðŸ“± MODULES MANQUANTS Ã€ CRÃ‰ER

D'aprÃ¨s le screenshot Excel de l'utilisateur:

| Module | Sous-modules | Priority |
|--------|--------------|----------|
| **Social Network** | Plateforme, Che-Nu Social, Post, Forum, Pages | ðŸ”´ HIGH |
| **Video Streaming** | Player, Chapitres IA, Recommendations | ðŸ”´ HIGH |
| **IA Labs** | Multi-LLM, Comparaison, Prompts | ðŸŸ  MED |
| **Scholars** | Course, Tutorial, Research | ðŸŸ  MED |
| **My Team** | HiÃ©rarchie agents, RÃ´les, Tasks | ðŸ”´ HIGH |
| **Database** | Connexions, Queries, Backups | ðŸŸ¡ LOW |
| **My Business** | Dashboard entreprise | âœ… EXISTS |
| **Creative Studio** | Media, Editor, Brand Kit | âœ… EXISTS |

**IMPORTANT:** Ces modules se connectent Ã :
1. Notre propre plateforme CHEÂ·NU
2. Plateformes externes (extraction data de tous les comptes):
   - YouTube, Twitch, TikTok (streaming)
   - Facebook, Instagram, LinkedIn, X (social)
   - Google Scholar, ResearchGate (scholars)
   - Notion, Trello, Asana (productivity)

---

### 3. ðŸ”— INTÃ‰GRATIONS SOCIAL PLATFORMS

CrÃ©er dans `apps/api/src/integrations/social-platforms/`:

```
social-platforms/
â”œâ”€â”€ youtube.py       # YouTube Data API
â”œâ”€â”€ twitch.py        # Twitch API
â”œâ”€â”€ tiktok.py        # TikTok for Developers
â”œâ”€â”€ facebook.py      # Meta Graph API
â”œâ”€â”€ instagram.py     # Instagram Basic Display
â”œâ”€â”€ linkedin.py      # LinkedIn API
â”œâ”€â”€ twitter.py       # X API v2
â”œâ”€â”€ notion.py        # Notion API
â”œâ”€â”€ google_scholar.py
â””â”€â”€ aggregator.py    # Unified data extraction
```

---

## ðŸ“ FICHIERS Ã€ COPIER DEPUIS UPLOADS

L'utilisateur a uploadÃ© ces fichiers qui n'ont pas encore Ã©tÃ© intÃ©grÃ©s:

```
/mnt/user-data/uploads/
â”œâ”€â”€ chenu-b35-nova3-core.js        # Nova v3 core
â”œâ”€â”€ chenu-b36-nova3-features.js    # Nova v3 features
â”œâ”€â”€ chenu-b46-computer-vision.ts   # Vision AI construction
â”œâ”€â”€ chenu-b47-multi-region.ts      # Multi-rÃ©gion/devises
â”œâ”€â”€ chenu-b48-global-integrations.ts
â”œâ”€â”€ roady-pricing-calculator.tsx
â”œâ”€â”€ roady-sprint51-conformite-qc.tsx
â”œâ”€â”€ MeetingRoom.tsx
â”œâ”€â”€ ROADY_API_Catalogue_Visual.html
â”œâ”€â”€ ROADY_Wireframe_UX.html
â””â”€â”€ PDFs (Lore Book, UX Deck, Avatar System, etc.)
```

---

## ðŸ—ï¸ STRUCTURE Ã€ UTILISER

```
/home/claude/chenu-v25/
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ web/src/
â”‚   â”‚   â”œâ”€â”€ app/           # App.tsx, Router
â”‚   â”‚   â”œâ”€â”€ spaces/        # 7 espaces (maison, entreprise, etc.)
â”‚   â”‚   â”œâ”€â”€ modules/       # creative-studio, social, forum, streaming, nova, che-learn, ia-labs, scholars
â”‚   â”‚   â”œâ”€â”€ components/    # layout, ui, avatars, widgets, search
â”‚   â”‚   â”œâ”€â”€ hooks/
â”‚   â”‚   â”œâ”€â”€ stores/
â”‚   â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â”œâ”€â”€ styles/themes/ # moderne, pierre, jungle, medieval
â”‚   â”‚   â””â”€â”€ types/
â”‚   â”œâ”€â”€ api/src/
â”‚   â”‚   â”œâ”€â”€ core/          # Nova Brain (master_mind, etc.)
â”‚   â”‚   â”œâ”€â”€ api/v1/        # Routes
â”‚   â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â””â”€â”€ integrations/  # stripe, quebec, google, openai, social-platforms
â”‚   â””â”€â”€ mobile/
â”œâ”€â”€ packages/
â”œâ”€â”€ infrastructure/
â”œâ”€â”€ docs/
â””â”€â”€ tests/
```

---

## ðŸ“Š MODULES DU SIDEBAR (Screenshot Excel)

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ â€¢ Personnals assistant      â”‚  â† Nova
â”‚ â€¢ Note                      â”‚
â”‚ â€¢ Notification              â”‚
â”‚ â€¢ My Team                   â”‚  â† HiÃ©rarchie agents
â”‚ â€¢ Database                  â”‚
â”‚ â€¢ My business               â”‚
â”‚ â€¢ Creative Studio           â”‚  â† 1 CLIC
â”‚   â”œâ”€â”€ Course                â”‚
â”‚   â””â”€â”€ Tutorial              â”‚
â”‚ â€¢ Scholar                   â”‚
â”‚   â””â”€â”€ Research              â”‚
â”‚ â€¢ Social Network            â”‚
â”‚   â”œâ”€â”€ Plateforme            â”‚
â”‚   â”œâ”€â”€ Che-Nu Social         â”‚
â”‚   â”œâ”€â”€ Post                  â”‚
â”‚   â”œâ”€â”€ Forum                 â”‚
â”‚   â””â”€â”€ Pages                 â”‚
â”‚ â€¢ Video streaming           â”‚
â”‚ â€¢ Government                â”‚
â”‚ â€¢ Association               â”‚
â”‚ â€¢ My account                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸŽ¯ ORDRE DE PRIORITÃ‰ SUGGÃ‰RÃ‰

1. **ðŸŽ¨ Avatars upgrade** (user request)
2. **ðŸ“± Social Network module** (high priority)
3. **ðŸŽ¬ Video Streaming module** (high priority)
4. **ðŸ‘¥ My Team module** (hiÃ©rarchie agents)
5. **ðŸ”¬ IA Labs module**
6. **ðŸ“š Scholars module**
7. **ðŸ”— Social platforms integrations**

---

## ðŸ“ NOTES IMPORTANTES

1. **CHEÂ·NU vs ROADY:** Le projet s'appelle maintenant **CHEÂ·NU** (Chez Nous), pas ROADY
2. **Multi-plateforme:** Chaque module doit pouvoir extraire data de notre plateforme ET des plateformes externes
3. **ThÃ¨mes:** 4 thÃ¨mes visuels (Moderne, Pierre, Jungle, MÃ©diÃ©val) - ne changent que le style, pas la fonction
4. **Nova:** Toujours visible, voit tous les espaces
5. **Permissions:** 3 niveaux (Global, Espace, Projet)

---

## ðŸ”— FICHIERS EXISTANTS UTILES

Dans le projet Claude:
- `/mnt/project/` contient beaucoup de fichiers existants
- `/home/claude/roady-v25-consolidated/` contient la consolidation prÃ©cÃ©dente
- `/mnt/user-data/uploads/` contient les derniers uploads

---

## âœ… CHECKLIST POUR PROCHAIN AGENT

- [ ] Lire ce fichier WORKLIST
- [ ] VÃ©rifier les uploads rÃ©cents dans `/mnt/user-data/uploads/`
- [ ] Commencer par l'upgrade avatars (prioritÃ© user)
- [ ] CrÃ©er les modules manquants un par un
- [ ] Respecter la structure `/home/claude/chenu-v25/`
- [ ] Mettre Ã  jour ce fichier avec la progression

---

**Bonne continuation! ðŸš€**
