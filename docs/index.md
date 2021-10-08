# Welcome to lrg-omics documentation

This is the codebase for omics data generation, processing, quality control and integration developed at the 
[Lewis Research Group (LRG)](https://www.lewisresearchgroup.org/).

## Installation

###  From source

You can install lrg-omics from source with:

```bash
    git clone https://github.com/LSARP/lrg-omics
    cd lrg-omics
    conda env create -f dev/conda/environment.yml
    conda activate lrg-omics-dev
    pip install -e .
```


To use LRG-omics we recommend to use JupyterLab.

### Install LRG kernel in JupyterLab

```bash
    jupyter labextension install jupyterlab-plotly@4.8.2
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    ipython kernel install --name "LRG" --user
```

### Dependencies

LRG-omics runs with Python=>3.8. It also uses [pandas] for data analysis and
the [scikit-learn] for Machine Learning (ML) as core libraries. 
Since this package is also intended as a visualization tool, LRG-omics has
Matplotlib and Seaborn as dependencies for data visualization. 

Check the [requirements] file for a full list of dependencies.

## Collaboration

LRG-omics is open source and welcomes your contributions! 

Please report bugs or requests to improve LRG-omics through the Issue Tracker.
Contributions are welcome, and they are highly appreciated!

These are some points to keep in mind:

- To report bugs please inlcude:

    - Your operating system (name and version).
    - Details about your local setup (environments, versions of dependencies, etc).
    - Step-by-step description to reproduce the bug.

- Documentation:

We are currently building our docs, then any help to make our docs better is also very appreciated!

### Development branch

Please note that current development on LRG-omics is limited to Linux OS. We are
planning to implement MacOS and Windows in the near future. To set up LRG-omics
for local development please follow the steps outlined below:

1. Fork lrg-omics using the “Fork” button.

1. Create and activate the development environment:

    ```
    conda create -f dev/conda/environment.yml
    conda activate lrg-omics-dev
    ```

1. Clone your forked repo locally in your preferred location:

    ```
    git clone git@github.com:YOURGITHUBNAME/lrg-omics.git
    ```

1. Create a branch for local development:

    ```
    git checkout -b your-branch-name
    git switch your-branch-name
    ```

    Now you're ready to make changes locally!

## Test coverage

LRG-omics uses [pytest] framework. You can run the tests in three steps:


1. Install 

    ```bash
    pip install pytest-cov
    ```

1. Go to the root folder of LRG-omics:

    ```
    cd lrg-omics    
    ```

1. Then you can run pytest with a coverage report in HTML with:

    ```
    pytest --cov=lrg-omics --cov-report=html
    ```


When submitting a Pull Request, all tests should pass.


[scikit-learn]: https://scikit-learn.org/stable/
[pandas]: https://pandas.pydata.org/
[requirements]: https://github.com/LSARP/lrg-omics/blob/develop/requirements.txt
[pytest]: https://doc.pytest.org/en/latest/