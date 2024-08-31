import pandas as pd
from io import StringIO
import requests
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

def get_exocarta_proteins():
    url = "http://exocarta.org/Archive/EXOCARTA_PROTEIN_MRNA_DETAILS_5.txt"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text), sep='\t')
        print(f"Retrieved {len(df)} proteins from ExoCarta")
        return set(df['GENE SYMBOL'])
    else:
        print("Failed to retrieve ExoCarta data")
        return set()

def get_vesiclepedia_proteins():
    url = "http://microvesicles.org/Archive/VESICLEPEDIA_PROTEIN_MRNA_DETAILS_5.1.txt"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text), sep='\t')
        print(f"Retrieved {len(df)} proteins from Vesiclepedia")
        return set(df['GENE SYMBOL'])
    else:
        print("Failed to retrieve Vesiclepedia data")
        return set()

def compare_proteins(pd_ndev_proteins, exocarta_proteins, vesiclepedia_proteins):
    pd_ndev_set = set(pd_ndev_proteins)

    in_exocarta = pd_ndev_set.intersection(exocarta_proteins)
    in_vesiclepedia = pd_ndev_set.intersection(vesiclepedia_proteins)
    in_both = in_exocarta.intersection(in_vesiclepedia)
    novel_proteins = pd_ndev_set - (in_exocarta.union(vesiclepedia_proteins))

    print(f"Total proteins in PD-NDsEV dataset: {len(pd_ndev_set)}")
    print(f"Proteins found in ExoCarta: {len(in_exocarta)}")
    print(f"Proteins found in Vesiclepedia: {len(in_vesiclepedia)}")
    print(f"Proteins found in both databases: {len(in_both)}")
    print(f"Potentially novel exosomal proteins: {len(novel_proteins)}")

    # Venn diagram
    plt.figure(figsize=(10, 10))
    venn3([pd_ndev_set, exocarta_proteins, vesiclepedia_proteins],
          ('PD-NDsEV', 'ExoCarta', 'Vesiclepedia'))
    plt.title('Protein Overlap between PD-NDsEV, ExoCarta, and Vesiclepedia')
    plt.show()

    return novel_proteins, in_exocarta, in_vesiclepedia

def plot_novel_proteins(novel_protein_data):
    if not novel_protein_data.empty:
        plt.figure(figsize=(10, 6))
        plt.scatter(novel_protein_data['Percent_Coverage'], novel_protein_data['Peptide_Count'],
                    alpha=0.5, c=novel_protein_data['Probability'], cmap='viridis')
        plt.colorbar(label='Probability')
        plt.xlabel('Percent Coverage')
        plt.ylabel('Peptide Count')
        plt.title('Distribution of Potentially Novel Exosomal Proteins')
        plt.show()
    else:
        print("No novel proteins found for plotting.")
