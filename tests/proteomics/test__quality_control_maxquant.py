import pandas as pd
import os
import pytest

from lrg_omics.proteomics.maxquant.quality_control import (
    maxquant_qc,
    maxquant_qc_summary,
    maxquant_qc_protein_groups,
    maxquant_qc_peptides,
    maxquant_qc_msmScans,
    maxquant_qc_evidence,
)

PATH = os.path.join("tests", "data", "maxquant", "tmt11", "example-0")


def _write_tsv(path, filename, data):
    pd.DataFrame(data).to_csv(os.path.join(path, filename), sep="\t", index=False)


def _build_protein_groups(path, channels, rows=None):
    row_template = {
        "Potential contaminant": None,
        "Reverse": None,
        "Majority protein IDs": "P00001",
        "Only identified by site": None,
        "Sequence coverage [%]": 50.0,
        "Protein IDs": "P00001",
        "Intensity": 1000.0,
        "Peptide counts (all)": 5,
    }
    if rows is None:
        rows = [
            {**row_template},
            {
                **row_template,
                "Majority protein IDs": "QC3_BSA",
                "Protein IDs": "QC3_BSA",
                "Intensity": 2000.0,
                "Peptide counts (all)": 11,
            },
        ]

    for row_idx, row in enumerate(rows):
        for ch in range(1, channels + 1):
            row[f"Reporter intensity corrected {ch}"] = (
                0 if (row_idx == 0 and ch % 2 == 0) else 1000 + ch
            )
    _write_tsv(path, "proteinGroups.txt", rows)


