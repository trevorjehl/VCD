"""
This file is designed to take in data about respiration phase
from a force sensitive resistor, process the data, and output 
it so that it can be useful for spectrogram_func.py

Created Jul 2022
by Trevor Jehl
"""
import sys
from scipy.ndimage.filters import uniform_filter1d
import numpy as np
import matplotlib.pyplot as plt

# The size of the running average window
RUNNING_WINDOW_SIZE = 15

def calcHz (millis):
    """
    Given the first two lines of the respiration data,
    calculate the sampling frequency in Hz (samples/s).
    """
    # Convert milliseconds to seconds
    seconds = [num / 1000 for num in millis]
    
    hz = len(seconds) / (seconds[1] - seconds[0])
    return hz


def readRespData(filename, startstop):
    """
    Given a file path & sample start and stop
    times (in sample #), open the file and
    return the breathing force data.
    """
    vals = []
    millis = []
    
    # Read FSR data into vals list
    with open(filename) as f:
        for line in f:
            line = line.split(' ')
            data = int(line[-1])
            vals.append(data)
    
    # If millis info is in the .txt file,
    # read the info and calculate samples/s (Hz)
    with open(filename) as f:
        for line in f:
            lst = line.split(';')
            if len(lst) > 1:
                time = float(lst[0])
                millis.append(time)
            else:
                Hz = 11.7
                break
            if len(millis) == 2:
                Hz = calcHz(millis)
                break
    
    # Calculate real time elapsed according to Hz
    time_list = []
    for i in range(len(vals)): 
        time = i / Hz
        time_list.append(time)
    
    return vals, time_list


def runningMean(vals):
    """
    Given the readings from the force sensitive resistor,
    compute a running average to normalize the data.
    Return a list of vals of the same dimension as the
    passed-in list.
    """
    return uniform_filter1d(vals, size = RUNNING_WINDOW_SIZE)


def calcDifferential(vals, time_list):
    """
    Given breathing vals, calculate the
    nth order differential of the data.
    """
    # Calculate the nth order discrete differential of
    # respiration force data
    diff = np.diff(vals, n = 1)

    # New time array for discrete differential array -- taking
    # differential reduces size of array, new x vals are needed
    diff_time_vals = []
    for i in range(1, len(vals)):
        end = time_list[i]
        start = time_list[i - 1]
        diff_time_vals.append(np.mean(end - start) + start)

    return diff, diff_time_vals


def findRespiratoryPhase(diff, diff_time_vals):
    """
    Given the differential dataset, find the
    x vals where the y vals are > 0 [inspiration]
    or where the y vals are < 0 [expiration], return
    a dictionary with a list of tuples that represent
    the start and end of each phase of respiration.
    """
    # A dictionary where all 'insp' data has y>0, 'exp'
    # has y<0
    resp_phase = {'insp' : [], 'exp' : []}

    # Each 'insp' & 'exp' list contains tuples with the start
    # and end time (in seconds) of each respiration phase
    resp_startstop =  {'insp' : [], 'exp' : []}

    # This for loop finds all the points where the 'diff' data
    #  is above/below the y-axis (inspiration/expiration respectively)
    for i, num in enumerate(diff):
        if num > 0:

            if resp_phase['exp']:
                end = resp_phase['exp'][-1]
                start = resp_phase['exp'][0]
                resp_startstop['exp'].append([start, end])
                resp_phase['exp'] = []
            
            x_val = diff_time_vals[i]
            resp_phase['insp'].append(x_val)
        
        if num < 0:

            if resp_phase['insp']:
                end = resp_phase['insp'][-1]
                start = resp_phase['insp'][0]
                resp_startstop['insp'].append([start, end])
                resp_phase['insp'] = []
    
            x_val = diff_time_vals[i]
            resp_phase['exp'].append(x_val)

    # Checks to make sure that inspiration/expiration
    # at the end of the file is still recorded.
    if resp_phase['exp']:
                end = resp_phase['exp'][-1]
                start = resp_phase['exp'][0]
                resp_startstop['exp'].append([start, end])
                resp_phase['exp'] = []

    if resp_phase['insp']:
                end = resp_phase['insp'][-1]
                start = resp_phase['insp'][0]
                resp_startstop['insp'].append([start, end])
                resp_phase['insp'] = []
    
    # Without the following code, the system identifies the first
    # value above/below zero. The following code pushes the index
    # of the start and end to the left/right respectively
    for key, lst in resp_startstop.items():
        resp_startstop[key] = [(diff_time_vals[diff_time_vals.index(tuple[0]) - 1], diff_time_vals[diff_time_vals.index(tuple[1]) + 1]) for tuple in lst ]

    # *** Optional code for graphing vertical lines at the
    # start and end of each respiration phase (usful for visually
    #  checking that the code works) ***
    # for lst in resp_startstop.values():
    #     for tup in lst:
    #         for val in tup:
    #             plt.subplot(2,1,1)
    #             plt.axvline(x = val, color = 'b')

    return resp_startstop


