import asyncio

from src.mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"

    async with Client(api_key=api_token) as client:
        virtual_machines = await client.compute.virtual_machines.list(
            limit=10,
            offset=0,
            sort="created_at:desc",
        )

    print(virtual_machines)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
