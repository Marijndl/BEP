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

baseline_1 = [0.12883378816993937, 0.14426108072435476, 0.17683227026476922, 0.2192957112691608, 0.24192813494600623, 0.2370253859361344, 0.2077060764297643, 0.1742043708039368, 0.15399783356579955, 0.1599722162618556, 0.1939770629352958, 0.22843311764352842, 0.25708844675213616, 0.2632354517786475, 0.23636392569421646, 0.19891431527087852, 0.17020394885152293, 0.1598966839088764, 0.188729269541799, 0.232564137075959, 0.2689682778151796, 0.2832963763036024, 0.27003813682208255, 0.23981739594278198, 0.19849211962621544, 0.1883728872385032, 0.19869468341087515, 0.2291451423368147, 0.27077809463345887, 0.29551194998300384, 0.29681869807602357, 0.26954441993341116, 0.2452319257398391, 0.2260622462625363, 0.22575747986635852, 0.25213972854195005, 0.28370824097828073, 0.3061920255296273, 0.31480564560618657, 0.299584571896894, 0.2674593831818452, 0.24883715610160487, 0.24940849156498096, 0.27092217745070923, 0.30579017471923137, 0.3390767324709508, 0.3452086944480067, 0.3358056035644525, 0.303040562301304, 0.27083009996863233, 0.26568798622286277, 0.28190696932418907, 0.31670993767071265, 0.35542785963799967, 0.37591739424401627, 0.3666013127145605, 0.3519539332900083, 0.3143319453195642, 0.2883376559993057, 0.2901506995071872, 0.3107076218565667, 0.34896624681202415, 0.37544851173876537, 0.3921429698059952, 0.3767094575292088, 0.3589758385123596, 0.3368318688821793, 0.3234235994606769, 0.34344217090297513, 0.3690793491331483, 0.3977386726609532, 0.4079836235514734, 0.4060532731867812, 0.38163988374730573, 0.35550838779660415, 0.35585740990965237, 0.3630931055711756, 0.4011335061708872, 0.42839667448740404, 0.4449858367717041, 0.4478565334985799, 0.4171907486742784, 0.38550783896503693, 0.3600772523182681, 0.3650974917724624, 0.3881410513371969, 0.43267038035934335, 0.4709974445139133, 0.48203110960834933, 0.47350798704861347, 0.4348695250944077, 0.40502956696770437, 0.38104922152586457, 0.3995917493729326, 0.4232406971028613, 0.4654828261433533, 0.49671474478486183, 0.4943432725720128, 0.48150002431613065, 0.4503103919981837, 0.4353026803572021]
baseline_2 = [0.17617760366389762, 0.17871716623749834, 0.1812641079267555, 0.18381842873166915, 0.1863801286522393, 0.18894920768846593, 0.191525665840349, 0.1941095031078886, 0.19670071949108467, 0.19929931498993722, 0.20190528960444626, 0.20451864333461173, 0.20713937618043374, 0.2097674881419122, 0.21240297921904713, 0.21504584941183857, 0.2176960987202865, 0.22035372714439086, 0.22301873468415176, 0.2256911213395691, 0.22837088711064293, 0.23105803199737326, 0.23375255599976005, 0.23645445911780333, 0.2391637413515031, 0.2418804027008593, 0.24460444316587207, 0.24733586274654124, 0.2500746614428669, 0.2528208392548491, 0.25557439618248773, 0.2583353322257828, 0.26110364738473446, 0.2638793416593425, 0.26666241504960714, 0.26945286755552816, 0.27225069917710565, 0.2750559099143397, 0.2778684997672302, 0.2806884687357772, 0.2835158168199806, 0.28635054401984056, 0.28919265033535696, 0.2920421357665299, 0.2948990003133592, 0.29776324397584514, 0.30063486675398743, 0.30351386864778623, 0.3064002496572415, 0.30929400978235333, 0.3121951490231216, 0.3151036673795463, 0.3180195648516275, 0.32094284143936525, 0.3238734971427594, 0.3268115319618101, 0.3297569458965173, 0.3327097389468809, 0.33566991111290095, 0.3386374623945776, 0.34161239279191064, 0.34459470230490025, 0.34758439093354626, 0.35058145867784873, 0.3535859055378077, 0.3565977315134232, 0.35961693660469524, 0.36264352081162365, 0.36567748413420853, 0.3687188265724499, 0.3717675481263478, 0.37482364879590213, 0.37788712858111306, 0.38095798748198034, 0.38403622549850414, 0.3871218426306844, 0.3902148388785212, 0.3933152142420145, 0.39642296872116417, 0.39953810231597037, 0.402660615026433, 0.40579050685255225, 0.4089277777943279, 0.41207242785176, 0.4152244570248486, 0.4183838653135937, 0.42155065271799524, 0.42472481923805333, 0.42790636487376793, 0.4310952896251389, 0.4342915934921664, 0.4374952764748503, 0.44070633857319075, 0.4439247797871878, 0.4471506001168412, 0.4503837995621511, 0.45362437812311746, 0.4568723357997403, 0.46012767259201975, 0.46339038849995556, 0.46666048352354783]

remove_baseline = False


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
    if remove_baseline:
        cond = list(np.subtract(np.array(cond),np.array(baseline_2)))
    return freq, cond


if __name__ == "__main__":
    # assign directory and initiate dictionaries
    directory = 'C:\\Users\\lolwi\\Documents\\GitHub\\BEP_VNA_data\\Round1'
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
    fig2 = plt.figure(figsize=(8, 8))
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
        mean_fit = [0] * len(df_all_samples_mean.index)
        for order in range(len(coeff)):
            mean_fit = mean_fit + coeff[order] * (df_all_samples_mean.index ** order)
        ax.plot(df_all_samples_mean.index, mean_fit, '--', label='_nolegend_', linewidth='1', color=mean_line.get_color())

    # Plot formatting:
    plt.xlabel('Frequency [Mhz]', fontsize=14)
    plt.ylabel('Conductivity [S/m]', fontsize=14)
    plt.title('Frequency sweep of all samples, mean plus standard deviation', fontsize=16)
    plt.legend()
    fig2.show()
    fig2.savefig('Round_1_all.png',dpi=200)

    pass
