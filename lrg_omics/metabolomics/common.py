#lrg_omics/metabolomics/common.py

import pandas as pd

def read_worklist(fn: String):
    worklist = pd.read_csv(fn)
    return worklist

def metadata_from_filename(fn: String):
    return pd.DataFrame()


