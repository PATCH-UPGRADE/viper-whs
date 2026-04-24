import { Link } from "lucide-react";
import type React from "react";

export const AppSidebar: React.FC = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-64 bg-white shadow-md">
        <div className="p-6">
          <h1 className="text-2xl font-bold">WHS</h1>
        </div>
        <nav className="mt-6">
          <a
            href="/devices"
            className="flex items-center px-6 py-3 text-gray-700 bg-gray-100 border-r-4 border-blue-600"
          >
            <span className="mx-3">Devices</span>
          </a>
          <a href="/images" className="flex items-center px-6 py-3 mt-2 text-gray-600 hover:bg-gray-100 hover:text-gray-700 transition-colors">
            <span className="mx-3">Images</span>
          </a>
        </nav>
      </div>
    </div>
  );
};
