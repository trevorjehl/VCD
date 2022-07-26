"""
Unit tests for spectrogram_func.py.
"""
import unittest
import numpy as np
from sound_analysis import *

class testSpectrogram(unittest.TestCase):

    def test_file_reading(self):
        # Test correct reading of various time selections inputs w/ sample rate
        self.assertEqual(readFile('two_channel_test.wav', [0, 0.1])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [1, 1.1])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [4, None])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [0, None])[0], 44100)
        self.assertAlmostEqual(readFile('two_channel_test.wav', [1, '1.1'])[4][1], 1.1)

        # Test ability to read sound file length
        self.assertAlmostEqual(readFile('two_channel_test.wav', [0, None])[2], 10.6666667)


    def test_downSample(self):
        x = np.arange(1,30,1)
        y = np.array([0,0,0,0,0,0,0,0,0,0,10,10,10,10,10,10,10,10,10,10,50,50,50,50,50,50,50,50,50,50])
        downsampled_x, downsampled_y = downSample(x,y)
        downsampled_y = [num for num in downsampled_y]
        downsampled_x = [num for num in downsampled_x]

        self.assertTrue(downsampled_y == [-0.5567635698632712, 2.9842633311385063, 32.106209846488376])
        self.assertTrue(downsampled_x == [1, 11,21])
    

    def test_find_peaks(self):
        filename = 'two_channel_test.wav'
        audio_startstop = [1, 1.1]

        sample_rate, samples, audio_length, time_array, audio_startstop = readFile(filename, audio_startstop)

        frequencies, times, spectrogram = spectralAnalysis(samples, sample_rate)

        # Consider only the first slice of spectrogram information
        spectrogram = spectrogram[:,0]

        sorted_coords = findPeaksAtTime(spectrogram, frequencies)
        self.assertEqual(type(sorted_coords), list)
        self.assertEqual(type(sorted_coords[0]), tuple)
        self.assertTrue(sorted_coords[0][0] == 1173.5595703125)
        self.assertAlmostEqual(sorted_coords[0][1], 19931.395, 3)


if __name__ == '__main__':
    unittest.main()