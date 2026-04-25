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
    ligand_dir = os.path.join(os.getcwd(), "chemistry", "ligand_lib")
    for file in os.listdir(ligand_dir):
        if file.endswith(".txt"):
            name = os.path.splitext(file)[0]
            names.append(name)
    return names

def build_library(names):
    codes = []
    ligand_dir = os.path.join(os.getcwd(), "chemistry", "ligand_lib")

    for name in names:
        with open(os.path.join(ligand_dir, f"{name}.txt"), "r") as f:
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

def check_smiles_type(smiles):
    ORGANIC_ATOMIC_NUMS = {1, 6, 7, 8, 9, 15, 16, 17, 35, 53}  # H, C, N, O, F, P, S, Cl, Br, I

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    
    mol = Chem.AddHs(mol)  # Add explicit hydrogens

    n_atoms = mol.GetNumAtoms()
    total_charge = Chem.GetFormalCharge(mol)

    if total_charge != 0:
        print(f"User input is an ion: {smiles}")
        return "ion"
    if n_atoms == 1:
        print(f"User input is an atom: {smiles}")
        raise ValueError("Uncharged, single atoms are not supported. PBPs cannot bind single atoms. Please provide a valid molecule.")
    print (f"User input is a compound: {smiles}")
    return "compound"
