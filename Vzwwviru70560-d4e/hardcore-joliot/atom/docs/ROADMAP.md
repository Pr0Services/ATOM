# AT-OM / CHE-NU (V76) — Roadmap (5 Phases)

This roadmap is written for two collaborating implementers:
- **Agent A (Chronicler)**: backend, data logic, determinism, traceability
- **Agent B (Architect)**: interface, visuals, glyph/mandala rendering

## Phase 1 — Alpha: Resonance (Arithmos)
**Goal:** deterministic conversion: `String -> Gematria -> Reduced -> (Hz, Color)`.
- Implement `core/arithmos.py` + `core/resonator.py`.
- Add unit tests for edge cases (empty string, accents, punctuation).
- Document the mapping table and rationale.

## Phase 2 — Beta: The Swarm (Oracles)
**Goal:** structured multi-agent output with provenance.
- Implement YAML-driven oracle profiles (`nexus/oracles_config.yaml`).
- Create a simple dispatcher layer (outside this starter repo) that:
  - routes tasks to the correct oracle,
  - requires `confidence` + `source_reference`,
  - blocks writes without provenance.

## Phase 3 — Gamma: The Sanctuary (Interface)
**Goal:** user sees the mandala; zero friction.
- Implement `interface/index.html` prototype.
- Render glyphs (SVG first, then Three.js if needed).
- Chromotherapy color mapping appears everywhere.

## Phase 4 — Delta: The Nexus (Causality)
**Goal:** graph storage and navigation.
- Replace JSON prototype with persistent store (SQL + graph table, or dedicated graph DB).
- Implement causality validation (no future links; no forbidden loops).

## Phase 5 — Omega: Transmedia (Book/Film/Game)
**Goal:** bind content artifacts to nodes (scripts, chapters, quests).
- Add media asset model.
- Add synchronization service (cascade updates on node edits).

---

### Definition of Done (V76 baseline)
- Deterministic arithmos + resonance mapping
- Working glyph preview
- Sample nexus schema validated and loadable
- Oracle config ready for runtime integration
