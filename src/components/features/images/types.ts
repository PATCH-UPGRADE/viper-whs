import { z } from "zod";

export enum ImageType {
    "qcow2",
    "raw",
    "container",
}

export const imageInputSchema = z.object({
    name: z.string().min(1),
    description: z.string(),
    version: z.float32(),
    type: z.enum(ImageType),
});

export const imageOutputSchema = z.object({

})

export const imagesOutputSchema = z.array(imageInputSchema);

export const createInputSchema = z.object({});

export type ImageInput = z.infer<typeof imageInputSchema>;
export type ImageResponse = z.infer<typeof imageOutputSchema>;
export type ImagesResponse = z.infer<typeof imagesOutputSchema>;
