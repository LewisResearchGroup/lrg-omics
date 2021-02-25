#!/usr/bin/env python

import argparse
import pandas as pd
from pathlib import Path as P


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read ThermoFisher worklist and extract data.')
    parser.add_argument('-f', dest='fn_inp', help='Input ThermoFisher workist file (csv format)')
    parser.add_argument('-o', dest='fn_out', help='Output file name')
    parser.add_argument('--hdf-key', default='Dataset')
    parser.add_argument('--sheet-name')
    parser.add_argument('--sep')

    args = parser.parse_args()

    fn_inp = P(args.fn_inp)
    fn_out = P(args.fn_out)

    assert fn_inp != fn_out

    sep = args.sep

    if fn_inp.suffix.lower() == '.csv':
        df = pd.read_csv(fn_inp, sep=args.sep or ',')
    elif fn_inp.suffix.lower() == '.tsv':
        df = pd.read_csv(fn_inp, sep=args.sep or '\t')
    elif fn_inp.suffix.lower() in ['.xlsx']:
        df = pd.read_excel(fn_inp, sheet_name=args.sheet_name)
    elif fn_inp.suffix.lower() in ['.parquet']:
        df = pd.read_parquet(fn_inp)
    elif fn_inp.suffix.lower() in ['.hdf', '.hdf5']:
        df = pd.read_hdf(fn_inp, key=args.hdf_key)

    if fn_out.suffix.lower() == '.parquet':
        df.to_parquet(fn_out)
    elif fn_out.suffix.lower() ==  '.csv':
        df.to_csv(fn_out)
    elif fn_out.suffix.lower() == '.tsv':
        df.to_csv(fn_out, sep='\t')
    elif fn_out.suffix.lower() == '.xlsx':
        df.to_excel(fn_out, sheet_name=args.sheet_name)
    elif fn_out.suffix.lower() in ['.hdf', '.hdf5']:
        df.to_hdf(fn_out, key=args.hdf_key)


