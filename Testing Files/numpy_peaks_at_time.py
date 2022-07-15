"""
This function is used to develop the peak finding algorythim for a spectrogram.
It evaluates the peak frequencies at a moment in time from a sample wav file.
"""

import matplotlib.pyplot as plt
from spectrogram_func import *
from scipy import signal
import numpy as np

filename = 'two_channel_test.wav'
audio_startstop = [1, 1.1]
audio_freqs = [100, 2000]

sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)

frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

# Consider only the first slice of spectrogram information
spectrogram = spectrogram[:,0]

# Find peaks using scipy peak finding algorythym
peaks = signal.find_peaks(spectrogram, prominence=1000)

# Remove the dict from peaks
peaks = peaks[0]
print('peaks type', type(peaks), peaks.shape)
print('spectrogram type', type(spectrogram), spectrogram.shape)
print('frequencies type', type(frequencies), frequencies.shape)

# Make the frequency intensity values a python list
spec_list = list(spectrogram)

peak_coordinates = []

for peak in peaks:
    x_val = frequencies[peak]
    y_val = spectrogram[peak]
    
    peak_coordinates.append((x_val, y_val))

sorted_coords = sorted(peak_coordinates, reverse = True, key=lambda coords: coords[1])
sorted_coords = sorted_coords[:N_SPECTRAL_PEAKS]

print(sorted_coords)
x_coords = [tup[0] for tup in sorted_coords]
y_coords = [tup[1] for tup in sorted_coords]

plt.plot(frequencies, spectrogram)
plt.plot(x_coords, y_coords, 'r', marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red", linestyle='None',)

plt.title("Frequency vs. Intesity")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Intensity')
plt.xlim([0,3000])
plt.show()