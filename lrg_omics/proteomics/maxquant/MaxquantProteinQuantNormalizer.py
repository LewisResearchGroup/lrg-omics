import pandas as pd
import numpy as np
import logging

from tqdm import tqdm
from pathlib import Path as P

from .MaxquantReader import MaxquantReader


class MaxquantProteinQuantNormalizer():
    def __init__(self, paths, map_to_tmt_channel=True):
        """
        Path is a list of paths towards Maxquant results folders.
        They are expected to contain proteinGroups.txt file.
        The name of the folder is taken as RawName.

        It should be something like:
        
        .../SA001-A/proteinGroups.txt
        .../SA001-B/proteinGroups.txt

        Then the data in this file will be stored as RawFile=SA001-A, RawFile=SA001-B, etc.

        Usage example:        
            
            mpqn = MaxquantProteinQuantNormalizer()
            mpqn.read(paths)
            df = mpqn.normalize(...)

        """

        self._df_paths = paths_to_df(paths)
        self.df_protein_groups = None
        self._read_protein_groups()
        self._map_to_tmt_channel = map_to_tmt_channel
        self._tmt_mapping = {f'Reporter intensity corrected {i}':  f'{i:02.0f}' for i in range(1, 24)}


    def _read_protein_groups(self):
        data = []
        for path, rawfile in tqdm(self._df_paths[['Path', 'RawFile']].values):
            fn = P(path)/'proteinGroups.txt'
            if not fn.is_file():
                logging.warning(f'FileNotFound: {fn}')
                continue
            df = MaxquantReader().read(P(path)/'proteinGroups.txt')
            df['RawFile'] = rawfile
            data.append(df)
        self.df_protein_groups = pd.concat(data).set_index('RawFile').reset_index()


    def normalize(self, fmt='plex', 
                  divide_by_column_mean=True, 
                  take_log=True,
                  normed='fold_change', 
                  mean_centering_per_plex=False,
                  drop_zero_q=False, 
                  data_cols=None,
                  protein_col='Fasta headers'):
        """
        Applies normalization and returns normalized datafame in specific format.
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
        """
        if data_cols is None: data_cols = []

        df = self.df_protein_groups
        minimum_n_of_values = 3
        n_of_values = (df.filter(regex='Reporter intensity corrected')!=0).sum(axis=1)        
        df = df[ n_of_values >= minimum_n_of_values]
        df = df[df['Reporter intensity corrected 1'] != 0]

        data = df[[protein_col]+data_cols].copy()
        reporter_intensity = df.filter(regex='RawFile|Reporter intensity corrected')
        
        # Replace 0 with NaN
        reporter_intensity = reporter_intensity.replace(0, np.NaN)

        self.reporter_intensity = reporter_intensity
         
        grps = reporter_intensity.groupby('RawFile')
        grps_normed = []

        for RawFile, grp in tqdm(grps):
            grp = grp.set_index('RawFile')
            grp = grp / grp.mean()
            grp = grp.divide( grp['Reporter intensity corrected 1'].values, axis=0)
            grp = grp.applymap(log2p1)
            grp = grp.sub(grp.mean(axis=1, skipna=True).values, axis=0)
            grps_normed.append(grp)

        reporter_intensity = pd.concat(grps_normed).reset_index()
        reporter_intensity.index = data.index

        del grps_normed, grps

        # Combine data with reporter int    

        output = pd.concat([data, reporter_intensity], axis=1)
     
        if output.reset_index().groupby(['RawFile', protein_col]).count().max().max() > 1:
            logging.warning(f'Found duplicated index (RawFile, {protein_col}) taking first')
            output = output.groupby(['RawFile', protein_col]).first()

        output = output.rename(columns=self._tmt_mapping)
        output.columns.name = 'TMT_CHANNEL'        
        
        if fmt == 'plex':
            return output
        elif fmt == 'sample':
            return output.unstack(protein_col).stack('TMT_CHANNEL')
        elif fmt == 'long':
            return output.reset_index().melt(id_vars=['RawFile', protein_col], var_name='TMT_CHANNEL', value_name='PROTEIN_QUANT')


def melt_protein_quant(df, id_vars=None, var_name='TMT'):
    if id_vars is None:
        id_vars = df.filter(regex='^(?!.*Reporter.*)').columns
    output = df.melt(id_vars=id_vars, var_name=var_name, value_name='ReporterIntensity')
    output['TMT'] = output['TMT'].str.replace('Reporter intensity corrected ', '').astype(int)
    return output


def log2p1(x):
    return np.log2(x+1)


def paths_to_df(paths):
    df = pd.DataFrame({'Path': paths})
    df['Path'] = df.Path.apply(lambda x: P(x).resolve())
    df['RawFile'] = df.Path.apply(lambda x: P(x).name)
    return df


