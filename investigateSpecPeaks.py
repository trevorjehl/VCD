from numpy import floating
import matplotlib.pyplot as plt
from spectrogram_func import *
from scipy import signal
import numpy as np
import time

filename = 'two_channel_test.wav'
audio_startstop = [1, 1.1]
audio_freqs = [100, 2000]

sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)
y = butter_bandpass(samples, audio_freqs, sample_rate, order=5)

frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

peaks = signal.find_peaks(spectrogram[: , 0], distance = 30)

peaks = np.asarray(peaks)
peaks = peaks[:-1]

x_vals = []
y_vals = []
spec_list = list(spectrogram[:, 0])
freq_list = list(frequencies)

for peak in peaks[0]:
    curr_x_val = frequencies[peak]
    y_val = spec_list[peak]
    
    x_vals.append(curr_x_val)
    y_vals.append(y_val)

plt.plot(frequencies, spectrogram[: , 0])
plt.plot(x_vals, y_vals, 'r', marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red", linestyle='None',)
plt.xlim([0,3000])
plt.show()
