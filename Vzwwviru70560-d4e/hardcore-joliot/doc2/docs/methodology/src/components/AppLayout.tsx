import { ReactNode } from "react";
import { SilenceToggle } from "./SilenceToggle";

type AppLayoutProps = {
  title?: string;
  showBack?: boolean;
  onBack?: () => void;
  children: ReactNode;
};

export function AppLayout({ title, showBack, onBack, children }: AppLayoutProps) {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "#f5f5f5",
      }}
    >
      <header
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "12px 16px",
          borderBottom: "1px solid #ddd",
          background: "#ffffff",
        }}
      >
        {showBack && (
          <button
            onClick={onBack}
            style={{
              padding: "6px 12px",
              cursor: "pointer",
              background: "#f5f5f5",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "14px",
            }}
          >
            ← Retour
          </button>
        )}
        <h1 style={{ margin: 0, fontSize: "18px" }}>{title ?? "CHE·NU"}</h1>
        <div style={{ marginLeft: "auto" }}>
          <SilenceToggle />
        </div>
      </header>

      <main style={{ padding: "16px", flex: 1 }}>{children}</main>
    </div>
  );
}
