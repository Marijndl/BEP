import os
from math import pi

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

samples_salt = {1: '0.25 [S/m] - 1.5417 [g/l]',
                2: '0.3 [S/m] - 1.8569 [g/l]',
                3: '0.35 [S/m] - 2.1727 [g/l]',
                4: '0.4 [S/m] - 2.4892 [g/l]',
                5: '0.5 [S/m] - 3.1241 [g/l]',
                6: '0.55 [S/m] - 3.4425 [g/l]',
                7: '0.6 [S/m] - 3.7616 [g/l]',
                8: '0.7 [S/m] - 4.4015 [g/l]',
                9: '0.8 [S/m] - 5.0441 [g/l]',
                10: '0.9 [S/m] - 5.6892 [g/l]',
                11: '1 [S/m] - 6.337 [g/l]',
                12: '1.25 [S/m] - 7.9677 [g/l]',
                13: '1.5 [S/m] - 9.6147 [g/l]',
                14: '1.75 [S/m] - 11.2782 [g/l]',
                15: '2 [S/m] - 12.9584 [g/l]',
                16: '2.5 [S/m] - 16.369 [g/l]'}

eps0 = 8.8542e-12


def read_file(file):
    '''
        Function to read .prn files that are outputted by the VNA.
        Will return a list of the frequencies and a list of the corresponding conductivities.
        Conductivity is calculated with: e'' * eps0 * 2pi * frequency
    '''
    #Prepare lists corresponding to columns in the .prn file
    freq = []
    e1 = []
    e2 = []
    cond = []

    with open(f'' + file) as data_file:
        data_file = data_file.readlines()
        for i in range(1, len(data_file)):              #Skip the first line, as this is the header
            result = data_file[i].split()
            freq.append(int(float(result[0]) / 1e6))    #Save as Mhz
            e1.append(float(result[1]))
            e2.append(float(result[2]))
            cond.append(float(result[2]) * eps0 * 2 * pi * float(result[0]))
    return freq, cond


if __name__ == "__main__":
    # assign directory and initiate dictionaries
    directory = 'C:\\Users\\20203226\\OneDrive - TU Eindhoven\\Bachelor end project - BEP\\230510\\Round1\\'
    samples_dict = {}

    # iterate over files in that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(filename)
            #format the name of the file and get the frequency and conductivity
            fname_splitted = filename.replace('.', '_').split('_')
            freq, cond = read_file(f)

            #add the measurements of the different sample to the dictionairy
            sample_number = int(fname_splitted[1][1:])
            if sample_number not in samples_dict:
                samples_dict[sample_number] = {'Frequency': freq, fname_splitted[2]: cond}
            else:
                samples_dict[sample_number][fname_splitted[2]] = cond

    #initiate dataframes that contain the means and standard deviation of all sample for all frequencies.
    all_samples_mean = {'Frequency': samples_dict[1]['Frequency']}
    all_samples_std = {'Frequency': samples_dict[1]['Frequency']}

    # Plotting:
    fig = plt.figure(figsize=(30, 30))

    for name, dict_ in samples_dict.items(): #Loop over all the samples
        #make a dataframe from the dictionary obtained
        df = pd.DataFrame(dict_).set_index('Frequency')

        # calculate and store the mean and stand deviation of the sample's dataframe
        df['mean'] = df.mean(axis=1)
        all_samples_mean[name] = df['mean'].tolist()
        df['standard deviation'] = df.loc[:, df.columns != 'mean'].std(axis=1)
        all_samples_std[name] = df['standard deviation'].tolist()

        #PLot the first three measurements of the sample
        ax = plt.subplot(4, 4, int(name))
        ax.plot(df['M1'])
        ax.plot(df['M2'])
        ax.plot(df['M3'])

        # Fitting a line to the mean:
        coeff = np.polyfit(df.index, df[['M1', 'M2', 'M3']].mean(axis=1), 2)
        coeff = np.flip(coeff)

        # Make the fitting work for all orders
        y_fit = [0]*len(df.index)
        for order in range(len(coeff)):
            y_fit = y_fit + coeff[order] * (df.index ** order)
        ax.plot(df.index, y_fit)

        # Formatting
        ax.title.set_text("Sample " + str(name) + ": " + samples_salt[name])
        plt.xlabel('Frequency [Mhz]')
        plt.ylabel('Conductivity [S/m]')
        plt.legend(['M1', 'M2', 'M3', 'mean fitted'])

    fig.show()
    # fig.savefig('Round_1_v2.png')

    # Mean and standarad deviation from all samples at all frequencies stored to csv file
    df_all_samples_mean = pd.DataFrame(all_samples_mean).set_index('Frequency')
    df_all_samples_mean = df_all_samples_mean.reindex(sorted(df_all_samples_mean.columns), axis=1)
    df_all_samples_mean.to_csv('all_samples_mean.csv', sep=';')

    df_all_samples_std = pd.DataFrame(all_samples_std).set_index('Frequency')
    df_all_samples_std = df_all_samples_std.reindex(sorted(df_all_samples_std.columns), axis=1)
    df_all_samples_std.to_csv('all_samples_std.csv', sep=';')

    # Make a figure with all the samples:
    fig2 = plt.figure(figsize=(15, 15))
    ax = plt.subplot(111)
    for sample in df_all_samples_mean.columns:
        #Loop over all the samples
        yfit = df_all_samples_mean[sample]
        std_dev = df_all_samples_std[sample]
        mean_line, = ax.plot(yfit, label=str(sample), linewidth='2')
        ax.fill_between(df_all_samples_mean.index, yfit - std_dev, yfit + std_dev, #Use the standard deviation to make the lines thicker.
                        alpha=0.2, label='_nolegend_')

        # Fitting a line to the mean:
        coeff = np.polyfit(df_all_samples_mean.index, yfit, 2)
        coeff = np.flip(coeff)

        # Make the fitting work for all orders
        mean_fit = [0] * len(df.index)
        for order in range(len(coeff)):
            mean_fit = mean_fit + coeff[order] * (df.index ** order)
        ax.plot(df.index, mean_fit, '--', label='_nolegend_', linewidth='1', color=mean_line.get_color())

    # Plot formatting:
    plt.xlabel('Frequency [Mhz]')
    plt.ylabel('Conductivity [S/m]')
    plt.title('Frequency sweep of all samples, mean plus standard deviation')
    plt.legend()
    fig2.show()
    fig2.savefig('Round_1_all.png',dpi=200)

    pass
