# pbp-designer
A pipeline for automated engineering of biosensors for small molecule ligands. PBP designer uses BoltzGen to create a periplasmic binding protein, which is then turned into a FRET molecule, and finally codon optimized for E. coli expression.
The pipeline requires the usage of a High Performance Computing cluster, with the apptainer module installed. Many clusters come with apptainer per-installed, but you can go to https://github.com/apptainer/apptainer.git to install the software.

**Getting started**
Begin by cloning the repository: ```git clone https://github.com/ExpertMirror/pbp-designer.git```
Furute work will require the user to be inside the repository, so use ```cd ./pbp-designer``` to enter the repo.
PBP designer requires the use of multiple .sif (apptainer/docker) images, as well as some python libraries. A script has been created to pull all the dependancies automatically (provided you have apptainer installed)
To pull the dependancies:
1. ```module load python```
2. ```module load apptainer```
3. ```python get_deps.py```
If you run into issues with the script, you can pull the dependancies manually. Check the ```dependancies.txt``` file and run a pip install for all python packages. Ex: ```pip install rdkit```
Once you have downloaded all the python packages, you can use the specified pull commands for apptainer images. Some apptainer images (converter.sif and vina.sif) have .def files used for their builds, so ensure you cd into the specified directory before attempting to pull.
For the colabfold image, use ```cd ./structure``` and run the pull command from there.
For the BoltzGen image, use ```cd ./boltzgen``` and run the pull command from there.


To run the pipeline, it is recommended you submit a SLURM job for GPU support. Please see ```recommended_slurm.sh``` for an example.
In order to begin the pipeline, ensure you use ```python run.py "<SMILES>" <project_name>
