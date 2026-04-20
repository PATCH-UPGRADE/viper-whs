import { carthageFetcher } from "@/fetcher";
import type { TopologiesResponse } from "./types";

export const getTopologies = () =>
  carthageFetcher<TopologiesResponse>(`/topologies`);
