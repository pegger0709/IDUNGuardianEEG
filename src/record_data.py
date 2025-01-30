"""
Sample script for using the Guardian Earbud Client

- Start recording data from the Guardian Earbuds
"""
import os
import asyncio
import argparse
from idun_guardian_sdk import GuardianClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

LED_SLEEP: bool = False

my_api_token = os.getenv('IDUN_API_TOKEN')

# Example callback function
def print_data(event):
    print("CB Func:", event.message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script records EEG data of a given time length from the Guardian Earbuds.")
    parser.add_argument('recording_timer', type=int, help='Time duration of the recording in seconds.')
    args = parser.parse_args()
    RECORDING_TIMER = args.recording_timer
    client = GuardianClient(api_token=my_api_token, debug=True)

    # Subscribe to live insights and/or realtime predictions
    #client.subscribe_live_insights(raw_eeg=True, filtered_eeg=True, handler=print_data)
    #client.subscribe_realtime_predictions(fft=True, jaw_clench=False, handler=print_data)

    # start a recording session
    print(f"We are about to record {RECORDING_TIMER} seconds of EEG data...")
    asyncio.run(
        client.start_recording(
            recording_timer=RECORDING_TIMER, led_sleep=LED_SLEEP, calc_latency=False
        )
    )
