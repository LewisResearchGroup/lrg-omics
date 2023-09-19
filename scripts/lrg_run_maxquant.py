#!/usr/bin/env python

import argparse
from os.path import isfile
from lrg_omics.proteomics import MaxquantRunner


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process MaxQuant runs.")
    parser.add_argument(
        "--raw", nargs="*", action="append", required=True, help="RAW files to process."
    )
    parser.add_argument("--fasta", help="Fasta file.", required=True)
    parser.add_argument(
        "--mqpar",
        required=True,
        help="MaxQuant parameter template file (mqpar.xml).",
    )
    parser.add_argument(
        "--run-dir", help="Temporary directory to perform the calculation."
    )
    parser.add_argument("--out-dir", help="Location of the final results.")
    parser.add_argument(
        "--cold-run",
        action="store_true",
        default=False,
        help="Just simulate run and show the actions.",
    )
    parser.add_argument(
        "--rerun",
        action="store_true",
        default=False,
        help="Start the run even if results already exist.",
    )
    parser.add_argument(
        "--submit", action="store_true", default=False, help="Submit slurm job."
    )
    parser.add_argument(
        "--batch-cmd",
        help=(
            "Additional commands for slum job script e.g. "
            '"source .bashrc conda activate omics;...".'
        ),
    )
    parser.add_argument(
        "--maxquantcmd",
        required=True,
        help='Command to start MaxQuant e.g. "mono MaxQuantCmd.exe".',
    )
    parser.add_argument(
        "--add-raw-name-to-outdir",
        default=True,
        action="store_false",
        help="Do not add subdirectory raw file name to run directory.",
    )
    parser.add_argument(
        "--add-uuid-to-rundir",
        default=True,
        action="store_false",
        help="Do not add uuid to run directory.",
    )
    parser.add_argument(
        "--cleanup",
        default=False,
        action="store_true",
        help="Remove run directory after running MaxQuant",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--time", default='5:00:00')
    
    args = parser.parse_args()

    mq = MaxquantRunner(
        fasta_file=args.fasta,
        mqpar_file=args.mqpar,
        run_dir=args.run_dir,
        out_dir=args.out_dir,
        sbatch_cmds=args.batch_cmd,
        maxquantcmd=args.maxquantcmd,
        verbose=args.verbose,
        cleanup=args.cleanup,
        add_raw_name_to_outdir=args.add_raw_name_to_outdir,
        add_uuid_to_rundir=args.add_uuid_to_rundir,
        time=args.time
    )

    for raw_file in args.raw[0]:
        if isfile(raw_file):
            mq.run(
                raw_file,
                cold_run=args.cold_run,
                rerun=args.rerun,
                submit=args.submit,
                run=True,
            )
        else:
            print("W (file not found):", raw_file)
