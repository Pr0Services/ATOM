# RUN: example.onboarding_30d
# template: template.onboarding_30d.v1
# factors:
#   profile_archetype: novice_guided
#   circumstance: exploration_phase
#   cadence: medium
#   budget_profile: normal
#   comms_mix: [comms.chat, meetings.core]
#   integration_set: [integrations.gdrive, integrations.email]
#   xr_level: blueprint_basic
#   governance_strictness: medium

DAY 1:
  ACTION register {{email: "user1@example.com"}}
  ACTION login {{email: "user1@example.com"}}
  ACTIVATE auth.core enabled_guided
  ACTIVATE identity.boundary enabled_restricted
  ACTION select_sphere {{sphere_id: "personal"}}
  ACTION create_thread {{founding_intent: "Start a community project plan"}}
  ACTIVATE threads.v2 enabled_balanced

DAY 2:
  ACTION nova.chat {{message: "Help me define the project scope and first steps"}}
  ACTIVATE nova.pipeline enabled_guided
  ACTIVATE governance.cea enabled_balanced
  ACTIVATE governance.orchestrator enabled_balanced
  DECISION_POINT create {{type: "scope_choice", options: ["small","medium","large"]}}

DAY 3:
  INTEGRATION integrations.gdrive import_files
  INTEGRATION integrations.email import_inbox
  ACTION nova.chat {{message: "Summarize imported documents and propose tasks"}}
  EXPECT p95_latency_ms < 1800
  EXPECT noise_rate < 0.15

DAY 7:
  MEETING 45 {{agenda_ref: "weekly_review"}}
  ACTION nova.chat {{message: "Weekly review and next actions"}}

DAY 14:
  INJECT disconnect {{duration_min: 20}}
  ACTION nova.chat {{message: "Continue offline notes; sync later"}}

DAY 30:
  ACTION nova.chat {{message: "Monthly retrospective: what worked, what to improve"}}
  EXPECT escape_rate < 0.08
  EXPECT abandonment_rate < 0.2
