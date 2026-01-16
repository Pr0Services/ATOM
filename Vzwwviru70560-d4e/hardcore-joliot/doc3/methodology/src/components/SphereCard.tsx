import { Sphere } from "../data/spheres";
import { SphereStatus } from "../types/sphereState";

type Props = {
  sphere: Sphere;
  status: SphereStatus;
  onOpen: (id: string) => void;
};

export default function SphereCard({ sphere, status, onOpen }: Props) {
  const statusColors = {
    active: { bg: "#e8f5e9", border: "#a5d6a7", text: "#2e7d32" },
    dormant: { bg: "#fff3e0", border: "#ffcc80", text: "#e65100" },
    archived: { bg: "#f5f5f5", border: "#ccc", text: "#666" },
  };

  const colors = statusColors[status];

  return (
    <button
      onClick={() => onOpen(sphere.id)}
      style={{
        padding: "16px",
        border: `1px solid ${colors.border}`,
        borderRadius: "8px",
        background: "#fff",
        textAlign: "left",
        cursor: "pointer",
        width: "100%",
        opacity: status === "archived" ? 0.6 : 1,
      }}
      aria-label={`Open ${sphere.name}`}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div style={{ fontSize: "28px" }}>{sphere.emoji}</div>
        <span
          style={{
            fontSize: "10px",
            padding: "2px 6px",
            borderRadius: "4px",
            background: colors.bg,
            color: colors.text,
            textTransform: "uppercase",
          }}
        >
          {status}
        </span>
      </div>
      <strong style={{ display: "block", marginTop: "8px" }}>{sphere.name}</strong>
      <p style={{ marginTop: "8px", color: "#555", fontSize: "14px" }}>{sphere.description}</p>
    </button>
  );
}
