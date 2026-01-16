import { useState } from "react";
import { callSimpleAgent } from "../services/simpleAgent";
import { useSilence } from "../hooks/useSilence";

export default function AgentPanel() {
  const { silence } = useSilence();
  const [input, setInput] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (silence.enabled) {
    return (
      <section style={{ marginTop: "24px", borderTop: "1px solid #ddd", paddingTop: "16px" }}>
        <p style={{ color: "#888" }}>🔕 Mode silence actif — agent indisponible.</p>
      </section>
    );
  }

  const submit = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const res = await callSimpleAgent({ input });
    setOutput(res.output);
    setLoading(false);
  };

  return (
    <section style={{ marginTop: "24px", borderTop: "1px solid #ddd", paddingTop: "16px" }}>
      <h3 style={{ marginBottom: "12px" }}>🤖 Agent (manuel)</h3>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={4}
        style={{
          width: "100%",
          padding: "12px",
          border: "1px solid #ccc",
          borderRadius: "4px",
          fontSize: "14px",
          fontFamily: "inherit",
          resize: "vertical",
        }}
        placeholder="Écris une instruction claire…"
      />

      <button
        onClick={submit}
        disabled={loading}
        style={{
          marginTop: "8px",
          padding: "8px 16px",
          background: loading ? "#ccc" : "#333",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: loading ? "default" : "pointer",
          fontSize: "14px",
        }}
      >
        {loading ? "Traitement..." : "Appeler l'agent"}
      </button>

      {output && (
        <pre
          style={{
            marginTop: "12px",
            padding: "12px",
            background: "#f7f7f7",
            border: "1px solid #eee",
            borderRadius: "4px",
            whiteSpace: "pre-wrap",
            fontSize: "14px",
            overflow: "auto",
          }}
        >
          {output}
        </pre>
      )}
    </section>
  );
}
