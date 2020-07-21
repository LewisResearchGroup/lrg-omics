
import pandas as pd


class MetabolomicsQcGui():
    def __init__(self):
        self._ms_files = []
        self._worklist = pd.DataFrame()
    
    def show():
        pass
    
    @property
    def ms_files:
        return self._ms_files
    
    @ms_files.setter
    def ms_files(filenames: list):
        self._ms_files = filenames

    @property
    def worklist:
        return self._worklist

    @worklist.setter
    def workist(self, worklist: pd.DataFrame):
        self._worklist = worklist
    
    def read_worklist(self, filename):
        worklist = pd.read_csv(filename)
        self.worklist = worklist

    def gui(self):
        
