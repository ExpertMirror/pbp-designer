import os
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem

def compute_tanimoto(smiles1, smiles2):
    """
    Compute Tanimoto similarity between two SMILES strings.
    """

    # Convert SMILES → RDKit molecule objects
    mol1 = Chem.MolFromSmiles(smiles1)
    mol2 = Chem.MolFromSmiles(smiles2)

    # Basic validation
    if mol1 is None:
        raise ValueError(f"Invalid first SMILES: {smiles1}")
    if mol2 is None:
        raise ValueError(f"Invalid second SMILES: {smiles2}")

    # Generate Morgan fingerprints (ECFP4 equivalent: radius=2)
    fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, radius=2, nBits=2048)
    fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, radius=2, nBits=2048)

    # Compute Tanimoto similarity
    similarity = DataStructs.TanimotoSimilarity(fp1, fp2)

    return similarity

def find_library():
    names = []
    os.chdir('./chemistry/ligand_lib')
    for file in os.listdir():
        if file.endswith(".txt"):
            name = os.path.splitext(file)[0]
            names.append(name)
    return names

def build_library(names):
    codes = []

    for name in names:
        with open(f"{name}.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

            if len(lines) == 1:
                codes.append(lines[0])
            else:
                codes.append(lines)
    return codes

def compute_scores(codes, input_code):
    scores = []

    for entry in codes:
        if isinstance(entry, str):
            # single SMILES
            score = compute_tanimoto(input_code, entry)
            scores.append(score)

        elif isinstance(entry, list):
            # multiple SMILES
            multi_scores = []
            for smi in entry:
                score = compute_tanimoto(input_code, smi)
                multi_scores.append(score)
            scores.append(multi_scores)

    return scores

def find_scaffold(names, scores):
    max = -1
    id = -1
    for entry in scores:
        if isinstance(entry, float):
            if entry > max:
                max = entry
                id = scores.index(entry)
        elif isinstance(entry, list):
            for score in entry:
                if score > max:
                    max = score
                    id = scores.index(entry)
    scaffold = names[id]
    print(f"Scaffold protein assigned: {scaffold}\nLigand similarity = {max * 100} %")
    return scaffold
