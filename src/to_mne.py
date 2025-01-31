import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mne

def load_raw_data(raw_filename):
    df_raw = pd.read_csv(f"data/raw_csv/{raw_filename}")
    df_raw.timestamp = pd.to_datetime(df_raw.timestamp, unit='s')
    df_raw = df_raw.set_index("timestamp")
    return df_raw

def pandas_to_mne(df, sfreq, ch_names=None, ch_types=None):
    """
    Convert a pandas DataFrame containing EEG data to an MNE Raw object.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing EEG data (time points as rows, channels as columns)
    sfreq : float
        Sampling frequency of the data in Hz
    ch_names : list of str, optional
        Channel names. If None, will use DataFrame column names
    ch_types : list of str, optional
        Channel types (e.g., 'eeg', 'ecg'). If None, all channels set to 'eeg'
        
    Returns
    -------
    mne.io.RawArray
        MNE Raw object containing the EEG data
    """
    # Get data as numpy array (channels x time points)
    data = df.values.T
    
    # Use DataFrame column names if channel names not provided
    if ch_names is None:
        ch_names = df.columns.tolist()
    
    # Set all channels to EEG if types not provided
    if ch_types is None:
        ch_types = ['eeg'] * len(ch_names)
        
    # Create info structure
    info = mne.create_info(
        ch_names=ch_names,
        sfreq=sfreq,
        ch_types=ch_types
    )
    
    # Create Raw object
    raw = mne.io.RawArray(data, info)
    return raw

def preprocess_mne(raw, l_freq=1., h_freq=50., pad_seconds=5.):
    """
    Conducts preprocessing consisting of a bandpass filter (with 5s cropping to remove filter artifacts) as that's longer than the filter
    """
    filtered = raw.filter(l_freq=l_freq, h_freq=h_freq)
    preprocessed = filtered.copy().crop(tmin=pad_seconds, tmax=filtered.times[-1] - pad_seconds)
    return preprocessed

if __name__ == "__main__":
    raw_filenames_list = os.listdir("data/raw_csv")
    print(os.listdir("data/raw_csv"))
    raw_filename = ""
    while raw_filename not in raw_filenames_list:
        raw_filename = input("Please choose a raw EEG file (in CSV) to convert to MNE fif format: ")
    df_raw = load_raw_data(raw_filename)
    raw = pandas_to_mne(df_raw, sfreq=250., ch_names=['ch1'], ch_types=['eeg'])
    raw.save(f"data/raw_mne/{raw_filename[:-4]}_raw.fif", overwrite=True)
    preprocessed = preprocess_mne(raw, l_freq=1., h_freq=50., pad_seconds=5.)
    preprocessed.save(f"data/preprocessed/{raw_filename[:-4]}_preprocessed.fif", overwrite=True)

