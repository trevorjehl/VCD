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
    """
    Given a file path & sample start and stop
    times (in sample #), open the file and
    return the breathing force data.
    """
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


def calcDifferential(vals):
    """
    Given breathing vals, calculate the
     nth order differential of the data.
    """
    diff = np.diff(vals, n = 1)
    return diff


def graphResp(vals, running, diff):
    """
    Given all the calculated data, 
    graph and label the data.
    """
    time_list = []
    for i in range(len(vals)): 
        time = i / HZ
        time_list.append(time)

    diff_time = time_list[1:]

    plt.plot(time_list, vals, label = 'Raw Data')
    plt.plot(time_list, running, label = f'Running Average (window size = {RUNNING_WINDOW_SIZE})')
    plt.plot(diff_time, diff, 'r', label = 'Running Average Derivative')

    # Fill above & below differential data to signal
    # different breathing phases.
    plt.fill_between(
        x = diff_time, 
        y1 = diff, 
        where = diff >= 0,
        color = "g",
        alpha = 0.2)
    
    plt.fill_between(
        x = diff_time, 
        y1 = diff, 
        where = diff <= 0,
        color = "b",
        alpha = 0.2)

    plt.title('Respiration Phase Analysis: Inspiration vs Expiration')
    plt.xlabel('Time [s]')
    # plt.ylabel('Force')
    plt.legend()


def main():
    # Interpret command line args
    args = sys.argv[1:]
    filename = args[0]
    startstop = (int(args[1]), int(args[2]))
    vals = readRespData(filename, startstop)
    
    running = runningMean(vals)
    diff = calcDifferential(running)
    graphResp(vals, running, diff)
    plt.show()


if __name__ == '__main__':
    main()