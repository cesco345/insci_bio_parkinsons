import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Protein frequency
protein_frequency = df['Protein'].value_counts()

# Bar plot of top 10 proteins by frequency
plt.figure(figsize=(12, 6))
sns.barplot(x=protein_frequency.head(10).index, y=protein_frequency.head(10).values)
plt.title('Top 10 Most Frequent Proteins')
plt.xlabel('Protein')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()