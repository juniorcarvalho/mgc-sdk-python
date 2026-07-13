import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"

    async with Client(api_key=api_token) as client:
        volumes = await client.block_storage.volumes.list(limit=10, offset=0)

    print(volumes)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
