import { z } from "zod";

export const topologySchema = z.object({});

export const topologiesSchema = z.array(topologySchema);

export const updateTopologySchema = z.object({});

export const typologyResponseSchema = z.object({});

export type TopologiesResponse = z.infer<typeof topologiesSchema>;
export type TypologyResponse = z.infer<typeof typologyResponseSchema>;
