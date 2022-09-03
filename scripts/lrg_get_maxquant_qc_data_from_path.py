#!/usr/bin/env python

import argparse

from lrg_omics.proteomics.tools import load_maxquant_data_from

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process MaxQuant runs.")
    parser.add_argument("--path", required=True)
    parser.add_argument("-o", '--output', required=False, default=None)
    args = parser.parse_args()

    df = load_maxquant_data_from(args.path)

    if args.output:
        df.to_csv(args.output, index=False)
    
    else:
        print(df)
