import pandas as pd


class Plate():
    def __init__(self):
        self._rows = []
        self._columns = []
        self._data = pd.DataFrame()


class Plate96Well(Plate):
    def __init__(self):
        self._rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self._columns = list(range(1, 12))
        self._data = pd.DataFrame(index=self._rows, columns=self._columns)
        
