"use client";

import type { ColumnDef } from "@tanstack/react-table";
import type { Device } from "./types";

export const columns: ColumnDef<Device>[] = [
  {
    accessorKey: "name",
    meta: { title: "name" },
    header: "Name",
    accessorFn: (row) => row.name,
  },
  {
    accessorKey: "name",
    meta: { title: "name" },
    header: "Name",
    accessorFn: (row) => row.name,
  },
  {
    accessorKey: "name",
    meta: { title: "name" },
    header: "Name",
    accessorFn: (row) => row.name,
  },
];
