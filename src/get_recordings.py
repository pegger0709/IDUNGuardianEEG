"""
Sample script for using the Guardian Earbud Client

Get a list of recordings
"""
import os
import pdb
from datetime import datetime
from idun_guardian_sdk import GuardianClient
from dotenv import load_dotenv

load_dotenv()
my_api_token = os.getenv('IDUN_API_TOKEN')
idun_address = os.getenv('IDUN_DEVICE_ADDRESS')


def to_date(timestamp):
    """
    Converts timestamp to formatted date/time
    """
    milliseconds = int(timestamp / 1000)
    dt = datetime.fromtimestamp(milliseconds)
    formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return formatted_date


if __name__ == "__main__":
    print(f"DEVICE: {idun_address}, API_TOKEN: {my_api_token}")
    client = GuardianClient(api_token=my_api_token, address=idun_address)
    recordings = client.get_recordings(limit=10)

    for recording in recordings["items"]:
        recording_date = to_date(recording["recordingId"])
        recording_id = recording["recordingId"]
        print(f"Recording Date: {recording_date}. Recording ID: {recording_id}")