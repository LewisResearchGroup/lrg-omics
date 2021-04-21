import os
import pandas as pd
import datetime
import numpy as np

from lrg_omics.metabolomics.common import metadata_from_worklist, metadata_from_filename, read_plate
from lrg_omics.metabolomics.common import classic_lstsqr, linear_range_finder
from lrg_omics import LRG_TEST_DATA

class Test_metadata_from_filename():
    def test__file_with_bi_nbr(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_BI_16_0028.mzXML')
        actual = metadata_from_filename(fn)
        data = {
                'MS_FILE': '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_BI_16_0028.mzXML',
                'BI_NBR': 'BI_16_0028', 
                'DATE': datetime.datetime.strptime('2020_05_11', '%Y_%m_%d'), 
                'RPT': 1, 
                'PLATE_ID': 'SA001',
                'SAMPLE_TYPE': 'BI',
                'STD_CONC': None,
                'MS_MODE': 'Pos',
                'COL':'Col001'
        }
        expected = pd.DataFrame(data, index=[0])
#         for col in expected.columns:
#             print(col + ': ')
#             print(actual[col] == expected[col])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'

    def test__file_with_standard(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_Standard-5000nm.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE': '2020_05_11RG_HILICPos15S_Col001_LSARP_SA001_RPT001_Standard-5000nm.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_05_11', '%Y_%m_%d'), 
                'RPT': 1, 
                'PLATE_ID': 'SA001',
                'SAMPLE_TYPE': 'ST',
                'STD_CONC': 5000.,
                'MS_MODE': 'Pos',
                'COL':'Col001'}
        expected = pd.DataFrame(data, index=[0])
#         print(expected.STD_CONC)
        print(actual.STD_CONC)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_qc01_sample(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC01_SA008.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE': '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC01_SA008.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_04_20', '%Y_%m_%d'), 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'QC',
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'COL': 'Col002'}
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
        
    def test__file_with_qc02_sample(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC02_SA008.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_QC02_SA008.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_04_20', '%Y_%m_%d'), 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'QC',
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'COL':'Col002'}
        expected = pd.DataFrame(data, index=[0])
        for col in expected.columns:
            print(col + ': ')
            print(actual[col] == expected[col])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_SA_pool_sample(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_04_20RG_HILICPos15S_Col001_LSARP_SA008_SA-Pool-4.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICPos15S_Col001_LSARP_SA008_SA-Pool-4.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_04_20', '%Y_%m_%d'), 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'PO-SA',
                'STD_CONC': None,
                'MS_MODE': 'Pos',
                'COL':'Col001'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_MH_pool_sample(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_MH-Pool-1.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_MH-Pool-1.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_04_20', '%Y_%m_%d'), 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'PO-MH',
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'COL':'Col002'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__file_with_Blank_sample(self):
        fn = os.path.join(LRG_TEST_DATA, 
                         '2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_Blank2.mzXML')
        actual = metadata_from_filename(fn)
        data = {'MS_FILE':'2020_04_20RG_HILICNeg15S_Col002_LSARP_SA008_Blank2.mzXML',
                'BI_NBR': None, 
                'DATE': datetime.datetime.strptime('2020_04_20', '%Y_%m_%d'), 
                'RPT': 0, 
                'PLATE_ID': 'SA008',
                'SAMPLE_TYPE': 'BL',
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'COL': 'Col002'}
        expected = pd.DataFrame(data, index=[0])
#         print(actual.BI_NBR == expected.BI_NBR)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    def test__read_plate(self):
        path = os.path.join(LRG_TEST_DATA, 'metabolomics_sample_0')

        worklist = 'LSARP-Full-May2020-Worklist.csv'
        actual = read_plate(path, worklist)
        names = ['2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0227.mzXML',
                 '2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0253.mzXML',
                 '2020_05_13RG_HILICNeg15S_Col002_LSARP_SA002_RPT001_BI_16_0371.mzXML']
        well_row = ['A','A','A']
        well_col = [2,3,4]
        
        bi_nbrs = ['BI_16_0227', 'BI_16_0253', 'BI_16_0371']
        dates = [datetime.datetime.strptime('2020_05_13', '%Y_%m_%d'),
                 datetime.datetime.strptime('2020_05_13', '%Y_%m_%d'),
                 datetime.datetime.strptime('2020_05_13', '%Y_%m_%d')]
        rpt = [1,1,1]
        sample_type = ['BI','BI','BI']
        plate_id = ['SA002','SA002','SA002']
        std_conc = [None,None,None]
        ms_mode = ['Neg','Neg','Neg']
        cols = ['Col002', 'Col002', 'Col002']
        data = {
                'MS_FILE': names,
                'BI_NBR': bi_nbrs, 
                'DATE': dates, 
                'RPT': rpt, 
                'PLATE_ID': plate_id,
                'SAMPLE_TYPE': sample_type,
                'STD_CONC': None,
                'MS_MODE': 'Neg',
                'COL': cols,
                'WELL_ROW': well_row,
                'WELL_COL': well_col
               }
        expected = pd.DataFrame(data)
        expected = expected.sort_values(by=['MS_FILE'])
#         print(expected.WELL_ROW == actual.WELL_ROW)
#         print(expected.WELL_COL == actual.WELL_COL)
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    
    def test__linear_range_finder_(self):
        x = np.array([ 0.,  2.,  3.,  3.,  4.,  6.,  6.,  7.,  8.,  9., 10., 12., 13.,
       13., 14., 15., 17., 18., 18., 19., 20., 21., 22., 24., 24., 25.,
       26., 27., 29., 30., 30., 31., 32., 33., 35., 35., 36., 38., 39.,
       40., 40., 42., 43., 43., 44., 45., 46., 47., 48., 50.])
        
        y = np.array([ 0.,  1.14142136,  0.4       ,  0.73484692,  2.13137085,
        2.58113883,  2.07846097,  3.61916017,  4.2       ,  3.81837662,
        4.47213595,  5.15945734,  6.87877538,  6.62872537,  8.40810367,
        8.21583836,  9.0509668 ,  9.91261822, 10.8       , 12.71238661,
       13.64911064, 14.60955547, 15.59314908, 16.59935896, 17.62768775,
       17.67766953, 19.74886663, 19.84086692, 20.95328137, 22.08574201,
       24.23790008, 25.40942441, 25.6       , 27.80932674, 28.03711825,
       30.28310093, 31.54701295, 31.82860349, 33.12763197, 34.44386738,
       36.77708764, 37.12707907, 38.49363584, 40.87655953, 42.27565869,
       42.69074841, 45.12165001, 45.56819066, 48.03020306, 49.50752519])
        
        expected = [12.0, 35.0]
        x_c , _ = linear_range_finder(x, y, 0.75)
        actual = [min(x_c), max(x_c)]
        assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'