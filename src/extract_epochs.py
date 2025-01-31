import mne
import os
import numpy as np
import pandas as pd
import itertools
from scipy import signal

def extract_epochs(preprocessed):
    """
    Extracts epochs from a preprocessed MNE file representing an EEG recording.

    This function takes a preprocessed MNE file and breaks it into epochs based on hardcoded event timestamps and categories.
    The event timestamps are generated for 24 events, each with a duration of 20 seconds, starting every 30 seconds.
    The event categories alternate between 1 (beginning of neutral stimulus) and 2 (beginning of emotion-evoking stimulus).

    Parameters:
    preprocessed (mne.io.Raw): The preprocessed MNE file representing the EEG recording.

    Returns:
    mne.Epochs: The epochs extracted from the preprocessed EEG recording.
    """
    event_timestamps = list(itertools.chain(*[[30*e, 30*e+20] for e in range(24)]))
    event_categories = [1, 2]*24 #1: beginning of neutral stimulus, 2: beginning of emotion-evoking stimulus
    events = np.column_stack([
        preprocessed.time_as_index(event_timestamps),
        np.zeros(len(event_timestamps)),
        np.array(event_categories) 
    ]).astype(int)

    emotional_epochs = mne.Epochs(
        preprocessed, 
        baseline=None, 
        events=events, 
        event_id=2, 
        tmin=0, 
        tmax=10, 
        preload=True
    ).drop_bad(reject={"eeg": 500})
    neutral_epochs = mne.Epochs(
        preprocessed, 
        baseline=None, 
        events=events, 
        event_id=1, 
        tmin=0, 
        tmax=20, 
        preload=True
    ).drop_bad(reject={"eeg": 500})

    return emotional_epochs, neutral_epochs

def extract_eeg_features(epochs):
    """
    Extract time and frequency domain features from EEG epochs.
    
    Parameters:
    -----------
    epochs : mne.Epochs
        The epochs object containing EEG data
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing features for each epoch and channel
    """
    # Initialize lists to store features
    features = []
    
    # Get data and parameters
    data = epochs.get_data()
    sfreq = epochs.info['sfreq']
    ch_names = epochs.ch_names
    
    # Define frequency bands
    freq_bands = {
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 100)
    }
    
    # Process each epoch
    for epoch_idx in range(len(epochs)):
        # Process each channel
        for ch_idx, ch_name in enumerate(ch_names):
            signal_data = data[epoch_idx, ch_idx]
            
            # Time domain features
            features_dict = {
                'epoch': epoch_idx
            }
            
            # Hjorth Parameters
            # Activity - variance of the signal
            activity = np.var(signal_data)
            
            # Mobility - square root of variance of first derivative divided by variance
            diff_first = np.diff(signal_data)
            mobility = np.sqrt(np.var(diff_first) / activity)
            
            # Complexity - compare mobility of first derivative to mobility of signal
            diff_second = np.diff(diff_first)
            complexity = np.sqrt(np.var(diff_second) / np.var(diff_first)) / mobility
            
            # Zero crossings
            zero_crossings = np.sum(np.diff(np.signbit(signal_data).astype(int)) != 0)
            
            # Add time domain features
            features_dict.update({
                'activity': activity,
                'mobility': mobility,
                'complexity': complexity,
                'zero_crossings': zero_crossings
            })
            
            # Frequency domain features
            # Calculate power spectral density
            freqs, psd = signal.welch(signal_data, fs=sfreq, nperseg=min(256, len(signal_data)))
            
            # Calculate band powers
            for band_name, (fmin, fmax) in freq_bands.items():
                freq_mask = (freqs >= fmin) & (freqs <= fmax)
                band_power = np.mean(psd[freq_mask])
                features_dict[f'{band_name}_power'] = band_power
            
            # Add relative band powers
            #total_power = np.sum(psd)
            #for band_name in freq_bands.keys():
            #    features_dict[f'{band_name}_relative_power'] = features_dict[f'{band_name}_power'] / total_power
            
            features.append(features_dict)
    
    # Convert to DataFrame
    df_features = pd.DataFrame(features).set_index('epoch')
    return df_features

if __name__ == "__main__":
    preprocessed_filenames_list = os.listdir("data/preprocessed")
    print(os.listdir("data/preprocessed"))
    preprocessed_filename = ""
    while preprocessed_filename not in preprocessed_filenames_list:
        preprocessed_filename = input("Please choose a preprocessed EEG file to epoch and extract features from: ")
    preprocessed = mne.io.read_raw_fif(f"data\\preprocessed\\{preprocessed_filename}", preload=True)
    emotional_epochs, neutral_epochs = extract_epochs(preprocessed)
    emotional_epochs.save(f"data\\epochs\\{preprocessed_filename[:-4]}_emotional-epo.fif")
    neutral_epochs.save(f"data\\epochs\\{preprocessed_filename[:-4]}_neutral-epo.fif")
    emotional_features = extract_eeg_features(emotional_epochs)
    emotional_features.to_csv(f"data\\features\\{preprocessed_filename[:-4]}_emotional-features.csv")