from numpy import floating
import matplotlib.pyplot as plt
from spectrogram_func import *
import time

audio_startstop = [0, 0.1]
filename = 'two_channel_test.wav'

sample_rate, samples, audio_length, time_array = readFile(filename, audio_startstop)
# print(samples[0])
# print(samples.shape)
# print(samples.shape[0])
runtimes = []

for i in range(500):
    start = time.time()
    floating_point_amplitudes, downsampled_amps = makeAmplitudeGraph(time_array, samples, audio_startstop, filename)
    end = time.time()
    time_elapsed = end - start
    runtimes.append(time_elapsed)

# print(floating_point_amplitudes[-100:])
# print(downsampled_amps[-20:])
x1 = np.arange(0,100)
x2 = np.arange(0,100, 5)
plt.subplot(2,1,2)
plt.plot(x1, floating_point_amplitudes[-100:])
plt.plot(x2, downsampled_amps[-20:])

print(sum(runtimes) / len(runtimes))
