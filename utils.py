import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

pd.options.display.float_format = '{:,.2f}'.format

@st.cache_data  
def load_data(url: str, sheet_name: int) -> pd.DataFrame:
    df = pd.read_excel(url, sheet_name=sheet_name)
    return df

@st.cache_data
def preprocess_s10(df: pd.DataFrame) -> pd.DataFrame:
    df['total_kg'] = df['Sacos de 70 kg. equivalente real Exportados'] * 70
    df['fecha'] = df['Año'].astype(str) + '-' + df['Mes'].astype(str) + '-01'
    df.rename(columns={'Sacos de 70 kg. equivalente real Exportados': 'Sacos de 70kg',
                   'Sacos de 60 Kg. Exportados': 'Sacos de 60kg','Valor Factura (USD)*': 'Valor en USD',
                   'Año': 'año', 'total_kg': 'Total en Kilogramos'}, inplace=True)
    return df

@st.cache_data
def preprocess_s7(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby(['Año','País de destino', 'Tipo de café'])[['Valor provisional de la Exportación (USD) *', 'Sacos de 70 kg. equivalente real Exportados','Sacos de 60 Kg. Exportados' ]].sum().reset_index()
    df = df.sort_values(by=['Valor provisional de la Exportación (USD) *', 'Tipo de café'], ascending=False).reset_index(drop=True)
    df['total_kg'] = df['Sacos de 70 kg. equivalente real Exportados'] * 70
    df = df.rename(columns={'Sacos de 70 kg. equivalente real Exportados': 'Sacos de 70kg', 
                                            'Sacos de 60 Kg. Exportados': 'Sacos de 60kg', 
                                            'Valor provisional de la Exportación (USD) *': 'Valor en USD',
                                            'Año': 'año', 'total_kg': 'Total en Kilogramos'})
    
    country_replacements = {
    'EE.UU.': 'United States',
    'Japón': 'Japan',
    'Canadá': 'Canada',
    'Bélgica': 'Belgium',
    'Alemania': 'Germany',
    'Corea del Sur': 'South Korea',
    'China': 'China',
    'España': 'Spain',
    'Italia': 'Italy',
    'Reino Unido': 'United Kingdom',
    'Francia': 'France',
    'Finlandia': 'Finland',
    'México': 'Mexico',
    'Australia': 'Australia',
    'Países Bajos': 'Netherlands',
    'Malasia': 'Malaysia',
    'Noruega': 'Norway',
    'Ecuador': 'Ecuador',
    'Israel': 'Israel',
    'Suecia': 'Sweden',
    'Taiwan': 'Taiwan',
    'Federación Rusa': 'Russia',
    'Chile': 'Chile',
    'Arabia Saudí': 'Saudi Arabia',
    'Colombia': 'Colombia',
    'Grecia': 'Greece',
    'Turquía': 'Turkey',
    'Guatemala': 'Guatemala',
    'Perú': 'Peru',
    'E.A.U.': 'United Arab Emirates',
    'Rumanía': 'Romania',
    'Polonia': 'Poland',
    'Vietnam': 'Vietnam',
    'Rep.Dominicana': 'Dominican Republic',
    'Nueva Zelanda': 'New Zealand',
    'Jordania': 'Jordan',
    'Eslovenia': 'Slovenia',
    'Argentina': 'Argentina',
    'Portugal': 'Portugal',
    'Dinamarca': 'Denmark',
    'Ucrania': 'Ukraine',
    'Egipto': 'Egypt',
    'Irlanda': 'Ireland',
    'Singapur': 'Singapore',
    'El Salvador': 'El Salvador',
    'Sudáfrica': 'South Africa',
    'Panamá': 'Panama',
    'Marruecos': 'Morocco',
    'Hong Kong': 'Hong Kong',
    'Letonia': 'Latvia',
    'Líbano': 'Lebanon',
    'Siria': 'Syria',
    'Chipre': 'Cyprus',
    'Suiza': 'Switzerland',
    'Estonia': 'Estonia',
    'Venezuela': 'Venezuela',
    'Kuwait': 'Kuwait',
    'Jamaica': 'Jamaica',
    'Libia': 'Libya',
    'Costa Rica': 'Costa Rica',
    'Filipinas': 'Philippines',
    'TrinidadyTobago': 'Trinidad and Tobago',
    'Paraguay': 'Paraguay',
    'Uruguay': 'Uruguay',
    'Puerto Rico': 'Puerto Rico',
    'Brasil': 'Brazil',
    'Lituania': 'Lithuania',
    'Antillas Neerl': 'Netherlands Antilles',
    'Bolivia': 'Bolivia',
    'Georgia': 'Georgia',
    'Islandia': 'Iceland',
    'Argelia': 'Algeria',
    'Aruba': 'Aruba',
    'Omán': 'Oman',
    'Irán': 'Iran',
    'Curaçao': 'Curaçao',
    'Indonesia': 'Indonesia',
    'Túnez': 'Tunisia',
    'Surinam': 'Suriname',
    'Tailandia': 'Thailand',
    'India': 'India',
    'Macao': 'Macau',
    'Dominica': 'Dominica',
    'Honduras': 'Honduras',
    'Níger': 'Niger',
    'Antigua/Barbuda': 'Antigua and Barbuda',
    'Reunión': 'Réunion',
    'Qatar': 'Qatar',
    'Bulgaria': 'Bulgaria',
    'Belice': 'Belize',
    'Nicaragua': 'Nicaragua',
    'Guyana': 'Guyana',
    'Albania': 'Albania',
    'República Congo': 'Congo (Brazzaville)',
    'Austria': 'Austria',
    'República Checa': 'Czech Republic',
    'Antillas hol.': 'Netherlands Antilles',
    'Somalia': 'Somalia',
    'Croacia': 'Croatia',
    'Camboya': 'Cambodia',
    'Iraq': 'Iraq',
    'Cuba': 'Cuba',
    'Islas Caimán': 'Cayman Islands',
    'Barbados': 'Barbados',
    'Bahráin': 'Bahrain',
    'Kenia': 'Kenya',
    'Eslovaquia': 'Slovakia',
    'Santa Lucía': 'Saint Lucia',
    'Polinesia fran.': 'French Polynesia',
    'Mauricio (Isl.)': 'Mauritius',
    'Granada': 'Grenada',
    'Kazajistán': 'Kazakhstan',
    'Pakistán': 'Pakistan',
    'Sint Maarten': 'Sint Maarten',
    'San Vicente': 'Saint Vincent and the Grenadines',
    'Mongolia': 'Mongolia',
    'Costa de Marfil': 'Ivory Coast',
    'Is.Vírgenes USA': 'U.S. Virgin Islands',
    'Malta': 'Malta',
    'Benín': 'Benin',
    'S.Cris.& Nieves': 'Saint Kitts and Nevis',
    'Nigeria': 'Nigeria'}

    # Aplicar el diccionario de reemplazo en tu DataFrame
    df['País de destino'] = df['País de destino'].replace(country_replacements)
    
    return df

@st.cache_data
def preprocess_s6(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[:, ['PAISES', 2017, 2018, 2019, 2020, 2021, 2022, 2023]]
    df = df.rename(columns={'Año':'año'})
    df_filtered = df[~df['PAISES'].str.contains('TOTAL')].reset_index(drop=True)
    df_melted = df_filtered.melt(id_vars='PAISES', var_name='año', value_name='Valor')
    return df_melted, df_filtered

@st.cache_data
def years_list(df: pd.DataFrame) -> list:
    years = df['año'].unique()
    years.sort()
    return years

@st.cache_data
def filter_by_year(df: pd.DataFrame, selected_years: list) -> pd.DataFrame:
    if selected_years:
        return df[df['año'].isin(selected_years)]
    return df

@st.cache_resource()
def create_treemap(df: pd.DataFrame, feature: str):
    df[feature] = pd.to_numeric(df[feature], errors='coerce')
    
    df_clean = df.dropna(subset=['País destino', 'Nombre exportador', feature])
    
    fig = px.treemap(
        df_clean, 
        path=['País destino', 'Nombre exportador'], 
        values=feature, 
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

@st.cache_resource()
def create_line_fig1(df: pd.DataFrame, feature:str):
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    df_grouped = df.groupby('fecha')[feature].sum().reset_index()

    df_grouped.sort_values(by='fecha', inplace=True)

    fig1 = px.line(df_grouped, x="fecha", y=feature)
    fig1.update_layout(xaxis_title="Fecha", yaxis_title=feature, title=f"Exportaciones de CAFÉ en Colombia en {feature}", width=800, height=400)
    return fig1

@st.cache_resource()
def create_line_fig2(df: pd.DataFrame, feature:str):
    
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    
    df['mes'] = df['fecha'].dt.month
    df['año'] = df['fecha'].dt.year

    
    df_grouped = df.groupby(['año', 'mes'])[feature].sum().reset_index()


    fig2 = px.line(df_grouped,
                   x='mes',
                   y=feature,
                   color='año',
                   title=f"Exportaciones de Café - {feature} por Año",
                   width=800,
                   height=400,
                   markers=True,
                   symbol="año")

    
    fig2.update_layout(
        xaxis_title="Mes",
        yaxis_title="Total de KG",
        title=f"Exportaciones de Café - {feature} por Año",
        width=800,
        height=400,
    )

    return fig2



@st.cache_resource()
def choropleth_map(df: pd.DataFrame, feature:str):
    df[feature] = df[feature].apply(lambda x: np.log10(x + 1) if x > 0 else 0)
    
    fig = px.choropleth(df,
                        locations='País de destino',  
                        locationmode='country names',  
                        color=feature,  
                        hover_name='País de destino',  
                        color_continuous_scale=px.colors.sequential.YlOrRd,  
                        range_color=[df[feature].min(), df[feature].max()],  
                        title=f"Exportaciones de Café por País {feature}",
                        width=800,
                        height=600)
    
    
    return fig

@st.cache_resource()
def heatmap(df: pd.DataFrame):
    fig = go.Figure(data=go.Heatmap(
                   z=df.set_index('PAISES').values,
                   x=df.columns[1:],  # Años
                   y=df['PAISES'],     # Países
                   colorscale='Viridis'))

    # Actualizar el layout del gráfico para que sea más cuadrado
    fig.update_layout(
        title='Mapa de Calor de Valores por País y Año',
        xaxis_title='Año',
        yaxis_title='Países',
        width=800,  # Ajusta el ancho
        height=600,  # Ajusta la altura
        margin=dict(l=50, r=50, t=50, b=50)  # Márgenes
    )

    fig.update_xaxes(
        tickvals=df.columns[1:],  # Usa solo los años disponibles
        ticktext=[str(int(year)) for year in df.columns[1:]],  # Asegúrate de mostrar solo años enteros
        tickmode='array'  # Establece el modo de ticks a 'array'
    )

    return  fig
@st.cache_resource()
def area(df: pd.DataFrame):
    fig = px.area(df, x='año', y='Valor', color='PAISES',
              title='Evolución de Valores por País (Área Apilada)',
              width=800, height=400,)
    
    fig.update_xaxes(
        tickvals=df['año'].unique(),  # Usa solo los años disponibles
        ticktext=[str(int(year)) for year in df['año'].unique()],  # Asegúrate de mostrar solo años enteros
        tickmode='array'  # Establece el modo de ticks a 'array'
    )
    
    return fig

def line(df: pd.DataFrame):
    fig = px.line(df, x='año', y='Valor', color='PAISES',
              title='Exportaciones de Café por País de 2000 a 2023',
              width=800,
                   height=400,)
    
    fig.update_xaxes(
        tickvals=df['año'].unique(),  # Usa solo los años disponibles
        ticktext=[str(int(year)) for year in df['año'].unique()],  # Asegúrate de mostrar solo años enteros
        tickmode='array'  # Establece el modo de ticks a 'array'
    )

    return fig