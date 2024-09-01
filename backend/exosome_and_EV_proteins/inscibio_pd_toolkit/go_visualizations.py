import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def shorten_go_term(term, max_length=30):
    if len(term) > max_length:
        return term[:max_length] + '...'
    return term

def plot_go_barchart(go_terms, p_values, output_file="go_barchart.png"):
    plt.figure(figsize=(12, 8))
    y_pos = np.arange(len(go_terms))
    
    # Sort terms by p-value
    sorted_indices = np.argsort(p_values)
    sorted_terms = [shorten_go_term(go_terms[i]) for i in sorted_indices]
    sorted_p_values = [p_values[i] for i in sorted_indices]
    
    plt.barh(y_pos, -np.log10(sorted_p_values), align='center', alpha=0.8)
    plt.yticks(y_pos, sorted_terms, fontsize=10)
    plt.xlabel('-log10(FDR-corrected p-value)', fontsize=12)
    plt.title('Top Enriched GO Terms', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def plot_go_bubbleplot(go_terms, p_values, output_file="go_bubbleplot.png"):
    plt.figure(figsize=(12, 8))
    
    # Sort terms by p-value
    sorted_indices = np.argsort(p_values)
    sorted_terms = [shorten_go_term(go_terms[i]) for i in sorted_indices]
    sorted_p_values = [p_values[i] for i in sorted_indices]
    
    sizes = [-np.log10(p) * 100 for p in sorted_p_values]
    
    plt.scatter(range(len(sorted_terms)), -np.log10(sorted_p_values), s=sizes, alpha=0.6)
    
    for i, term in enumerate(sorted_terms):
        plt.annotate(term, (i, -np.log10(sorted_p_values[i])), rotation=45, ha='right', va='bottom', fontsize=8)
    
    plt.xlabel('GO Terms', fontsize=12)
    plt.ylabel('-log10(FDR-corrected p-value)', fontsize=12)
    plt.title('Enriched GO Terms Bubble Plot', fontsize=14)
    plt.xticks([])  # Hide x-axis labels
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def plot_go_network(go_terms, p_values, output_file="go_network.png"):
    G = nx.Graph()
    
    # Sort terms by p-value
    sorted_indices = np.argsort(p_values)
    sorted_terms = [shorten_go_term(go_terms[i]) for i in sorted_indices]
    sorted_p_values = [p_values[i] for i in sorted_indices]
    
    # Add nodes
    for term, p_value in zip(sorted_terms, sorted_p_values):
        G.add_node(term, p_value=p_value)
    
    # Add edges (you may need to customize this based on your GO term relationships)
    for i in range(len(sorted_terms)):
        for j in range(i+1, len(sorted_terms)):
            if any(word in sorted_terms[i].lower() for word in sorted_terms[j].lower().split()):
                G.add_edge(sorted_terms[i], sorted_terms[j])
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue', alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")
    
    plt.title("GO Terms Network", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
