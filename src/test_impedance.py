import asyncio
import os
from idun_guardian_sdk import GuardianClient
from dotenv import load_dotenv

def print_impedance(data):
    print(f"{data/1000.}\tkOhm")


async def sample_task(seconds):
    """
    Replace your function/task here
    """
    for i in range(seconds):
        print(f"Run a sample task for: {i}/{seconds} seconds")
        await asyncio.sleep(1)


async def main():
    load_dotenv()  # Load variables from .env file
    idun_api_token = os.getenv('IDUN_API_TOKEN')
    idun_address = os.getenv('IDUN_DEVICE_ADDRESS')
    client = GuardianClient(debug=True, api_token=idun_api_token, address=idun_address)
    await client.connect_device()  # Connect to the device is not required, sdk handles it

    print("Starting impedance task")
    task = asyncio.create_task(client.stream_impedance(handler=print_impedance))

    try:
        await sample_task(seconds=30)
        client.stop_impedance()
        await task
        await client.disconnect_device()  # Disconnect to the device is not required to be called, sdk handles it on program exit

    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


if __name__ == "__main__":
    asyncio.run(main())