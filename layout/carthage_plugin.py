
from carthage import inject, Injector
from . import layout
from .web_backend import start_web_server, web_server_key

@inject(injector=Injector)
def carthage_plugin(injector):
    injector.add_provider(layout.layout)
    injector.add_provider(web_server_key, start_web_server)
    
