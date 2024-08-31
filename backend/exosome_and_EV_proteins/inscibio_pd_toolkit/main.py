from pride_data_retrieval import get_pride_data, get_gene_symbols
from protein_comparison import get_exocarta_proteins, get_vesiclepedia_proteins, compare_proteins, plot_novel_proteins
from go_analysis import perform_go_analysis
from go_visualizations import plot_go_barchart, plot_go_bubbleplot, plot_go_network

def main():
    pride_id = "PXD020794"
    data = get_pride_data(pride_id)

    if data is not None:
        pd_ndev_uniprot_ids = data['Protein'].tolist()
        print(f"Number of proteins in PD-NDsEV dataset: {len(pd_ndev_uniprot_ids)}")
        print("First 10 UniProt IDs:", pd_ndev_uniprot_ids[:10])

        # Convert UniProt IDs to gene symbols
        uniprot_to_gene = get_gene_symbols(pd_ndev_uniprot_ids)
        pd_ndev_gene_symbols = [uniprot_to_gene.get(uniprot_id, uniprot_id) for uniprot_id in pd_ndev_uniprot_ids]
        print("First 10 gene symbols:", pd_ndev_gene_symbols[:10])

        exocarta_proteins = get_exocarta_proteins()
        vesiclepedia_proteins = get_vesiclepedia_proteins()

        novel_proteins, in_exocarta, in_vesiclepedia = compare_proteins(pd_ndev_gene_symbols, exocarta_proteins, vesiclepedia_proteins)

        print("\nTop 10 potentially novel exosomal proteins (gene symbols):")
        print(list(novel_proteins)[:10])

        print("\nTop 10 proteins found in ExoCarta:")
        print(list(in_exocarta)[:10])

        print("\nTop 10 proteins found in Vesiclepedia:")
        print(list(in_vesiclepedia)[:10])

        # Additional analysis on novel proteins
        novel_protein_data = data[data['Protein'].isin([uniprot_id for uniprot_id, gene in uniprot_to_gene.items() if gene in novel_proteins])]
        print("\nStatistics for potentially novel exosomal proteins:")
        print(novel_protein_data.describe())

        # Plot distribution of novel proteins
        plot_novel_proteins(novel_protein_data)

        # Perform GO analysis on novel proteins
        go_output_file = "go_enrichment_results.txt"
        go_results, go_terms, p_values = perform_go_analysis(novel_proteins, go_output_file)

        if go_results and go_terms and p_values:
            print("\nTop 10 enriched GO terms:")
            for i, (term, p_value) in enumerate(zip(go_terms[:10], p_values[:10])):
                print(f"{i+1}. {term} (FDR-corrected p-value: {p_value:.2e})")
            
            # Generate GO visualizations
            plot_go_barchart(go_terms[:10], p_values[:10])
            plot_go_bubbleplot(go_terms[:10], p_values[:10])
            plot_go_network(go_terms[:10], p_values[:10])
        else:
            print("\nNo significant enriched GO terms found. This could be due to:")
            print("1. The novel proteins are not well-annotated in GO databases.")
            print("2. The novel proteins have diverse functions without significant enrichment.")
            print("3. Issues with mapping gene symbols to NCBI gene IDs.")
            print("\nConsider manual investigation of the novel proteins or using alternative annotation databases.")

        print("\nFirst 10 cleaned gene symbols:")
        print([gene.split(';')[0].strip() for gene in list(novel_proteins)[:10]])

    else:
        print("Failed to retrieve data from PRIDE. Please check the project ID and try again.")

if __name__ == "__main__":
    main()
