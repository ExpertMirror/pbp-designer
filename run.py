import init
import sys
from chemistry import compute_similarity as cs

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <SMILES> <project_name>", flush=True)
        sys.exit(1)
    project_name=sys.argv[2]
    ligand_smiles = sys.argv[1]
    init.opening()
    init.print_project(project_name)
    init.validate_smiles(ligand_smiles)
    names = cs.find_library()
    codes = cs.build_library(names)
    scores = cs.compute_scores(codes, ligand_smiles)
    scaffold = cs.find_scaffold(names,scores)


if __name__=="__main__":
    main()
