import plotly.express as px
from ....plotly import set_template
import plotly.graph_objects as go

colors = ['rgba(100, 0, 0, 0.5)', 
          'rgba(0, 100, 0, 0.5)',
          'rgba(0, 0, 100, 0.5)']

set_template()

def lines_plot(rawtools_matrix, cols, colors=colors, title=None, **kwargs):
    fig = go.Figure()
    for i, col in enumerate( cols ):
        fig.add_trace(
            go.Scatter(
                x=rawtools_matrix.index,
                y=rawtools_matrix[col], 
                name=col,
                mode='lines',
                line=dict(width=0.5, color=colors[i]),  
                **kwargs),
               )
    fig.update_layout(legend_title_text='', 
                      title=title)
    fig.update_xaxes(title_text=rawtools_matrix.index.name)
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


def histograms(rawtools_matrix, cols=['ParentIonMass'], 
               title=None, colors=colors):
    fig = go.Figure()
    if len(cols) == 1:
        fig.update_layout(title=cols[0])
        fig.update_layout(showlegend=False)
    for i, col in enumerate( cols ) :
        fig.add_trace(
                go.Histogram(
                        x=rawtools_matrix[col], 
                        visible = 'legendonly' if i>0 else None, 
                        name=col, 
                        marker_color=colors[i]
                        ))
    fig.update_layout(legend_title_text='')
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    fig.update_layout(title=title)
    return fig