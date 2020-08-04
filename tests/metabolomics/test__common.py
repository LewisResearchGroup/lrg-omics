import os
import pandas as pd

from lrg_omics.metabolomics.common import metadata_from_worklist, metadata_from_filename, read_plate
from lrg_omics import LRG_TEST_DATA

class Test_metadata_from_filename():
    def test__file_with_bi_nbr(self):
        fn = 'example-01/2020_05_11RG_SA001_RPT001/2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_BI_16_0028.mzXML'
        actual = metadata_from_filename(fn)
        data = {
                'MS_FILE': '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_BI_16_0028.mzXML',
                'BI_NBR': 'BI_16_0028', 
                'DATE': '2020-05-11', 
                'RPT': 1, 
                'PLATE_ID': 'SA001',
                'SAMPLE_TYPE': 'BI',
                'STD_CONC': None,
                'MS_MODE': 'Pos'
        }
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'

    def test__file_with_standard(self):
        fn = 'example-01/2020_05_11RG_SA001_RPT001/2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_Standard-5000nm.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE': '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_Standard-5000nm.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-05-11', 
                'RPT': 1, 
                'PLATE_ID': 'SA001',
                'SAMPLE_TYPE': 'ST',
                'STD_CONC': 5000.,
                'MS_MODE': 'Pos'}
        expected = pd.DataFrame(data, index=[0])
#         print(expected.STD_CONC)
        print(actual.STD_CONC)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_qc01_sample(self):
        fn = '/media/luis/WORK/metabolomics/SA_data/data/f1/2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC01_SA008.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE': '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC01_SA008.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-04-20', 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'QC',
                'STD_CONC': None,
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
        
    def test__file_with_qc02_sample(self):
        fn = '/media/luis/WORK/metabolomics/SA_data/data/f1/2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC02_SA008.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC02_SA008.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-04-20', 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'QC',
                'STD_CONC': None,
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_SA_pool_sample(self):
        fn = '/media/luis/WORK/metabolomics/SA_data/data/f1/2020_04_20RG_HILICPos15S_Col001_LSARP_SA008_SA-Pool-4.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICPos15S_Col001_LSARP_SA008_SA-Pool-4.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-04-20', 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'PO-SA',
                'STD_CONC': None,
                'MS_MODE': 'Pos'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_MH_pool_sample(self):
        fn = '/media/luis/WORK/metabolomics/SA_data/data/f1/2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_MH-Pool-1.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_MH-Pool-1.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-04-20', 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'PO-MH',
                'STD_CONC': None,
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_Blank_sample(self):
        fn = '/media/luis/WORK/metabolomics/SA_data/data/f1/2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_Blank2.mzXML'
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_Blank2.mzXML',
                'BI_NBR': None, 
                'DATE': '2020-04-20', 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'BL',
                'STD_CONC': None,
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__read_plate(self):
        path = '/media/luis/WORK/metabolomics/QC_pipeline/lrg_omics/sample_files'

        worklist = 'LSARP-Full-May2020-Worklist.csv'
        actual = read_plate(path, worklist)
        names = ['2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0227.mzXML',
                 '2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0253.mzXML',
                 '2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0371.mzXML']
        well_row = ['A','A','A']
        well_col = [2,3,4]
        
        bi_nbrs = ['BI_16_0227', 'BI_16_0253', 'BI_16_0371']
        dates = ['2020-05-13','2020-05-13','2020-05-13']
        rpt = [1,1,1]
        sample_type = ['BI','BI','BI']
        plate_id = ['SA002','SA002','SA002']
        std_conc = [None,None,None]
        ms_mode = ['Neg','Neg','Neg']
        file_size = [22931245, 22927568, 22896208]
        data = {
                'MS_FILE': names,
                'BI_NBR': bi_nbrs, 
                'DATE': dates, 
                'RPT': rpt, 
                'PLATE_ID': plate_id,
                'SAMPLE_TYPE': sample_type,
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'FILE_SIZE': file_size,
                'WELL_ROW': well_row,
                'WELL_COL': well_col
               }
        expected = pd.DataFrame(data)
        expected = expected.sort_values(by=['MS_FILE'])
        print(expected.WELL_ROW == actual.WELL_ROW)
        print(expected.WELL_COL == actual.WELL_COL)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'