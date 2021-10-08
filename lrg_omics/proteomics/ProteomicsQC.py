import pandas as pd

import requests
import json
import logging

from tqdm import tqdm



class ProteomicsQC:
    '''
    Python API to interact with the Proteomics QC pipeline.
    
    -------
    Example:
    
    d3op = D3OP(host='https://proteomics.resistancedb.org', 
                uid='your-user-uuid',     # Optional, required for upload of RAW files
                pid='your-pipeline-uuid'  # Optional, required for upload of RAW files
                )
                
    d3op.get_projects()
    
    d3op.get_pipelines(project='lsarp')
    
    d3op.get_qc_data(project='lsarp', pipeline='staphylococcus-aureus-tmt11', data_range=100)
    
    d3op.upload_raw(fns=[list-of-filenames])  # Requires uid and pid
    
    '''
    
    def __init__(self, 
                 host='https://localhost:8000', 
                 pid=None, 
                 uid=None, 
                 verbose=False):
        
        self._host = host
        self._pipeline_uuid = pid
        self._user_uuid = uid
        self._verbose = verbose
        self._projects = None
        self._pipeline = None
        self._qc_data  = None
    
    def get_projects(self):
        url = f'{self._host}/api/projects'
        r = requests.post(url).json()
        self.projects = pd.DataFrame(r)
        return self.projects
        
    def get_pipelines(self, project_slug):
        url = f'{self._host}/api/mq/pipelines'
        headers = {'Content-type': 'application/json'}
        data = json.dumps( dict(project=project_slug) )
        r = requests.post(url, data=data, headers=headers).json()
        return pd.DataFrame(r)

    def get_qc_data(self, project_slug, pipeline_slug, columns=None, data_range=30):
        url = f'{self._host}/api/mq/qc-data'
        headers = {'Content-type': 'application/json'}
        #if columns is None: columns = ['Index', 'Date', 'RawFile',  'DateAcquired', 
        #                               'Use Downstream','Flagged', 'N_protein_groups']

        data_dict =dict(project=project_slug, pipeline=pipeline_slug, data_range=data_range)
        if columns is not None: data_dict['columns'] = columns

        data = json.dumps(data_dict)
        r = requests.post(url, data=data, headers=headers).json()
        df = pd.DataFrame(r)
        df['DateAcquired'] = pd.to_datetime( df['DateAcquired'] )
        return df
    
    def upload_raw(self, fns):
        if isinstance(fns, str): fns = [fns]
        url = f'{self._host}/api/upload/raw'
        pipeline = self._pipeline_uuid
        user = self._user_uuid
        
        if (pipeline is None) or (user is None):
            logging.error('Please, initiate D3PO with user_uuid '\
                          'and pipeline_uuid to submit RAW files.')

        for fn in tqdm(fns):
            with open(fn, 'rb') as file:
                files = {'orig_file': file}
                data = {'pipeline': pipeline, 'user': user}
                if self._verbose: print(f'Uploading {fn}...', end='')
                r = requests.post(url, files=files, data=data)
                status_code = r.status_code
                if self._verbose:
                    if status_code == 201: print(' success')
                    else: print(' failed ([{status_code}])')
            
            
    def download_maxquant_data(self, project_slug, pipeline_slug, filename):
        url = f'{self._host}/api/download'
        print(url)
        
        
