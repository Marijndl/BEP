from Helmholtz_recon import *
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import cv2
from scipy import ndimage
import os

sample = 15

directory = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\masks\\Round_3_TSE\\Sample_{}'.format(sample)
path_phase = 'C:\\Users\\20203226\\Documents\\GitHub\\BEP\\MRI results\\3_TSE_tra_A.mat'

conductivites = np.array([])

# iterate over files in that directory
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)
    
    mask = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    mask_bool = mask>0

    slice_number = int(filename.split('.')[0])

    #phase
    ph_b = scipy.io.loadmat(path_phase)['SE']
    sig_HH = Helmholtz_ph(np.angle(ph_b[:,:,slice_number]))
    sig_b = smooth_HH(sig_HH, 3)

    conductivites = np.append(conductivites,sig_b[mask_bool])

print(directory)
mean_cond = str(np.mean(conductivites)).replace('.',',')
std_cond = str(np.std(conductivites)).replace('.',',')
print(mean_cond, std_cond)
print(len(conductivites))









