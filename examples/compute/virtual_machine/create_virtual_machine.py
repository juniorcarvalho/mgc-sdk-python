import asyncio

from mgc.client import Client


async def main() -> None:
    api_token = "YOUR_API_TOKEN"

    async with Client(api_key=api_token) as client:
        virtual_machine = await client.compute.virtual_machines.create(
            name="example-instance",
            image_id="YOUR_IMAGE_ID",
            machine_type_id="YOUR_MACHINE_TYPE_ID",
            ssh_key_name="YOUR_SSH_KEY_NAME",
            availability_zone="br-se1-a",
        )

    print(virtual_machine)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
