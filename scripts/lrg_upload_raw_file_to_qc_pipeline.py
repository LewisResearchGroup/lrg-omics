import argparse
import requests

class ProteomicsRawUploadToQC():
    def __init__(self, url, pipeline, user, verbose=True):
        self.url = url
        self.pipeline = pipeline
        self.user = user
        self.verbose = verbose
    
    def submit(self, raw_fn):
        url = self.url
        pipeline = self.pipeline
        user = self.user
        with open(raw_fn, 'rb') as file:
            files = {'orig_file': file}
            #headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            data = {'pipeline': pipeline, 'user': user}
            if self.verbose: print(data, raw_fn)
            r = requests.post(url, files=files, data=data)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Submit raw files to proteomics QC pipeline.')

    parser.add_argument('--raw', nargs='*', action='append', required=True, help='RAW files to process.')
    parser.add_argument('--pipeline', help='UUID of pipeline to submit the raw file to.', required=True)
    parser.add_argument('--host', required=True, default='https://proteomics.resistancedb.org', help='Base URL of the pipeline.',)
    parser.add_argument('--user', help='User UUID to use for authentification')
    args = parser.parse_args()


    host = args.host
    #assert ( host.startswith('https://') or host.startswith('http://') ),\
    #    'Host URL should start with https:// or http://'

    url = f'{host}/api/upload-raw'
    user = args.user
    pipeline = args.pipeline

    uploader = ProteomicsRawUploadToQC(url=url, user=user, pipeline=pipeline)

    for raw_fn in args.raw[0]:
        print(raw_fn)
        uploader.submit(raw_fn)

