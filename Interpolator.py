import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
from math import pi
from scipy import signal
from scipy.signal import savgol_filter
import os

eps0 = 8.8542e-12

def interpolate(file):
    freq = []
    e1 = []
    e2 = []

    with open(f''+file) as data_file:
        data_file = data_file.readlines()
        for i in range(1,len(data_file)):
            result = data_file[i].split()
            freq.append(float(result[0]))
            e1.append(float(result[1]))
            e2.append(float(result[2]))

    #interpolate to find the value at 128 Mhz
    interp_func = interp1d(freq, e2)
    interp_freq = np.arange(100000000.0, 902000000.0, 28000000.0)
    epsl = interp_func(np.arange(100000000.0, 902000000.0, 28000000.0))
    epsl3 = savgol_filter(e2, 75, 3)  # window size 51, polynomial order 3

    x_value = np.interp(128000000.0, freq, e2)
    x_value2 = np.interp(128000000.0, freq, epsl3)

    # fig = plt.figure()
    # plt.plot(freq, e2)
    # # plt.plot(interp_freq,epsl)
    # plt.plot(freq,epsl3)
    # plt.legend(['normal','interp'])
    # fig.show()

    #Caluclate the conductivity:
    cond = x_value2 * eps0 * 2 * pi * 128e6

    return cond


if __name__ == "__main__":
    # assign directory
    directory = 'C:\\Users\\20203226\\OneDrive - TU Eindhoven\\Bachelor end project - BEP\\230510\\'
    file_names = []
    conductivities = []
    # iterate over files in that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            file_names.append(filename)
            print(filename)
            conductivities.append(interpolate(f))

    dict_temp = {'file name': file_names, 'conductivity': conductivities}
    df = pd.DataFrame(dict_temp)
    df.to_csv('Conductivities_VNA_11_05_2023')
    print(df.head())



