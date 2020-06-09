# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 


# Create the environment

    conda create -n lrg_omics -c bioconda -c conda-forge -c plotly jupyterlab matplotlib pandas scikit-learn seaborn tqdm rawtools dash pyteomics pymzml versioneer pytest "notebook>=5.3" "ipywidgets>=7.2" plotly=4.8.1

    conda activate lrg_omics
    
    pip install versioneer
    
    jupyter labextension install jupyterlab-plotly@4.8.1
    
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.1
    


##  Download and install from source

    git clone ...
    cd lrg_omics
    pip install -e . 


## Install new kernel into JupyterLab

    conda activate lrg_omics
    ipython kernel install --name "LRG" --user

    



