# lgr_omics.proteomics.quality_control.maxquant
import os
import pandas as pd

from pathlib import Path as P
from glob import glob
from os.path import dirname, isdir, isfile, basename

def collect_maxquant_qc_data(root_path):
    update_maxquant_qc_data(root_path)
    csvs = glob(f'{root_path}/**/maxquant_quality_control.csv', recursive=True)
    dfs = [pd.read_csv(csv) for csv in csvs]
    df = pd.concat(dfs, sort=False)
    df.index = range(len(df))
    return df


def update_maxquant_qc_data(root_path, force_update=False):
    paths = [dirname(i) for i in glob(f'{root_path}/**/summary.txt', recursive=True)]
    for path in paths:
        generate_maxquant_qc_data(path, force_update=force_update)


def maxquant_qc(txt_path, output='maxquant_quality_control.csv', force_update=False):
    '''
    Runs all MaxQuant quality control functions 
    and returns a concatenated pandas.Series() 
    object including meta data.
    Args:
        txt_path: path with MaxQuant txt output.
    '''
    txt_path = P(txt_path)
    to_csv = False
    meta_json = txt_path/P('meta.json')

    if output is not None:
        fn_output = txt_path/P(output)
        if output.endswith('.csv'):
            to_csv = True

    assert isdir(txt_path), f'Path does not exists: {txt_path}'
    
    dfs = []
    if isfile(meta_json):
        meta = pd.read_json(meta_json, typ='series')
        dfs.append(meta)
    for df in [maxquant_qc_summary(txt_path),
            maxquant_qc_protein_groups(txt_path),
            maxquant_qc_peptides(txt_path),
            maxquant_qc_msmScans(txt_path)]:
        dfs.append(df)
    df = pd.concat(dfs, sort=False).to_frame().T
    df['RUNDIR'] = str(txt_path)
    if to_csv:
        df.to_csv(fn_output, index=False)
    return df


def maxquant_qc_summary(txt_path):
    filename = 'summary.txt'
    cols = ["MS", "MS/MS", "MS3", "MS/MS Submitted", 
            "MS/MS Identified", "MS/MS Identified [%]",  
            "Peptide Sequences Identified", 
            "Av. Absolute Mass Deviation [mDa]",
            "Mass Standard Deviation [mDa]"]
    return pd.read_csv(txt_path/P(filename), sep='\t', nrows=1, usecols=cols).T[0]


def maxquant_qc_protein_groups(txt_path):
    filename = 'proteinGroups.txt'
    df = pd.read_csv(txt_path/P(filename), sep='\t')
    n_contaminants = df['Potential contaminant'].eq('+').sum()
    n_reverse = df['Reverse'].fillna('-').eq('+').sum()
    # assert df[['Potential contaminant', 'Reverse']].eq('+').sum(axis=1).max() <= 1
    n_true_hits = len(df) - (n_contaminants + n_reverse)
    mean_sequence_coverage = df[(df['Potential contaminant'].isnull()) &
                                (df['Reverse'].isnull())]['Sequence coverage [%]'].mean()
    result = {
        "N_protein_groups": len(df),
        "N_protein_potential_contaminants": n_contaminants,
        "N_protein_true_hits": n_true_hits,
        "N_protein_reverse_seq": n_reverse,
        "Protein_mean_seq_cov [%]": mean_sequence_coverage
        }
    return pd.Series(result).round(2)


def maxquant_qc_peptides(txt_path):
    filename = 'peptides.txt'
    df = pd.read_csv(txt_path/P(filename), sep='\t')
    max_missed_cleavages = 3
    last_amino_acids = ['K', 'R']
    n_peptides = len(df)
    n_contaminants = df['Potential contaminant'].eq('+').sum()
    n_reverse = df['Reverse'].fillna('-').eq('+').sum()
    # assert df[['Potential contaminant', 'Reverse']].eq('+').sum(axis=1).max() <= 1
    ox_pep_seq = len(df) - df['Oxidation (M) site IDs'].isnull().sum()
    ox_pep_seq_percent = ox_pep_seq / n_peptides * 100
    result = {
        'N_peptides': n_peptides,
        'N_peptides_potential_contaminants': n_contaminants,
        'N_peptides_reverse': n_reverse,
        'Oxidations [%]': ox_pep_seq_percent,
        'N_missed_cleavages_total': (df['Missed cleavages'] != 0).sum()
    }
    for n in range(max_missed_cleavages):
        result[f'N_missed_cleavages_eq_{n} [%]'] = (df['Missed cleavages'] == n).sum() / n_peptides * 100
    result[f'N_missed_cleavages_gt_{max_missed_cleavages} [%]'] = (df['Missed cleavages'] > max_missed_cleavages).sum() / n_peptides * 100
    for amino in last_amino_acids:
        result[f'N_peptides_last_amino_acid_{amino} [%]'] = df['Last amino acid'].eq(amino).sum() / n_peptides * 100
    result['N_peptides_last_amino_acid_other [%]'] = (~df['Last amino acid'].isin(last_amino_acids)).sum() / n_peptides * 100       
    return pd.Series(result).round(2)


def maxquant_qc_msmScans(txt_path, t0=None, tf=None):
    filename = 'msmsScans.txt'
    df = pd.read_csv(txt_path/P(filename), sep='\t')
    if t0 is None:
        t0 = df['Retention time'].min()
    if tf is None:
        tf = df['Retention time'].max()
    mean_parent_int_frac = df['Parent intensity fraction'].mean()
    df_filtered_peaks = df[['Retention time', 'Filtered peaks']].set_index('Retention time')
    x = df_filtered_peaks.loc[t0:tf].index
    y = df_filtered_peaks.loc[t0:tf, 'Filtered peaks'].values
    results = {'Mean_parent_intensity_fraction': mean_parent_int_frac, 
              }
    return pd.Series(results).round(2)

