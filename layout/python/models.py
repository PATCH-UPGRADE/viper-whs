from typing import Literal, Optional, TypeVar
from pydantic import BaseModel, Field, ConfigDict, IPvAnyAddress
from pathlib import Path
import yaml
from uuid import uuid4

default_model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        validate_assignment=True,
    )

ModelType = TypeVar('ModelType', bound=BaseModel)

class VmImage(BaseModel):
    model_config = default_model_config
    id: str = Field(default_factory=lambda: uuid4().hex)

    name: str = Field(description='Name of the image', min_length=1, max_length=64)
    description: str = Field(description='Description or tags', default='')
    version: float = Field(default=1.00)
    type: Literal['qcow2', 'raw'] = Field(description='Type of image being used, qcow2 or raw', default='raw')

class ContainerImage(BaseModel):
    model_config = default_model_config
    id: str = Field(default_factory=lambda: uuid4().hex)

    name: str = Field(description='Name of the image', min_length=1, max_length=64)
    description: str = Field(description='Description or tags', default='')
    version: float = Field(default=1.00)

class Device(BaseModel):
    model_config = default_model_config
    id: str = Field(default_factory=lambda: uuid4().hex)

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
    image_name: Optional[str] = Field(description='Image to use for the machine', default=None)

    dhcp: bool = Field(description='Leave True to use DHCP. If a static is desired, set this to False and set ipv4_manual, gateway, and dns_servers.', default=True)
    mac_address: Optional[str] = Field(description='Hardware MAC address', default=None, pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    ipv4_manual: Optional[IPvAnyAddress] = Field(description='Static IP address', default=None)
    gateway: Optional[IPvAnyAddress] = Field(description='Default gateway', default=None)
    dns_servers: list[IPvAnyAddress] = Field(default_factory=list)

class ModelStore(BaseModel):
    model_config = default_model_config

    vm_images: list[VmImage] = Field(default_factory=list)
    container_images: list[ContainerImage] = Field(default_factory=list)
    devices: list[Device] = Field(default_factory=list)
    model_dir: Path = Field(default=Path(__file__).with_name('models'))

    def _load_model_file(self, path: Path, model_class: type[ModelType]) -> list[ModelType]:
        if not path.exists():
            return []

        with path.open('r', encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)

        if raw_data is None:
            return []
        if not isinstance(raw_data, list):
            raise ValueError(f'Expected a list of records in {path}')

        return [model_class.model_validate(item) for item in raw_data]

    def _save_model_file(self, path: Path, records: list[ModelType]) -> None:
        with path.open('w', encoding='utf-8') as f:
            yaml.safe_dump(
                [record.model_dump(mode='json') for record in records],
                f,
                sort_keys=False,
                default_flow_style=False,
            )

    def load(self) -> 'ModelStore':
        '''Loads models from yaml'''
        self.vm_images = self._load_model_file(self.model_dir / 'vm_images.yml', VmImage)
        self.container_images = self._load_model_file(self.model_dir / 'container_images.yml', ContainerImage)
        self.devices = self._load_model_file(self.model_dir / 'devices.yml', Device)
        return self

    def save(self) -> 'ModelStore':
        '''Saves all models off to yaml'''
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self._save_model_file(self.model_dir / 'vm_images.yml', self.vm_images)
        self._save_model_file(self.model_dir / 'container_images.yml', self.container_images)
        self._save_model_file(self.model_dir / 'devices.yml', self.devices)
        self.validate_references()
        return self
    
    def get_device_image(self, device: Device) -> Optional[VmImage | ContainerImage]:
        '''Helper to get the actual image for a specific device.'''
        if not device.image_name:
            return None
        for img in self.vm_images + self.container_images:
            if img.name == device.image_name:
                return img
        return None
    
    def validate_references(self):
        '''Ensures any referenced images actually exist'''
        for device in self.devices:
            if device.image_name and not self.get_device_image(device):
                raise ValueError(f"Device {device.name} references a missing image: {device.image_name}")



# For testing purposes
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
        image_name = 'sdr_img',
    )
    test_store = ModelStore(
        vm_images = [test_image],
        devices = [test_device],
    )
    test_store.save()
    loaded_store = ModelStore().load()
    print(loaded_store.model_dump())
