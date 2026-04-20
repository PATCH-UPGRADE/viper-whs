import { carthageFetcher } from "@/fetcher";
import type { DevicesResponse } from "./types";

export const getDevices = () => carthageFetcher<DevicesResponse>("/devices");
