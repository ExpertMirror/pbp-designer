import os
import subprocess as sp
from unittest import result
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

def convert_ligand(smiles, name):
    base_dir = os.getcwd()
    os.makedirs(os.path.join(base_dir, "docking", "prep"), exist_ok=True)
    prep_dir = os.path.join(base_dir, "docking", "prep")
    sif_path = os.path.join(base_dir, "docking", "converter.sif")
    os.makedirs(prep_dir, exist_ok=True)

    sdf_path = os.path.join(prep_dir, f"{name}_ligand.sdf")

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)
    Chem.MolToMolFile(mol, sdf_path)

    cmd = [
        "apptainer", "exec",
        "-B", f"{prep_dir}:/prep",
        f"{sif_path}",
        "mk_prepare_ligand.py",
        "-i", f"/prep/{name}_ligand.sdf",
        "-o", f"/prep/{name}_ligand_prepared.pdbqt"
    ]

    print("Running:", " ".join(cmd))
    result = sp.run(cmd, text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError("Ligand prep failed")

def get_pdb(name):
    base_dir = os.getcwd()
    pdb_path = os.path.join(base_dir, "outs", "colabfold", name)
    pdbs = [f for f in os.listdir(pdb_path) if os.path.isfile(os.path.join(pdb_path, f))]
    try:
        for pdb in pdbs:
            if 'rank_001' in pdb and '.pdb' in pdb:
                top_pdb=pdb
    except Exception as e:
        print(f"Error processing colabfold output files: {e}")


    print(f"Top ranked ColabFold structure: {top_pdb}")

    prep_dir = os.makedirs(os.path.join(base_dir, "docking", "prep"), exist_ok=True)

    cmd = [
        "cp", os.path.join(pdb_path, top_pdb), os.path.join(f"{base_dir}", "docking", "prep", f"{name}.pdb")
    ]


    sp.run(cmd, check=True)

def convert_protein(name):
    base_dir = os.getcwd()
    prep_dir = os.path.join(base_dir, "docking", "prep")
    sif_path = os.path.join(base_dir, "docking", "converter.sif")
    os.makedirs(prep_dir, exist_ok=True)
    pdbqt_path = os.path.join(prep_dir, f"{name}_protein_prepared.pdbqt")

    cmd = [
        "apptainer", "exec",
        "-B", f"{prep_dir}:/prep",
        f"{sif_path}",
        "bash", "-c",
        f"obabel /prep/{name}.pdb -O /prep/{name}_protein_prepared.pdbqt -xh -d"
    ]

    print("Running:", " ".join(cmd))
    sp.run(cmd, check=True)

    # ensure output exists
    if not os.path.exists(pdbqt_path):
        raise RuntimeError("PDBQT conversion failed: file not created")

def fix_receptor_pdbqt(name):
    remove = {"ROOT", "ENDROOT", "BRANCH", "ENDBRANCH", "TORSDOF"}

    base_dir = os.getcwd()
    filepath = os.path.join(base_dir, "docking", "prep", f"{name}_protein_prepared.pdbqt")
    with open(filepath) as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if any(line.startswith(tag) for tag in remove):
            continue
        cleaned.append(line)

    with open(filepath, "w") as f:
        f.writelines(cleaned)

def compute_protein_grid_box(name, padding = 5.0):
    coords = []
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, "docking", "prep", f"{name}_protein_prepared.pdbqt")

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    coords.append((x, y, z))
                except ValueError:
                    print(f"Warning: Could not parse coordinates in {name}_protein_prepared.pdbqt at line: {line.strip()}")

    coords = np.array(coords)
    if coords.size == 0:
        raise ValueError(f"No valid coordinates found in {name}_protein_prepared.pdbqt")
    min_xyz = coords.min(axis=0)
    max_xyz = coords.max(axis=0)

    center = (min_xyz + max_xyz) / 2
    size = (max_xyz - min_xyz) + (2 * padding)

    return tuple(center), tuple(size)

def write_config(name, center, size):

    cx, cy, cz = center
    sx, sy, sz = size
    base_dir = os.getcwd()
    config_path = os.path.join(base_dir, "docking", "prep", f"{name}_config.txt")

    with open(config_path, 'w') as f:
        f.write(f"receptor = /prep/{name}_protein_prepared.pdbqt\n")
        f.write(f"ligand = /prep/{name}_ligand_prepared.pdbqt\n\n")

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
    base_dir = os.getcwd()
    config_path = os.path.join(base_dir, "docking", "prep", f"{name}_config.txt")
    output_path = os.path.join(base_dir, "docking", "prep", f"{name}_vina_out.pdbqt")
    os.makedirs(os.path.join(base_dir, "outs", "vina", name), exist_ok=True)
    log_path = os.path.join(base_dir, "outs", "vina", name, f"{name}_vina.log")
    vina_sif = os.path.join(base_dir, "docking", "vina.sif")
    prep_dir = os.path.join(base_dir, "docking", "prep")
    cmd = [
        "apptainer", "exec",
        "-B", f"{prep_dir}:/prep",
        f"{vina_sif}",
        "vina",
        "--config", f"{config_path}",
        "--out", f"{output_path}"
    ]

    print("Running:", " ".join(cmd))

    with open(log_path, "w") as log_file:
        sp.run(cmd, check=True, stdout=log_file, stderr=log_file)
