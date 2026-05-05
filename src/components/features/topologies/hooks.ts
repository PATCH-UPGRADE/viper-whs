import { carthageFetcher } from "@/fetcher";
import type { TopologyStatusResponseStatus } from "./types";

export const getDeploymentStatus = () =>
  carthageFetcher<TopologyStatusResponseStatus>(`/deployment-status`);

export const startDeploy = () =>
  carthageFetcher<null>(`/deploy`, {
    method: "POST",
    body: "",
  });
