import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pywt
import math
import scipy
import PyWavelet as pywt


def swtDenoise(signal, waveletChoose = 'db', orderChoose = 4, levelChoose = 4, setThreshold = 0):
    """ Denoise the ECG signal using the Stationary Wavelet Transform (SWT).

    Args:
        signal (array-like):                        The ECG signal.
        waveletChoose (str, optional):              The choice of wavelet for SWT. Default is the daubchies wavelet'db'.
                                                    other options - Symlet 'sym', Haar 'haar' etc. 
        orderChoose (int, optional):                The order of the selected wavelet. Default is 4.
        levelChoose (int, optional):                The number of decomposition levels for SWT. Default is 4.
        setThreshold (float, optional):             The noise threshold for coefficient thresholding. Default is 0.

    Returns:
        denoised_ecg (array):                       The denoised ECG signal after SWT.
    """

    # Construct the input to the choice of wavelet with order
    waveletOrder = waveletChoose + str(orderChoose)

    # Do the DWT transform
    if levelChoose == 1:
        cApproximate, cDetailed = pywt.dwt(signal, waveletOrder)
    else:
        wv = pywt.Wavelet(waveletOrder)
        multilevelCoefficients = pywt.wavedec(signal, waveletOrder, level=levelChoose)

    # Declare wavelet to the library
    wv = pywt.Wavelet(waveletOrder)

    # Use thresholding to isolate approx. coefficients & reconstruct
    if levelChoose == 1:
        # Set the detailed coefficients above the desired noise threshold to the desired value
        for k in range(0, len(cDetailed) - 1):
            if abs(cDetailed[k]) >= setThreshold:
                cDetailed[k] = 0

        # Reconstruct using the noise thresholded coefficients
        denoised_ecg = pywt.idwt(cApproximate, cDetailed, waveletOrder, mode='constant')

    else:
        # Set the detailed coefficients at the nth level of the transform that are above the threshold to the desired value (0 here)
        cDetailed = multilevelCoefficients[1]
        
        for k in range(0, len(cDetailed) - 1):
            if abs(cDetailed[k]) >= setThreshold:
                cDetailed[k] = 0
        
        multilevelCoefficients[1] = cDetailed

        # Reconstruct using the noise thresholded coefficients
        denoised_ecg = pywt.waverec(multilevelCoefficients, wv)
    
    return denoised_ecg


def calculateSTDev_SNR(arr, axis=0, ddof=0):
    """ Calculate the Signal-to-Noise Ratio (SNR) based on the standard deviation.

    Args:
        arr (array-like):                           The input data for which SNR is calculated.
        axis (int, optional):                       The axis along which to calculate the mean and standard deviation. Default is 0.
        ddof (int, optional):                       The delta degrees of freedom in standard deviation calculation. Default is 0.

    Returns:
        snr (array):                                The Signal-to-Noise Ratio (SNR) based on standard deviation.
    """

    arr = np.asanyarray(arr)
    m = arr.mean(axis)
    sd = arr.std(axis=axis, ddof=ddof)

    # [Optional] Calculate SNR at peaks
    snrAtPeaks = 10 * np.log10(np.sum(signal[peaks] ** 2) / np.sum((signal - denoised_ecg) ** 2))

    return np.where(sd == 0, 0, m / sd)


def calulatePSD_SNR(signal, denoised_ecg, fs):
    """ Calculate the Signal-to-Noise Ratio (SNR) based on Power Spectral Density (PSD).

    Args:
        signal (array-like):                        The original ECG signal.
        denoised_ecg (array-like):                  The denoised ECG signal.
        fs (float):                                 The sampling frequency in Hz.

    Returns:
        snrCal (float):                             The Signal-to-Noise Ratio (SNR) calculated from PSD.
    """

    # Find PSD > SNR etc.
    (f_L, Sig) = scipy.signal.welch(signal, fs)

    # Removing the few [5 samples] from the beginning and end to remove transitional noise
    (f_L, Noise) = scipy.signal.welch(denoised_ecg[5: len(denoised_ecg) - 5], fs)  

    # absSignalPower = np.abs(sum(Sig))**2
    # absNoisePower = np.abs(sum(Noise))**2
    signalPower = sum(Sig)
    noisePower = sum(Noise)
    print('Signal power' + str(round(signalPower, 4)) + ', Noise: ' + str(round(noisePower, 4)))
    snrCal = 20 * math.log(signalPower / noisePower, 2)

    return snrCal


def calculateGraph_SNR(signal, denoised_ecg):
    """     Calculate the Signal-to-Noise Ratio (SNR) using the PSD function from the matplotlib library.

    Args:
        signal (array-like):                        The original ECG signal.
        denoised_ecg (array-like):                  The denoised ECG signal.

    Returns:
        snrCal (float):                             The Signal-to-Noise Ratio (SNR) calculated from the matplotlib PSD.
    """

    # Use matplotlib PSD
    frequencies, psd_signal = plt.psd(signal, NFFT=1000, Fs=1000, noverlap=0)
    _, psd_noise = plt.psd(signal-denoised_ecg, NFFT=1000, Fs=1000, noverlap=0)

    # Calculate and pass SNR
    snrCal = 20 * math.log(psd_signal / psd_noise, 2)

    return snrCal