from go_analysis import perform_go_analysis

# Sample list of novel proteins (NCBI gene IDs)
novel_proteins = ['338', '348', '351', '355', '358', '7054', '7040', '2335', '4478', '57817']

# Perform GO analysis
go_output_file = "test_go_enrichment_results.txt"
go_results = perform_go_analysis(novel_proteins, go_output_file)

if go_results:
    print("\nTop 10 enriched GO terms:")
    for i, r in enumerate(sorted(go_results, key=lambda r: r.p_fdr_bh)[:10]):
        print(f"{i+1}. {r.name} (FDR-corrected p-value: {r.p_fdr_bh:.2e})")
else:
    print("\nNo enriched GO terms found. Check the gene IDs and ensure they are in the correct format.")
