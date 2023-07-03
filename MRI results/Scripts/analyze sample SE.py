from Helmholtz_recon import *
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import cv2
from scipy import ndimage
import os
import pandas as pd
import scipy

path_phase_A = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\1_SE_tra_A.mat'
path_phase_P = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\1_SE_tra_P.mat'

def get_cond(sample, directory):
    
    directory = directory.format(sample)
    conductivites = np.array([])

    # iterate over files in that directory
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        
        mask = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        kernel = np.ones((5,5), np.uint8)
        img_erosion = cv2.erode(mask, kernel, iterations=1)
        mask_bool = img_erosion>0

        slice = int(filename.split('.')[0])

        #phase
        ph_b_A = scipy.io.loadmat(path_phase_A)['SE']
        ph_b_P = scipy.io.loadmat(path_phase_P)['SE']
        ph_b_P = ndimage.zoom(ph_b_P, (1,1,1.2), order=1)
        ph_b = (np.angle(ph_b_A) + np.angle(ph_b_P)) / 2

        sig_HH = Helmholtz_ph(ph_b[:,:,slice], voxs=2e-3)
        sig_b = smooth_HH(sig_HH, 3)
        mask_small = sig_b[mask_bool] < 5

        conductivites = np.append(conductivites,sig_b[mask_bool])

    print(directory)
    mean_cond = str(np.mean(conductivites))
    std_cond = str(np.std(conductivites))
    print(mean_cond, std_cond, len(conductivites))
    return mean_cond, std_cond, len(conductivites)

def calculate_stats(directory):
    cond = []
    std = []
    N_pixels = []
    index_samp = []
    for sample in range(1,16):
        if sample != 5:
            mean_cond, std_cond, N = get_cond(sample, directory)
            cond.append(mean_cond)
            std.append(std_cond)
            N_pixels.append(N)
            index_samp.append(sample)

    
    temp_dict = {'cond': cond, 'std': std, 'N': N_pixels}
    results = pd.DataFrame(data = temp_dict, index = index_samp)
    return results

if __name__ == '__main__':


    directory_1 = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\masks\\Round_1_SE\\Sample_{}'
    # directory_2 = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\masks\\Round_3_TSE\\Sample_{}'

    R1 = calculate_stats(directory_1)
    # R2 = calculate_stats(directory_2)
    # R1.to_csv('MRI_2_SE.csv')
    R1.to_clipboard()
    print(R1)

    # p_values = []
    # for sample in range(1,16):
    #     if sample != 5:
    #        p_values.append( scipy.stats.ttest_ind_from_stats(float(R1.loc[sample, 'cond']), R1.loc[sample, 'std'], R1.loc[sample, 'N'], float(R2.loc[sample, 'cond']), R2.loc[sample, 'std'], R2.loc[sample, 'N'], equal_var=True, alternative='two-sided'))
    # print(p_values)    