class TestClass:
    def test__maxquant_qc_summary(self):
        out = maxquant_qc_summary(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f"It is a {type(out)} not a Series"

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = [
            "MS",
            "MS/MS",
            "MS3",
            "MS/MS Submitted",
            "MS/MS Identified",
            "MS/MS Identified [%]",
            "Peptide Sequences Identified",
            "Av. Absolute Mass Deviation [mDa]",
            "Mass Standard " "Deviation [mDa]",
        ]

        assert len(expected_cols) - len(out.index) == 0, (
            f"New columns {out.index[len(expected_cols):]} in output "
            f"file. Adjust expected_cols variable accordingly"
        )

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(
            set(expected_cols) - set(out.index)
        )

        # check if there is any NaN value in out
        assert (
            ~out.isnull().values.any()
        ), f"NaN value at {out.index[out.isna().any()].tolist()}"

    def test__maxquant_qc_protein_groups(self):
        out = maxquant_qc_protein_groups(PATH, protein=None)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f"It is a {type(out)} not a Series"

        actual_ndx = out.index.to_list()

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_ndx = [
            "N_protein_groups",
            "N_protein_true_hits",
            "N_protein_potential_contaminants",
            "N_protein_reverse_seq",
            "Protein_mean_seq_cov [%]",
            "TMT1_missing_values",
            "TMT2_missing_values",
            "TMT3_missing_values",
            "TMT4_missing_values",
            "TMT5_missing_values",
            "TMT6_missing_values",
            "TMT7_missing_values",
            "TMT8_missing_values",
            "TMT9_missing_values",
            "TMT10_missing_values",
            "TMT11_missing_values",
            "Protein_qc",
            "N_of_Protein_qc_pepts",
            "N_Protein_qc_missing_values",
            "reporter_intensity_corrected_Protein_qc_ave",
            "reporter_intensity_corrected_Protein_qc_sd",
            "reporter_intensity_corrected_Protein_qc_cv",
        ]

        assert len(expected_ndx) - len(actual_ndx) == 0, (
            f"New columns {actual_ndx[len(expected_ndx):]} in output "
            f"file. Adjust expected_cols variable accordingly"
        )

        # check for mismatches between columns in expected_ndx and out
        assert len(list(set(expected_ndx) - set(actual_ndx))) == 0, list(
            set(expected_ndx) - set(actual_ndx)
        )

        # check if there is any NaN values in out
        assert (
            ~out.isnull().values.any()
        ), f"NaN value at {actual_ndx[out.isna().any()].tolist()}"

    def test__maxquant_qc_peptides(self):
        out = maxquant_qc_peptides(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f"It is a {type(out)} not a Series"

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = [
            "N_peptides",
            "N_peptides_potential_contaminants",
            "N_peptides_reverse",
            "Oxidations [%]",
            "N_missed_cleavages_total",
            "N_missed_cleavages_eq_0 [%]",
            "N_missed_cleavages_eq_1 [%]",
            "N_missed_cleavages_eq_2 [%]",
            "N_missed_cleavages_gt_3 [%]",
            "N_peptides_last_amino_acid_K [%]",
            "N_peptides_last_amino_acid_R [%]",
            "N_peptides_last_amino_acid_other [%]",
        ]

        assert len(expected_cols) - len(out.index) == 0, (
            f"New columns {out.index[len(expected_cols):]} in output "
            f"file. Adjust expected_cols variable accordingly"
        )

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(
            set(expected_cols) - set(out.index)
        )

        # check if there is any NaN values in out
        assert (
            ~out.isnull().values.any()
        ), f"NaN value at {out.index[out.isna().any()].tolist()}"

    def test__maxquant_qc_msmScans(self):
        out = maxquant_qc_msmScans(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f"It is a {type(out)} not a Series"

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ["Mean_parent_int_frac"]

        assert len(expected_cols) - len(out.index) == 0, (
            f"New columns {out.index[len(expected_cols):]} in output "
            f"file. Adjust expected_cols variable accordingly"
        )

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(
            set(expected_cols) - set(out.index)
        )

        # check if there is any NaN values in out
        assert (
            ~out.isnull().values.any()
        ), f"NaN value at {out.index[out.isna().any()].tolist()}"

    def test__maxquant_qc_evidence(self):
        out = maxquant_qc_evidence(PATH, pept_list=None)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f"It is a {type(out)} not a Series"

        actual_ndx = out.index.to_list()

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file

        expected_ndx = [
            "Uncalibrated - Calibrated m/z [ppm] (ave)",
            "Uncalibrated - Calibrated m/z [ppm] (sd)",
            "Uncalibrated - Calibrated m/z [Da] (ave)",
            "Uncalibrated - Calibrated m/z [Da] (sd)",
            "Peak Width(ave)",
            "Peak Width (std)",
            "qc1_peptide_charges",
            "N_qc1_missing_values",
            "reporter_intensity_corrected_qc1_ave",
            "reporter_intensity_corrected_qc1_sd",
            "reporter_intensity_corrected_qc1_cv",
            "calibrated_retention_time_qc1",
            "retention_length_qc1",
            "N_of_scans_qc1",
            "qc2_peptide_charges",
            "N_qc2_missing_values",
            "reporter_intensity_corrected_qc2_ave",
            "reporter_intensity_corrected_qc2_sd",
            "reporter_intensity_corrected_qc2_cv",
            "calibrated_retention_time_qc2",
            "retention_length_qc2",
            "N_of_scans_qc2",
            "qc3_peptide_charges",
            "N_qc3_missing_values",
            "reporter_intensity_corrected_qc3_ave",
            "reporter_intensity_corrected_qc3_sd",
            "reporter_intensity_corrected_qc3_cv",
            "calibrated_retention_time_qc3",
            "retention_length_qc3",
            "N_of_scans_qc3",
            "qc4_peptide_charges",
            "N_qc4_missing_values",
            "reporter_intensity_corrected_qc4_ave",
            "reporter_intensity_corrected_qc4_sd",
            "reporter_intensity_corrected_qc4_cv",
            "calibrated_retention_time_qc4",
            "retention_length_qc4",
            "N_of_scans_qc4",
            "qc5_peptide_charges",
            "N_qc5_missing_values",
            "reporter_intensity_corrected_qc5_ave",
            "reporter_intensity_corrected_qc5_sd",
            "reporter_intensity_corrected_qc5_cv",
            "calibrated_retention_time_qc5",
            "retention_length_qc5",
            "N_of_scans_qc5",
            "qc6_peptide_charges",
            "N_qc6_missing_values",
            "reporter_intensity_corrected_qc6_ave",
            "reporter_intensity_corrected_qc6_sd",
            "reporter_intensity_corrected_qc6_cv",
            "calibrated_retention_time_qc6",
            "retention_length_qc6",
            "N_of_scans_qc6",
        ]

        assert len(expected_ndx) - len(actual_ndx) == 0, (
            f"New columns {actual_ndx[len(expected_ndx):]} in output "
            f"file. Adjust expected_cols variable accordingly"
        )

        # check for mismatches between columns in expected_ndx and out
        assert len(list(set(expected_ndx) - set(actual_ndx))) == 0, list(
            set(expected_ndx) - set(actual_ndx)
        )

        # check if there is any NaN values in out
        assert (
            ~out.isnull().values.any()
        ), f"NaN value at {out[out.isna()].index.to_list()}"

    def test__maxquant_qc_columns(self):
        result = maxquant_qc(PATH, protein=None, pept_list=None)
        actual_cols = result.columns

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = [
            "Date",
            "MS",
            "MS/MS",
            "MS3",
            "MS/MS Submitted",
            "MS/MS Identified",
            "MS/MS Identified [%]",
            "Peptide Sequences Identified",
            "Av. Absolute Mass Deviation [mDa]",
            "Mass Standard Deviation [mDa]",
            "N_protein_groups",
            "N_protein_true_hits",
            "N_protein_potential_contaminants",
            "N_protein_reverse_seq",
            "Protein_mean_seq_cov [%]",
            "TMT1_missing_values",
            "TMT2_missing_values",
            "TMT3_missing_values",
            "TMT4_missing_values",
            "TMT5_missing_values",
            "TMT6_missing_values",
            "TMT7_missing_values",
            "TMT8_missing_values",
            "TMT9_missing_values",
            "TMT10_missing_values",
            "TMT11_missing_values",
            "N_peptides",
            "N_peptides_potential_contaminants",
            "N_peptides_reverse",
            "Oxidations [%]",
            "N_missed_cleavages_total",
            "N_missed_cleavages_eq_0 [%]",
            "N_missed_cleavages_eq_1 [%]",
            "N_missed_cleavages_eq_2 [%]",
            "N_missed_cleavages_gt_3 [%]",
            "N_peptides_last_amino_acid_K [%]",
            "N_peptides_last_amino_acid_R [%]",
            "N_peptides_last_amino_acid_other [%]",
            "Mean_parent_int_frac",
            "Uncalibrated - Calibrated m/z [ppm] (ave)",
            "Uncalibrated - Calibrated m/z [ppm] (sd)",
            "Uncalibrated - Calibrated m/z [Da] (ave)",
            "Uncalibrated - Calibrated m/z [Da] (sd)",
            "Peak Width(ave)",
            "Peak Width (std)",
            # 'qc1_peptide',
            "qc1_peptide_charges",
            "N_qc1_missing_values",
            "reporter_intensity_corrected_qc1_ave",
            "reporter_intensity_corrected_qc1_sd",
            "reporter_intensity_corrected_qc1_cv",
            "calibrated_retention_time_qc1",
            "retention_length_qc1",
            "N_of_scans_qc1",
            #'qc2_peptide',
            "qc2_peptide_charges",
            "N_qc2_missing_values",
            "reporter_intensity_corrected_qc2_ave",
            "reporter_intensity_corrected_qc2_sd",
            "reporter_intensity_corrected_qc2_cv",
            "calibrated_retention_time_qc2",
            "retention_length_qc2",
            "N_of_scans_qc2",
            #'qc3_peptide',
            "N_of_Protein_qc_pepts",
            "N_Protein_qc_missing_values",
            "reporter_intensity_corrected_Protein_qc_ave",
            "reporter_intensity_corrected_Protein_qc_sd",
            "reporter_intensity_corrected_Protein_qc_cv",
        ]

        assert set(expected_cols).issubset(set(actual_cols)), actual_cols

    @pytest.mark.parametrize("channels", [2, 6, 11, 18])
    def test__dynamic_tmt_channel_counts(self, tmp_path, channels):
        _build_protein_groups(tmp_path, channels)

        out = maxquant_qc_protein_groups(tmp_path, protein=["QC3_BSA"])

        for idx in range(1, channels + 1):
            assert f"TMT{idx}_missing_values" in out.index

        missing_values = out["N_Protein_qc_missing_values"].split(";")
        assert len(missing_values) == channels
        assert out["N_of_Protein_qc_pepts"] == "11"

    def test__dynamic_tmt_multiple_max_intensity_rows(self, tmp_path):
        rows = [
            {
                "Potential contaminant": None,
                "Reverse": None,
                "Majority protein IDs": "QC3_BSA",
                "Only identified by site": None,
                "Sequence coverage [%]": 55.0,
                "Protein IDs": "QC3_BSA",
                "Intensity": 3000.0,
                "Peptide counts (all)": 7,
            },
            {
                "Potential contaminant": None,
                "Reverse": None,
                "Majority protein IDs": "QC3_BSA",
                "Only identified by site": None,
                "Sequence coverage [%]": 60.0,
                "Protein IDs": "QC3_BSA",
                "Intensity": 3000.0,
                "Peptide counts (all)": 9,
            },
        ]
        _build_protein_groups(tmp_path, channels=6, rows=rows)
        out = maxquant_qc_protein_groups(tmp_path, protein=["QC3_BSA"])

        assert out["N_of_Protein_qc_pepts"] in {"7", "9"}
        assert ";" not in out["N_of_Protein_qc_pepts"]

    def test__empty_peptides_file(self, tmp_path):
        _write_tsv(
            tmp_path,
            "peptides.txt",
            {
                "Potential contaminant": [],
                "Reverse": [],
                "Oxidation (M) site IDs": [],
                "Missed cleavages": [],
                "Last amino acid": [],
            },
        )
        out = maxquant_qc_peptides(tmp_path)

        assert out["N_peptides"] == 0
        assert out["N_missed_cleavages_total"] == 0
        assert out["Oxidations [%]"] == 0.0

    def test__empty_evidence_file(self, tmp_path):
        _write_tsv(
            tmp_path,
            "evidence.txt",
            {
                "Sequence": [],
                "Charge": [],
                "Intensity": [],
                "Calibrated retention time": [],
                "Retention length": [],
                "Number of scans": [],
                "Uncalibrated - Calibrated m/z [ppm]": [],
                "Uncalibrated - Calibrated m/z [Da]": [],
                "Reporter intensity corrected 1": [],
                "Reporter intensity corrected 2": [],
            },
        )
        out = maxquant_qc_evidence(tmp_path)

        assert out["qc1_peptide_charges"] == "not detected"
        assert out["N_qc1_missing_values"] == "not detected"
        assert out["reporter_intensity_corrected_qc1_cv"] == "not detected"

    def test__empty_protein_groups_file(self, tmp_path):
        _write_tsv(
            tmp_path,
            "proteinGroups.txt",
            {
                "Potential contaminant": [],
                "Reverse": [],
                "Majority protein IDs": [],
                "Only identified by site": [],
                "Sequence coverage [%]": [],
                "Protein IDs": [],
                "Intensity": [],
                "Peptide counts (all)": [],
                "Reporter intensity corrected 1": [],
                "Reporter intensity corrected 2": [],
            },
        )
        out = maxquant_qc_protein_groups(tmp_path, protein=["QC3_BSA"])

        assert out["N_protein_groups"] == 0
        assert out["TMT1_missing_values"] == 0
        assert out["TMT2_missing_values"] == 0
        assert out["Protein_qc"] == "not detected"

    def test__key_metric_regression_against_fixture(self):
        result = maxquant_qc(PATH, protein=None, pept_list=None).iloc[0]
        fixture = pd.read_csv(os.path.join(PATH, "maxquant_quality_control.csv")).iloc[0]

        assert result["N_protein_groups"] == pytest.approx(fixture["N_protein_groups"])
        assert result["N_peptides"] == pytest.approx(fixture["N_peptides"])

        fixture_parent_frac_key = (
            "Mean_parent_int_frac"
            if "Mean_parent_int_frac" in fixture.index
            else "Mean_parent_intensity_fraction"
        )
        assert result["Mean_parent_int_frac"] == pytest.approx(
            fixture[fixture_parent_frac_key]
        )
