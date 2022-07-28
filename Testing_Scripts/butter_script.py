from numpy import floating
import matplotlib.pyplot as plt
from sound_analysis import *
import time

audio_startstop = [0, 0.1]
audio_freqs = [100,1000]
filename = 'two_channel_test.wav'

sample_rate, samples, audio_length, time_array = readFile(filename, audio_startstop)
y, sos = butterBandpass(samples, audio_freqs, sample_rate, order=5)

plt.plot(y)
plt.show()