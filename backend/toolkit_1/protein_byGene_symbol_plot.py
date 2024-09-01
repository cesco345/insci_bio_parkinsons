import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Top 10 most common gene symbols
top_genes = df['Gene_Symbol'].value_counts().head(10)

# Bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x=top_genes.index, y=top_genes.values)
plt.title('Top 10 Most Common Gene Symbols')
plt.xlabel('Gene Symbol')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()