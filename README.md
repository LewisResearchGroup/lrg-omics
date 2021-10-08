![](images/coverage.svg)
[![Python version](https://img.shields.io/badge/Python-3.8-blue?style=plastic)](https://www.python.org/)
[![GitHub Actions Status](https://github.com/LSARP/lrg-omics/actions/workflows/python-package.yml/badge.svg?branch=develop)](https://github.com/LSARP/lrg-omics/actions/?query=workflow)
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
