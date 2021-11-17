#!/usr/bin/env python

from psims.transform.mzml import MzMLToMzMLb
from pathlib import Path as P
from tqdm import tqdm
import argparse
import os
import logging

def mzml2mzmlb(fn, fn_out=None, out_parent=None):
    if out_parent is None:
        out_parent = P(fn).parent
    if fn_out is None:
        fn_out = out_parent / P(fn).with_suffix('.mzMLb').name
    if fn_out.is_file():
        logging.warning(f'File exists {fn_out}')
    else:
        os.makedirs(out_parent, exist_ok=True) 
        logging.info(f'{fn} --> {fn_out}')
        MzMLToMzMLb(fn, fn_out).write()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='append')
    parser.add_argument('-o', '--output', action='append')
    parser.add_argument('-d', '--output-directory', action='append')
   
    args = parser.parse_args()

    fns = args.input
    fn_out = args.output
    out_parent = args.output_directory
    for fn in tqdm(fns):
        mzml2mzmlb(fn, fn_out, out_parent)

