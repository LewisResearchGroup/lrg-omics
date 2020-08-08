#lrg_omics/metabolomics/common.py

import pandas as pd
import os
import glob
import numpy as np
import re
import datetime

def metadata_from_worklist(fn: str):
    worklist = pd.read_csv(fn)
    return worklist


# def metadata_from_filename(fn: str):
#     '''
#     this function extracts the metadata from the file name and returns a dataframe
#     '''
#     file_name = str(os.path.basename(fn))
#     if file_name.endswith('.mzXML'):
#         file_name, extention = os.path.splitext(file_name)
#     if file_name.endswith('.raw'):
#         file_name, extention = os.path.splitext(file_name)
        
        
#     if('.raw' in file_name):
#         file_name = file_name[:-4]
        
        
#     bi_nbr = None
#     if 'BI_' in file_name:
#         bi_nbr = 'BI'+file_name.split('BI')[-1]
        
#     date = file_name.split('RG')[0].replace('_','-')
    
#     rpt = 0
#     if 'RPT' in file_name:
#         rpt = int(file_name.split('RPT')[-1][:3])
        
#     conc = None
        
#     sample_type = 'BI'                             # BI samples
#     if 'Standard' in file_name: 
#         sample_type = 'ST'                         # standard samples
#         conc = float(file_name.split('Standard-')[-1][:-2])
#     if 'Blank' in file_name: sample_type = 'BL'    # Blank samples
#     if ('SA-pool' in file_name) or ('SA-Pool' in file_name): sample_type = 'PO-SA'  # SA-pool samples
#     if ('MH-pool' in file_name) or ('MH-Pool' in file_name): sample_type = 'PO-MH'      # MH-pool samples
#     if 'QC' in file_name: sample_type = 'QC'       # QC samples
#     mode = file_name.split('HILIC')[-1][:3]
    
#     plate_id = 'SA0'+file_name.split('SA0')[-1][:2]
    
#     data = {
#             'MS_FILE':str(os.path.basename(fn)),
#             'BI_NBR': bi_nbr, 
#             'DATE': date, 
#             'RPT': rpt, 
#             'PLATE_ID': plate_id,
#             'SAMPLE_TYPE': sample_type,
#             'STD_CONC': conc,
#             'MS_MODE': mode
#             }
    
#     df = pd.DataFrame(data, index=[0])
#     return df 

def metadata_from_filename(filename):
    
    
    base = os.path.basename(filename)

    patterns = dict(
                    BI_NBR='BI_[0-9][0-9]_[0-9][0-9][0-9][0-9]',
                    DATE='[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9]',
                    RPT='RPT[0-9]*',
                    PLATE_ID='LSARP_SA([0-9]*)',
                    SAMPLE_TYPE = None,
                    STD_CONC='Standard-[0-9]*nm',
                    MS_MODE = 'HILIC*[A-Z][a-z][a-z]',
                    COL='Col[0-9]*',
#                     TAG='[A-Za-z0-9-]*.mzXML',
                    )
    results = {}
#     if base.endswith('.mzXML'):
#         base, extention = os.path.splitext(base)
#     if base.endswith('.raw'):
#         base, extention = os.path.splitext(base)
    results['MS_FILE'] = base
    
    for name, pattern in patterns.items():
        try:
            results[name] = re.search(pattern, base)[0]
        except:
            results[name] = None
#     if results['BI_NBR'] is not None:
#         results['TAG'] = None
#     else:
#         results['TAG'] = results['TAG'].replace('.mzXML', '')
    if results['PLATE_ID'] is not None:
        results['PLATE_ID'] = results['PLATE_ID'].replace('LSARP_', '')
    if results['RPT'] is None:
        results['RPT'] = 0
    else:
        results['RPT'] = int(results['RPT'].replace('RPT', ''))
    if results['DATE'] is not None:
        results['DATE'] = datetime.datetime.strptime(results['DATE'], '%Y_%m_%d')
    if results['STD_CONC'] is not None:
        results['STD_CONC'] = results['STD_CONC'].replace('Standard-', '')
        results['STD_CONC'] = float(results['STD_CONC'].replace('nm', ''))
    if results['MS_MODE'] is not None:
        results['MS_MODE'] = results['MS_MODE'].replace('HILIC', '')
        
    sample_type = 'BI'                                                        # BI samples
    if 'Standard' in base: sample_type = 'ST'                                 # standard samples
    if 'Blank' in base: sample_type = 'BL'                                    # Blank samples
    if ('SA-pool' in base) or ('SA-Pool' in base): sample_type = 'PO-SA'      # SA-pool samples
    if ('MH-pool' in base) or ('MH-Pool' in base): sample_type = 'PO-MH'      # MH-pool samples
    if 'QC' in base: sample_type = 'QC'                                       # QC samples
    results['SAMPLE_TYPE'] = sample_type    
    return pd.DataFrame(results,index = [0])

def read_plate(path, worklist):
    filenames = [os.path.basename(x) for x in glob.glob(path + '/*.mzXML')]
    frames = []
    for files in filenames:
        frames.append(metadata_from_filename(files))
    output = pd.concat(frames).reset_index().drop(['index'], axis = 1)
    
#     sizes = [os.path.getsize(path+'/'+filenames[k]) for k in range(len(filenames))]
#     output['FILE_SIZE'] = sizes
    output = output.sort_values(by =['MS_FILE']).reset_index().drop(['index'],axis =1 )
    
    wl = pd.read_csv(path +'/' + worklist, skiprows=1)
    wl['File Name'] += '.mzXML'
    isin = [wl['File Name'][k] in filenames for k in range(len(wl))]
    wl = wl[ isin ].sort_values(by=['File Name']).reset_index().drop(['index'],axis = 1)
    output['WELL_ROW'] = wl.Position.str.split(':').apply(lambda x: x[-1][0])
    output['WELL_COL'] = wl.Position.str.split(':').apply(lambda x: int(x[-1][1:]))
    
    
    
    return output
