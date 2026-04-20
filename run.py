import init
import sys
import os
from chemistry import compute_similarity as cs
from boltzgen import run_boltzgen as rb


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
    rb.write_yaml(scaffold, ligand_smiles, project_name)
    rb.activate_boltzgen(project_name)


if __name__=="__main__":
    main()
