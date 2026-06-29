import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    snapshot_id = "YOUR_SNAPSHOT_ID"
    instance_id = "YOUR_INSTANCE_ID"

    async with Client(api_key=api_token) as client:
        restore = await client.compute.snapshots.restore(
            snapshot_id,
            instance_id=instance_id,
        )

    print(restore)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
