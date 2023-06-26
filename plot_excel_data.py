import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig2 = plt.figure(figsize=(6,5))
ax = plt.subplot(111)

salts_R1 = [1.5417, 1.8569, 2.1727, 2.4892, 3.1241, 3.4425, 3.7616, 4.4015, 5.0441, 5.6892, 6.337, 7.9677, 9.6147, 11.2782, 12.9584, 16.369]
salts_R2 = [1.5417, 1.8569, 2.1727, 2.4892, 3.1241, 3.7616, 5.0441, 6.337, 9.6147, 12.9584]
salts_MRI = [1.5417, 1.8569, 2.1727, 2.4892, 3.4425, 3.7616, 4.4015, 5.0441, 5.6892, 6.337, 7.9677, 9.6147, 11.2782, 12.9584]


cond_R1 = [0.222578289, 0.31633019, 0.391969893, 0.389041185, 0.389809291, 0.428214577, 0.529513325, 0.646164223, 0.728802384, 0.755279431, 0.894423012, 1.107830573, 1.329319244, 1.523412228, 1.762462275, 2.29569611]
cond_R2 = [0.248261893, 0.277251446, 0.336148745, 0.382538061, 0.459795468, 0.544667846, 0.763202904, 0.911748973, 1.38699225, 1.797188743]
# mean_cond = [0.235420091,0.296790818,0.364059319,0.385789623,0.424802379,0.428214577,0.537090585,0.646164223,0.746002644,0.755279431,0.903085992,1.107830573,1.358155747,1.523412228,1.779825509,2.29569611]
mean_cond = [0.420520091,0.481890818,0.549159319,0.586126011,0.617970794,0.65072209,0.722190585,0.831264223,0.931102644,0.940379431,1.088185992,1.292930573,1.543255747,1.708512228,1.964925509,2.48079611]
mean_cond_MRI = [0.420520091,0.481890818,0.549159319,0.586126011,0.65072209,0.722190585,0.831264223,0.931102644,0.940379431,1.088185992,1.292930573,1.543255747,1.708512228,1.964925509]

mean_MRI = [0.265674173,0.362965782,0.420293657,0.465857001,0.446416936,0.537398599,0.658390478,0.714145284,0.809159818,0.902934395,1.102417949,1.199778455,1.356224831,1.580441539]

std_VNA_1 = [0.058226412,0.001175248,0.01098812,0.001703994,0.001925014,0.001777715,0.002178012,0.001693819,0.012855891,0.003886681,0.004068581,0.004205705,0.027936619,0.01177391,0.003074124,0.00713803]
std_VNA_2 = [0.00094609,0.002904317,0.002392513,0.001222148,0.002829586,0.015121056,8.67533e-05,0.004562165,0.010281559,0.034887665]

Stogryn = [0.25, 0.3, 0.35,0.4,0.5,0.55,0.6,0.7,0.8,0.9,1,1.25,1.5,1.75,2,2.5]
Stogryn_21 = [0.255,0.306,0.357,0.408,0.51,0.561,0.612,0.715,0.816,0.918,1.021,1.276,1.531,1.786,2.042,2.552]
Stogryn_19 = [0.245,0.294,0.343,0.392,0.49,0.539,0.588,0.686,0.784,0.881,0.979,1.224,1.469,1.714,1.958,2.44]
NYU = [0.290,0.342,0.395,0.447,0.552,0.604,0.656,0.760,0.863,0.966,1.069,1.327,1.586,1.843,2.102,2.627]

mean_cond_1 = [x - 0.1851 for x in mean_cond]
print(mean_cond_1)
ax.plot(salts_R1, mean_cond_1, marker='o', markersize=3, color='red')
trend_VNA = np.polyfit(salts_R1, mean_cond_1, 1)
trend_VNA = np.poly1d(trend_VNA)
ax.plot(salts_R1, trend_VNA(salts_R1), linestyle='dotted', color='red')
# Fitting a line to the mean:
# coeff = np.polyfit(salts_R1, mean_cond, 2)
# y_trend = np.poly1d(coeff)
# plt.plot(salts_R1,y_trend(salts_R1),'--',  marker='o', markersize=3)

#Model lines:
stogryn_fit = np.polyfit(salts_R1, Stogryn, 1)
print('Stogryn baby:' + str(np.poly1d(stogryn_fit)))

sto, = ax.plot(salts_R1, Stogryn, marker='o', markersize=3, color='purple')
ax.fill_between(salts_R1, Stogryn_19,Stogryn_21, #Use the standard deviation to make the lines thicker.
                        alpha=0.2, label='_nolegend_', color = sto.get_color())
ax.plot(salts_R1, NYU, marker='o', markersize=3, color='grey')
# ax.set_xscale('log')

