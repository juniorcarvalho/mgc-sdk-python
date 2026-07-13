import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    backup_id = "YOUR_BACKUP_ID"

    async with Client(api_key=api_token) as client:
        await client.compute.backups.rename(
            backup_id,
            name="example-backup-renamed",
        )

    print("Backup renamed successfully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
