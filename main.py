import asyncio
from pprint import pprint

from src.mgc.client import Client
from src.mgc.config import ClientConfig, Region


async def main():
    client = Client(
        api_key="API_KEY",
        config=ClientConfig(
            region=Region.BR_SE1,
        ),
    )

    try:
        print("\n== INSTANCES LIST ==")
        instances = await client.compute.instances.list()
        pprint(instances)

        # pega uma instância se existir
        items = instances.get("instances") or instances.get("items") or []

        if items:
            instance_id = items[0]["id"]

            print("\n== INSTANCE GET ==")
            instance = await client.compute.instances.get(instance_id)
            pprint(instance)

        print("\n== SNAPSHOTS LIST ==")
        snapshots = await client.compute.snapshots.list()
        pprint(snapshots)

        print("\n== BACKUPS LIST ==")
        backups = await client.compute.backups.list()
        pprint(backups)

    except Exception as e:
        print("\nERROR:")
        print(e)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())