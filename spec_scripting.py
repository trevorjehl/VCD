from spectrogram_func import *

sample_rate, samples, floating_point_amplitudes, audio_length, time_array = readFile('two_channel_test.wav', [0,0.1])
print(samples[0])
print(samples.shape)
print(samples.shape[0])