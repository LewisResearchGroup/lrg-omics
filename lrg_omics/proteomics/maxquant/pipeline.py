# lrg_omics.proteomics.pipelines.maxquant
import os
import lrg_omics

from os.path import isfile, basename, join, abspath, dirname
from datetime import date
from pathlib import Path as P
from ...common import maybe_make_dir_and_chdir, maybe_create_symlink

FAKEPATH = abspath("tests/data/maxquant/tmt11/txt")


def run_maxquant(
    raw,
    fasta,
    mqpar,
    pipename,
    force=False,
    submit=False,
    run_root=None,
    raw_root=None,
    fasta_root=None,
    mqpar_root=None,
    run_path=None,
    maxquantbin=None,
    fake=False,
    execute=True,
):
    """
    Uses a combination of a raw-file, fasta-file and mqpar-template to
    create folder structure, commands and batch files to start
    MaxQuant jobs.
    ====
    Args:
        raw: str or PosixPath
            - absolute path to a RAW file
        fasta: str or PosixPath
            - absolute path to a FASTA file (protein library)
        mqpar_temp: str or PosixPath
            - absolute path to mqpar template file
        pipename: str, default is the name of the pipeline
        force: bool, default False
            - whether or not to start run when folders are
              already present
        submit: bool, default False
            - whether or not to submit the generated batch file to
              the queue system (supported SLURM)
    """

    if maxquantbin is None:
        maxquantbin = os.getenv("MAXQUANTBIN")
        assert isfile(maxquantbin)

    if raw_root is None:
        raw_root = dirname(raw)
    if fasta_root is None:
        fasta_root = dirname(fasta)
    if mqpar_root is None:
        mqpar_root = dirname(mqpar)

    if run_path is None:
        run_path = get_run_path(
            raw=raw,
            fasta=fasta,
            mqpar=mqpar,
            run_root=run_root,
            raw_root=raw_root,
            fasta_root=fasta_root,
            mqpar_root=mqpar_root,
        )

    if os.path.isdir(join(run_path, "combined")) and not force:
        return []

    maybe_make_dir_and_chdir(run_path)
    maybe_create_symlink(raw, basename(raw))

    create_mqpar(
        mqpar_temp=mqpar,
        raw=str(run_path / P(basename(raw))),
        fasta=fasta,
        label=pipename,
    )

    fn_meta = join(run_path, "meta.json")
    write_meta_json(
        raw=raw,
        fasta=fasta,
        mqpar=mqpar,
        pipename=pipename,
        maxquantbin=maxquantbin,
        filename=fn_meta,
    )
    assert isfile(fn_meta)

    cmd = gen_maxquant_cmd(run_path, maxquantbin)

    if fake:
        cmd = f"cd {run_path}; mkdir combined; cp -r {FAKEPATH} combined"

    with open("commands.txt", "w") as file:
        file.write("\n\n{}\n\n".format(cmd))

    gen_sbatch(commands=[cmd], jobname=run_path, submit=submit)

    if execute:
        os.system(cmd)

    return [cmd]


def gen_maxquant_cmd(run_path, maxquantbin):
    mqpar_cmd = f"(mono {maxquantbin} mqpar.xml && touch DONE) 1>maxquant_out.log 2>maxquant_error.log"
    cmd = "cd {};\n({}; \n) > run.log".format(run_path, mqpar_cmd)
    return cmd


def get_run_path(raw, fasta, mqpar, run_root, raw_root, fasta_root, mqpar_root):
    """
    Returns P(RUNROOT/RAW/FASTA/MQPAR/) where
    RUNROOT is the root directory of the pipeline
    FASTA the basename of the fasta file to use and
    MQPAR the basename of the mqpar template file to use.
    Sub-directories relative to the root folders are
    included in the generated paths.
    """
    name = "{}{}/{}/{}".format(
        run_root,
        str(raw).replace(str(raw_root), "").split(".")[0],
        str(fasta).replace(str(fasta_root), "").split(".")[0],
        str(mqpar).replace(str(mqpar_root), "").split(".")[0],
    )
    return P(name)


def create_mqpar(mqpar_temp, raw, fasta, label, outfilename="mqpar.xml"):
    with open(mqpar_temp, "r") as file:
        string = (
            file.read()
            .replace("__RAW__", str(raw))
            .replace("__FASTA__", str(fasta))
            .replace("__LABEL__", str(label))
        )
    with open(outfilename, "w") as file:
        file.write(string)
    assert os.path.isfile(outfilename)


def write_meta_json(raw, fasta, mqpar, pipename, maxquantbin, filename="meta.json"):
    today = str(date.today())
    json = f"""{{
    "Date": "{today}",
    "LRG_omics version": "{lrg_omics.__version__}",
    "PIPENAME": "{pipename}",
    "MAXQUANTBIN": "{maxquantbin}",
    "RAW_file": "{raw}",
    "FASTA_file": "{fasta}",
    "MQPAR_TEMP_file": "{mqpar}"\n}}
    """.strip()
    with open(filename, "w") as file:
        file.write(json + "\n")


def gen_sbatch(commands, jobname, submit=False, fn="run.sbatch"):
    cmds_txt = "\n\n".join(commands)
    txt = f"""#!/bin/bash
#SBATCH --time=100:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1 
#SBATCH --mem=10000
#SBATCH -J {jobname}

. /home/swacker/.bashrc
conda activate py3
which mono

{cmds_txt}
"""
    with open("run.sbatch", "w") as file:
        file.write(txt)
    if submit:
        os.system("sbatch run.sbatch")
