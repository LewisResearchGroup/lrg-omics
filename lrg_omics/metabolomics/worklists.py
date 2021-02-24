import os
import pandas as pd
from .common import metadata_from_filename


def read_worklist(fn):
    df = pd.read_csv(fn)[['File Name', 'Position']].drop_duplicates()
    df['MS_FILE'] = df['File Name'].apply(os.path.basename)+'.mzXML'
    df['PLATE_ROW'] = df.Position.apply(lambda x: x.split(':')[1][0])
    df['PLATE_COL'] = df.Position.apply(lambda x:  '{:02.0f}'.format(int( x.split(':')[1][1:] )))
    if not df.MS_FILE.duplicated().sum() == 0: df[df.MS_FILE.isin( df[df.MS_FILE.duplicated()].MS_FILE )].sort_values('MS_FILE')
    return df[['MS_FILE', 'PLATE_ROW', 'PLATE_COL']]


def get_metadata_from_worklist(worklist, parse_func='LSARP'):
    n_errors = 0
    if parse_func == 'LSARP':
        parse_func = metadata_from_filename
    metadata = pd.concat([parse_func(fn) for fn in worklist.MS_FILE])
    metadata = pd.merge(worklist, metadata, on='MS_FILE', how='right').sort_values(['PLATE_ID', 'PLATE_ROW', 'PLATE_COL', 'RPT'])
    metadata = metadata[['MS_FILE', 'DATE', 'PLATE_ID', 'PLATE_ROW', 'PLATE_COL', 'MS_MODE', 'RPT', 'SAMPLE_TYPE', 'BI_NBR']]
    metadata = metadata.reset_index(drop=True)
    metadata['RPT'] = metadata['RPT'].astype(int)
    return metadata
