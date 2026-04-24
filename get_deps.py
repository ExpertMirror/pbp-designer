import os
import subprocess as sp

def get_packages():
    print("Updating pip...")
    sp.run(['pip', 'install', '--upgrade', 'pip'])
    with open('requirements.txt') as f:
        deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        for dep in deps:
            print(f"Installing {dep}...")
            sp.run(['pip', 'install', dep])

    return

def pull_sifs():
    sp.run(['module', 'load', 'apptainer'])
    base_dir = os.getcwd()
    dock_dir = os.path.join(base_dir, 'docking')
    os.chdir(dock_dir)
    print("Building 'converter.sif' from 'converter.def'...")
    sp.run(['apptainer', 'build', 'converter.sif', 'converter.def'])
    print("Building 'vina.sif' from 'vina.def'...")
    sp.run(['apptainer', 'build', 'vina.sif', 'vina.def'])
    os.chdir(base_dir)
    boltzgen_dir = os.path.join(base_dir, 'boltzgen')
    os.chdir(boltzgen_dir)
    print("Building 'boltzgen.sif' from 'docker://fastfold/boltzgen:v0.2.0'...")
    sp.run(['apptainer', 'pull', 'boltzgen.sif', 'docker://fastfold/boltzgen:v0.2.0'])
    os.chdir(base_dir)
    fold_dir = os.path.join(base_dir, 'structure')
    os.chdir(fold_dir)
    print("Building 'colabfold.sif' from 'docker://ghcr.io/sokrypton/colabfold:1.5.5-cuda12.2.2'...")
    sp.run(['apptainer', 'pull', 'colabfold.sif', 'docker://ghcr.io/sokrypton/colabfold:1.5.5-cuda12.2.2'])
    os.chdir(base_dir)
    return

def get_colabfold_weights():
    base_dir = os.getcwd()
    fold_dir = os.path.join(base_dir, 'structure')
    os.chdir(fold_dir)
    os.makedirs('colabfold_weights', exist_ok=True)
    print("Downloading ColabFold weights...")
    sp.run(['apptainer', 'exec', '--cleanenv', '-B', './colabfold_weights:/cache', 'colabfold.sif', 'python', '-m', 'colabfold.download'])
    return

def main():
    get_packages()
    pull_sifs()
    get_colabfold_weights()

if __name__ == "__main__":
    main()
