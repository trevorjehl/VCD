"""
2022 Trevor Jehl, CNMC

Spectrogram generation script for audio sample visualization. Takes in a mono wav file,
generates a spectrographic view of file
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
from more_itertools import sample
from scipy.io import wavfile
from scipy import signal
import numpy as np

# Modify default matplotlib behavior.
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (9, 7)

sound_start = 0
sound_end = None

min_freq = 0
max_freq = 8000

# Read relevant wav file, generating two elements: the Sample Rate (fs) and the data (samples)
sample_rate, samples = wavfile.read('orchestra.wav')

# Convert the sound samples to floating point values ranging from -1 to 1
floating_point = samples / max(samples)

audio_length = samples.shape[0] / sample_rate

time = (np.arange(samples.shape[0]) / samples.shape[0]) * audio_length

if sound_end == None:
    sound_end = audio_length

# plt.subplot(2,1,1)
# plt.ylabel('Amplitude')
# plt.plot(time, floating_point)
# plt.xlim([sound_start, sound_end])

# Compute a spectrogram with consecutive Fourier transforms.
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg = 2048)

# plt.subplot(2,1,2)

# Log calculatio accounts for data scaling
plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), cmap='jet')

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.xlim([sound_start, sound_end])
plt.ylim([min_freq, max_freq])

plt.show()