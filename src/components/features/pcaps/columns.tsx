import type { ColumnDef } from "@tanstack/react-table";
import { TrashIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useDeletePcap } from "./hooks";
import type { Pcap } from "./types";

export const columns: ColumnDef<Pcap>[] = [
  {
    accessorKey: "id",
    meta: { title: "id" },
    header: "UUID",
  },
  {
    accessorKey: "name",
    meta: { title: "name" },
    header: "Pcap Name",
  },
  {
    accessorKey: "description",
    meta: { title: "description" },
    header: "Description",
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const data = row.original;

      const deletePcap = useDeletePcap();
      const handleRemove = () => {
        deletePcap.mutate(data.id);
      };

      return (
        <Button
          className=""
          onClick={handleRemove}
          disabled={deletePcap.isPending}
          variant="destructive"
        >
          <TrashIcon />
          Delete
        </Button>
      );
    },
  },
];
