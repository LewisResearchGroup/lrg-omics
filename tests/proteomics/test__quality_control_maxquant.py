
import os
import pandas as pd


from lrg_omics.proteomics.quality_control.maxquant import maxquant_qc

PATH = os.path.join( 'tests', 'data', 'maxquant', 'tmt11', 'txt')


class TestClass:
    def test__maxquant_qc_is_dataframe(self):
        out = maxquant_qc(PATH)
        assert isinstance(out, pd.DataFrame), type(out)
    
    def test__maxquant_qc_columns(self):
        result = maxquant_qc(PATH).columns.to_list()
        expected = ['MS', 'MS/MS', 'MS3', 'MS/MS Submitted', 'MS/MS Identified', 'MS/MS Identified [%]',
        'Peptide Sequences Identified', 'Av. Absolute Mass Deviation [mDa]', 'Mass Standard Deviation [mDa]', 
        'N_protein_groups', 'N_protein_true_hits', 'N_missing_values', 'N_protein_potential_contaminants', 
        'N_protein_reverse_seq', 'Protein_mean_seq_cov [%]', 'N_peptides', 'N_peptides_potential_contaminants', 
        'N_peptides_reverse', 'Oxidations [%]', 'N_missed_cleavages_total', 'N_missed_cleavages_eq_0 [%]', 
        'N_missed_cleavages_eq_1 [%]', 'N_missed_cleavages_eq_2 [%]', 'N_missed_cleavages_gt_3 [%]', 
        'N_peptides_last_amino_acid_K [%]', 'N_peptides_last_amino_acid_R [%]', 'N_peptides_last_amino_acid_other [%]', 
        'Mean_parent_int_frac', 'Uncalibrated - Calibrated m/z [ppm] (ave)', 'Uncalibrated - Calibrated m/z [ppm] (sd)',
        'Uncalibrated - Calibrated m/z [Da] (ave)', 'Uncalibrated - Calibrated m/z [Da] (sd)', 'Peak Width(ave)',
        'Peak Width (std)', 'qc1_peptide_charge', 'N_qc1_missing_values', 'reporter_intensity_corrected_qc1_ave',
        'reporter_intensity_corrected_qc1_sd', 'reporter_intensity_corrected_qc1_cv', 'calibrated_retention time_qc1',
        'retention_length_qc1', 'N_of_scans_qc1', 'qc2_peptide_charge', 'N_qc2_missing_values', 
        'reporter_intensity_corrected_qc2_ave', 'reporter_intensity_corrected_qc2_sd',
        'reporter_intensity_corrected_qc2_cv', 'calibrated_retention time_qc2', 'retention_length_qc2',
        'N_of_scans_qc2', 'N_of_BSA_pepts', 'N_qc3_missing_values', 'reporter_intensity_corrected_qc3_ave',
        'reporter_intensity_corrected_qc3_sd', 'reporter_intensity_corrected_qc3_cv', 'RT_for_ATEEQLK',
        'Ave_Intensity_for_ATEEQLK', 'RT_for_AEFVEVTK', 'Ave_Intensity_for_AEFVEVTK', 'RT_for_QTALVELL',
        'Ave_Intensity_for_QTALVELL', 'RT_for_TVMENFVAFVDK', 'Ave_Intensity_for_TVMENFVAFVDK', 'RUNDIR']
        
        for n, (expect, actual) in enumerate( zip(expected, result) ) :
            if expect != actual:
                print(f'MISSMATCH ({n}): {expect} != {actual}')

        print(result)
        assert result == expected, ('Got these columns', result.to_list())