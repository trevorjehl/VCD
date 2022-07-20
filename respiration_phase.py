"""
This file is designed to take in data about respiration phase
from a force sensitive resistor, process the data, and output 
it so that it can be useful for spectrogram_func.py
"""
import sys
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d
import numpy as np

# Approximate sensor readings/s [in Hz]
HZ = 11.705685618729097
# The size of the running average window
RUNNING_WINDOW_SIZE = 15


def readRespData(filename, startstop):
    vals = []
    with open(filename) as f:
        for line in f:
            line = line.split(' ')
            data = int(line[-1])
            vals.append(data)
    return vals[startstop[0] : startstop[1]]


def runningMean(vals):
    """
    Given the readings from the force sensitive resistor,
    compute a running average to normalize the data.
    Return a list of vals of the same dimension as the
    passed-in list.
    """
    running = uniform_filter1d(vals, size = RUNNING_WINDOW_SIZE)
    return running


def graphResp(vals, running):
    time_list = []
    for i in range(len(vals)): 
        time = i / HZ
        time_list.append(time)

    plt.plot(time_list, vals)
    plt.plot(time_list, running)

    plt.xlabel("Time [s]")
    plt.ylabel("Force")


def main():
    # Interpret command line args
    args = sys.argv[1:]
    filename = args[0]
    startstop = (int(args[1]), int(args[2]))
    vals = readRespData(filename, startstop)
    
    running = runningMean(vals)
    graphResp(vals, running)
    plt.show()


if __name__ == '__main__':
    main()