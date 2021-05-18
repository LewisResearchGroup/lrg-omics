
import os
import pytest

from lrg_omics.proteomics.MaxQuantRunner import MaxQuantRunner

from pathlib import Path as P
from glob import glob

PATH = P('tests/data')

class TestMaxQuantRunner:

    def test_missing_faa_raises_exception(self, tmpdir):
        fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
        fn_faa = PATH/'fasta'/'does-not-exist.faa'
        with pytest.raises(Exception):
            mq = MaxQuantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp)

    
    def test_missing_mqpar_raises_exception(self, tmpdir):
        fn_mqp = PATH/'does-not-exist.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'
        with pytest.raises(Exception):
            mq = MaxQuantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp)


    def test_missing_maxquantcmd_raises_exception(self, tmpdir):
        fn_mqp = PATH/'does-not-exist.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'
        maxquantcmd = 'a-command-that-does-not-exist...'
        with pytest.raises(Exception):
            mq = MaxQuantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, maxquantcmd=maxquantcmd)


    def test_input_files_created(self, tmpdir):

        run_dir = P(tmpdir)/'run'
        out_dir = P(tmpdir)/'out'

        fn_raw = PATH/'fake'/'fake.raw'
        fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'

        mq = MaxQuantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, 
                            run_dir=run_dir, output_dir=out_dir)

        mq.run(fn_raw, run=False, add_uuid=False)

        print( glob(str(run_dir/'*')) ) 

        files_generated = [(run_dir/'run.sbatch').is_file(), 
                           (run_dir/'fake.raw').is_file(),
                           (run_dir/'mqpar.xml').is_file()]

        assert all(files_generated), files_generated



    def test_log_files_created(self, tmpdir):

        run_dir = P(tmpdir)/'run'
        out_dir = P(tmpdir)/'out'

        fn_raw = PATH/'fake'/'fake.raw'
        fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'

        mq = MaxQuantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, 
                            run_dir=run_dir, output_dir=out_dir)

        mq.run(fn_raw, run=True, add_uuid=False)

        files_generated = [(run_dir/'maxquant.err').is_file(), 
                           (run_dir/'maxquant.out').is_file(),
                           (run_dir/'time.txt').is_file(),
                           (run_dir/'combined').is_dir()]

        assert all(files_generated), files_generated





    def test_time_works(self, tmpdir):
        assert os.system('time') != 32512, os.system('time')
    
