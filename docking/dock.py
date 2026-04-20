import os
import subprocess as sp
from unittest import result
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

def convert_ligand(smiles, name):
    base_dir = os.getcwd()
    prep_dir = os.path.abspath("prep")

    sdf_path = os.path.join(prep_dir, f"{name}.sdf")

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)
    Chem.MolToMolFile(mol, sdf_path)

    cmd = [
        "apptainer", "exec",
        "-B", f"{prep_dir}:/prep",
        "converter.sif",
        "mk_prepare_ligand.py",
        "-i", f"/prep/{name}.sdf",
        "-o", f"/prep/{name}_prepared.pdbqt"
    ]

    print("Running:", " ".join(cmd))
    sp.run(cmd, check=True)

def convert_protein(name):
    base_dir = os.getcwd()
    prep_dir = os.path.abspath("prep")
    pdb_path = os.path.join(prep_dir, f"{name}.pdb")
    pdbqt_path = os.path.join(prep_dir, f"{name}_prepared.pdbqt")

    cmd = [
        "apptainer", "exec",
        "-B", f"{prep_dir}:/prep",
        "converter.sif",
        "mk_prepare_receptor.py",
        "-i", f"/prep/{name}.pdb",
        "-o", f"/prep/{name}_prepared", "-p",
        "--delete_residues", "HOH"
    ]
    print("Running:", " ".join(cmd))
    sp.run(cmd, check=True)


def compute_protein_grid_box(name, padding = 5.0):
    coords = []

    file_path = os.path.abspath(os.path.join("prep", f"{name}_prepared.pdbqt"))

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    coords.append((x, y, z))
                except ValueError:
                    print(f"Warning: Could not parse coordinates in {name}_prepared.pdbqt at line: {line.strip()}")
                
    coords = np.array(coords)
    if coords.size == 0:
        raise ValueError(f"No valid coordinates found in {name}_prepared.pdbqt")
    min_xyz = coords.min(axis=0)
    max_xyz = coords.max(axis=0)

    center = (min_xyz + max_xyz) / 2
    size = (max_xyz - min_xyz) + (2 * padding)

    return tuple(center), tuple(size)

def write_config(name, ligand_name, center, size):

    cx, cy, cz = center
    sx, sy, sz = size
    config_path = os.path.join("prep", f"{name}_config.txt")
    
    with open(config_path, 'w') as f:
        f.write(f"receptor = /prep/{name}_prepared.pdbqt\n")
        f.write(f"ligand = /prep/{ligand_name}_prepared.pdbqt\n\n")

        f.write(f"center_x = {cx:.3f}\n")
        f.write(f"center_y = {cy:.3f}\n")
        f.write(f"center_z = {cz:.3f}\n\n")
        
        f.write(f"size_x = {sx:.3f}\n")
        f.write(f"size_y = {sy:.3f}\n")
        f.write(f"size_z = {sz:.3f}\n\n")

        f.write("exhaustiveness = 8\n")
        f.write("num_modes = 10\n")
        f.write("energy_range = 3\n")

def run_vina(name):
    config_path = os.path.join("prep", f"{name}_config.txt")
    output_path = os.path.join("prep", f"{name}_docked.pdbqt")
    log_path = os.path.join("prep", f"{name}_vina.log")

    cmd = [
        "apptainer", "exec",
        "-B", f"{os.path.abspath('prep')}:/prep",
        "vina.sif",
        "vina",
        "--config", f"/prep/{name}_config.txt",
        "--out", f"/prep/{name}_docked.pdbqt"
    ]

    print("Running:", " ".join(cmd))

    with open(log_path, "w") as log_file:
        sp.run(cmd, check=True, stdout=log_file, stderr=log_file)






def main():
    convert_ligand("CC1=C(C(=O)NC(=O)N1)C2=CC=CC=C2", "proline")
    convert_protein("hisj_pro")
    center, size = compute_protein_grid_box("hisj_pro")
    write_config("hisj_pro", "proline", center, size)
    run_vina("hisj_pro")


if __name__ == "__main__":
    main()
