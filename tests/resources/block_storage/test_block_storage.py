from mgc.resources.block_storage.block_storage import BlockStorage
from mgc.resources.block_storage.snapshots import Snapshots
from mgc.resources.block_storage.volumes import Volumes


def test_block_storage_initializes_resources_with_same_transport(fake_transport):
    block_storage = BlockStorage(fake_transport)

    assert isinstance(block_storage.volumes, Volumes)
    assert isinstance(block_storage.snapshots, Snapshots)
    assert block_storage.volumes._transport is fake_transport
    assert block_storage.snapshots._transport is fake_transport
