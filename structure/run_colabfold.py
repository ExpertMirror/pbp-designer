import os
import subprocess as sp


def write_seq(seq, name):
    base_dir = os.getcwd()

    input_dir = os.path.join(base_dir, "structure", "inputs")
    os.makedirs(input_dir, exist_ok=True)

    fasta_path = os.path.join(input_dir, f"{name}.fasta")

    with open(fasta_path, "w") as f:
        f.write(f">{name}_designed_protein_seq\n{seq}\n")

    return fasta_path


def activate_colabfold(name):
    base_dir = os.getcwd()

    # Paths
    input_dir = os.path.join(base_dir, "structure", "inputs")
    out_dir = os.path.join(base_dir, "outs", "colabfold")
    os.makedirs(out_dir, exist_ok=True)

    run_out_dir = os.path.join(out_dir, name)
    os.makedirs(run_out_dir, exist_ok=True)

    weights_dir = os.path.join(base_dir, "structure", "colabfold_weights")
    image_path = os.path.join(base_dir, "structure", "colabfold.sif")

    # IMPORTANT: input is DIRECTORY, not file
    cmd = [
        "apptainer", "exec",
        "-e",             # Clean environment (vital for portability)
        "--nv",           # GPU support

        "-B", f"{input_dir}:/input",
        "-B", f"{run_out_dir}:/output",
        "-B", f"{weights_dir}:/cache",

        image_path,

        "colabfold_batch",
        "/input",
        "/output"
    ]

    print("\n[INFO] Running ColabFold command:\n", " ".join(cmd), "\n")

    result = sp.run(cmd, text=True)

    if result.returncode != 0:
        raise RuntimeError("ColabFold failed — check logs above.")
