import matplotlib.pyplot as plt

fig2 = plt.figure(figsize=(8, 8))
ax = plt.subplot(111)

salts_R1 = [1.5417, 1.8569, 2.1727, 2.4892, 3.1241, 3.4425, 3.7616, 4.4015, 5.0441, 5.6892, 6.337, 7.9677, 9.6147, 11.2782, 12.9584, 16.369]
salts_R2 = [1.5417, 1.8569, 2.1727, 2.4892, 3.1241, 3.7616, 5.0441, 6.337, 9.6147, 12.9584]

cond_R1 = [0.222578289, 0.31633019, 0.391969893, 0.389041185, 0.389809291, 0.428214577, 0.529513325, 0.646164223, 0.728802384, 0.755279431, 0.894423012, 1.107830573, 1.329319244, 1.523412228, 1.762462275, 2.29569611]
cond_R2 = [0.248261893, 0.277251446, 0.336148745, 0.382538061, 0.459795468, 0.544667846, 0.763202904, 0.911748973, 1.38699225, 1.797188743]

Stogryn = [0.25, 0.3, 0.35,0.4,0.5,0.55,0.6,0.7,0.8,0.9,1,1.25,1.5,1.75,2,2.5]
Stogryn_21 = [0.255,0.306,0.357,0.408,0.51,0.561,0.612,0.715,0.816,0.918,1.021,1.276,1.531,1.786,2.042,2.552]
Stogryn_19 = [0.245,0.294,0.343,0.392,0.49,0.539,0.588,0.686,0.784,0.881,0.979,1.224,1.469,1.714,1.958,2.448]

ax.plot(salts_R1, cond_R1, marker='o', markersize=3)
ax.plot(salts_R2, cond_R2, marker='o', markersize=3)
ax.plot(salts_R1, Stogryn, marker='o', markersize=3)
ax.fill_between(salts_R1, Stogryn_19,Stogryn_21, #Use the standard deviation to make the lines thicker.
                        alpha=0.2, label='_nolegend_')
# ax.set_xscale('log')

plt.xlabel('Salt [g/L]', fontsize=14)
plt.ylabel('Conductivity [S/m]', fontsize=14)
plt.title('Salt vs. conductivity, Round 1 and 2', fontsize=16)
plt.grid()
plt.legend(['Round 1', 'Round 2', 'Stogryn'])
fig2.show()
fig2.savefig('Salt_vs_cond.png',dpi=200)