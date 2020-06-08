import versioneer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = 'lrg_omics'

config = {
    'description': 'LRG multi-omics toolkit',
    'author': 'Soren Wacker',
    'url': 'https://github.com/soerendip',
    'download_url': f'https://github.com/soerendip/{NAME}',
    'author_email': 'swacker@ucalgary.ca',
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass(),
    'install_requires': [],
    'packages': [f'{NAME}'],
    'scripts': [],
    'name': f'{NAME}'
}

setup(**config)
