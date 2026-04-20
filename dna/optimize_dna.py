import os
from dnachisel import DnaOptimizationProblem
from dnachisel.biotools import reverse_translate

def append_fret_proteins(name):
    base_dir = os.getcwd()
    binder_dir = os.path.join(base_dir, f"{name}.fasta")
    fret_dir = os.path.join(base_dir, "fret_seqs")

    cfp_path = os.path.join(fret_dir, "cfp.fasta")
    yfp_path = os.path.join(fret_dir, "yfp.fasta")

    with open(binder_dir, 'r') as f:
        binder_content = f.read()
    
    binder_seq = binder_content.splitlines()[0]  # Get the sequence line

    with open(cfp_path, 'r') as f:
        cfp_content = f.read()

    cfp_seq = cfp_content.splitlines()[0]  # Get the sequence line

    with open(yfp_path, 'r') as f:
        yfp_content = f.read()

    yfp_seq = yfp_content.splitlines()[0]  # Get the sequence line

    fret_seq = cfp_seq + binder_seq + yfp_seq

    return fret_seq

def optimized_ecoli_dna(protein_seq):
    problem = DnaOptimizationProblem(
        sequence=reverse_translate(protein_seq),
        constraints=[],
        objectives=[]
    )

    problem.optimize()
    optimized_dna = problem.sequence
    print(f"Optimized DNA sequence:\n{optimized_dna}")
    print(f"Checking sequence is in-frame: {len(optimized_dna) % 3 == 0}")


def main():
    fret_protein = append_fret_proteins("hisj_pro")
    optimized_ecoli_dna(fret_protein)

if __name__ == "__main__":
    main()
