import asyncio
import os
from typing import Annotated
import uvicorn
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from carthage import AsyncInjector, inject, InjectionKey, CarthagePlugin, base_injector
from carthage.modeling import CarthageLayout
from carthage.deployment import DeploymentIntrospection, DeploymentResult
from carthage.dependency_injection import instantiation_roots
from .models import *

def get_ainjector(request:Request)->AsyncInjector:
    return request.app.state.layout.ainjector

def get_layout(request:Request)-> CarthageLayout:
    return request.app.state.layout

def get_model_store(request:Request)->ModelStore:
    return request.app.state.model_store

def running_deployment()-> DeploymentResult | None:
    for r in instantiation_roots:
        if isinstance(r, DeploymentIntrospection):
            return r.result
    return None


ainjector_dependency = Annotated[AsyncInjector, Depends(get_ainjector)]

layout_dependency = Annotated[CarthageLayout, Depends(get_layout)]

model_store_dependency = Annotated[ModelStore, Depends(get_model_store)]
                                   
async def regenerate_layout(request:Request):
    '''
    Backgrount task to update the layout after mutations to the ModelStore.
    Scheduled as  asyncio.ensure_future(regenerate_layout()
    Only allows one regeneration to be pending at a time.
    '''
    state = request.app.state
    base_injector = request.app.state.base_injector
    if state.regeneration_task:
        return
    state.regeneration_task = asyncio.current_task()
    async with state.deployment_lock:
        state.regeneration_task = None
        from .layout import build_layout
        base_injector.replace_provider(InjectionKey(CarthageLayout), build_layout)
        ainjector = AsyncInjector(base_injector)
        state.layout = await ainjector.get_instance_async(CarthageLayout)

    


api_v1 = APIRouter(prefix="/api/v1")

@api_v1.get("/devices")
async def get_devices(model_store:model_store_dependency)-> list[Device]:
    return list(model_store.devices.values())

@api_v1.post('/devices')
async def create_device(device:Device, request:Request, model_store:model_store_dependency):
    model_store.devices[device.id] = device
    model_store.save()
    asyncio.ensure_future(regenerate_layout(request))

@api_v1.put('/devices/{device_id}')
async def update_device(device_id:str, device:Device, request:Request, model_store:model_store_dependency):
    if not device_id in model_store.devices:
        raise HTTPException(status_code=404, detail="Device not found")

    model_store.devices[device_id] = device
    model_store.save()
    asyncio.ensure_future(regenerate_layout(request))

@api_v1.delete('/devices/{device_id}')
async def delete_device(device_id:str, request:Request, model_store:model_store_dependency):
    if not device_id in model_store.devices:
        raise HTTPException(status_code=404, detail="Device not found")

    model_store.devices.pop(device_id)
    model_store.save()
    asyncio.ensure_future(regenerate_layout(request))

@inject(
    layout=InjectionKey(CarthageLayout, _ready=False),
    plugin=InjectionKey(CarthagePlugin, name='viper-whs'))
async def start_web_server(layout, plugin):
    app = FastAPI()
    app.state.layout = layout
    #: This lock should be held while calling run_deploy or run_deployment_destroy or regenerating the layout. In general  frontend should return 409 rather than blocking on this lock. The only thing that should block on this lock is a background replace of the layout.
    app.state.deployment_lock = asyncio.Lock()
    #: The task of a layout regeneration that has not yet started. If
    #a model change is made and this is non-None, no regeneration
    #needs to be queued. This should be cleared in the regeneration
    #task after the lock is obtained but before the ModelStore is read
    #by the new layout so that future changes will force a new
    #regeneration.
    app.state.regeneration_task = None
    app.state.base_injector = base_injector
    app.state.model_store = base_injector.get_instance(ModelStore)
    app.include_router(api_v1)
    if (plugin.resource_dir/'../dist').exists():
        app.mount('/', StaticFiles(directory=plugin.resource_dir/'../dist', html=True), name='frontend')
    config = uvicorn.Config(app,
                             port=int(os.environ.get('PORT', 8080)),
                             host='0.0.0.0',
                            )
    server = uvicorn.Server(config)
    asyncio.get_event_loop().create_task(server.serve())

web_server_key = InjectionKey('viper_whs.webserver')
