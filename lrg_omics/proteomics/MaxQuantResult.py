from pyteomics import mgf


class MaxQuantResult():
    def __init__(self, path=None, mgf_file=None):
        if path is not None:
            self.read(path)
        else:
            self._evidence = pd.DataFrame()
            self._msms =  pd.DataFrame()
            self._proteins =  pd.DataFrame()
            self._peptides = pd.DataFrame()
        if mgf_file is not None:
            self.add_spectra(mgf_file)
        else:
            self._spectra = None
            
    def read(self, path):
        self._evidence = pd.read_csv(f'{path}/evidence.txt', sep='\t')
        self._msms = pd.read_csv(f'{path}/msmsScans.txt', sep='\t', index_col='Scan index')
        self._proteins = pd.read_csv(f'{path}/proteinGroups.txt', sep='\t', index_col='id')
        self._peptides = pd.read_csv(f'{path}/peptides.txt', sep='\t')      
        
    def add_spectra(self, mgf_file):
        self._spectra = mgf.read(mgf_file)
    
    def get_spectrum(self, index):
        if self._spectra is None:
            return None
        df = spectrum_to_df( self._spectra.get_by_index(index) )
        df['Scan index'] = index
        return df
    
    def get_proteins(self, ids=None, regex=None, seq=None, cols=None):
        if cols is None:
            cols = []
        df = self._proteins
        if ids is not None:
            df = df.loc[ids]
        if regex is not None:
            df = df[df['Protein IDs'].str.contains(regex)]
        if seq is not None:
            df = df[df.Sequence.str.contains(seq)]
        return df
    
    def get_msms_scan_index(self, protein_id=None, column='Best MS/MS'):
        if protein_id is not None:
            df = self._proteins
            scan_index = [ int(i) for i in df.loc[protein_id][column].split(';')]
            return scan_index       
    
    def get_spectra(self, protein_id=None):
        if self._spectra is None:
            return None
        if protein_id is not None:
            scan_index = self.get_msms_scan_index(protein_id=protein_id)
            spectra = []
            for ndx in scan_index:
                spectrum = self.get_spectrum(ndx)
                spectra.append(spectrum)
            return pd.concat(spectra)
    

def spectrum_to_df(spectrum):
    rt_entry_to_float_minutes = lambda x: float(x)/60
    df = pd.DataFrame()
    df['mz_array'] = spectrum['m/z array']
    df['intensity'] = spectrum['intensity array']
    df['spectrum'] = spectrum['params']['title']
    df['raw_file'] = spectrum['params']['rawfile']
    df['retention_time[min]'] = rt_entry_to_float_minutes(spectrum['params']['rtinseconds'])
    return df