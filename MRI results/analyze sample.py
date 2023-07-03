import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import scipy.io

from Helmholtz_recon import *
#Choose the data file for analysis:
path_phase = 'MRI results/MRI data/1_TSE_tra_A.mat'

def get_cond(sample, directory, hist=False):
    directory = directory.format(sample)
    conductivites = np.array([])

    # iterate over files in that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        mask = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        # kernel = np.ones((5,5), np.uint8)
        # img_erosion = cv2.erode(mask, kernel, iterations=1)
        mask_bool = mask > 0

        slice_number = int(filename.split('.')[0])

        # phase
        ph_b = scipy.io.loadmat(path_phase)['SE']
        sig_HH = Helmholtz_ph(np.angle(ph_b[:, :, slice_number]))
        sig_b = smooth_HH(sig_HH, 3)
        mask_small = sig_b[mask_bool] < 4

        conductivites = np.append(conductivites, sig_b[mask_bool][mask_small])

    #Print statistics of the voxels of a sample:
    print(directory)
    mean_cond = str(np.mean(conductivites))
    std_cond = str(np.std(conductivites))
    print(mean_cond, std_cond, len(conductivites))

    #If needed, plot histogram of the voxels
    if hist:
        ax = plt.subplot(4, 4, int(sample))
        ax.hist(conductivites, bins=20)
        ax.set_title('Histogram of' + str(sample))

    return mean_cond, std_cond, len(conductivites)


def calculate_stats(directory):
    cond = []
    std = []
    N_pixels = []
    index_samp = []
    for sample in range(1, 16):
        if sample != 5:
            mean_cond, std_cond, N = get_cond(sample, directory)
            cond.append(mean_cond)
            std.append(std_cond)
            N_pixels.append(N)
            index_samp.append(sample)

    temp_dict = {'cond': cond, 'std': std, 'N': N_pixels}
    results = pd.DataFrame(data=temp_dict, index=index_samp)
    return results


if __name__ == '__main__':
    # fig = plt.figure(figsize=(30, 30))

    #Pick the directory with all the masks to be considered:
    directory_1 = 'MRI results/masks/Round_1_TSE/Sample_{}'

    R1 = calculate_stats(directory_1)
    # R2 = calculate_stats(directory_2)
    # R1.to_csv('MRI_1.2_TSE.csv')
    R1.to_clipboard()
    print(R1)

    # fig.show()
    # fig.savefig('MRI B1_1 histograms', dpi=300)
