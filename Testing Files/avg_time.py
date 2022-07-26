"""
Use this file to calculate mean real time 
that spectrogram_func takes to process a file
or list of files. If .wav is in local dir, only
**filename** is needed, otherwise supply path.
Make sure to remove plt.show() as needed.
"""

import time
from sound_analysis import *

filenames = ['/Users/trevorj/Documents/GitHub/VCD/Test Audio/two_channel_test.wav', 
            '/Users/trevorj/Downloads/long_wav.wav']

num_iterations = 10
time_taken = {}
mean_time_taken = {}

for file in filenames:
    time_taken[file] = []

    for i in range(num_iterations):

        start = time.time()
        doAnalysis(file, [0, None], [100, 2000])
        end = time.time()
        
        dur = end - start

        time_taken[file].append(dur)
    
    mean_time_taken[file] = sum(time_taken[file]) / num_iterations

print(mean_time_taken)

