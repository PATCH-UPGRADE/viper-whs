# Copyright (C) 2026, Hadron Industries.
# Carthage is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation. It is distributed
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the file
# LICENSE for details.


from carthage import *
from carthage.modeling import *
from carthage.ansible import *
from carthage.network import V4Config

class layout(CarthageLayout):
    layout_name = 'viper-whs'
    