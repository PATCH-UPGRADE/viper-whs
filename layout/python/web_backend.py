import asyncio
import os
from typing import Annotated
import uvicorn
from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from carthage import AsyncInjector, inject, InjectionKey, CarthagePlugin
from carthage.modeling import CarthageLayout

def get_ainjector(request:Request)->AsyncInjector:
    return request.app.state.ainjector

ainjector_dependency = Annotated[AsyncInjector, Depends(get_ainjector)]


api_v1 = APIRouter(prefix="/api/v1")

@api_v1.get("/devices")
async def get_devices(ainjector:ainjector_dependency):
    raise NotImplementedError

@inject(
    layout=InjectionKey(CarthageLayout, _ready=False),
    plugin=InjectionKey(CarthagePlugin, name='viper-whs'))
async def start_web_server(layout, plugin):
    app = FastAPI()
    app.state.ainjector = layout.ainjector
    app.include_router(api_v1)
    if (plugin.resource_dir/'../dist').exists():
        breakpoint()
        app.mount('/', StaticFiles(directory=plugin.resource_dir/'../dist', html=True), name='frontend')
    config = uvicorn.Config(app,
                             port=int(os.environ.get('PORT', 8080)),
                             host='0.0.0.0',
                            )
    server = uvicorn.Server(config)
    asyncio.get_event_loop().create_task(server.serve())

web_server_key = InjectionKey('viper_whs.webserver')
