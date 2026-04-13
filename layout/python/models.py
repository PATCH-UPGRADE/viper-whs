from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, IPvAnyAddress
import yaml

default_model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        validate_assignment=True,
    )

class Image(BaseModel):
    model_config = default_model_config

    name: str = Field(description='Name of the image', min_length=3, max_length=20)
    description: str = Field(description='Description or tags', default='')
    version: float = Field(default=1.00)
    type: Literal['qcow2', 'raw', 'container'] = Field(description='Type of image being used, qcow2, raw, or container', default='container')
    read_only: bool = Field(description='Set the image to read only', default=False)


class Device(BaseModel):
    model_config = default_model_config

    name: str = Field(description='Name of the device', min_length=3, max_length=20)
    description: str = Field(description='Description or tags', default='')
    type: Literal['qcow2', 'raw', 'container'] = Field(description='Type of image being used, qcow2, raw, or container', default='container')

    architecture: Literal['x86_64', 'arm_aarch64'] = Field(description='Architecture of the device, x86_64 or arm_aarch64', default='x86_64')
    cpus: int = Field(description='Number of CPUs assigned', default=2)
    memory: int = Field(description='System memory (in MB) assigned', default=4096)
    disk: int = Field(description='Disk size (in GB)', default=20)
    disk_controller: str = Field(description='Controller used for disk', default='virtio')
    display: bool = Field(description='Display needed', default=False)

    # Set a default image and/or allow for pulling from container registry
    image: Optional[Image] = Field(description='Image to use for the machine', default=None)

    dhcp: bool = Field(default=True)
    mac_address: Optional[str] = Field(description='Hardware MAC address', default=None, pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    ipv4_manual: Optional[IPvAnyAddress] = Field(description='Static IP address', default=None)
    gateway: Optional[IPvAnyAddress] = Field(description='Default gateway', default=None)
    dns_servers: list[IPvAnyAddress] = Field(default_factory=list)


# Remove later
if __name__ == '__main__':
    test_image = Image(
        name = 'sdr_img',
        description = 'Siemens Digital Radiography',
        version = 13.37,
        type = 'container',
    )
    test_device = Device(
        name = 'tester01',
        description = 'Test device information',
        cpus = 4,
        image = test_image,
    )
    with open('data.yaml', 'w') as f:
        yaml.dump(test_device.model_dump(), f)

