#lrg_omics/metabolomics/common.py

import pandas as pd
import os
import glob
import numpy as np
import re
import datetime

def metadata_from_worklist(fn: str):
    worklist = pd.read_csv(fn, skiprows=1, usecols=[1,3, 4, 7])
    worklist['MS_FILE'] = worklist['File Name']+'.mzXML'
    worklist['PLATE_ROW'] = worklist.Position.apply(lambda x: x.split(':')[1][0])
    worklist['PLATE_COL'] = worklist.Position.apply(lambda x: x.split(':')[1][1:]).astype(int)
    return worklist

def metadata_from_filename(filename):
    """function to extract the information contained in the file names"""
    
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
    """function to read the files in a plate and organize them as a dataframe"""
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
    
    
def classic_lstsqr(x_list, y_list):
    """ Computes the least-squares solution to a linear matrix equation by fixing the slope to 1 """ 
    """ its suitable to work on the log-scale  """ 
    
    N = len(x_list)
    x_avg = sum(x_list)/N
    y_avg = sum(y_list)/N
    var_x, cov_xy = 0, 0
    for x,y in zip(x_list, y_list):
        temp = x - x_avg
        var_x += temp**2
        cov_xy += temp * (y - y_avg)
#     slope = cov_xy / var_x
    slope = 1.0
    y_interc = y_avg - slope * x_avg
    
    y_hat = y_interc + slope * x_list
    
    residual = sum((y_list - y_hat)**2)/N
    r_ini = (y_list[0] - y_hat[0])**2
    r_last = (y_list[-1] - y_hat[-1])**2
    
    return (slope, y_interc, residual, r_ini, r_last )

def linear_range_finder(x , y , th):
    
    """ this algorith searches the range of x values in which the data behaves linearly with slope 1"""
    """ suitable to work on the log-scale """
    x_c = x
    y_c = y
    _, _, res, r_ini, r_last = classic_lstsqr(x_c, y_c)
    while res > th and len(x_c) > 3:
        if r_ini > r_last:
            x_c = x_c[1:]
            y_c = y_c[1:]
        else:
            x_c = x_c[:-1]
            y_c = y_c[:-1]
        _, _, res, r_ini, r_last = classic_lstsqr(x_c, y_c)
    return (x_c, y_c)