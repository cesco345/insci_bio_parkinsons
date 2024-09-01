# main.py

import time
from fetch_pride_data import get_pride_data
from parse_protxml import parse_protxml
from gene_symbol_retrieval import get_gene_symbols
from visualize_data import visualize_proteomics_data

if __name__ == "__main__":
    pride_id = "PXD020794"  # Example PRIDE dataset identifier

    # Timing the data fetching
    start_time = time.time()
    xml_content = get_pride_data(pride_id)
    print(f"Fetching data took {time.time() - start_time} seconds")

    if xml_content:
        # Timing the XML parsing
        start_time = time.time()
        df_proteins = parse_protxml(xml_content)
        print(f"Parsing XML took {time.time() - start_time} seconds")

        if not df_proteins.empty:
            print(df_proteins.head())

            # Timing the visualization
            start_time = time.time()
            visualize_proteomics_data(df_proteins)
            print(f"Visualization took {time.time() - start_time} seconds")

            # Timing the gene symbol retrieval
            start_time = time.time()
            uniprot_ids = df_proteins['Protein'].unique()
            gene_symbols = get_gene_symbols(uniprot_ids)
            df_proteins['Gene_Symbol'] = df_proteins['Protein'].map(gene_symbols)
            print(f"Gene symbol retrieval took {time.time() - start_time} seconds")

            # Save the final DataFrame to a CSV file
            df_proteins.to_csv(f"{pride_id}_proteomics_data.csv", index=False)
            print(f"Data saved to {pride_id}_proteomics_data.csv")
        else:
            print("No data available for analysis.")
    else:
        print("Failed to retrieve or parse the PRIDE data.")


