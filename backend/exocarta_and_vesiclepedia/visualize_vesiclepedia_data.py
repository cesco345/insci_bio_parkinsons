import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2

# Load ExoCarta data from CSV file
exocarta_file_path = 'human_exocarta_proteins.csv'  # Replace with your actual file path
exocarta_data = pd.read_csv(exocarta_file_path)

# Load Vesiclepedia data from CSV file
vesiclepedia_file_path = 'vesiclepedia_data.csv'  # Replace with your actual file path
vesiclepedia_data = pd.read_csv(vesiclepedia_file_path)

def compare_and_visualize(exocarta_data, vesiclepedia_data):
    # 1. Compare protein sets
    exocarta_proteins = set(exocarta_data['GENE SYMBOL'])
    vesiclepedia_proteins = set(vesiclepedia_data['GENE SYMBOL'])
    
    common_proteins = exocarta_proteins.intersection(vesiclepedia_proteins)
    exocarta_unique = exocarta_proteins - vesiclepedia_proteins
    vesiclepedia_unique = vesiclepedia_proteins - exocarta_proteins
    
    print(f"Common proteins: {len(common_proteins)}")
    print(f"ExoCarta unique proteins: {len(exocarta_unique)}")
    print(f"Vesiclepedia unique proteins: {len(vesiclepedia_unique)}")
    
    # 2. Venn diagram of protein overlap
    plt.figure(figsize=(10, 6))
    venn2([exocarta_proteins, vesiclepedia_proteins], ('ExoCarta', 'Vesiclepedia'))
    plt.title('Protein Overlap between ExoCarta and Vesiclepedia')
    plt.show()
    
    # 3. Bar plot of top 10 common proteins
    common_protein_counts = pd.concat([
        exocarta_data[exocarta_data['GENE SYMBOL'].isin(common_proteins)]['GENE SYMBOL'].value_counts(),
        vesiclepedia_data[vesiclepedia_data['GENE SYMBOL'].isin(common_proteins)]['GENE SYMBOL'].value_counts()
    ], axis=1).fillna(0)
    common_protein_counts.columns = ['ExoCarta', 'Vesiclepedia']
    common_protein_counts = common_protein_counts.sort_values('ExoCarta', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    common_protein_counts.plot(kind='bar')
    plt.title('Top 10 Common Proteins in ExoCarta and Vesiclepedia')
    plt.xlabel('Protein')
    plt.ylabel('Count')
    plt.legend(title='Database')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # 4. Heatmap of species distribution
    species_distribution = pd.DataFrame({
        'ExoCarta': exocarta_data['SPECIES'].value_counts(),
        'Vesiclepedia': vesiclepedia_data['SPECIES'].value_counts()
    }).fillna(0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(species_distribution, annot=True, fmt='g', cmap='YlOrRd')
    plt.title('Species Distribution in ExoCarta and Vesiclepedia')
    plt.tight_layout()
    plt.show()

# Run the comparison and visualization
compare_and_visualize(exocarta_data, vesiclepedia_data)

