import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
from math import pi
from scipy import signal
from scipy.signal import savgol_filter
import os

eps0 = 8.8542e-12

def read_file(file):
    freq = []
    e1 = []
    e2 = []
    cond = []

    with open(f''+file) as data_file:
        data_file = data_file.readlines()
        for i in range(1,len(data_file)):
            result = data_file[i].split()
            freq.append(int(float(result[0])/1e6))
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

    # dataframes = {}
    # all_samples_mean = {'Frequency': dicts[1]['Frequency']}
    # all_samples_std = {'Frequency': dicts[1]['Frequency']}

    #Plotting:
    fig = plt.figure(figsize=(30,20))
    counter = 1

    for name,dict_ in dicts.items():
        df = pd.DataFrame(dict_).set_index('Frequency')
        ax = plt.subplot(2,3,counter) #give the plot the right place in the figure

        #subplot formatting
        ax.title.set_text("Sample " + str(name))
        for column in df.columns:
            ax.plot(df[column])
            print(column)

        plt.xlabel('Frequency [Mhz]')
        plt.ylabel('Conductivity')
        plt.legend(list(df.columns))

        #Calculating of mean between samples.
        # df['mean'] = df.mean(axis=1)
        # all_samples_mean[name] = df['mean'].tolist()
        # df['standard deviation'] = df.loc[:, df.columns != 'mean'].std(axis=1)
        # all_samples_std[name] = df['standard deviation'].tolist()

        counter += 1

    fig.show()
    fig.savefig('Misc2.png')

    #Mean and standarad deviation from all samples at all frequencies
    # df_all_samples_mean = pd.DataFrame(all_samples_mean).set_index('Frequency')
    # df_all_samples_mean = df_all_samples_mean.reindex(sorted(df_all_samples_mean.columns), axis=1)
    # df_all_samples_mean.to_csv('all_samples_mean2.csv',sep=';')
    #
    # df_all_samples_std = pd.DataFrame(all_samples_std).set_index('Frequency')
    # df_all_samples_std = df_all_samples_std.reindex(sorted(df_all_samples_std.columns), axis=1)
    # df_all_samples_std.to_csv('all_samples_std2.csv',sep=';')
    pass



