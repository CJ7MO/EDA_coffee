import streamlit as st
import pandas as pd
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

@st.cache_data
def load_data(url: str, sheet_name: int) -> pd.DataFrame:
    df = pd.read_excel(url, sheet_name=sheet_name)
    return df

@st.cache_data
def preprocess_s1(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={'MES': 'fecha', 'Total Exportaciones': 'total_export'})
    df['total_kg'] = df['total_export'] * 60
    df = df.loc[df['fecha']>'2016-12-31']
    df['año'] = pd.to_datetime(df['fecha']).dt.year
    df['mes'] = pd.to_datetime(df['fecha']).dt.strftime('%m')
    return df

@st.cache_data
def preprocess_s10(df: pd.DataFrame) -> pd.DataFrame:
    df['fecha'] = s10['Año'].astype(str) + '-' + s10['Mes'].astype(str) + '-01'
    df = df.rename(columns={'Año':'año'})
    return df

@st.cache_data
def filter_by_year(df: pd.DataFrame, selected_years: list) -> pd.DataFrame:
    if selected_years:
        return df[df['año'].isin(selected_years)]
    return df

@st.cache_resource()
def create_treemap(df: pd.DataFrame):
    fig = px.treemap(
        df, 
        path=['País destino', 'Nombre exportador'], 
        values='Valor Factura (USD)*', 
        color='Nombre exportador', 
        color_discrete_sequence=px.colors.qualitative.Bold,
        width=1750,
        height=600
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(
        autosize=True,
        title="Treemap de Exportaciones por País y Exportador",
        title_x=0.4,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    return fig

file_path = 'https://github.com/CJ7MO/EDA_coffee/raw/refs/heads/main/exportaciones_coffee.xlsx'

s1 = load_data(file_path, 0)
s1 = preprocess_s1(s1)

years = s1['año'].unique().tolist()
option = st.multiselect('Selecciona el año', years, placeholder="Selecciona un año")

s1 = filter_by_year(s1, option)

s10 = load_data(file_path, 9)
s10 = preprocess_s10(s10)
s10 = filter_by_year(s10, option)

treemap_fig = create_treemap(s10)
st.plotly_chart(treemap_fig)

col1, col2 = st.columns(2)
with col1:
    fig1 = px.line(s1, x="fecha", y="total_kg")
    fig1.update_layout(xaxis_title="Fecha", yaxis_title="Total de Kgs", title="Exportaciones de CAFÉ en Colombia", width=800, height=400)
    st.plotly_chart(fig1)

with col2:
    fig2 = px.line(s1, 
                x='mes', 
                y='total_kg', 
                color='año',  # Diferente color por año
                labels={'mes_dia': 'Mes', 'total_kg': 'Total KG'}, 
                title='Total KG por Año',
                width=800, height=400)

    st.plotly_chart(fig2)