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
fig5.savefig('figures results/VNA vs MRI steps 2.png',dpi=300)








#                   VNA vs MRI
#------------------------------------------------

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
ax = plt.subplot(111)
ax.errorbar(salts_MRI, R1_1['cond'], yerr=R1_1['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.1')
ax.errorbar(salts_MRI, R1_2['cond'], yerr=R1_2['std']  , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 1.2')
ax.errorbar(salts_MRI, R2['cond'], yerr=R2['std']      , elinewidth=1, capsize=2.5, fmt='o', capthick=2, label='MRI 2')

ax.plot(salts_R1[:-1], mean_cond[:-1], 'o-',markersize=6, linewidth=2, label='VNA mean')

fig3.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.xlabel('NaCl [g/L]', fontsize=14)
plt.ylabel('Conductivity [S/m]', fontsize=14)
plt.title('NaCl vs. conductivity, VNA B1 and B2,\n MRI 1.1, 1.2, 2 (20°C - 128 Mhz)', fontsize=16)
plt.grid()
plt.legend()
fig3.show()
fig3.savefig('figures results/VNA vs MRI.png',dpi=300)
print(corr1_1)

