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
from scipy.io import wavfile
from scipy import signal
from scipy.signal import butter, sosfilt
import numpy as np
# Modify default matplotlib behavior.
plt.rcParams['figure.dpi'] = 100

# Number of spectral peaks to be graphed
N_SPECTRAL_PEAKS = 4
# Order # of butterworth bandpass filter
N_BUTTER_PASS = 5
# Order of downsampling
DOWNSAMPLE_FACTOR = 10

def readFile(filename, audio_startstop):
    """
    Using a file path, opens a wav file into an array.
    Returns the raw audio information.
    """
    # Sample_rate = the sampling rate of the wav file
    # samples = the displacement at a time
    sample_rate, samples = wavfile.read(filename)

    # If the passed in audio file is stereo, use
    # the audio from only one channel.
    if len(np.shape(samples)) != 1:
        samples = samples[0: ,1]

    # audio_length is the length of the audio file
    audio_length = samples.shape[0] / sample_rate
    
    # If an ending time is passed in, use that time; otherwise use the rest of the audio file
    if not audio_startstop[1] == 'None' and not audio_startstop[1] == None:
        audio_startstop[1] = float(audio_startstop[1])
    else:
        audio_startstop[1] = audio_length

    # time_array = array of time values for each sample (converts 
    # file from sample number in x-axis to time [s])
    time_array = (np.arange(samples.shape[0]) / samples.shape[0]) * audio_length

    return sample_rate, samples, audio_length, time_array, audio_startstop

def downSample(x, y):
    """
    Given an arbitrary set of (x,y) coordinates, downsample
    the given information while preserving the scale of the x-axis
    information (e.x. time).
    """
    # Downsample the signal after applying an anti-aliasing filter.
    downsampled_y = signal.decimate(y, DOWNSAMPLE_FACTOR)
    # Downsample the x-axis by simply choosing every DOWNSAMPLE_FACTOR instance
    downsampled_x = x[::DOWNSAMPLE_FACTOR]

    return downsampled_x, downsampled_y


def butterBandpass(samples, audio_freqs, sample_rate):
    """
    Given an opened wav file, implement butterworth band-pass
    filtering according to the *lowcut* & *highcut* variables.
    Returns filtered version of the passed in *samples* var.
    """
    # Calculate Nyquist frequency
    nyq = 0.5 * sample_rate

    # Calculate low & high cuts with nyquist freq
    low = audio_freqs[0] / nyq
    high = audio_freqs[1] / nyq

    # Calculate second-order sections representation of the IIR butter filter.
    sos = butter(N_BUTTER_PASS, [low, high], analog=False, btype='band', output='sos')

    # Filter data along one dimension using cascaded second-order sections.
    y = sosfilt(sos, samples)
    
    return y


def spectralAnalysis(samples, sample_rate: int):
    """
    After being passed in sample (amplitude information) and a sample rate (sample
    frequecy), completes a FFT analysis passing the information from time domain to the
    frequency domain.
    """
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, 
        nperseg = 4096,
        noverlap = 4096 // 4,
        nfft = 4096*1, 
        window = 'hamming')
    
    return frequencies, times, spectrogram


def findPeaksAtTime(spectrogram, frequencies):
    """
    Assuming a slice of spectrogram has been passed in
    (i.e. spectrogram[:, iterable]), return the (x,y) coordinates
    (x = frequency, y = intensity) of the peaks of the slice of time.
    """
    # Find peaks using scipy peak finding algorythym
    # peak-finding sensitivity can be adjusted using the prominence value
    peaks = signal.find_peaks(spectrogram, prominence=1000)

    # Remove the dict from peaks list
    peaks = peaks[0]
    
    peak_coordinates = []
    for peak in peaks:
        # Consider the xy coordinates in the frequency/intensity axes
        x_val = frequencies[peak]
        y_val = spectrogram[peak]
        
        peak_coordinates.append((x_val, y_val))

    # Select only the *n* largest peaks to return
    sorted_coords = sorted(peak_coordinates, reverse = True, key=lambda coords: coords[1])
    sorted_coords = sorted_coords[:N_SPECTRAL_PEAKS]

    return sorted_coords


