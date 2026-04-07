# Copyright (C) 2026, Hadron Industries.
# Carthage is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation. It is distributed
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the file
# LICENSE for details.


from carthage import *
import carthage.libvirt
from carthage.modeling import *
from carthage.podman import *
from carthage.oci import *
from carthage.network import V4Config
from carthage_base import *
from .images import WhsBaseImage, whs_vm_image


class layout(CarthageLayout):
    layout_name = 'viper-whs'
    domain = 'whs.local'
    from .images import WhsBaseImage, whs_vm_image

    @provides('bridge_net')
    class net(NetworkModel):
        bridge_name = 'whs-lab'
        v4_config=V4Config(dhcp=True)
    
    class net_config(NetworkConfigModel):
        add('eth0', mac=persistent_random_mac, net=injector_access('bridge_net'))

    class linux_vm(MachineModel):
        name = 'vm01'
        cpus = 2
        memory_mb = 1024 * 8
        console_needed = True
        add_provider(machine_implementation_key, dependency_quote(carthage.libvirt.Vm))
        add_provider(carthage.libvirt.vm_image_key, whs_vm_image)
