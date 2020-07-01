import plotly.express as px
from .template import *




colors = ['rgba(80, 80, 200, 0.5)', 
          'rgba(80, 150, 150, 0.5)',
          'rgba(150, 150, 80, 0.5)']


def lines_plot(rawtools_matrix, cols, colors=colors, title=None):
    fig = go.Figure()
    for i, col in enumerate( cols ):
        fig.add_trace(
            go.Scatter(
                x=rawtools_matrix.index,
                y=rawtools_matrix[col], 
                fill=None, name=col,
                mode='lines',
    fig.update_layout(legend_title_text='', title=title)
    return fig
                                 
                                 
def filltime(rawtools_matrix, title=None):
    cols = ['Ms1FillTime', 'Ms2FillTime', 'DutyCycle(s)']
    return lines_plot(rawtools_matrix, cols=cols, title=title)

def median_intensity(rawtools_matrix, title=None):
    cols = ['PeakParentScanIntensity', 
            'Ms1MedianIntensity', 
            'Ms2MedianIntensity']
    if title is None:
        title = 'Intensity'
    fig = lines_plot(rawtools_matrix, cols=cols, title=title)
    fig.update_layout(yaxis_type="log")
    return fig 

def histograms(rawtools_matrix, cols=['ParentIonMass'], title=None):
    fig = px.histogram(rawtools_matrix[cols[0]])
    if len(cols) == 1:
        fig.update_layout(title=cols[0])
        fig.update_layout(showlegend=False)
    for col in cols[1:]:
        fig.add_trace(
                go.Histogram(
                        x=rawtools_matrix[col], 
                        visible = 'legendonly', 
                        name=col,
                        title=title))
    fig.update_layout(legend_title_text='')
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    return fig