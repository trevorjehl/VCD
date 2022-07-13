import unittest
from matplotlib.testing.decorators import image_comparison
from spectrogram_func import *

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

    # def test_amplitude_graph(self):
    #     samples = np.array([0,1000,0,0,-500,0,1000,0,0,-500,0,1000,0,0,-500,0,1000,0,0,-500,0,1000,0,0,-500,0,1000,0,0,-500,])
    #     time_array = np.arange(0,len(samples) * 0.2, 0.2)
    #     audio_startstop = [0, len(samples) * 0.2]
    #     filename = 'test_graph'
    #     makeAmplitudeGraph(time_array, samples, audio_startstop, filename)
    #     x_plot, yplot = plt.get_
    #     np.testing.assert_array_equal(yplot,)


if __name__ == '__main__':
    unittest.main()

