
from ..metabolomics.common import metadata_from_filename, metadata_from_worklist
import os
from os.path import basename

from glob import glob
import pandas as pd


LSARP_DATA = os.getenv('LSARP_DATA', '/home/lrg-share/LSARP/')
LSARP_METAB = os.getenv('LSARP_METAB', '/home/lrg-ms/ms-share/ms-data/QEHF/LRG/LSARP/')


def get_shipments(path=f'{LSARP_DATA}/Plate-Register/APL/Shipments'):
    print('Shipments from:', path)
    shipments = pd.concat([pd.read_excel(fn) for fn in glob(f'{path}/*xlsx')])
    shipments['PLATE_ID'] = shipments['LSARP_PLATE'].apply(lambda x: x.split(',')[0]).apply(lambda x: x.split('_')[1])
    shipments['PLATE_ROW'] = shipments['LSARP_LOCN'].apply(lambda x: x.split(',')[0])
    shipments['PLATE_COL'] = shipments['LSARP_LOCN'].apply(lambda x: x.split(',')[1]).astype(int)
    shipments.sort_values(['PLATE_ID', 'PLATE_ROW', 'PLATE_COL'], inplace=True)
    shipments.reset_index(drop=True, inplace=True)
    return shipments


def get_broad_plates(path=f'{LSARP_DATA}/Plate-Register/Broad/Plates'):
    broad_plates = []
    for fn in glob(f'{path}/*/*xls*'):
        df = pd.read_excel(fn, header=[0,1])
        df['Filename'] = basename(fn)
        broad_plates.append(df.reset_index(drop=True))
    broad_plates = pd.concat(broad_plates)
    return broad_plates


def get_proteomics_plates(path=LSARP_DATA):
    proteomics = pd.concat([pd.read_excel(fn) for fn in glob(f'{path}/Plate-Register/Proteomics/*.xls*')])
    return proteomics


def get_metabolomics_plates(worklist_path=f'{LSARP_DATA}/Plate-Register/Metabolomics', file_path=LSARP_METAB):
    print('Metabolomics worklists directory:', worklist_path)
    print('Metabolomics MS-file directory:', file_path)
    
    metabolomics = []
    for fn in glob(f'{file_path}/**/*mzXML'):
        try:
            metabolomics.append( metadata_from_filename(basename(fn)) )
        except:
            print(f'W: Could not parse data from {fn}')
    metabolomics = pd.concat( metabolomics ).reset_index(drop=True)
    print(f'Found {len(metabolomics)}  MS-files')
    worklists = []
    for fn in glob(f'{worklist_path}/*csv'):
        df = metadata_from_worklist(fn)
        worklists.append(df)
    worklists = pd.concat( worklists )
    worklists['MS_FILE'] = worklists['File Name']+'.mzXML'
    metabolomics = pd.merge(metabolomics, worklists, on='MS_FILE')
    return metabolomics.sort_values(['PLATE_ID', 'PLATE_ROW', 'PLATE_COL'])


def read_growth_xlsx(fn, long_form=True):
    df = pd.read_excel(fn, skiprows=9, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).head(8)
    df.index = list('ABCDEFGH')
    df.index.name = 'PLATE_ROW'
    df.columns.name = 'PLATE_COL'
    if long_form: df = df.T.reset_index().melt(id_vars='PLATE_COL', value_name='OD')[['PLATE_ROW', 'PLATE_COL', 'OD']]
    fn = basename(fn)
    df['FILE'] = fn
    df['PLATE_ID'] = fn.split(' ')[0]
    df['OD'] = df.OD.astype(float)
    for i in fn.replace('.xlsx', '').split(' - '):
        if i.endswith('h'):
            df['TIME'] = i
        try:
            df['DATE'] = pd.to_datetime(i)
        except:
            pass
    return df.reset_index(drop=True)


def get_growth_protein(path=f'{LSARP_DATA}/Growth/Plates'):
    fns = glob(f'{path}/**/S*Prot*xlsx', recursive=True)
    dfs = []
    for fn in fns:
        df = read_growth_xlsx(fn)
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)


def get_growth_monitor(path=f'{LSARP_DATA}/Growth/Plates'):
    fns = glob(f'{path}/**/S*monitor*xlsx', recursive=True)
    dfs = []
    for fn in fns:
        df = read_growth_xlsx(fn)
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)

