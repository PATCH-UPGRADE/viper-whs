import { RouterProvider } from "@tanstack/react-router";
import router from "./router";
import { AppSidebar } from "./components/features/AppSidebar";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex flex-col">
        <AppSidebar />
        <div className="flex flex-col">
          <RouterProvider router={router} />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
