from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, IPvAnyAddress
import yaml

default_model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        validate_assignment=True,
    )

class VmImage(BaseModel):
    model_config = default_model_config
    name: str = Field(description='Name of the image', min_length=1, max_length=64)
    description: str = Field(description='Description or tags', default='')
    version: float = Field(default=1.00)
    type: Literal['qcow2', 'raw'] = Field(description='Type of image being used, qcow2 or raw', default='raw')

class ContainerImage(BaseModel):
    model_config = default_model_config
    name: str = Field(description='Name of the image', min_length=1, max_length=64)
    description: str = Field(description='Description or tags', default='')
    version: float = Field(default=1.00)

class Device(BaseModel):
    model_config = default_model_config

    name: str = Field(description='Name of the device', min_length=3, max_length=20)
    description: str = Field(description='Description or tags', default='')
    type: Literal['vm', 'container'] = Field(description='Type of device, vm or container. Only vm is supported today.', default='vm')
    cloud_init: bool = Field(description='Use cloud init', default=True)

    architecture: Literal['x86_64', 'arm_aarch64'] = Field(description='Architecture of the device, x86_64 or arm_aarch64', default='x86_64')
    cpus: int = Field(description='Number of CPUs assigned', default=2)
    memory: int = Field(description='System memory (in MB) assigned', default=4096)
    disk: int = Field(description='Disk size (in GB)', default=20)
    disk_controller: str = Field(description='Controller used for disk', default='virtio')
    display: bool = Field(description='Display needed', default=False)

    # Set a default image and/or allow for pulling from container registry
    image: Optional[VmImage | ContainerImage] = Field(description='Image to use for the machine', default=None)

    dhcp: bool = Field(description='Leave True to use DHCP. If a static is desired, set this to False and set ipv4_manual, gateway, and dns_servers.', default=True)
    mac_address: Optional[str] = Field(description='Hardware MAC address', default=None, pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    ipv4_manual: Optional[IPvAnyAddress] = Field(description='Static IP address', default=None)
    gateway: Optional[IPvAnyAddress] = Field(description='Default gateway', default=None)
    dns_servers: list[IPvAnyAddress] = Field(default_factory=list)


# Remove later
if __name__ == '__main__':
    test_image = VmImage(
        name = 'sdr_img',
        description = 'Siemens Digital Radiography',
        version = 13.37,
        type = 'qcow2',
    )
    test_device = Device(
        name = 'tester01',
        description = 'Test device information',
        cpus = 4,
        image = test_image,
    )
    with open('data.yaml', 'w') as f:
        yaml.dump(test_device.model_dump(), f)

