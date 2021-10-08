
import os
import pytest

from glob import glob
from pathlib import Path as P

from lrg_omics.proteomics import MaxquantRunner


PATH = P('tests/data')

class TestMaxquantRunner:

    def test_missing_faa_raises_exception(self, tmpdir):
        fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
        fn_faa = PATH/'fasta'/'does-not-exist.faa'
        with pytest.raises(Exception):
            mq = MaxquantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, maxquantcmd='lrg_fake_maxquant.sh')
            del mq

    
    def test_missing_mqpar_raises_exception(self, tmpdir):
        fn_mqp = PATH/'does-not-exist.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'
        with pytest.raises(Exception):
            mq = MaxquantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, maxquantcmd='lrg_fake_maxquant.sh')
            del mq

    def test_missing_Maxquantcmd_raises_exception(self, tmpdir):
        fn_mqp = PATH/'does-not-exist.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'
        maxquantcmd = 'a-command-that-does-not-exist...'
        with pytest.raises(Exception):
            mq = MaxquantRunner(fasta_file=fn_faa, mqpar_file=fn_mqp, maxquantcmd=maxquantcmd)
            del mq

    def test_input_files_created(self, tmpdir):

        run_dir = P(tmpdir)/'run'
        out_dir = P(tmpdir)/'out'

        fn_raw = PATH/'fake'/'fake.raw'
        fn_mqp = PATH/'maxquant'/'tmt11'/'mqpar'/'mqpar.xml'
        fn_faa = PATH/'fasta'/'minimal.faa'

        mq = MaxquantRunner(fasta_file=fn_faa, 
                            mqpar_file=fn_mqp, 
                            run_dir=run_dir, 
                            out_dir=out_dir,
                            add_uuid_to_rundir=False,
                            add_raw_name_to_outdir=False,
                            maxquantcmd='lrg_fake_maxquant.sh'
                            )

        mq.run(fn_raw, run=False)

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

        mq = MaxquantRunner(fasta_file=fn_faa,
                            mqpar_file=fn_mqp, 
                            run_dir=run_dir, 
                            out_dir=out_dir,
                            add_uuid_to_rundir=False,
                            add_raw_name_to_outdir=False,
                            cleanup=False,
                            verbose=True,
                            maxquantcmd='lrg_fake_maxquant.sh'
                            )

        mq.run(fn_raw, run=True)

        files_generated = [(out_dir/'maxquant.err').is_file(), 
                           (out_dir/'maxquant.out').is_file(),
                           (out_dir/'time.txt').is_file(),
                           (run_dir/'combined').is_dir()]

        assert all(files_generated), files_generated


    def test_time_works(self, tmpdir):
        assert os.system('time') != 32512, os.system('time')
    
