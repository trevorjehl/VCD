from email.mime import audio
import matplotlib.pyplot as plt
from spectrogram_func import *
from scipy import signal
import numpy as np

filename = 'two_channel_test.wav'
audio_startstop = [0, 10]
audio_freqs = [100, 1000]

doAnalysis(filename, audio_startstop, audio_freqs)

sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)

# Do spectral analysis on wav file
frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

# Make graphs.
makeAmplitudeGraph(time_array, samples, audio_startstop, filename)
makeSpectrogram(times, frequencies, spectrogram, audio_startstop, audio_freqs)

plt.subplot(2,1,2)
for i in range(spectrogram.shape[1]):
    working_spectrogram = spectrogram[:,i]
    sorted_coords = findPeaksAtTime(working_spectrogram, frequencies)

    y_coords = [tup[0] for tup in sorted_coords]
    x_coords = [i * (audio_length / spectrogram.shape[1]) for x in range(len(y_coords))]

    plt.plot(x_coords, y_coords, marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green", linestyle='None',)

print(type(times))

plt.ylim(audio_freqs[0], audio_freqs[1])
plt.show()
