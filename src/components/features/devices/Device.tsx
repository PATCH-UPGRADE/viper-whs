import { useParams } from "@tanstack/react-router";
import { SlashIcon } from "lucide-react";
import { useEffect, useRef } from "react";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
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
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/devices">All Devices</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator>
            <SlashIcon />
          </BreadcrumbSeparator>
          <BreadcrumbItem>
            <BreadcrumbPage>{deviceId}</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      <div id="vncDesktopName" className="mt-3">
        N/A
      </div>
      <div id="vncStatus">Not Connected</div>
      <div id="vncScreen" className="mt-1"></div>
    </div>
  );
};
