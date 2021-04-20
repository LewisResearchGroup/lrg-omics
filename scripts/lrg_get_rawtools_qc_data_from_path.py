#!/usr/bin/env python

import argparse

from lrg_omics.proteomics.tools import load_rawtools_data_from

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process MaxQuant runs.')
    parser.add_argument('--path', required=True)
    args = parser.parse_args()

    df = load_rawtools_data_from( args.path )
    
    print(df.shape)
    print(df)