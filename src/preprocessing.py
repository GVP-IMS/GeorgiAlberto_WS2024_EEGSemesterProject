### Imports ###

import mne
from mne_bids import read_raw_bids
import numpy as np

### Functions ###

def load_subject(given_path, debug_logs, debug_images):
    """Load subject data from given path, drop unnecessary channels and setup scalp montage
    given_path (str): Path to BIDS data
    debug_logs & debug_images (bool): control logging output
    Returns mne.io.Raw"""

    # Read raw BIDS data and load it into memory for manipulation
    raw_data = read_raw_bids(bids_path = given_path, verbose = debug_logs).load_data()

    # Exclude non-EEG channels
    # These channels are unlabeled but should be the 4 facial and 4 ocular from the paper (they also cause issues)
    raw_data.drop_channels(['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8'])

    # Set up electrode montage scheme
    raw_data.set_montage('standard_1020', match_case = False)

    # Sanity check
    if debug_images:
        raw_data.plot_sensors(show_names = True)
        raw_data.plot()
        raw_data

    return raw_data

def filter_data(given_data, debug_logs, debug_images):
    """Apply re-referencing, low and high pass filters and resampling
    given_data: mne.io.Raw"""
    
    # EEG trace re-referenced to scalp average
    given_data.set_eeg_reference(ref_channels = 'average', verbose = debug_logs)
    # Sanity check
    if debug_images: given_data.plot()

    # Set low/high-pass filters (l_freq = low number = high-pass / h_freq = high number = low-pass)
    given_data.filter(l_freq = 1, h_freq = 25, fir_design = 'firwin', verbose = debug_logs)
    # Sanity check
    if debug_images: given_data.plot()

    # Downsample
    given_data.resample(sfreq=128, verbose = debug_logs)
    # Sanity check
    if debug_images: given_data.plot()

    return given_data

def ica(given_data, debug_logs, debug_images):
    """Analyzes possible components and excludes faulty ones"""
    
    # Initialize ICA and fit it to the data
    # ICA is stochastic, here we opt for the random seed 2
    ica = mne.preprocessing.ICA(method = 'picard', n_components = 40, random_state = 2, verbose = debug_logs).fit(given_data, verbose = debug_logs)
    # Sanity check
    if debug_images: ica.plot_components()

    # Find bad components
    componnets1, scores1 = ica.find_bads_eog(given_data, 'AFz', verbose = debug_logs)
    componnets2, scores2 = ica.find_bads_muscle(given_data, verbose = debug_logs)
    # Sanity check
    if debug_images:
        ica.plot_scores(scores1, componnets1)
        ica.plot_scores(scores2, componnets2)

    # Remove bad components
    ica.apply(given_data, exclude = componnets1 + componnets2, verbose = debug_logs)
    # Sanity check
    if debug_images: given_data
    
    return given_data

def epoch_data(given_data, time_min, time_max, reject_criteria, debug_logs, debug_images):
    """Separate data into epochs
    tmin (float): Start time of the epoch in seconds
    tmax (float): End time of the epoch in seconds
    reject_criteria (float or None): Threshold for trial rejection based on amplitude
    Returns epoched data as mne.Epochs"""

    # Define events
    event_dict = {'regular': 1, 'random': 3}

    # Get epochs
    events = mne.find_events(given_data, initial_event = True, verbose = debug_logs)
    epochs = mne.Epochs(given_data, events, event_dict, tmin = time_min, tmax = time_max, baseline = (-0.2,0.05), verbose = debug_logs)
    
    # Reject bad trials (amplitude exceeds given ±μV)
    if reject_criteria:
        epochs.drop_bad(reject = {'eeg': reject_criteria})
    
    # Sanity check
    if debug_images: epochs

    return epochs

def perform_tfr(given_epochs, debug_logs):
    """Perform time-frequency analysis on epoched data using DPSS tapers
    Return dictionary containing time-frequency representations for each event type"""

    # Define frequency range (Y axis)
    freqs = np.logspace(np.log10(5), np.log10(20), num = 30)
    # Define number of cycles per frequency
    n_cycles = freqs / 2.0

    # Perform time-frequency analysis
    power_regular = mne.time_frequency.tfr_multitaper(given_epochs['regular'], freqs = freqs, n_cycles = n_cycles,
                                                    use_fft = True, return_itc = False, verbose = debug_logs)
    power_random = mne.time_frequency.tfr_multitaper(given_epochs['random'], freqs = freqs, n_cycles = n_cycles,
                                                    use_fft = True, return_itc = False, verbose = debug_logs)

    return {'regular': power_regular, 'random': power_random}