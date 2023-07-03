import pandas as pd
import scipy

R1 = pd.read_csv('MRI_1.1_TSE.csv')
R2 = pd.read_csv('MRI_1.2_TSE.csv')

R1['N'] = R1['N']
R2['N'] = R2['N']
print(R1)
print(R2)

p_values = []

for sample in range(len(R1)):
    stat, p = scipy.stats.ttest_ind_from_stats(float(R1.loc[sample, 'cond']), R1.loc[sample, 'std'], R1.loc[sample, 'N'], float(R2.loc[sample, 'cond']), R2.loc[sample, 'std'], R2.loc[sample, 'N'], equal_var=False, alternative='two-sided')
    p_values.append(p)
    print(R1.loc[sample, 'cond'], R2.loc[sample, 'cond'], p)
print(p_values)

R1['p_value'] = p_values
R1.to_clipboard()