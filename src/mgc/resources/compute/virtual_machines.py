from typing import Any

from src.mgc.transport import Transport


class VirtualMachines:
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
            "compute/v1/instances",
            params=params,
        )

    async def get(
        self,
        instance_id: str,
        *,
        expand: list[str] | None = None,
    ) -> dict[str, Any]:

        params = {}

        if expand:
            params["expand"] = expand

        return await self._transport.get(
            f"compute/v1/instances/{instance_id}",
            params=params,
        )

    async def create(
        self,
        *,
        name: str,
        image_id: str,
        machine_type_id: str,
        ssh_key_name: str,
        availability_zone: str | None = None,
        user_data: str | None = None,
        network: dict | None = None,
    ) -> dict[str, Any]:
        payload = {
            "name": name,
            "image": {
                "id": image_id,
            },
            "machine_type": {
                "id": machine_type_id,
            },
            "ssh_key_name": ssh_key_name,
        }

        if availability_zone:
            payload["availability_zone"] = availability_zone

        if user_data:
            payload["user_data"] = user_data

        if network:
            payload["network"] = network

        return await self._transport.post(
            "/v1/instances",
            json=payload,
        )

    async def delete(
        self,
        instance_id: str,
        *,
        delete_public_ip: bool = False,
    ) -> None:

        await self._transport.delete(
            f"compute/v1/instances/{instance_id}",
            params={
                "delete_public_ip": delete_public_ip,
            },
        )

    async def start(
        self,
        instance_id: str,
    ) -> None:

        await self._transport.post(f"compute/v1/instances/{instance_id}/start")

    async def stop(
        self,
        instance_id: str,
    ) -> None:

        await self._transport.post(f"compute/v1/instances/{instance_id}/stop")

    async def reboot(
        self,
        instance_id: str,
    ) -> None:

        await self._transport.post(f"compute/v1/instances/{instance_id}/reboot")

    async def suspend(
        self,
        instance_id: str,
    ) -> None:

        await self._transport.post(f"compute/v1/instances/{instance_id}/suspend")

    async def rename(
        self,
        instance_id: str,
        name: str,
    ) -> None:

        await self._transport.patch(
            f"compute/v1/instances/{instance_id}/rename",
            json={
                "name": name,
            },
        )

    async def retype(
        self,
        instance_id: str,
        machine_type_id: str,
    ) -> None:

        await self._transport.post(
            f"compute/v1/instances/{instance_id}/retype",
            json={
                "machine_type": {
                    "id": machine_type_id,
                }
            },
        )
