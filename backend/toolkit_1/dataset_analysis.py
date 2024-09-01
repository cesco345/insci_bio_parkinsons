import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data (example)
ev_data = pd.read_csv('ev_data.csv')

# Example of visualizing particle size distribution using Seaborn
sns.histplot(ev_data['particle_size'], kde=True)
plt.title('Particle Size Distribution')
plt.xlabel('Size (nm)')
plt.ylabel('Count')
plt.show()

# Example of comparing protein levels across different EV populations
sns.boxplot(x='EV_population', y='protein_concentration', data=ev_data)
plt.title('Protein Concentration in Different EV Populations')
plt.xlabel('EV Population')
plt.ylabel('Protein Concentration (ng/ml)')
plt.show()

# Perform a t-test to compare protein concentrations between two EV populations
group1 = ev_data[ev_data['EV_population'] == 'L1CAM+']['protein_concentration']
group2 = ev_data[ev_data['EV_population'] == 'CD81+']['protein_concentration']

t_stat, p_val = stats.ttest_ind(group1, group2)
print(f'T-test results: t-statistic = {t_stat}, p-value = {p_val}')

