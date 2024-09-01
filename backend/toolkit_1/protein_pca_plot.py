import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Scaling the data
features = ['Probability', 'Percent_Coverage', 'Peptide_Count']
X = StandardScaler().fit_transform(df[features])

# PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PC1'] = principal_components[:, 0]
df['PC2'] = principal_components[:, 1]

# Scatter plot of PCA components
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='PC1', y='PC2')
plt.title('PCA of Proteomics Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()