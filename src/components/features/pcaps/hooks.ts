import { useMutation, useQueryClient } from "@tanstack/react-query";
import { carthageFetcher, carthageFetcherUpload } from "@/fetcher";
import type { Pcap, UploadPcapResponseSchema } from "./types";

export const getPcaps = () => carthageFetcher<Pcap[]>("/pcaps");

export const useUploadPcap = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FormData) =>
      carthageFetcherUpload<UploadPcapResponseSchema>(`/pcaps/upload`, {
        method: "post",
        body: data,
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["pcaps"],
      });
      return data;
    },
    onError: (error) => {
      console.error(error);
    },
  });
};


export const useDeletePcap = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      carthageFetcher<Pcap>(`/pcaps/${id}`, {
        method: "DELETE",
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["pcaps"] });
      return data;
    },
    onError: (error) => {
      console.error(error);
    },
  });
};