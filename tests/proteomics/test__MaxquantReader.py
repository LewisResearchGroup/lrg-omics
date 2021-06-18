import pandas as pd
from pathlib import Path as P

from lrg_omics.proteomics import MaxquantReader



PATH = P('tests/data')

class TestMaxquantReader:
    def test__read_tmt11_protein_groups_example0(self):
        fn = PATH/'maxquant'/'tmt11'/'example-0'/'proteinGroups.txt'
        reader = MaxquantReader()
        df = reader.read(fn)
        print(df)
        assert isinstance(df, pd.DataFrame)

    def test__read_tmt11_protein_groups_example1(self):
        fn = PATH/'maxquant'/'tmt11'/'example-1'/'proteinGroups.txt'
        reader = MaxquantReader()
        df = reader.read(fn)
        print(df)
        assert isinstance(df, pd.DataFrame)
    '''


    def test__read_tmt11_protein_groups_example0_(self):
        fn = PATH/'maxquant'/'tmt11'/'example-0'/'proteinGroups.txt'
        reader = MaxquantReader()
        df = reader.read_protein_groups(fn)
        print(df)
        assert isinstance(df, pd.DataFrame)


    def test__read_tmt11_protein_groups_example1_(self):
        fn = PATH/'maxquant'/'tmt11'/'example-1'/'proteinGroups.txt'
        reader = MaxquantReader()
        df = reader.read_protein_groups(fn)
        df.to_csv('~/test_out.csv')
        print(df)
        for c in df.columns: print(c)
        assert isinstance(df, pd.DataFrame)
        assert False
    '''