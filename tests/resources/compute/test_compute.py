from mgc.resources.compute.backups import Backups
from mgc.resources.compute.compute import Compute
from mgc.resources.compute.images import Images
from mgc.resources.compute.machine_types import MachineTypes
from mgc.resources.compute.snapshots import Snapshots
from mgc.resources.compute.virtual_machines import VirtualMachines


def test_compute_initializes_compute_resources_with_same_transport(fake_transport):
    compute = Compute(fake_transport)

    assert isinstance(compute.virtual_machines, VirtualMachines)
    assert isinstance(compute.images, Images)
    assert isinstance(compute.machine_types, MachineTypes)
    assert isinstance(compute.snapshots, Snapshots)
    assert isinstance(compute.backups, Backups)
    assert compute.virtual_machines._transport is fake_transport
    assert compute.images._transport is fake_transport
    assert compute.machine_types._transport is fake_transport
    assert compute.snapshots._transport is fake_transport
    assert compute.backups._transport is fake_transport
