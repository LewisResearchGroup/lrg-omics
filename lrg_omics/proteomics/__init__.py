import os
import pandas as pd

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .quality_control.rawtools import collect_rawtools_qc_data, update_rawtools_qc_data
from .quality_control.maxquant import collect_maxquant_qc_data, update_maxquant_qc_data


def load_rawtools_data_from(path='/var/www/html/proteomics/files/raw'):
    try:
        df = collect_rawtools_qc_data(path).drop_duplicates()
        df['md5'] = df.RawFile.apply(lambda x: x.split('/')[-2])
        df.index = df.iloc[::-1].index
        df.reset_index(inplace=True)
        df['RawFilePath'] = df['RawFile'].apply(os.path.dirname)
        df['RawFile'] = df['RawFile'].apply(os.path.basename)
        for col in ['Instrument', 
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
        df['Day'] = df.DateAcquired.dt.dayofyear.astype(str)
        df['Week'] = df.DateAcquired.dt.week.astype(str)
        df['Month'] = df.DateAcquired.dt.month.astype(str)
        df['Year'] = df.DateAcquired.dt.year.astype(str)
        df['Month'] = df['Year'] + '-' + df['Month']
        df['Week'] = df['Year'] + '-' + df['Week']
        df['Day'] = df['Year'] + '-' + df['Day']
    except:
        df = pd.DataFrame()
        df['RawFile'] = ''
    return df.round(2)
    
    
def load_maxquant_data_from(path='/var/www/html/proteomics/files/'):
    assert os.path.isdir(path)
    try:
        df = collect_maxquant_qc_data(path).drop_duplicates()
        df.index = df.iloc[::-1].index
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df.Date)
        df.rename(columns={
            'index': 'Index',
            'PIPENAME': 'Pipename', 
            'RAW_file': 'RawFile', 
            'FASTA_file': 'FastaFile', 
            'MQPAR_TEMP_file': 'MaxQuantPar'}, inplace=True)
        df['md5'] = df.RawFile.apply(lambda x: x.split('/')[-2])
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
    except:
        df = pd.DataFrame()
    return df.round(2)
