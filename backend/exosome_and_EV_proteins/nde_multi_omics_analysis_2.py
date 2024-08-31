import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
import requests
import io
import gzip
from pyteomics import mzml

# Function to fetch and parse proteomics data from PRIDE
def get_proteomics_data(pride_id):
    url = f"https://www.ebi.ac.uk/pride/archive/projects/{pride_id}/files/{pride_id}.mzML"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # Parse mzML file using pyteomics
            with mzml.read(io.BytesIO(response.content)) as spectra:
                mz_values = []
                intensity_values = []
                for spectrum in spectra:
                    mz_values.append(spectrum['m/z array'])
                    intensity_values.append(spectrum['intensity array'])

            # For simplicity, let's create a DataFrame with m/z values as features
            max_len = max(len(mz) for mz in mz_values)
            X = np.zeros((len(mz_values), max_len))
            for i, mz in enumerate(mz_values):
                X[i, :len(mz)] = mz
            
            return pd.DataFrame(X)  # Assuming intensity values or m/z values as features
        except Exception as e:
            print(f"Error processing proteomics data: {e}")
    else:
        print(f"Failed to download data from {url}")
    return None

# Function to fetch and parse RNA-seq data from GEO
def get_rnaseq_data(geo_id):
    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{geo_id[:-3]}nnn/{geo_id}/matrix/{geo_id}_series_matrix.txt.gz"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            content = gzip.decompress(response.content).decode('utf-8')
            data = pd.read_csv(io.StringIO(content), sep='\t', comment='!')
            # Assuming gene names are in the first column and samples in subsequent columns
            X = data.set_index('ID_REF').T.iloc[1:, :]  # Transpose so that samples are rows
            return X
        except Exception as e:
            print(f"Error processing RNA-seq data: {e}")
    else:
        print(f"Failed to download data from {url}")
    return None

# Analysis function
def analyze_data(X, y):
    if X.empty or y.empty:
        print("Empty dataset. Cannot perform analysis.")
        return

    print(f"Data shape: {X.shape}")
    print(X.head())

    # Feature selection for candidate biomarkers
    selector = SelectKBest(f_classif, k=10)
    X_new = selector.fit_transform(X, y)

    # Get the indices of the selected features
    selected_indices = selector.get_support(indices=True)
    selected_features = X.columns[selected_indices]

    print("\nTop 10 selected features:")
    print(selected_features)

# Debugging function and print statements
def get_proteomics_data(pride_id):
    url = f"https://www.ebi.ac.uk/pride/archive/projects/{pride_id}/files/{pride_id}.mzML"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            print(response.content[:500])  # Print the first 500 characters to inspect
            # Parse mzML file using pyteomics
            with mzml.read(io.BytesIO(response.content)) as spectra:
                mz_values = []
                intensity_values = []
                for spectrum in spectra:
                    mz_values.append(spectrum['m/z array'])
                    intensity_values.append(spectrum['intensity array'])

            # For simplicity, let's create a DataFrame with m/z values as features
            max_len = max(len(mz) for mz in mz_values)
            X = np.zeros((len(mz_values), max_len))
            for i, mz in enumerate(mz_values):
                X[i, :len(mz)] = mz
            
            return pd.DataFrame(X)  # Assuming intensity values or m/z values as features
        except Exception as e:
            print(f"Error processing proteomics data: {e}")
    else:
        print(f"Failed to download data from {url}")
    return None

# Main function to retrieve and analyze data
def main():
    pride_id = "PXD000561"  # Example PRIDE dataset ID
    geo_id = "GSE68719"  # Example GEO dataset ID

    proteomics_data = get_proteomics_data(pride_id)
    rnaseq_data = get_rnaseq_data(geo_id)

    # Analyze Proteomics Data
    if proteomics_data is not None:
        print("Proteomics data retrieved successfully. Processing...")
        proteomics_y = np.random.choice([0, 1], size=proteomics_data.shape[0])  # Mock labels
        analyze_data(proteomics_data, pd.Series(proteomics_y))
    else:
        print("Proteomics data could not be retrieved.")

    # Analyze RNA-seq Data
    if rnaseq_data is not None and not rnaseq_data.empty:
        print("\nRNA-seq Data Analysis:")
        rnaseq_y = np.random.choice([0, 1], size=rnaseq_data.shape[0])  # Mock labels
        analyze_data(rnaseq_data, pd.Series(rnaseq_y))
    else:
        print("RNA-seq data could not be retrieved or is empty.")

if __name__ == "__main__":
    main()

