import asyncio

import pytest

from mgc.resources.block_storage.snapshots import Snapshots


def run(coro):
    return asyncio.run(coro)


def test_list_uses_default_pagination(fake_transport):
    resource = Snapshots(fake_transport)

    result = run(resource.list())

    assert result == {
        "method": "get",
        "path": "block-storage/v1/snapshots",
        "kwargs": {"params": {"_limit": 50, "_offset": 0}},
    }
    assert fake_transport.calls == [result]


def test_list_includes_optional_sort_expand_and_name(fake_transport):
    resource = Snapshots(fake_transport)

    run(
        resource.list(
            limit=10,
            offset=20,
            sort="created_at:desc",
            expand=["volume"],
            name="snapshot-name",
        )
    )

    assert fake_transport.calls == [
        {
            "method": "get",
            "path": "block-storage/v1/snapshots",
            "kwargs": {
                "params": {
                    "_limit": 10,
                    "_offset": 20,
                    "_sort": "created_at:desc",
                    "expand": ["volume"],
                    "name": "snapshot-name",
                }
            },
        }
    ]


def test_create_with_volume_id(fake_transport):
    resource = Snapshots(fake_transport)

    run(
        resource.create(
            name="snapshot-name",
            description="description",
            volume_id="vol-1",
        )
    )

    assert fake_transport.calls == [
        {
            "method": "post",
            "path": "block-storage/v1/snapshots",
            "kwargs": {
                "json": {
                    "name": "snapshot-name",
                    "description": "description",
                    "volume": {"id": "vol-1"},
                }
            },
        }
    ]


def test_create_with_volume_name(fake_transport):
    resource = Snapshots(fake_transport)

    run(
        resource.create(
            name="snapshot-name",
            description="description",
            volume_name="volume-name",
        )
    )

    assert fake_transport.calls[0]["kwargs"]["json"] == {
        "name": "snapshot-name",
        "description": "description",
        "volume": {"name": "volume-name"},
    }


def test_create_prefers_volume_id_over_volume_name(fake_transport):
    resource = Snapshots(fake_transport)

    run(
        resource.create(
            name="snapshot-name",
            description="description",
            volume_id="vol-1",
            volume_name="volume-name",
        )
    )

    assert fake_transport.calls[0]["kwargs"]["json"]["volume"] == {"id": "vol-1"}


def test_create_requires_volume(fake_transport):
    resource = Snapshots(fake_transport)

    with pytest.raises(ValueError, match="volume_id or volume_name is required"):
        run(resource.create(name="snapshot-name", description="description"))

    assert fake_transport.calls == []


@pytest.mark.parametrize(
    ("expand", "expected_params"),
    [
        (None, {}),
        (["volume"], {"expand": ["volume"]}),
    ],
)
def test_get_builds_params(fake_transport, expand, expected_params):
    resource = Snapshots(fake_transport)

    result = run(resource.get(snapshot_id="snap-1", expand=expand))

    assert result == {
        "method": "get",
        "path": "block-storage/v1/snapshots/snap-1",
        "kwargs": {"params": expected_params},
    }
    assert fake_transport.calls == [result]


def test_delete_deletes_snapshot(fake_transport):
    resource = Snapshots(fake_transport)

    assert run(resource.delete(snapshot_id="snap-1")) is None
    assert fake_transport.calls == [
        {"method": "delete", "path": "block-storage/v1/snapshots/snap-1", "kwargs": {}},
    ]


def test_rename_renames_snapshot(fake_transport):
    resource = Snapshots(fake_transport)

    run(resource.rename(snapshot_id="snap-1", name="new-name"))

    assert fake_transport.calls == [
        {
            "method": "patch",
            "path": "block-storage/v1/snapshots/snap-1/rename",
            "kwargs": {"json": {"name": "new-name"}},
        }
    ]
