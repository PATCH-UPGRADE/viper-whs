from pathlib import Path

from fastapi.testclient import TestClient

from python.models import Device


def test_model_store_is_seeded(model_store):
    assert "tester01" in model_store.devices
    assert "sdr_img" in model_store.vm_images


def test_app_reads_seeded_devices(app, model_store, state_dir: Path):
    client = TestClient(app)

    response = client.get("/api/v1/devices")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == "tester01"
    assert (state_dir / "model_store" / "devices.yml").exists()


def test_model_store_saves_into_temp_state_dir(model_store, state_dir: Path):
    device = Device(
        id="tester02",
        name="tester02",
        description="Second test device",
    )
    model_store.devices[device.id] = device
    model_store.save()

    saved = (state_dir / "model_store" / "devices.yml").read_text()
    assert "tester02" in saved
