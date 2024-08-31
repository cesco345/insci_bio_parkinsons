import requests
import pandas as pd
from io import StringIO
from collections import Counter

def get_exocarta_proteins():
    url = "http://exocarta.org/Archive/EXOCARTA_PROTEIN_MRNA_DETAILS_5.txt"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text), sep='\t')
        return data
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")

def analyze_exocarta_data(data):
    print(f"Retrieved {len(data)} entries from ExoCarta")
    print("\nColumns in the dataset:")
    print(data.columns.tolist())
    
    print("\nFirst few rows:")
    print(data.head())
    
    print("\nData types of columns:")
    print(data.dtypes)
    
    if 'CONTENT TYPE' in data.columns:
        content_type_counts = data['CONTENT TYPE'].value_counts()
        print("\nContent type distribution:")
        print(content_type_counts)
    
    if 'METHODS' in data.columns:
        all_methods = data['METHODS'].str.split('|', expand=True).stack()
        method_counts = Counter(all_methods)
        print("\nTop 10 most common methods:")
        for method, count in method_counts.most_common(10):
            print(f"{method}: {count}")

try:
    exocarta_data = get_exocarta_proteins()
    analyze_exocarta_data(exocarta_data)
except Exception as e:
    print(f"An error occurred: {str(e)}")
