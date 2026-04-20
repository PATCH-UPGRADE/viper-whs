from pathlib import Path
from carthage import inject, Injector, ConfigLayout, InjectionKey
from . import layout
from .models import ModelStore

@inject(injector=Injector)
def build_model_store(injector: Injector):
    config = injector(ConfigLayout)
    state_dir = Path(config.state_dir)
    return ModelStore(model_dir=state_dir/"model_store")

@inject(injector=Injector)
def carthage_plugin(injector):
    injector.add_provider(layout.layout)
    injector.add_provider(InjectionKey(ModelStore), build_model_store)
