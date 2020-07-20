#lrg_omics/metabolomics/common.py

import pandas as pd

def read_worklist(fn: str):
    worklist = pd.read_csv(fn)
    return worklist

def metadata_from_filename(fn: str):
    return pd.DataFrame()


