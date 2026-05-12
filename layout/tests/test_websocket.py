import os
import socket

from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse

from python import web_backend


class FakeDomain:
    def __init__(self, backend_socket: socket.socket):
        self.backend_socket = backend_socket
        self.calls: list[tuple[int, int]] = []

    def openGraphicsFD(self, idx: int, flags: int = 0) -> int:
        self.calls.append((idx, flags))
        return os.dup(self.backend_socket.fileno())


class FakeLibvirtConnection:
    def __init__(self, domain: FakeDomain):
        self.domain = domain
        self.lookups: list[str] = []

    def lookupByName(self, name: str) -> FakeDomain:
        self.lookups.append(name)
        return self.domain


def test_vnc_websocket_proxies_bytes_for_seeded_device(app):
    backend_socket, peer_socket = socket.socketpair()
    backend_socket.settimeout(1.0)
    peer_socket.settimeout(1.0)
    fake_domain = FakeDomain(backend_socket)
    fake_conn = FakeLibvirtConnection(fake_domain)
    app.dependency_overrides[web_backend.get_libvirt_connection] = lambda: fake_conn
    client = TestClient(app)

    try:
        with client.websocket_connect("/api/v1/vnc_websocket/tester01", subprotocols=["binary"]) as websocket:
            websocket.send_bytes(b"client-to-vnc")
            assert peer_socket.recv(1024) == b"client-to-vnc"

            peer_socket.sendall(b"vnc-to-client")
            assert websocket.receive_bytes() == b"vnc-to-client"

        assert fake_conn.lookups == ["whs-tester01"]
        assert fake_domain.calls == [(0, web_backend.libvirt.VIR_DOMAIN_OPEN_GRAPHICS_SKIPAUTH)]
    finally:
        app.dependency_overrides.clear()
        backend_socket.close()
        peer_socket.close()


def test_vnc_websocket_missing_device_fails_handshake(app):
    client = TestClient(app)

    try:
        with client.websocket_connect("/api/v1/vnc_websocket/does-not-exist", subprotocols=["binary"]):
            raise AssertionError("websocket handshake unexpectedly succeeded")
    except WebSocketDenialResponse as exc:
        assert exc.status_code == 404
        assert exc.content == b'{"detail":"Device not found"}'
