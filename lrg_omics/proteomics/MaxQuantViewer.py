from .MaxQuantResult import MaxQuantResult
from .viz.plotly.maxquant import plot_spectrum

class MaxQuantViewer(MaxQuantResult):
    def plot_spectra(self, protein_id=None):
        spectra = self.get_spectra(protein_id)
        fig = plot_spectrum(spectra)
        return fig