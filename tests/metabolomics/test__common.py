from lrg_omics.metabolomics.common import read_worklist, metadata_from_filename




class Test_metadata_from_filename():
    
    def test__file_with_bi_nbr():
        fn = '2020_05_11RG_HILICNeg15S_Col002_LSARP_SA001_RPT001_BI_16_0076.mzXML'
        actual = metadata_from_filename(fn)
        data = {'BI_NBR': 'BI_16_0076'} 
        expected = pd.DataFrame(data)
        assert actual.equals(expected), f'Expected: {expected}\nReceived: {actual}'
