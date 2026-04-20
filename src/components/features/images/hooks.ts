import { carthageFetcher } from "@/fetcher";
import type { ImageInput, ImageResponse, ImagesResponse } from "./types";

export const getImages = () => carthageFetcher<ImagesResponse>("/images");

export const updateImage = (payload: ImageInput) =>
  carthageFetcher<ImageResponse>(`/images`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
