# EEG Project - Symmetry Perception

In this project, our team attempted to partially recreate the symmetry perception and affective response experimental results of [Makin et al.](https://www.sciencedirect.com/science/article/abs/pii/S0028393212004307) More specifically, we are using the BIDS EEG data from their 1st experiment, where 24 subjects are presented with symmetrical and random patterns. We focused on event-related potentials (ERPs) and time-frequency representations (TFRs) and tried to recreate the pipeline using the Python MNE library.


## I. Analysis Steps

Given our limited knowledge of EEG analysis, we focused on replicate the steps in the paper, with some minor differences:
1. We removed non-EEG electrodes, since our project is more limited in scope. There seemed to be an issue with missing names and types for electrodes, but we believe the last 8 in the data are the 4 ocular and 4  facial used for the MEG and EOG analysis.
2. Like in the paper, we re-referenced to scalp average, which we found a good standard as opposed to looking at individual electrodes.
3. Like in the paper, we applied a 25Hz low-pass filter and down-sampled to 128Hz, which seemed standard. Curiously enough, for the ERP analysis, the authors did not apply a high-pass filter, since they were worried about an erroneous latency bias, but we found that strange and it made us run into multiple issues in the next steps. This is why we opted for a 1Hz high-pass filter. 
5. Similar to the paper, we applied ICA, and attempted to remove ocular and muscle artefacts, but our experience was quite different. Our program only removed a few components (around 1 on average as opposed to 9 in the paper) it detected as ocular artefacts by referencing a frontal electrode between the eyes. Using a lower number of components did not seem to impact this, hence our choice of 40 components instead of 64 like in the paper, which also speeds up analysis. While 9 components on average might be too much to remove, we're not confident in our implementation, since it produced issues with rejection in epoching.
6. Like in the paper, we performed epoching with a -1 to 1s time window and a baseline correction of -200 to 50ms intervals for ERP experiments. For TFR, the window was -1 to 3 seconds.
7. In the paper, after ICA and epoching, and for ERP, trials are rejected if they exceed +-100µV, while for TFR it's +-75µV. For 5 subjects, applying ICA made them sensitive to any rejection criteria for our ERP experiment, although we couldn't figure out why, which led us to drop the rejection for TFR. It's possible it had something to do with our implementation of rejection (e.g. using drop instead of interpolate).

## II. Analysis Findings

We chose to analyze the case where we performed ICA without the 5 problematic subjects (4,8,16,17,18) and no rejection for TFR, the plots for which can be seen in the appropriate folders.

For the average ERP analysis, using a t-test, we found a statistically significant N1 difference (t = -4.17, p = 0.0006, p < 0.05), with N1 being stronger for symmetrical patterns, similar to the paper, which further supporting the hypothesis that humans respond differently to symmetry. The sustained posterior negativity was also similarly shaped to the paper, with symmetry having a lower overall amplitude. In fact, even the average P1 appeared to be a little stronger for symmetry. If we couple this with the EMG channels, we would likely be able to confirm a link between an unconscious biased affective response and symmetry.

Our TFR results also hint at higher activity in the right hemisphere like in the paper (stronger with all subjects), furthering the association between the right hemisphere and visuospatial activities. However, our average TFR visualization approach had some resolution issues, and we were mostly able to see a strong onset activity. This likely confirms the effect of time on the frequency bands, but we were unable to confirm an effect related desynchronization/later 10-14 Hz activity like in the paper.

## III. References
1. Makin, A. D. J., Wilton, M. M., Pecchinenda, A., & Bertamini, M. (2012). Symmetry perception and affective responses: A combined EEG/EMG study. _Neuropsychologia_, _50_(14), 3250–3261. doi:10.1016/j.neuropsychologia.2012.10.003
2. [MNE](https://mne.tools/stable/index.html)
3. [T-test method](https://neuraldatascience.io/7-eeg/erp_group_stats.html)
