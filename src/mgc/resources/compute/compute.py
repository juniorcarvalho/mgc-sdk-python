from .machine_types import MachineTypes
from .virtual_machines import VirtualMachines
from .images import Images
from .snapshots import Snapshots
from .backups import Backups

class Compute:
    def __init__(self, transport):
        self.virtual_machines = VirtualMachines(transport)
        self.images = Images(transport)
        self.machine_types = MachineTypes(transport)
        self.snapshots = Snapshots(transport)
        self.backups = Backups(transport)