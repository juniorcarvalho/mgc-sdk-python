import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    volume_id = "YOUR_VOLUME_ID"

    async with Client(api_key=api_token) as client:
        snapshot = await client.block_storage.snapshots.create(
            name="example-snapshot",
            description="Snapshot created with the Python SDK.",
            volume_id=volume_id,
        )

    print(snapshot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
