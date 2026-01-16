# AT-OM / CHE-NU (V76) — Workspace Seed

This repository seed implements the **minimum viable Resonance Engine** described in your architectural spec:

- `core/arithmos.py` — deterministic gematria (Pythagorean) + reduction
- `core/resonator.py` — assigns **444 Hz**-centered frequencies + chromotherapy colors
- `nexus/mapping_schema.json` — prototype graph schema + seed nodes (Fire, AI, Iron, Blood)
- `nexus/oracles_config.yaml` — 18-oracle swarm config (audit-first prompts)
- `interface/index.html` + `interface/glyphs.js` — lightweight mandala + SVG glyph prototype
- `production/templates/encyclopedia_layout.json` — canonical entry layout blueprint
- `docs/ROADMAP.md` + `docs/manifeste_technique.md`

## Quick run (prototype UI)
Open `interface/index.html` in a browser.

## Philosophy in code comments
Every file carries short notes so the system stays explainable and reviewable.

## Next integration step
Agent B can swap `interface/` rendering to Three.js. Agent A can plug `core/` into your backend service layer.
