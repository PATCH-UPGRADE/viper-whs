<<<<<<< HEAD

from carthage import inject, Injector
||||||| e92a32c
# Copyright (C) 2026, Hadron Industries.
# Carthage is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation. It is distributed
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the file
# LICENSE for details.

from carthage import inject, Injector
=======
from pathlib import Path
from carthage import inject, Injector, ConfigLayout, InjectionKey
>>>>>>> modelstore
from . import layout
<<<<<<< HEAD
from .web_backend import start_web_server, web_server_key
||||||| e92a32c
=======
from .models import ModelStore
from .web_backend import start_web_server, web_server_key

@inject(injector=Injector)
def build_model_store(injector: Injector):
    config = injector(ConfigLayout)
    state_dir = Path(config.state_dir)
    return ModelStore(model_dir=state_dir/"model_store")
>>>>>>> modelstore

@inject(injector=Injector)
def carthage_plugin(injector):
    injector.add_provider(layout.layout)
    injector.add_provider(InjectionKey(ModelStore), build_model_store)
    injector.add_provider(web_server_key, start_web_server)
