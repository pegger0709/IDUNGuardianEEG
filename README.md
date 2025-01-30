# Recording and analyzing ear-EEG signals with the IDUN Guardian (TM)

The goal of this project is to help you get started using your IDUN Guardian device together with the IDUN Python SDK to record and analyze ear-EEG signals. For more documentation on the Python SDK, please see [here](https://sdk-docs.idunguardian.com/index.html).

## Installation

We assume you have Python version 3.10 or higher.

```bash
# Clone the repository
git clone https://github.com/pegger0709/IDUNGuardianEEG.git

# Navigate to the project directory
cd IDUNGuardianEEG

# Create a virtual environment 
python -m venv .venv

# Activate the virtual environment (Windows)
.\.venv\Scripts\activate

# Activate the virtual environment (MacOS/Linux)
source .venv\bin\activate

# Install dependencies
pip install -r .\requirements.txt
```

## Environment variables
First, we'll set the environment variables you need to use the SDK with your Guardian. The device address should look like A1-B2-C3-D4-E5-F6 and be written on the back of the device. If you do not have your API token for the SDK, please email [IDUN Support](mailto:support@iduntechnologies.com) for help.

Assuming you have both the device address and API token, you will create a `.env` file in the root directory, with the following content:

```
IDUN_DEVICE_ADDRESS=<device_address>
IDUN_API_TOKEN=<api_token>
```

## Usage 
Now for the fun part, actually recording EEG signals! First ensure your Guardian is powered on and the Bluetooth function on your laptop is activated. Then ensure both your ears and the Guardian electrodes are clean before inserting the Guardian according to the instructions.

Before starting a recording, we should check that the device has sufficient battery power, and that the impedance is sufficiently low to allow for a good signal. Ideally, you should have impedance levels consistently below 200kOhm before beginning recording, your signal quality will thank you for taking the time for this.

```bash
# check battery level
python .\src\check_battery.py

#check impedance
python .\src\test_impedance.py
```
Now that we have good impedance, we will actually begin recording. We need to choose the length of the recording in seconds.

```
python .\src\record_data.py <seconds_to_record_for>
```
After the recording is complete, you should see something like the following in the console:
```
[INFO] YYYY-MM-DD hh:mm:ss: [CLIENT]: Recording ID <UTC_in_milliseconds_when_the_recording_began>
[DEBUG] YYYY-MM-DD hh:mm:ss: [BLE]: Connection handler gracefully stopping.
[DEBUG] YYYY-MM-DD hh:mm:ss: [BLE]: Disconnecting from the device on handler stop...
[DEBUG] YYYY-MM-DD hh:mm:ss: [BLE]: Callback function recognised a disconnection.
```
Now the recording is ready to be downloaded onto your machine. Simply run

```
python .\src\download_data.py <UTC_in_milliseconds_when_the_recording_began>
```
and the csv of the raw EEG will be saved to your root directory. We recommend creating a directory called `data` at root level with subdirectories called `raw_csv`, `raw_mne`, `preprocessed`, `epochs`, and `features`. The raw EEG in csv form that you just downloaded would thus belong in the `data\raw_csv` directory.

If you want to download a recording other than the one you just made, you can find which recordings are downloadable by running
```
python .\src\get_recordings.py
```

