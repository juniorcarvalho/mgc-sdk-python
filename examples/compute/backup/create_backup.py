import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    instance_id = "YOUR_INSTANCE_ID"

    async with Client(api_key=api_token) as client:
        backup = await client.compute.backups.create(
            instance_id=instance_id,
            name="example-backup",
        )

    print(backup)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
