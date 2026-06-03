from typing import Any

from src.mgc.transport import Transport


class Snapshots:
    def __init__(self, transport: Transport):
        self._transport = transport

    async def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        sort: str | None = None,
        expand: list[str] | None = None,
    ) -> dict[str, Any]:

        params = {
            "_limit": limit,
            "_offset": offset,
        }

        if sort:
            params["_sort"] = sort

        if expand:
            params["expand"] = expand

        return await self._transport.get(
            "compute/v1/snapshots",
            params=params,
        )

    async def get(
        self,
        snapshot_id: str,
        *,
        expand: list[str] | None = None,
    ) -> dict[str, Any]:

        params = {}

        if expand:
            params["expand"] = expand

        return await self._transport.get(
            f"compute/v1/snapshots/{snapshot_id}",
            params=params,
        )

    async def create(
        self,
        *,
        instance_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:

        payload = {
            "instance_id": instance_id,
        }

        if name:
            payload["name"] = name

        if description:
            payload["description"] = description

        return await self._transport.post(
            "compute/v1/snapshots",
            json=payload,
        )

    async def delete(
        self,
        snapshot_id: str,
    ) -> None:

        await self._transport.delete(
            f"compute/v1/snapshots/{snapshot_id}",
        )

    async def restore(
        self,
        snapshot_id: str,
        *,
        instance_id: str | None = None,
    ) -> dict[str, Any]:

        payload = {}

        if instance_id:
            payload["instance_id"] = instance_id

        return await self._transport.post(
            f"compute/v1/snapshots/{snapshot_id}/restore",
            json=payload,
        )

    async def create_from_instance(
        self,
        *,
        instance_id: str,
        name: str | None = None,
    ) -> dict[str, Any]:

        payload = {
            "instance_id": instance_id,
        }

        if name:
            payload["name"] = name

        return await self._transport.post(
            "compute/v1/snapshots",
            json=payload,
        )