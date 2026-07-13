from __future__ import annotations

from typing import Any

from mgc.transport import Transport


class Snapshots:
    """Manage Block Storage snapshot operations."""

    def __init__(self, transport: Transport):
        """Create a snapshots resource client.

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
        """List Block Storage snapshots.

        Args:
            limit: Maximum number of snapshots to return.
            offset: Number of snapshots to skip before returning results.
            sort: Optional API sort expression.
            expand: Optional related fields to expand in the response.
            name: Optional snapshot name filter.

        Returns:
            Parsed API response containing snapshot data.
        """
        params: dict[str, Any] = {
            "_limit": limit,
            "_offset": offset,
        }

        filters = {"_sort": sort, "expand": expand, "name": name}
        for key, value in filters.items():
            if value:
                params[key] = value

        return await self._transport.get(
            "block-storage/v1/snapshots",
            params=params,
        )

    async def create(
        self,
        *,
        name: str,
        description: str | None,
        volume_id: str | None = None,
        volume_name: str | None = None,
    ) -> dict[str, Any]:
        """Create a Block Storage snapshot.

        Args:
            name: Name for the new snapshot.
            description: Description for the new snapshot.
            volume_id: Optional ID of the source volume.
            volume_name: Optional name of the source volume.

        Returns:
            Parsed API response, usually containing the created snapshot ID.
        """
        payload: dict[str, Any] = {
            "name": name,
            "description": description,
        }

        if volume_id:
            payload["volume"] = {"id": volume_id}
        elif volume_name:
            payload["volume"] = {"name": volume_name}
        else:
            raise ValueError("volume_id or volume_name is required")

        return await self._transport.post(
            "block-storage/v1/snapshots",
            json=payload,
        )

    async def delete(
        self,
        *,
        snapshot_id: str,
    ) -> None:
        """Delete a Block Storage snapshot.

        Args:
            snapshot_id: ID of the snapshot to delete.
        """
        await self._transport.delete(
            f"block-storage/v1/snapshots/{snapshot_id}",
        )

    async def get(
        self,
        *,
        snapshot_id: str,
        expand: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a Block Storage snapshot by ID.

        Args:
            snapshot_id: ID of the snapshot to retrieve.
            expand: Optional related fields to expand in the response.

        Returns:
            Parsed API response containing snapshot data.
        """
        params: dict[str, Any] = {}

        if expand:
            params["expand"] = expand

        return await self._transport.get(
            f"block-storage/v1/snapshots/{snapshot_id}",
            params=params,
        )

    async def rename(
        self,
        *,
        snapshot_id: str,
        name: str,
    ) -> None:
        """Rename a Block Storage snapshot.

        Args:
            snapshot_id: ID of the snapshot to rename.
            name: New name for the snapshot.
        """
        await self._transport.patch(
            f"block-storage/v1/snapshots/{snapshot_id}/rename",
            json={"name": name},
        )
