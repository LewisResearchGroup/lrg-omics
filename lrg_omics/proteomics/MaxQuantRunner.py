import os
from os.path import isfile, basename, join, abspath, dirname, isdir
from shutil import rmtree
from uuid import uuid1

from .common import maybe_create_symlink


class MaxQuantRunnner():
    def __init__(self, fasta_file, mqpar_file, maxquantcmd='maxquant', 
                 run_dir=None, target_dir=None, add_raw_name_to_dir=True,
                 sbatch_cmds=''):
        self._fasta = abspath(fasta_file)
        self._mqpar = abspath(mqpar_file)
        self._mqcmd = maxquantcmd
        self._run_dir = run_dir
        self._tar_dir = target_dir
        self._add_raw_name_to_dir = add_raw_name_to_dir
        self._sbatch_cmds = [i.strip() for i in sbatch_cmds.split(';')]
        
    def run(self, raw_file, cold_run=False, rerun=False, submit=False, run=False):
        raw_file = abspath( raw_file)
        if raw_file.lower().endswith('.raw'):
            raw_label = basename(raw_file[:-4])
        else :
            raw_label = basename(raw_file)   
        if self._run_dir is None:
            run_dir = join( abspath( dirname(raw_file), 'run' ) )
        else:
            run_dir = self._run_dir
        if self._tar_dir is None:
            tar_dir = join( abspath( dirname(raw_file) ), 'result')
        else:
            tar_dir = self._tar_dir
        
        if self._add_raw_name_to_dir: run_dir = join(run_dir, raw_label )
        if self._add_raw_name_to_dir: tar_dir = join(tar_dir, raw_label )

        run_id = str(uuid1())
        run_id_short = run_id.split('-')[0]
        run_dir = join(run_dir, run_id)           
            
        if isdir(run_dir):
            if not rerun:
                return None
            else:
                rmtree(run_dir)
        
        if isdir(tar_dir):
            if not rerun:
                return None
            else:
                rmtree(tar_dir)
        
        run_raw_ref = join(run_dir, basename(raw_file))
        run_mqpar = join(run_dir, basename(self._mqpar))
        run_sbatch = join(run_dir, 'run.sbatch')
        
        cmds = [
            f'cd {run_dir}',
            f'{self._mqcmd} {run_mqpar} 1>maxquant.out 2>maxquant.err',
            f'mv {run_dir}/combined/txt/* {tar_dir}', 
            f'rm -r {run_dir}']
                        
        if not cold_run:
            os.makedirs(run_dir, exist_ok=True)
            os.makedirs(tar_dir, exist_ok=True)            
            maybe_create_symlink( raw_file, run_raw_ref )
        else:
            print(f'Create run directory: {run_dir}')
            print(f'Create target directory: {tar_dir}')
            print(f'Create link:', raw_file, run_raw_ref )
            print(f'Commands:')
            for cmd in cmds:
                print( cmd )
            print('sbatch file:')
        
        create_mqpar(self._mqpar, run_raw_ref, self._fasta, raw_label, fn=run_mqpar, cold_run=cold_run)
        
        gen_sbatch_file(self._sbatch_cmds + cmds, run_id_short+run_raw_ref, 
                        fn=run_sbatch, cold_run=cold_run, submit=submit)
        
        cmds = '; '.join( cmds )
        
        if run:
            print(run_id)
            os.system(cmds)
        return cmds


def gen_sbatch_file(commands, jobname, submit=False, fn='run.sbatch', cold_run=False):
    cmds_txt = '\n\n'.join(commands)
    txt = f"""#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --mem=5000
#SBATCH -J {jobname}

{cmds_txt}
"""
    if not cold_run:
        with open(fn, 'w') as file:
            file.write(txt)
        if submit:
            os.system(f'sbatch {fn}')
    else: print(txt)

    
def create_mqpar(mqpar_temp, raw, fasta, label, fn='mqpar.xml', cold_run=False):
    with open(mqpar_temp, 'r') as file:
        string = file.read()\
                     .replace('__RAW__', str(raw))\
                     .replace('__FASTA__', str(fasta))\
                     .replace('__LABEL__', str(label))
    if not cold_run:
        with open(fn, 'w') as file:
            file.write(string)
    else:
        print(f'Create {fn}:\n', string)

