import { carthageFetcher } from "@/fetcher";
import { TopologiesResponse } from "./types";

export const getTopologies = () => carthageFetcher<TopologiesResponse>(`/topologies`);
