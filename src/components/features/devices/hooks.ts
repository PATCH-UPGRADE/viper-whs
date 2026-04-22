import { useMutation, useQueryClient } from "@tanstack/react-query";
import { carthageFetcher } from "@/fetcher";
import type { Device, DeviceFormValues } from "./types";

export const getDevices = () => carthageFetcher<Device[]>("/devices");

export const useCreateDevice = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newDevice: DeviceFormValues) =>
      carthageFetcher<Device>(`/device`, {
        method: "POST",
        body: JSON.stringify(newDevice),
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["devices"] });
      return data;
    },
    onError: (error) => {
      console.error(error);
    },
  });
};
