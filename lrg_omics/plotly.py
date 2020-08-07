import pandas as pd 

import plotly.graph_objects as go
import plotly.offline as opy
import plotly.figure_factory as ff

import plotly.io as pio


def set_template():
    pio.templates["draft"] = go.layout.Template(
        layout=dict(font={'size': 10}),
    )

    pio.templates.default = "draft"


def plotly_heatmap(df: pd.DataFrame(), x=None, y=None, title=None, max_label_length=None):
    '''
    Creates a heatmap from pandas.DataFrame().
    '''

    df = df.copy()

    if isinstance(df.index, pd.MultiIndex):
        df.index = ['_'.join([str(i) for i in ndx]) for ndx in df.index]

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(i) for i in ndx]) for ndx in df.columns]

    if isinstance(max_label_length, int):
        df.columns = [str(i)[:max_label_length] for i in df.columns]
        df.index = [str(i)[:max_label_length] for i in df.index]

    if x is None:
        x = df.columns
    if y is None:
        y = df.index.to_list()

    fig = go.Figure(data=go.Heatmap(z=df, y=y, x=x, hoverongaps=False))

    fig.update_layout(
        title=title,
        )

    fig.update_layout(
        title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)

    return fig


def plotly_dendrogram(df: pd.DataFrame()):
    fig = ff.create_dendrogram(df, color_threshold=1.5)
    return fig


def plotly_fig_to_div(fig):
    return opy.plot(fig, auto_open=False, output_type='div')


def plotly_dendrogram(df: pd.DataFrame(), labels=None, 
                      orientation='left', color_threshold=1,
                      height=None, width=None, max_label_lenght=None):
    if labels is None:
        labels = df.index
    
    if max_label_lenght is not None:
        labels = [i[:max_label_lenght] for i in labels]
        
    if height is None:
        height = max(500, 10*len(df))
    fig = ff.create_dendrogram(df, color_threshold=color_threshold, 
                               labels=labels, orientation=orientation)
    
    fig.update_layout(width=width, height=height, font_family="Monospace")
    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True)
    
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    return fig
