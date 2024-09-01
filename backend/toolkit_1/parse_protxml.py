# parse_protxml.py

import xml.etree.ElementTree as ET
import pandas as pd

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
