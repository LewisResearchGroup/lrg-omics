# lrg_omics.proteomics.quality_control.maxquant
import pandas as pd
import numpy as np

from pathlib import Path as P
from glob import glob
from os.path import dirname, isdir, isfile, join, abspath

expected_columns = ['Date', 'LRG_omics version', 'PIPENAME', 'MAXQUANTBIN', 'RAW_file',
                    'FASTA_file', 'MQPAR_TEMP_file', 'MS', 'MS/MS', 'MS3',
                    'MS/MS Submitted', 'MS/MS Identified', 'MS/MS Identified [%]',
                    'Peptide Sequences Identified', 'Av. Absolute Mass Deviation [mDa]',
                    'Mass Standard Deviation [mDa]', 'N_protein_groups',
                    'N_protein_true_hits', 'N_protein_potential_contaminants',
                    'N_protein_reverse_seq', 'Protein_mean_seq_cov [%]',
                    'TMT1_missing_values', 'TMT2_missing_values', 'TMT3_missing_values',
                    'TMT4_missing_values', 'TMT5_missing_values', 'TMT6_missing_values',
                    'TMT7_missing_values', 'TMT8_missing_values', 'TMT9_missing_values',
                    'TMT10_missing_values', 'TMT11_missing_values', 'N_peptides',
                    'N_peptides_potential_contaminants', 'N_peptides_reverse',
                    'Oxidations [%]', 'N_missed_cleavages_total',
                    'N_missed_cleavages_eq_0 [%]', 'N_missed_cleavages_eq_1 [%]',
                    'N_missed_cleavages_eq_2 [%]', 'N_missed_cleavages_gt_3 [%]',
                    'N_peptides_last_amino_acid_K [%]', 'N_peptides_last_amino_acid_R [%]',
                    'N_peptides_last_amino_acid_other [%]', 'Mean_parent_int_frac',
                    'Uncalibrated - Calibrated m/z [ppm] (ave)',
                    'Uncalibrated - Calibrated m/z [ppm] (sd)',
                    'Uncalibrated - Calibrated m/z [Da] (ave)',
                    'Uncalibrated - Calibrated m/z [Da] (sd)', 'Peak Width(ave)',
                    'Peak Width (std)', 'qc1_peptide_charges', 'N_qc1_missing_values',
                    'reporter_intensity_corrected_qc1_ave',
                    'reporter_intensity_corrected_qc1_sd',
                    'reporter_intensity_corrected_qc1_cv', 'calibrated_retention_time_qc1',
                    'retention_length_qc1', 'N_of_scans_qc1', 'qc2_peptide_charges',
                    'N_qc2_missing_values', 'reporter_intensity_corrected_qc2_ave',
                    'reporter_intensity_corrected_qc2_sd',
                    'reporter_intensity_corrected_qc2_cv', 'calibrated_retention_time_qc2',
                    'retention_length_qc2', 'N_of_scans_qc2', 'N_of_Protein_qc_pepts',
                    'N_Protein_qc_missing_values',
                    'reporter_intensity_corrected_Protein_qc_ave',
                    'reporter_intensity_corrected_Protein_qc_sd',
                    'reporter_intensity_corrected_Protein_qc_cv', 'RUNDIR']


def collect_maxquant_qc_data(root_path, force_update=False, from_csvs=True):
    '''
    Generate MaxQuant quality control in all
    sub-directories of `root_path` where summary.txt is found.
    '''
    paths = [abspath(dirname(i)) for i in glob(f'{root_path}/**/summary.txt',
                                               recursive=True)]
    if len(paths) == 0: return None
    if from_csvs:
        dfs = [maxquant_qc_csv(path, force_update=force_update) for path in paths]
    else:
        dfs = [maxquant_qc(path) for path in paths]
    return pd.concat(dfs, sort=False).reset_index(drop=True)


def maxquant_qc_csv(txt_path, out_fn='maxquant_quality_control.csv',
                    force_update=False, ):
    abs_path = join(txt_path, out_fn)
    if isfile(abs_path) and not force_update:
        df = pd.read_csv(abs_path)
    else:
        df = maxquant_qc(txt_path)
        if out_fn is not None:
            df.to_csv(abs_path, index=False)
    df = df.reindex(columns=expected_columns)
    return df


