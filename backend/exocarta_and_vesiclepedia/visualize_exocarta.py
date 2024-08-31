import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load and Inspect the Dataset
file_path = 'human_exocarta_proteins.csv'  # Adjust this to the correct file path if needed
exocarta_data = pd.read_csv(file_path)

print("Columns in the dataset:")
print(exocarta_data.columns)

print("\nFirst few rows of the dataset:")
print(exocarta_data.head())

# Step 2: Visualize the Data
def visualize_exocarta_data(data):
    # 1. Bar plot of top 10 proteins
    protein_counts = data['GENE SYMBOL'].value_counts().head(10)  # Adjusted column name
    plt.figure(figsize=(12, 6))
    protein_counts.plot(kind='bar')
    plt.title('Top 10 Proteins in ExoCarta')
    plt.xlabel('Protein')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 2. Pie chart of sample types
    if 'SPECIES' in data.columns:
        sample_counts = data['SPECIES'].value_counts()
        plt.figure(figsize=(10, 10))
        plt.pie(sample_counts.values, labels=sample_counts.index, autopct='%1.1f%%')
        plt.title('Distribution of Species Types')
        plt.axis('equal')
        plt.show()

    # 3. Heatmap of protein presence across different organisms
    if 'GENE SYMBOL' in data.columns and 'SPECIES' in data.columns:
        protein_organism = pd.crosstab(data['GENE SYMBOL'], data['SPECIES'])
        plt.figure(figsize=(12, 8))
        sns.heatmap(protein_organism.head(20), cmap='YlOrRd', cbar_kws={'label': 'Presence'})
        plt.title('Protein Presence Across Different Species')
        plt.tight_layout()
        plt.show()

# Visualize the data
visualize_exocarta_data(exocarta_data)

