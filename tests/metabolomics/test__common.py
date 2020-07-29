import pandas as pd

from lrg_omics.metabolomics.common import metadata_from_worklist, metadata_from_filename


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
                'MS_MODE': 'Pos'}
        expected = pd.DataFrame(data, index=[0])
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
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'