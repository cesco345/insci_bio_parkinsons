import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Summary statistics
print(df.describe())

# Histogram of Protein Probability
plt.figure(figsize=(10, 6))
sns.histplot(df['Probability'], bins=30, kde=True)
plt.title('Distribution of Protein Probability')
plt.xlabel('Probability')
plt.ylabel('Frequency')
plt.show()
