"""
This function animates the peak finding algorithym across time.
"""

import matplotlib.pyplot as plt
from sound_analysis import *
from scipy import signal
import matplotlib.animation as animation
import numpy as np

filename = 'two_channel_test.wav'
audio_startstop = [1, 1.1]
audio_freqs = [100, 2000]

sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)

frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

for i in range(spectrogram.shape[1]):
    # For each iteration, consider a vertical slice of the spectrogram
    working_spectrogram = spectrogram[:,i]

    # Find peaks using scipy peak finding algorythym
    peaks = signal.find_peaks(working_spectrogram, prominence=1000)

    # Remove the dict from peaks
    peaks = peaks[0]

    # Make the frequency intensity values a python list
    spec_list = list(working_spectrogram)

    peak_coordinates = []

    for peak in peaks:
        x_val = frequencies[peak]
        y_val = working_spectrogram[peak]
        
        peak_coordinates.append((x_val, y_val))

    sorted_coords = sorted(peak_coordinates, reverse = True, key=lambda coords: coords[1])
    sorted_coords = sorted_coords[:N_SPECTRAL_PEAKS]

    x_coords = [tup[0] for tup in sorted_coords]
    y_coords = [tup[1] for tup in sorted_coords]


    plt.title("Frequency vs. Intesity")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Intensity')
    plt.xlim([0,3000])
    plt.ylim([0,40000])

    plt.plot(frequencies, working_spectrogram)
    plt.plot(x_coords, y_coords, 'r', marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red", linestyle='None',)
    plt.pause(0.05)
    plt.clf()

plt.show()