def maxquant_qc(txt_path, protein=None, pept_list=None):
    '''
    Runs all MaxQuant quality control functions 
    and returns a concatenated pandas.Series() 
    object including meta data.
    Args:
        txt_path: path with MaxQuant txt output.
        protein: list with protein name (only the first one will be processed). If None then protein = ['BSA']
        pept_list: list with peptides names (only the first two will be processed). If None then pept_list = ['HVLTSIGEK', 'LTILEELR']
    '''
    txt_path = P(abspath(txt_path))
    meta_json = txt_path / P('meta.json')
    assert isdir(txt_path), f'Path does not exists: {txt_path}'
    dfs = []
    if isfile(meta_json):
        meta = pd.read_json(meta_json, typ='series')
        dfs.append(meta)
    try:
        for df in [maxquant_qc_summary(txt_path),
               maxquant_qc_protein_groups(txt_path, protein),
               maxquant_qc_peptides(txt_path),
               maxquant_qc_msmScans(txt_path),
               maxquant_qc_evidence(txt_path, pept_list)]:
            dfs.append(df)
    except:
        pass
    if len(dfs) == 0: return None
    df = pd.concat(dfs, sort=False).to_frame().T
    df['RUNDIR'] = str(txt_path)
    df = df.reindex(columns=expected_columns)
    return df


def maxquant_qc_summary(txt_path):
    filename = 'summary.txt'
    cols = ["MS", "MS/MS", "MS3", "MS/MS Submitted",
            "MS/MS Identified", "MS/MS Identified [%]",
            "Peptide Sequences Identified",
            "Av. Absolute Mass Deviation [mDa]",
            "Mass Standard Deviation [mDa]"]
    return pd.read_csv(txt_path / P(filename), sep='\t', nrows=1, usecols=cols).T[0]


def maxquant_qc_protein_groups(txt_path, protein=None):
    filename = 'proteinGroups.txt'
    df = pd.read_csv(txt_path / P(filename), sep='\t')
    n_contaminants = df['Potential contaminant'].eq('+').sum()
    n_reverse = df['Reverse'].fillna('-').eq('+').sum()
    n_true_hits = len(df) - (n_contaminants + n_reverse)
    mean_sequence_coverage = df[(df['Potential contaminant'].isnull()) &
                                (df['Reverse'].isnull())]['Sequence coverage [%]'].mean(skipna=True)

    df1 = df[(df['Potential contaminant'] != '+') &
             (df.Reverse != '+') &
             (df['Majority protein IDs'] != 'QC1|Peptide1') &
             (df['Majority protein IDs'] != 'QC2|Peptide2') &
             (df['Only identified by site'] != '+')]

    m_v = df1.filter(regex='Reporter intensity corrected').replace(np.nan, 0).isin([0]).sum().to_list()

    result = {
        "N_protein_groups": len(df),
        "N_protein_true_hits": n_true_hits,
        "N_protein_potential_contaminants": n_contaminants,
        "N_protein_reverse_seq": n_reverse,
        "Protein_mean_seq_cov [%]": mean_sequence_coverage
    }

    if len(m_v) != 0:
        l_1 = ["TMT1_missing_values", "TMT2_missing_values", "TMT3_missing_values", "TMT4_missing_values",
               "TMT5_missing_values", "TMT6_missing_values", "TMT7_missing_values", "TMT8_missing_values",
               "TMT9_missing_values", "TMT10_missing_values", "TMT11_missing_values"]
        l_2 = m_v + (11 - len(m_v)) * ['not detected']
        dic_m_v = dict(zip(l_1, l_2))
        result.update(dic_m_v)

    if protein is None:
        protein = ['BSA']

    df_qc3 = df[df['Protein IDs'].str.contains(protein[0], na=False, case=True)]
    if len(df_qc3) != 0:
        dict_info_qc3 = {
            "N_of_Protein_qc_pepts": df_qc3['Peptide counts (all)'].to_list(),
            "N_Protein_qc_missing_values": df_qc3.filter(regex='Reporter intensity corrected').replace(np.nan, 0).isin(
                [0]).sum().to_list(),
            "reporter_intensity_corrected_Protein_qc_ave": float(
                df_qc3.filter(regex='Reporter intensity corrected').mean(axis=1)),
            "reporter_intensity_corrected_Protein_qc_sd": float(
                df_qc3.filter(regex='Reporter intensity corrected').std(axis=1, ddof=0)),
            "reporter_intensity_corrected_Protein_qc_cv": float(
                df_qc3.filter(regex='Reporter intensity corrected').std(axis=1, ddof=0)) / float(df_qc3.filter(
                regex='Reporter intensity corrected').mean(axis=1)) * 100
        }

        result.update(dict_info_qc3)
    else:
        dict_info_qc3 = {
            "N_of_Protein_qc_pepts": "not detected",
            "N_Protein_qc_missing_values": "not detected",
            "reporter_intensity_corrected_Protein_qc_ave": "not detected",
            "reporter_intensity_corrected_Protein_qc_sd": "not detected",
            "reporter_intensity_corrected_Protein_qc_cv": "not detected"
        }
        result.update(dict_info_qc3)

    return pd.Series(result)


