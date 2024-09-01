import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Top 10 proteins by probability
top_proteins = df.nlargest(10, 'Probability')

# Bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=top_proteins, x='Protein', y='Probability')
plt.title('Top 10 Proteins by Probability')
plt.xlabel('Protein')
plt.ylabel('Probability')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
