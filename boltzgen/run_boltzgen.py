import os
import subprocess as sp
from unittest import result

def write_yaml(scaffold, smiles, name):
    base_dir = os.getcwd()
    scaffold_path = os.path.join(base_dir, "boltzgen", "specs", f"{scaffold}.yaml")
    os.makedirs(os.path.join(base_dir, "outs", "boltzgen", "yamls"), exist_ok=True)
    yaml_out = os.path.join(base_dir, "outs", "boltzgen", "yamls", f"{name}.yaml")

    with open(scaffold_path, 'r') as f:
        lines = f.readlines()


    for i, line in enumerate(lines):
        if 'smiles:' in line:
            lines[i] = f'      smiles: "{smiles.strip()}"\n'
            break

    print(f"yaml_out: {yaml_out}")

    with open(yaml_out, 'w') as f:
        f.writelines(lines)

def activate_boltzgen(name):
    base_dir = os.getcwd()

    workdir = os.path.abspath(os.path.join(base_dir, "outs", "boltzgen"))
    example_dir = os.path.abspath(os.path.join(base_dir, "outs", "boltzgen", "yamls"))
    sif_path = os.path.join(base_dir, "boltzgen", "boltzgen.sif")

    os.makedirs(os.path.join(workdir, name), exist_ok=True)

    scratch = os.environ.get("SCRATCH")
    if scratch is None:
        raise RuntimeError("SCRATCH not set")
    

    cmd = [
        "apptainer", "run", "--nv",
        "--bind", f"{scratch}:{scratch}",
        "-B", f"{workdir}:/workdir",
        "-B", f"{example_dir}:/example",

        sif_path,

        "boltzgen", "run",
        f"/example/{name}.yaml",                 # ✅ FIXED
        "--output", f"/workdir/{name}",          # ✅ FIXED
        "--protocol", "protein-small_molecule",
        "--num_designs", "50",
        "--budget", "30"
    ]

    print("Running:", " ".join(cmd))

    sp.run(cmd, check=True)
