from utils import (load_data, 
                   preprocess_s10,
                   preprocess_s6,
                   years_list,
                   filter_by_year,
                   create_treemap,
                   create_line_fig1,
                   create_line_fig2,
                   preprocess_s7,
                   choropleth_map,
                   heatmap,
                   area,
                   line 
                   )

import streamlit as st
import warnings

import plotly.express as px
px.defaults.template = "seaborn"

warnings.filterwarnings('ignore')

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



file_path = 'https://github.com/CJ7MO/EDA_coffee/raw/refs/heads/main/exportaciones_coffee.xlsx'
df = load_data(file_path, 9)
df = preprocess_s10(df)
years_list = years_list(df)

col1, col2 = st.columns(2)
with col1:
    option = st.multiselect('Selecciona el año', years_list, placeholder="Selecciona un año")

with col2:
    features = ['Sacos de 70kg', 'Sacos de 60kg', 'Total en Kilogramos', 'Valor en USD']
    feature = st.selectbox('Selecciona la variable', features)

df = filter_by_year(df, option)
fig = create_treemap(df, feature)
st.plotly_chart(fig)

col1, col2 = st.columns(2)
with col1:
    fig1 = create_line_fig1(df, feature)
    st.plotly_chart(fig1)

with col2:
    fig2 = create_line_fig2(df, feature)
    st.plotly_chart(fig2)

s6 = load_data(file_path, 5)
s6_melted, s6_filtered = preprocess_s6(s6)
available_years = [col for col in option if col in s6.columns]
if available_years:
    selected_columns = ['PAISES'] + available_years
    s6_filtered = s6_filtered.loc[:, selected_columns]
else:
    s6_filtered = s6_filtered

s6_melted = filter_by_year(s6_melted, option)
col1, col2 = st.columns(2)
with col1:
    fig5 = area(s6_melted)
    st.plotly_chart(fig5)

with col2:
    fig6 = line(s6_melted)
    st.plotly_chart(fig6)

s7 = load_data(file_path, 6)
s7 = preprocess_s7(s7)
s7 = filter_by_year(s7, option)

col1, col2 = st.columns(2)
with col1:
    fig3 = choropleth_map(s7, feature)
    st.plotly_chart(fig3)

with col2:
    fig4 = heatmap(s6_filtered)
    st.plotly_chart(fig4)

