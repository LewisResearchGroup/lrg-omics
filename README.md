[![Python Package](https://github.com/LewisResearchGroup/lrg-omics/actions/workflows/pytest.yml/badge.svg)](https://github.com/LewisResearchGroup/lrg-omics/actions/workflows/pytest.yml)
[![Python version](https://img.shields.io/badge/Python-3.8-blue?style=plastic)](https://www.python.org/)
![](images/coverage.svg)
[![Documentation Status](https://readthedocs.org/projects/lrg-omics/badge?/?version=stable)](https://lsarp.github.io/lrg-omics/?badge=stable)

# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 


 [Documentation](https://LSARP.github.io/lrg-omics/)



##  Download and install from source

    git clone https://github.com/LSARP/lrg-omics
    
    cd lrg-omics
    conda env create -f dev/conda/environment.yml
    conda activate lrg-omics-dev
    pip install -e .


## Install LRG kernel in JupyterLab

    jupyter labextension install jupyterlab-plotly@4.8.2
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    ipython kernel install --name "LRG" --user


## Authors

- Soren Wacker
- Mario Ernesto-Valdés
- Luis Ponce Alvares
- Estefania Barreto-Ojeda (@ojeda-e)


# Scripts

## lrg_run_maxquant.py

A script to run MaxQuant runs from the Linux command line.

```
usage: lrg_run_maxquant.py [-h] --raw [RAW ...] --fasta FASTA --mqpar MQPAR [--run-dir RUN_DIR] [--out-dir OUT_DIR] [--cold-run] [--rerun] [--submit] [--batch-cmd BATCH_CMD] --maxquantcmd MAXQUANTCMD [--add-raw-name-to-outdir]
                           [--add-uuid-to-rundir] [--cleanup] [--verbose]

Process MaxQuant runs.

options:
  -h, --help            show this help message and exit
  --raw [RAW ...]       RAW files to process.
  --fasta FASTA         Fasta file.
  --mqpar MQPAR         MaxQuant parameter template file (mqpar.xml).
  --run-dir RUN_DIR     Temporary directory to perform the calculation.
  --out-dir OUT_DIR     Location of the final results.
  --cold-run            Just simulate run and show the actions.
  --rerun               Start the run even if results already exist.
  --submit              Submit slurm job.
  --batch-cmd BATCH_CMD
                        Additional commands for slum job script e.g. "source .bashrc conda activate omics;...".
  --maxquantcmd MAXQUANTCMD
                        Command to start MaxQuant e.g. "mono MaxQuantCmd.exe".
  --add-raw-name-to-outdir
                        Do not add subdirectory raw file name to run directory.
  --add-uuid-to-rundir  Do not add uuid to run directory.
  --cleanup             Remove run directory after running MaxQuant
  --verbose
```
