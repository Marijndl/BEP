import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

def interpolate(file):
    freq = []
    e1 = []
    e2 = []

    with open(f'C:\\Users\\20203226\\OneDrive - TU Eindhoven\\Bachelor end project - BEP\\230510\\'+file) as data_file:
        data_file = data_file.readlines()
        for i in range(1,len(data_file)):
            result = data_file[i].split()
            freq.append(float(result[0]))
            e1.append(float(result[1]))
            e2.append(float(result[2]))

    interp_func = interp1d(freq, e1)
    mhz_128 = interp_func(np.arange(124000000.0, 132000000.0, 2000000.0))[2]
    return mhz_128

if __name__ == "__main__":
    df = pd.dataframe()

# fig = plt.figure()
# plt.plot(freq,e2)
# fig.show()



