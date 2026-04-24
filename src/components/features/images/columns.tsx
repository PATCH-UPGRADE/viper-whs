import { zodResolver } from "@hookform/resolvers/zod";
import type { ColumnDef } from "@tanstack/react-table";
import { SquarePen, TrashIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";

import { Image } from "./types";

export const columns: ColumnDef<Image>[] = [
  {
    accessorKey: "id",
    meta: { title: "id" },
    header: "UUID",
  },
  {
    accessorKey: "name",
    meta: { title: "name" },
    header: "Image Name",
  },
  {
    accessorKey: "description",
    meta: { title: "description" },
    header: "Description",
  },
  {
    accessorKey: "type",
    meta: { title: "type" },
    header: "Type",
  },
  {
    accessorKey: "version",
    meta: { title: "version" },
    header: "Version",
  },
 
//   {
//     id: "actions",
//     enableHiding: false,
//     cell: ({ row }) => {
//       const data = row.original;

//       const deleteDevice = useDeleteDevice();
//       const handleRemove = () => {
//         deleteDevice.mutate({ id: data.id });
//       };

//       const updateDevice = useUpdateDevice();
//       const [open, setOpen] = useState(false);

//       const form = useForm<DeviceFormValues>({
//         resolver: zodResolver(deviceInputSchema),
//         defaultValues: {
//           name: data.name,
//           description: data.description,
//           type: data.type,
//           architecture: data.architecture,
//           cloud_init: data.cloud_init,
//           cpus: data.cpus,
//           memory: data.memory,
//           disk: data.disk,
//           disk_controller: data.disk_controller,
//           display: data.display,
//           image_id: data.image_id,
//           dhcp: data.dhcp,
//           mac_address: data.mac_address,
//           ipv4_manual: data.ipv4_manual,
//           gateway: data.gateway,
//           dns_servers: data.dns_servers,
//         },
//       });

//       const handleUpdate = (item: DeviceFormValues) => {
//         updateDevice.mutate(
//           { id: data.id, updateDevice: item },
//           {
//             onSuccess: () => {
//               form.reset();
//               setOpen(false);
//             },
//             onError: () => {
//               setOpen(true);
//             },
//           },
//         );
//       };

//       return (
//         <>
//           <Button
//             className=""
//             onClick={() => setOpen(true)}
//             disabled={updateDevice.isPending}
//           >
//             <SquarePen />
//             {updateDevice.isPending ? "Updating..." : "Update"}
//           </Button>
//           <Button
//             className=""
//             onClick={handleRemove}
//             disabled={deleteDevice.isPending}
//             variant="destructive"
//           >
//             <TrashIcon />
//             Delete Device
//           </Button>

//           {open && (
//             <DeviceCreateUpdateModal
//               form={form}
//               open={open}
//               setOpen={setOpen}
//               handleCreate={handleUpdate}
//               isUpdate={true}
//             />
//           )}
//         </>
//       );
//     },
//   },
];
