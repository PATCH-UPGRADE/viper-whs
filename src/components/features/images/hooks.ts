import { useMutation, useQueryClient } from "@tanstack/react-query";
import { carthageFetcher, carthageFetcherUpload } from "@/fetcher";
import type { Image, UploadImageResponseSchema } from "./types";

export const getImages = () => carthageFetcher<Image[]>("/images");

export const useUploadImage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FormData) =>
      carthageFetcherUpload<UploadImageResponseSchema>(`/images/upload`, {
        method: "post",
        body: data,
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["images"],
      });
      return data;
    },
    onError: (error) => {
      console.error(error);
    },
  });
};
