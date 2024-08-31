import requests
import pandas as pd
from io import StringIO

# Function to retrieve data from ExoCarta
def get_exocarta_proteins():
    url = "http://exocarta.org/Archive/EXOCARTA_PROTEIN_MRNA_DETAILS_5.txt"
    
    response = requests.get(url)
    if response.status_code == 200:
        # Read the tab-separated file into a pandas DataFrame
        data = pd.read_csv(StringIO(response.text), sep='\t')
        return data
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")

# Main code block
try:
    exocarta_data = get_exocarta_proteins()
    print(f"Retrieved {len(exocarta_data)} entries from ExoCarta\n")

    print("Columns in the dataset:")
    print(exocarta_data.columns)
    
    print("\nFirst few rows:")
    print(exocarta_data.head())

    print("\nData types of columns:")
    print(exocarta_data.dtypes)

    print("\nContent type distribution:")
    content_type_distribution = exocarta_data['CONTENT TYPE'].value_counts()
    print(content_type_distribution)

    print("\nTop 10 most common methods:")
    methods_distribution = exocarta_data['METHODS'].value_counts().head(10)
    print(methods_distribution)

    # Filter for human proteins
    human_proteins = exocarta_data[exocarta_data['SPECIES'] == 'Homo sapiens']

    print(f"\nNumber of human proteins: {len(human_proteins)}")
    print(human_proteins.head())  # Display the first few rows of human proteins

    # Explore content types specific to human proteins
    human_content_type_distribution = human_proteins['CONTENT TYPE'].value_counts()
    print("\nContent type distribution for human proteins:")
    print(human_content_type_distribution)

    # Explore the most common methods used for human proteins
    human_methods_distribution = human_proteins['METHODS'].value_counts().head(10)
    print("\nTop 10 most common methods for human proteins:")
    print(human_methods_distribution)

    # Save the filtered human proteins data to a CSV file
    human_proteins.to_csv("human_exocarta_proteins.csv", index=False)
    print("\nFiltered human proteins data has been saved to 'human_exocarta_proteins.csv'.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

