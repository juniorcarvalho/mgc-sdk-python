import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    snapshot_id = "YOUR_SNAPSHOT_ID"

    async with Client(api_key=api_token) as client:
        await client.block_storage.snapshots.delete(snapshot_id=snapshot_id)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
