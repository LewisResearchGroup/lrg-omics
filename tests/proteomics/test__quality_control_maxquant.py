
import os
import pandas as pd


from lrg_omics.proteomics.quality_control.maxquant import \
    maxquant_qc

PATH = os.path.join( 'tests', 'data', 'maxquant', 'tmt11', 'txt')


class TestClass:
    def test__maxquant_qc_is_dataframe(self):
        out = maxquant_qc(PATH)
        assert isinstance(out, pd.DataFrame), type(out)
    
    def test__maxquant_qc_columns(self):
        result = maxquant_qc(PATH).columns.to_list()
        expected = ['MS',
        'MS/MS',
        'MS3',
        'MS/MS Submitted',
        'MS/MS Identified',
        'MS/MS Identified [%]',
        'Peptide Sequences Identified',
        'Av. Absolute Mass Deviation [mDa]',
        'Mass Standard Deviation [mDa]',
        'N_protein_groups',
        'N_protein_potential_contaminants',
        'N_protein_true_hits',
        'N_protein_reverse_seq',
        'Protein_mean_seq_cov [%]',
        'N_peptides',
        'N_peptides_potential_contaminants',
        'N_peptides_reverse',
        'Oxidations [%]',
        'N_missed_cleavages_total',
        'N_missed_cleavages_eq_0 [%]',
        'N_missed_cleavages_eq_1 [%]',
        'N_missed_cleavages_eq_2 [%]',
        'N_missed_cleavages_gt_3 [%]',
        'N_peptides_last_amino_acid_K [%]',
        'N_peptides_last_amino_acid_R [%]',
        'N_peptides_last_amino_acid_other [%]',
        'Mean_parent_int_frac',
        'RUNDIR']
        
        for n, (i, j) in enumerate( zip(expected, result) ) :
            if i != j:
                print(f'MISSMATCH ({n}): {i} != {j}')
                
        assert result == expected