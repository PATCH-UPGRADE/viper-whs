import {
  createRootRoute,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import { DevicesContainer } from "./components/features/devices/Devices";

const rootRoute = createRootRoute();

const routes = [
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: () => <DevicesContainer />,
  }),
];

const routeTree = rootRoute.addChildren(routes);
const router = createRouter({ routeTree });

export default router;
