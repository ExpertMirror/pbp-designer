import os
import json
import numpy as np
import csv

def get_colabfold_out(name):

    base_dir = os.getcwd()
    colab_outs = os.path.join(base_dir, "outs", "colabfold", name)
    pipeline_outs = os.path.join(base_dir, "outs")

    json_file = None
    for f in os.listdir(colab_outs):
        if 'rank_001' in f and f.endswith('.json'):
            json_file = os.path.join(colab_outs, f)
            break

    if json_file is None:
        raise FileNotFoundError("No JSON file found in the specified directory.")
    
    with open(json_file, 'r') as f:
        data = json.load(f)

    ptm = data.get('ptm', data.get('pTM'))
    if ptm is None:
        raise KeyError("pTM score not found in the JSON file.")
    
    plddt = data.get('plddt')
    if plddt is None:
        raise KeyError("pLDDT scores not found in the JSON file.")
    avg_plddt = float(np.mean(plddt))

    pae = data.get('pae')
    if pae is None:
        raise KeyError("PAE scores not found in the JSON file.")
    avg_pae = float(np.mean(pae))

    max_pae = data.get('max_pae')

    return {
        'ptm': float(ptm),
        'avg_plddt': avg_plddt,
        'avg_pae': avg_pae,
        'max_pae': float(max_pae) if max_pae is not None else None
    }

def get_vina_out(name):
    base_dir = os.getcwd()
    vina_outs = os.path.join(base_dir, "outs", "vina", name)
    vina_out_file = os.path.join(vina_outs, f"{name}_vina.log")

    if not os.path.isfile(vina_out_file):
        raise FileNotFoundError(f"Vina output file not found: {vina_out_file}")
    
    with open(vina_out_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip().startswith("1"):
            cols = line.split()
            if len(cols) >= 2:
                try:
                    binding_affinity = float(cols[1])
                except ValueError:
                    raise ValueError(f"Could not parse binding affinity from line: {line}")
                
    if binding_affinity is None:
        raise ValueError("Binding affinity not found in the Vina output file.")
    return binding_affinity

def write_out_csv(name, colabfold_out, vina_out, aa_seq, dna_seq):
    base_dir = os.getcwd()
    out_dir = os.path.join(base_dir, "outs")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{name}_results.csv")

    row = {
        'project_name': name,
        'ptm': colabfold_out['ptm'],
        'avg_plddt': colabfold_out['avg_plddt'],
        'avg_pae': colabfold_out['avg_pae'],
        'max_pae': colabfold_out['max_pae'],
        'binding_affinity': vina_out,
        'aa_sequence': aa_seq,
        'dna_sequence': dna_seq
     }
    
    fieldnames = [
        'project_name',
        'ptm',
        'avg_plddt',
        'avg_pae',
        'max_pae',
        'binding_affinity',
        'aa_sequence',
        'dna_sequence'
    ]

    with open(out_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)

    return

def write_pdb_out(name):
    base_dir = os.getcwd()
    pdb_out_path = os.path.join(base_dir, "outs", f"{name}.pdb")
    colab_out_path = os.path.join(base_dir, "outs", "colabfold", name)

    for f in os.listdir(colab_out_path):
        if 'rank_001' in f and f.endswith('.pdb'):
            source_pdb = os.path.join(colab_out_path, f)
            break
    if not os.path.isfile(source_pdb):
        raise FileNotFoundError(f"Source PDB file not found in: {colab_out_path}")
    
    with open(source_pdb, 'r') as src, open(pdb_out_path, 'w') as dst:
        dst.write(src.read())

    return

def write_aa_out(name, aa_seq):
    base_dir = os.getcwd()
    aa_out_path = os.path.join(base_dir, "outs", f"{name}_aa_sequence.fasta")
    with open(aa_out_path, 'w') as f:
        f.write(f">{name}_aa_sequence\n")
        f.write(aa_seq + "\n")

    return

def write_dna_out(name, dna_seq):
    base_dir = os.getcwd()
    dna_out_path = os.path.join(base_dir, "outs", f"{name}_dna_sequence.fasta")
    with open(dna_out_path, 'w') as f:
        f.write(f">{name}_dna_sequence\n{dna_seq}\n")

    return
