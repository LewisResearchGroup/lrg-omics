
import pandas as pd


class MetabolomicsQcGui():
    def __init__(self):
        self._ms_files = []
        self._worklist = pd.DataFrame()
    
    def show(self):
        pass
    
    @property
    def ms_files(self):
        return self._ms_files
    
    @ms_files.setter
    def ms_files(filenames: list):
        self._ms_files = filenames

    @property
    def worklist(self):
        return self._worklist

    @worklist.setter
    def workist(self, worklist: pd.DataFrame):
        self._worklist = worklist
    
    def read_worklist(self, filename: str):
        worklist = pd.read_csv(filename)
        self.worklist = worklist

    def gui(self):
        pass
