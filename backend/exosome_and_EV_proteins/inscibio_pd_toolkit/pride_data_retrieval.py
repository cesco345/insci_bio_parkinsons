import requests
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os

def get_pride_data(pride_id, max_retries=3, retry_delay=5):
    url = f"https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{pride_id}/files"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            files = data['_embedded']['files']
            suitable_file = next((file for file in files if file['fileName'].endswith('.prot.xml')), None)
            
            if suitable_file:
                ftp_url = next((loc['value'] for loc in suitable_file['publicFileLocations'] if loc['name'] == 'FTP Protocol'), None)
                
                if ftp_url:
                    print(f"Downloading file: {suitable_file['fileName']}")
                    
                    for download_attempt in range(max_retries):
                        try:
                            with urlopen(ftp_url) as response:
                                xml_content = response.read()
                            return parse_protxml(xml_content)
                        except Exception as e:
                            print(f"Download attempt {download_attempt + 1} failed: {str(e)}")
                            if download_attempt < max_retries - 1:
                                print(f"Retrying in {retry_delay} seconds...")
                                time.sleep(retry_delay)
                            else:
                                print("All download attempts failed. Trying to use local file if available.")
                                return use_local_file(suitable_file['fileName'])
                else:
                    print("No FTP URL found for the suitable file.")
                    return use_local_file(suitable_file['fileName'])
            else:
                print("No suitable .prot.xml file found in the project.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All attempts to retrieve PRIDE data failed. Trying to use local file if available.")
                return use_local_file(pride_id + ".prot.xml")
    
    return None

def use_local_file(filename):
    if os.path.exists(filename):
        print(f"Using local file: {filename}")
        with open(filename, 'rb') as f:
            return parse_protxml(f.read())
    else:
        print(f"Local file {filename} not found.")
        return None

def parse_protxml(xml_content):
    root = ET.fromstring(xml_content)
    namespace = {'ns': 'http://regis-web.systemsbiology.net/protXML'}

    proteins = []
    for protein_group in root.findall('.//ns:protein_group', namespace):
        for protein in protein_group.findall('ns:protein', namespace):
            protein_name = protein.get('protein_name')
            probability = float(protein.get('probability', 0))
            percent_coverage = float(protein.get('percent_coverage', 0))
            peptide_count = len(protein.findall('.//ns:peptide', namespace))

            proteins.append({
                'Protein': protein_name,
                'Probability': probability,
                'Percent_Coverage': percent_coverage,
                'Peptide_Count': peptide_count
            })

    return pd.DataFrame(proteins)

def get_gene_symbols(uniprot_ids):
    base_url = "https://www.uniprot.org/uniprot/"
    gene_symbols = {}
    for uniprot_id in uniprot_ids:
        try:
            url = f"{base_url}{uniprot_id}.txt"
            response = requests.get(url)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.startswith("GN   Name="):
                        gene_symbol = line.split("=")[1].split("{")[0].strip()
                        gene_symbols[uniprot_id] = gene_symbol
                        break
            time.sleep(0.5)  # Add a small delay to avoid overloading the server
        except Exception as e:
            print(f"Error retrieving gene symbol for {uniprot_id}: {e}")
    print(f"Retrieved {len(gene_symbols)} gene symbols")
    return gene_symbols