def indexOfClosest(lst: list, num: float):
    """
    Given lst and any number num, returns the index of the number in lst
    that is closest to K.
    """
    closest =  lst[min(range(len(lst)), key = lambda i: abs(lst[i] - num))]
    return lst.index(closest)


def graphResp(vals, running, time_list, diff, diff_time_vals, startstop):
    """
    Given all the calculated data, graph and label the data.
    """
    # Plot raw & calculated data
    data_start = indexOfClosest(time_list, startstop[0])
    data_end = indexOfClosest(time_list, startstop[1])

    plt.subplot(2, 1, 1)
    # Graph raw data
    plt.plot(time_list[data_start : data_end],
            vals[data_start : data_end],
            label = 'Raw Sensor Data')
    # Graph moving avg data
    plt.plot(time_list[data_start : data_end], 
            running[data_start : data_end],
            label = f'Running Average (window size = {RUNNING_WINDOW_SIZE})')
    
    # Graph calculated respiration phase data
    plt.subplot(2, 1, 2)
    plt.plot(diff_time_vals[data_start : data_end],
            diff[data_start : data_end],
            'r', label = 'Breath Phase')

    # Fill above & below differential data to 
    # different breathing phases.
    plt.fill_between(
        x = diff_time_vals[data_start : data_end], 
        y1 = diff[data_start : data_end], 
        where = diff[data_start : data_end] >= 0,
        color = "g",
        alpha = 0.2)
    
    plt.fill_between(
        x = diff_time_vals[data_start : data_end], 
        y1 = diff[data_start : data_end],
        where = diff[data_start : data_end] <= 0,
        color = "b",
        alpha = 0.2)

    # Bottom plot styling
    plt.xlabel('Time [s]')
    # Top plot styling
    plt.subplot(2, 1, 1)
    plt.legend()
    plt.title('Respiration Phase Analysis')
    

def doRespAnalysis(filename, startstop):
    """ 
    Given a .txt with a list of FSR vals, and a tuple of the start
    and stop times to show on the graph, calculate all data for graphing.
    Actuall graphing is not done within this function so that this function
    can be easily called form other python scripts without automatically 
    generating a plot.
    """
    vals, time_list= readRespData(filename, startstop)
        
    running = runningMean(vals)
    diff, diff_time_vals = calcDifferential(running, time_list)

    # Currently unused, extracts a dictionary of the start/stop 
    # time of each respiratory phase
    resp_startstop = findRespiratoryPhase(diff, diff_time_vals)
    
    return vals, running, time_list, diff, diff_time_vals


def main():
    # Interpret command line args
    args = sys.argv[1:]
    filename = args[0]
    if len(args) > 0:
        startstop = (float(args[1]), float(args[2]))
    
    vals, running, time_list, diff, diff_time_vals = doRespAnalysis(filename, startstop)
    
    graphResp(vals, running, time_list, diff, diff_time_vals, startstop)
    plt.show()


if __name__ == '__main__':
    main()