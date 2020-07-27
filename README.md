# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 

##  Download and install from source

    git clone https://github.com/LSARP/lrg_omics
    cd lrg_omics
    
    conda env create -f enviroment.yml
    conda activate omics
    pip install -e . 

    jupyter labextension install jupyterlab-plotly@4.8.2
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    ipython kernel install --name "LRG" --user




