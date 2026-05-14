import {
  createRootRoute,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import { DeviceViewer } from "./components/features/devices/Device";
import { DevicesContainer } from "./components/features/devices/Devices";
import { ImagesContainer } from "./components/features/images/Images";
import { TopologiesContainer } from "./components/features/topologies/Topologies";

const rootRoute = createRootRoute();

const routes = [
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: () => <DevicesContainer />,
  }),
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/devices/$deviceId",
    component: () => <DeviceViewer />,
  }),
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/devices",
    component: () => <DevicesContainer />,
  }),
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/images",
    component: () => <ImagesContainer />,
  }),
  createRoute({
    getParentRoute: () => rootRoute,
    path: "/topologies",
    component: () => <TopologiesContainer />,
  }),
];

const routeTree = rootRoute.addChildren(routes);
const router = createRouter({ routeTree });

export default router;
