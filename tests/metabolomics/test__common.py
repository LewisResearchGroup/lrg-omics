import pandas as pd

from lrg_omics.metabolomics.common import read_worklist, metadata_from_filename


class Test_metadata_from_filename():
    def test__file_with_bi_nbr(self):
        fn = '2020_05_11RG_HILICNeg15S_Col002_LSARP_SA001_RPT001_BI_16_0076.mzXML'
        actual = metadata_from_filename(fn)
        data = {'BI_NBR': 'BI_16_0076', 
                'DATE': '2020-05-11', 
                'RPT': 1, 
                'PLATE_ID': 'SA001',
                'IS_STANDARD': False,
                'MS_MODE': 'Neg'}
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
