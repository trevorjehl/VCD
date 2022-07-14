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
y = butter_bandpass(samples, audio_freqs, sample_rate, order=5)

frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)
spectrogram = spectrogram[:,0]

# peaks = signal.find_peaks(spectrogram, prominence=1000)

# peaks = peaks[0]

# peak_coordinates = []
# spec_list = list(spectrogram)

# for peak in peaks:
#     x_val = frequencies[peak]
#     y_val = spec_list[peak]
    
#     peak_coordinates.append((x_val, y_val))

# sorted_coords = sorted(peak_coordinates, reverse = True, key=lambda coords: coords[1])
# sorted_coords = sorted_coords[:4]

# print(sorted_coords)
# x_coords = [tup[0] for tup in sorted_coords]
# y_coords = [tup[1] for tup in sorted_coords]

# plt.plot(frequencies, spectrogram)
# plt.plot(x_coords, y_coords, 'r', marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red", linestyle='None',)
# plt.xlim([0,3000])
# plt.show()



sorted_coords = findPeaksAtTime(spectrogram, frequencies)

x_coords = [tup[0] for tup in sorted_coords]
y_coords = [tup[1] for tup in sorted_coords]

plt.plot(frequencies, spectrogram)
plt.plot(x_coords, y_coords, 'r', marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red", linestyle='None',)
plt.xlim([0,3000])
plt.show()
