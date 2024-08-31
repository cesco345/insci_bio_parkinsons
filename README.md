# InSci Bio Tools: Neurological Disease Exosome Analysis Toolkit

## Overview

InSci Bio Tools is a comprehensive toolkit for analyzing exosomal proteins in neurological diseases, with a focus on Parkinson's Disease (PD). This suite of tools enables researchers to identify novel exosomal proteins, compare them with existing databases, and perform Gene Ontology (GO) enrichment analysis. The results are visualized through various plots, facilitating the interpretation of complex proteomic data.

## Importance in Drug Discovery

Exosomes are small extracellular vesicles that play crucial roles in intercellular communication and disease progression. In the context of neurological disorders like Parkinson's Disease, exosomes have emerged as:

1. Potential biomarkers for early disease detection and progression monitoring.
2. Targets for therapeutic interventions.
3. Delivery vehicles for drugs across the blood-brain barrier.

This InSci Bio toolkit aids drug discovery efforts by:

- Identifying novel exosomal proteins that could serve as drug targets or biomarkers.
- Comparing disease-specific exosomal proteins with established databases to highlight unique features.
- Providing functional insights through GO enrichment analysis, which can guide drug development strategies.
- Offering clear visualizations to help researchers quickly interpret complex data and form hypotheses.

## Features

1. **PRIDE Data Retrieval**: Fetch proteomic data from the PRIDE database.
2. **Protein Comparison**: Compare identified proteins with ExoCarta and Vesiclepedia databases.
3. **Novel Protein Identification**: Highlight potentially novel exosomal proteins.
4. **GO Enrichment Analysis**: Perform functional analysis of identified proteins.
5. **Data Visualization**: Generate informative plots including:
   - Venn diagrams for protein overlap
   - Scatter plots for novel protein characteristics
   - Bar charts, bubble plots, and network graphs for GO terms

## Installation

```bash
git clone https://github.com/your-username/insci_bio_parkinsons.git
cd insci_bio_parkinsons
pip install -r requirements.txt
```

## Usage

Run the main analysis script:

```bash
python main.py
```

This will execute the entire workflow, including data retrieval, analysis, and visualization.

## File Description

- `main.py`: Orchestrates the entire analysis workflow.
- `pride_data_retrieval.py`: Handles fetching and parsing data from the PRIDE database.
- `protein_comparison.py`: Compares proteins with ExoCarta and Vesiclepedia databases.
- `go_analysis.py`: Performs GO enrichment analysis.
- `go_visualizations.py`: Generates visualizations for GO analysis results.

## Output

- `go_enrichment_results.txt`: Detailed results of the GO enrichment analysis.
- `go_barchart.png`: Bar chart of top enriched GO terms.
- `go_bubbleplot.png`: Bubble plot of enriched GO terms.
- `go_network.png`: Network visualization of GO term relationships.

## Contributing

Contributions to InSci Bio Parkinson's are welcome! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Citation

If you use InSci Bio Parkinson's toolkit in your research, please cite:

```
[Francesco Piscani]. (2024). InSci Bioscience: Neurological Disease Exosome Analysis Toolkit. GitHub repository, https://github.com/cesco345/insci_bio_parkinsons
```

## Contact

[Francesco Piscani] - [fpiscani@inscibioscience.com]

Project Link: [https://github.com/cesco345/insci_bio_parkinsons](https://github.com/cesco345/insci_bio_parkinsons)
