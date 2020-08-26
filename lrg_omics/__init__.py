import os

from . import metabolomics
from . import proteomics

from ._version import get_versions
__version__ = get_versions()['version']

del get_versions

def lrg_home_path():
    lrg_home = os.path.dirname(__file__)
    lrg_home = os.path.join( lrg_home , '..')
    lrg_home = os.path.abspath(lrg_home)
    return lrg_home

LRG_HOME = lrg_home_path()
LRG_TEST_DATA = os.getenv('LRG_TEST_DATA', os.path.join(LRG_HOME, 'lrg_omics_test_data'))

