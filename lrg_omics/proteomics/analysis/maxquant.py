<<<<<<< HEAD
def get_maxquant_txt(raw_file, txt='proteinGroups.txt', 
                     pipename='Standard-QC__SA_MS2'):
=======
import pandas as pd
import numpy as np
from os.path import isfile


def get_maxquant_txt(path, txt='proteinGroups.txt', mq_run_name=None,
                     pipename=None):
>>>>>>> 9ccb24aada0a6dae9d8c718238bac60d07c267ef
    '''
    Graps a MaxQuant txt based on the name of the
    .RAW file and the name of the pipeline. raw_file
    and pipename are added to all rows. Pipename is
    removed from all column names.
    '''
<<<<<<< HEAD
    try:
        path = RAWTOOLS.loc[RAWTOOLS.RawFile == raw_file, 'RawFilePath'].values[0]
    except:
        print(f'Could not find path for {raw_file}' )
        print(RAWTOOLS.loc[RAWTOOLS.RawFile == raw_file, 'RawFilePath'])
        return pd.DataFrame()
    full_path = f'{path}/maxquant/{pipename}/{raw_file}/txt/{txt}'
    if isfile(full_path):
        df = pd.read_table(full_path)
    else:
        print(f'File not found: {full_path}')
        return pd.DataFrame()
    df['RawFile'] = raw_file
    df['PipeName'] = pipename
    df = df.set_index('RawFile').reset_index()
    df.columns = [i.replace(pipename, '').strip() for i in df.columns]
    return df

def melt_protein_quant(df, protein_col='Protein IDs'):
    output = df.melt(id_vars=['RawFile', protein_col], var_name='TMT', value_name='RepInt')
    output['TMT'] = output['TMT'].str.replace('Reporter intensity corrected ', '').astype(int)
    output = output.set_index(['RawFile', 'TMT'])\
                   .reset_index()
    return output

def get_protein_quant(raw_file, melt=False, normed=None, take_log=False,
                      divide_by_column_mean=False, mean_centering_per_plex=False,
                      drop_zero_q=False, data_cols=['RawFile'],
                      protein_col='Protein IDs'):
=======
    full_path = f'{path}/{txt}'
    if isfile(full_path):
        df = pd.read_table(full_path)
    else:   
        print(f'File not found: {full_path}')
        return pd.DataFrame()
    df['MaxQuantRun'] = mq_run_name
    df['PipeName'] = pipename
    df = df.set_index(['MaxQuantRun', 'PipeName']).reset_index()
    df.columns = [i.replace(pipename, '').strip() for i in df.columns]
    return df

def melt_protein_quant(df, id_vars=None, var_name='TMT'):
    if id_vars is None:
        id_vars=['MaxQuantRun', 'PipeName' ,'Protein IDs', 'Score']
    output = df.melt(id_vars=id_vars, var_name=var_name, value_name='ReporterIntensity')
    output['TMT'] = output['TMT'].str.replace('Reporter intensity corrected ', '').astype(int)
    return output

def get_protein_quant(path, melt=False, normed=None, take_log=False,
                      divide_by_column_mean=False, mean_centering_per_plex=False,
                      drop_zero_q=False, data_cols=['MaxQuantRun', 'PipeName'],
                      protein_col='Protein IDs', pipename=None, mq_run_name=None):
>>>>>>> 9ccb24aada0a6dae9d8c718238bac60d07c267ef
    '''
    Gets the proteinGroups file based on the .RAW name 
    and the pipename. Records starting with REV or CON 
    are removed. The "Reporter intensity corrected"
    columns are extracted.
    -----
    Args:
        - divide_by_column_mean: bool
            * divide intensities by column-wise mean
        - take_log: apply log1p transformation, devide_by_mean 
            is applied before log-transformation if set to True.
        - normed:
            * None: Don't apply further normalization
            * diff_to_ref: Substract intensities of reference
            column (super-mix in channel 1).
            * fold_change: Divide by reference intensities.
        - drop_zero_q
        - melt: Return a melted DataFrame
    '''
<<<<<<< HEAD
    df = get_maxquant_txt(raw_file, txt='proteinGroups.txt')
=======
    df = get_maxquant_txt(path, txt='proteinGroups.txt', 
                          pipename=pipename, mq_run_name=mq_run_name)
