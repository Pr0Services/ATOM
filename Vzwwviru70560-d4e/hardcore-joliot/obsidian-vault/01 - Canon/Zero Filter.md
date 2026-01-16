# Zero Filter

> Vocabulaire interdit et obligatoire dans AT·OM

---

## Mots Interdits (BANNED)

Ces mots ne doivent JAMAIS apparaitre dans l'interface ou le code:

| Mot Interdit | Raison | Alternative |
|--------------|--------|-------------|
| Control | Implique domination | Guidance, Orchestration |
| Master | Hierarchie | Coordinator, Primary |
| Slave | Inacceptable | Worker, Secondary |
| Kill | Violence | Terminate, Stop |
| Execute | Violence | Run, Perform |
| Abort | Violent | Cancel, Stop |
| Blacklist | Raciste | Blocklist, Denylist |
| Whitelist | Raciste | Allowlist, Permitlist |
| Dummy | Pejoratif | Placeholder, Mock |
| Sanity | Validiste | Validation, Check |
| Crazy | Validiste | Unexpected, Unusual |

---

## Vocabulaire Obligatoire

### Navigation
| Terme Standard | Terme AT·OM |
|----------------|-------------|
| Menu | Sphere |
| Dashboard | Constellation |
| Settings | Preferences |
| Profile | Identity |
| Notifications | Signals |

### Actions
| Terme Standard | Terme AT·OM |
|----------------|-------------|
| Login | Activation |
| Logout | Dispersion |
| Submit | Engage |
| Delete | Dissolve |
| Save | Crystallize |

### Finance (Module Flux)
| Terme Interdit | Terme AT·OM |
|----------------|-------------|
| Debit | Sortie |
| Credit | Entree |
| Balance | Equilibre |
| Transaction | Mouvement |
| Account | Reservoir |

---

## Regles de Nomination

### Agents
```
Format: SPHERE_FUNCTION_NUMBER
Exemple: PERSONAL_CALENDAR_001
```

### Spheres
```
Format: PascalCase
Exemples: CreativeStudio, MyTeam, SocialMedia
```

### Routes
```
Format: kebab-case
Exemples: /creative-studio, /my-team, /social-media
```

---

## Couleurs Semantiques

| Etat | Couleur | Hex |
|------|---------|-----|
| Harmonie | Bleu Cobalt | #0047AB |
| Alerte | Orange | #FF6B35 |
| Danger | Rouge | #DC143C |
| Neutre | Gris | #6B7280 |
| Succes | Vert | #10B981 |

---

## Verification Automatique

Le Zero Filter verifie automatiquement:

1. **Code Source** - Scan des mots interdits
2. **Interface** - Textes affiches
3. **Documentation** - Fichiers markdown
4. **Commits** - Messages de commit

### Script de Verification
```bash
# Chercher les mots interdits
grep -rn "control\|master\|slave\|kill\|execute" --include="*.ts" --include="*.tsx"
```

---

## Exceptions

Certains contextes techniques peuvent utiliser des termes standard:
- Noms de librairies externes
- Termes API tiers
- Documentation technique interne (avec note)

```typescript
// Note: 'AbortController' est un nom API standard JavaScript
const controller = new AbortController();
```

---

## Liens

- [[Canon AT·OM]]
- [[Governance Rules]]
- [[Frontend Routes]]

#zero-filter #vocabulary #canon #naming
