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
y = butterBandpass(samples, audio_freqs, sample_rate)

frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

# Consider only the first slice of spectrogram information
spectrogram = spectrogram[:,0]

sorted_coords = findPeaksAtTime(spectrogram, frequencies)
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