import pandas as pd

import requests
import json

class D3OP:
    '''
    Python API to interact with the Proteomics QC pipeline.
    
    -------
    Example:
    
    d3op = D3OP(host='https://proteomics.resistancedb.org', 
                uid='your-user-uuid',  # Optional
                pid='your-pipeline-uuid'  # Optional
                )
                
    d3op.get_projects()
    d3op.get_pipelines(project='lsarp')
    d3op.get_qc_data(project='lsarp', pipeline='staphylococcus-aureus-tmt11', data_range=100)
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
        
    def get_pipelines(self, project):
        url = f'{self._host}/api/mq/pipelines'
        headers = {'Content-type': 'application/json'}
        data = json.dumps( dict(project=project) )
        r = requests.post(url, data=data, headers=headers).json()
        return pd.DataFrame(r)

    def get_qc_data(self, project, pipeline, columns=None, data_range=None):
        url = f'{self._host}/api/mq/qc-data'
        headers = {'Content-type': 'application/json'}
        if columns is None: columns = ['Index', 'Date', 'RawFile',  'DateAcquired', 
                                       'Use Downstream','Flagged', 'N_protein_groups']
        data = json.dumps( dict(project=project, pipeline=pipeline, 
                                columns=columns, data_range=data_range) )
        r = requests.post(url, data=data, headers=headers).json()
        df = pd.DataFrame(r)
        df['DateAcquired'] = pd.to_datetime( df['DateAcquired'] )
        return df
    
    def submit(self, raw_fn):
        url = f'{self.host}/api/upload/raw'
        pipeline = self.pipeline
        user = self.user
        with open(raw_fn, 'rb') as file:
            files = {'orig_file': file}
            data = {'pipeline': pipeline, 'user': user}
            if self.verbose: print(data, raw_fn)
            r = requests.post(url, files=files, data=data)        
