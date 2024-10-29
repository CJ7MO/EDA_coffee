from utils import (load_data, 
                   preprocess_s10,
                   yearsList,
                   filter_by_year,
                   create_treemap,
                   create_line_fig1,
                   create_line_fig2,                  
                   )


import streamlit as st
from streamlit.logger import get_logger
import warnings

import plotly.express as px
px.defaults.template = "seaborn"

warnings.filterwarnings('ignore')


def tree_line() -> None:
    
    file_path = 'https://github.com/CJ7MO/EDA_coffee/raw/refs/heads/main/exportaciones_coffee.xlsx'
    df = load_data(file_path, 9)
    df = preprocess_s10(df)
    years_list = yearsList(df)

    col1, col2 = st.columns(2)
    with col1:
        option = st.multiselect('Selecciona el año', years_list)

    with col2:
        features = ['Sacos de 70kg', 'Sacos de 60kg', 'Total en Kilogramos', 'Valor en USD']
        feature = st.selectbox('Selecciona la variable', features)

    df = filter_by_year(df, option)
    fig = create_treemap(df, feature)
    show_tree_map = st.sidebar.checkbox("Mostrar Tree Map")

    if show_tree_map:
        fig = create_treemap(df, feature)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = create_line_fig1(df, feature)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = create_line_fig2(df, feature)
        st.plotly_chart(fig2, use_container_width=True)

st.set_page_config(page_title="Consolidado", page_icon=":coffee:", layout="wide")
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)
html_title = """
<style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
</style>
<center><h1 class="title-test">📉📈 Dashboard del Café en Colombia 📊☕</h1></center>
"""
st.markdown(html_title, unsafe_allow_html=True)



tree_line()
