import { useState } from "react";
import { Methodology } from "../../types/methodology";
import { METHODOLOGY_REGISTRY } from "../../data/methodologyRegistry";
import { useSilence } from "../../hooks/useSilence";

type MethodologySelectorProps = {
  selectedId: string | null;
  onSelect: (methodologyId: string, context: string) => void;
  onClear: () => void;
  sphereContext?: string;
};

export function MethodologySelector({
  selectedId,
  onSelect,
  onClear,
  sphereContext,
}: MethodologySelectorProps) {
  const { silence } = useSilence();
  const [context, setContext] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const handleSelect = (methodology: Methodology) => {
    const finalContext = context.trim() || sphereContext || "Sélection manuelle";
    onSelect(methodology.id, finalContext);
    setContext("");
  };

  const selectedMethodology = METHODOLOGY_REGISTRY.find((m) => m.id === selectedId);

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "8px",
        border: "1px solid #ddd",
        padding: "16px",
      }}
    >
      <h3 style={{ margin: "0 0 16px 0", fontSize: "16px", color: "#333" }}>
        📋 Méthodologie
      </h3>

      {/* Current selection */}
      {selectedMethodology && (
        <div
          style={{
            marginBottom: "16px",
            padding: "12px",
            background: "#e8f5e9",
            borderRadius: "6px",
            border: "1px solid #a5d6a7",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong style={{ color: "#2e7d32" }}>Active: {selectedMethodology.name}</strong>
              <p style={{ margin: "4px 0 0 0", fontSize: "12px", color: "#666" }}>
                {selectedMethodology.description}
              </p>
            </div>
            <button
              onClick={onClear}
              style={{
                padding: "6px 12px",
                background: "#fff",
                border: "1px solid #ccc",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "12px",
              }}
            >
              ✕ Désélectionner
            </button>
          </div>
        </div>
      )}

      {/* Context input */}
      {!selectedMethodology && (
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "13px", color: "#666", display: "block", marginBottom: "6px" }}>
            Contexte d'application (optionnel):
          </label>
          <input
            type="text"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Ex: Projet résidentiel Brossard..."
            style={{
              width: "100%",
              padding: "8px 12px",
              border: "1px solid #ddd",
              borderRadius: "4px",
              fontSize: "13px",
            }}
          />
        </div>
      )}

      {/* Methodology list */}
      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {METHODOLOGY_REGISTRY.map((methodology) => {
          const isSelected = methodology.id === selectedId;
          const isExpanded = methodology.id === expandedId;

          return (
            <div
              key={methodology.id}
              style={{
                border: `1px solid ${isSelected ? "#a5d6a7" : "#ddd"}`,
                borderRadius: "6px",
                overflow: "hidden",
                background: isSelected ? "#f1f8e9" : "#fff",
              }}
            >
              {/* Header */}
              <div
                onClick={() => setExpandedId(isExpanded ? null : methodology.id)}
                style={{
                  padding: "12px",
                  cursor: "pointer",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div>
                  <strong style={{ fontSize: "14px" }}>{methodology.name}</strong>
                  <div style={{ fontSize: "11px", color: "#888", marginTop: "2px" }}>
                    Complexité: {methodology.suitedFor.complexity} | Volume:{" "}
                    {methodology.suitedFor.volume}
                  </div>
                </div>
                <span style={{ fontSize: "12px", color: "#888" }}>
                  {isExpanded ? "▲" : "▼"}
                </span>
              </div>

              {/* Expanded content */}
              {isExpanded && (
                <div style={{ padding: "0 12px 12px 12px", borderTop: "1px solid #eee" }}>
                  <p style={{ margin: "12px 0", fontSize: "13px", color: "#666" }}>
                    {methodology.description}
                  </p>

                  {/* Suited for */}
                  <div style={{ marginBottom: "12px" }}>
                    <strong style={{ fontSize: "12px", color: "#666" }}>Domaines:</strong>
                    <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", marginTop: "4px" }}>
                      {methodology.suitedFor.domains.map((domain) => (
                        <span
                          key={domain}
                          style={{
                            padding: "2px 8px",
                            background: "#e3f2fd",
                            borderRadius: "12px",
                            fontSize: "11px",
                            color: "#1565c0",
                          }}
                        >
                          {domain}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Steps */}
                  <div style={{ marginBottom: "12px" }}>
                    <strong style={{ fontSize: "12px", color: "#666" }}>Étapes:</strong>
                    <ol style={{ margin: "8px 0", paddingLeft: "20px", fontSize: "12px" }}>
                      {methodology.steps.map((step, index) => (
                        <li key={index} style={{ marginBottom: "4px", color: "#555" }}>
                          {step}
                        </li>
                      ))}
                    </ol>
                  </div>

                  {/* Select button */}
                  {!isSelected && (
                    <button
                      onClick={() => handleSelect(methodology)}
                      style={{
                        width: "100%",
                        padding: "10px",
                        background: "#4a90d9",
                        color: "#fff",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "13px",
                      }}
                    >
                      ✓ Sélectionner cette méthodologie
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Silence mode notice - no suggestions */}
      {silence.enabled && (
        <div
          style={{
            marginTop: "16px",
            padding: "10px",
            background: "#f5f5f5",
            borderRadius: "4px",
            fontSize: "12px",
            color: "#666",
          }}
        >
          🔕 Mode silence — Aucune suggestion automatique
        </div>
      )}
    </div>
  );
}
