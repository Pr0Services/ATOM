# Scenario Generator Spec (v1)

## Inputs
- Need Canon: `catalog/need_canon.v1.yaml`
- Module Catalog: `catalog/module_catalog.v1.yaml`
- Scenario Templates: `scenarios/templates/*.json`
- Factor Library: `scenarios/factors/factor_library.v1.json`

## Output artifacts per run
- Run ID + seed
- Template chosen
- Factor assignment (combination lock digits)
- ModuleSet enabled with activation modes
- 30‑day activity plan (DSL script)
- Expected metrics targets (budgets, thresholds)
- Results capture schema (signals/backlogs/latency/cost)

## Generation algorithm (conceptual)
1) Choose template T
2) Draw factor values F from library (or provided config)
3) Derive primary needs N from template phase steps + circumstance
4) Select candidate modules M where needs_served intersects N
5) Add required dependencies closure
6) Assign activation modes per module using:
   - profile archetype
   - governance strictness
   - risk level + circumstance
   - budget profile
7) Build 30‑day plan:
   - day cadence from `cadence`
   - comms mix from `comms_mix`
   - integration steps from `integration_set`
   - XR entry from `xr_level`
8) Emit DSL script and validation report:
   - dependency satisfaction
   - invariants enforcement

## Combination‑Lock rule
- **Do not mutate template steps.**
- Only change factor digits and module activation modes.

## Recommended scale
- 1 template × 200 combinations = quick sweep
- 3 templates × 2,000 combinations = calibration run
- 6 templates × 10,000 combinations = stress run
