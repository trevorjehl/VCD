"""
2022 Trevor Jehl, CNMC
Date-Created: 07-11-2022

Spectrogram generation script for audio sample visualization. Takes in a mono wav file,
generates a spectrographic view of file.

TODO:
    - implement audio playing feature
    - modify FFT implementation depending on granularity of selected timescale

##########################################################################################
To use the program, navigate to the relevant directory in terminal. Use syntax as follows:

>>> python3 spectrogram_func.py filename.wav starting_time ending_time minimum_frequency maximum_frequency

    - starting_time = Starting time (in s) to graph (i.e. minimum x-axis value)
    - ending_time = Ending time (in s) to graph (i.e. maximum x-axis value). If ending time == "None", 
the program will default to the audio file's duration.
    - minimum_frequency = Lowest frequency (Hz) to show on graph (i.e. minimum y-axis value)
    - maximum_frequency = Highest frequency (Hz) to show on graph (i.e. maximum y-axis value)
"""
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import numpy as np
# Modify default matplotlib behavior.
plt.rcParams['figure.dpi'] = 100


def readFile(filename):
    """
    Opens wav file, returns sample_rate, samples, floating_point, audio_length, time_array.
    
    Sample_rate = the sampling rate of the wav file
    samples = the value of the sound at a sample
    floating_point = converts the sound amplitude to a range from -1:1 for graphing convenience
    audio_length = length of the audio file
    time_array = array of time values for each second (converts file from sample rate in x-axis to time in s)
    """
    print("Reading file...")

    sample_rate, samples = wavfile.read(filename)

    # If the passed in audio file is stereo, use
    # the audio from only one channel.
    if len(np.shape(samples)) != 1:
        samples = samples[0: ,1]

    floating_point = samples / max(samples)
    audio_length = samples.shape[0] / sample_rate
    time_array = (np.arange(samples.shape[0]) / samples.shape[0]) * audio_length

    return sample_rate, samples, floating_point, audio_length, time_array


def spectralAnalysis(samples, sample_rate):
    """
    After being passed in sample (amplitude information) and a sample rate (sample
    frequecy), completes a FFT analysis passing the information from time domain to the
    frequency domain.
    """
    print("Doing spectral analysis...")
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    
    return frequencies, times, spectrogram


def makeAmplitudeGraph(time_array, floating_point, sound_start, sound_end, filename):
    """
    Using opened .wav file, plots the sound amplitude with respect to time,
    limiting the x-axis using passed in parameters sound_start & sound_end.
    """
    print("Making amplitude graph...")
    plt.subplot(2, 1, 1)
    plt.ylabel('Amplitude')
    plt.plot(time_array, floating_point)
    plt.xlim(sound_start, sound_end)
    plt.title(f'{filename} Sound Analysis')


def makeSpectrogram(times, frequencies, spectrogram, sound_start, sound_end, min_freq, max_freq):
    """
    After spectral analysis is performed, this function takes that 
    information and plots it, limiting the axes using passed in 
    parameters sound_start, sound_end, min_freq, and max_freq.
    """
    print("Making spectrogram...")
    
    # Tell matplot that the following code refers to the second plot.
    plt.subplot(2, 1, 2)

    plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), cmap='jet')

    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.xlim(sound_start, sound_end)
    plt.ylim([min_freq, max_freq])
    plt.show()


def doAnalysis(filename, sound_start, sound_end, min_freq, max_freq):
    print("Analyzing file...")
    sample_rate, samples, floating_point, audio_length, time_array = readFile(filename)

    if sound_end == None:
        sound_end = audio_length

    frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)
    makeAmplitudeGraph(time_array, floating_point, sound_start, sound_end, filename)
    makeSpectrogram(times, frequencies, spectrogram, sound_start, sound_end, min_freq, max_freq)
    plt.show()
    

def main():
    print('Main running.')
    args = sys.argv[1:]

    if len(args) != 5:
        raise Exception("Imporper arguments. Must pass in 5 parameters: filename, sound_start, sound_end, min_freq, max_freq.")
    
    filename = args[0]
    sound_start = float(args[1])
    
    if args[2] == "None":
        sound_end = None
    else:
        sound_end = float(args[2])
    
    min_freq = int(args[3])
    max_freq = int(args[4])

    doAnalysis(filename, sound_start, sound_end, min_freq, max_freq)


if __name__ == '__main__':
    main()