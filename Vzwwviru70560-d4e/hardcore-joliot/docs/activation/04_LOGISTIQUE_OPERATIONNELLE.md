# 4. Logistique Opérationnelle

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHAPITRE 4 — LOGISTIQUE TERRAIN                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 4.1 Mode Souverain (Offline)

### Objectif Principal

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRINCIPE DE SOUVERAINETÉ                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Fonctionnement GARANTI sans connexion Internet                 │
│                                                                  │
│   • Aucune dépendance critique externe                           │
│   • Autonomie complète pendant la phase d'activation             │
│   • Résilience face aux aléas réseau                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Mesures Techniques

| Mesure | Description | Statut |
|--------|-------------|--------|
| **Données locales** | LocalStorage + IndexedDB | Implémenté |
| **Scripts préparés** | Commandes pré-chargées | À préparer |
| **PWA Mode** | Service Worker pour offline | Configuré |
| **Cache Assets** | Images, fonts, CSS | Actif |

### Checklist Mode Souverain

- [ ] Application chargée et fonctionnelle sans réseau
- [ ] Données utilisateur persistées localement
- [ ] Commandes pré-définies accessibles
- [ ] Interface Cortex Admin utilisable offline
- [ ] Synchronisation différée configurée

---

## 4.2 Redondance Énergétique

### Matériel Requis

```
┌─────────────────────────────────────────────────────────────────────┐
│                    KIT ÉNERGIE TULUM                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   PRINCIPAL                                                         │
│   ├── Laptop chargé à 100%                                          │
│   │   └── Autonomie estimée : 4-6 heures                            │
│   │                                                                 │
│   BACKUP 1                                                          │
│   ├── Batterie externe 20,000+ mAh                                  │
│   │   └── Recharge complète supplémentaire                          │
│   │                                                                 │
│   BACKUP 2                                                          │
│   ├── Smartphone chargé (hotspot de secours)                        │
│   │   └── Avec forfait data international                           │
│   │                                                                 │
│   OPTIONNEL                                                         │
│   └── Deuxième batterie externe ou chargeur solaire                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Estimation de Consommation

| Activité | Consommation | Durée Max (batterie laptop) |
|----------|--------------|----------------------------|
| Écran luminosité max | Haute | ~3h |
| Écran luminosité 50% | Moyenne | ~5h |
| Mode économie | Basse | ~7h |

### Recommandations

1. **Luminosité** : Réduire à 60-70% (suffisant à l'aube)
2. **Wi-Fi/Bluetooth** : Désactiver si non utilisé
3. **Applications** : Fermer tout sauf navigateur/app CHE-NU
4. **Écran** : Mise en veille après 2 minutes d'inactivité

---

## 4.3 Protection Matérielle

### Risques Environnementaux à Tulum

```
┌──────────────────────────────────────────────────────────────────┐
│                    MENACES IDENTIFIÉES                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   🌊 HUMIDITÉ                                                    │
│      • Proximité océan = air salin                               │
│      • Rosée matinale importante                                 │
│      • Risque : corrosion, court-circuit                         │
│                                                                  │
│   🏖️ SABLE (SILICE)                                             │
│      • Particules fines omniprésentes                            │
│      • Risque : infiltration clavier, ports, ventilateurs        │
│                                                                  │
│   ☀️ CHALEUR                                                     │
│      • Température ambiante élevée                               │
│      • Risque : surchauffe, throttling CPU                       │
│                                                                  │
│   🦟 INSECTES                                                    │
│      • Moustiques à l'aube                                       │
│      • Distraction, inconfort                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Solutions de Protection

| Risque | Solution | Coût |
|--------|----------|------|
| **Humidité** | Housse étanche type "dry bag" | ~$15 |
| **Humidité** | Sachets dessicants (silica gel) | ~$5 |
| **Sable** | Cache-clavier silicone | ~$10 |
| **Sable** | Bouchons ports USB/jack | ~$5 |
| **Chaleur** | Support ventilé ou surélevé | ~$20 |
| **Insectes** | Répulsif, vêtements longs | Variable |

### Kit de Protection Recommandé

```
┌─────────────────────────────────────────────────────────────────────┐
│                    KIT PROTECTION MATÉRIEL                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   □ Housse étanche (dry bag ou pochette zip)                        │
│   □ 3-5 sachets silica gel (dessicant)                              │
│   □ Lingette microfibre (nettoyage écran)                           │
│   □ Cache-clavier silicone (si disponible)                          │
│   □ Petit support/rehausseur (ventilation)                          │
│   □ Répulsif anti-moustiques                                        │
│   □ Chapeau/casquette (ombre sur écran)                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4.4 Règles d'Utilisation Terrain

### Durée d'Exposition

```
┌──────────────────────────────────────────────────────────────────┐
│                    RÈGLE DE TEMPS                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Utilisation COURTE et CIBLÉE                                   │
│                                                                  │
│   • Session max : 90 minutes                                     │
│   • Pause technique : 10 min / heure                             │
│   • Pas de travail prolongé en environnement agressif            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Checklist Avant Sortie

- [ ] Batterie à 100%
- [ ] Application testée offline
- [ ] Housse de protection prête
- [ ] Dessicants dans le sac
- [ ] Backup énergie chargé
- [ ] Écran nettoyé
- [ ] Commandes préparées/mémorisées

### Checklist Après Retour

- [ ] Nettoyer l'appareil (sable, sel)
- [ ] Vérifier ports et clavier
- [ ] Laisser sécher si humidité
- [ ] Synchroniser les données
- [ ] Charger tous les appareils

---

## 4.5 Choix du Lieu Précis

### Critères de Sélection

| Critère | Priorité | Notes |
|---------|----------|-------|
| **Stabilité** | Haute | Surface plane, pas de sable direct |
| **Ombre** | Haute | Visibilité écran, protection thermique |
| **Calme** | Moyenne | Concentration, pas de touristes |
| **Vue** | Symbolique | Horizon Est visible (aube) |
| **Sécurité** | Haute | Pas de vol, pas de vagues |

### Lieux Suggérés à Tulum

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OPTIONS DE LIEU                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   OPTION A : Terrasse privée (hébergement)                          │
│   ├── + Sécurité maximale                                           │
│   ├── + Accès Wi-Fi backup                                          │
│   └── - Moins "symbolique"                                          │
│                                                                     │
│   OPTION B : Ruines de Tulum (si accès matinal)                     │
│   ├── + Vue iconique                                                │
│   ├── - Accès limité aux heures                                     │
│   └── - Touristes potentiels                                        │
│                                                                     │
│   OPTION C : Plage isolée (nord de Tulum)                           │
│   ├── + Calme, vue horizon                                          │
│   ├── - Risques environnementaux max                                │
│   └── - Sécurité variable                                           │
│                                                                     │
│   RECOMMANDÉ : Option A avec vue Est                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Points de Contrôle

- [ ] Mode offline testé et fonctionnel
- [ ] Kit énergie complet et chargé
- [ ] Kit protection matériel préparé
- [ ] Lieu choisi et repéré
- [ ] Timing validé (heure aube locale)

---

*Prochain chapitre : 05_PROTOCOLE_ATOM_GENESIS.md*
