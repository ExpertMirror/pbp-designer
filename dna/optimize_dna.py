import os
from dnachisel import DnaOptimizationProblem
from dnachisel.biotools import reverse_translate

def append_fret_proteins(name, sequence):
    binder_seq = sequence
    base_dir = os.getcwd()
    fret_dir = os.path.join(base_dir, "dna", "fret_seqs")

    cfp_path = os.path.join(fret_dir, "cfp.fasta")
    yfp_path = os.path.join(fret_dir, "yfp.fasta")

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
    in_frame = len(optimized_dna) % 3 == 0
    print(f"Checking sequence is in-frame: {in_frame}")
    if not in_frame:
        raise ValueError("Optimized DNA sequence is not in-frame.")


    return optimized_dna
