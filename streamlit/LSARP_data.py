import streamlit as st

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

import altair as alt


from lrg_omics.LSARP.tools import get_shipments, get_broad_plates,  get_proteomics_plates,\
    get_metabolomics_plates, get_growth_protein, get_growth_monitor

st.beta_set_page_config(layout='wide')
st.sidebar.title('LSARP Metadata')

show = st.sidebar.selectbox('Show', ['APL Shipments', 'Broad', 'Metabolomics', 'Proteomics', 'Growth'])

if show == 'APL Shipments':
    st.title('APL Shipments')

    shipments = get_shipments().fillna('')
    gprs = shipments.groupby('PLATE_ID')

    _plates = list( gprs.groups.keys() )
    show_element = st.selectbox('Show', ['Layout', 'Table', 'Statistics'])
    
    plates = st.multiselect('Plate', _plates + ['All plates'] )

    if plates is not None:
        if 'All plates' in plates: plates = _plates
        for plate in plates:

            st.write(plate)
            _plate = gprs.get_group(plate).fillna('')

            if show_element == 'Layout':
                crosstab = pd.crosstab(_plate.PLATE_COL, _plate.PLATE_ROW, 
                        _plate.ISOLATE_NBR, aggfunc=sum)

                st.dataframe(crosstab) 

            if show_element == 'Table':
                st.dataframe(_plate)

            st.markdown('---')

    if show_element == 'Statistics':

        print(shipments.columns)
        _data = shipments['DATE shipped'].value_counts().to_frame().reset_index()
        _data.columns = ['DATE shipped', '# Isolates']

        chart = alt.Chart(_data).mark_bar()\
                    .encode(y='# Isolates', x='DATE shipped')

        st.altair_chart(chart, use_container_width=True)

        _data = shipments.ORGANISM.value_counts().to_frame().reset_index()
        _data.columns = ['ORGANISM', 'Counts']

        chart = alt.Chart(_data).mark_bar()\
                    .encode(x='ORGANISM', y='Counts')

        st.altair_chart(chart, use_container_width=True)



if show == 'Broad':
    st.title('Broad DNA plates')

    broad_plates = get_broad_plates()
    grps = broad_plates.groupby('Filename')

    _plates = list( grps.groups.keys() )
    plates = st.multiselect('Plate', _plates+['All plates'])

    if plates is not None:
        if 'All plates' in plates: plates = _plates
        for plate in plates:
            st.header(plate)
            _data = grps.get_group(plate)
            st.dataframe(_data)

            _bi_counts = _data.iloc[:,3].value_counts()
            _broad_id_counts = _data.iloc[:,1].value_counts()

            if _bi_counts.max() > 1:
                st.dataframe(_bi_counts[_bi_counts>1].to_frame()\
                    .style.highlight_max(axis=0, color='red'))
            
            if _broad_id_counts.max() > 1:
                st.write(_broad_id_counts[_broad_id_counts>1].to_frame()\
                    .style.highlight_max(axis=0, color='red'))
            st.markdown('---')



if show == 'Proteomics':
    st.title('Proteomics plates')

    proteomics_plates = get_proteomics_plates()
    #grps = proteomics_plates

    st.dataframe(proteomics_plates)


if show == 'Metabolomics':
    st.title('Metabolomics plates')

    metabolomics_plates = get_metabolomics_plates()
    grps = metabolomics_plates.groupby('PLATE_ID')

    show_element = st.selectbox('Show', ['Layout', 'Table', 'Statistics'])

    _plates = list( grps.groups.keys() )
    plates = st.multiselect('Plates', _plates+['All plates'])

    ms_mode = st.selectbox('MS-Mode', ['Positive', 'Negative'])

    if ms_mode == 'Positive': ms_mode = 'pos'
    if ms_mode == 'Negative': ms_mode = 'neg'

    if show_element == 'Layout':
        if 'All plates' in plates: plates = _plates
        for plate in plates:
            st.header(plate)
            tmp = grps.get_group(plate)[['PLATE_ROW', 'PLATE_COL', 'BI_NBR']].fillna('').drop_duplicates()
            crosstab = pd.crosstab(tmp['PLATE_ROW'], tmp['PLATE_COL'], tmp['BI_NBR'], aggfunc=sum)
            st.dataframe(crosstab)
            st.markdown('---')

    elif show_element == 'Table':
        
        if plates is not None:
            if 'All plates' in plates: plates = _plates
            if ms_mode == 'Positive': ms_mode = 'pos'
            if ms_mode == 'Negative': ms_mode = 'neg'
            for plate in plates:
                st.header(plate)
                tmp = grps.get_group(plate)
                tmp = tmp[tmp.MS_MODE.str.lower() == ms_mode]
                st.dataframe(tmp)
                st.markdown('---')

if show == 'Growth':
    st.title('Isolate growth data')

    show_element = st.selectbox('Show', ['Layout', 'Table', 'Statistics'])

    growth_type = st.selectbox('Growth Type', ['Protein', 'Monitor'])

    if growth_type == 'Protein':
        growth_data = get_growth_protein()
    elif growth_type == 'Monitor':
        growth_data = get_growth_monitor()
        timepoint = st.selectbox('Time', growth_data.TIME.drop_duplicates().values )
        growth_data = growth_data[growth_data.TIME == timepoint]

    grps = growth_data.groupby('PLATE_ID')

    od_min = growth_data.OD.min()
    od_max = growth_data.OD.max()

    _plates = list( grps.groups.keys() )
    plates = st.multiselect('Plates', _plates+['All plates'])

    if plates is not None:
        if 'All plates' in plates: plates = _plates
        for plate in plates:
            _data = grps.get_group(plate)
            if len(_data) == 0:
                continue
            st.header(plate)

            if show_element == 'Table':
                st.dataframe(_data)

            if show_element == 'Layout':
                crosstab = pd.crosstab(_data['PLATE_ROW'], _data['PLATE_COL'], _data['OD'], aggfunc=np.mean)
                cm = sns.light_palette("green", as_cmap=True)
                st.dataframe(crosstab.style.background_gradient(cmap=cm, low=od_min, high=od_max))
            
            st.markdown('---')

