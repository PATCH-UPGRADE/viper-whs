from __future__ import annotations

import asyncio
import importlib
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import FastAPI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

LAYOUT_ROOT = PROJECT_ROOT / "layout"
if str(LAYOUT_ROOT) not in sys.path:
    sys.path.insert(0, str(LAYOUT_ROOT))

CARTHAGE_BASE_ROOT = Path(__file__).resolve().parents[4] / "carthage-base"
if CARTHAGE_BASE_ROOT.exists() and str(CARTHAGE_BASE_ROOT) not in sys.path:
    sys.path.insert(0, str(CARTHAGE_BASE_ROOT))

import carthage_base  # noqa: F401
from carthage import AsyncInjector, ConfigLayout, base_injector, shutdown_injector
from carthage.dependency_injection import InjectionKey, dependency_quote
from carthage.modeling import CarthageLayout
from carthage.plugins import CarthagePlugin
from python import layout as layout_module
from python.models import ModelStore
import python.web_backend as web_backend
from python.web_backend import web_app_key, web_server_key

sys.modules.setdefault("layout.layout", layout_module)
sys.modules.setdefault("layout.models", importlib.import_module("python.models"))
sys.modules.setdefault("layout.web_backend", web_backend)
from layout.carthage_plugin import carthage_plugin

base_injector(carthage_plugin)

@pytest.fixture(scope="session")
def loop():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    base_injector.add_provider(InjectionKey(asyncio.AbstractEventLoop), event_loop)
    yield event_loop
    event_loop.close()


@pytest.fixture(scope="session")
def modelstore_defaults_dir() -> Path:
    return Path(__file__).parent / "resources" / "modelstore"


@pytest.fixture
def state_dir(tmp_path: Path, modelstore_defaults_dir: Path) -> Path:
    state_dir = tmp_path / "state"
    model_store_dir = state_dir / "model_store"
    shutil.copytree(modelstore_defaults_dir, model_store_dir, dirs_exist_ok=True)
    return state_dir


@pytest.fixture
def injector(state_dir: Path):
    injector = base_injector.claim()
    config = injector(ConfigLayout)
    config.base_dir = str(state_dir.parent)
    config.state_dir = str(state_dir)
    config.cache_dir = str(state_dir / "cache")
    config.log_dir = str(state_dir / "log")
    config.vm_image_dir = str(state_dir / "vm")
    config.local_run_dir = str(state_dir)
    config.delete_volumes = True
    config.persist_local_networking = False

    model_store = ModelStore(model_dir=state_dir / "model_store").load()
    plugin_root = state_dir / "plugin"
    plugin_root.mkdir(parents=True, exist_ok=True)
    plugin = SimpleNamespace(resource_dir=plugin_root)
    base_injector.add_provider(InjectionKey(CarthagePlugin, name="viper-whs"), plugin, replace=True)
    injector.add_provider(InjectionKey(CarthageLayout), layout_module.build_layout)
    injector.add_provider(InjectionKey(ModelStore), model_store)
    injector.add_provider(InjectionKey(CarthagePlugin, name="viper-whs"), plugin)
    injector.add_provider(web_app_key, web_backend.build_web_app, replace=True)
    injector.add_provider(web_server_key, dependency_quote(None))
    return injector


@pytest.fixture
def ainjector(injector, loop):
    ainjector = injector(AsyncInjector)
    yield ainjector
    loop.run_until_complete(shutdown_injector(ainjector))


@pytest.fixture
def model_store(injector) -> ModelStore:
    return injector.get_instance(InjectionKey(ModelStore))


@pytest.fixture
def layout(ainjector, loop):
    return loop.run_until_complete(ainjector.get_instance_async(CarthageLayout))


@pytest.fixture
def app(ainjector, state_dir, loop):
    dist_root = state_dir / "dist"
    dist_root.mkdir(parents=True, exist_ok=True)
    app = asyncio.get_event_loop().run_until_complete(ainjector.get_instance_async(web_app_key))
    assert isinstance(app, FastAPI)
    yield app

    pending = [task for task in asyncio.all_tasks(loop) if not task.done()]
    for task in pending:
        task.cancel()
    if pending:
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
