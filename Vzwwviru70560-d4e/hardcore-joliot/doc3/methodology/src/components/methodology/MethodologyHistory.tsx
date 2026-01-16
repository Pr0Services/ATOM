import { MethodologyApplication } from "../../types/methodology";
import { getMethodologyById } from "../../data/methodologyRegistry";

type MethodologyHistoryProps = {
  history: MethodologyApplication[];
};

export function MethodologyHistory({ history }: MethodologyHistoryProps) {
  if (history.length === 0) {
    return (
      <div
        style={{
          background: "#fff",
          borderRadius: "8px",
          border: "1px solid #ddd",
          padding: "16px",
        }}
      >
        <h4 style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#666" }}>
          📜 Historique d'application
        </h4>
        <p style={{ margin: 0, fontSize: "13px", color: "#888" }}>
          Aucune méthodologie appliquée pour le moment.
        </p>
      </div>
    );
  }

  // Show most recent first
  const sortedHistory = [...history].reverse();

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "8px",
        border: "1px solid #ddd",
        padding: "16px",
      }}
    >
      <h4 style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#666" }}>
        📜 Historique d'application
      </h4>

      <div
        style={{
          maxHeight: "300px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "8px",
        }}
      >
        {sortedHistory.map((application) => {
          const methodology = getMethodologyById(application.methodologyId);

          return (
            <div
              key={application.id}
              style={{
                padding: "10px",
                background: "#f9f9f9",
                borderRadius: "6px",
                border: "1px solid #eee",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <strong style={{ fontSize: "13px", color: "#333" }}>
                    {methodology?.name || application.methodologyId}
                  </strong>
                  <p style={{ margin: "4px 0 0 0", fontSize: "12px", color: "#666" }}>
                    {application.context}
                  </p>
                </div>
                <span
                  style={{
                    fontSize: "11px",
                    color: "#888",
                    fontFamily: "monospace",
                    whiteSpace: "nowrap",
                  }}
                >
                  {formatDate(application.appliedAt)}
                </span>
              </div>

              {application.sphereId && (
                <div style={{ marginTop: "6px" }}>
                  <span
                    style={{
                      padding: "2px 6px",
                      background: "#e8eaf6",
                      borderRadius: "4px",
                      fontSize: "10px",
                      color: "#5c6bc0",
                    }}
                  >
                    Sphère: {application.sphereId}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <p
        style={{
          margin: "12px 0 0 0",
          fontSize: "11px",
          color: "#999",
          fontStyle: "italic",
        }}
      >
        Lecture seule — L'historique ne peut pas être modifié
      </p>
    </div>
  );
}

function formatDate(date: Date): string {
  return date.toLocaleDateString("fr-CA", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}
