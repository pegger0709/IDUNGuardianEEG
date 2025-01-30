import os
import asyncio
from idun_guardian_sdk import GuardianClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file
idun_api_token = os.getenv('IDUN_API_TOKEN')
idun_address = os.getenv('IDUN_DEVICE_ADDRESS')
client = GuardianClient(api_token=idun_api_token, address=idun_address)
MAINS_FREQUENCY_60Hz = False

if __name__ == "__main__":
    print(idun_address)
    battery_level = asyncio.run(client.check_battery())
    print("Battery Level: %s%%" % battery_level)