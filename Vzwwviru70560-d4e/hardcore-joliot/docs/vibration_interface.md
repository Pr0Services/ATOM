# Interface « Vibrationnelle » — Notes d’implémentation (Film / Jeu)

## Objectif
Ajouter une couche sensorielle/artistique où certains concepts peuvent être:
- **sonifiés** (mappage nombres → notes / textures audio)
- **visualisés** (patterns, spectres, animations)

## Garde-fous (obligatoires)
- Afficher clairement : *« Métadonnée interprétative (créative), pas une vérité physique »*
- Ne jamais présenter ces valeurs comme des fréquences “réelles” d’un monument, d’une civilisation ou d’un mot.
- Tout “Nœud d’Or” doit être validé par un humain (et si possible un spécialiste) avant publication.

## Suggestion de sonification (simple)
- Méthode: MIDI (0–127)
- Entrée: somme A1Z26 ou ASCII
- Mapping:
  - note = (total % 24) + 48  (2 octaves au-dessus du Do2)
  - vélocité = clamp(30..100) selon confidence
  - durée = 0.2–1.2s selon score

Cette sonification est un **langage artistique** pour aider la narration et l’immersion.
