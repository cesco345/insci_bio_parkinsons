import matplotlib.pyplot as plt
import seaborn as sns

def visualize_proteomics_data(df):
    # First Plot: Probability Barplot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df.head(10), x='Protein', y='Probability')
    plt.title('Top 10 Proteins by Probability')
    plt.xlabel('Protein')
    plt.ylabel('Probability')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show(block=True)  # Ensure this plot is shown and waits for close
    plt.close()  # Explicitly close to release resources

    # Second Plot (for example): Coverage Barplot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df.head(10), x='Protein', y='Percent_Coverage')
    plt.title('Top 10 Proteins by Percent Coverage')
    plt.xlabel('Protein')
    plt.ylabel('Percent Coverage')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show(block=True)  # Ensure this plot is shown and waits for close
    plt.close()  # Explicitly close to release resources

    # Third Plot (example): Peptide Count
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df.head(10), x='Protein', y='Peptide_Count')
    plt.title('Top 10 Proteins by Peptide Count')
    plt.xlabel('Protein')
    plt.ylabel('Peptide Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show(block=True)  # Ensure this plot is shown and waits for close
    plt.close()  # Explicitly close to release resources



