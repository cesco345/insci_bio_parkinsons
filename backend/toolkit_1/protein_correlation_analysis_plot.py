import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Correlation matrix
corr_matrix = df[['Probability', 'Percent_Coverage', 'Peptide_Count']].corr()

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Protein Metrics')
plt.show()
