# Function List and usage
# Assuming you have denoised ECG data/ signal, the followin ECG metrics can be extracted
#
# rr_intervals          = np.diff(r_peaks) / sampling_rate
# heart_rate            = calculate_heart_rate(r_peaks)
# rhythm_status         = analyze_rhythm(rr_intervals)
# st_segment_changes    = analyze_st_segment(denoised_ecg, r_peaks)
# t_wave_status         = analyze_t_wave(denoised_ecg)
# pq_interval_status    = analyze_pq_interval(rr_intervals)
#
# Ensure following Python dependencies are installed: numpy, scipy
# Use:  ' pip install numpy'
#       ' pip install scipy'
#
# Author: Kaustubh Sinha, 2023


import numpy as np
from scipy.signal import find_peaks


def find_r_peaks(ecg_signal, threshold=0.2, sampling_rate=1000):
    """ Find R-peaks in an ECG signal.

    Args:
        ecg_signal                      (array-like): The ECG signal.
        threshold                       (float, optional): Peak detection threshold. Default is 0.2.
        sampling_rate                   (int, optional): Sampling rate in Hz. Default is 1000.

    Returns:
        r_peak_indices (array):         Indices of R-peaks.
    """
    peaks, _ = find_peaks(ecg_signal, height=threshold)

    return peaks

def calculate_heart_rate(r_peak_indices, sampling_rate=1000):
    """ Calculate heart rate from R-peak indices.

    Args:
        r_peak_indices (array):         Indices of R-peaks.
        sampling_rate (int, optional):  Sampling rate in Hz. Default is 1000.

    Returns:
        heart_rate (float):             Heart rate in BPM (beats per minute).
    """
    if len(r_peak_indices) <= 1:
        return 0  # Return 0 if not enough R-peaks are detected

    rr_intervals = np.diff(r_peak_indices) / sampling_rate
    heart_rate = 60.0 / np.mean(rr_intervals)

    return heart_rate, rr_intervals

def analyze_rhythm(rr_intervals, threshold=0.15):
    """ Analyze the heart rhythm based on RR intervals.

    Args:
        rr_intervals (array-like):      RR intervals.
        threshold (float, optional):    Threshold for identifying rhythm abnormalities. Default is 0.15.

    Returns:
        rhythm_status (str):            "Regular" or "Irregular" based on threshold.
    """

    # Check threshold and classify result 
    std_dev = np.std(rr_intervals)
    if std_dev <= threshold:
        return "Regular"
    else:
        return "Irregular"

def analyze_st_segment(ecg_signal, r_peak_indices, sampling_rate=1000):
    """ Analyze the ST-segment for changes.

    Args:
        ecg_signal (array-like):        The ECG signal.
        r_peak_indices (array-like):    Indices of R-peaks.
        sampling_rate (int, optional):  Sampling rate in Hz. Default is 1000.

    Returns:
        st_segment_changes (str):       "Normal" or "Abnormal" based on ST-segment analysis.
    """
    st_segment_duration = int(0.08 * sampling_rate)  # Typically, the ST-segment is about 80 ms long
    t_segment_start = int(0.2 * sampling_rate)  # T-segment usually starts around 200 ms after the R-peak

    # Find ST and TP segments
    st_segments = [ecg_signal[r_peak + t_segment_start:r_peak + t_segment_start + st_segment_duration]
                   for r_peak in r_peak_indices]
    
    tp_segments = [ecg_signal[r_peak - st_segment_duration:r_peak]
                   for r_peak in r_peak_indices]

    # Find ST baseline over all 
    st_baseline = np.mean(tp_segments)
    st_amplitudes = [np.mean(st_segment) - st_baseline for st_segment in st_segments]
    
    # Check ST amplitude threshold and return status
    for st_amplitude in st_amplitudes:
        if abs(st_amplitude) > 0.1:  # Adjust this threshold as needed
            return "Abnormal"
    
    return "Normal"

def analyze_t_wave(ecg_signal, threshold=0.1):
    """ Analyze T-wave morphology for abnormalities.

    Args:
        ecg_signal (array-like):        The ECG signal.
        threshold (float, optional):    Threshold for T-wave analysis. Default is 0.1.

    Returns:
        t_wave_status (str):            "Normal" or "Abnormal" based on T-wave analysis.
    """
    t_wave_start = int(0.35 * len(ecg_signal))  # Assume T-wave starts approximately 350 ms into the ECG
    t_wave_duration = int(0.25 * len(ecg_signal))  # T-wave duration is typically about 250 ms

    t_wave_amplitude = np.max(ecg_signal[t_wave_start:t_wave_start + t_wave_duration]) - np.min(ecg_signal[t_wave_start:t_wave_start + t_wave_duration])

    # Check average T-wave threshold and classify result 
    if t_wave_amplitude < threshold:
        return "Abnormal"

    return "Normal"

def analyze_pr_interval(rr_intervals, sampling_rate =1000, threshold=0.2):
    """ Analyze the P-Q interval for atrioventricular conduction.

    Args:
        rr_intervals (array-like):      RR intervals.
        sampling_rate:                  Sampling frequency
        p_peak_indices:                 P-peaks (self-annotated) 
        qrs_peak_indices:               QRS-peaks (self-annotated)
        threshold (float, optional):    Threshold for P-Q interval analysis. Default is 0.2.

    Returns:
        pr_interval_status (str):       "Normal" or "Abnormal" based on P-Q interval analysis.
    """
    # Find P-peaks (search in an [Rpeak-X] ms window: BEFORE the R-peaks)
    p_peak_search_window = 0.04 * 1000  # 40 ms search window (adjust as needed)
    p_peak_indices = []

    for r_peak in r_peak_indices:
        # Search for P-peaks in the search window before the R-peak
        search_start = max(0, r_peak - p_peak_search_window)
        search_end = r_peak
        p_peak, _ = find_peaks(ecg_data[search_start:search_end])
        
        if len(p_peak) > 0:
            p_peak_indices.append(search_start + p_peak[0])

    # Find QRS peaks (search in [Rpeak+X] ms window: AFTER the R-peaks)
    qrs_peak_search_window = 0.1 * 1000  # 100 ms search window (adjust as needed)
    qrs_peak_indices = []

    for r_peak in r_peak_indices:
        # Search for QRS peaks in the search window after the R-peak
        search_start = r_peak
        search_end = r_peak + qrs_peak_search_window
        qrs_peak, _ = find_peaks(ecg_data[search_start:search_end])
    
    if len(qrs_peak) > 0:
        qrs_peak_indices.append(search_start + qrs_peak[0])
    
    # Calculate PR intervals
    pr_intervals = [(qrs_peak - p_peak) / sampling_rate for p_peak, qrs_peak in zip(p_peak_indices, qrs_peak_indices)]

    # Check average PR interval length and classify result 
    mean_pr_interval = np.mean(pr_intervals)
    if abs(mean_pr_interval - 0.2) > 0.04:  # Assuming a normal P-Q interval is around 200 ms
        return "Abnormal"
    
    return "Normal"

