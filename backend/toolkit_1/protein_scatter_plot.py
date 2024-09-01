import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Percent_Coverage', y='Peptide_Count', hue='Probability', size='Probability', sizes=(20, 200))
plt.title('Protein Coverage vs. Peptide Count')
plt.xlabel('Percent Coverage')
plt.ylabel('Peptide Count')
plt.legend(title='Probability')
plt.tight_layout()
plt.show()