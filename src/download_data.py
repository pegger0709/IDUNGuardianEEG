"""
Sample script for using the Guardian Earbud Client

Download EEG data from a recording
"""
import os
import argparse
from idun_guardian_sdk import GuardianClient, FileTypes
from dotenv import load_dotenv

load_dotenv()
my_api_token = os.getenv('IDUN_API_TOKEN')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script downloads recorded raw EEG data to csv and saves it on your machine.")
    parser.add_argument('recording_id', type=str, help='ID of the recordign to download.')
    args = parser.parse_args()
    recording_id = args.recording_id
    client = GuardianClient(api_token=my_api_token)
    client.download_file(recording_id=recording_id, file_type=FileTypes.EEG)