import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2

def load_and_inspect_data(file_path, dataset_name):
    data = pd.read_csv(file_path)
    print(f"\n{dataset_name} Data:")
    print(f"Shape: {data.shape}")
    print("Columns:")
    print(data.columns.tolist())
    print("\nFirst few rows:")
    print(data.head())
    return data

def identify_neuron_specific_proteins(exocarta_data, vesiclepedia_data):
    # Assume ExoCarta data is neuron-derived (NDE)
    nde_proteins = set(exocarta_data['GENE SYMBOL'])
    
    # Check if 'SPECIES' column exists in Vesiclepedia data
    if 'SPECIES' in vesiclepedia_data.columns:
        other_proteins = set(vesiclepedia_data[vesiclepedia_data['SPECIES'] != 'Homo sapiens']['GENE SYMBOL'])
    else:
        print("Warning: 'SPECIES' column not found in Vesiclepedia data. Using all Vesiclepedia proteins.")
        other_proteins = set(vesiclepedia_data['GENE SYMBOL'])

    # Identify neuron-specific proteins
    neuron_specific_proteins = nde_proteins - other_proteins
    
    print(f"\nTotal NDE proteins: {len(nde_proteins)}")
    print(f"Total other cell-type proteins: {len(other_proteins)}")
    print(f"Neuron-specific proteins: {len(neuron_specific_proteins)}")
    
    # Visualize the results
    plt.figure(figsize=(10, 6))
    venn2([nde_proteins, other_proteins], ('NDE Proteins', 'Other Cell-Type Proteins'))
    plt.title('Comparison of NDE Proteins with Other Cell-Type Proteins')
    plt.show()
    
    # Bar plot of top 10 neuron-specific proteins
    neuron_specific_counts = exocarta_data[exocarta_data['GENE SYMBOL'].isin(neuron_specific_proteins)]['GENE SYMBOL'].value_counts().head(10)
    
    plt.figure(figsize=(12, 6))
    neuron_specific_counts.plot(kind='bar')
    plt.title('Top 10 Neuron-Specific Proteins')
    plt.xlabel('Protein')
    plt.ylabel('Count in NDE')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return neuron_specific_proteins

def analyze_surface_proteins(neuron_specific_proteins):
    known_surface_proteins = {'NCAM1', 'L1CAM', 'NRCAM', 'CNTN2', 'NFASC'}  # Example set
    potential_surface_targets = neuron_specific_proteins.intersection(known_surface_proteins)
    print(f"\nPotential neuron-specific surface protein targets: {potential_surface_targets}")
    return potential_surface_targets

# Load and inspect data
exocarta_file_path = 'human_exocarta_proteins.csv'
vesiclepedia_file_path = 'vesiclepedia_data.csv'

exocarta_data = load_and_inspect_data(exocarta_file_path, "ExoCarta")
vesiclepedia_data = load_and_inspect_data(vesiclepedia_file_path, "Vesiclepedia")

# Run the analysis
neuron_specific_proteins = identify_neuron_specific_proteins(exocarta_data, vesiclepedia_data)
potential_targets = analyze_surface_proteins(neuron_specific_proteins)

# Output results
print("\nTop 20 Neuron-Specific Proteins:")
print(list(neuron_specific_proteins)[:20])
print("\nPotential Neuron-Specific Surface Protein Targets:")
print(list(potential_targets))
