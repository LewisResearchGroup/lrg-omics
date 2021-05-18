import os
import shutil 
from os.path import isfile, basename, join, abspath, dirname, isdir
from uuid import uuid1

from pathlib import Path as P
import logging

from .common import maybe_create_symlink


class MaxQuantRunner():
    def __init__(self, fasta_file, mqpar_file, maxquantcmd='maxquant', 
                 run_dir=None, output_dir=None, add_raw_name_to_dir=False,
                 sbatch_cmds=None, clean_up=False, verbose=False):

        self._fasta = abspath(fasta_file)
        self._mqpar = abspath(mqpar_file)
        self._mqcmd = maxquantcmd
        self._run_dir = run_dir
        self._tgt_dir = output_dir
        self._add_raw_name_to_dir = add_raw_name_to_dir
        if sbatch_cmds is None: sbatch_cmds = ''
        self._sbatch_cmds = [i.strip() for i in sbatch_cmds.split(';')]
        self._clean_up = clean_up
        self._verbose = verbose

        assert isfile( self._fasta ), self._fasta
        assert isfile( self._mqpar ), self._mqpar
        
        assert os.system( maxquantcmd ) != 32512, f'Command not found: {maxquantcmd}'


    def run(self, raw_file, cold_run=False, rerun=False, submit=False, run=True, 
            add_uuid=True):
        raw_file = abspath( raw_file)
        if raw_file.lower().endswith('.raw'):
            raw_label = basename(raw_file[:-4])
        else :
            raw_label = basename(raw_file)   
        if self._run_dir is None:
            run_dir = abspath( join( os.getcwd(), 'run' ) )
        else:
            run_dir = abspath( self._run_dir )
        if self._tgt_dir is None:
            tgt_dir = abspath( join( os.getcwd(), 'out' ) ) 
        else:
            tgt_dir = abspath( self._tgt_dir ) 
        
        if self._add_raw_name_to_dir: run_dir = join(run_dir, raw_label )
        if self._add_raw_name_to_dir: tgt_dir = join(tgt_dir, raw_label )

        run_id = f'{raw_label}'
        
        if add_uuid: 
            str(uuid1())[:8]+f'-{run_id}'
            run_dir = join(run_dir, run_id)

        if isdir(run_dir):
            if not rerun:
                logging.warning(f'Run directory exists ({run_dir}).')
                return None
            else:
                shutil.rmtree(run_dir)
        
        if isdir(tgt_dir):
            if not rerun:
                logging.warning(f'Output directory exists ({tgt_dir}) omitting raw file: {raw_file}.')
                return None
            else:
                shutil.rmtree(tgt_dir)
        
        run_raw_ref = join(run_dir, basename(raw_file))
        run_mqpar = join(run_dir, basename(self._mqpar))
        run_sbatch = join(run_dir, 'run.sbatch')
        
        cmds = [
            f'cd {run_dir}',
            f'/usr/bin/time -o {run_dir}/time.txt -f "%E" {self._mqcmd} {run_mqpar} 1>maxquant.out 2>maxquant.err',
            f'mv time.txt {run_dir}/combined/txt/',
            f'mv {run_dir}/combined/txt/* {tgt_dir}', 
            ]

        if self._clean_up:
            cmds.append(f'rm -r {run_dir}')

        if not cold_run:
            os.makedirs(run_dir, exist_ok=True)
            os.makedirs(tgt_dir, exist_ok=True)            
            maybe_create_symlink( raw_file, run_raw_ref )

        if self._verbose or cold_run:
            print(f'Create run directory: {run_dir}')
            print(f'Create target directory: {tgt_dir}')
            print(f'Create link:', raw_file, run_raw_ref )
            print(f'Commands:')
            for cmd in cmds:
                print( cmd )
            print('sbatch file:')
        
        create_mqpar(self._mqpar, run_raw_ref, self._fasta, raw_label, fn=run_mqpar, cold_run=cold_run)
        
        gen_sbatch_file(self._sbatch_cmds + cmds, jobname=run_id, 
                        fn=run_sbatch, cold_run=cold_run, submit=submit)
        
        cmds = '; '.join( cmds )
        
        if run:
            print(run_id, cmds)
            os.system(cmds)
            if self._clean_up: self.clean_up()

        return cmds

    def clean_up(self):
        shutil.rmtree( self._run_dir )


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

