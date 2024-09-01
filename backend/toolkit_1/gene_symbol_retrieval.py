# gene_symbol_retrieval.py

import requests
import time

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
