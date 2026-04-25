import os
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.SeqUtils import seq1

def extract_seq(name):
    base_dir = os.getcwd()
    boltz_out = os.path.join(base_dir, "outs", "boltzgen", name, "final_ranked_designs", "final_30_designs")

    cifs = [f for f in os.listdir(boltz_out) if os.path.isfile(os.path.join(boltz_out, f))]
    for cif in cifs:
        try:
            if 'rank1' in cif and '.cif' in cif:
                top_res=cif
        except Exception as e:
            print(f"Error processing file {cif}: {e}")
    print(f"Top ranked BoltzGen design: {top_res}")

    parser = MMCIFParser()
    cif_path = os.path.join(boltz_out, top_res)
    structure = parser.get_structure('design', cif_path)

    for model in structure:
        if 'A' not in model:
            raise ValueError("Chain A not found. BoltzGen protein design may have failed. Please check the BoltzGen output for errors.")

        chain = model['A']

        seq = []
        for residue in chain:
            seq.append(seq1(residue.get_resname()))

        print(f"Chain {chain.id}: {''.join(seq)}")

    return ''.join(seq)
