from .snapshots import Snapshots
from .volumes import Volumes


class BlockStorage:
    """Namespace for block storage volume operations."""

    def __init__(self, transport):
        """Create a volume resource client that share the same transport.

        Args:
            transport: Transport used to make API requests.
        """
        self.volumes = Volumes(transport)
        self.snapshots = Snapshots(transport)
