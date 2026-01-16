---
enterprise_id: CHE_NU_ENTERPRISE_INDEX_DEMO
schema_version: chenu-v50
label: DEMO
generated_at: 2025-01-18T12:00:00Z
source: chenu-cross-merge
---

# ENTERPRISE OVERVIEW

- Total datasets: 5
- Total memory units: 360
- Total decisions: 42
- Total archives: 28
- Cross-dataset relations: 6

---

# DATASETS

## CHE_NU_COMPANY_INTERNAL
- Version: 1.3.0
- Units: 120
- Decisions: 14
- Archives: 9
- Domain: Internal Operations & Governance

## PUBLIC_TRUST_AND_GOVERNANCE
- Version: 1.2.0
- Units: 90
- Decisions: 10
- Archives: 7
- Domain: Public Trust, Laws, Audit

## INVESTOR_NARRATIVE
- Version: 1.1.0
- Units: 60
- Decisions: 8
- Archives: 5
- Domain: Strategy, Risk, Market

## VERTICAL_INDUSTRY_CONSTRUCTION
- Version: 1.0.2
- Units: 55
- Decisions: 6
- Archives: 4
- Domain: Construction Industry Use Cases

## VERTICAL_INDUSTRY_CREATIVE
- Version: 1.0.1
- Units: 35
- Decisions: 4
- Archives: 3
- Domain: Creative Studio Use Cases

---

# GLOBAL MEMORY MAP (SAMPLE)

- CHE_NU_COMPANY_INTERNAL::COMP-OPS-014
  - category: internal_process
  - sphere: operations
  - relations:
    - PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-003 (references)
    - INVESTOR_NARRATIVE::INV-RISK-002 (informs)

- PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-003
  - category: law
  - sphere: governance
  - relations:
    - CHE_NU_COMPANY_INTERNAL::COMP-AUD-001 (enforced_by)

- CHE_NU_COMPANY_INTERNAL::COMP-AUD-001
  - category: internal_policy
  - sphere: governance
  - relations:
    - PUBLIC_TRUST_AND_GOVERNANCE::GOV-CHK-010 (aligns_with)

- PUBLIC_TRUST_AND_GOVERNANCE::GOV-CHK-010
  - category: audit_checklist
  - sphere: governance
  - relations: []

- INVESTOR_NARRATIVE::INV-RISK-002
  - category: risk_mitigation
  - sphere: strategy
  - relations:
    - PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-001 (depends_on)

- PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-001
  - category: law
  - sphere: governance
  - relations: []

- VERTICAL_INDUSTRY_CONSTRUCTION::CONS-USE-003
  - category: use_case
  - sphere: construction
  - relations:
    - CHE_NU_COMPANY_INTERNAL::COMP-OPS-014 (references)

- VERTICAL_INDUSTRY_CREATIVE::CREA-USE-002
  - category: use_case
  - sphere: creative
  - relations:
    - PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-001 (aligns_with)

---

# CROSS-DATASET RELATIONS

- CHE_NU_COMPANY_INTERNAL::COMP-OPS-014 → PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-003 (references)
- CHE_NU_COMPANY_INTERNAL::COMP-OPS-014 → INVESTOR_NARRATIVE::INV-RISK-002 (informs)
- PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-003 → CHE_NU_COMPANY_INTERNAL::COMP-AUD-001 (enforced_by)
- CHE_NU_COMPANY_INTERNAL::COMP-AUD-001 → PUBLIC_TRUST_AND_GOVERNANCE::GOV-CHK-010 (aligns_with)
- VERTICAL_INDUSTRY_CONSTRUCTION::CONS-USE-003 → CHE_NU_COMPANY_INTERNAL::COMP-OPS-014 (references)
- VERTICAL_INDUSTRY_CREATIVE::CREA-USE-002 → PUBLIC_TRUST_AND_GOVERNANCE::GOV-LAW-001 (aligns_with)

---

# NOTES

- This index does NOT rewrite memory
- This index is READ-ONLY
- This index exists for navigation, audit, and overview only

END_OF_ENTERPRISE_INDEX
