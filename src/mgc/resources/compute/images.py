from typing import Any

from src.mgc.transport import Transport


class Images:
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
            "compute/v1/images",
            params=params,
        )