def maxquant_qc_peptides(txt_path):
    filename = 'peptides.txt'
    df = pd.read_csv(txt_path / P(filename), sep='\t')
    max_missed_cleavages = 3
    last_amino_acids = ['K', 'R']
    n_peptides = len(df)
    n_contaminants = df['Potential contaminant'].eq('+').sum()
    n_reverse = df['Reverse'].fillna('-').eq('+').sum()
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
    result[f'N_missed_cleavages_gt_{max_missed_cleavages} [%]'] = (df[
                                                                       'Missed cleavages'] > max_missed_cleavages).sum() / n_peptides * 100
    for amino in last_amino_acids:
        result[f'N_peptides_last_amino_acid_{amino} [%]'] = df['Last amino acid'].eq(amino).sum() / n_peptides * 100
    result['N_peptides_last_amino_acid_other [%]'] = (~df['Last amino acid'].isin(
        last_amino_acids)).sum() / n_peptides * 100
    return pd.Series(result).round(2)


def maxquant_qc_msmScans(txt_path, t0=None, tf=None):
    filename = 'msmsScans.txt'
    df = pd.read_csv(txt_path / P(filename), sep='\t')
    if t0 is None:
        t0 = df['Retention time'].min()
    if tf is None:
        tf = df['Retention time'].max()
    mean_parent_int_frac = df['Parent intensity fraction'].mean(skipna=True)
    results = {'Mean_parent_int_frac': mean_parent_int_frac}
    return pd.Series(results).round(2)


