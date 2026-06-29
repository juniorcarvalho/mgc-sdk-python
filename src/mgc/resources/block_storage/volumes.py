from __future__ import annotations

from typing import Any

from mgc.exceptions import InvalidVolumeTypeNameError
from mgc.transport import Transport

VALID_VOLUME_TYPE_NAMES = frozenset(
    {
        "cloud_nvme1k",
        "cloud_nvme5k",
        "cloud_nvme10k",
        "cloud_nvme15k",
        "cloud_nvme20k",
    }
)


def _validate_volume_type_name(type_name: str) -> None:
    if type_name not in VALID_VOLUME_TYPE_NAMES:
        valid_types = ", ".join(sorted(VALID_VOLUME_TYPE_NAMES))
        raise InvalidVolumeTypeNameError(f"Invalid volume type name: {type_name}. Valid types are: {valid_types}")


class Volumes:
    """Manage volumes operations."""

    def __init__(self, transport: Transport):
        """Create a volumes resource client.

        Args:
            transport: Shared transport used to send API requests.
        """
        self._transport = transport

    async def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        sort: str | None = None,
        expand: list[str] | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        """List block storage volumes.

        Args:
            limit: Maximum number of volumes to return.
            offset: Number of volumes to skip before returning results.
            sort: Optional API sort expression.
            expand: Optional related fields to expand in the response.
            name: Optional volume name filter.

        Returns:
            Parsed API response containing volume data.
        """

        params: dict[str, Any] = {
            "_limit": limit,
            "_offset": offset,
        }

        FILTERS = {"_sort": sort, "expand": expand, "name": name}
        for key, value in FILTERS.items():
            if value:
                params[key] = value

        return await self._transport.get(
            "block-storage/v1/volumes",
            params=params,
        )

    async def create(
        self,
        *,
        name: str,
        size: int,
        type_id: str | None = None,
        type_name: str | None = None,
        backup_id: str | None = None,
        backup_name: str | None = None,
        snapshot_id: str | None = None,
        snapshot_name: str | None = None,
        availability_zone: str | None = None,
    ) -> dict[str, Any]:
        """Create a block storage volume.

        Args:
            name: Name for the new volume. Must contain between 3 and 50 characters.
            size: Volume size in GiB, within the range accepted by the API.
            type_id: Optional ID of the volume type to assign.
            type_name: Optional name of the volume type to assign.
            backup_id: Optional ID of the backup used to create the volume.
            backup_name: Optional name of the backup used to create the volume.
            snapshot_id: Optional ID of the snapshot used to create the volume.
            snapshot_name: Optional name of the snapshot used to create the volume.
            availability_zone: Optional availability zone for the volume.

        Returns:
            Parsed API response, usually containing the created volume ID.
        """
        payload: dict[str, Any] = {
            "name": name,
            "size": size,
        }

        if type_id:
            payload["type"] = {"id": type_id}
        elif type_name:
            _validate_volume_type_name(type_name)
            payload["type"] = {"name": type_name}
        else:
            raise ValueError("type_id or type_name is required")

        if backup_id:
            payload["backup"] = {"id": backup_id}
        elif backup_name:
            payload["backup"] = {"name": backup_name}

        if snapshot_id:
            payload["snapshot"] = {"id": snapshot_id}
        elif snapshot_name:
            payload["snapshot"] = {"name": snapshot_name}

        if availability_zone:
            payload["availability_zone"] = availability_zone

        return await self._transport.post(
            "block-storage/v1/volumes",
            json=payload,
        )

    async def delete(
        self,
        *,
        volume_id: str,
    ) -> None:
        """Delete a block storage volume.

        Args:
            volume_id: ID of the volume to delete.
        """

        await self._transport.delete(
            f"block-storage/v1/volumes/{volume_id}",
        )

    async def get(
        self,
        *,
        volume_id: str,
        expand: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a block storage volume by ID.

        Args:
            volume_id: ID of the volume to retrieve.
            expand: Optional related fields to expand in the response.

        Returns:
            Parsed API response containing volume data.
        """

        params: dict[str, Any] = {}

        if expand:
            params["expand"] = expand

        return await self._transport.get(
            f"block-storage/v1/volumes/{volume_id}",
            params=params,
        )

    async def attach(
        self,
        *,
        volume_id: str,
        virtual_machine_id: str,
    ) -> None:
        """Attach a block storage volume to a virtual machine.

        Args:
            volume_id: ID of the volume to attach.
            virtual_machine_id: ID of the target virtual machine.
        """

        await self._transport.post(
            f"block-storage/v1/volumes/{volume_id}/attach/{virtual_machine_id}",
        )

    async def detach(
        self,
        *,
        volume_id: str,
    ) -> None:
        """Detach a block storage volume from a virtual machine.

        Args:
            volume_id: ID of the volume to detach.
        """

        await self._transport.post(
            f"block-storage/v1/volumes/{volume_id}/detach",
        )

    async def extend(
        self,
        *,
        volume_id: str,
        size: int,
    ) -> None:
        """Extend the size of a block storage volume.

        Args:
            volume_id: ID of the volume to extend.
            size: New size for the volume in GiB.
        """

        await self._transport.post(
            f"block-storage/v1/volumes/{volume_id}/extend",
            json={"size": size},
        )

    async def rename(
        self,
        *,
        volume_id: str,
        name: str,
    ) -> None:
        """Rename a block storage volume.

        Args:
            volume_id: ID of the volume to rename.
            name: New name for the volume.
        """

        await self._transport.patch(
            f"block-storage/v1/volumes/{volume_id}/rename",
            json={"name": name},
        )

    async def retype(
        self,
        *,
        volume_id: str,
        type_id: str | None = None,
        type_name: str | None = None,
    ) -> None:
        """Change the type of a block storage volume.

        Args:
            volume_id: ID of the volume to retype.
            type_id: Optional ID of the new volume type.
            type_name: Optional name of the new volume type.
        """

        payload: dict[str, Any] = {}

        if type_id:
            payload["new_type"] = {"id": type_id}
        elif type_name:
            _validate_volume_type_name(type_name)
            payload["new_type"] = {"name": type_name}
        else:
            raise ValueError("type_id or type_name is required")

        return await self._transport.post(
            f"block-storage/v1/volumes/{volume_id}/retype",
            json=payload,
        )

    async def get_volume_types(
        self,
        *,
        availability_zone: str | None = None,
    ) -> dict[str, Any]:
        """Get available block storage volume types.

        Args:
            availability_zone: Optional availability zone filter.

        Returns:
            Parsed API response containing volume type data.
        """

        params: dict[str, Any] = {}

        if availability_zone:
            params["availability-zone"] = availability_zone

        return await self._transport.get(
            "block-storage/v1/volume-types",
            params=params,
        )
