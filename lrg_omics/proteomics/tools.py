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
    for col in [ 
                'Ms1Analyzer', 
                'Ms2Analyzer', 
                'Ms3Analyzer', 
                'MedianMassDrift(ppm)',
                'IdentificationRate(IDs/Ms2Scan)',
                'DigestionEfficiency',
                'MissedCleavageRate(/PSM)',
                'MedianPeptideScore',
                'CutoffDecoyScore(0.05FDR)',
                'NumberOfPSMs',
                'NumberOfUniquePeptides',
                'PsmChargeRatio3to2',
                'PsmChargeRatio4to2',
                'SearchParameters']:
        del df[col]
    df.rename(columns={'index': 'Index'}, inplace=True)
    df['Date'] =  df.DateAcquired.dt.date.astype(str)
    df['Day'] = df.DateAcquired.dt.dayofyear.astype(str)
    df['Week'] = df.DateAcquired.dt.isocalendar().week.astype(str)
    df['Month'] = df.DateAcquired.dt.month.astype(str)
    df['Year'] = df.DateAcquired.dt.year.astype(str)
    df['Month'] = df['Year'] + '-' + df['Month']
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
    df.rename(columns={
        'index': 'Index',
        'PIPENAME': 'Pipeline', 
        'RAW_file': 'RawFile', 
        'FASTA_file': 'FastaFile', 
        'MQPAR_TEMP_file': 'MaxQuantPar'}, inplace=True)

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
