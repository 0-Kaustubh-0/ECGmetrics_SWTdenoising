# Project:
#   1) Denoise ECG data with Stationary Wavelet Analysis
#   2) Analyze the ECG data and obtain several metrics   
#
# Read README file for more information
# 
# Author: Kaustubh Sinha, Jun 2023

# Import dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pywt
import math
import scipy

# Import custom function libraries
import ecgDenoising as ecgDen
import ecgAnalyses as ecAna


# Read data (change filename or reading function here)
# For excel, use: pd.read_excel()
dataTable = pd.read_csv('ptbdb_normal.csv')
[sets, nSamples] = dataTable.shape
print('Signal sets in table, ' + str(dataTable.shape))

# If you know the sampling frequency for your signal, write it here (fs = 10000 which is a sampling frequency of 10kHz)
# Sampling frequency and time-axis
fs = 125
timeAxis = np.linspace(1, nSamples / fs, nSamples)

# Calculate SNR
# snr = calculateSTDev_SNR(np.array(dataTable))     # 1) Std deviation of the signal method [Rough statistical estimate] 
# snr = calculatePSD_SNR(np.array(dataTable))       # 2) Power Spectral Density method (Signal power :Noise power ratio) [More accurate spectral power estimate] 
# snr = calculateGraph_SNR()                        # 3) Calculate using the PSD function in matplotlib library

# Iterate over each signal in the dataframe
for j in range(0, sets - 1):

    # Option to enable user input for: wavelet families, order, level, noise Threshold
    # waveletChoose = input('Choose a wavelet family for conducting the spectral De-noising')
    # orderChoose = input('Choose the order for spectral De-noising')
    # levelChoose = input('Choose the level for spectral De-noising')
    # setThreshold = input('Enter threshold for De-noising detail coefficients')

    # Load each row in the dataTable dataframe
    signal = dataTable.iloc[j, :]

    waveletChoose = 'db'
    orderChoose = 4
    levelChoose = 8
    setThreshold = 0

    denoised_ecg = swtDenoise(signal, waveletChoose = 'db', orderChoose = 4, levelChoose = 8, setThreshold = 0)

    # Refer to this article for using the PyWavelet SWT function directly (less control)
    # link here once published

    # Find R-peaks in the denoised ECG signal
    rPeaks, _ = eca.find_r_peaks(denoised_ecg, height=0.2, fs)  # Adjust threshold as needed

    # Calculate the heart rate and RR intervals for the given denoised signal data from R-peaks
    HR, RRintervals = eca.calculate_heart_rate(rPeaks, fs)

    # Analyze hear rhythm based on R-R intervals
    HeartRhythmState = eca.analyze_rhythm(RRintervals, threshold=0.15)

    # Calculate ST-segments and anlayze changes
    STsegmentState = eca.analyze_st_segment(denoised_ecg, rPeaks, fs)

    # Analyze T-waves for abnormalities
    TwaveState = eca.analyze_t_wave(denoised_ecg, threshold=0.1)

    # Use P-peaks and QRS intervals to extract the the P-R intervals
    PTintervalState = eca.analyze_pr_interval(RRintervals, fs, threshold=0.2)

    # Display all metrics
    print("Heart rate: ", HR)
    print("Hear rhythm state: ", HeartRhythmState)
    print("ST segment state: ", STsegmentState)
    print("T-Wave state: ", TwaveState)
    print("PT interval state: ", PTintervalState)

    # Choose to plot the raw and denoised ECG signal 
    plotData = 0

    # Plot data 
    if plotData == 1

        # Plot each dataset
        plt.figure(1)  # Create figure window
        plt.subplot(211)
        plt.plot(timeAxis, signal)
        plt.plot(timeAxis, signalReconstructed, color='red')
        plt.title('Signal set:' + str(j + 1) + ', SNR: ' + str(round(snrCal, 4)))
        plt.ylabel('Amplitude [a.u.]')
        plt.tick_params(axis='x', which='minor', pad=10)
        
        # Plot the noise + PSD
        plt.subplot(212)
        plt.plot(timeAxis, signal - signalReconstructed, color='black')
        plt.title('Subtracted noise in the signal' + str(j + 1))
        plt.xlabel('Time [s]')
        plt.ylabel('Noise Amplitude [a.u.]')
        plt.tick_params(axis='x', which='minor', pad=10)
        
        # Create plot
        plt.show()
        plt.tight_layout()
