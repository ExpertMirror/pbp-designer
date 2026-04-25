import init
import sys
import os
from chemistry import compute_similarity as cs
from boltzgen import run_boltzgen as rb
from sequence import get_seq as seq
from structure import run_colabfold as fold
from docking import dock
from dna import optimize_dna as dna
import get_output as out



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
    if cs.check_smiles_type(ligand_smiles) == "ion":
        scaffold = "moda"
        rb.write_yaml(scaffold, ligand_smiles, project_name)
        rb.activate_boltzgen(project_name)
        init_seq = seq.extract_seq(project_name)
        fold.write_seq(init_seq, project_name)
        fold.activate_colabfold(project_name)
        dock.get_pdb(project_name)
        dock.convert_ligand(ligand_smiles, project_name)
        dock.convert_protein(project_name)
        dock.fix_receptor_pdbqt(project_name)
        center, size = dock.compute_protein_grid_box(project_name)
        dock.write_config(project_name, center, size)
        dock.run_vina(project_name)
        aa_seq = dna.append_fret_proteins(project_name, init_seq)
        dna_seq = dna.optimized_ecoli_dna(aa_seq)
        colabfold_out = out.get_colabfold_out(project_name)
        vina_out = out.get_vina_out(project_name)
        out.write_out_csv(project_name, colabfold_out, vina_out, aa_seq, dna_seq)
        out.write_pdb_out(project_name)
        out.write_aa_out(project_name, aa_seq)
        out.write_dna_out(project_name, dna_seq)

    else:
        scaffold = cs.find_scaffold(names,scores)
        rb.write_yaml(scaffold, ligand_smiles, project_name)
        rb.activate_boltzgen(project_name)
        init_seq = seq.extract_seq(project_name)
        fold.write_seq(init_seq, project_name)
        fold.activate_colabfold(project_name)
        dock.get_pdb(project_name)
        dock.convert_ligand(ligand_smiles, project_name)
        dock.convert_protein(project_name)
        dock.fix_receptor_pdbqt(project_name)
        center, size = dock.compute_protein_grid_box(project_name)
        dock.write_config(project_name, center, size)
        dock.run_vina(project_name)
        aa_seq = dna.append_fret_proteins(project_name, init_seq)
        dna_seq = dna.optimized_ecoli_dna(aa_seq)
        colabfold_out = out.get_colabfold_out(project_name)
        vina_out = out.get_vina_out(project_name)
        out.write_out_csv(project_name, colabfold_out, vina_out, aa_seq, dna_seq)
        out.write_pdb_out(project_name)
        out.write_aa_out(project_name, aa_seq)
        out.write_dna_out(project_name, dna_seq)

if __name__=="__main__":
    main()
