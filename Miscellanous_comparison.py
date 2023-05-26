import os
from math import pi

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

eps0 = 8.8542e-12


def read_file(file):
    '''
            Function to read .prn files that are outputted by the VNA.
            Will return a list of the frequencies and a list of the corresponding conductivities.
            Conductivity is calculated with: e'' * eps0 * 2pi * frequency
    '''
    freq = []
    e1 = []
    e2 = []
    cond = []

    with open(f'' + file) as data_file:
        data_file = data_file.readlines()
        for i in range(1, len(data_file)):
            result = data_file[i].split()
            freq.append(int(float(result[0]) / 1e6))
            e1.append(float(result[1]))
            e2.append(float(result[2]))
            cond.append(float(result[2]) * eps0 * 2 * pi * float(result[0]))
    return freq, cond


if __name__ == "__main__":
    # assign directory
    directory = 'C:\\Users\\20203226\\OneDrive - TU Eindhoven\\Bachelor end project - BEP\\230510\\Misc\\'
    file_names = []
    dicts = {}
    # iterate over files in that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            file_names.append(filename)
            print(filename)
            parts = filename.replace('.', '_').split('_')
            freq, cond = read_file(f)

            if len(parts) > 3:
                sample = parts[0] + " " + parts[1]
            else:
                sample = parts[0]

            if sample not in dicts:
                dicts[sample] = {'Frequency': freq, parts[-2][1:]: cond}
            else:
                dicts[sample][parts[-2][1:]] = cond

    # Plotting:
    fig = plt.figure(figsize=(30, 20))
    counter = 1

    for name, dict_ in dicts.items():
        df = pd.DataFrame(dict_).set_index('Frequency')
        ax = plt.subplot(2, 3, counter)  # give the plot the right place in the figure

        # subplot formatting
        ax.title.set_text("Sample " + str(name))
        for column in df.columns:
            ax.plot(df[column])
            print(column)

        # Fitting a line to the mean:
        coeff = np.polyfit(df.index, df.mean(axis=1), 2)
        coeff = np.flip(coeff)

        # Make the fitting work for all orders
        y_fit = [0] * len(df.index)
        for order in range(len(coeff)):
            y_fit = y_fit + coeff[order] * (df.index ** order)
        ax.plot(df.index, y_fit)

        #Finding conductivities at 128 Mhz
        cond_128 = np.interp(128, df.index, y_fit)
        print(name+" has at 128 Mhz the cond: "+str(cond_128))

        plt.xlabel('Frequency [Mhz]')
        plt.ylabel('Conductivity [S/m]')
        plt.legend(list(df.columns)+['mean fitted'])

        counter += 1

    fig.show()
    #fig.savefig('Misc2.png')
    pass
