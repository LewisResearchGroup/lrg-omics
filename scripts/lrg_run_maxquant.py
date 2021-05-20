#!/usr/bin/env python

import argparse
from os.path import isfile
from lrg_omics.proteomics.MaxQuantRunner import MaxQuantRunner


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process MaxQuant runs.')
    parser.add_argument('--raw', nargs='*', action='append', required=True,
        help='RAW files to process.')
    parser.add_argument('--fasta', 
        help='Fasta file.', required=True)
    parser.add_argument('--mqpar', required=True, 
        help='MaxQuant parameter template file (mqpar.xml).',)
    parser.add_argument('--run-dir', 
        help='Temporary directory to perform the calculation.')
    parser.add_argument('--out-dir', 
        help='Location of the final results.')
    parser.add_argument('--cold-run', action='store_true', default=False,
        help='Just simulate run and show the actions.')
    parser.add_argument('--rerun', action='store_true', default=False,
        help='Start the run even if results already exist.')
    parser.add_argument('--submit', action='store_true', default=False,
        help='Submit slurm job.')
    parser.add_argument('--batch-cmd', 
        help=('Additional commands for slum job script e.g. '
              '"source .bashrc conda activate omics;...".') )
    parser.add_argument('--maxquantcmd', required=True, 
        help='Command to start MaxQuant e.g. "mono MaxQuantCmd.exe".',)
    parser.add_argument('--dont-add-raw-name', default=True, action='store_false',
        help='Do not create sub-directory with name of raw file in output directory.')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    mq = MaxQuantRunner(fasta_file=args.fasta, 
                        mqpar_file=args.mqpar, 
                        run_dir=args.run_dir, 
                        out_dir=args.out_dir, 
                        sbatch_cmds=args.batch_cmd,
                        maxquantcmd=args.maxquantcmd)

    for raw_file in args.raw[0]:
        if isfile(raw_file):
            mq.run(raw_file, cold_run=args.cold_run, rerun=args.rerun, submit=args.submit)
        else:
            print('W (file not found):', raw_file)