import versioneer

from setuptools import setup, find_packages

NAME = 'lrg_omics'

install_requires = [
    'pandas',
    'streamlit',
    'matplotlib',
    'scikit-learn',
]

config = {
    'description': 'LRG multi-omics toolkit',
    'author': 'Soren Wacker',
    'url': 'https://github.com/soerendip',
    'download_url': f'https://github.com/soerendip/{NAME}',
    'author_email': 'swacker@ucalgary.ca',
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass(),
    'install_requires': ['pandas'],
    'packages': [find_packages()],
    'scripts': [],
    'name': f'{NAME}'
}

setup(**config)
