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
    
    def test__read_tmt11_peptides_example0(self):
        fn = PATH/'maxquant'/'tmt11'/'example-0'/'peptides.txt'
        reader = MaxquantReader()
        df = reader.read(fn)
        print(df)
        assert isinstance(df, pd.DataFrame), type(df)

    def test__read_tmt11_summary_example0(self):
        fn = PATH/'maxquant'/'tmt11'/'example-0'/'summary.txt'
        reader = MaxquantReader()
        df = reader.read(fn)
        print(df)
        assert isinstance(df, pd.DataFrame), type(df)