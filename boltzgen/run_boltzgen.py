import os
import subprocess as sp

def write_yaml(scaffold, smiles, name):
    os.chdir('../../boltzgen/specs')
    with open(f'{scaffold}.yaml', 'r') as f:
        lines = f.readlines()


    for i, line in enumerate(lines):
        if 'smiles:' in line:
            lines[i] = f'      smiles: "{smiles.strip()}"\n'
            break
        
    os.chdir('../')
    with open(f'{name}.yaml', 'w') as f:
        f.writelines(lines)

def activate_boltzgen(name):
    base_dir = os.getcwd()
    out_dir = os.path.abspath(os.path.join(base_dir, "../outs/boltzgen", name))
    workdir = os.path.abspath(os.path.join(base_dir, "../outs/boltzgen"))
    example_dir = os.path.abspath(os.path.join(base_dir, "../boltzgen"))

    os.makedirs(out_dir, exist_ok=True)

    scratch = os.environ.get("SCRATCH")
    if scratch is None:
        raise RuntimeError("SCRATCH not set")

    cmd = [
        "apptainer", "run", "--nv",
        "--bind", f"{scratch}:{scratch}",
        "-B", f"{workdir}:/workdir",
        "-B", f"{example_dir}:/example",
        "boltzgen.sif",
        "boltzgen", "run", f"./{name}.yaml",
        "--output", f"/workdir/{name}",   # important: use container path
        "--protocol", "protein-small_molecule",
        "--num_designs", "50",
        "--budget", "30"
    ]

    print("Running:", " ".join(cmd))  # debug
    sp.run(cmd, check=True)


"""
apptainer run   --nv   --bind $SCRATCH:$SCRATCH   -B "../outs/boltzgen/workdir":/workdir   -B "$PWD":/example   boltzgen.sif     boltzgen check /example/mppa_idk/mi.yaml
"""

"""
apptainer run   --nv   --bind $SCRATCH:$SCRATCH   -B "$PWD/workdir":/workdir   -B "$PWD/example":/example   boltzgen_weights.sif     boltzgen check /example/mppa_idk/mi.yaml
"""
