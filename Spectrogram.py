"""
2022 Trevor Jehl, CNMC

Spectrogram generation script for audio sample visualization. Takes in a wav file,
generates a spectrographic ciew of.
"""
from email.mime import audio
import sys
import matplotlib.pyplot as plt
from more_itertools import sample
from scipy.io import wavfile
from scipy import signal
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

# Import relevant wav file, generating two elements: the Sample Rate (fs) and the data (samples)
sample_rate, samples = wavfile.read('piano_sampleM.wav')

audio_length = len(samples) / sample_rate
print(audio_length)
# # Compute a spectrogram with consecutive Fourier transforms.
# frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=12288)

# plt.pcolormesh(times, frequencies, spectrogram, cmap='jet')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.ylim([0, 1000])

# plt.show()






# # Read the wav file (mono)
# samplingFrequency, signalData = wavfile.read('piano_sample.wav')

# # print(samplingFrequency, signalData)

# # Plot the signal read from wav file
# plt.subplot(211)
# plt.title('Spectrogram of a wav file with piano music')

# plt.plot(signalData)
# plt.xlabel('Sample')
# plt.ylabel('Amplitude')

# # plt.subplot(212)
# # plt.specgram(signalData,Fs=samplingFrequency)
# # plt.xlabel('Time')
# # plt.ylabel('Frequency')

# plt.show()











# def main():

#     args = sys.argv[1:]

#     # if len(args) == 1:
#     #     # filename
#     #     counts = read_counts(args[0])
#     #     print_counts(counts)

#     # if len(args) == 3 and args[0] == '-top':
#     #     # -top n filename
#     #     n = int(args[1])
#     #     counts = read_counts(args[2])
#     #     print_top(counts, n)

# if __name__ == '__main__':
#     main()