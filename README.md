![](images/coverage.svg)

# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 


 [Documentation](https://LSARP.github.io/lrg-omics/)



##  Download and install from source

    git clone https://github.com/LSARP/lrg-omics
    
    cd lrg-omics
    conda env create -f dev/conda/environment.yml
    conda activate lrg-omics-dev
    pip install -r requirements.txt
    pip install -e .


## Install LRG kernel in JupyterLab

    jupyter labextension install jupyterlab-plotly@4.8.2
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    ipython kernel install --name "LRG" --user


## Authors

- Soren Wacker
- Mario Ernesto-Valdés
- Luis Ponce Alvares