def makeAmplitudeGraph(time_array, samples, audio_startstop, filename):
    """
    Using opened .wav file, plots the sound amplitude with respect to time,
    limiting the x-axis using passed in parameters sound_start & sound_end.
    """

    # floating_point converts the sound amplitude to 
    # a range from -1:1 for graphing convenience
    floating_point_amplitudes = samples / max([num for num in samples])

    # Remove some of the amplitude data for graphing (easier to graph)
    downsampled_time, downsampled_amps = downSample(time_array, floating_point_amplitudes)

    # Select the top plot.
    plt.subplot(2, 1, 1)
    # Plot & label amplitude data
    plt.plot(downsampled_time, downsampled_amps)
    plt.ylabel('Amplitude')
    plt.xlim(audio_startstop[0], audio_startstop[1])

    # Title the graph using the file name,
    # not the file path (if applicable)
    filename = filename.split('/')
    filename = filename[-1]
    plt.title(f'{filename} Sound Analysis')


def makeSpectrogram(times: np.ndarray, frequencies, spectrogram: np.ndarray, audio_startstop: list, audio_freqs):
    """
    After spectral analysis is performed, this function takes that 
    information and plots it, limiting the axes using passed in 
    parameters sound_start, sound_end, min_freq, and max_freq.
    """
    plt.subplot(2,1,2)
    # Create spectrogram
    
    spectrogram = 10*np.log10(spectrogram) #account for dB scaling
    plt.pcolormesh(times, frequencies, spectrogram, cmap='magma', shading='auto')

    # Stylize graphs
    plt.ylabel('Frequency [Hz]')
    
    plt.yscale('log')
    plt.xlabel('Time [sec]')
    plt.xlim(audio_startstop[0], audio_startstop[1])
    plt.ylim(audio_freqs[0], audio_freqs[1])


def graphSpectralPeaks(spectrogram: np.ndarray, frequencies: np.ndarray, audio_length: float):
    """
    Given the full spectrogram array, plot N_SPECTRAL_PEAKS points vertically
    along each horizontal 'slice' of the spectrogram.
    """
    # Selet the second plot
    plt.subplot(2,1,2)

    for i in range(spectrogram.shape[1]):
        # For each iteration, consider a vertical slice of the spectrogram
        working_spectrogram = spectrogram[:,i]
        # For each slice, find the spectral peaks
        sorted_coords = findPeaksAtTime(working_spectrogram, frequencies)

        # Convert the given xy axes (frequency/intensity) to the time/frequency axes (i.e. for spectrogram)
        y_coords = [tup[0] for tup in sorted_coords]
        x_coords = [i * (audio_length / spectrogram.shape[1]) for _ in range(len(y_coords))]

        plt.plot(x_coords, y_coords,
            marker="o", 
            markersize=3,
            markeredgecolor="green",
            markerfacecolor="green",
            linestyle='None',)


def doAnalysis(filename: str, audio_startstop: list, audio_freqs: list):
    """
    *** For command line usage *** 

    Given a file path, the starting and ending 
    times (in s) to graph of the sound file, and the minimum and maximum
    frequencies to graph, return a 
    """
    sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)

    # Pass commands into butterworth band pass filter
    samples = butterBandpass(samples, audio_freqs, sample_rate)

    # Do spectral analysis on wav file
    frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

    # Make graphs.
    makeAmplitudeGraph(time_array, samples, audio_startstop, filename)
    makeSpectrogram(times, frequencies, spectrogram, audio_startstop, audio_freqs)
    graphSpectralPeaks(spectrogram, frequencies, audio_length)
    

def main():
    args = sys.argv[1:]

    # If the user has provided insufficient command line arguments, raise error
    if len(args) != 5:
        raise Exception("Improper arguments. Must pass in 5 parameters: filename, sound_start, sound_end, min_freq, max_freq.")
    
    # Interpret command line args
    filename = args[0]
    sound_start = float(args[1])
    audio_startstop = [sound_start, args[2]]
    # Frequencies can only be int values
    audio_freqs = [int(args[3]), int(args[4])]

    doAnalysis(filename, audio_startstop, audio_freqs)
    plt.show()

if __name__ == '__main__':
    main()