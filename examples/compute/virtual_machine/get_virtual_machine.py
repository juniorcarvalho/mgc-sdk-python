import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"
    instance_id = "YOUR_INSTANCE_ID"

    async with Client(api_key=api_token) as client:
        virtual_machine = await client.compute.virtual_machines.get(
            instance_id,
            expand=["image", "machine_type"],
        )

    print(virtual_machine)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
