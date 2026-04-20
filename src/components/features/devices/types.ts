import { z } from "zod";
import { ImageType, imageInputSchema } from "../images/types";

export enum DeviceArchitectureType {
  x86_64,
  aarch64,
}

export const deviceSchema = z.object({
  name: z.string().min(3),
  description: z.string(),
  type: z.enum(ImageType),
  architecture: z.enum(DeviceArchitectureType),
  cpus: z.number(),
  memory: z.number(),
  disk: z.number(),
  disk_controller: z.string(),
  display: z.boolean(),
  image: imageInputSchema.optional(),
  dhcp: z.boolean(),
  mac_address: z.string().optional(),
  ipv4_manual: z.string().optional(),
  gateway: z.string().optional(),
  dns_servers: z.array(z.string()),
});

export const devicesSchema = z.array(deviceSchema);

export const createDeviceSchema = z.object({});

export const updateDeviceSettingsSchema = z.object({});

export const typologyResponseSchema = z.object({});

export type DeviceResponse = z.infer<typeof deviceSchema>;
export type DevicesResponse = z.infer<typeof devicesSchema>;
