import os
import pytest

from lrg_omics.proteomics import MaxquantRunner

from pathlib import Path as P
from glob import glob

PATH = P('tests/data')



def test__time(tmpdir):

    os.system('which time')
    return_values = os.system('time --version')
    print(f'`os.system` returned {return_values}')
    assert return_values == 0, '`time` is not working, you may have to install the package "time" with apt or conda'


def test__missing_faa_raises_exception(tmpdir):

    fn_raw = PATH/'fake'/'fake.raw'
    fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
    fn_faa = PATH/'fasta'/'minimal.faa'
    run_dir = P(tmpdir)/'run'
    out_dir = P(tmpdir)/'out'
    cmd = f'lrg_run_maxquant.py --fasta {fn_faa} --raw {fn_raw} --mqpar {fn_mqp} --run-dir {run_dir} --out-dir {out_dir}  --maxquantcmd lrg_fake_maxquant.sh --verbose --add-raw-name-to-outdir --add-uuid-to-rundir'
    
    print( cmd )

    return_value = os.system(cmd)
    
    assert return_value == 0, f'Could not run: {cmd}'

    files_generated = [(out_dir/'maxquant.err').is_file(), 
                       (out_dir/'maxquant.out').is_file(),
                       (out_dir/'time.txt').is_file(),
                       (run_dir/'combined').is_dir()]

    assert all(files_generated), files_generated

