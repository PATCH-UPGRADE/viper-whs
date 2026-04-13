import React from "react";
import { DeviceResponse, DevicesResponse } from "./types";
import { useQuery } from "@tanstack/react-query";
import { getDevices } from "./hooks";

export const DevicesContainer = () => {
    const { data: devices, isPending, isError, error } = useQuery({
        queryKey: ["topologies"],
        queryFn: getDevices,
    });

    if (isPending) {
        return (<DevicesLoading />);
    }

    if (isError) {
        return (<DevicesError />);
    }

    return (
        <DevicesList devices={devices} />
    );
}

const DevicesLoading = () => {
    return (
        <div>Devices loading...</div>
    );
}

const DevicesError = () => {
    return (
        <div>An error occured while loading Devices!</div>
    );
}

interface DevicesListI {
    devices: DevicesResponse;
}

const DevicesList = ({ devices }: DevicesListI) => {
    return (
        <div>
            {devices.map((device, index) => (
                <div key={index}>
                    {device.name}
                </div>
            ))}
        </div>
    );
}
