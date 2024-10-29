import streamlit as st
from streamlit.logger import get_logger
import warnings

import plotly.express as px
px.defaults.template = "seaborn"

warnings.filterwarnings('ignore')
LOGGER = get_logger(__name__)

def run():
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
    st.markdown("""
    ---
    Desarrollado bajo la dirección del **Ph.D. Oscar Mayorga**, Ingeniero Industrial, este tablero busca ofrecer una perspectiva integral sobre las exportaciones de café colombiano. 
    A través de una serie de visualizaciones interactivas y análisis detallados, los usuarios pueden examinar los datos de exportación desde múltiples dimensiones: **consolidado general**, 
    **país de destino**, **tipo de café**, y **puerto de embarque**. La plataforma emplea gráficos de línea, mapas de árbol, coropletas y heatmaps, facilitando la identificación de patrones 
    y tendencias clave en el comercio internacional del café.

    ## Índice de Visualizaciones

    ### 1. Consolidado de Datos
    - **Tree Map**: Visualización de la distribución general de exportaciones.
    - **Gráficos de Línea**: Evolución temporal de las exportaciones en kilogramos y valores en USD.

    ### 2. Por País
    - **Mapa de Coropletas**: Representación geográfica de las exportaciones de café por país de destino.
    - **Heatmap**: Análisis de intensidad de exportación por país.
    - **Gráficos de Línea**: Tendencias de exportación a lo largo del tiempo para cada país.

    ### 3. Por Tipo de Café
    - Visualización de las exportaciones desglosadas por tipos de café exportados.

    ### 4. Por Puerto de Embarque
    - Análisis de volúmenes de exportación segmentado por los principales puertos de embarque en Colombia.

    ---
    Cada visualización ha sido diseñada para facilitar el análisis de las exportaciones de café, promoviendo la toma de decisiones informadas y apoyando el crecimiento de la industria cafetera en el mercado global.
    """)

if __name__ == "__main__":
    run()




