from carthage import *
from carthage import libvirt
from carthage.debian import debian_container_to_vm
from carthage.modeling import *
from carthage_base import DebianImage

@provides(InjectionKey(ModelGroup, role='images'))
class Images(ModelGroup):
    @globally_unique_key(InjectionKey('whs_base_debian'))
    class WHSDebianImage(DebianImage):
        guest_agent = customization_task(libvirt.InstallQemuAgent)

    @inject(ainjector=AsyncInjector, image=WHSDebianImage)
    async def whs_base_debian_image(ainjector, image):
        return await ainjector(
            debian_container_to_vm,
            image, f'whs_base_debian.raw',
            '30G',
            classes = '+SERIAL,CLOUD_INIT,GROW,OPENROOT'
        )
    
    add_provider(InjectionKey('whs_base_debian', _globally_unique=True), whs_base_debian_image, propagate = True)