def maxquant_qc_evidence(txt_path, pept_list=None):
    filename = 'evidence.txt'
    df = pd.read_csv(txt_path / P(filename), sep='\t')

    result = {
        'Uncalibrated - Calibrated m/z [ppm] (ave)': df['Uncalibrated - Calibrated m/z [ppm]'].mean(skipna=True),
        'Uncalibrated - Calibrated m/z [ppm] (sd)': df['Uncalibrated - Calibrated m/z [ppm]'].std(ddof=0, skipna=True),
        'Uncalibrated - Calibrated m/z [Da] (ave)': df['Uncalibrated - Calibrated m/z [Da]'].mean(skipna=True),
        'Uncalibrated - Calibrated m/z [Da] (sd)': df['Uncalibrated - Calibrated m/z [Da]'].std(ddof=0, skipna=True),
        'Peak Width(ave)': df['Retention length'].mean(skipna=True),
        'Peak Width (std)': df['Retention length'].std(ddof=0, skipna=True)
    }

    if pept_list is None:
        pept_list = ['HVLTSIGEK', 'LTILEELR']
    elif len(pept_list) < 2:
        pept_list = pept_list + (2 - len(pept_list)) * ['dummy_peptide']
    elif len(pept_list) > 2:
        pept_list = pept_list[:2]

    for i in pept_list:
        df_pept = df[df.Sequence == i]
        if not df_pept.empty:
            charges = df_pept['Charge'].to_list()
            df_pept = df_pept[df.Intensity == df_pept.Intensity.max()]
            dict_info_qc = {
                f"qc{pept_list.index(i) + 1}_peptide_charges": charges,
                f"N_qc{pept_list.index(i) + 1}_missing_values": df_pept.filter(
                    regex='Reporter intensity corrected').replace(np.nan, 0).isin([0]).sum().to_list(),
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_ave": float(
                    df_pept.filter(regex='Reporter intensity corrected').mean(axis=1)),
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_sd": float(
                    df_pept.filter(regex='Reporter intensity corrected').std(axis=1, ddof=0)),
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_cv": float(
                    df_pept.filter(regex='Reporter intensity corrected').std(axis=1, ddof=0)) / float(df_pept.filter(
                    regex='Reporter intensity corrected').mean(axis=1)) * 100,
                f"calibrated_retention_time_qc{pept_list.index(i) + 1}": float(df_pept['Calibrated retention time']),
                f"retention_length_qc{pept_list.index(i) + 1}": float(df_pept['Retention length']),
                f"N_of_scans_qc{pept_list.index(i) + 1}": float(df_pept['Number of scans'])
            }

            result.update(dict_info_qc)
        else:
            dict_info_qc = {
                f"qc{pept_list.index(i) + 1}_peptide_charges": "not detected",
                f"N_qc{pept_list.index(i) + 1}_missing_values": "not detected",
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_ave": "not detected",
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_sd": "not detected",
                f"reporter_intensity_corrected_qc{pept_list.index(i) + 1}_cv": "not detected",
                f"calibrated_retention_time_qc{pept_list.index(i) + 1}": "not detected",
                f"retention_length_qc{pept_list.index(i) + 1}": "not detected",
                f"N_of_scans_qc{pept_list.index(i) + 1}": "not detected"
            }
            result.update(dict_info_qc)

    # qc_peptides_from_evidence_table = {
    #     'QC1|Peptide1_index': df.Proteins[df.Proteins == 'QC1|Peptide1'].index.tolist(),
    #     'QC2|Peptide2_index': df.Proteins[df.Proteins == 'QC2|Peptide2'].index.tolist()}
    #
    # dict_evidence_qc1 = {}
    # if len(qc_peptides_from_evidence_table['QC1|Peptide1_index']) != 0:
    #     for i in range(len(qc_peptides_from_evidence_table['QC1|Peptide1_index'])):
    #         reporter_intensity_corrected_qc1_values = df.loc[
    #             qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], [
    #                 'Reporter intensity corrected 1',
    #                 'Reporter intensity corrected 2',
    #                 'Reporter intensity corrected 3',
    #                 'Reporter intensity corrected 4',
    #                 'Reporter intensity corrected 5',
    #                 'Reporter intensity corrected 6',
    #                 'Reporter intensity corrected 7',
    #                 'Reporter intensity corrected 8',
    #                 'Reporter intensity corrected 9',
    #                 'Reporter intensity corrected 10',
    #                 'Reporter intensity corrected 11']].astype(
    #             float).to_list()
    #
    #         dict_evidence_qc1.update(
    #             {
    #                 f"{i}_QC1|Peptide1_charge_+{float(df.loc[qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], ['Charge']])}":
    #                     [reporter_intensity_corrected_qc1_values,
    #                      qc_peptides_from_evidence_table['QC1|Peptide1_index'][i],
    #                      float(df.loc[qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], ['Charge']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], [
    #                          'Calibrated retention time']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], ['Retention length']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC1|Peptide1_index'][i], ['Number of scans']])
    #                      ]})
    #
    #         # qc1_key_with_higher_ave = list(dict_evidence_qc1.keys())[
    #         #    list(dict_evidence_qc1.values()).index(max(list(dict_evidence_qc1.values())))]
    #
    #     charges = []
    #     for keys in dict_evidence_qc1:
    #         charges.append(dict_evidence_qc1[keys][2])
    #
    #     intensities = []
    #     for keys in dict_evidence_qc1:
    #         intensities.append(dict_evidence_qc1[keys][0])
    #
    #     intensities_sum = intensities[0]
    #     if len(intensities) > 1:
    #         for i in intensities[1:]:
    #             intensities_sum = [np.nansum(x) for x in zip(intensities_sum, i)]
    #     else:
    #         pass
    #
    #     log_intensities_sum = [np.log2(x) for x in intensities_sum if x > 0]
    #
    #     rts = []
    #     for keys in dict_evidence_qc1:
    #         rts.append(dict_evidence_qc1[keys][3])
    #
    #     rls = []
    #     for keys in dict_evidence_qc1:
    #         rls.append(dict_evidence_qc1[keys][4])
    #
    #     no_scans = []
    #     for keys in dict_evidence_qc1:
    #         no_scans.append(dict_evidence_qc1[keys][5])
    #
    #     dict_info_qc1 = {
    #         "qc1_peptide_charges": charges,
    #         "N_qc1_missing_values": 11 - np.count_nonzero(np.array(intensities_sum)),
    #         "reporter_intensity_corrected_qc1_ave": np.nanmean(np.array(log_intensities_sum)),
    #         "reporter_intensity_corrected_qc1_sd": np.nanstd(np.array(log_intensities_sum), ddof=0),
    #         "reporter_intensity_corrected_qc1_cv": (np.nanstd(np.array(log_intensities_sum), ddof=0) / np.nanmean(
    #             np.array(log_intensities_sum))) * 100,
    #         "calibrated_retention_time_qc1": np.nanmean(np.array(rts)),
    #         "retention_length_qc1": np.nanmean(np.array(rls)),
    #         "N_of_scans_qc1": no_scans
    #     }
    #
    #     result.update(dict_info_qc1)
    #
    # else:
    #
    #     dict_info_qc1 = {
    #         "qc1_peptide_charges": "not detected",
    #         "N_qc1_missing_values": "not detected",
    #         "reporter_intensity_corrected_qc1_ave": "not detected",
    #         "reporter_intensity_corrected_qc1_sd": "not detected",
    #         "reporter_intensity_corrected_qc1_cv": "not detected",
    #         'calibrated_retention_time_qc1': 'not detected',
    #         'retention_length_qc1': 'not detected',
    #         "N_of_scans_qc1": 'not detected'
    #     }
    #
    #     result.update(dict_info_qc1)
    #
    # dict_evidence_qc2 = {}
    # if len(qc_peptides_from_evidence_table['QC2|Peptide2_index']) != 0:
    #     for i in range(len(qc_peptides_from_evidence_table['QC2|Peptide2_index'])):
    #         reporter_intensity_corrected_qc2_values = df.loc[
    #             qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], [
    #                 'Reporter intensity corrected 1',
    #                 'Reporter intensity corrected 2',
    #                 'Reporter intensity corrected 3',
    #                 'Reporter intensity corrected 4',
    #                 'Reporter intensity corrected 5',
    #                 'Reporter intensity corrected 6',
    #                 'Reporter intensity corrected 7',
    #                 'Reporter intensity corrected 8',
    #                 'Reporter intensity corrected 9',
    #                 'Reporter intensity corrected 10',
    #                 'Reporter intensity corrected 11']].astype(
    #             float).to_list()
    #
    #         dict_evidence_qc2.update(
    #             {
    #                 f"{i}_QC2|Peptide2_charge_+{float(df.loc[qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], ['Charge']])}":
    #                     [reporter_intensity_corrected_qc2_values,
    #                      qc_peptides_from_evidence_table['QC2|Peptide2_index'][i],
    #                      float(df.loc[qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], ['Charge']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], [
    #                          'Calibrated retention time']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], ['Retention length']]),
    #                      float(df.loc[qc_peptides_from_evidence_table['QC2|Peptide2_index'][i], ['Number of scans']])
    #                      ]})
    #
    #         # qc2_key_with_higher_ave = list(dict_evidence_qc2.keys())[
    #         #    list(dict_evidence_qc2.values()).index(max(list(dict_evidence_qc2.values())))]
    #
    #     charges = []
    #     for keys in dict_evidence_qc2:
    #         charges.append(dict_evidence_qc2[keys][2])
    #
    #     intensities = []
    #     for keys in dict_evidence_qc2:
    #         intensities.append(dict_evidence_qc2[keys][0])
    #
    #     intensities_sum = intensities[0]
    #     if len(intensities) > 1:
    #         for i in intensities[1:]:
    #             intensities_sum = [np.nansum(x) for x in zip(intensities_sum, i)]
    #     else:
    #         pass
    #
    #     log_intensities_sum = [np.log2(x) for x in intensities_sum if x > 0]
    #
    #     rts = []
    #     for keys in dict_evidence_qc2:
    #         rts.append(dict_evidence_qc2[keys][3])
    #
    #     rls = []
    #     for keys in dict_evidence_qc2:
    #         rls.append(dict_evidence_qc2[keys][4])
    #
    #     no_scans = []
    #     for keys in dict_evidence_qc2:
    #         no_scans.append(dict_evidence_qc2[keys][5])
    #
    #     dict_info_qc2 = {
    #         "qc2_peptide_charges": charges,
    #         "N_qc2_missing_values": 11 - np.count_nonzero(np.array(intensities_sum)),
    #         "reporter_intensity_corrected_qc2_ave": np.nanmean(np.array(log_intensities_sum)),
    #         "reporter_intensity_corrected_qc2_sd": np.nanstd(np.array(log_intensities_sum), ddof=0),
    #         "reporter_intensity_corrected_qc2_cv": (np.nanstd(np.array(log_intensities_sum), ddof=0) / np.nanmean(
    #             np.array(log_intensities_sum))) * 100,
    #         "calibrated_retention_time_qc2": np.nanmean(np.array(rts)),
    #         "retention_length_qc2": np.nanmean(np.array(rls)),
    #         "N_of_scans_qc2": no_scans
    #     }
    #
    #     result.update(dict_info_qc2)
    #
    # else:
    #
    #     dict_info_qc2 = {
    #         "qc2_peptide_charges": "not detected",
    #         "N_qc2_missing_values": "not detected",
    #         "reporter_intensity_corrected_qc2_ave": "not detected",
    #         "reporter_intensity_corrected_qc2_sd": "not detected",
    #         "reporter_intensity_corrected_qc2_cv": "not detected",
    #         'calibrated_retention_time_qc2': 'not detected',
    #         'retention_length_qc2': 'not detected',
    #         "N_of_scans_qc2": 'not detected'
    #     }
    #
    #     result.update(dict_info_qc2)
    #
    # dict_evidence_qc3 = {}
    #
    # df_qc3 = df[df.Proteins.str.contains('QC3|BSA', na=False)]
    # if len(df_qc3) != 0:
    #     df_qc3 = df_qc3[['Sequence', 'Proteins', 'Calibrated retention time',
    #                      'Reporter intensity corrected 1',
    #                      'Reporter intensity corrected 2',
    #                      'Reporter intensity corrected 3',
    #                      'Reporter intensity corrected 4',
    #                      'Reporter intensity corrected 5',
    #                      'Reporter intensity corrected 6',
    #                      'Reporter intensity corrected 7',
    #                      'Reporter intensity corrected 8',
    #                      'Reporter intensity corrected 9',
    #                      'Reporter intensity corrected 10',
    #                      'Reporter intensity corrected 11']]
    #
    #     df_qc3.index = pd.RangeIndex(len(df_qc3.index))
    #
    #     df_qc3_mod = df_qc3.groupby(['Sequence'], as_index=False).agg({'Calibrated retention time': [np.nanmean],
    #                                                                    'Reporter intensity corrected 1': [np.nansum],
    #                                                                    'Reporter intensity corrected 2': [np.nansum],
    #                                                                    'Reporter intensity corrected 3': [np.nansum],
    #                                                                    'Reporter intensity corrected 4': [np.nansum],
    #                                                                    'Reporter intensity corrected 5': [np.nansum],
    #                                                                    'Reporter intensity corrected 6': [np.nansum],
    #                                                                    'Reporter intensity corrected 7': [np.nansum],
    #                                                                    'Reporter intensity corrected 8': [np.nansum],
    #                                                                    'Reporter intensity corrected 9': [np.nansum],
    #                                                                    'Reporter intensity corrected 10': [np.nansum],
    #                                                                    'Reporter intensity corrected 11': [np.nansum]})
    #     df_qc3_mod.columns = df_qc3_mod.columns.droplevel(1)
    #     no_of_pept = len(df_qc3_mod)
    #
    #     for i in ['ATEEQLK', 'AEFVEVTK', 'QTALVELLK', 'TVMENFVAFVDK']:
    #         if i not in df_qc3_mod.Sequence.to_list():
    #             df_qc3_mod.loc[len(df_qc3_mod)] = [i] + [np.nan]*(len(df_qc3_mod.columns) - 1)
    #
    #     df_qc3_mod.loc["Row_Total"] = df_qc3_mod.iloc[:, 2:].sum(numeric_only=True).replace(0, 1)
    #     df_qc3_mod.loc["Row_Log2_Total"] = [np.log2(x) for x in df_qc3_mod.loc["Row_Total"].to_list()]
    #
    #     dict_evidence_qc3.update({"N_of_BSA_pepts": no_of_pept,
    #                               "N_qc3_missing_values": 11 - np.count_nonzero(np.array(df_qc3_mod.iloc[-1, 2:])),
    #                               "reporter_intensity_corrected_qc3_ave": np.nanmean(
    #                                   np.array(df_qc3_mod.loc["Row_Log2_Total"])),
    #                               "reporter_intensity_corrected_qc3_sd": np.nanstd(
    #                                   np.array(df_qc3_mod.loc["Row_Log2_Total"]), ddof=0),
    #                               "reporter_intensity_corrected_qc3_cv": (np.nanstd(
    #                                   np.array(df_qc3_mod.loc["Row_Log2_Total"]), ddof=0)
    #                                                                       / np.nanmean(
    #                                           np.array(df_qc3_mod.loc["Row_Log2_Total"]))) * 100,
    #                               'RT_for_ATEEQLK':
    #                                   float(
    #                                       df_qc3_mod[
    #                                           df_qc3_mod['Sequence'].str.contains('ATEEQLK').replace(np.nan, False)][
    #                                           'Calibrated retention time']),
    #                               'Ave_Intensity_for_ATEEQLK': float(df_qc3_mod[
    #                                                                      df_qc3_mod['Sequence'].str.contains(
    #                                                                          'ATEEQLK').replace(
    #                                                                          np.nan, False)].iloc[:, 2:].mean(
    #                                   skipna=True,
    #                                   axis=1)),
    #                               'RT_for_AEFVEVTK':
    #                                   float(df_qc3_mod[
    #                                             df_qc3_mod['Sequence'].str.contains('AEFVEVTK').replace(np.nan, False)][
    #                                             'Calibrated retention time']),
    #                               'Ave_Intensity_for_AEFVEVTK': float(df_qc3_mod[
    #                                                                       df_qc3_mod['Sequence'].str.contains(
    #                                                                           'AEFVEVTK').replace(
    #                                                                           np.nan, False)].iloc[:, 2:].mean(
    #                                   skipna=True,
    #                                   axis=1)),
    #                               'RT_for_QTALVELLK':
    #                                   float(df_qc3_mod[
    #                                             df_qc3_mod['Sequence'].str.contains('QTALVELLK').replace(np.nan, False)][
    #                                             'Calibrated retention time']),
    #                               'Ave_Intensity_for_QTALVELLK': float(df_qc3_mod[
    #                                                                       df_qc3_mod['Sequence'].str.contains(
    #                                                                           'QTALVELLK').replace(
    #                                                                           np.nan, False)].iloc[:, 2:].mean(
    #                                   skipna=True,
    #                                   axis=1)),
    #                               'RT_for_TVMENFVAFVDK':
    #                                   float(df_qc3_mod[
    #                                             df_qc3_mod['Sequence'].str.contains('TVMENFVAFVDK').replace(np.nan,
    #                                                                                                         False)][
    #                                             'Calibrated retention time']),
    #                               'Ave_Intensity_for_TVMENFVAFVDK': float(df_qc3_mod[
    #                                                                           df_qc3_mod['Sequence'].str.contains(
    #                                                                               'TVMENFVAFVDK').replace(
    #                                                                               np.nan, False)].iloc[:, 2:].mean(
    #                                   skipna=True,
    #                                   axis=1))
    #                               })
    #     result.update(dict_evidence_qc3)
    #
    # else:
    #     dict_evidence_qc3.update({"N_of_BSA_pepts": "not detected",
    #                               "N_qc3_missing_values": "not detected",
    #                               "reporter_intensity_corrected_qc3_ave": "not detected",
    #                               "reporter_intensity_corrected_qc3_sd": "not detected",
    #                               "reporter_intensity_corrected_qc3_cv": "not detected",
    #                               'RT_for_ATEEQLK': "not detected",
    #                               'Ave_Intensity_for_ATEEQLK': "not detected",
    #                               'RT_for_AEFVEVTK': "not detected",
    #                               'Ave_Intensity_for_AEFVEVTK': "not detected",
    #                               'RT_for_QTALVELLK': "not detected",
    #                               'Ave_Intensity_for_QTALVELLK': "not detected",
    #                               'RT_for_TVMENFVAFVDK': "not detected",
    #                               'Ave_Intensity_for_TVMENFVAFVDK': "not detected"
    #                               })
    #     result.update(dict_evidence_qc3)

    return pd.Series(result)

