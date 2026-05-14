import { useParams } from "@tanstack/react-router";
import { useEffect, useRef } from "react";
import VncConnection from "./VNCViewer";

export const DeviceViewer = () => {
  const { deviceId } = useParams({ from: "/devices/$deviceId" });
  const connectionRef = useRef<VncConnection | null>(null);

  useEffect(() => {
    if (connectionRef.current !== null) {
      return;
    }

    connectionRef.current = new VncConnection(deviceId);
  }, [deviceId]);

  return (
    <div>
      <div id="vncDesktopName">Placeholder</div>
      <div id="vncStatus">Not Connected</div>
      {/* <canvas id="vncScreen" /> */}
      <div id="vncScreen"></div>
    </div>
  );
};