plt.xlabel('Salt [g/L]', fontsize=14)
plt.ylabel('Conductivity [S/m]', fontsize=14)
plt.title('Salt vs. conductivity, VNA 1 and 2,\n Stogryn and NYU models (20°C - 128 Mhz)', fontsize=16)
plt.grid()
plt.legend(['VNA B1 & B2 mean','Mean VNA fit','Stogryn', 'NYU'])
fig2.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
fig2.show()
fig2.savefig('Salt_vs_cond.png',dpi=300)


#Final comparison:

R1_1 = pd.read_csv('MRI results/MRI_1.1_TSE.csv')
R1_2 = pd.read_csv('MRI results/MRI_1.2_TSE.csv')
R2 = pd.read_csv('MRI results/MRI_2_TSE.csv')

#Correcting the MRI data by the offset of MRI 1.1
corr1_1 = [x * -0.0295 - 0.0466 for x in salts_MRI]
# R1_1['cond'] = R1_1['cond'] - corr1_1
# R1_2['cond'] = R1_2['cond'] - corr1_1
# R2['cond'] = R2['cond'] - corr1_1

fig3 = plt.figure(figsize=(7.2,6))
ax2 = plt.subplot(111)
ax2.errorbar(salts_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.1')
ax2.errorbar(salts_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.2')
ax2.errorbar(salts_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 2')

ax2.plot(salts_R1[:-1], mean_cond[:-1], 'o-',markersize=6, linewidth=2, label='VNA mean')

fig3.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.xlabel('Salt [g/L]', fontsize=14)
plt.ylabel('Conductivity [S/m]', fontsize=14)
plt.title('Salt vs. conductivity, VNA 1 and 2,\n MRI 1.1, 1.2, 2 (20°C - 128 Mhz)', fontsize=16)
plt.grid()
plt.legend()
fig3.show()
fig3.savefig('VNA vs MRI.png',dpi=300)
print(corr1_1)


fig4 = plt.figure(figsize=(6,5))
cond_R1 = [x + 0.1851 for x in cond_R1]
cond_R2 = [x + 0.1851 for x in cond_R2]
trend_R1 = np.polyfit(salts_R1, cond_R1, 1)
print(trend_R1)
trend_R1 = np.poly1d(trend_R1)
trend_R2 = np.polyfit(salts_R2, cond_R2, 1)
print(trend_R2)
trend_R2 = np.poly1d(trend_R2)

ax3 = plt.subplot(111)
ax3.errorbar(salts_R1, cond_R1, yerr=std_VNA_1, elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='VNA 1', color='red')
ax3.errorbar(salts_R2, cond_R2, yerr=std_VNA_2, elinewidth=1, capsize=2.5, fmt='s', capthick=2, label='VNA 2', color='orange')
ax3.plot(salts_R1, trend_R1(salts_R1), color='red')
ax3.plot(salts_R1, trend_R2(salts_R1), color='orange')

#Formatting
plt.title('Salt vs. conductivity, VNA 1 and 2,\n mean, standard deviation and fit (20°C - 128 Mhz)', fontsize=16)
plt.xlabel('Salt [g/L]', fontsize=14)
plt.ylabel('Conductivity [S/m]', fontsize=14)
fig4.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.grid()
plt.legend()
fig4.savefig('VNA 1 vs VNA 2.png',dpi=300)
fig4.show()



# MRI vs VNA for correction
#Correcting the MRI data by the offset of MRI 1.1
corr1_1 = [x * -0.0295 - 0.0466 for x in salts_MRI]
# R1_1['cond'] = R1_1['cond'] - corr1_1
# R1_2['cond'] = R1_2['cond'] - corr1_1
# R2['cond'] = R2['cond'] - corr1_1
# mean_MRI = np.subtract(np.array(mean_MRI), np.array(corr1_1))

trend_MRI1_1 = np.polyfit(mean_cond_MRI, R1_1['cond'], 1)
trend_MRI1_1 = np.poly1d(trend_MRI1_1)

trend_MRI1_2 = np.polyfit(mean_cond_MRI, R1_2['cond'], 1)
trend_MRI1_2 = np.poly1d(trend_MRI1_2)

trend_MRI2= np.polyfit(mean_cond_MRI, R2['cond'], 1)
trend_MRI2 = np.poly1d(trend_MRI2)

fig5 = plt.figure(figsize=(3*7.2,6))
ax5 = plt.subplot(131)
ax5.errorbar(mean_cond_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.1')
ax5.errorbar(mean_cond_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='s', capthick=2, label='MRI 1.2')
ax5.errorbar(mean_cond_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='v', capthick=2, label='MRI 2')
ax5.plot([0, 2], [0, 2], 'k--', label='diagonal')
# ax5.plot(mean_cond_MRI, trend_MRI1_1(mean_cond_MRI), label='MRI 1.1 fitted')
# ax5.plot(mean_cond_MRI, trend_MRI1_2(mean_cond_MRI), label='MRI 1.2 fitted')
# ax5.plot(mean_cond_MRI, trend_MRI2(mean_cond_MRI), label='MRI 2 fitted')
ax5.legend()
ax5.grid()
ax5.set_ylim(-0.2,2.5)
ax5.set_ylabel('MRI conductivity [S/m]', fontsize=14)
ax5.set_xlabel('VNA conductivity [S/m]', fontsize=14)

ax6 = plt.subplot(132)
ax6.plot([0, 2], [0, 2], 'k--', label='diagonal')
ax6.plot(mean_cond_MRI, trend_MRI1_1(mean_cond_MRI), label='MRI 1.1 fitted',marker='o')
ax6.plot(mean_cond_MRI, trend_MRI1_2(mean_cond_MRI), label='MRI 1.2 fitted',marker='s')
ax6.plot(mean_cond_MRI, trend_MRI2(mean_cond_MRI), label='MRI 2 fitted'    ,marker='v')
ax6.legend()
ax6.grid()
ax6.set_ylim(-0.2,2.5)
ax6.set_xlabel('VNA conductivity [S/m]', fontsize=14)
ax6.set_title('VNA vs MRI conductivity \n (20°C - 128 Mhz)', fontsize=16)

#adjusting
ax7 = plt.subplot(133)
# R1_1['cond'] = R1_1['cond'] - corr1_1
# R1_2['cond'] = R1_2['cond'] - corr1_1
# R2['cond'] = R2['cond'] - corr1_1

trend_MRI1_1 = np.polyfit(mean_cond_MRI, R1_1['cond'], 1)
trend_MRI1_1 = np.poly1d(trend_MRI1_1)

trend_MRI1_2 = np.polyfit(mean_cond_MRI, R1_2['cond'], 1)
trend_MRI1_2 = np.poly1d(trend_MRI1_2)

trend_MRI2= np.polyfit(mean_cond_MRI, R2['cond'], 1)
trend_MRI2 = np.poly1d(trend_MRI2)

mean_MRI = np.subtract(np.array(mean_MRI), np.array(corr1_1))
ax7.errorbar(mean_cond_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.1')
ax7.errorbar(mean_cond_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='s', capthick=2, label='MRI 1.2')
ax7.errorbar(mean_cond_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='v', capthick=2, label='MRI 2')
ax7.plot([0, 2], [0, 2], 'k--', label='diagonal')
# ax7.plot(mean_cond_MRI, trend_MRI1_1(mean_cond_MRI), label='MRI 1.1 fitted', color= '#1f77b4')
# ax7.plot(mean_cond_MRI, trend_MRI1_2(mean_cond_MRI), label='MRI 1.2 fitted', color= '#ff7f0e')
# ax7.plot(mean_cond_MRI, trend_MRI2(mean_cond_MRI), label='MRI 2 fitted'    , color= '#2ca02c')

fig5.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.xlabel('VNA conductivity [S/m]', fontsize=14)
# plt.ylabel('MRI conductivity [S/m]', fontsize=14)
plt.ylim(-0.2,2.5)
plt.grid()
plt.legend()
fig5.show()
fig5.savefig('VNA vs MRI steps 2.png',dpi=300)






# # MRI vs VNA for correction
# #Correcting the MRI data by the offset of MRI 1.1
# corr1_1 = [x * -0.0295 - 0.0466 for x in salts_MRI]
# # R1_1['cond'] = R1_1['cond'] - corr1_1
# # R1_2['cond'] = R1_2['cond'] - corr1_1
# # R2['cond'] = R2['cond'] - corr1_1
# # mean_MRI = np.subtract(np.array(mean_MRI), np.array(corr1_1))
#
# trend_MRI = np.polyfit(mean_cond_MRI, mean_MRI, 1)
# trend_MRI = np.poly1d(trend_MRI)
#
# fig5 = plt.figure(figsize=(7.2,6))
# ax5 = plt.subplot(111)
# ax5.errorbar(mean_cond_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.1')
# ax5.errorbar(mean_cond_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='s', capthick=2, label='MRI 1.2')
# ax5.errorbar(mean_cond_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='v', capthick=2, label='MRI 2')
# ax5.plot([0, 2], [0, 2], 'k--', label='diagonal')
# ax5.plot(mean_cond_MRI, trend_MRI(mean_cond_MRI), label='Mean MRI')
#
# fig5.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
# plt.xlabel('VNA conductivity [S/m]', fontsize=14)
# plt.ylabel('MRI conductivity [S/m]', fontsize=14)
# plt.ylim(-0.2,2.5)
# plt.title('VNA vs MRI conductivity \n (20°C - 128 Mhz)', fontsize=16)
# plt.grid()
# plt.legend()
# fig5.show()
# fig5.savefig('VNA vs MRI.png',dpi=300)


### comparing VNA to MRI and correction explanation inbetween:


trend_MRI1_1 = np.polyfit(salts_MRI, R1_1['cond'], 1)
trend_MRI1_1 = np.poly1d(trend_MRI1_1)
print('MRI B1.1:'+str(trend_MRI1_1))

trend_MRI1_2 = np.polyfit(salts_MRI, R1_2['cond'], 1)
trend_MRI1_2 = np.poly1d(trend_MRI1_2)

trend_MRI2= np.polyfit(salts_MRI, R2['cond'], 1)
trend_MRI2 = np.poly1d(trend_MRI2)

trend_VNA_mean = np.polyfit(salts_R1, mean_cond, 1)
trend_VNA_mean = np.poly1d(trend_VNA_mean)
print('VNA mean'+str(trend_VNA_mean))

#VNA - 22%
mean_cond_85 = [x*0.78 for x in mean_cond]
trend_VNA_mean_85 = np.polyfit(salts_R1, mean_cond_85, 1)
trend_VNA_mean_85 = np.poly1d(trend_VNA_mean_85)

cond_MRI1_1_comp = [x/0.78 for x in R1_1['cond']]
trend_MRI1_1_comp = np.polyfit(salts_MRI, cond_MRI1_1_comp, 1)
trend_MRI1_1_comp = np.poly1d(trend_MRI1_1_comp)

fig6 = plt.figure(figsize=(3*7.2,6))

corr1_1 = [x * -0.0295 - 0.0466 for x in salts_MRI]

ax1 = plt.subplot(131)
ax1.errorbar(salts_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B1.1', color='blue')
ax1.errorbar(salts_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B1.2', color='green')
ax1.errorbar(salts_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B3', color='darkcyan')

ax1.plot(salts_R1[:-1], mean_cond[:-1], 'o-',markersize=6, linewidth=2, label='VNA mean', color='red')

fig3.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
ax1.set_xlabel('Salt [g/L]', fontsize=14)
ax1.set_ylabel('Conductivity [S/m]', fontsize=14)
ax1.set_title('Salt vs. conductivity, VNA mean,\n MRI B1.1, B1.2, B3 (20°C - 128 Mhz)', fontsize=16)
ax1.grid()
ax1.legend()
ax1.set_ylim(-0.2,2.5)

ax2 = plt.subplot(132)

ax2.plot(salts_MRI, trend_MRI1_1(salts_MRI), label='MRI B1.1 fitted, not corrected',marker='o', color='blue')
ax2.plot(salts_MRI, trend_MRI1_2(salts_MRI), label='MRI B1.2 fitted, not corrected',marker='s', color='green')
ax2.plot(salts_MRI, trend_MRI2(salts_MRI),   label='MRI B3 fitted, not corrected'  ,marker='v', color='darkcyan')
ax2.plot(salts_R1, trend_VNA_mean(salts_R1), label='Mean VNA fitted'   ,marker='x', color='red')
# ax2.plot(salts_R1, trend_VNA_mean_85(salts_R1), label='Mean VNA sigma comp'   ,marker='x', color='tomato')
ax2.plot(salts_MRI, trend_MRI1_1_comp(salts_MRI), label='MRI B1.1, $σ_{z}$ corrected'   ,marker='o', color='deepskyblue')
ax2.legend()
ax2.grid()
ax2.set_ylim(-0.2,2.5)
ax2.set_xlabel('Salt [g/L]', fontsize=14)
ax2.set_title('VNA vs MRI conductivity, fitted\n (20°C - 128 Mhz)', fontsize=16)

corr1_1 = [x * -0.0346 - 0.0208 for x in salts_MRI]
print(corr1_1)
R1_1['cond'] = R1_1['cond'] - corr1_1
R1_2['cond'] = R1_2['cond'] - corr1_1
R2['cond'] = R2['cond'] - corr1_1

ax3 = plt.subplot(133)
ax3.errorbar(salts_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B1.1', color='blue')
ax3.errorbar(salts_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B1.2', color='green')
ax3.errorbar(salts_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI B3)', color='darkcyan')

ax3.plot(salts_R1[:-1], mean_cond[:-1], 'o-',markersize=6, linewidth=2, label='VNA mean', color='red')

fig3.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
ax3.set_xlabel('Salt [g/L]', fontsize=14)
ax3.set_ylabel('Conductivity [S/m]', fontsize=14)
ax3.set_title('Salt vs. conductivity, VNA mean,\n MRI B1.1, B1.2, B3 compensated (20°C - 128 Mhz)', fontsize=16)
ax3.grid()
ax3.legend()
ax3.set_ylim(-0.2,2.5)

fig6.show()
fig6.savefig('MRI and VNA sigma compensated 2.png',dpi=300)

