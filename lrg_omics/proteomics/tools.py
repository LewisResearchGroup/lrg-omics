import os
import logging

from .quality_control.rawtools import collect_rawtools_qc_data
from .quality_control.maxquant import collect_maxquant_qc_data

def load_rawtools_data_from(path='/var/www/html/proteomics/files/raw'):
    df = collect_rawtools_qc_data(path)
    if df is None: return None
    df.index = df.iloc[::-1].index
    df.reset_index(inplace=True)
    df['RawFilePath'] = df['RawFile'].apply(os.path.dirname)
    df['RawFile'] = df['RawFile'].apply(os.path.basename)
    df.rename(columns={'index': 'Index'}, inplace=True)
    df['Date'] =  df.DateAcquired.dt.date.astype(str)
    df['Day'] = df.DateAcquired.dt.dayofyear.map('{:03d}'.format)
    df['Week'] = df.DateAcquired.dt.isocalendar().week.map('{:02d}'.format)
    df['Month'] = df.DateAcquired.dt.month.map('{:02d}'.format)
    df['Year'] = df.DateAcquired.dt.year.astype(str)
    df['Month'] = df['Year'] + '-' + df["Month"]
    df['Week'] = df['Year'] + '-' + df['Week']
    df['Day'] = df['Year'] + '-' + df['Day']
    return df

formated_rawtools_data_from = load_rawtools_data_from  
    
def load_maxquant_data_from(path='/var/www/html/proteomics/files/'):
    if not os.path.isdir(path):
        logging.warning(f'FileNotFound: {path}')
        return None
    df = collect_maxquant_qc_data(path)
    if df is None: return None
    df.index = df.iloc[::-1].index
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Index'}, inplace=True)
    df['Missed Cleavages [%]'] = (100-df['N_missed_cleavages_eq_0 [%]'])

    for col in ['MAXQUANTBIN', 'proteomics_tools version', 'RUNDIR', 'Date']:
        try:
            del df[col]
        except:
            pass
    for col in ['FastaFile', 'RawFile', 'MaxQuantPar']:
        try:
            df[col] = df[col].apply(os.path.basename)
        except:
            pass
    return df
