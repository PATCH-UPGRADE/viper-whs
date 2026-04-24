import asyncio
from carthage import *
from carthage import podman, libvirt
from carthage.libvirt.images import guestfs_container_to_vm, DebianBaseContainer
from carthage.modeling import *


class WhsBaseImage(DebianBaseContainer, podman.PodmanImageModel):
    '''Podman image for use as a basis for libvirt VMs'''
    add_provider(podman.podman_container_host, podman.LocalPodmanContainerHost)
    override_dependencies = True # Is this needed? 
    from carthage.libvirt.images import NoRootCustomization, CloudInitCustomization, SerialCustomization

    oci_image_tag = 'localhost/whs-base-image'
    base_image = 'debian:trixie'
    oci_image_command = ['/sbin/init']

    class install_prereqs(FilesystemCustomization):
        @setup_task('Create netdev group')
        async def create_netdev_group(self):
            await self.run_command('groupadd', '--system', 'netdev')

        @setup_task('apt update')
        async def apt_update(self):
            await self.run_command('apt-get', 'update')

        @setup_task('Install packages')
        async def install_packages(self):
            await self.run_command('apt-get', '-y', 'install', 'openssh-server', 'systemd-resolved', 'systemd-sysv', 'udev', 'iputils-ping')
        
        guest_agent = customization_task(libvirt.InstallQemuAgent)

vm_image_build_lock = asyncio.Lock()

@provides(libvirt.vm_image_key)
@inject(ainjector = AsyncInjector, image=WhsBaseImage)
async def whs_vm_image(ainjector, image):
    async with vm_image_build_lock:
        return await ainjector(
            guestfs_container_to_vm,
            image, f"whs_vm_image.raw",
            20*1024,
        )
