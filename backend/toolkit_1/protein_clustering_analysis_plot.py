import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_csv('PXD020794_proteomics_data.csv')

# Scaling the data
features = ['Probability', 'Percent_Coverage', 'Peptide_Count']
X = StandardScaler().fit_transform(df[features])

# Applying KMeans
kmeans = KMeans(n_clusters=3)
df['Cluster'] = kmeans.fit_predict(X)

# Scatter plot colored by cluster
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Percent_Coverage', y='Peptide_Count', hue='Cluster', palette='Set1')
plt.title('Clustering of Proteins based on Coverage and Peptide Count')
plt.xlabel('Percent Coverage')
plt.ylabel('Peptide Count')
plt.show()
