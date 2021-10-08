import os
import pandas as pd
import datetime

from lrg_omics.metabolomics.common import metadata_from_filename
from lrg_omics import LRG_TEST_DATA



def test__file_with_bi_nbr():
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
    assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'


def test__file_with_standard():
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


def test__file_with_qc01_sample():
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


def test__file_with_qc02_sample():
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


def test__file_with_SA_pool_sample():
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


def test__file_with_MH_pool_sample():
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


def test__file_with_blank_sample():
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

'''
def test__read_plate():
    path = os.path.join(LRG_TEST_DATA, 'metabolomics_sample_0')

    worklist = 'tests/data/metabolomics/example-worklist.csv'
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
    assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
'''

