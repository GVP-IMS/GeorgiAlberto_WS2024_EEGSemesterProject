### Imports ###

import mne
from matplotlib import pyplot as plt

### Functions ###

"""All return plots/figs"""

def plot_erp(given_epochs, subject_id = 1):
    
    # Define epochs
    regular_epochs = given_epochs['regular'].average()
    random_epochs = given_epochs['random'].average()
    evokeds = dict(regular = regular_epochs, random = random_epochs)

    # Focus on channels PO7 and PO8
    picks = [f'PO{n}' for n in range(7, 9)]

    # Visualize mean ERP
    # For some reason matplotlib seems to save plots as a list, hence the [0] (or at least it fixes our plot saves)
    fig = mne.viz.plot_compare_evokeds(evokeds, picks = picks, combine = 'mean',
                                 title = f'Subject {subject_id} PO7 & PO8 ERP', colors = ['tab:blue','tab:orange'])[0]
    
    return fig

def plot_average_erp(given_average):

    # Focus on channels PO7 and PO8
    picks = [f'PO{n}' for n in range(7, 9)]

    # Visualize mean ERP
    fig = mne.viz.plot_compare_evokeds(given_average, picks = picks, combine = 'mean',
                                 title = f'Average PO7 & PO8 ERP', colors = ['tab:blue','tab:orange'])[0]
    
    return fig

def plot_tfr(given_powers, debug_logs, subject_id = 1):

    # Iterate over each subject's stimuli and power in spectra to get subplots
    figs = []
    for stimuli, power in given_powers.items():
        # Joint plot for channels PO3 & PO7
        figs.append(power.plot_joint(picks = ['PO3','PO7'], mode = 'logratio',
                        title = f'Subject {subject_id} PO3 & PO7 TFR, left posterior, {stimuli} trials',
                        baseline = (-0.5,0), timefreqs = [(0.5, 12), (1.5, 12)], verbose = debug_logs))
        # Joint plot for channels PO4 & PO8
        figs.append(power.plot_joint(picks = ['PO4','PO8'], mode = 'logratio',
                        title = f'Subject {subject_id} PO4 & PO8 TFR, right posterior, {stimuli} trials',
                        baseline = (-0.5,0), timefreqs = [(0.5, 12), (1.5, 12)], verbose = debug_logs))

    # Create the main 2x2 plot
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(f'Subject {subject_id} TFR overview')

    # Combine subplots
    for counter, (stimuli, power) in enumerate(given_powers.items()):
        axes[counter, 0].imshow(figs[counter * 2].canvas.buffer_rgba(), aspect = 'auto', origin = 'upper')
        axes[counter, 0].axis('off')
        axes[counter, 1].imshow(figs[counter * 2 + 1].canvas.buffer_rgba(), aspect = 'auto', origin = 'upper')
        axes[counter, 1].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()

    return fig

def plot_topomap(given_evoked, times = [0.52, 2.0], title = 'Topomap', save_path=None):

    # Get topomap subplots
    fig_regular = given_evoked['regular'].plot_topomap(times = times, ch_type = 'eeg')
    fig_random = given_evoked['random'].plot_topomap(times = times, ch_type = 'eeg')
    
    # Create the main 2x1 plot
    fig, axes = plt.subplots(2, 1, figsize=(4, 5))
    fig.suptitle(title)

    # Combine subplots
    axes[0].imshow(fig_regular.canvas.buffer_rgba(), aspect='auto', origin='upper')
    axes[0].set_title(f"Regular trials")
    axes[0].axis('off')
    axes[1].imshow(fig_random.canvas.buffer_rgba(), aspect='auto', origin='upper')
    axes[1].set_title(f"Random trials")
    axes[1].axis('off')
    
    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()

    return fig