>>>>>>> 9ccb24aada0a6dae9d8c718238bac60d07c267ef
    if len(df) == 0:
        return None
    df = df[~( df['Protein IDs'].str.startswith('REV_') | 
               df['Protein IDs'].str.startswith('CON_') )]
    if drop_zero_q:
        df = df[df['Q-value'] != 0]
    # Data columns
    data = df[data_cols+[protein_col]].copy()
    # Formating protein to shorter names.
    # Take second element by '|', if possible else 
    # the first element and allow 30 letters at max.
    # data[protein_col] = data[protein_col].apply(lambda x: x.split('|')[:2][-1][:30])
    # Just the reporter intensities
    reporter_intensity = df.iloc[:,list(range(22, 33))]
    # Replace 0 with NaN
    reporter_intensity = reporter_intensity.replace(0, np.NaN)
    assert normed in [None, 'fold_change', 'diff_to_ref']
    if divide_by_column_mean is True:
        # Devide by the mean column-wise
        reporter_intensity = ( reporter_intensity / reporter_intensity.mean() )
    if take_log is True:
        # Apply log(x+1) transformation
        reporter_intensity = reporter_intensity.apply(np.log1p)
    if normed == 'diff_to_ref':
        # Substract reference strain (TMT-channel 1) intensity
        reporter_intensity = reporter_intensity.add(-reporter_intensity['Reporter intensity corrected 1'], axis=0)
        del reporter_intensity['Reporter intensity corrected 1']
    if normed == 'fold_change':
        reporter_intensity = reporter_intensity.divide(reporter_intensity['Reporter intensity corrected 1'], axis=0)
        del reporter_intensity['Reporter intensity corrected 1']
    if mean_centering_per_plex:
        cols = reporter_intensity.filter(regex='Reporter intensity corrected').columns
        a = reporter_intensity.loc[:, cols].copy()
        row_means = a.mean(axis=1)
        a = a.subtract(row_means, axis=0)
        reporter_intensity.loc[:, cols] = a
            
    # Combine data with reporter int    
    output = pd.concat([data, reporter_intensity], axis=1)
    if melt:
        output = melt_protein_quant(output)      
    return output
<<<<<<< HEAD

def well_col_from_raw_fn(rawfile):
    try:
        xs = re.findall('-[ABCDEFGH]-', rawfile)[0][1]
        return xs 
    except:
        print('Could not extract row-id from file:', rawfile)
        if rawfile.startswith('SA009-R1-C'):
            print('Assigning row C')
            return 'C'
        return None


def get_protein_data(raw_files, divide_by_column_mean=True, take_log=True, normed='diff_to_ref', 
                     mean_centering_per_plex=False, protein_col='Protein IDs'):
    data = pd.concat([get_protein_quant(i, normed=normed, take_log=take_log,
                                        divide_by_column_mean=divide_by_column_mean, 
                                        mean_centering_per_plex=mean_centering_per_plex, 
                                        melt=False) 
                      for i in raw_files])
    melted = melt_protein_quant(data, protein_col=protein_col)
    melted[protein_col] = 'QUANT|' + melted[protein_col]
    
    pivoted = melted.pivot_table(values='RepInt', columns=['RawFile', 'TMT'],
                                 index=protein_col)
    proteins = pivoted.T.reset_index()
    proteins = proteins.reset_index(drop=True)
    proteins = proteins.set_index(['RawFile', 'TMT'])#.fillna(0).astype(int)
    proteins = proteins.reset_index()
    proteins.columns.name = None    
    proteins['PLATE'] = proteins.RawFile.apply(lambda x: x.split('-')[0])
    proteins['WELL_ROW'] = proteins.RawFile.apply(well_col_from_raw_fn)
    proteins['WELL_COL'] = 12 - proteins.TMT
    proteins = proteins.set_index(['RawFile', 'PLATE', 'WELL_ROW', 'WELL_COL', 'TMT']).reset_index()
    proteins['TMT'] = proteins['TMT'].apply(lambda x: f'{int(x):02.0f}')
    #del proteins['n_batch']
    return proteins
=======
>>>>>>> 9ccb24aada0a6dae9d8c718238bac60d07c267ef
