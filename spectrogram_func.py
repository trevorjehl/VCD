"""
2022 Trevor Jehl, CNMC
Date-Created: 07-11-2022

Spectrogram generation script for audio sample visualization. Takes in a mono wav file,
generates a spectrographic view of file.

TODO:
    - implement audio playing feature
    - modify FFT implementation depending on granularity of selected timescale
"""

import sys
import matplotlib.pyplot as plt
# from more_itertools import sample
from scipy.io import wavfile
from scipy import signal
from scipy.signal import butter, sosfilt
import numpy as np
# Modify default matplotlib behavior.
plt.rcParams['figure.dpi'] = 100


def readFile(filename, audio_startstop):
    """
    Opens wav file, returns sample_rate, samples, floating_point, audio_length, time_array.
    """
    print("Reading file...")

    # Sample_rate = the sampling rate of the wav file
    # samples = the value of the sound at a sample
    sample_rate, samples = wavfile.read(filename)

    # If the passed in audio file is stereo, use
    # the audio from only one channel.
    if len(np.shape(samples)) != 1:
        samples = samples[0: ,1]

    # audio_length is the length of the audio file
    audio_length = samples.shape[0] / sample_rate

    # If an ending time is passed in, use that time; otherwise use the rest of the audio file
    audio_startstop[1] = float(audio_startstop[1]) if str(audio_startstop[1]).isdigit() else audio_length

    # time_array = array of time values for each sample (converts 
    # file from sample number in x-axis to time [s])
    time_array = (np.arange(samples.shape[0]) / samples.shape[0]) * audio_length

    return sample_rate, samples, audio_length, time_array


def butter_bandpass(samples, audio_freqs, sample_rate, order=5):
    """
    Given an opened wav file, implement butterworth band-pass
    filtering according to the *lowcut* & *highcut* variables.
    Returns filtered version of the passed in *samples* var.
    """
    # Calculate Nyquist frequency
    nyq = 0.5 * sample_rate

    low = audio_freqs[0] / nyq
    high = audio_freqs[1] / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')

    # Filter data along one dimension using cascaded second-order sections.
    y = sosfilt(sos, samples)
    
    return y


def spectralAnalysis(samples, sample_rate):
    """
    After being passed in sample (amplitude information) and a sample rate (sample
    frequecy), completes a FFT analysis passing the information from time domain to the
    frequency domain.
    """
    print("Doing spectral analysis...")

    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, 
        nperseg = 4096,
        noverlap = 4096 // 4,
        nfft = 4096*1, 
        window = 'hamming')
    
    return frequencies, times, spectrogram


def makeAmplitudeGraph(time_array, samples, audio_startstop, filename):
    """
    Using opened .wav file, plots the sound amplitude with respect to time,
    limiting the x-axis using passed in parameters sound_start & sound_end.
    """
    print("Making amplitude graph...")

    # floating_point converts the sound amplitude to a range from -1:1 for graphing convenience
    floating_point_amplitudes = samples / max(samples)

    #Select the top plot.
    plt.subplot(2, 1, 1)

    # Plot & label amplitude data
    plt.plot(time_array, floating_point_amplitudes)
    plt.ylabel('Amplitude')
    plt.xlim(audio_startstop[0], audio_startstop[1])
    plt.title(f'{filename} Sound Analysis')


def makeSpectrogram(times, frequencies, spectrogram, audio_startstop, audio_freqs):
    """
    After spectral analysis is performed, this function takes that 
    information and plots it, limiting the axes using passed in 
    parameters sound_start, sound_end, min_freq, and max_freq.
    """
    print("Making spectrogram...")

    plt.subplot(2,1,2)
    # Create spectrogram
    plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), cmap='magma')

    # Stylize graphs
    plt.ylabel('Frequency [Hz]')
    plt.yscale('log')
    plt.xlabel('Time [sec]')
    plt.xlim(audio_startstop[0], audio_startstop[1])
    plt.ylim(audio_freqs[0], audio_freqs[1])
    plt.show()


def doAnalysis(filename, audio_startstop, audio_freqs):
    """
    *** For command line usage *** 

    Given a file path, the starting and ending 
    times (in s) to graph of the sound file, and the minimum and maximum
    frequencies to graph, return a 
    """
    print("Analyzing file...")

    sample_rate, samples, audio_length, time_array = readFile(filename, audio_startstop)

    if audio_startstop[1] == None:
        audio_startstop[1] = audio_length

    # Pass commands into butterworth band pass filter
    samples = butter_bandpass(samples, audio_freqs, sample_rate, 5)

    # Do spectral analysis on wav file
    frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

    # Make graphs.
    makeAmplitudeGraph(time_array, samples, audio_startstop, filename)
    makeSpectrogram(times, frequencies, spectrogram, audio_startstop, audio_freqs)
    

def main():
    print('Main running.')
    args = sys.argv[1:]

    # If the user has provided insufficient command line arguments, raise error
    if len(args) != 5:
        raise Exception("Improper arguments. Must pass in 5 parameters: filename, sound_start, sound_end, min_freq, max_freq.")
    
    filename = args[0]

    #
    sound_start = float(args[1])
    audio_startstop = [sound_start, args[2]]
    
    # Frequencies can only be int values
    audio_freqs = (int(args[3]), int(args[4]))

    doAnalysis(filename, audio_startstop, audio_freqs)


if __name__ == '__main__':
    main()