import numpy as np
import matplotlib.pyplot as plt

cond = [0.3356786,0.311672497,0.374274142,0.375324192,0.334042824,0.485600096,0.256440552,0.27,0.231196635,0.464730835,0.535392627,0.356723678,0.20490336,0.221237993,0.181595775,0.285156945,0.2918288,0.194929207]
cond_1 = cond[:6]
cond_2 = cond[6:12]
cond_3 = cond[12:]
std = [1] * len(cond)
x_pos = np.array([0,1,2,4,5,6,9,10,11,13,14,15,18,19,20,22,23,24])
labels = ['MRI B1.1', 'MRI B1.2', 'MRI B3']

fig = plt.figure()
ax = plt.subplot(111)

ax.errorbar(x_pos, cond,
       yerr=std,
       alpha=0.5,
       ecolor='black',
       capsize=10)

ax.set_ylabel('Category')
ax.set_title('Coefficent of Thermal Expansion (CTE) of Three Metals')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()

plt.show()
