import asyncio
import sys
import types

from mgc.config import ClientConfig
from mgc.region import Region

fake_compute_module = types.ModuleType("mgc.resources.compute.compute")


class ImportedCompute:
    def __init__(self, transport):
        self.transport = transport


fake_compute_module.Compute = ImportedCompute
sys.modules["mgc.resources.compute.compute"] = fake_compute_module

from mgc import client as client_module  # noqa: E402
from mgc.client import ApiKeyAuth, Client  # noqa: E402


def run(coro):
    return asyncio.run(coro)


def test_api_key_auth_returns_api_key_header():
    auth = ApiKeyAuth("secret-key")

    headers = auth.get_access_token()

    assert headers == {"x-api-key": "secret-key"}


def test_client_uses_default_config_and_exposes_compute(monkeypatch):
    created = {}

    class FakeTransport:
        def __init__(self, *, auth, config):
            created["auth"] = auth
            created["config"] = config
            self.closed = False

        async def close(self):
            self.closed = True

    class FakeCompute:
        def __init__(self, transport):
            self.transport = transport

    monkeypatch.setattr(client_module, "Transport", FakeTransport)
    monkeypatch.setattr(client_module, "Compute", FakeCompute)

    client = Client(api_key="secret-key")

    assert isinstance(created["config"], ClientConfig)
    assert created["config"].region == Region.BR_SE1
    assert created["auth"].get_access_token() == {"x-api-key": "secret-key"}
    assert isinstance(client.compute, FakeCompute)
    assert client.compute.transport is client._transport


def test_client_exposes_block_storage_without_replacing_compute_snapshots(monkeypatch):
    compute_snapshots = object()

    class FakeTransport:
        def __init__(self, *, auth, config):
            pass

    class FakeCompute:
        def __init__(self, transport):
            self.transport = transport
            self.snapshots = compute_snapshots

    class FakeBlockStorage:
        def __init__(self, transport):
            self.transport = transport

    monkeypatch.setattr(client_module, "Transport", FakeTransport)
    monkeypatch.setattr(client_module, "Compute", FakeCompute)
    monkeypatch.setattr(client_module, "BlockStorage", FakeBlockStorage)

    client = Client(api_key="secret-key")

    assert isinstance(client.block_storage, FakeBlockStorage)
    assert client.block_storage.transport is client._transport
    assert client.compute.snapshots is compute_snapshots


def test_client_uses_custom_config(monkeypatch):
    created = {}
    config = ClientConfig(region=Region.BR_NE1, timeout=5.0)

    class FakeTransport:
        def __init__(self, *, auth, config):
            created["config"] = config

    class FakeCompute:
        def __init__(self, transport):
            self.transport = transport

    monkeypatch.setattr(client_module, "Transport", FakeTransport)
    monkeypatch.setattr(client_module, "Compute", FakeCompute)

    Client(api_key="secret-key", config=config)

    assert created["config"] is config


def test_client_close_delegates_to_transport(monkeypatch):
    class FakeTransport:
        def __init__(self, *, auth, config):
            self.closed = False

        async def close(self):
            self.closed = True

    class FakeCompute:
        def __init__(self, transport):
            self.transport = transport

    monkeypatch.setattr(client_module, "Transport", FakeTransport)
    monkeypatch.setattr(client_module, "Compute", FakeCompute)
    client = Client(api_key="secret-key")

    run(client.close())

    assert client._transport.closed is True


def test_client_async_context_manager_closes_transport(monkeypatch):
    class FakeTransport:
        def __init__(self, *, auth, config):
            self.closed = False

        async def close(self):
            self.closed = True

    class FakeCompute:
        def __init__(self, transport):
            self.transport = transport

    monkeypatch.setattr(client_module, "Transport", FakeTransport)
    monkeypatch.setattr(client_module, "Compute", FakeCompute)

    async def use_client():
        async with Client(api_key="secret-key") as client:
            assert isinstance(client, Client)
            return client

    client = run(use_client())

    assert client._transport.closed is True
