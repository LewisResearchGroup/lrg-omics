# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 


# Create the environment

    conda env create -f enviroment.yml

    conda activate omics
    
    jupyter labextension install jupyterlab-plotly@4.8.2
    
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    


##  Download and install from source

    git clone https://github.com/LSARP/lrg_omics
    cd lrg_omics
    pip install -e . 


## Install new kernel into JupyterLab

    conda activate omics
    ipython kernel install --name "LRG" --user

    



