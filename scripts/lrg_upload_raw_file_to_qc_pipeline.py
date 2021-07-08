#!/usr/bin/env python

import argparse

from lrg_omics.proteomics.D3OP import D3OP


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Submit raw files to proteomics QC pipeline.')

    parser.add_argument('--host', required=True, default='https://proteomics.resistancedb.org', help='Base URL of the pipeline.',)
    parser.add_argument('--uid', help='UUID of pipeline to submit the raw file to.', required=True)
    parser.add_argument('--pid', help='User UUID to use for authentification')
    parser.add_argument('--raw', nargs='*', action='append', required=True, help='RAW files to process.')
    parser.add_argument('--verbose', default=False, action='store_true')
    args = parser.parse_args()

    host = args.host
    assert ( host.startswith('https://') or host.startswith('http://') ),\
        'Host URL should start with https:// or http://'

    uid = args.uid
    pid = args.pid
    verbose = args.verbose
    raw_fns = args.raw[0]

    uploader = D3OP(host=host, uid=uid, pid=pid, verbose=verbose)

    print(raw_fns)
    
    uploader.upload_raw(raw_fns)
    
    

