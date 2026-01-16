# ============================================================================
# CHE·NU™ V69 — DATA_AI SPHERE POLICY
# ============================================================================
package che_nu.spheres.data_ai

default allow := true

# Data/AI exports require HITL (data leakage prevention)
deny_reason[msg] {
    input.request.agent.sphere == "data_ai"
    input.request.action.type == "export"
    not input.request.hitl.approved
    msg := "DATA_AI_EXPORT_REQUIRES_HITL"
}

# Model training actions require explicit approval
deny_reason[msg] {
    input.request.agent.sphere == "data_ai"
    input.request.action.type == "execute"
    input.request.action.target == "model_training"
    not input.request.hitl.approved
    msg := "DATA_AI_MODEL_TRAINING_REQUIRES_HITL"
}
