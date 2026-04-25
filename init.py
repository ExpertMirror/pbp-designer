from rdkit import Chem
import sys
import os

def opening():
    message = """Welcome to PBP Designer! A pipeline for building new protein-based FRET biosensors.
This pipeline is designed to be user-friendly and accessible to researchers of all levels of experience. 
All that is required from you is a SMILES code for you ligand of interest, and a name for your project.
Smiles codes can be found from PubChem at: https://pubchem.ncbi.nlm.nih.gov/
For instructions and information on how to use the PBP Designer pipeline, please refer to our 
GitHub repository at: https://github.com/ExpertMirror/pbp-designer
"""
    print(message)

def validate_smiles(smiles):
    print(f"Checking SMILES code '{smiles}'..." , end="")
    try:
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            print("Error: Invalid SMILES string.")
            return False
        else:
            print("Success")

    except Exception as e:
        print(f"Unexpected error during conversion: {e}")
        return False
    
def print_project(project_name):
        print(f"Beginning project '{project_name}'.")
        return
