#lrg_omics/metabolomics/common.py

import pandas as pd



def metadata_from_worklist(fn: str):
    worklist = pd.read_csv(fn)
    return worklist


def metadata_from_filename(fn: str):
    return pd.DataFrame()


def read_plate(filenames, worklist):
    return pd.DataFrame()
