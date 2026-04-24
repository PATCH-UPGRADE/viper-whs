from pydantic import BaseModel, Field
from carthage import Machine, Deployable, DeploymentFailure, DeploymentResult
from carthage.network  import TechnologySpecificNetwork, this_network

'''
Models for dynamic Carthage objects that are transported to the frontend
'''
__all__ = []

class DeviceDeployable(BaseModel):
    '''A device as actually deployed
    '''
    
    id: str
    name: str

__all__ += ['DeviceDeployable']

class NetworkDeployable(BaseModel):

    '''A netork in the topology
    '''
    name: str
    network: str = Field(description='The network and netmask in CIDR notation')

__all__ += ['NetworkDeployable']

FrontendDeployable = DevideDeployable | NetworkDeployable

__all__ += ['FrontendDeployable']

class FrontendDeploymentFailure(BaseModel):
    deployable: FrontendDeployable | None = None
    failure:str

class FrontendDeployableResult(BaseModel):
    successes: list[FrontendDeployable] = []
    failures: list[FrontendDeployableFailure] = []
    dependency_failures: list[FrontendDeployableFailure] = []
    ignored: list[FrontendDeployable] = []
    orphans: list[FrontendDeployable] = []

__all__ += ['FrontendDeploymentResult']

def map_deployable(d:Deployable)-> FrontendDeployable|None:
    match d:
        case Machine(device_model=Device() as model) as machine:
            return DeployableDevice(id=model.id, name=machine.name)
        case TechnologySpecificNetwork() as net:
            model = net.injector.get_instance(this_network)
            try:
                cidr = str(model.v4_config.network)
            except AttributeError:
                cidr = ""
            return NetworkDeployable(name=model.name, network=cidr)
        case _:
            return

__all__ += ['map_deployable']

def map_deployables(deployables: list[Deployable])-> list[FrontendDeployable]:
    return [fd for  d in deployables if fd := map_deployable(d)]

__all__ += ['map_deployables']
def map_deployment_failure(failure:DeploymentFailure)-> str:
    return str(failure)

def map_deployment_result(result:DeploymentResult)-> FrontendDeploymentResult:
    frontend_result = FrontendDeploymentResult(
        successes = map_deployables(result.successes),
        failures=[map_deployment_failure(f) for f in result.failures],
        dependency_failures=[map_deployment_failure(d) for d in result.dependency_failures],
        ignored=map_deployables(result.ignored),
        orphans=map_deployables(result.orphans))
    return frontend_result

__all__ += ['map_deployment_result']
