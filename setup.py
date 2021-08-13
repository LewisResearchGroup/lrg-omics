#!/usr/bin/env python 

import versioneer

from setuptools import setup, find_packages


NAME = 'lrg_omics'


install_requires = []


scripts = [
    'scripts/lrg_run_maxquant.py',
    'scripts/lrg_metabolomics_metadata_from_worklist.py',
    'scripts/lrg_pd_convert.py',
    'scripts/lrg_fake_maxquant.sh',
    'scripts/lrg_get_maxquant_qc_data_from_path.py',
    'scripts/lrg_get_rawtools_qc_data_from_path.py',
    'scripts/lrg_upload_raw_file_to_qc_pipeline.py'
]

config = {
    'description': 'LRG multi-omics toolkit',
    'author': 'Soren Wacker',
    'url': 'https://github.com/soerendip',
    'download_url': f'https://github.com/soerendip/{NAME}',
    'author_email': 'swacker@ucalgary.ca',
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass(),
    'install_requires': install_requires,
    'packages': find_packages(),
    'scripts': scripts,
    'name': f'{NAME}'
}

setup(**config)
