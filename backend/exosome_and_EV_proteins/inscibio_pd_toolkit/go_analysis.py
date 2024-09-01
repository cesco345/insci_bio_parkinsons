import os
import re
from goatools import obo_parser
from goatools.go_enrichment import GOEnrichmentStudy
from goatools.base import download_go_basic_obo

def clean_gene_symbol(symbol):
    return re.sub(r';.*$', '', symbol).strip()

def perform_go_analysis(novel_proteins, output_file):
    print(f"\nStarting GO analysis with {len(novel_proteins)} novel proteins")
    
    # Clean gene symbols and convert to upper case
    novel_proteins = [clean_gene_symbol(gene).upper() for gene in novel_proteins]
    
    # Load GO-basic.obo file
    go_obo = "go-basic.obo"
    if not os.path.exists(go_obo):
        download_go_basic_obo(go_obo)
    go = obo_parser.GODag(go_obo)

    # Load gene2go file
    gene2go = "gene2go"
    if not os.path.exists(gene2go):
        os.system(f"wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz")
        os.system(f"gunzip gene2go.gz")

    # Create mappings
    geneid_to_go = {}
    symbol_to_geneid = {}

    # Manually parse gene2go file
    print("Parsing gene2go file...")
    with open(gene2go, 'r') as f:
        next(f)  # Skip header
        for line in f:
            fields = line.strip().split('\t')
            if fields[0] == '9606':  # Human taxid
                gene_id, symbol, go_id = fields[1], fields[2].upper(), fields[5]
                if gene_id not in geneid_to_go:
                    geneid_to_go[gene_id] = set()
                geneid_to_go[gene_id].add(go_id)
                symbol_to_geneid[symbol] = gene_id

    print(f"Parsed {len(geneid_to_go)} unique gene IDs")
    print(f"Parsed {len(symbol_to_geneid)} unique gene symbols")

    # Debug: Print some entries from symbol_to_geneid
    print("\nSample entries from symbol_to_geneid:")
    for symbol in list(symbol_to_geneid.keys())[:10]:
        print(f"{symbol}: {symbol_to_geneid[symbol]}")

    # Debug: Print some novel proteins
    print("\nSample novel proteins:")
    print(novel_proteins[:10])

    # Map novel proteins to NCBI gene IDs
    study_genes = set()
    unmapped_genes = []
    for gene in novel_proteins:
        if gene in symbol_to_geneid:
            study_genes.add(symbol_to_geneid[gene])
        else:
            unmapped_genes.append(gene)

    print(f"Mapped {len(study_genes)} out of {len(novel_proteins)} novel proteins to NCBI gene IDs")
    if unmapped_genes:
        print(f"Warning: Could not map {len(unmapped_genes)} genes: {', '.join(unmapped_genes[:10])}{'...' if len(unmapped_genes) > 10 else ''}")

    if not study_genes:
        print("No genes could be mapped for GO analysis. Check if the gene symbols are correct.")
        return None, None, None

    # Define background genes (all human genes)
    background_genes = set(geneid_to_go.keys())

    # Perform GO enrichment analysis
    goeaobj = GOEnrichmentStudy(
        background_genes,
        geneid_to_go,
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
        
        # Extract GO terms and p-values for visualization
        go_terms = [r.name for r in goea_results if r.p_fdr_bh < 0.05]  # Only significant terms
        p_values = [r.p_fdr_bh for r in goea_results if r.p_fdr_bh < 0.05]
        
        return goea_results, go_terms, p_values
    else:
        print("No enriched GO terms found.")
        return None, None, None
