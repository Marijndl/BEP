from Helmholtz_recon import *
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import cv2
from scipy import ndimage
import os

sample = 7
directory = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\masks\\Round_1_SE\\Sample_{}'.format(sample)
path_phase_A = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\1_SE_tra_A.mat'
path_phase_P = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\1_SE_tra_P.mat'

conductivites = np.array([])

# iterate over files in that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    mask = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    mask_bool = mask>0

    slice = int(filename.split('.')[0])

    #phase
    ph_b_A = scipy.io.loadmat(path_phase_A)['SE']
    ph_b_P = scipy.io.loadmat(path_phase_P)['SE']
    signal_mean = np.mean( np.array([ np.angle(ph_b_A[:,:,slice]), np.angle(ph_b_P[:,:,slice]) ]), axis=0 )
    signal_A = np.angle(ph_b_A[:,:,slice])


    sig_HH = Helmholtz_ph(signal_mean)
    
    sig_b = smooth_HH(sig_HH, 1)

    conductivites = np.append(conductivites,sig_b[mask_bool])

print(directory)
mean_cond = str(np.mean(conductivites)).replace('.',',')
std_cond = str(np.std(conductivites)).replace('.',',')
print(mean_cond, std_cond)
print(len(conductivites))









