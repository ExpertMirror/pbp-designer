import os
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.SeqUtils import seq1

def extract_seq(name):
    base_dir = os.getcwd()
    boltz_out = os.path.abspath(os.path.join(base_dir, f"../outs/boltzgen/{name}/final_ranked_designs/final_30_designs"))
    os.chdir(boltz_out)
    cifs = [f for f in os.listdir(boltz_out) if os.path.isfile(os.path.join(boltz_out, f))]
    for cif in cifs:
        try:
            if 'rank01' in cif and '.cif' in cif:
                top_res=cif
        except Exception as e:
            print(f"Error processing file {cif}: {e}")
    print(f"Top ranked design: {top_res}")

    parser = MMCIFParser()
    structure = parser.get_structure('design', top_res)

    for model in structure:
        if 'A' not in model:
            raise ValueError("Chain A not found")

        chain = model['A']

        seq = []
        for residue in chain:
            seq.append(seq1(residue.get_resname()))

        print(f"Chain {chain.id}: {''.join(seq)}")


def main():
    extract_seq('proline1')


if __name__ == "__main__":
    main()
