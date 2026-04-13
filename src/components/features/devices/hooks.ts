import { carthageFetcher } from "@/fetcher";
import { DevicesResponse } from "./types";

export const getDevices = () => carthageFetcher<DevicesResponse>("/devices");
