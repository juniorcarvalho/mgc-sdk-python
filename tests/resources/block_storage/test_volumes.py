import asyncio

import pytest

from mgc.exceptions import InvalidVolumeTypeNameError
from mgc.resources.block_storage.volumes import Volumes


def run(coro):
    return asyncio.run(coro)


def test_list_uses_default_pagination(fake_transport):
    resource = Volumes(fake_transport)

    result = run(resource.list())

    assert result == {
        "method": "get",
        "path": "block-storage/v1/volumes",
        "kwargs": {"params": {"_limit": 50, "_offset": 0}},
    }
    assert fake_transport.calls == [result]


def test_list_includes_optional_sort_expand_and_name(fake_transport):
    resource = Volumes(fake_transport)

    run(
        resource.list(
            limit=10,
            offset=20,
            sort="created_at:desc",
            expand=["volume_type", "attachment"],
            name="volume-name",
        )
    )

    assert fake_transport.calls == [
        {
            "method": "get",
            "path": "block-storage/v1/volumes",
            "kwargs": {
                "params": {
                    "_limit": 10,
                    "_offset": 20,
                    "_sort": "created_at:desc",
                    "expand": ["volume_type", "attachment"],
                    "name": "volume-name",
                }
            },
        }
    ]


def test_create_with_minimal_payload(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.create(name="volume-name", size=10, type_id="type-1"))

    assert fake_transport.calls == [
        {
            "method": "post",
            "path": "block-storage/v1/volumes",
            "kwargs": {
                "json": {
                    "name": "volume-name",
                    "size": 10,
                    "type": {"id": "type-1"},
                }
            },
        }
    ]


def test_create_with_type_name(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.create(name="volume-name", size=10, type_name="cloud_nvme1k"))

    assert fake_transport.calls[0]["kwargs"]["json"] == {
        "name": "volume-name",
        "size": 10,
        "type": {"name": "cloud_nvme1k"},
    }


def test_create_rejects_invalid_volume_type_name(fake_transport):
    resource = Volumes(fake_transport)

    with pytest.raises(InvalidVolumeTypeNameError, match="Invalid volume type name"):
        run(resource.create(name="volume-name", size=10, type_name="regional-volume-type"))

    assert fake_transport.calls == []


def test_create_requires_type(fake_transport):
    resource = Volumes(fake_transport)

    with pytest.raises(ValueError, match="type_id or type_name is required"):
        run(resource.create(name="volume-name", size=10))

    assert fake_transport.calls == []


def test_create_includes_optional_id_payload_fields(fake_transport):
    resource = Volumes(fake_transport)

    run(
        resource.create(
            name="volume-name",
            size=10,
            type_id="type-1",
            backup_id="backup-1",
            snapshot_id="snapshot-1",
            availability_zone="br-se1-a",
        )
    )

    assert fake_transport.calls[0]["kwargs"]["json"] == {
        "name": "volume-name",
        "size": 10,
        "type": {"id": "type-1"},
        "backup": {"id": "backup-1"},
        "snapshot": {"id": "snapshot-1"},
        "availability_zone": "br-se1-a",
    }


def test_create_includes_optional_name_payload_fields(fake_transport):
    resource = Volumes(fake_transport)

    run(
        resource.create(
            name="volume-name",
            size=10,
            type_id="type-1",
            backup_name="backup-name",
            snapshot_name="snapshot-name",
        )
    )

    assert fake_transport.calls[0]["kwargs"]["json"] == {
        "name": "volume-name",
        "size": 10,
        "type": {"id": "type-1"},
        "backup": {"name": "backup-name"},
        "snapshot": {"name": "snapshot-name"},
    }


@pytest.mark.parametrize(
    ("expand", "expected_params"),
    [
        (None, {}),
        (["volume_type"], {"expand": ["volume_type"]}),
    ],
)
def test_get_builds_params(fake_transport, expand, expected_params):
    resource = Volumes(fake_transport)

    result = run(resource.get(volume_id="vol-1", expand=expand))

    assert result == {
        "method": "get",
        "path": "block-storage/v1/volumes/vol-1",
        "kwargs": {"params": expected_params},
    }
    assert fake_transport.calls == [result]


def test_delete_deletes_volume(fake_transport):
    resource = Volumes(fake_transport)

    assert run(resource.delete(volume_id="vol-1")) is None
    assert fake_transport.calls == [
        {"method": "delete", "path": "block-storage/v1/volumes/vol-1", "kwargs": {}},
    ]


def test_attach_attaches_volume(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.attach(volume_id="vol-1", virtual_machine_id="vm-1"))

    assert fake_transport.calls == [
        {"method": "post", "path": "block-storage/v1/volumes/vol-1/attach/vm-1", "kwargs": {}},
    ]


def test_detach_detaches_volume(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.detach(volume_id="vol-1"))

    assert fake_transport.calls == [
        {"method": "post", "path": "block-storage/v1/volumes/vol-1/detach", "kwargs": {}},
    ]


def test_extend_extends_volume(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.extend(volume_id="vol-1", size=20))

    assert fake_transport.calls == [
        {
            "method": "post",
            "path": "block-storage/v1/volumes/vol-1/extend",
            "kwargs": {"json": {"size": 20}},
        }
    ]


def test_rename_renames_volume(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.rename(volume_id="vol-1", name="new-name"))

    assert fake_transport.calls == [
        {
            "method": "patch",
            "path": "block-storage/v1/volumes/vol-1/rename",
            "kwargs": {"json": {"name": "new-name"}},
        }
    ]


def test_retype_retypes_volume_with_type_id(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.retype(volume_id="vol-1", type_id="type-1"))

    assert fake_transport.calls == [
        {
            "method": "post",
            "path": "block-storage/v1/volumes/vol-1/retype",
            "kwargs": {"json": {"new_type": {"id": "type-1"}}},
        }
    ]


def test_retype_retypes_volume_with_type_name(fake_transport):
    resource = Volumes(fake_transport)

    run(resource.retype(volume_id="vol-1", type_name="cloud_nvme20k"))

    assert fake_transport.calls == [
        {
            "method": "post",
            "path": "block-storage/v1/volumes/vol-1/retype",
            "kwargs": {"json": {"new_type": {"name": "cloud_nvme20k"}}},
        }
    ]


def test_retype_rejects_invalid_volume_type_name(fake_transport):
    resource = Volumes(fake_transport)

    with pytest.raises(InvalidVolumeTypeNameError, match="Invalid volume type name"):
        run(resource.retype(volume_id="vol-1", type_name="regional-volume-type"))

    assert fake_transport.calls == []


def test_retype_requires_type(fake_transport):
    resource = Volumes(fake_transport)

    with pytest.raises(ValueError, match="type_id or type_name is required"):
        run(resource.retype(volume_id="vol-1"))

    assert fake_transport.calls == []


@pytest.mark.parametrize(
    ("availability_zone", "expected_params"),
    [
        (None, {}),
        ("br-se1-a", {"availability-zone": "br-se1-a"}),
    ],
)
def test_get_volume_types_builds_params(fake_transport, availability_zone, expected_params):
    resource = Volumes(fake_transport)

    result = run(resource.get_volume_types(availability_zone=availability_zone))

    assert result == {
        "method": "get",
        "path": "block-storage/v1/volume-types",
        "kwargs": {"params": expected_params},
    }
    assert fake_transport.calls == [result]
