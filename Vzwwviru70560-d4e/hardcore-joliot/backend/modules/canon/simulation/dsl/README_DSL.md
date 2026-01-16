# Simulation DSL (30‑Day Runs)

## Purpose
A compact script format to represent a full onboarding/project life over 30 days.

## Core primitives
- DAY n:
  - ACTION <type> <payload>
  - CALL <channel> <duration_min> <topic>
  - MEETING <duration_min> <agenda_ref>
  - ACTIVATE <module_id> <mode>
  - INTEGRATION <provider> <operation>
  - DECISION_POINT <create|respond|defer|archive> <payload>
  - EXPECT <metric> <target>
  - INJECT <fault> (disconnect, latency, malformed_input, etc.)

## Notes
- All actions ultimately append ThreadEvents (append‑only)
- Governance runs can be explicit or implicit (Nova pipeline)

See examples in `simulation/dsl/examples/`.
