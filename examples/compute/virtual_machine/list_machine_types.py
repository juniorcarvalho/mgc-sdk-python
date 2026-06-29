import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"

    async with Client(api_key=api_token) as client:
        machine_types = await client.compute.machine_types.list(
            limit=10,
            offset=0,
            sort="name:asc",
        )

    print(machine_types)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
