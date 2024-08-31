def perform_go_analysis(novel_proteins, output_file):
    print(f"\nStarting GO analysis with {len(novel_proteins)} novel proteins")
    
    # Clean gene symbols and convert to upper case
    novel_proteins = [clean_gene_symbol(gene).upper() for gene in novel_proteins]
    
    # Load GO-basic.obo file
    go_obo = "go-basic.obo"
    if not os.path.exists(go_obo):
        os.system(f"wget http://purl.obolibrary.org/obo/go/go-basic.obo")
    go = obo_parser.GODag(go_obo)

    # Load gene2go file
    gene2go = "gene2go"
    if not os.path.exists(gene2go):
        os.system(f"wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz")
        os.system(f"gunzip gene2go.gz")

    # Read gene associations
    geneid2gos = read_ncbi_gene2go(gene2go, taxids=[9606])  # 9606 is the taxid for human

    # Define background genes (all human genes)
    background_genes = set(geneid2gos.keys())

    # Convert gene symbols to NCBI gene IDs
    symbol_to_geneid = {}
    with open(gene2go) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if fields[0] == "9606":  # Human taxid
                symbol_to_geneid[fields[2].upper()] = fields[1]
    
    # Print the first 10 items in symbol_to_geneid for debugging
    print("\nFirst 10 items in symbol_to_geneid:")
    print(list(symbol_to_geneid.items())[:10])

    # More flexible mapping approach
    study_genes = set()
    for gene in novel_proteins:
        if gene in symbol_to_geneid:
            study_genes.add(symbol_to_geneid[gene])
        else:
            # Try to find a partial match
            matches = [geneid for symbol, geneid in symbol_to_geneid.items() if gene in symbol]
            if matches:
                study_genes.add(matches[0])
    
    print(f"Mapped {len(study_genes)} out of {len(novel_proteins)} novel proteins to NCBI gene IDs")
    
    # Print the first 10 mapped genes for debugging
    print("\nFirst 10 mapped genes:")
    print(list(study_genes)[:10])

    if not study_genes:
        print("No genes could be mapped for GO analysis. Check if the gene symbols are correct.")
        return None

    # Perform GO enrichment analysis
    goeaobj = GOEnrichmentStudy(
        background_genes,
        geneid2gos,
        go,
        propagate_counts=False,
        alpha=0.05,
        methods=['fdr_bh']
    )

    goea_results = goeaobj.run_study(study_genes)

    if goea_results:
        # Write results to file
        goeaobj.wr_txt(output_file, goea_results)
        print(f"GO enrichment analysis completed. Results written to {output_file}")
        return goea_results
    else:
        print("No enriched GO terms found.")
        return None
