import requests
import pandas as pd
import numpy as np
from io import StringIO, BytesIO
from sklearn.feature_selection import SelectKBest, f_classif
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import seaborn as sns
import matplotlib.pyplot as plt


def list_pride_files(pride_id):
    url = f"https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{pride_id}/files"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['_embedded']['files']
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve file list: {e}")
        return None

def download_pride_file(file_url):
    try:
        with urlopen(file_url) as response:
            return response.read()
    except Exception as e:
        print(f"Failed to download file: {e}")
        return None

def parse_protxml(xml_content):
    try:
        root = ET.fromstring(xml_content)
        namespace = {'ns': 'http://regis-web.systemsbiology.net/protXML'}
        
        proteins = []
        for protein_group in root.findall('.//ns:protein_group', namespace):
            for protein in protein_group.findall('ns:protein', namespace):
                protein_name = protein.get('protein_name')
                probability = float(protein.get('probability', 0))
                percent_coverage = float(protein.get('percent_coverage', 0))
                
                # Extract peptide count
                peptide_count = len(protein.findall('.//ns:peptide', namespace))
                
                proteins.append({
                    'Protein': protein_name,
                    'Probability': probability,
                    'Percent_Coverage': percent_coverage,
                    'Peptide_Count': peptide_count
                })
        
        return pd.DataFrame(proteins)
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return pd.DataFrame()

def analyze_ndev_data(data):
    print("\nPD-NDsEV Proteomics Data Analysis:")
    print(f"Data shape: {data.shape}")
    print(data.head())
    print("\nColumns in the dataset:")
    print(data.columns.tolist())

    if not data.empty:
        if 'Protein' in data.columns:
            protein_counts = data['Protein'].value_counts()
            print("\nTop 10 most frequent proteins:")
            print(protein_counts.head(10))

        if 'Probability' in data.columns:
            high_prob_proteins = data[data['Probability'] > 0.9]
            print(f"\nNumber of high-probability proteins (>0.9): {len(high_prob_proteins)}")

        if 'Percent_Coverage' in data.columns:
            high_coverage_proteins = data[data['Percent_Coverage'] > 50]
            print(f"\nNumber of high-coverage proteins (>50%): {len(high_coverage_proteins)}")

        if 'Peptide_Count' in data.columns:
            print("\nPeptide count statistics:")
            print(data['Peptide_Count'].describe())

    else:
        print("No data available for analysis.")

# Retrieve and analyze PD-NDsEV data
pride_id = "PXD020794"
files = list_pride_files(pride_id)

if files:
    print("Available files:")
    for file in files:
        print(f"- {file['fileName']} ({file['fileCategory']['value']})")
    
    suitable_file = next((file for file in files if file['fileName'].endswith('.prot.xml')), None)
    
    if suitable_file:
        print(f"\nAttempting to download and analyze: {suitable_file['fileName']}")
        ftp_url = next((loc['value'] for loc in suitable_file['publicFileLocations'] if loc['name'] == 'FTP Protocol'), None)
        if ftp_url:
            xml_content = download_pride_file(ftp_url)
            if xml_content is not None:
                print(f"Successfully downloaded {len(xml_content)} bytes")
                data = parse_protxml(xml_content)
                analyze_ndev_data(data)
            else:
                print("Failed to download the selected file.")
        else:
            print("FTP URL not found for the selected file.")
    else:
        print("No suitable protein XML file found. Please manually specify a file to analyze.")
else:
    print("Failed to retrieve file list from PRIDE.")

print("\nNote: This analysis uses real PD-NDsEV proteomics data from the PRIDE repository. For a more comprehensive analysis, you may need to integrate this with additional data sources or perform more advanced statistical tests.")
def correlation_analysis(data):
    print("\nCorrelation Analysis:")
    corr_matrix = data[['Probability', 'Percent_Coverage', 'Peptide_Count']].corr()
    print(corr_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap of Protein Metrics')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='Percent_Coverage', y='Peptide_Count', hue='Probability', palette='viridis')
    plt.title('Relationship between Coverage, Peptide Count, and Probability')
    plt.show()

# Add this function call after the analyze_ndev_data function in your main script
correlation_analysis(data)
