import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    volume_id = "YOUR_VOLUME_ID"

    async with Client(api_key=api_token) as client:
        await client.block_storage.volumes.delete(volume_id=volume_id)

    print("Volume deleted successfully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
