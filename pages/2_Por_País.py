from utils import ( load_data,
                    preprocess_s6,
                    yearsList,
                    filter_by_year,
                    area,
                    line,
                    preprocess_s7,
                    choropleth_map,
                    heatmap
                    )

import streamlit as st
from streamlit.logger import get_logger
import warnings

import plotly.express as px
px.defaults.template = "seaborn"

warnings.filterwarnings('ignore')

def pais() -> None:
    years_list = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    option = st.multiselect('Selecciona el año', years_list, placeholder="Selecciona un año")

    file_path = 'https://github.com/CJ7MO/EDA_coffee/raw/refs/heads/main/exportaciones_coffee.xlsx'
    s6 = load_data(file_path, 5)
    s6_melted, s6_filtered = preprocess_s6(s6)
    available_years = [col for col in option if col in s6.columns]
    if available_years:
        selected_columns = ['PAISES'] + available_years
        s6_filtered = s6_filtered.loc[:, selected_columns]
    else:
        s6_filtered = s6_filtered


    s7 = load_data(file_path, 6)
    s7 = preprocess_s7(s7)
    s7 = filter_by_year(s7, option)


    features = ['Sacos de 70kg', 'Sacos de 60kg', 'Total en Kilogramos', 'Valor en USD']
    feature = st.sidebar.selectbox('Selecciona la variable', features)
    fig3 = choropleth_map(s7, feature)
    st.plotly_chart(fig3, use_container_width=True)

    s6_melted = filter_by_year(s6_melted, option)
    col1, col2 = st.columns(2)
    with col1:
        fig4 = heatmap(s6_filtered)
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        fig6 = line(s6_melted)
        st.plotly_chart(fig6, use_container_width=True)

st.set_page_config(page_title="CoffeeViz", page_icon=":coffee:", layout="wide") 
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

pais()