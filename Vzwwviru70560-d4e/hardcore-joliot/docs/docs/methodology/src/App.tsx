import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import UniverseView from "./views/UniverseView";
import SphereView from "./views/SphereView";
import XRUniverseView from "./views/XRUniverseView";
import XRMeetingRoom from "./views/XRMeetingRoom";
import MethodologyView from "./views/MethodologyView";
import { loadSession } from "./state/sessionStore";

export default function App() {
  const session = loadSession();

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            session && session.lastRoute !== "/" ? (
              <Navigate to={session.lastRoute} replace />
            ) : (
              <UniverseView />
            )
          }
        />
        <Route path="/sphere/:id" element={<SphereView />} />
        <Route path="/xr" element={<XRUniverseView />} />
        <Route path="/xr/meeting/:id" element={<XRMeetingRoom />} />
        <Route path="/methodology" element={<MethodologyView />} />
      </Routes>
    </BrowserRouter>
  );
}
