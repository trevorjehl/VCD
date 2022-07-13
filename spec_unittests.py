import unittest
from spectrogram_func import *

class testSpectrogram(unittest.TestCase):

    def test_file_reading(self):
        # Test correct reading of various time selections w/ sample rate
        self.assertEqual(readFile('two_channel_test.wav', [0, 0.1])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [1, 1.1])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [4, None])[0], 44100)
        self.assertEqual(readFile('two_channel_test.wav', [0, None])[0], 44100)

        self.assertAlmostEqual(readFile('two_channel_test.wav', [0, None])[2], 10.6666667)

if __name__ == '__main__':
    unittest.main()

