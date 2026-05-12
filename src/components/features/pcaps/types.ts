import { z } from "zod";

export const pcapOutputSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
});

export const pcapUploadInputSchema = z.object({
  file: z.instanceof(File),
  description: z.string(),
});

export const pcapUploadResponseSchema = z.object({
  message: z.string(),
});

export type Pcap = z.infer<typeof pcapOutputSchema>;
export type PcapUploadFormValues = z.infer<typeof pcapUploadInputSchema>;
export type UploadPcapResponseSchema = z.infer<
  typeof pcapUploadResponseSchema
>;
