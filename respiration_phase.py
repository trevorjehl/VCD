"""
This file is designed to take in data about respiration phase
from a force sensitive resistor, process the data, and output 
it so that it can be useful for spectrogram_func.py
"""
import sys
from scipy.ndimage.filters import uniform_filter1d
import numpy as np
import matplotlib.pyplot as plt

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

    time_list = []
    for i in range(len(vals)): 
        time = i / HZ
        time_list.append(time)

    return vals[startstop[0] : startstop[1]], time_list[startstop[0] : startstop[1]]


def runningMean(vals):
    """
    Given the readings from the force sensitive resistor,
    compute a running average to normalize the data.
    Return a list of vals of the same dimension as the
    passed-in list.
    """
    running = uniform_filter1d(vals, size = RUNNING_WINDOW_SIZE)
    return running


def calcDifferential(vals, time_list):
    """
    Given breathing vals, calculate the
     nth order differential of the data.
    """
    diff = np.diff(vals, n = 1)

    # New time array for differential
    diff_time_vals = []
    for i in range(1, len(vals)):
        end = time_list[i]
        start = time_list[i - 1]
        diff_time_vals.append(np.mean(end - start) + start)

    return diff, diff_time_vals


def findRespiratoryPhase(diff, diff_time_vals):
    """
    Given the differential dataset, find the
    x vals where the y vals are >= 0 [inspiration]
    or where the y vals are <= 0 [expiration].
    """
    resp_phase = {'insp' : [], 'exp' : []}
    resp_startstop =  {'insp' : [], 'exp' : []}

    for i, num in enumerate(diff):
        # print(f'i: {i}, num: {num}, time_val: {diff_time_vals[i]}')
        if num > 0:

            if resp_phase['exp']:
                end = resp_phase['exp'][-1]
                start = resp_phase['exp'][0]
                resp_startstop['exp'].append((start, end))
                resp_phase['exp'] = []
            
            x_val = diff_time_vals[i]
            resp_phase['insp'].append(x_val)
        
        if num < 0:

            if resp_phase['insp']:
                end = resp_phase['insp'][-1]
                start = resp_phase['insp'][0]
                resp_startstop['insp'].append((start, end))
                resp_phase['insp'] = []
    
            x_val = diff_time_vals[i]
            resp_phase['exp'].append(x_val)

    print(resp_startstop)

    return resp_phase


def graphResp(vals, running, time_list, diff, diff_time_vals):
    """
    Given all the calculated data, 
    graph and label the data.
    """
    plt.plot(time_list, vals, label = 'Raw Data')
    plt.plot(time_list, running, label = f'Running Average (window size = {RUNNING_WINDOW_SIZE})')
    plt.plot(diff_time_vals, diff, 'r', label = 'Running Average Derivative')

    # Fill above & below differential data to signal
    # different breathing phases.
    plt.fill_between(
        x = diff_time_vals, 
        y1 = diff, 
        where = diff >= 0,
        color = "g",
        alpha = 0.2)
    
    plt.fill_between(
        x = diff_time_vals, 
        y1 = diff, 
        where = diff <= 0,
        color = "b",
        alpha = 0.2)

    plt.title('Respiration Phase Analysis: Inspiration vs Expiration')
    plt.xlabel('Time [s]')
    plt.legend()


def main():
    # Interpret command line args
    args = sys.argv[1:]
    filename = args[0]
    if len(args) > 0:
        startstop = (int(args[1]), int(args[2]))
    
    vals, time_list= readRespData(filename, startstop)
    
    running = runningMean(vals)
    diff, diff_time_vals = calcDifferential(running, time_list)

    findRespiratoryPhase(diff, diff_time_vals)

    graphResp(vals, running, time_list, diff, diff_time_vals)
    plt.show()


if __name__ == '__main__':
    main()