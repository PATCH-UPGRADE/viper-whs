from __future__ import annotations

from pydantic import BaseModel, Field

from carthage import Machine
from carthage.deployment import Deployable, DeploymentFailure, DeploymentResult
from carthage.network import TechnologySpecificNetwork, this_network

from .models import Device

"""
Models for dynamic Carthage objects that are transported to the frontend.
"""

__all__: list[str] = []


class DeviceDeployable(BaseModel):
    """A device as actually deployed."""

    id: str
    name: str


__all__ += ["DeviceDeployable"]


class NetworkDeployable(BaseModel):
    """A network in the topology."""

    name: str
    network: str = Field(description="The network and netmask in CIDR notation")


__all__ += ["NetworkDeployable"]


FrontendDeployable = DeviceDeployable | NetworkDeployable

__all__ += ["FrontendDeployable"]


class FrontendDeploymentResult(BaseModel):
    running: bool = False
    successes: list[FrontendDeployable] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)
    dependency_failures: list[str] = Field(default_factory=list)
    ignored: list[FrontendDeployable] = Field(default_factory=list)
    orphans: list[FrontendDeployable] = Field(default_factory=list)


__all__ += ["FrontendDeploymentResult"]


def map_deployable(d: Deployable) -> FrontendDeployable | None:
    match d:
        case Machine(device_model=Device() as model) as machine:
            return DeviceDeployable(id=model.id, name=machine.name)
        case TechnologySpecificNetwork() as net:
            model = net.injector.get_instance(this_network)
            try:
                cidr = str(model.v4_config.network)
            except AttributeError:
                cidr = ""
            return NetworkDeployable(name=model.name, network=cidr)
        case _:
            return None


__all__ += ["map_deployable"]


def map_deployables(deployables: list[Deployable]) -> list[FrontendDeployable]:
    return [frontend for deployable in deployables if (frontend := map_deployable(deployable))]


__all__ += ["map_deployables"]


def map_deployment_failure(failure: DeploymentFailure) -> str:
    return str(failure)


def map_deployment_result(
    result: DeploymentResult,
    *,
    running: bool = False,
) -> FrontendDeploymentResult:
    return FrontendDeploymentResult(
        running=running,
        successes=map_deployables(result.successes),
        failures=[map_deployment_failure(f) for f in result.failures],
        dependency_failures=[map_deployment_failure(d) for d in result.dependency_failures],
        ignored=map_deployables(result.ignored),
        orphans=map_deployables(result.orphans),
    )


__all__ += ["map_deployment_result"]
