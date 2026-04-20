import { useQuery } from "@tanstack/react-query";
import { getDevices } from "./hooks";
import type { DevicesResponse } from "./types";

export const DevicesContainer = () => {
  const {
    data: devices,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ["topologies"],
    queryFn: getDevices,
  });

  if (isPending) {
    return <DevicesLoading />;
  }

  if (isError) {
    console.error(error);
    return <DevicesError />;
  }

  return <DevicesList devices={devices} />;
};

const DevicesLoading = () => {
  return <div>Devices loading...</div>;
};

const DevicesError = () => {
  return <div>An error occured while loading Devices!</div>;
};

interface DevicesListI {
  devices: DevicesResponse;
}

const DevicesList = ({ devices }: DevicesListI) => {
  return (
    <div>
      {devices.map((device, index) => (
        <div key={index}>{device.name}</div>
      ))}
    </div>
  );
};
