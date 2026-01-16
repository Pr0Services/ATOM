import { useSilence } from "../hooks/useSilence";

export function SilenceToggle() {
  const { silence, toggle } = useSilence();

  return (
    <button
      onClick={toggle}
      style={{
        padding: "8px 12px",
        marginLeft: "12px",
        background: silence.enabled ? "#222" : "#eee",
        color: silence.enabled ? "#fff" : "#000",
        border: "1px solid #ccc",
        borderRadius: "4px",
        cursor: "pointer",
        fontSize: "14px",
      }}
      aria-label="Toggle silence mode"
    >
      {silence.enabled ? "🔕 Mode Silence" : "🔔 Mode Normal"}
    </button>
  );
}
