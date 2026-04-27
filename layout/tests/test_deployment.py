import asyncio

from carthage.pytest import async_test
from httpx import ASGITransport, AsyncClient


async def wait_for_completed_deployment(client: AsyncClient, timeout: float = 120.0):
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    last_body = None
    while True:
        response = await client.get("/api/v1/deployment-status")
        assert response.status_code == 200
        body = response.json()
        if body is not None:
            last_body = body
            if not body["running"]:
                return body
        if loop.time() >= deadline:
            raise AssertionError(f"deployment did not complete before timeout; last status: {last_body!r}")
        await asyncio.sleep(0.25)


@async_test
async def test_deployment_status_starts_empty(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/deployment-status")

    assert response.status_code == 200
    assert response.json() is None


@async_test
async def test_deploy_endpoint_wires_through(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/deploy")
        assert response.status_code == 200

        status = await wait_for_completed_deployment(client)

    assert status["running"] is False
    assert status["failures"] == []
    assert status["dependency_failures"] == []
    assert status["successes"]
